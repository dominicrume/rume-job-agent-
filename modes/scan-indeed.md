# MODE: SCAN INDEED
# Command: /career-ops scan
# Purpose: Search Indeed UK for new matching roles, deduplicate, add to pipeline

## What This Mode Does
Searches Indeed UK using Rume's target queries from `config/profile.yml`.
Deduplicates against existing pipeline and applications.
Adds new finds to `data/pipeline.md`.
Returns a summary table of new roles found.

---

## Step 1 — Load Search Config

Read `config/profile.yml` → `indeed_search`:
- `primary_queries` (list of search terms)
- `location_filter`
- `remote_filter`
- `date_posted` (days)
- `salary_min_gbp`
- `exclude_keywords`

---

## Step 2 — Execute Searches

For each query in `primary_queries`, execute a WebSearch:

Query format:
```
site:uk.indeed.com "[query]" [location] remote OR hybrid
```

Example:
```
site:uk.indeed.com "Lead AI Engineer" United Kingdom remote
site:uk.indeed.com "Senior AI ML Engineer" United Kingdom
site:uk.indeed.com "LLMOps Engineer" United Kingdom remote OR hybrid
```

Collect all result URLs and job titles.

---

## Step 3 — Enrich Each Result

For each result URL, extract:
- Job title
- Company name
- Location (remote / hybrid / on-site)
- Salary (if listed)
- Date posted
- ATS platform (Indeed Easy Apply / external link)
- Brief JD summary (2–3 sentences)

---

## Step 4 — Filter & Deduplicate

**Filter out:**
- Roles matching any `exclude_keywords` (junior, graduate, entry level, internship)
- Roles posted > `date_posted` days ago
- Roles with confirmed salary below `salary_min_gbp`
- Roles already in `data/pipeline.md` or `data/applications.md`

---

## Step 5 — Add to Pipeline

Append each new role to `data/pipeline.md`:

```
- [ ] [Date Found] | [Company] | [Title] | [Location/Remote] | [Salary if known] | [URL]
```

---

## Step 6 — Summary Report

Output a table of all new roles added:

```
| # | Company | Title | Location | Salary | Score Preview | URL |
```

For Score Preview: give a rough 1-sentence match assessment (not full evaluation).
Ask Rume: "Run full pipeline evaluation on all [N] new roles? → /career-ops pipeline"

---

## Search Cadence

Recommended: run scan every 3–4 days.
Always record scan date in `data/scan-history.tsv`:
```
[date]\t[query]\t[new_results_count]\t[added_to_pipeline_count]
```
