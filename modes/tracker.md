# MODE: TRACKER
# Command: /career-ops tracker
# Purpose: View, update, and manage the applications tracker

## Commands

### View full tracker
`/career-ops tracker` — display `data/applications.md` formatted as a table

### Update status
`/career-ops tracker update [company] [new_status]`
Valid statuses (from `modes/_shared.md`):
PIPELINE / EVALUATED / APPLIED / INTERVIEW_1 / INTERVIEW_2 / FINAL / OFFER / REJECTED / WITHDRAWN / SKIP

### Add note
`/career-ops tracker note [company] [note text]`

### Show stats
`/career-ops tracker stats` — output:
- Total in pipeline
- Total evaluated
- Total applied
- Interview rate (interviews / applied)
- Active roles (not rejected/withdrawn/skip)

---

## Tracker Format

`data/applications.md` is the master tracker. Format:

```markdown
| Date Added | Company | Title | Score | Status | Remote | Salary | URL | Notes |
|------------|---------|-------|-------|--------|--------|--------|-----|-------|
```

Always append new rows at the top (newest first).
Never delete rows — use status WITHDRAWN or SKIP instead.
