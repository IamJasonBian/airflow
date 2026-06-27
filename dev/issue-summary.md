# Fork Status Summary

**Updated:** 2026-06-27
**Branch:** `claude/vibrant-thompson-uwtwnv`

## Sync Status

- **Fork main:** `384f6505` — last commit is "Merge branch 'apache:main' into main" (fork is current with upstream as of that merge)
- **Upstream (apache/airflow):** not reachable via the proxy in this environment — run `git fetch upstream main` locally to check for new upstream commits
- **Current branch vs origin/main:** identical (0 commits ahead, 0 behind)

## Open Issues

**0 open issues** on `iamjasonbian/airflow`.

## Open Pull Requests (10)

### Ready for Review

| # | Title | Branch |
|---|-------|--------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add `airflowctl monitor get-health` command | `airflowctl-monitor-health` |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add `airflowctl tasks list/get` commands | `airflowctl-tasks-structural` |

### Draft — Feature PRs

| # | Title | Branch | Base |
|---|-------|--------|------|
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add `airflowctl dagrun clear/update/delete` | `airflowctl-dagrun-extensions` | `main` |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add `airflowctl taskinstances list/get-tries/get-dependencies` | `airflowctl-taskinstances-extensions` | `fix/airflowctl-taskinstances-integration-test` |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add `airflowctl eventlogs` commands | `airflowctl-eventlogs` | `main` |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add `airflowctl dags get-source` command | `airflowctl-dag-sources` | `main` |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support `--map-index` in `airflowctl tasks state` | `fix/airflowctl-taskinstances-integration-test` | `main` |

### Draft — Stale Scheduled-Run Snapshots (candidates for closing)

| # | Title |
|---|-------|
| [#39](https://github.com/IamJasonBian/airflow/pull/39) | Add open issues summary and sync status to dev/ (2026-06-26) |
| [#38](https://github.com/IamJasonBian/airflow/pull/38) | Update fork status summary (2026-06-25) |
| [#37](https://github.com/IamJasonBian/airflow/pull/37) | Update fork status summary and close stale PRs (2026-06-24) |

## Recurring Blocker

All feature PRs (#26–#32) have unregeneated help artifacts:
- `airflow-ctl/docs/images/command_hashes.txt`
- `airflow-ctl/docs/images/output_main.svg` (and per-command SVGs)

These are produced by `prek run capture-airflowctl-help`, which runs inside the Breeze/Docker CI image. That image is unavailable in automated sessions. **Manual action required:** run `prek run capture-airflowctl-help` locally (with Docker) before any feature PR can merge.
