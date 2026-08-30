# Fork Status — IamJasonBian/airflow

_Last updated: 2026-08-30 (automated)_

## Sync status

Fork `main` is at `2fe1537a` ("Merge branch 'apache:main' into main"). The working
branch for this update (`claude/vibrant-thompson-q4124d`) was created from `main` and
is flush with it — zero commits ahead or behind, so no rebase was needed this run.
Direct fetch from `apache/airflow` upstream is out of scope for this automated session
(GitHub access here is scoped to `IamJasonBian/airflow` only); upstream sync must be
performed manually:

```bash
git fetch upstream main && git merge upstream/main
```

## Open issues

**0** — no open issues on this fork.

## Open PRs (3, before this one)

| # | Title | Branch | Base | Status |
|---|-------|--------|------|--------|
| [#49](https://github.com/IamJasonBian/airflow/pull/49) | Add fork status and open issue/PR summary to `dev/` | `claude/vibrant-thompson-nbk084` | `main` | draft — duplicate of this PR, see Notes |
| [#48](https://github.com/IamJasonBian/airflow/pull/48) | Add fork status and open issue/PR summary to `dev/` | `claude/vibrant-thompson-j8mdqb` | `main` | draft — duplicate of this PR, see Notes |
| [#44](https://github.com/IamJasonBian/airflow/pull/44) | Fix fork CI failures in K8s tests and e2e PROD image tests | `claude/ci-failures-resolution-u1vwvt` | `fix/airflowctl-taskinstances-integration-test` | draft — targets #26, needs that PR's base to move first |

## Notes — the recurring "PR pileup" problem is still unresolved

This is at minimum the **seventh** PR proposing `dev/issue-summary.md` for this
recurring scheduled task (`#43` → `#45` → `#46` → `#47` → `#48` → `#49` → this one).
The root cause, first documented in `#48` and repeated in `#49`, is unchanged: each
scheduled run is assigned a brand-new branch (`claude/vibrant-thompson-*`) it has no
prior history with, and the session's git branch policy for this task requires
developing and pushing only on that assigned branch — so a session cannot push a
follow-up commit onto a previous run's branch even when one exists, and instead must
open a new PR each time.

**This still has not been fixed since `#48` first flagged it two runs ago.**
Recommended one-time actions for a human (unchanged from `#49`):

1. Close `#48` and `#49` as superseded by this PR, without merging their branches —
   they contain no code, only this status file.
2. Reconfigure the recurring schedule so each run is assigned the **same** fixed
   branch (e.g. `dev/fork-status`) instead of a fresh `claude/vibrant-thompson-*`
   branch every time, so future runs can push follow-up commits to one long-lived PR
   instead of opening a new one.

## Recurring blocker (from `#48`/`#49`, still applicable)

Every `airflowctl` feature PR (`#27`–`#31`, if still open) was blocked on regenerating
help artifacts (`airflow-ctl/docs/images/command_hashes.txt`, `output_main.svg`, etc.)
via `prek run capture-airflowctl-help`, which requires the Breeze/Docker CI image and
has not run successfully in any automated session. This was not re-verified in this run
since GitHub Issues, not those specific PRs, was this run's scope — check those PRs
directly for current status.
