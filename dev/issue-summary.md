# Fork Status & Open PR Summary

**Last updated:** 2026-06-29  
**Branch:** `claude/vibrant-thompson-0bzv2d`  
**Sync status:** In sync with `origin/main` at `384f6505` (last upstream merge: "Merge branch 'apache:main' into main"). Direct fetch from `apache/airflow` is blocked in automated sessions — sync manually when upstream access is available.

---

## Open Issues

**0 open issues** on `iamjasonbian/airflow`. Issues are tracked upstream at `apache/airflow`; out of scope for this session.

---

## Open PRs (12 total)

### Ready for Review

| # | Title | Branch |
|---|-------|--------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add `airflowctl monitor get-health` command | `airflowctl-monitor-health` |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add `airflowctl tasks list/get` commands | `airflowctl-tasks-structural` |

### Feature Drafts

| # | Title | Branch |
|---|-------|--------|
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add `airflowctl dagrun clear/update/delete` | `airflowctl-dagrun-extensions` |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add `airflowctl taskinstances list/get-tries/get-dependencies` | `airflowctl-taskinstances-extensions` |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add `airflowctl eventlogs list/get` commands | `airflowctl-eventlogs` |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add `airflowctl dags get-source` command | `airflowctl-dag-sources` |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support `--map-index` in `airflowctl tasks state` (CI test) | `fix/airflowctl-taskinstances-integration-test` |

### Stale Scheduled-Run Snapshots (should be closed)

These PRs were opened by automated sessions and contain only a previous version of this summary file. They have not been merged and can be closed.

| # | Title | Opened |
|---|-------|--------|
| [#41](https://github.com/IamJasonBian/airflow/pull/41) | Add fork status and open PR summary to dev/ | 2026-06-28 |
| [#40](https://github.com/IamJasonBian/airflow/pull/40) | Add fork status and open PR summary to dev/ | 2026-06-27 |
| [#39](https://github.com/IamJasonBian/airflow/pull/39) | Add open issues summary and sync status to dev/ | 2026-06-26 |
| [#38](https://github.com/IamJasonBian/airflow/pull/38) | Update fork status summary (2026-06-25) | 2026-06-25 |
| [#37](https://github.com/IamJasonBian/airflow/pull/37) | Update fork status summary and close stale PRs (2026-06-24) | 2026-06-24 |

---

## Recurring Blocker

**`prek run capture-airflowctl-help`** (generates `command_hashes.txt` and `output_main.svg`) requires the Breeze/Docker CI image, which is not available in automated sessions. This blocks merging all feature PRs (#27–#32). Run manually before any feature PR merge:

```bash
prek run capture-airflowctl-help --all-files
```
