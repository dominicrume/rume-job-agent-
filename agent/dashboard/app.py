"""
Rume Dominic — Job Search Agent Dashboard v2
Flask Human-in-the-Loop Control Centre
Runs on: http://localhost:5050
"""

import sqlite3, json, os
from pathlib import Path
from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "rume-dominic-agent-2026")
DB_PATH = Path(__file__).parent.parent / "db" / "submission_log.db"


# ── DB helpers ─────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query(sql, params=()):
    conn = get_db()
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows

def execute(sql, params=()):
    conn = get_db()
    conn.execute(sql, params)
    conn.commit()
    conn.close()

def now():
    return datetime.now(timezone.utc).isoformat()


# ── API ────────────────────────────────────────────────────────────────────

@app.get("/api/applications")
def get_applications():
    rows = query("SELECT * FROM applications ORDER BY match_score DESC")
    for r in rows:
        try:
            r["gap_keywords"] = json.loads(r.get("gap_keywords") or "[]")
        except Exception:
            r["gap_keywords"] = []
    return jsonify(rows)

@app.get("/api/stats")
def get_stats():
    apps = query("SELECT status, match_score, submitted, follow_up_sent FROM applications")
    total = len(apps)
    scores = [a["match_score"] or 0 for a in apps]
    return jsonify({
        "total": total,
        "shortlisted": sum(1 for a in apps if a["status"] == "shortlisted"),
        "review": sum(1 for a in apps if a["status"] == "review"),
        "applied": sum(1 for a in apps if a["submitted"]),
        "follow_ups": sum(1 for a in apps if a["follow_up_sent"]),
        "avg_match": round(sum(scores) / total, 1) if total else 0,
    })

@app.post("/api/approve")
def approve():
    data = request.get_json(force=True)
    app_id  = data.get("application_id")
    ev_type = data.get("event_type", "cover_letter_approved")
    if not app_id:
        return jsonify({"error": "application_id required"}), 400

    execute(
        "INSERT INTO approval_events (application_id, event_type, approved, approved_at) VALUES (?,?,1,?)",
        (app_id, ev_type, now()),
    )
    new_status = "approved_for_submission" if ev_type == "submission_approved" else "approved"
    execute(
        "UPDATE applications SET status=?, updated_at=? WHERE id=?",
        (new_status, now(), app_id),
    )
    return jsonify({"ok": True, "application_id": app_id, "status": new_status})

@app.post("/api/reject")
def reject():
    data = request.get_json(force=True)
    app_id = data.get("application_id")
    reason = data.get("reason", "")
    if not app_id:
        return jsonify({"error": "application_id required"}), 400

    execute(
        "INSERT INTO approval_events (application_id, event_type, approved, rejected_reason) VALUES (?,?,0,?)",
        (app_id, "rejected", reason),
    )
    execute(
        "UPDATE applications SET status='rejected', updated_at=? WHERE id=?",
        (now(), app_id),
    )
    return jsonify({"ok": True, "application_id": app_id, "status": "rejected"})

@app.post("/api/status")
def update_status():
    data = request.get_json(force=True)
    execute(
        "UPDATE applications SET status=?, updated_at=? WHERE id=?",
        (data["status"], now(), data["application_id"]),
    )
    return jsonify({"ok": True})

@app.post("/api/mark-submitted")
def mark_submitted():
    data = request.get_json(force=True)
    execute(
        "UPDATE applications SET submitted=1, submitted_at=?, status='applied', updated_at=? WHERE id=?",
        (now(), now(), data["application_id"]),
    )
    return jsonify({"ok": True})

@app.get("/api/follow-ups")
def get_follow_ups():
    rows = query(
        "SELECT * FROM applications WHERE follow_up_drafted=1 AND follow_up_sent=0 ORDER BY submitted_at ASC"
    )
    return jsonify(rows)

@app.post("/api/approve-followup")
def approve_followup():
    data = request.get_json(force=True)
    app_id = data["application_id"]
    execute(
        "UPDATE applications SET follow_up_sent=1, follow_up_sent_at=?, updated_at=? WHERE id=?",
        (now(), now(), app_id),
    )
    return jsonify({"ok": True})

@app.get("/api/application/<int:app_id>")
def get_application(app_id):
    rows = query("SELECT * FROM applications WHERE id=?", (app_id,))
    if not rows:
        return jsonify({"error": "not found"}), 404
    r = rows[0]
    try:
        r["gap_keywords"] = json.loads(r.get("gap_keywords") or "[]")
    except Exception:
        r["gap_keywords"] = []
    return jsonify(r)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "agent": "Rume Dominic Job Search Agent v2", "db": str(DB_PATH)})


# ── Dashboard UI ───────────────────────────────────────────────────────────

DASHBOARD = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Rume Dominic — Job Agent</title>
<style>
:root{
  --bg:#0a0c12;--surf:#13161f;--surf2:#1a1e2e;--surf3:#212640;
  --border:#252a3d;--accent:#4f8ef7;--purple:#7c3aed;--green:#22c55e;
  --yellow:#f59e0b;--red:#ef4444;--pink:#ec4899;--text:#e2e8f0;--muted:#64748b;
  --r:10px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Inter',system-ui,sans-serif;min-height:100vh}

/* ── NAV ── */
nav{
  background:var(--surf);border-bottom:1px solid var(--border);
  padding:0 32px;display:flex;align-items:center;height:56px;gap:8px;
  position:sticky;top:0;z-index:50;
}
.logo{font-weight:800;font-size:1rem;color:var(--accent);margin-right:auto}
.logo span{color:var(--muted);font-weight:400;font-size:.8rem;margin-left:8px}
.nav-tab{
  padding:6px 16px;border-radius:6px;font-size:.78rem;font-weight:600;
  cursor:pointer;border:none;background:transparent;color:var(--muted);
  transition:all .15s;
}
.nav-tab:hover{color:var(--text);background:var(--surf2)}
.nav-tab.active{background:var(--accent);color:#fff}
.hitl-badge{
  background:linear-gradient(135deg,var(--purple),var(--accent));
  color:#fff;font-size:.65rem;font-weight:700;padding:3px 10px;
  border-radius:20px;letter-spacing:.05em;margin-left:8px;
}

/* ── VIEWS ── */
.view{display:none;padding:28px 32px}
.view.active{display:block}

/* ── STATS ── */
.stats{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-bottom:28px}
.stat{
  background:var(--surf);border:1px solid var(--border);border-radius:var(--r);
  padding:16px 18px;text-align:center;
}
.stat .n{font-size:1.9rem;font-weight:800}
.stat .l{font-size:.68rem;color:var(--muted);margin-top:3px;text-transform:uppercase;letter-spacing:.07em}

/* ── FILTERS ── */
.toolbar{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap;align-items:center}
.fbtn{
  background:var(--surf2);border:1px solid var(--border);color:var(--muted);
  padding:5px 14px;border-radius:20px;font-size:.75rem;cursor:pointer;transition:all .15s;
}
.fbtn:hover,.fbtn.on{background:var(--accent);border-color:var(--accent);color:#fff}
.search{
  margin-left:auto;background:var(--surf2);border:1px solid var(--border);
  color:var(--text);padding:6px 14px;border-radius:20px;font-size:.78rem;
  width:200px;outline:none;
}
.search:focus{border-color:var(--accent)}

/* ── CARDS GRID ── */
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}
.card{
  background:var(--surf);border:1px solid var(--border);border-radius:var(--r);
  padding:20px;transition:border-color .15s,box-shadow .15s;cursor:pointer;
}
.card:hover{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)22}
.card-top{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}
.card-icon{
  width:42px;height:42px;border-radius:8px;display:flex;align-items:center;
  justify-content:center;font-size:1.2rem;flex-shrink:0;
  background:linear-gradient(135deg,var(--surf2),var(--surf3));
}
.card-title{font-size:.92rem;font-weight:700;margin-bottom:2px}
.card-company{font-size:.78rem;color:var(--muted)}
.card-meta{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.tag{display:inline-flex;align-items:center;gap:4px;font-size:.65rem;font-weight:600;
  padding:3px 9px;border-radius:10px;text-transform:uppercase;letter-spacing:.04em}
.t-short{background:rgba(79,142,247,.12);color:#7dd3fc;border:1px solid rgba(79,142,247,.2)}
.t-approved{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.2)}
.t-applied{background:rgba(34,197,94,.2);color:#4ade80;border:1px solid rgba(34,197,94,.3)}
.t-review{background:rgba(245,158,11,.12);color:#fbbf24;border:1px solid rgba(245,158,11,.2)}
.t-rejected{background:rgba(239,68,68,.12);color:#f87171;border:1px solid rgba(239,68,68,.2)}
.t-high{background:rgba(239,68,68,.1);color:#f87171}
.t-medium{background:rgba(245,158,11,.1);color:#fbbf24}
.t-low{background:rgba(100,116,139,.1);color:var(--muted)}
.t-loc{background:var(--surf2);color:var(--muted)}
.t-cl{background:rgba(168,85,247,.1);color:#c084fc;border:1px solid rgba(168,85,247,.2)}

/* ── SCORE BAR ── */
.score-row{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.score-label{font-size:.7rem;color:var(--muted);width:40px}
.bar-track{flex:1;height:7px;background:var(--surf3);border-radius:4px;overflow:hidden}
.bar-fill{height:100%;border-radius:4px;transition:width .4s ease}
.score-num{font-size:.82rem;font-weight:800;width:32px;text-align:right}

/* ── CARD FOOTER ── */
.card-footer{display:flex;gap:8px;flex-wrap:wrap}
.btn{
  flex:1;min-width:80px;padding:8px 12px;border-radius:7px;border:none;
  font-size:.75rem;font-weight:700;cursor:pointer;transition:all .15s;
  display:flex;align-items:center;justify-content:center;gap:5px;
}
.btn-approve{background:var(--green);color:#000}
.btn-approve:hover{background:#16a34a}
.btn-reject{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.3)}
.btn-reject:hover{background:var(--red);color:#fff}
.btn-apply{background:linear-gradient(135deg,var(--accent),var(--purple));color:#fff}
.btn-apply:hover{opacity:.85}
.btn-view{background:var(--surf2);color:var(--muted);border:1px solid var(--border)}
.btn-view:hover{border-color:var(--accent);color:var(--accent)}
.btn-submitted{background:rgba(34,197,94,.1);color:var(--green);border:1px solid rgba(34,197,94,.2)}
.btn-submitted:hover{background:var(--green);color:#000}

/* ── MODAL ── */
.overlay{
  display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);
  z-index:200;align-items:center;justify-content:center;padding:20px;
}
.overlay.open{display:flex}
.modal{
  background:var(--surf);border:1px solid var(--border);border-radius:14px;
  width:640px;max-width:100%;max-height:90vh;overflow-y:auto;
}
.modal-header{
  padding:22px 24px 0;display:flex;align-items:flex-start;
  justify-content:space-between;border-bottom:1px solid var(--border);
  padding-bottom:16px;position:sticky;top:0;background:var(--surf);z-index:1;
}
.modal-header h2{font-size:1rem;font-weight:700}
.modal-header p{font-size:.78rem;color:var(--muted);margin-top:3px}
.close-btn{
  background:var(--surf2);border:1px solid var(--border);color:var(--muted);
  width:30px;height:30px;border-radius:6px;cursor:pointer;font-size:1rem;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.close-btn:hover{border-color:var(--red);color:var(--red)}
.modal-body{padding:20px 24px}
.field-group{margin-bottom:16px}
.field-group label{font-size:.72rem;color:var(--muted);display:block;margin-bottom:5px;font-weight:600;text-transform:uppercase;letter-spacing:.05em}
.field-group select,.field-group textarea,.field-group input{
  width:100%;background:var(--surf2);border:1px solid var(--border);
  color:var(--text);padding:9px 12px;border-radius:7px;font-size:.82rem;outline:none;
}
.field-group select:focus,.field-group textarea:focus{border-color:var(--accent)}
.field-group textarea{height:140px;resize:vertical;line-height:1.6}
.cl-box{
  background:var(--surf2);border:1px solid var(--border);border-radius:7px;
  padding:14px;font-size:.8rem;line-height:1.7;color:var(--text);
  white-space:pre-wrap;max-height:220px;overflow-y:auto;
}
.cl-empty{color:var(--muted);font-style:italic;text-align:center;padding:20px}
.modal-footer{
  padding:16px 24px;border-top:1px solid var(--border);
  display:flex;gap:8px;justify-content:flex-end;
  position:sticky;bottom:0;background:var(--surf);
}

/* ── TOAST ── */
.toast{
  position:fixed;bottom:24px;right:24px;
  background:var(--surf);border:1px solid var(--border);border-radius:8px;
  padding:12px 18px;font-size:.8rem;font-weight:600;z-index:500;
  transform:translateY(80px);opacity:0;transition:all .3s;
  display:flex;align-items:center;gap:8px;
}
.toast.show{transform:translateY(0);opacity:1}
.toast.success{border-color:var(--green);color:var(--green)}
.toast.error{border-color:var(--red);color:var(--red)}

/* ── EMPTY STATE ── */
.empty{text-align:center;padding:60px 20px;color:var(--muted)}
.empty .ico{font-size:2.5rem;margin-bottom:12px}

/* ── FOLLOW-UPS VIEW ── */
.fu-card{
  background:var(--surf);border:1px solid var(--border);border-radius:var(--r);
  padding:20px;margin-bottom:14px;
}
.fu-card h3{font-size:.9rem;font-weight:700;margin-bottom:4px}
.fu-card .sub{font-size:.75rem;color:var(--muted);margin-bottom:14px}
.msg-box{
  background:var(--surf2);border:1px solid var(--border);border-radius:7px;
  padding:12px;font-size:.78rem;line-height:1.6;margin-bottom:8px;
}
.msg-label{font-size:.65rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px}

/* ── PIPELINE VIEW ── */
.pipeline{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;align-items:start}
.pipe-col{background:var(--surf);border:1px solid var(--border);border-radius:var(--r);padding:14px}
.pipe-col h4{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:12px;display:flex;align-items:center;gap:6px}
.pipe-card{background:var(--surf2);border:1px solid var(--border);border-radius:7px;padding:10px;margin-bottom:8px;font-size:.75rem}
.pipe-card .r{font-weight:700;margin-bottom:2px}
.pipe-card .c{color:var(--muted)}
</style>
</head>
<body>

<nav>
  <div class="logo">Rume Dominic — Job Agent <span>orumedominic@gmail.com</span></div>
  <button class="nav-tab active" onclick="showView('applications',this)">Applications</button>
  <button class="nav-tab" onclick="showView('pipeline',this)">Pipeline</button>
  <button class="nav-tab" onclick="showView('followups',this)">Follow-ups</button>
  <span class="hitl-badge">HUMAN-IN-THE-LOOP</span>
</nav>

<!-- ── APPLICATIONS VIEW ── -->
<div class="view active" id="view-applications">
  <div class="stats" id="stats-row"></div>
  <div class="toolbar">
    <button class="fbtn on" onclick="filterBy('all',this)">All</button>
    <button class="fbtn" onclick="filterBy('shortlisted',this)">Shortlisted</button>
    <button class="fbtn" onclick="filterBy('review',this)">Review</button>
    <button class="fbtn" onclick="filterBy('approved',this)">Approved</button>
    <button class="fbtn" onclick="filterBy('applied',this)">Applied</button>
    <button class="fbtn" onclick="filterBy('rejected',this)">Rejected</button>
    <input class="search" type="text" placeholder="Search role, company…" oninput="filterSearch(this.value)"/>
  </div>
  <div class="cards" id="cards-grid"></div>
</div>

<!-- ── PIPELINE VIEW ── -->
<div class="view" id="view-pipeline">
  <div class="pipeline" id="pipeline-board"></div>
</div>

<!-- ── FOLLOW-UPS VIEW ── -->
<div class="view" id="view-followups">
  <div id="followups-list"></div>
</div>

<!-- ── DETAIL MODAL ── -->
<div class="overlay" id="modal" onclick="if(event.target===this)closeModal()">
  <div class="modal">
    <div class="modal-header">
      <div>
        <h2 id="m-title">Role</h2>
        <p id="m-sub">Company · Location</p>
      </div>
      <button class="close-btn" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="field-group">
        <label>Status</label>
        <select id="m-status">
          <option value="shortlisted">Shortlisted</option>
          <option value="review">Under Review</option>
          <option value="approved">Approved</option>
          <option value="approved_for_submission">Approved for Submission</option>
          <option value="applied">Applied</option>
          <option value="interview">Interview</option>
          <option value="offer">Offer</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>
      <div class="field-group">
        <label>Cover Letter</label>
        <div class="cl-box" id="m-cl-text"></div>
      </div>
      <div class="field-group">
        <label>Gap Keywords</label>
        <div id="m-gaps"></div>
      </div>
      <div class="field-group">
        <label>Notes</label>
        <textarea id="m-notes" placeholder="Add notes…"></textarea>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-reject" style="flex:0;min-width:100px" onclick="rejectCurrent()">✕ Reject</button>
      <button class="btn btn-view" style="flex:0;min-width:100px" onclick="saveStatus()">Save</button>
      <button class="btn btn-approve" style="flex:0;min-width:120px" onclick="approveCurrent()">✓ Approve</button>
    </div>
  </div>
</div>

<!-- ── TOAST ── -->
<div class="toast" id="toast"></div>

<script>
let allApps = [];
let currentFilter = 'all';
let currentSearch = '';
let modalId = null;

// ── Score colour ──────────────────────────────────────────────────────────
const scoreCol = s => s>=75?'#22c55e':s>=60?'#f59e0b':'#ef4444';

// ── Status tag class ──────────────────────────────────────────────────────
const stCls = s => ({
  shortlisted:'t-short', review:'t-review', approved:'t-approved',
  approved_for_submission:'t-approved', applied:'t-applied', rejected:'t-rejected',
  interview:'t-approved', offer:'t-approved'
}[s] || 't-review');

const stLabel = s => ({
  shortlisted:'Shortlisted', review:'Review', approved:'Approved ✓',
  approved_for_submission:'Ready to Apply', applied:'Applied ✓',
  rejected:'Rejected', interview:'Interview 🎉', offer:'Offer 🏆'
}[s] || s);

// ── Flag helper ───────────────────────────────────────────────────────────
const flag = loc => {
  if(!loc) return '🌍';
  const l = loc.toLowerCase();
  if(l.includes('uk')||l.includes('england')||l.includes('london')||l.includes('birmingham')) return '🇬🇧';
  if(l.includes('ireland')||l.includes('dublin')) return '🇮🇪';
  if(l.includes('germany')||l.includes('berlin')) return '🇩🇪';
  if(l.includes('norway')||l.includes('oslo')) return '🇳🇴';
  if(l.includes('australia')||l.includes('brisbane')) return '🇦🇺';
  if(l.includes('usa')||l.includes('york')||l.includes('francisco')) return '🇺🇸';
  if(l.includes('canada')||l.includes('toronto')) return '🇨🇦';
  if(l.includes('amsterdam')||l.includes('netherlands')) return '🇳🇱';
  return '🌍';
};

// ── Toast ──────────────────────────────────────────────────────────────────
function toast(msg, type='success') {
  const t = document.getElementById('toast');
  t.textContent = (type==='success'?'✓ ':'✕ ') + msg;
  t.className = `toast ${type} show`;
  setTimeout(()=>t.classList.remove('show'), 3000);
}

// ── API calls ──────────────────────────────────────────────────────────────
async function api(path, body=null) {
  const opts = body
    ? {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)}
    : {method:'GET'};
  const r = await fetch(path, opts);
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}

// ── Load all data ─────────────────────────────────────────────────────────
async function loadAll() {
  try {
    const [apps, stats] = await Promise.all([
      api('/api/applications'),
      api('/api/stats'),
    ]);
    allApps = apps;
    renderStats(stats);
    renderCards();
    renderPipeline();
  } catch(e) {
    toast('Failed to load: '+e.message, 'error');
  }
}

// ── Stats ─────────────────────────────────────────────────────────────────
function renderStats(s) {
  document.getElementById('stats-row').innerHTML = `
    <div class="stat"><div class="n" style="color:var(--accent)">${s.total}</div><div class="l">Total Roles</div></div>
    <div class="stat"><div class="n" style="color:var(--yellow)">${s.shortlisted}</div><div class="l">Shortlisted</div></div>
    <div class="stat"><div class="n" style="color:var(--muted)">${s.review}</div><div class="l">In Review</div></div>
    <div class="stat"><div class="n" style="color:var(--green)">${s.applied}</div><div class="l">Applied</div></div>
    <div class="stat"><div class="n" style="color:var(--purple)">${s.follow_ups}</div><div class="l">Follow-ups</div></div>
    <div class="stat"><div class="n" style="color:var(--pink)">${s.avg_match}%</div><div class="l">Avg Match</div></div>
  `;
}

// ── Cards ─────────────────────────────────────────────────────────────────
function renderCards() {
  const grid = document.getElementById('cards-grid');
  const apps = allApps.filter(a => {
    const mf = currentFilter==='all' || a.status===currentFilter;
    const q = currentSearch.toLowerCase();
    const ms = !q || (a.role||'').toLowerCase().includes(q)
                  || (a.company||'').toLowerCase().includes(q)
                  || (a.location||'').toLowerCase().includes(q);
    return mf && ms;
  });

  if(!apps.length) {
    grid.innerHTML = '<div class="empty" style="grid-column:1/-1"><div class="ico">🔍</div><p>No applications match this filter.</p></div>';
    return;
  }

  grid.innerHTML = apps.map(a => {
    const sc = a.match_score||0;
    const col = scoreCol(sc);
    const gaps = (a.gap_keywords||[]).slice(0,3);
    const hasCL = a.cover_letter_text && a.cover_letter_text.length > 10;
    const isApplied = a.submitted;

    return `
    <div class="card" onclick="openModal(${a.id})">
      <div class="card-top">
        <div class="card-icon">${flag(a.location)}</div>
        <div style="flex:1;min-width:0">
          <div class="card-title">${a.role||'—'}</div>
          <div class="card-company">${a.company||'—'} · <span style="color:var(--muted)">${(a.compensation||'Comp N/A')}</span></div>
        </div>
      </div>

      <div class="card-meta">
        <span class="tag ${stCls(a.status)}">${stLabel(a.status)}</span>
        <span class="tag ${a.priority==='high'?'t-high':a.priority==='medium'?'t-medium':'t-low'}">${(a.priority||'medium').toUpperCase()}</span>
        <span class="tag t-loc">📍 ${a.location||'Remote'}</span>
        ${hasCL?'<span class="tag t-cl">✍ CL Ready</span>':''}
      </div>

      <div class="score-row">
        <div class="score-label">Match</div>
        <div class="bar-track"><div class="bar-fill" style="width:${sc}%;background:${col}"></div></div>
        <div class="score-num" style="color:${col}">${sc}</div>
      </div>

      ${gaps.length?`<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:14px">
        ${gaps.map(g=>`<span style="background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.25);color:#a78bfa;font-size:.62rem;padding:2px 7px;border-radius:4px">${g}</span>`).join('')}
      </div>`:'<div style="margin-bottom:14px"></div>'}

      <div class="card-footer" onclick="event.stopPropagation()">
        ${isApplied
          ? `<button class="btn btn-submitted" disabled>✓ Submitted</button>`
          : `<button class="btn btn-approve" onclick="quickApprove(${a.id},event)">✓ Approve</button>
             <button class="btn btn-reject" onclick="quickReject(${a.id},event)">✕ Reject</button>`
        }
        ${a.url?`<a href="${a.url}" target="_blank" onclick="event.stopPropagation()">
          <button class="btn btn-apply">→ Apply</button></a>`:''}
      </div>
    </div>`;
  }).join('');
}

// ── Pipeline board ────────────────────────────────────────────────────────
function renderPipeline() {
  const cols = [
    {key:'shortlisted', label:'Shortlisted', color:'var(--accent)'},
    {key:'review',      label:'In Review',   color:'var(--yellow)'},
    {key:'approved',    label:'Approved',    color:'var(--purple)'},
    {key:'applied',     label:'Applied',     color:'var(--green)'},
    {key:'interview',   label:'Interview',   color:'var(--pink)'},
  ];
  const board = document.getElementById('pipeline-board');
  board.innerHTML = cols.map(col => {
    const items = allApps.filter(a => a.status===col.key || (col.key==='applied'&&a.submitted&&a.status==='applied'));
    return `<div class="pipe-col">
      <h4><span style="width:8px;height:8px;border-radius:50%;background:${col.color};display:inline-block"></span>${col.label} <span style="margin-left:auto;color:${col.color}">${items.length}</span></h4>
      ${items.length
        ? items.map(a=>`<div class="pipe-card" onclick="openModal(${a.id})" style="cursor:pointer">
            <div class="r">${a.role}</div>
            <div class="c">${a.company}</div>
            <div style="margin-top:5px;font-size:.68rem;color:${scoreColor(a.match_score||0)};font-weight:700">${a.match_score||0}/100</div>
          </div>`).join('')
        : `<div style="font-size:.72rem;color:var(--muted);text-align:center;padding:12px">Empty</div>`
      }
    </div>`;
  }).join('');
}
function scoreColor(s){return s>=75?'#22c55e':s>=60?'#f59e0b':'#ef4444'}

// ── Follow-ups ────────────────────────────────────────────────────────────
async function renderFollowUps() {
  try {
    const fus = await api('/api/follow-ups');
    const el = document.getElementById('followups-list');
    if(!fus.length) {
      el.innerHTML = '<div class="empty"><div class="ico">📬</div><p>No follow-ups ready yet.<br><span style="font-size:.75rem">Follow-ups appear 48h after a successful submission.</span></p></div>';
      return;
    }
    el.innerHTML = fus.map(f=>`
      <div class="fu-card">
        <h3>${f.role} @ ${f.company}</h3>
        <div class="sub">${f.location} · Submitted: ${f.submitted_at||'—'}</div>
        ${f.follow_up_connection_note?`<div class="msg-label">LinkedIn Connection Note (≤300 chars)</div>
          <div class="msg-box">${f.follow_up_connection_note}</div>`:''}
        ${f.follow_up_inmail?`<div class="msg-label">LinkedIn InMail (~80 words)</div>
          <div class="msg-box">${f.follow_up_inmail}</div>`:''}
        <div style="display:flex;gap:8px;margin-top:12px">
          <button class="btn btn-approve" style="flex:0;padding:7px 18px" onclick="approveFollowUp(${f.id})">✓ Send Approved</button>
          <button class="btn btn-view" style="flex:0;padding:7px 18px">Copy InMail</button>
        </div>
      </div>`).join('');
  } catch(e) {
    toast('Error loading follow-ups: '+e.message,'error');
  }
}

async function approveFollowUp(id) {
  await api('/api/approve-followup',{application_id:id});
  toast('Follow-up marked as sent');
  renderFollowUps();
}

// ── Quick actions (card buttons) ──────────────────────────────────────────
async function quickApprove(id, e) {
  e.stopPropagation();
  try {
    await api('/api/approve',{application_id:id, event_type:'cover_letter_approved'});
    toast('Approved ✓');
    await loadAll();
  } catch(err) { toast(err.message,'error'); }
}

async function quickReject(id, e) {
  e.stopPropagation();
  const reason = prompt('Reason for rejection (optional):') || '';
  try {
    await api('/api/reject',{application_id:id, reason});
    toast('Rejected');
    await loadAll();
  } catch(err) { toast(err.message,'error'); }
}

// ── Modal ──────────────────────────────────────────────────────────────────
function openModal(id) {
  const a = allApps.find(x=>x.id===id);
  if(!a) return;
  modalId = id;

  document.getElementById('m-title').textContent = a.role;
  document.getElementById('m-sub').textContent   = `${a.company} · ${a.location||'—'} · ${a.compensation||'Comp N/A'}`;
  document.getElementById('m-status').value       = a.status||'shortlisted';
  document.getElementById('m-notes').value        = a.notes||'';

  const clEl = document.getElementById('m-cl-text');
  clEl.innerHTML = a.cover_letter_text
    ? a.cover_letter_text
    : '<div class="cl-empty">No cover letter drafted yet.<br>Ask Claude to draft one in the chat.</div>';

  const gaps = a.gap_keywords||[];
  document.getElementById('m-gaps').innerHTML = gaps.length
    ? gaps.map(g=>`<span style="background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.25);color:#a78bfa;font-size:.72rem;padding:3px 9px;border-radius:5px;margin:2px;display:inline-block">${g}</span>`).join('')
    : '<span style="color:var(--muted);font-size:.75rem">No gaps identified</span>';

  document.getElementById('modal').classList.add('open');
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
  modalId = null;
}

async function approveCurrent() {
  if(!modalId) return;
  await saveStatus();
  try {
    await api('/api/approve',{application_id:modalId, event_type:'cover_letter_approved'});
    toast('Approved ✓');
    closeModal();
    await loadAll();
  } catch(e) { toast(e.message,'error'); }
}

async function rejectCurrent() {
  if(!modalId) return;
  const reason = prompt('Reason for rejection (optional):') || '';
  try {
    await api('/api/reject',{application_id:modalId, reason});
    toast('Rejected');
    closeModal();
    await loadAll();
  } catch(e) { toast(e.message,'error'); }
}

async function saveStatus() {
  if(!modalId) return;
  const status = document.getElementById('m-status').value;
  const notes  = document.getElementById('m-notes').value;
  try {
    await api('/api/status',{application_id:modalId, status});
    const a = allApps.find(x=>x.id===modalId);
    if(a){ a.status=status; a.notes=notes; }
    toast('Saved');
  } catch(e) { toast(e.message,'error'); }
}

// ── View switching ────────────────────────────────────────────────────────
function showView(name, btn) {
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(b=>b.classList.remove('active'));
  document.getElementById('view-'+name).classList.add('active');
  btn.classList.add('active');
  if(name==='followups') renderFollowUps();
}

// ── Filters ───────────────────────────────────────────────────────────────
function filterBy(f, btn) {
  currentFilter = f;
  document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  renderCards();
}
function filterSearch(q) {
  currentSearch = q;
  renderCards();
}

// ── Boot ──────────────────────────────────────────────────────────────────
loadAll();
setInterval(loadAll, 30000); // auto-refresh every 30s
</script>
</body>
</html>"""


@app.get("/")
def dashboard():
    return render_template_string(DASHBOARD)


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5050))
    print(f"\n🚀 Dashboard → http://localhost:{port}")
    print(f"   Health  → http://localhost:{port}/health")
    print(f"   API     → http://localhost:{port}/api/applications\n")
    app.run(debug=False, port=port, host="0.0.0.0")
