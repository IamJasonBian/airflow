# Fork Status — iamjasonbian/airflow

_Last updated: 2026-06-30 (automated)_

## Sync status

Fork `main` is at `384f6505` ("Merge branch 'apache:main' into main").
Direct fetch from `apache/airflow` upstream is blocked in the automated environment (proxy 403);
upstream sync must be performed manually (`git fetch upstream main && git merge upstream/main`).

## Open issues

**0** — issues are disabled on this fork. Upstream issues live at
<https://github.com/apache/airflow/issues>.

## Open PRs (7)

### Ready for review

| # | Title | Branch |
|---|-------|--------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add `airflowctl monitor get-health` | `airflowctl-monitor-health` |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add `airflowctl tasks list/get` | `airflowctl-tasks-structural` |

### Draft — feature work

| # | Title | Branch | Blocker |
|---|-------|--------|---------|
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add `airflowctl dagrun clear/update/delete` | `airflowctl-dagrun-extensions` | help artifacts |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add `airflowctl taskinstances list/get-tries/get-dependencies` | `airflowctl-taskinstances-extensions` | help artifacts |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add `airflowctl eventlogs list/get` | `airflowctl-eventlogs` | help artifacts |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add `airflowctl dags get-source` | `airflowctl-dag-sources` | help artifacts |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support `--map-index` in `airflowctl tasks state` (CI) | `fix/airflowctl-taskinstances-integration-test` | — |

## Recurring blocker

Every feature PR above (#27–#32) is blocked on regenerating the help artifacts
(`airflow-ctl/docs/images/command_hashes.txt`, `output_main.svg`, etc.).
These are produced by `prek run capture-airflowctl-help`, which requires the
Breeze/Docker CI image and has not run successfully in any automated session.

**Required action (manual):** In a local Breeze environment, run:

```bash
prek run capture-airflowctl-help
```

then push the updated artifacts on each feature branch before requesting review.

## Notes

- Stale daily-snapshot PRs (#37–#42) were closed on 2026-06-30 — they all
  attempted to add this file but were never merged. Merge this PR to establish
  a stable location for the status file; subsequent runs will update it in place.
