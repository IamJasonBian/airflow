# Fork Status Summary

**Updated:** 2026-06-24  
**Branch:** `claude/vibrant-thompson-ew4yu2`  
**Sync:** at `384f6505` — matches `origin/main` (up to date with apache:main)

---

## Open Issues

**0** open issues on `IamJasonBian/airflow` — issues live on the upstream `apache/airflow`.

---

## Open Pull Requests (7 active feature PRs)

### Ready for Review (non-draft)

| # | Title | Branch |
|---|-------|--------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add airflowctl monitor get-health command | `airflowctl-monitor-health` |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add airflowctl tasks list/get commands | `airflowctl-tasks-structural` |

### Draft (in progress)

| # | Title | Branch |
|---|-------|--------|
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add airflowctl dagrun clear/update/delete | `airflowctl-dagrun-extensions` |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add airflowctl taskinstances list/get-tries/get-dependencies | `airflowctl-taskinstances-extensions` |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add airflowctl eventlogs commands | `airflowctl-eventlogs` |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add airflowctl dags get-source command | `airflowctl-dag-sources` |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support --map-index in airflowctl tasks state (CI test) | `fix/airflowctl-taskinstances-integration-test` |

### Recurring Blocker

All 7 feature PRs are blocked from merging by missing generated help artifacts.  
**Fix:** run `prek run capture-airflowctl-help` inside a Breeze environment to regenerate
`airflow-ctl/docs/images/command_hashes.txt` and `output_main.svg`.

---

## Stale Scheduled-Run PRs (closed)

PRs #24, #25, #33, #34, #35, #36 were routine snapshot PRs from prior agent sessions
and have been closed.
