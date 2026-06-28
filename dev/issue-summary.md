# Fork Status & Open PR Summary

**Last updated:** 2026-06-28
**Branch:** `claude/vibrant-thompson-2hg1bp`
**Sync status:** Up to date with `origin/main` at `384f6505`
("Merge branch 'apache:main' into main")

> Note: `upstream` (apache/airflow) is not reachable in automated sessions.
> Run `git fetch upstream main && git rebase upstream/main` locally when
> upstream access is available. Open issues on this fork: **0**.

---

## Open PRs (11 total)

### Ready for review (2)

| PR | Title | Branch |
|----|-------|--------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add `airflowctl monitor get-health` command | `airflowctl-monitor-health` |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add `airflowctl tasks list/get` commands | `airflowctl-tasks-structural` |

### Feature drafts (5)

| PR | Title | Branch |
|----|-------|--------|
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add `airflowctl dagrun clear/update/delete` | `airflowctl-dagrun-extensions` |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add `airflowctl taskinstances list/get-tries/get-dependencies` | `airflowctl-taskinstances-extensions` |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add `airflowctl eventlogs list/get` commands | `airflowctl-eventlogs` |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add `airflowctl dags get-source` command | `airflowctl-dag-sources` |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support `--map-index` in `airflowctl tasks state` (CI branch) | `fix/airflowctl-taskinstances-integration-test` |

### Stale scheduled-run snapshot drafts (4)

These were auto-created by previous scheduled sessions and duplicate each other.
Consider closing #37, #38, #39 in favour of the most recent (#40).

| PR | Title |
|----|-------|
| [#40](https://github.com/IamJasonBian/airflow/pull/40) | Add fork status and open PR summary to dev/ (2026-06-27) |
| [#39](https://github.com/IamJasonBian/airflow/pull/39) | Add open issues summary and sync status to dev/ (2026-06-26) |
| [#38](https://github.com/IamJasonBian/airflow/pull/38) | Update fork status summary (2026-06-25) |
| [#37](https://github.com/IamJasonBian/airflow/pull/37) | Update fork status summary and close stale PRs (2026-06-24) |

---

## Recurring Blocker

**`prek run capture-airflowctl-help` cannot run in automated sessions.**

All feature PRs (#27–#32) have stale generated help artifacts:
- `airflow-ctl/docs/images/command_hashes.txt`
- `airflow-ctl/docs/images/output_main.svg`

These must be regenerated via Breeze/Docker before any feature PR can merge.
Run locally: `prek run capture-airflowctl-help`

---

## PR Dependency Chain

```
#26 (map-index CI) ← base for #29 (taskinstances extensions)
#28, #27, #31 ← target main directly
#30, #32 ← target main directly (ready for review)
```
