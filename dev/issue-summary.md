# Fork Status — iamjasonbian/airflow

_Last updated: 2026-08-06 (automated)_

## Sync status

Fork `main` is at `2fe1537a` ("Merge branch 'apache:main' into main"), unchanged since
the last snapshot (2026-08-03). The working branch for this update
(`claude/vibrant-thompson-g2z6ko`) was created from `main` and is rebased flush with it —
zero commits ahead or behind. Direct fetch from `apache/airflow` upstream is out of scope
for this automated session (GitHub access here is scoped to `iamjasonbian/airflow` only);
upstream sync must be performed manually:

```bash
git fetch upstream main && git merge upstream/main
```

## Open issues

**0** — no open issues on this fork (GitHub Issues has no history here, open or closed;
issues for this codebase are tracked upstream at `apache/airflow`, which is out of this
session's repository scope).

## Open PRs (11)

| # | Title | Branch | Base | Status |
|---|-------|--------|------|--------|
| [#46](https://github.com/IamJasonBian/airflow/pull/46) | Add fork status and open issue/PR summary to `dev/` | `claude/vibrant-thompson-oqwrs5` | `main` | draft — duplicate of this update, see Notes |
| [#45](https://github.com/IamJasonBian/airflow/pull/45) | Add fork status and open PR summary to `dev/` | `claude/vibrant-thompson-ig10ka` | `main` | draft — duplicate of this update, see Notes |
| [#44](https://github.com/IamJasonBian/airflow/pull/44) | Fix fork CI failures in K8s tests and e2e PROD image tests | `claude/ci-failures-resolution-u1vwvt` | `fix/airflowctl-taskinstances-integration-test` | draft — targets #26, needs that PR's base to move first |
| [#43](https://github.com/IamJasonBian/airflow/pull/43) | Add fork status and open PR summary to `dev/` | `claude/vibrant-thompson-0h8jsi` | `main` | draft — duplicate of this update, see Notes |
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add `airflowctl monitor get-health` command | `airflowctl-monitor-health` | `main` | ready for review |
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add `airflowctl dagrun clear/update/delete` | `airflowctl-dagrun-extensions` | `main` | draft — help artifacts |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add `airflowctl tasks list/get` commands | `airflowctl-tasks-structural` | `main` | ready for review |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add `airflowctl taskinstances list/get-tries/get-dependencies` | `airflowctl-taskinstances-extensions` | `fix/airflowctl-taskinstances-integration-test` | draft — help artifacts |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add `airflowctl eventlogs` commands | `airflowctl-eventlogs` | `main` | draft — help artifacts |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add `airflowctl dags get-source` command | `airflowctl-dag-sources` | `main` | draft — help artifacts |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support `--map-index` in `airflowctl tasks state` (CI test on fork) | `fix/airflowctl-taskinstances-integration-test` | `main` | draft |

## Recurring blocker

Every `airflowctl` feature PR above (#27–#31) is still blocked on regenerating the help
artifacts (`airflow-ctl/docs/images/command_hashes.txt`, `output_main.svg`, etc.),
produced by `prek run capture-airflowctl-help`, which requires the Breeze/Docker CI
image and has not run successfully in any automated session.

**Required action (manual):** in a local Breeze environment, run:

```bash
prek run capture-airflowctl-help
```

then push the updated artifacts on each feature branch before requesting review.

## Notes — PR pileup on `dev/issue-summary.md`

This is now the **fourth** PR proposing `dev/issue-summary.md` (`#43` → `#45` → `#46` →
this one). Each prior attempt landed on a branch this session had no permission to push
follow-up commits to (the scheduled task is assigned a fresh branch each run), so the file
could not be updated in place and a new PR was opened instead — exactly the pileup this
file is meant to prevent.

**Recommend, as a one-time manual cleanup:** merge the most recent of these PRs and close
the other three as superseded, without merging their branches. Going forward this stays a
problem as long as each scheduled run gets a brand-new branch — consider either (a)
configuring the recurring task to reuse one fixed branch/PR for this snapshot, or (b)
having future runs check for an existing open "fork status" PR and push a follow-up commit
to *that* branch instead of opening a new one, if permissions allow it.
