---
title: shelltutor Status
category: status
component: project-status
status: active
version: 0.2.0
last_updated: 2026-11-07
tags: [status, posture, deferrals]
priority: high
---

# Status

Current truth for the `shelltutor` repository.

## Posture

- **Lifecycle**: pre-release implementation. Curriculum redesign
  (ROADMAP Phase 3) is complete; awaiting Phase 2 portability
  validation and Phase 4 release-posture decision.
- **Semantic owner**: Jefahnierocks (personal workspace).
- **Current host**: local workstation; GitHub remote at
  `github.com/jefahnierocks/shelltutor` (public).
- **Secrets authority**: none required; the tutor handles no secrets.
- **Review cadence**: ad-hoc until a release cadence stabilizes.
- **PaC status**: local static analysis only — `scripts/check-*.sh`
  driven from `Makefile`; no PaC engine, no enforcing control plane.
- **IaC status**: none — no live infrastructure.
- **Bash floor**: 3.2 (stock macOS `/bin/bash` 3.2.57 satisfies it;
  no install step required on any supported platform).

## What Is True Now

- Day-1 documentation set (`README.md`, `CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`) plus `docs/contracts.md`
  is in place.
- Root `project.yaml` follows Specification 1 and projects this file as a
  public-available, linkable working prototype. Required operational state is
  `unverified`; it makes no deployed-system claim. The development check points
  to `scripts/verify-project.sh`, which delegates to the existing `make verify`.
- Owner-directed adoption source is prepared with the public immutable Release 1
  bundle and separate bootstrap. Contributor Python/Git prerequisites are separate
  from the Bash/POSIX learner runtime. On 2026-10-17, all 23 focused regression
  tests and the no-argument native gate passed locally with prepared Python 3.13.16
  and Git 2.56.0. Hosted qualification, adoption acceptance and effective branch
  enforcement remain pending; local source validation is not runtime acceptance.
- The tutor script (`shelltutor`) was imported from prior-art at
  `fedora-top:~/Projects/shelltutor` (commit `136f6a3`, 2026-05-17).
- **ROADMAP Phase 1 — User-Agnostic Refactor — is complete** (commit
  `e6257aa`, 2026-05-21).
- **ROADMAP Phase 3 — Curriculum Redesign — is complete** (commit
  `9f61570`, 2026-05-21). shelltutor is a vimtutor-prerequisite
  course delivered as five mastery-gated stages with a Bash 3.2 runtime floor.
  Current cross-version evidence is recorded below under F-009; the full
  Phase 2 walkthroughs remain pending.
- First profile cycle and first audit cycle complete (snapshot
  2026-05-21). See `profile/2026-05-21/` and
  `audit/2026-05-21/SUMMARY.md`. **All seven audit findings closed**
  (F-001 … F-007). Six of seven proposed fitness functions
  implemented as `make` targets (FF-001 safety, FF-002 write-scope,
  FF-004 lesson portability, FF-005 shellcheck, FF-006 smoke,
  FF-007 governance citations). FF-003 (STATUS/ROADMAP drift heuristic)
  remains deferred — periodic audit cycles cover it better than a
  fuzzy CI check.
- Quality gates: `make check | lint | smoke | verify | self-test`
  (Makefile). All four checker self-test suites pass locally.
- **Simulation-design plan adopted** (`docs/simulation-design-plan.md`
  v0.3.0, commit `f4f0a23`, 2026-05-23). Reframes FF-006 as a ladder:
  `FF-006a` static smoke (in place via `make smoke`) and `FF-006b`
  lesson-flow PTY harness (Slice 1 complete in commit `29dc0d3`, run via
  `make lesson-flow`). Slice 2 practice-shell hardening is next;
  `FF-006c` depth + multi-persona remains deferred. The harness is optional contributor
  tooling on Python 3.9+ stdlib only and is **not** part of
  `make verify`.
- **Stage 1 density audit** recorded
  (`audit/2026-05-23/stage1-density.md`, commit `c8b2dd8`,
  2026-05-23). Two screens (S1-L1 running commands; S1-L2 identity)
  flagged SPLIT. The audit preceded the committed Slice 1 `current-rc`
  baseline as required; those lesson-density improvements remain follow-on work.
- **F-008 surfaced and fixed** — Stage 1 gate verifier was broken on
  macOS BSD sed (`\L` GNU extension). Caught by the Slice 1 PTY
  harness on its first `current-rc` baseline run, 2026-05-23.
  Release-blocking; silent since commit `9f61570`. Fix replaces the
  affected `sed` call with portable `awk`; see
  `audit/2026-05-23/findings.md` F-008 for the writeup. First
  value-add from FF-006b ("observe before harden") validating the
  simulation-design-plan posture.
- **F-009 surfaced and fixed** — current Bash 5.3 could hang before
  argument dispatch while macOS Bash 3.2 did not reliably load the practice
  rcfile through process substitution. Commit `d893ea8` selects Bash 5.0
  compatibility for temporary-file-backed here-documents and feeds the rcfile
  through fd 3; see `audit/2026-07-14/findings.md`. On 2026-07-14,
  `make verify`, all checker self-tests, and both
  Stage 1 PTY variants passed under Bash 3.2.57 and Bash 5.3.15. The no-TTY
  negative test exited 1 with the documented preflight diagnostic. This is
  not a substitute for the still-pending full five-stage Phase 2 walks.
- `.claude/settings.json` carries a PostToolUse shellcheck hook so
  Claude Code sessions get the FF-005 warning immediately on script
  edits.
- **2026-11 work plan adopted** (`docs/workplan/README.md`, 2026-11-07,
  prepared at `b2fdff7`): eight worker-executable packages WP-01 to WP-08
  with a binding decision log (D-01 to D-18). Sequence: five-stage harness
  baseline → tutor correctness fixes → practice-shell hardening (Slice 2,
  C-007) → Stage 1 density split → gate feedback alignment → doc sweep.
  Hosted Linux evidence capture and release preparation are operator-gated.
- **WP-01 landed: five-stage harness baseline** (`audit/2026-11-08/sim/`,
  harness at `72f6021`, FF-006c rung 1 — one persona, five stages; second
  persona still deferred). `make sim` drives `careful-beginner` across all
  five stages with an empty per-run `HOME`; the pre-fix baseline observes
  F-010 (`S5-L3`) and F-011 (`S2-L2`, `S3-L2`) as `error-signature` events.
  Green on Bash 3.2.57 and 5.3.20; nothing fixed yet (WP-02).
- **Slice 2 practice-shell hardening landed (C-007)** (WP-03,
  `audit/2026-11-08/sim/all-slice2*`, `audit/2026-11-08/slice2-comparison.md`):
  the practice shell no longer sources the system bashrc, scrubs the
  environment and fixes the Readline defaults; the preview variant is
  retired. The Linux before/after comparison remains pending until WP-06 or
  the operator's Phase 2 Linux session.
- **WP-02 landed: tutor correctness fixes** (F-010 to F-013 resolved; post-fix
  evidence `audit/2026-11-08/sim/all-postfix/`). Stage 3–5 lessons now run in
  their stage folder with fixtures seeded on stage entry (C-003); lesson copy
  uses `${SANDBOX}` or relative paths; `SHELLTUTOR_HOME` is normalised at
  startup (C-004); `ask_question` normalises with `tr -s`; the Stage 1 day check
  accepts the locale form of `date`. New gates: FF-004 sandbox-path rule and
  FF-008 (`scripts/check-posix-tools.sh`, in `make check`). The five-stage
  harness is green on Bash 3.2.57 and 5.3.20 with no `error-signature` events.
  The interactive `de_DE` gate walk remains an operator spot-check.
- **F-010 to F-013 surfaced by static review** (`audit/2026-11-07/findings.md`,
  2026-11-07; all four resolved by WP-02, see the landing line above):
  lesson 5.3 promises a `practice.txt` fixture that does not exist at lesson
  time (F-010, sev 3); lesson copy hardcodes `~/.shelltutor` and fails under
  `SHELLTUTOR_HOME` (F-011, sev 3); `ask_question` uses GNU-sed `\+`, a no-op
  on macOS (F-012, sev 2); the Stage 1 day-of-week check assumes an English
  locale and cannot pass under e.g. `de_DE` (F-013, sev 3). FF-008 (POSIX
  text-tool portability in script code) was proposed there and is now
  implemented.
- On 2026-11-07 `make verify` (24 declaration tests plus the static, lint and
  smoke checks), `make self-test`, and the Stage 1 PTY harness passed locally
  under Bash 3.2.57 and 5.3.20; the hosted `verify` run on `b2fdff7`
  succeeded. Inside an agent session the manifest check refuses inherited
  `GIT_CONFIG_*` overrides and reports NOT_CHECKED; the work plan's worker
  protocol gives the environment-clearing command that restores the verdict.
- **Operator decisions of 2026-11-07**: license **MIT** (landed via WP-08
  part A, see the License bullet below); WP-06 (non-gating hosted Linux evidence workflow)
  **approved**, to start after WP-01.
- The companion `wyn-setup/` directory from prior-art is intentionally
  not carried forward.
- **License adopted (WP-08 part A)**: MIT, SPDX id `MIT`, `Copyright (c) 2026
  Jefahnierocks` (operator decision and copyright line of 2026-11-07).
  `LICENSE` is at the repo root and `shelltutor` carries the SPDX header.
  Distribution is unchanged: clone + run remains the install story. No
  `CHANGELOG.md` yet (see Deferrals); the Phase 2 walkthrough results are
  still pending.

## Immediate Next Steps

1. **Execute the 2026-11 work plan** (`docs/workplan/README.md`) —
   WP-01 → WP-02 → WP-03 → WP-04 in order, WP-05 after WP-02, WP-06 after
   operator approval, WP-07 last; WP-08 once the operator supplies the
   license choice and the Phase 2 walkthrough results. Each package names
   its commits, validation and evidence; `STATUS.md` records each landing.
2. **Portability validation (ROADMAP Phase 2)** — manually walk all
   five mastery-gated stages on macOS with stock `/bin/bash` 3.2 and
   on a Debian/Ubuntu-family Linux host with Bash 5.x. The no-TTY negative
   test is recorded above; Fedora-family validation is optional. Record the
   walkthrough dates + observed results here. The
   static checks (`make verify`) confirm the script's invariants; the
   manual walkthrough confirms the human-facing experience.
3. **Second profile + audit cycle** — once Phase 2 manual validation
   lands, run a focused-refresh profile and a focused-diff audit
   (Phases 1, 6, 8, 10, 10.5) per the cadence recommended in
   `audit/2026-05-21/SUMMARY.md`. Expected outcomes:
   - F-001..F-007 smoke-test as `struck` (no longer supported by
     current evidence)
   - FF-001..FF-007 promoted from "proposed" to "implemented"
     (FF-003 remains "deferred")
   - new dimension scores per §11 reflecting the closures
4. **License adoption (ROADMAP Phase 4)** — MIT was chosen on 2026-11-07.
   Confirm the copyright line in `docs/workplan/WP-08-release-prep.md` and
   run its part A (LICENSE, script header, README/STATUS wording).
   `CHANGELOG.md` and the `v0.1.0` tag inputs (part B) follow the Phase 2
   walkthrough closure.

## Deferrals

| Deferred surface | Reason | Trigger to revisit |
|------------------|--------|--------------------|
| `CHANGELOG.md` | Nothing released yet; no tagged history | First tagged release |
| `CODEOWNERS`, PR templates and unrelated GitHub automation | Not needed by the declaration migration | A project-specific need |
| Hosted `verify` qualification and branch enforcement | Specification 1 adoption supplies the activation trigger; source is prepared | Actual hosted checks and effective protection readback |
| Cross-platform CI | Hosted cross-platform *acceptance* remains deferred; `sim-evidence` captures Linux transcripts only | When manual validation stops scaling |
| Package distribution (Homebrew tap, AUR, etc.) | Single-file script; install is `clone + run` | If users ask for managed install |

## Blockers

- None.

## Decision-Disagreement Rule

If `STATUS.md`, `ROADMAP.md`, and `CONTRIBUTING.md` disagree about
project-level posture, fix the disagreement here first; downstream
documents defer to this file for current truth.
