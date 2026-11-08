---
title: shelltutor Status
category: status
component: project-status
status: active
version: 0.3.0
last_updated: 2026-11-07
tags: [status, posture, deferrals]
priority: high
---

# Status

Current truth for the `shelltutor` repository.

## Posture

- **Lifecycle**: pre-release implementation. Curriculum redesign
  (ROADMAP Phase 3) is complete and the 2026-11 work plan has landed;
  awaiting the human Phase 2 portability walkthroughs and the Phase 4
  release steps (CHANGELOG, `v0.1.0`).
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

### The 2026-11 cycle, in one place

The work plan (`docs/workplan/README.md`, adopted 2026-11-07) ran in the
order observe → fix → harden → shape → verify. Outcome: the tutor's four
known correctness defects are fixed with before/after PTY evidence, the
practice shell is hardened and contracted, Stage 1 is split into four
lessons, every gate escalates feedback without ever auto-passing, and the
documents agree with the code.

| Package | Landed | What it delivered |
| --- | --- | --- |
| WP-01 | `c4f92c5` | Five-stage PTY harness (`make sim`, FF-006c rung 1) and the pre-fix baseline, which showed F-010 and F-011 as transcript evidence. |
| WP-02 | `f4fb671` | F-010 to F-013 resolved; stage-folder model (C-003); `SHELLTUTOR_HOME` normalised (C-004); FF-004 sandbox-path rule and the FF-008 POSIX text-tool checker; post-fix evidence. |
| WP-03 | `4482554` | Slice 2 practice-shell hardening (C-007); the `no-system-rc-preview` variant retired. |
| WP-04 | `a909d4b` | Stage 1 density split: four lessons (1.1 running commands, 1.2 keyboard habits, 1.3 where/who/when, 1.4 what just happened). |
| WP-05 | `ff4248b` | Stage 2 (`cd`) and Stage 4 (`*.txt` glob) verified from practice history; escalating hint/worked-example feedback on every gate; `second-try` persona. |
| WP-06 | `a71ab76` | Non-gating `sim-evidence` workflow for hosted Linux transcripts (commits 1–2); the first hosted run and its evidence commit remain with the operator. |
| WP-07 | this sweep | Documents realigned with the code and with this file; the governance check covers `docs/` and the harness README. |
| WP-08 part A | `7d5065f` | MIT `LICENSE` and the script's SPDX header; part B (CHANGELOG, `v0.1.0` inputs) waits for the Phase 2 results. |
| WP-09 | `bd841ae` | F-014 fixed: the practice shell runs under the outer script's own Bash (`"$BASH"`); the harness records the Bash path and version; post-WP-04/05 macOS baseline `all-current`. |

### Curriculum and tutor

- `shelltutor` is a vimtutor-prerequisite course: five mastery-gated stages,
  each closing with three recall questions and one practical task, on a
  Bash 3.2 runtime floor (ROADMAP Phase 3 is complete, `9f61570`,
  2026-05-21; Phase 1, the user-agnostic refactor, is complete, `e6257aa`).
- Stage 1 has four lessons; the other stages have three or four. Stages 1
  and 2 start practice prompts in `$SANDBOX`; stages 3 to 5 start in their
  stage folder (C-003). Fixtures are seeded on stage entry.
- Gates verify the filesystem; Stages 1, 2 and 4 also check the practice
  history. A second miss shows a hint, a third a worked example; nothing
  auto-passes (D-14, C-006).
- The practice shell does not source the system bashrc, resets the
  behaviour-changing variables and fixes the Readline defaults (C-007). The
  Linux before/after comparison for Slice 2 remains pending until the hosted
  run or the operator's Phase 2 Linux session.
- Contracts C-001 to C-007 are in `docs/contracts.md`.
- The tutor was imported from prior-art at `fedora-top:~/Projects/shelltutor`
  (commit `136f6a3`, 2026-05-17); the companion `wyn-setup/` directory is
  intentionally not carried forward.

### Quality gates and fitness functions

- `make check | lint | smoke | verify | self-test` (all offline), plus the
  optional `make lesson-flow` and `make sim` PTY harness targets, which are
  not part of `verify`. All five checker self-test suites pass locally.
- Seven of eight proposed fitness functions are implemented: FF-001 safety,
  FF-002 write-scope, FF-004 lesson portability (now also rejecting a
  hardcoded `~/.shelltutor`), FF-005 shellcheck, FF-006 smoke and PTY harness
  (a, b and c rung 1), FF-007 governance citations (now covering `docs/*.md`,
  `docs/workplan/*.md` and `scripts/sim/README.md`), and FF-008 POSIX
  text-tool portability. FF-003 (STATUS/ROADMAP drift) stays deferred; the
  WP-07 sweep is its manual stand-in and the next audit cycle covers it.
  FF-008 is to be admitted to the catalogue at the next audit cycle.
- `.claude/settings.json` carries a PostToolUse shellcheck hook so Claude
  Code sessions get the FF-005 warning on script edits.
- Last full local gate run, 2026-11-07: `make verify` (24 declaration tests
  plus the static, lint and smoke checks), `make self-test`, and the PTY
  harness (`careful-beginner` across all five stages; `second-try` on stages 2
  and 4) passed under Bash 3.2.57 and 5.3.20 with no `error-signature`
  events. Inside an agent session the manifest check refuses inherited
  `GIT_CONFIG_*` overrides and reports NOT_CHECKED; the work plan's worker
  protocol gives the environment-clearing command that restores the verdict.

### Simulation ladder

- FF-006a static smoke (`make smoke`); FF-006b Stage 1 PTY harness (Slice 1,
  `29dc0d3`); FF-006c rung 1 (`careful-beginner`, five stages, plus
  `second-try` on stages 2 and 4). Slice 2 hardening is complete.
  `confused-novice` and the confusion events (Slice 3) remain deferred. The
  harness is contributor tooling on Python 3.9+ stdlib only
  (`docs/simulation-design-plan.md`, `scripts/sim/README.md`).
- Evidence is under `audit/2026-11-08/` (pre-fix baseline, post-fix,
  Slice 2, Stage 1 split, `second-try`); only synthetic bundles are committed.

### Findings and audit cycles

- First profile and audit cycle complete (snapshot 2026-05-21): see
  `profile/2026-05-21/` and `audit/2026-05-21/SUMMARY.md`. All seven findings
  (F-001 to F-007) closed.
- F-008 (BSD-sed gate verifier, caught by the first PTY baseline) and F-009
  (Bash 5.3 startup hang, Bash 3.2 rcfile loading) are fixed; see
  `audit/2026-05-23/findings.md` and `audit/2026-07-14/findings.md`.
- F-010 to F-013 (stage-5 fixture, hardcoded sandbox path, GNU-sed `\+`,
  English-only day check) surfaced by static review on 2026-11-07 and are
  resolved by WP-02 (`audit/2026-11-07/findings.md`).
- F-014 (the practice shell was whichever `bash` was first on `PATH`, not the
  interpreter running the script) surfaced on 2026-11-08 and is resolved by
  WP-09 (`audit/2026-11-08/findings.md`): `practice()` launches `"$BASH"`, and
  run metadata records `bash_path` and `bash_version`. The 2026-11-08 macOS
  Phase 2 walk did not confirm the practice shell's Bash version, so it should
  be repeated with `/bin/bash ./shelltutor` and `echo $BASH_VERSION` recorded;
  the operator re-records it. The like-for-like macOS baseline is
  `audit/2026-11-08/sim/all-current/`.
- The Stage 1 density audit (`audit/2026-05-23/stage1-density.md`) preceded
  the first baseline as required; its follow-up
  (`audit/2026-11-08/stage1-density-followup.md`) records the WP-04 split.

### Declaration and license

- Root `project.yaml` follows Specification 1 and projects this file as a
  public-available, linkable working prototype. Required operational state is
  `unverified`; it makes no deployed-system claim. The development check points
  to `scripts/verify-project.sh`, which delegates to the existing `make verify`.
- Owner-directed adoption source is prepared with the public immutable Release 1
  bundle and separate bootstrap. Contributor Python/Git prerequisites are
  separate from the Bash/POSIX learner runtime. Hosted qualification, adoption
  acceptance and effective branch enforcement remain pending; local source
  validation is not runtime acceptance.
- **License**: MIT, SPDX id `MIT`, `Copyright (c) 2026 Jefahnierocks`
  (operator decision and copyright line of 2026-11-07). `LICENSE` is at the
  repo root and `shelltutor` carries the SPDX header. Distribution is
  unchanged: clone + run. No `CHANGELOG.md` yet (see Deferrals).
- Day-1 documentation set (`README.md`, `CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`) plus `docs/contracts.md` is in
  place.

### Design record

- `docs/design-description.md` (2026-11-08) is the formal design baseline:
  game-design, software, user-journey and pedagogy lenses, a glossary, the
  design tensions the framing exposes, and which claims are backed by
  evidence under `audit/`. Descriptive only.
- `docs/design-direction-2026-11.md` (draft, 2026-11-08) records the
  operator's stated direction toward a general-purpose, agent-aware shell
  course and the decisions that must precede any specification. No
  identity, contract or curriculum change has been made on its account.

## Immediate Next Steps

1. **Portability validation (ROADMAP Phase 2)** — the operator walks all five
   mastery-gated stages by hand on macOS with stock `/bin/bash` 3.2 and on a
   Debian/Ubuntu-family Linux host with Bash 5.x, runs the no-TTY negative
   test, and spot-checks the Stage 1 day answer under a non-English locale
   (for example `LC_ALL=de_DE.UTF-8`). Checklist:
   `docs/phase2-walkthrough-checklist.md`. Record walkthrough dates and
   observed results here. The automated evidence supports these walks; it
   does not replace them.
2. **WP-06 hosted run** — dispatch the `sim-evidence` workflow, review the
   artifact by hand and commit it as the Linux evidence bundle
   (`scripts/sim/README.md`, "Hosted Linux evidence intake").
3. **Release inputs (ROADMAP Phase 4, WP-08 part B)** — `CHANGELOG.md` and the
   `v0.1.0` tag inputs follow the Phase 2 walkthrough results.
4. **Second profile + audit cycle** — once Phase 2 manual validation lands,
   run a focused-refresh profile and a focused-diff audit (Phases 1, 6, 8, 10,
   10.5) per `audit/2026-05-21/SUMMARY.md`. Expected outcomes: F-001 to F-007
   smoke-test as `struck`; FF-001 to FF-008 promoted from "proposed" to
   "implemented" (FF-003 remains "deferred"); new dimension scores reflecting
   the closures.

## Deferrals

| Deferred surface | Reason | Trigger to revisit |
|------------------|--------|--------------------|
| `CHANGELOG.md` | Nothing released yet; no tagged history | First tagged release (WP-08 part B) |
| `CODEOWNERS`, PR templates and unrelated GitHub automation | Not needed by the declaration migration | A project-specific need |
| Hosted `verify` qualification and branch enforcement | Specification 1 adoption supplies the activation trigger; source is prepared | Actual hosted checks and effective protection readback |
| Cross-platform CI | Hosted cross-platform *acceptance* remains deferred; `sim-evidence` captures Linux transcripts only and is non-gating | When manual validation stops scaling |
| Slice 3 personas and confusion events (`confused-novice`, mechanical confusion triggers) | The two implemented personas cover the gate and escalation surfaces; confusion modelling needs stable evidence first | After the Phase 2 results |
| FF-003 (STATUS/ROADMAP drift heuristic) | Periodic audit cycles and the manual WP-07 sweep cover it better than a fuzzy CI check | A recurring drift finding |
| Package distribution (Homebrew tap, AUR, etc.) | Single-file script; install is `clone + run` | If users ask for managed install |

## Blockers

- None.

## Decision-Disagreement Rule

If `STATUS.md`, `ROADMAP.md`, and `CONTRIBUTING.md` disagree about
project-level posture, fix the disagreement here first; downstream
documents defer to this file for current truth.
