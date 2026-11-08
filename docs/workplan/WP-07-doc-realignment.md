---
title: WP-07 — Documentation realignment sweep
category: planning
component: workplan
status: ready-after-wp05
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, docs, status, consistency, ff-003]
priority: medium
---

# WP-07 — Documentation realignment sweep

**Depends on**: WP-02 through WP-05 (run last; WP-06 and WP-08 may still
be pending). **Touches `shelltutor`**: no. **Operator gate**: none.

## Goal

Make every tracked document agree with the code and with `STATUS.md`
after the cycle's changes. This is the manual stand-in for the deferred
FF-003 drift check; do it with a checklist, not a heuristic.

## Read first

- `STATUS.md` (Decision-Disagreement Rule: fix disagreements there
  first), `ROADMAP.md`, `README.md`, `CONTRIBUTING.md`, `AGENTS.md`,
  `docs/contracts.md`, `docs/phase2-walkthrough-checklist.md`,
  `docs/simulation-design-plan.md`, `docs/sim-slice-2-sketch.md`,
  `scripts/sim/README.md`, `Makefile` header, `project.yaml`.
- `audit/2026-11-07/findings.md` observation O-B.
- The reports of WP-01 to WP-05.

## Cross-document invariants to verify

| Fact | Must agree in |
| --- | --- |
| Lesson count per stage (Stage 1 = 4 after WP-04) | `shelltutor` intro screens, `ROADMAP.md` Phase 3 + Amendments, density audits |
| Where each stage's practice prompt starts (D-04) | `docs/contracts.md` C-003, `shelltutor` header comment, `docs/phase2-walkthrough-checklist.md` |
| Stage 2 gate folder is `$SANDBOX/stage2/practice/` | `docs/phase2-walkthrough-checklist.md` (O-B, corrected 2026-11-07), C-003 |
| Gate verification rules (history checks, escalation) | `ROADMAP.md` Phase 3 Amendments, C-006, `README.md` "Stages" prose |
| Practice-shell contract | C-007, C-004 pointer, `shelltutor` header comment, `README.md` Run section ("Inherited host rc behavior remains a Phase 2/Slice 2 validation and hardening surface" is no longer true after WP-03) |
| Make targets and fitness functions (FF-008, `sim`) | `Makefile` header + `help`, `CONTRIBUTING.md` tables, `AGENTS.md` §Validation, `.claude/settings.json` comment (do not edit the file unless an allow entry is needed) |
| Harness capabilities and exit codes | `scripts/sim/README.md`, `docs/simulation-design-plan.md` Implementation State and Ladder |
| Findings status | `audit/2026-11-07/findings.md`, `STATUS.md` one-liners |
| Phase 2 exit criterion "shellcheck clean" | `ROADMAP.md` Phase 2 (met: `make lint`, hosted verify); the human walkthroughs remain the open criteria |
| `last_updated` and `version` frontmatter | every doc touched in this cycle |
| `project.yaml` `status.as_of` | equal to `STATUS.md` `last_updated`; posture unchanged (`working-prototype`, `unverified`) |

## Specific edits

1. `docs/phase2-walkthrough-checklist.md`: Stage 1 row → the day answer
   may be typed as `date` printed it (after WP-02); add "run `--info`
   first" as an explicit step. (The Stage 2 path, O-B, was corrected on
   2026-11-07.)
2. `ROADMAP.md` Phase 2: confirm the shellcheck and Bash-floor bullets
   still read as done; append dated landing lines under Phase 3
   `### Amendments` for WP-02, WP-04 and WP-05 if a package forgot to;
   leave Phase 2 `(current)` until the human walkthroughs land.
3. `README.md`: Current Shape tree includes `docs/workplan/`; Run section
   mentions `make sim`; delete the "Inherited host rc behavior remains…"
   sentence once WP-03 has landed and replace with a pointer to C-007.
4. `CONTRIBUTING.md`: tables match `Makefile` exactly (run `make help` and
   compare).
5. `scripts/check-governance.sh` `DEFAULT_FILES`: extend to
   `docs/*.md docs/workplan/*.md scripts/sim/README.md` (expand at runtime;
   keep explicit-argument behaviour). Add a self-test fixture only if the
   expansion logic is non-trivial.
6. `STATUS.md`: consolidate "What Is True Now" (sim ladder: FF-006a,
   FF-006b, FF-006c rung 1; Slice 2 complete; FF-008 implemented; findings
   resolved), refresh "Immediate Next Steps" (Phase 2 human walks; second
   profile + audit cycle; license decision), update Deferrals if WP-06
   landed. Keep it current truth, not a backlog.
7. `AGENTS.md` Active Artifacts: add `audit/2026-11-07/findings.md` and
   any new dated audit directories; keep the `docs/workplan/README.md`
   pointer and mark the cycle status there.
8. `docs/workplan/README.md` status table: every WP's status column
   reflects the landed short SHAs.

## Acceptance criteria

1. `make verify` passes (run with the worker protocol's environment
   clearing if inside an agent sandbox).
2. `./scripts/check-governance.sh` with the extended default set is
   clean.
3. A reviewer reading only `STATUS.md` can state the cycle's outcome
   without opening the work plan.

## Commits

1. `docs(sweep): realign checklist, roadmap, readme and contributing after the 2026-11 cycle`
2. `chore(quality): governance check covers docs/ and the harness README (FF-007)`
3. `docs(status): current truth after the 2026-11 cycle; project.yaml as_of`

## Report

Template in `docs/workplan/README.md`; list every invariant row with
"agrees" or the fix applied.
