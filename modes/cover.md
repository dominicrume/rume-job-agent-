# MODE: COVER LETTER
# Command: /career-ops cover [company] [title] OR follow-up after eval
# Purpose: Generate a tailored, voice-compliant cover letter for an evaluated role

## Pre-conditions
- Evaluation report must exist in `reports/` for this role
- If no report exists: run auto-pipeline first

---

## Step 1 — Load Context

Read the evaluation report for this role (Block A–F).
Read `cv.md`.
Read `config/profile.yml` → `voice` section.
Load Block E (personalisation plan) — use the identified proof points.

---

## Step 2 — Identify the 3 Core Match Points

From Block B (CV Match), select the 3 requirements with the strongest STRONG ratings.
These become the spine of the cover letter.

---

## Step 3 — Generate Cover Letter

**Format: 3 paragraphs, max 250 words**

### Paragraph 1 — The Hook
- Open with Rume's single strongest proof point mapped to this JD's #1 requirement
- Do NOT start with "I" or "My name is" or "I am writing to apply"
- Do NOT use hollow openers
- Example structure: "[Concrete proof point] — [connect directly to what this company needs]."

### Paragraph 2 — The Bridge
- Map 2 more proof points to JD requirements using the JD's own language
- Include at least one quantifiable outcome (performance score, system deployed, scale achieved)
- Keep sentences tight and declarative

### Paragraph 3 — The Close
- 1–2 sentences max
- Forward-looking: what Rume will build or solve in this role specifically
- Confident, not deferential
- Never: "I look forward to hearing from you" / "I hope to be considered"

---

## Step 4 — Voice Check

Before outputting:
- [ ] No hollow phrases
- [ ] No founder language
- [ ] Opens with a concrete proof point
- [ ] JD vocabulary appears ≥ 3 times
- [ ] Under 250 words
- [ ] Tone: authoritative, calm, innovative, edgy — not eager

---

## Step 5 — Output

Output the cover letter as clean, ready-to-paste text.
Then ask: "Ready to apply? I'll update the tracker to APPLIED when confirmed."
