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
- The tutor script (`shelltutor`) has been imported from prior-art at
  `fedora-top:~/Projects/shelltutor` (commit `136f6a3`, 2026-05-17).
- The imported script still carries two `WYN OPS` accent comments
  (lines 17 and 35); user-agnostic refactor is the next change.
- The companion `wyn-setup/` directory from prior-art is intentionally
  not carried forward.
- No `LICENSE` or `CHANGELOG.md` file yet (see Deferrals).

## Immediate Next Steps

1. **User-agnostic refactor commit** — replace `WYN OPS` accent comments
   with neutral wording; sweep for any other user-specific framing.
2. **Portability sweep** — confirm the script behaves on macOS (Homebrew
   bash 5+) and a generic Linux. Note which surfaces are validated.
3. **Lesson surface review** — decide whether the initial command list
   (`pwd`, `ls`, `cd`, `cat`, `man`, `whoami`, `hostname`, `date`,
   `uptime`, `df`, `free`) is the right Day-1 set.
4. **License decision** — pick a posture before inviting outside
   contribution or linking the repo publicly.

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
