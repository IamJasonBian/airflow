# Fork Status Summary

**Updated:** 2026-06-25
**Fork main:** `384f6505` (up to date with `origin/main`)
**Upstream sync:** `apache/airflow` not reachable via proxy in this environment — fork was last synced manually to `384f6505`.

## Open Issues

None — the fork `IamJasonBian/airflow` has no open issues.

## Open Pull Requests (8 total)

### Ready for Review (not draft)

| # | Title | Branch |
|---|-------|--------|
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add airflowctl tasks list/get commands | `airflowctl-tasks-structural` |
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add airflowctl monitor get-health command | `airflowctl-monitor-health` |

### Draft

| # | Title | Branch |
|---|-------|--------|
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support `--map-index` in airflowctl tasks state (CI test) | `fix/airflowctl-taskinstances-integration-test` |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add airflowctl dags get-source command | `airflowctl-dag-sources` |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add airflowctl eventlogs list/get commands | `airflowctl-eventlogs` |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add airflowctl taskinstances list/get-tries/get-dependencies | `airflowctl-taskinstances-extensions` |
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add airflowctl dagrun clear/update/delete | `airflowctl-dagrun-extensions` |
| [#37](https://github.com/IamJasonBian/airflow/pull/37) | Update fork status summary and close stale PRs (2026-06-24) | `claude/vibrant-thompson-ew4yu2` |

## Recurring Blocker

All feature PRs (#27–#32) are blocked on regenerating help artifacts:
- `airflow-ctl/docs/images/command_hashes.txt`
- `airflow-ctl/docs/images/output_main.svg` (and per-command SVGs)

These are produced by `prek run capture-airflowctl-help`, which requires a Breeze/Docker environment. None of the automated sessions have been able to run it. **Manual action needed:** run `prek run capture-airflowctl-help` locally before any feature PR can merge.

## PR Dependency Chain

```
main
 ├── #26  fix/airflowctl-taskinstances-integration-test  (draft)
 │    └── #29  airflowctl-taskinstances-extensions  (draft, based on #26)
 ├── #27  airflowctl-dag-sources  (draft)
 ├── #28  airflowctl-eventlogs  (draft)
 ├── #30  airflowctl-tasks-structural  (ready)
 ├── #31  airflowctl-dagrun-extensions  (draft)
 ├── #32  airflowctl-monitor-health  (ready)
 └── #37  claude/vibrant-thompson-ew4yu2  (draft, status snapshot)
```
