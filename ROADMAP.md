---
title: shelltutor Roadmap
category: planning
component: roadmap
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [roadmap, phases, planning]
priority: medium
---

# Roadmap

Phase sequence for `shelltutor`. Each phase closes when its exit criteria
hold; sequence is intentionally linear so the tutor stays inspectable.

## Phase 0 — Day-1 Scaffold (current)

Goal: land the project shell with documentation set, imported prior-art
script, and a published public remote.

Exit criteria:

- Day-1 docs in place (`README`, `CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`).
- Prior-art script imported with provenance commit.
- GitHub remote published.
- Workspace shell records the project in `STATUS.md` and `.gitignore`.

## Phase 1 — User-Agnostic Refactor

Goal: strip all user-specific framing from the imported script so the
tutor honors its core property.

Work:

- Replace `WYN OPS` accent comments with neutral language.
- Sweep for hostname, operator-name, distro-specific, or prompt-theme
  assumptions.
- Confirm the tutor's output never names a specific operator or host.

Exit criteria:

- No grep hits for user-specific or operator-private vocabulary in tracked
  files.
- Tutor runs cleanly on a clean account with no prior shelltutor history.

## Phase 2 — Portability Validation

Goal: confirm the tutor runs correctly on macOS and Linux without
environment assumptions.

Work:

- Validate on macOS with Homebrew bash 5+.
- Validate on a generic Linux distro (Fedora and Debian/Ubuntu families
  at minimum).
- Document any bash version floor.
- Add a `shellcheck` pass; resolve or annotate findings.

Exit criteria:

- Documented run instructions for macOS and Linux, both validated.
- `shellcheck` clean (or each suppression justified).

## Phase 3 — Lesson Surface Review

Goal: decide whether the initial command set is the right Day-1 surface
and what to add next.

Work:

- Review the current lesson list against a "first 15 commands" frame.
- Identify gaps (e.g., file viewing pager, basic redirection,
  globbing) and decide which belong in this tutor versus a follow-on.
- Make lessons individually addressable so a learner can jump to one
  without replaying earlier lessons.

Exit criteria:

- Lesson list and order documented in `README.md`.
- Lessons jump-addressable from the tutor's menu.

## Phase 4 — Release Posture

Goal: choose a license, cut a tagged release, decide on distribution.

Work:

- License decision (see `STATUS.md` deferral).
- Create `CHANGELOG.md` and tag `v0.1.0`.
- Decide whether managed distribution (Homebrew tap, AUR, etc.) is worth
  the maintenance cost or whether `clone + run` stays the install story.

Exit criteria:

- `LICENSE` present, posture clear.
- First tagged release.
- Distribution decision recorded in `STATUS.md`.

## Out Of Scope

- Shell scripting tutorials (a separate project, if any).
- Sysadmin curriculum.
- Multi-user / classroom features.
- Network-aware lessons.
- Anything that requires the learner to install something beyond `bash`.
