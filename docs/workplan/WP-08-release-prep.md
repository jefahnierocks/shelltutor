---
title: WP-08 — Release preparation (LICENSE, CHANGELOG, v0.1.0 inputs)
category: planning
component: workplan
status: part-a-ready
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, release, license, changelog, phase4]
priority: medium
---

# WP-08 — Release preparation (LICENSE, CHANGELOG, v0.1.0 inputs)

**Depends on**: operator inputs below; WP-07 recommended before part B.
**Touches `shelltutor`**: one header comment line. **Operator gate**:
**yes** — the inputs below. Part A (steps 1–5) may start once the
copyright line is confirmed; part B (steps 6–8) waits for the Phase 2
results.

- **License**: **MIT** — decided by the operator on 2026-11-07
  (`docs/license-decision.md`). SPDX id `MIT`.
- **Copyright line**: **`Copyright (c) 2026 Jefahnierocks`** — confirmed by
  the operator on 2026-11-07. Part A may start.
- **Phase 2 walkthrough results**: _pending_ (the `STATUS.md` lines for
  macOS Bash 3.2 and a Debian/Ubuntu Bash 5.x host, per
  `docs/phase2-walkthrough-checklist.md`; these come from a human walk,
  not from the harness).

## Goal

Land everything `ROADMAP.md` Phase 4 needs except the tag itself, so the
operator can review and tag. The worker never creates or pushes a tag.

## Read first

- `docs/license-decision.md` §What changes when a license is chosen
  (steps 1–6); `ROADMAP.md` Phase 4; `STATUS.md` Deferrals;
  `README.md` §License Posture; `docs/contracts.md` §Versioning posture.
- `docs/project-manifest.md`: the vendored `project-manifest` MIT license
  is unrelated to this choice; do not touch `vendor/`.

## Steps

**Part A — license adoption** (steps 1–5; commit 1):

1. `LICENSE` at the repo root with the exact OSI MIT text and the
   operator's confirmed copyright line as its first line.
2. `shelltutor` header: one comment line after the title line:
   `# SPDX-License-Identifier: MIT  — see LICENSE`. Nothing else in the
   script changes; `make smoke` structural checks must still pass.
3. `README.md` §License Posture: replace the deferral paragraph with the
   choice, the SPDX id and a link to `LICENSE`.
4. `STATUS.md`: remove the `LICENSE file` deferral row; add a "What Is
   True Now" bullet with the choice and date; add the Phase 2 walkthrough
   lines supplied by the operator; record the distribution decision
   ("clone + run remains the install story" unless the operator says
   otherwise).
5. `docs/license-decision.md`: frontmatter `status: decided`; a dated
   "Decision" section at the top naming the choice.
**Part B — release inputs** (steps 6–8; commit 2; after the Phase 2
results are in):

6. `CHANGELOG.md` (Keep a Changelog shape) with an `Unreleased` heading
   and a `v0.1.0 — <date>` section listing: five-stage curriculum
   (Phase 3), portability fixes F-008/F-009/F-010–F-013, practice-shell
   contract C-007, quality gates FF-001–FF-008, FF-006 ladder through
   rung 1, Specification 1 adoption, Phase 2 walkthrough closure, license
   adoption. Link each item to the relevant doc, not to commits.
7. `ROADMAP.md` Phase 4: mark the license and CHANGELOG criteria met with
   dates; leave "First tagged release" for the operator to tick after
   tagging. Phase 2: mark complete with the walkthrough dates.
8. `docs/contracts.md` §Versioning posture: "After v0.1.0: semver
   applies" becomes effective on tagging; add the date placeholder for
   the operator.

## Acceptance criteria

1. `make verify` passes; `make smoke` structural invariants hold.
2. `./scripts/check-governance.sh` clean (no operator-private paths in
   the new files).
3. `git log` shows the commits below and no tag.

## Commits (in order)

1. `chore(license): adopt MIT — LICENSE, script header, README/STATUS/decision record` (part A)
2. `docs(release): CHANGELOG v0.1.0 section; STATUS and ROADMAP Phase 2/4 closure` (part B)

## Handoff to the operator

The report ends with the exact tag command for the operator to run after
review:

```sh
git tag -a v0.1.0 -m "shelltutor v0.1.0 — working in a Unix shell: five mastery-gated stages, handing off to vimtutor"
```

and the reminder to push the tag only after the hosted `verify` run on the
release commit is green.
