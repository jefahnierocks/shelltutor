---
title: shelltutor Audit — Cycle-History Proposed Updates
category: audit
component: cycle-history-notes
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, cycle-history, proposed-conventions]
priority: medium
---

# Cycle-History — Proposed Updates (First Cycle)

These are proposals only. The audit **does not** edit
`profile/cycle-history.md` directly. The next profile run owns
appending operator-ratified entries (directive v1.2 §I).
`profile/cycle-history.md` does not yet exist; if the operator ratifies
any of the proposals below, the next profile run initializes the file.

Proposals are grouped by the §9 cycle-history.md template categories.

## Active conventions (proposed)

### Audit/profile artifact conventions

1. **Audit-package placement** — Copy authority/companion files for
   the active audit-spec version into
   `docs/audit/directives/<package-name>/` rather than referencing them
   from machine-local `~/Downloads/`. Reproducibility + repo-relative
   citations satisfy the profile directive §7 `governance.companion_artifacts`
   check on any clone.

2. **Operator-supplied references** — Place reference materials the
   audit consults but does not audit (e.g., curriculum docs,
   industry-standard explainers) under `docs/audit/references/` and
   list them in `00-scope.md` under "Reference materials" with
   `applies_to_phases`. Exclude this directory from `scope.include_paths`
   so they are not treated as audit subjects.

3. **Dated snapshot tree** — Two parallel dated trees:
   - `profile/<date>/` for profile artifacts
   - `audit/<date>/` for audit artifacts

   This pairing matches the directive's recommended layout and keeps
   each cycle's evidence self-contained.

### Score-with-context conventions

4. **Score 0 with context for absent-by-design surfaces** — When the
   §11 rubric scores 0 on a dimension because the underlying surface
   is absent and absence is appropriate for project lifecycle
   (Day-1 scaffold, no agentic runtime, no production deployment),
   record the score honestly **and** record `score_context` explaining
   the absence. The aggregate score remains informational; the
   `score_context` is the operative communication. Applied here at
   11.2 (vacuous 3), 11.4 (vacuous 3), 11.7 (0), 11.9 (0), 11.11 (0).

5. **Vacuous 3 vs honest 0** — When a dimension would score 3 only
   because the underlying surface is absent (e.g., 11.4 Tool/action
   surface clarity in a project with zero tools), record the vacuous
   3 with the same `score_context` mechanism. Do not collapse
   vacuous-3 and honest-3 in the priority-weighting step.

### Fitness-function conventions

6. **Fitness functions enforceable without CI** — For projects with
   intentional no-CI posture (e.g., shelltutor's
   CONTRIBUTING.md:72-75), propose fitness functions enforceable via
   pre-commit hook, `Makefile` target, or manual-review checklist
   **before** demoting to `manual-review-only`. CI activation, when
   it comes, picks up the same checks unchanged.

7. **Demotion path documented in the FF entry** — When a fitness
   function's enforcement tech might be unavailable, the FF entry
   itself records the demotion path (e.g., FF-006's "demote full
   lesson-flow to manual-review-only; retain minimal -h variant as
   static-analysis"). Phase 10.5 then applies the demotion based on
   evidence rather than re-deriving the path.

### Contract conventions

8. **`ad-hoc` is an honest classification for single-file CLIs** —
   For projects with one executable + zero public SDK + zero
   protocol surfaces, the §8.5 Contract.format value `ad-hoc` is the
   correct classification and is not by itself a finding. Phase 4
   records it; Phase 10 evaluates whether formalization is warranted
   for the lifecycle stage.

### Operator-focus-question conventions

9. **Route operator focus to the natural phase via profile flag** —
   When the operator names a focus question (`scope.focus_question`),
   route it via a profile `audit_attention_flag` to its natural
   audit phase. The audit then lifts the flag into a Phase 10
   finding without losing the operator's framing. Applied here:
   `subshell-safety-claim-vs-shell-authority` profile flag →
   Phase 6 → finding F-002.

## Branching and PR conventions

(No proposals — current AGENTS.md/CONTRIBUTING.md rules cover branching
and PR posture and were not contradicted by audit evidence.)

## Commit and verification conventions

(No proposals — Conventional Commits, linear history, focused changes
already in place at AGENTS.md:83-86 and CONTRIBUTING.md:19-22.)

## ADR conventions

(No proposals — no ADRs currently exist and ROADMAP does not call for
them. If the operator decides to introduce ADRs, the v3.1 spec's
"Decides / Scopes to / Does not decide / Carve-outs" template should
be considered as the format.)

## Halt and rescope conventions

(No halts triggered this cycle. No proposals.)

## Agent caveat conventions

10. **Caveat type per §9.6 in every finding** — Findings should
    declare `substantive-deviation` vs `cosmetic-or-framing-deviation`
    vs `exact-match` explicitly. Applied here at F-005
    (cosmetic-or-framing) vs F-001..F-004, F-006, F-007 (substantive).

## Per-cycle log (proposed format)

```markdown
### 2026-05-21 — first cycle

- Adopted: audit-package placement under docs/audit/directives/; operator
  references under docs/audit/references/.
- Adopted: dated parallel trees profile/<date>/ + audit/<date>/.
- Adopted: score-0-with-context for absent-by-design surfaces.
- Adopted: vacuous-3 distinct from honest-3 in score context.
- Adopted: fitness functions enforceable without CI (pre-commit/Makefile/
  checklist) before demotion to manual-review-only.
- Adopted: demotion path documented in the FF entry itself.
- Adopted: ad-hoc classification is honest for single-file CLIs.
- Adopted: route operator focus question to natural phase via profile flag.
- Adopted: caveat type (§9.6) declared explicitly in each finding.
- Open question for next cycle: when ROADMAP Phase 2 (portability
  validation) lands, should manual-walkthrough results be recorded in
  STATUS.md or in a new docs/validation-log.md?
- Open question for next cycle: when ROADMAP Phase 4 (release posture)
  lands, what build/source-provenance position will the project adopt?
```

## Boundary Declarations Honored

- These are **proposals**. The audit does not commit them to
  `profile/cycle-history.md`. The next profile run owns ratification
  (directive v1.2 §I).
- No unreviewed agent-derived conventions are appended; every proposal
  cites an audit-cycle origin.
- No transcript dumps; each entry is a short, durable convention
  statement.
