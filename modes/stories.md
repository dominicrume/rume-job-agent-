# MODE: STORY BANK
# Command: /career-ops stories
# Purpose: Add, retrieve, and manage STAR+Reflection interview stories

## STAR+R Format

Every story must follow this exact format:

```
## [Story Title — short, memorable]
**Archetype(s):** [which role archetypes this story serves]
**Competencies:** [leadership / technical depth / stakeholder management / delivery / innovation / etc.]
**JD Keywords:** [terms from JDs this story addresses]

**Situation:** [Context — 2–3 sentences. What was the environment? What was the challenge?]

**Task:** [What was Rume's specific responsibility? What was expected of him?]

**Action:** [What did Rume specifically do? Be concrete — tools, decisions, trade-offs made.]

**Result:** [Quantifiable outcome where possible. What changed? What was delivered?]

**Reflection:** [What did Rume learn? What would he do differently? Shows maturity.]
```

---

## Commands

### Add a story
`/career-ops stories add` — Rume describes an experience, agent formats it into STAR+R and appends to `interview-prep/story-bank.md`

### Find a story for a role
`/career-ops stories find [JD requirement or keyword]` — search story bank for matching stories

### Generate stories for a role
`/career-ops stories generate [company] [title]` — pull the eval report, identify top competencies, surface the best 5 stories from the bank

### Review all stories
`/career-ops stories list` — display all stories with their archetype and competency tags
