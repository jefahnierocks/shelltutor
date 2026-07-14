---
title: shelltutor Simulation Slice 2 Sketch
category: planning
component: sim-slice-2
status: draft
version: 0.1.0
last_updated: 2026-07-14
tags: [simulation, slice-2, hardening, pty, planning]
priority: medium
---

# Simulation Slice 2 Sketch

Refinement of `docs/simulation-design-plan.md` §First Three Slices
§Slice 2 ("Practice-Shell Hardening") in light of the Slice 1
evidence committed at `audit/2026-05-23/sim/stage1/`. This sketch
is planning input for the next implementation cycle; it does not
itself change runtime behavior or contracts.

## Slice 1 findings that shape Slice 2

The Slice 1 PTY harness produced two green baselines on macOS
Darwin 25.5.0, Apple Silicon, in ~0.4s per variant. Two findings
came out of it:

1. **F-008 — BSD-sed gate verifier bug** (resolved on `main` as
   commit `a581c1b` before the green baselines were captured).
   The harness's first run found a release-blocking portability
   regression silent since the Phase 3 curriculum rewrite. This
   is the proof point for the plan's "observe before harden"
   discipline — the same discipline that gates Slice 2 on having
   Slice 1 evidence.
2. **`/etc/bashrc` leak signature is null on this host.** The
   `current-rc` and `no-system-rc-preview` baselines differ only
   on per-run sandbox UUID and a date-second offset — see
   `audit/2026-05-23/sim/stage1/diff.md`. On Apple Silicon
   macOS 15.5, sourcing `/etc/bashrc` produces no visible
   transcript change.

The plan's predicted leak signature is a banner or alias injection
that appears in the practice subshell because `/etc/bashrc`
sources distribution-managed files. Apple's bash 3.2.57 ships
without a banner-emitting default `/etc/bashrc`; Linux
distributions typically do.

## What Slice 2 should do (unchanged from the plan)

The plan's `§Practice-Shell Hardening Sequence` still stands as
the implementation skeleton:

1. Stop sourcing `/etc/bashrc` in the `practice()` rcfile (the exact
   `[ -r /etc/bashrc ] && . /etc/bashrc` statement).
2. Replace inherited rc behavior with explicit shell options.
3. Scrub high-risk env vars before the practice subshell starts:
   `INPUTRC`, `CDPATH`, `GLOBIGNORE`, `BASH_ENV`,
   `PROMPT_COMMAND`.
4. Ship a minimal project-controlled Readline config (Tab
   contract: single-Tab complete-or-bell, double-Tab list, no
   menu-cycle).
5. Add `C-007 — Practice-shell environment and Readline behavior`
   to `docs/contracts.md`.
6. Re-run the Slice 1 PTY baseline and compare transcript drift.

## What Slice 2 should do **differently** given Slice 1 evidence

### Reordering: capture Linux baseline before hardening

The plan implicitly expects the `/etc/bashrc` leak signature to
be visible from Slice 1. On macOS Apple Silicon it is not. The
hardening's user-visible payoff is therefore unproven on the
operator's primary host. Before landing Slice 2, run the Slice 1
harness on a Debian/Ubuntu Bash 5.x host and capture the leak
signature there. Two options for that capture:

- **(A) Inline in Phase 2.** The Phase 2 walkthrough already
  requires a Debian/Ubuntu manual walkthrough. The operator runs
  `make lesson-flow` on that host between the human stage runs
  and commits the additional baseline under
  `audit/<date>/sim/stage1-linux/`. This is the cheapest path; a
  single ssh / VM session captures both.
- **(B) As Slice 1.5.** A separate dated commit
  (`docs(sim): linux baseline (Slice 1.5)`) adds the Linux
  evidence bundle. Cleaner provenance, more commits.

Recommendation: **(A)**. The Phase 2 portability walkthrough
already opens a Debian/Ubuntu session; bundling the harness run
into that session is one commit, not two.

### What "compare transcript drift" means in practice

After Slice 2 lands, re-run `make lesson-flow` on:

1. macOS Apple Silicon (current baseline). Expected drift: none
   relative to current `current-rc`, because the macOS leak
   signature was null already. Any drift is from the explicit
   shell-option / env-scrub changes — not the `/etc/bashrc` drop.
2. Debian/Ubuntu (new baseline). Expected drift: the leak
   signature disappears between `current-rc` (with system
   `/etc/bashrc`) and the new post-hardening run. The diff is
   the user-visible payoff.

The post-Slice-2 baselines should be committed alongside the
hardening commit to make the "before/after" reviewable.

### Where the C-007 contract lands

Append a new C-007 section to `docs/contracts.md`. Keep C-004
focused on outer-script env vars; C-007 owns the practice-shell
interactive environment, shell-option, rcfile, and Readline
contract. The contract's stability commitment level can mirror
C-003 (stable for the lifetime of the 5-stage curriculum).

### Lesson-text adjustments (small)

Per the plan's Tab Completion Contract: when Slice 2 ships the
Readline config, lesson 1.1 should mention that Tab behavior
"varies across shells and setups; this tutor is teaching its own
practice-shell behavior, not a universal law of every terminal."
Lesson 1.1 is already a SPLIT candidate per
`audit/2026-05-23/stage1-density.md`; consider whether the Slice 2
copy change is bundled with the 1.1a/1.1b split or done as a
separate commit. Recommendation: separate; the Slice 2 commit
should be hardening-only so the comparison is clean.

## Specific deliverables for Slice 2 (when undertaken)

Per the simulation-design-plan §First Three Slices §Slice 2:

1. Modify the `[ -r /etc/bashrc ] && . /etc/bashrc` statement in
   `practice()` (the exact target already used by the Slice 1 patcher).
2. Add explicit shell-option block in the practice rcfile (e.g.,
   `set -o emacs`, `bind 'set bell-style none'`, etc.).
3. Add an env-var scrub block in the outer script before the
   practice rcfile heredoc runs.
4. Add a minimal `--rcfile`-embedded Readline config (the plan's
   four `set` lines).
5. Document C-007 in `docs/contracts.md`.
6. Re-run Slice 1 harness on both hosts; commit the new evidence
   alongside.
7. Update `STATUS.md` with the Slice 2 completion date.

## Out of scope for Slice 2 (per plan)

- `PATH` reduction. The plan explicitly defers; `--info` covers
  missing-command reporting.
- `COLUMNS` / `LINES` resetting. Capture, do not control.
- Runtime command blocking. Pedagogical containment only;
  `SHELLTUTOR_STRICT=1` remains a future consideration.
- Slice 3 work (confusion events + second persona). Slice 2 is
  hardening-only.

## Risks to watch

- **Over-hardening that breaks lessons.** The plan's "Tab no
  menu-cycle" line is correct in spirit but Readline's actual
  default depends on the operator's `/etc/inputrc` and
  `~/.inputrc`. Slice 2 must verify against the Slice 1 evidence
  that lesson 1.1's Tab demo still works after the env-var scrub
  scrubs `INPUTRC`.
- **Loss of accidental functionality.** If a learner's
  `/etc/bashrc` happens to set a useful alias that the lessons
  expect (e.g., `ls` as an alias for `ls --color=auto`), Slice 2
  removes that. Verify lesson copy doesn't depend on
  distro-managed aliases.
- **Cross-platform drift between macOS (no leak) and Linux
  (leak).** After Slice 2, both hosts should produce equivalent
  transcripts modulo per-run noise. Any residual divergence is a
  finding for a future cycle.

## Cross-references

- `docs/simulation-design-plan.md` §First Three Slices §Slice 2
  — authoritative plan.
- `docs/simulation-design-plan.md` §Practice-Shell Hardening
  Sequence — implementation skeleton.
- `docs/simulation-design-plan.md` §Tab Completion Contract —
  Readline contract details.
- `audit/2026-05-23/sim/stage1/diff.md` — current-rc vs
  no-system-rc-preview baseline diff (the null signature).
- `audit/2026-05-23/findings.md` F-008 — Slice 1's first finding.
- `docs/contracts.md` C-004 — existing env-var contract that
  C-007 will extend.
- `audit/2026-05-23/stage1-density.md` S1-L1 — Tab demo screen
  that interacts with Readline behavior.
