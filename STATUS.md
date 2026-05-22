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

- **Lifecycle**: foundation / Day-1 scaffold.
- **Semantic owner**: Jefahnierocks (personal workspace).
- **Current host**: local workstation; GitHub remote at
  `github.com/jefahnierocks/shelltutor` (public).
- **Secrets authority**: none required; the tutor handles no secrets.
- **Review cadence**: ad-hoc until a lesson cadence stabilizes.
- **PaC status**: none — no control plane to enforce against.
- **IaC status**: none — no live infrastructure.

## What Is True Now

- Day-1 documentation set (`README.md`, `CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`) is in place.
- The tutor script (`shelltutor`) was imported from prior-art at
  `fedora-top:~/Projects/shelltutor` (commit `136f6a3`, 2026-05-17).
- **ROADMAP Phase 1 — User-Agnostic Refactor — is complete** (commit
  `e6257aa`, 2026-05-21). The tracked script carries no operator-
  named or theme-named content.
- The companion `wyn-setup/` directory from prior-art is intentionally
  not carried forward.
- First profile cycle and first audit cycle are complete (snapshot
  2026-05-21). See `profile/2026-05-21/` and `audit/2026-05-21/SUMMARY.md`.
  Seven active findings (`F-001`–`F-007`) and seven proposed fitness
  functions (`FF-001`–`FF-007`).
- ROADMAP Phase 3 has been expanded into a five-stage mastery-gated
  curriculum spec (vimtutor-prerequisite framing). Implementation is
  the current active engagement.
- No `LICENSE` or `CHANGELOG.md` file yet (see Deferrals).

## Immediate Next Steps

1. **Curriculum redesign implementation (ROADMAP Phase 3)** — implement
   the five mastery-gated stages in `shelltutor` per the spec in
   `ROADMAP.md`. Fixes audit findings `F-002` (narrows the welcome-
   screen sandbox claim) and `F-003` (moves lesson 7 `/proc`+`free` and
   lesson 8 `dnf` install hint out of the gated path).
2. **Portability sweep (ROADMAP Phase 2)** — once Phase 3 lands, walk
   the redesigned stages on macOS with stock `/bin/bash` (3.2) and on
   a generic Linux distro. Record results. Run `make verify` to
   exercise the static-analysis gates locally.
3. **License decision (ROADMAP Phase 4 trigger)** — pick a posture
   before inviting outside contribution or linking the repo publicly.

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
