---
title: shelltutor LICENSE Decision Options
category: planning
component: license-decision
status: draft
version: 0.1.0
last_updated: 2026-05-23
tags: [license, phase4, planning, decision-pending]
priority: medium
---

# LICENSE Decision Options (Phase 4)

`shelltutor` is currently published under default copyright (no
`LICENSE` file). The repo is public at
`github.com/jefahnierocks/shelltutor` but external reuse is not
granted until a license is chosen. This document surfaces the
options and tradeoffs so the operator can decide deliberately.

**Status: decision pending.** This document does not pick a
license. It is an input to Phase 4 of `ROADMAP.md`, which gates
the first tagged release (`v0.1.0`) and the creation of
`CHANGELOG.md`.

## Constraints to honor

The project's identity (`AGENTS.md` §Identity) and the Phase 3
exit criteria put real bounds on which licenses are coherent:

- **Single-file portable bash tutor.** The redistribution surface
  is one executable script. A license whose obligations require
  shipping a separate notice file alongside every copy adds
  friction to the "clone + run" install story.
- **User-agnostic / safe on a stranger's machine.** The script is
  intended to be inspected and run by readers who may not be
  programmers. Friction-heavy license headers in the script
  header itself can hurt readability.
- **No outside contribution invited yet.** The license choice can
  be made on the operator's authority alone; no community CLA is
  needed.
- **Educational positioning.** The tutor is a learning artifact;
  permissive licensing aligns with the "anyone can read, run, and
  borrow ideas" posture.

## Candidate licenses

### MIT

- **Pros**: Shortest text. Strongly recognized. Compatible with
  almost everything downstream. Single-file projects often inline
  the MIT notice in a top comment plus a `LICENSE` file at the
  repo root.
- **Cons**: No explicit patent grant. (Low risk for a bash tutor;
  no patentable subject matter.)
- **Friction for single-file reuse**: A reader who copies
  `shelltutor` into their own repo can include the MIT header in
  a comment block; no separate file required for compliance.

### Apache-2.0

- **Pros**: Explicit patent grant; widely-respected for projects
  intended for institutional adoption.
- **Cons**: Longer text. The NOTICE-file requirement is mild but
  non-zero overhead. Comment-block license headers in
  redistribution become bulkier than MIT.
- **Friction for single-file reuse**: A reader copying the script
  needs to include the Apache header, which is several lines —
  acceptable but heavier than MIT.

### BSD-2-Clause / BSD-3-Clause

- **Pros**: Permissive, similar to MIT in spirit.
- **Cons**: Less common in educational projects; no real
  advantage over MIT for this surface.

### CC0 (Public Domain Dedication)

- **Pros**: Maximally permissive; no obligations.
- **Cons**: Not a recognized license in some jurisdictions
  (CC0's public-domain dedication is treated as a fallback license
  in countries that don't recognize voluntary surrender to the
  public domain). Some package ecosystems (e.g., Debian's
  ftpmaster team) flag CC0 because of patent-grant ambiguity.
  Loses normal author-attribution courtesy.
- **Friction for single-file reuse**: zero, except the
  jurisdictional ambiguity.

### GPL-3.0 / AGPL-3.0

- **Pros**: Copyleft preserves the "everyone gets to learn from
  this" intent if a future fork tries to close the source.
- **Cons**: Strong compatibility constraints. A reader who copies
  any meaningful portion of `shelltutor` into a permissively-
  licensed project must relicense the combined work as GPL —
  high friction for the educational "borrow ideas" use case.
  Also: AGPL is overkill for a CLI tutor that does not run as a
  network service.
- **Friction for single-file reuse**: high; arguably misaligned
  with the project's positioning.

### Unlicense

- **Pros**: Like CC0, maximally permissive; widely used.
- **Cons**: Same jurisdictional concerns as CC0; less mature
  legal recognition than MIT.

## Lean (operator decides)

The shape of the project — single-file, permissive, educational,
friction-averse — points toward **MIT** as the conservative
default and **Apache-2.0** as the alternative if patent-grant
explicit-ness becomes a future concern.

CC0 / Unlicense are tempting but the jurisdictional ambiguity is
worse for a project that wants to be unambiguously safe to copy.

GPL is misaligned with the "borrow ideas" educational intent for
a one-file shell script.

This document is not making the decision; it just records the
tradeoffs.

## What changes when a license is chosen

Once the operator decides, the following land in one or two
commits:

1. `LICENSE` file at repo root, with the canonical text of the
   chosen license, the operator's copyright line (e.g.,
   "Copyright (c) 2026 Jefahnierocks").
2. Top-of-script header in `shelltutor` updated to point at the
   `LICENSE` file (one comment line — keep the script readable).
3. `README.md` "License Posture" section rewritten from the
   current "deferral" wording to the active choice + link.
4. `STATUS.md` "Deferrals" table: remove the `LICENSE file` row;
   add a "What Is True Now" bullet noting the choice and date.
5. `CHANGELOG.md` created with a `v0.1.0` section that includes
   the license adoption and the Phase 2 walkthrough closure.
6. Git tag `v0.1.0`.

Steps 5 and 6 are the explicit Phase 4 exit per `ROADMAP.md`.

## Cross-references

- `ROADMAP.md` Phase 4 — exit criteria.
- `STATUS.md` "Deferrals" — current state.
- `README.md` "License Posture" — current wording.
- `AGENTS.md` §Identity — project posture this decision must honor.

## Out of scope for this document

- Contribution licensing (CLA / DCO) — defer until external
  contribution is actually invited; not a Phase 4 requirement.
- Trademark posture for the name `shelltutor` — not a copyright
  question.
- Patent grant strategy beyond license choice — single-file bash
  tutor has no patentable surface; this is informational only.
