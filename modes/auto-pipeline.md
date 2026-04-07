# MODE: AUTO-PIPELINE
# Trigger: User pastes an Indeed URL, any job URL, or raw JD text
# This is the default mode — runs automatically on any job input

## What This Mode Does
1. Detects input type (URL vs raw text)
2. Fetches JD if URL provided (WebFetch → WebSearch fallback)
3. Runs full 6-block A–F evaluation
4. Generates tailored cover letter
5. Updates `data/applications.md` tracker
6. Saves evaluation report to `reports/`

---

## Step 1 — Input Detection

If input contains a URL:
- Attempt WebFetch on the URL
- If WebFetch fails: use WebSearch to find the job posting text
- Extract: title, company, location, salary, remote policy, full JD text

If input is raw JD text:
- Parse directly — extract all requirements, responsibilities, and must-haves

---

## Step 2 — Pre-Flight

Load `modes/_shared.md` Pre-Flight Checklist.
Check `data/applications.md` for duplicates.
If duplicate found: report status and stop.
If entry-level/junior/graduate: log SKIP and stop.

---

## Step 3 — Full Evaluation (Blocks A–F)

Run all 6 blocks from `modes/_shared.md` Block Definitions.
Calculate weighted score.
Print evaluation with clear visual score:

```
╔══════════════════════════════════════╗
║  SCORE: 4.2/5.0  →  APPLY           ║
╚══════════════════════════════════════╝
```

Decision verdict must be one of:
- APPLY IMMEDIATELY (4.5+)
- APPLY (4.0–4.4)
- APPLY WITH REASON (3.5–3.9) — state the reason
- SKIP (< 3.5)

---

## Step 4 — Cover Letter

If verdict is APPLY IMMEDIATELY or APPLY:
Generate cover letter per `modes/_shared.md` Cover Letter Rules.
Output ready-to-paste text.

If verdict is APPLY WITH REASON:
Ask Rume: "Score is 3.5–3.9. Reason to apply: [state reason]. Shall I generate the cover letter?"

---

## Step 5 — Tracker Update

Append to `data/applications.md`:

```
| [Date] | [Company] | [Title] | [Score] | [Status] | [URL] | [Notes] |
```

Status = EVALUATED (or APPLIED if Rume confirms submission).

---

## Step 6 — Save Report

Save full A–F evaluation to `reports/YYYY-MM-DD_[company]_[title].md`
