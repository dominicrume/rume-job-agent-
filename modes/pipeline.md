# MODE: PIPELINE
# Command: /career-ops pipeline
# Purpose: Process all pending URLs in data/pipeline.md

## What This Mode Does
Reads `data/pipeline.md`, evaluates each unchecked item using auto-pipeline logic,
and produces a ranked summary table to help Rume decide where to focus.

---

## Step 1 — Read Pipeline

Open `data/pipeline.md`.
Identify all items marked `- [ ]` (not yet evaluated).
If pipeline is empty: report "Pipeline is clear." and stop.

---

## Step 2 — Evaluate Each Item

For each pending URL:
1. Run Steps 1–3 of `modes/auto-pipeline.md` (fetch JD + full A–F evaluation)
2. Calculate score
3. Mark item as `- [x]` in pipeline

For 3+ pending items: run evaluations in order, but report all results together at the end.

---

## Step 3 — Ranked Summary

Output a ranked table (highest score first):

```
| Rank | Score | Company | Title | Verdict | URL |
|------|-------|---------|-------|---------|-----|
| 1    | 4.7   | ...     | ...   | APPLY IMMEDIATELY | ... |
| 2    | 4.1   | ...     | ...   | APPLY | ... |
| 3    | 3.4   | ...     | ...   | SKIP | ... |
```

---

## Step 4 — Action Prompt

For all APPLY IMMEDIATELY and APPLY roles:
"Generate cover letters for the top [N] roles? → yes / [specify which ones]"

For all SKIP roles:
Update `data/applications.md` with status SKIP and reason.
