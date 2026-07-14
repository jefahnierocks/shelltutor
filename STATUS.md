---
title: shelltutor Status
category: status
component: project-status
status: active
version: 0.1.0
last_updated: 2026-07-14
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
- Root `project.yaml` v0.1 projects this file into meta-inventory as a
  public-available, linkable working prototype. It deliberately carries no
  deployed-system or operational-state claim.
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
- The companion `wyn-setup/` directory from prior-art is intentionally
  not carried forward.
- No `LICENSE` or `CHANGELOG.md` file yet (see Deferrals).

## Immediate Next Steps

1. **Portability validation (ROADMAP Phase 2)** — manually walk all
   five mastery-gated stages on macOS with stock `/bin/bash` 3.2 and
   on a Debian/Ubuntu-family Linux host with Bash 5.x. The no-TTY negative
   test is recorded above; Fedora-family validation is optional. Record the
   walkthrough dates + observed results here. The
   static checks (`make verify`) confirm the script's invariants; the
   manual walkthrough confirms the human-facing experience.
2. **Second profile + audit cycle** — once Phase 2 manual validation
   lands, run a focused-refresh profile and a focused-diff audit
   (Phases 1, 6, 8, 10, 10.5) per the cadence recommended in
   `audit/2026-05-21/SUMMARY.md`. Expected outcomes:
   - F-001..F-007 smoke-test as `struck` (no longer supported by
     current evidence)
   - FF-001..FF-007 promoted from "proposed" to "implemented"
     (FF-003 remains "deferred")
   - new dimension scores per §11 reflecting the closures
3. **License decision (ROADMAP Phase 4 trigger)** — pick a posture
   before inviting outside reuse or contribution and before a tagged release.
   Triggers `CHANGELOG.md` creation and `v0.1.0` tag.

## Deferrals

| Deferred surface | Reason | Trigger to revisit |
|------------------|--------|--------------------|
| `LICENSE` file | Not yet chosen; repo is public but default copyright applies | Before inviting outside reuse/contribution or tagging a release |
| `CHANGELOG.md` | Nothing released yet; no tagged history | First tagged release |
| GitHub-side automation (workflows, `CODEOWNERS`, PR templates, branch protection) | Workspace posture defers these until a real trigger exists | Real activation trigger |
| Cross-platform CI | Same as above; manual validation suffices for now | When manual validation stops scaling |
| Package distribution (Homebrew tap, AUR, etc.) | Single-file script; install is `clone + run` | If users ask for managed install |

## Blockers

- None.

## Decision-Disagreement Rule

If `STATUS.md`, `ROADMAP.md`, and `CONTRIBUTING.md` disagree about
project-level posture, fix the disagreement here first; downstream
documents defer to this file for current truth.
