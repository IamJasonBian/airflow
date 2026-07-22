# Fork Status — iamjasonbian/airflow

_Last updated: 2026-07-22 (automated)_

## Sync status

Fork `main` is at `2fe1537a` ("Merge branch 'apache:main' into main"), and the working
branch for this update is rebased flush with it (no divergence). Direct fetch from
`apache/airflow` upstream is out of scope for this automated session (GitHub access here
is scoped to `iamjasonbian/airflow` only); upstream sync must be performed manually:

```bash
git fetch upstream main && git merge upstream/main
```

## Open issues

**0** — no open issues on this fork.

## Open PRs (9)

### Ready for review

| # | Title | Branch |
|---|-------|--------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add `airflowctl monitor get-health` | `airflowctl-monitor-health` |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add `airflowctl tasks list/get` | `airflowctl-tasks-structural` |

### Draft — feature work

| # | Title | Branch | Blocker |
|---|-------|--------|---------|
| [#44](https://github.com/IamJasonBian/airflow/pull/44) | Fix fork CI failures in K8s tests and e2e PROD image tests | `claude/ci-failures-resolution-u1vwvt` | targets #26, needs that PR's base to move first |
| [#43](https://github.com/IamJasonBian/airflow/pull/43) | Add fork status and open PR summary to `dev/` | `claude/vibrant-thompson-0h8jsi` | superseded by this update — see Notes |
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add `airflowctl dagrun clear/update/delete` | `airflowctl-dagrun-extensions` | help artifacts |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add `airflowctl taskinstances list/get-tries/get-dependencies` | `airflowctl-taskinstances-extensions` | help artifacts |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add `airflowctl eventlogs list/get` | `airflowctl-eventlogs` | help artifacts |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add `airflowctl dags get-source` | `airflowctl-dag-sources` | help artifacts |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support `--map-index` in `airflowctl tasks state` (CI) | `fix/airflowctl-taskinstances-integration-test` | — |

## Recurring blocker

Every feature PR above (#27–#32) is blocked on regenerating the help artifacts
(`airflow-ctl/docs/images/command_hashes.txt`, `output_main.svg`, etc.), produced by
`prek run capture-airflowctl-help`, which requires the Breeze/Docker CI image and has not
run successfully in any automated session.

**Required action (manual):** in a local Breeze environment, run:

```bash
prek run capture-airflowctl-help
```

then push the updated artifacts on each feature branch before requesting review.

## Notes

- PR #43 proposed this exact file three weeks ago (2026-06-30) to stop new snapshot PRs
  from piling up, but it was never merged — so this update had to land as a new PR anyway,
  which is exactly the pileup #43 was meant to prevent. **Recommend closing #43 in favor of
  this PR** once merged, so future automated runs update this file in place instead of
  opening another one.
