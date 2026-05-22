---
title: shelltutor Status
category: status
component: project-status
status: active
version: 0.1.0
last_updated: 2026-05-21
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
- The tutor script (`shelltutor`) was imported from prior-art at
  `fedora-top:~/Projects/shelltutor` (commit `136f6a3`, 2026-05-17).
- **ROADMAP Phase 1 — User-Agnostic Refactor — is complete** (commit
  `e6257aa`, 2026-05-21).
- **ROADMAP Phase 3 — Curriculum Redesign — is complete** (commit
  `9f61570`, 2026-05-21). shelltutor is a vimtutor-prerequisite
  course delivered as five mastery-gated stages. The script grew from
  459 to 1620+ lines; runs on bash 3.2+, verified under macOS stock
  `/bin/bash 3.2.57`.
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
  (Makefile). 12 fixture-based self-test cases pass locally.
- `.claude/settings.json` carries a PostToolUse shellcheck hook so
  Claude Code sessions get the FF-005 warning immediately on script
  edits.
- The companion `wyn-setup/` directory from prior-art is intentionally
  not carried forward.
- No `LICENSE` or `CHANGELOG.md` file yet (see Deferrals).

## Immediate Next Steps

1. **Portability validation (ROADMAP Phase 2)** — manually walk all
   five mastery-gated stages on macOS with stock `/bin/bash` 3.2 AND
   on a generic Linux distro (Fedora and Debian/Ubuntu families at
   minimum). Record validation date + observed result here. The
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
   before inviting outside contribution or linking the repo publicly.
   Triggers `CHANGELOG.md` creation and `v0.1.0` tag.

## Deferrals

| Deferred surface | Reason | Trigger to revisit |
|------------------|--------|--------------------|
| `LICENSE` file | Not yet chosen; repo is public but default copyright applies | Before inviting contribution or linking publicly |
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
