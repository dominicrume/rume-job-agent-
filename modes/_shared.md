# SHARED RULES — ALL MODES
# Loaded automatically by every mode. Do not modify unless updating core logic.

## Pre-Flight Checklist (run before every evaluation)
1. Read `cv.md` — full CV, all proof points
2. Read `config/profile.yml` — profile, voice, north star, gaps
3. Read `data/applications.md` — check if this role or company already exists (dedup)
4. If the role is entry-level, junior, or graduate → STOP. Log as "rejected: seniority mismatch" and do not evaluate.

---

## SCORING RUBRIC

Score each dimension 1.0–5.0:

**1 = Poor / No match**
**2 = Weak match — significant gaps**
**3 = Partial match — addressable gaps**
**4 = Strong match — minor gaps only**
**5 = Near-perfect match**

Weighted final score calculation:
```
score = (cv_match * 0.25) + (north_star * 0.20) + (comp * 0.15) + (remote * 0.10) + (seniority * 0.10) + (trajectory * 0.08) + (culture * 0.05) + (red_flags * 0.05) + (stack * 0.02)
```
*Note: red_flags score = 5 - (severity of flags). Zero red flags = 5.0.*

---

## COVER LETTER RULES

Structure: 3 paragraphs, max 250 words total.

**Paragraph 1 — The Hook (2–3 sentences)**
Lead with a specific proof point from Rume's work that directly maps to the role's primary requirement.
Do not introduce yourself. Do not say "I am writing to apply."
Open mid-thought, as if continuing a conversation.

**Paragraph 2 — The Bridge (3–4 sentences)**
Map 2–3 of Rume's strongest relevant proof points to the JD's top requirements.
Use the JD's exact vocabulary. Rume's words, their frame.
Include a quantifiable outcome where possible.

**Paragraph 3 — The Close (1–2 sentences)**
Forward-looking. What Rume will build or solve in this role.
Confident, not deferential. Not "I hope to hear from you."

**Voice check before output:**
- [ ] No hollow phrases (passionate, excited, love to, hoping)
- [ ] No founder language (founded, CEO, visionary, built from scratch)
- [ ] Opening sentence contains a real proof point
- [ ] JD vocabulary used at least 3 times
- [ ] Under 250 words

---

## BLOCK DEFINITIONS (A–F)

### Block A — Role Summary
| Field | Value |
|-------|-------|
| Title | |
| Company | |
| Location | |
| Remote policy | |
| Salary | |
| Archetype | |
| Seniority | |
| ATS Platform | |
| TL;DR | (1 sentence — what this role is really asking for) |

### Block B — CV Match
For every requirement in the JD:
- Map it to the exact line(s) in `cv.md` that address it
- Mark each as: STRONG / PARTIAL / GAP
- For every GAP: provide a mitigation from `config/profile.yml` → `known_gaps` or reframe existing experience

Format:
```
| JD Requirement | CV Match | Strength | Mitigation |
```

### Block C — Level Strategy
How to position Rume's experience for this specific role:
- Seniority framing (Lead vs Senior IC vs Staff)
- Which experience to lead with (most relevant proof point first)
- How to reframe Vorem Limited as Lead AI/ML Engineer (not Founder)
- Any tenure or recency considerations

### Block D — Compensation Intel
Research the market rate for this role in this location/remote via WebSearch:
- Glassdoor range
- LinkedIn Salary range
- Levels.fyi (if tech company)
- Verdict: below / at / above Rume's floor (£60k)

### Block E — Personalisation Plan
Top 5 CV line changes to better match this JD (reformulation only — no fabrication):
1.
2.
3.
4.
5.

Top 3 LinkedIn profile changes for this application cycle:
1.
2.
3.

### Block F — Interview Prep
Generate 5–8 STAR+Reflection stories mapped to this JD's core competencies.
Format:
```
**Story: [Title]**
Situation: ...
Task: ...
Action: ...
Result: ...
Reflection: (what Rume learned / would do differently)
JD Requirement mapped: ...
```
Add any new stories not already in `interview-prep/story-bank.md` to the story bank.

---

## TRACKER STATUS VALUES

| Status | Meaning |
|--------|---------|
| PIPELINE | URL in inbox, not yet evaluated |
| EVALUATED | Scored, not yet applied |
| APPLIED | Application submitted |
| INTERVIEW_1 | First interview scheduled or completed |
| INTERVIEW_2 | Second interview |
| FINAL | Final round |
| OFFER | Offer received |
| REJECTED | Rejected at any stage |
| WITHDRAWN | Rume withdrew |
| SKIP | Scored < 3.5, skipped |
