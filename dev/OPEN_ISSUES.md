# Open Issues Snapshot

**Updated:** 2026-05-21  
**Branch:** `claude/vibrant-thompson-5zWae`  
**Sync status:** Rebased onto `upstream/main` (`075937c4`)

---

## Fork: Open GitHub Issues

The fork (`IamJasonBian/airflow`) has **0 open issues**.  
Upstream issues live at <https://github.com/apache/airflow/issues>.

---

## Fork: Open Draft PRs

All three PRs have a stale base (`940c5fdd`) — upstream/main has moved forward
significantly since they were opened. Each needs a rebase before it can be
merged.

| # | Title | Branch | Opened |
|---|-------|--------|--------|
| [#6](https://github.com/IamJasonBian/airflow/pull/6) | Add open issues snapshot to dev/ | `claude/vibrant-thompson-GaTKc` | 2026-05-19 |
| [#5](https://github.com/IamJasonBian/airflow/pull/5) | Docs: Add pre-submit checks quick reference to PR guidelines | `claude/vibrant-thompson-zvCHm` | 2026-05-18 |
| [#4](https://github.com/IamJasonBian/airflow/pull/4) | Add open issues snapshot to dev/ | `claude/vibrant-thompson-MgGIN` | 2026-05-16 |

### Notes on each

**PR #5 & current branch** — Both carry the same commit ("Docs: Add pre-submit
checks quick reference to PR guidelines"). PR #5 was opened from branch
`claude/vibrant-thompson-zvCHm`; the current branch (`claude/vibrant-thompson-5zWae`)
carries the same change and is now rebased onto the latest main.  
→ **Action:** close PR #5 as superseded, or rebase it; open a fresh PR from the
current branch.

**PR #4 & #6** — Both add `dev/OPEN_ISSUES.md` from earlier sessions. Neither
was merged. PR #6 is the more recent attempt.  
→ **Action:** close #4 as superseded by #6; rebase #6 (or close and replace
with the current session's snapshot).

---

## Current Branch Ahead of Upstream

```
97481ba5  Docs: Add pre-submit checks quick reference to PR guidelines
```

One commit to ship. Rebase is clean; ready to push and open a PR targeting
`apache/airflow main`.
