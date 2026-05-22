---
title: shelltutor Audit — SUMMARY (first cycle)
category: audit
component: summary
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, summary, first-cycle]
priority: high
---

# shelltutor Audit — SUMMARY (first cycle)

| Field | Value |
| --- | --- |
| Audit spec | `agentic-audit-spec-v3.1` (2026-05-08) |
| Profile directive | `project-profile-directive-v1.2` (2026-05-08) |
| Audit mode | `first-cycle` |
| Profile snapshot date | 2026-05-21 |
| Audit date | 2026-05-21 |
| Current branch | `main` |
| Current revision | `e6257aa420b037139764c1f8f213853bd2574b92` |
| Profile-snapshot revision | same |
| Halts triggered | 0 |
| Stale findings (Phase 10.5) | 0 / 7 |
| Recommended next cadence | **post-refactor or release-gated** (the operator left `scope.audit_cadence: unknown` in the profile; the audit's recommendation is to re-run after the four `priority ≥ 2` findings are remediated, then again before the first tagged release per ROADMAP Phase 4) |

## Score Table (§11 rubric, 0–3)

| Dimension | Score | Context |
| --- | ---: | --- |
| 11.1 Bounded contexts | 2 | one confirmed context; vocabulary mostly coherent; "user-agnostic" / "portable" / "WYN OPS" collisions |
| 11.2 Domain/application | 3 | vacuous — no domain plane to leak into; nothing to score |
| 11.3 Contract discipline | 1 | six de-facto `ad-hoc` contracts; appropriate for project scope |
| 11.4 Tool/action surface | 3 | vacuous — no tools in the agent sense |
| 11.5 State and memory | 2 | five stores classified; one gap (subshell scope claim) — F-002 |
| 11.6 Authority | 2 | three contributor-side gates; one runtime claim mismatch — F-002 |
| 11.7 Observability | 0 | absent-by-design; no agentic runtime to instrument |
| 11.8 Policy / prompt | 2 | AGENTS.md skill-or-sop carries safety policy without code enforcement — F-004 |
| 11.9 Evals | 0 | absent-by-design; Day-1 scaffold; ROADMAP Phase 2 quality gates pending |
| 11.10 Governance | 2 | comprehensive docs; STATUS/ROADMAP drift — F-001 |
| 11.11 Fitness functions | 0 | none exist; seven proposed (FF-001..FF-007) |

**Lowest dimensions: 11.7, 11.9, 11.11 (all 0).** All three are
absent-by-design at the Day-1 lifecycle stage; the score should be
read with `score_context` (see `10-scores.json`). Strategic themes do
not weight any of these to 1.5×, so they do not dominate the
priority ranking.

## Findings (Phase 10.5 smoke-tested, all `confirmed-current`)

Priority = severity × confidence × strategic_weight × reversibility_factor.

| # | ID | Title | Priority | Caveat |
| --- | --- | --- | ---: | --- |
| 1 | F-001 | Documentation drift: STATUS/ROADMAP claim user-agnostic refactor pending; commit `e6257aa` shows complete | 3.0 | substantive |
| 1 | F-002 | Welcome-screen sandbox claim broader than the practice subshell actually sandboxes | 3.0 | substantive |
| 1 | F-003 | Lesson 7 (`/proc`, `free -h`) and lesson 8 (`sudo dnf install`) under a Linux+macOS portability claim | 3.0 | substantive |
| 4 | F-004 | Safety policy rules in AGENTS.md have no code-level enforcement | 2.16 | substantive |
| 5 | F-007 | De-facto external contracts lack formal schemas | 1.2 | substantive |
| 6 | F-005 | `AGENTS.md:22` cites parent workspace by absolute machine-local path | 1.0 | cosmetic-or-framing |
| 6 | F-006 | No automated eval / smoke / regression coverage | 1.0 | substantive |

Three findings tie at priority 3.0; the operator may resolve the tie
at planning time. The natural triage order is **F-001 → F-002 → F-003**
because F-001 is documentation-only (lowest cost, immediate), F-002 is
a one-line text change in the script, and F-003 needs ~30 lines of
lesson rework or a narrowing of the portability claim.

## Strategic Themes

| Theme | Multiplier | Findings advancing the theme | Findings directly observed |
| --- | --- | --- | --- |
| Single-file portability | 1.5× | F-003 (direct), F-007 (indirect) | yes |
| Documentation–code consistency | 1.5× | F-001 (direct), F-004 (indirect) | yes |

Both themes are exemplified by direct evidence in Phase 1, Phase 6,
and Phase 8 artifacts.

## Profile / Current-Branch Drift

| Class | Result |
| --- | --- |
| Profile-cited paths missing from current branch | 0 |
| Source-file content drift between snapshot and current | 0 |
| Companion-document drift | 0 — all six companion files align on audit spec v3.1 / profile directive v1.2 (2026-05-08) |
| Smoke-test outcome distribution | 7 / 7 `confirmed-current`; 0 `re-evidenced`, `reclassified`, `promoted`, `demoted`, `struck`, `drift-only`, or `not-run` |

The snapshot and the audit run against the same revision on the same
calendar date; this is the cleanest drift posture possible.

## Proposed Fitness Functions (Phase 10)

| ID | Title | Category |
| --- | --- | --- |
| FF-001 | Safety-rule static analysis on `shelltutor` | static-analysis |
| FF-002 | Write-scope static analysis on `shelltutor` | static-analysis |
| FF-003 | Documentation-code drift check (STATUS/ROADMAP vs git log) | companion-doc-drift |
| FF-004 | Lesson portability check (gate-and-fallback per CONTRIBUTING.md:51-54) | static-analysis |
| FF-005 | `shellcheck shelltutor` clean pass | static-analysis |
| FF-006 | Lesson-flow smoke test (full variant `manual-review-only` per FF-006 demotion path; `-h` minimal variant `static-analysis`) | eval-coverage |
| FF-007 | Avoid absolute machine-local paths in governance citations | companion-doc-drift |

All seven are enforceable as pre-commit hook / `Makefile` target /
manual-review checklist under the project's bash-only + POSIX-userland
constraint (AGENTS.md:75-78). CI activation per the workspace posture
(CONTRIBUTING.md:72-75) is deferred; the same checks become CI checks
unchanged when activation arrives.

## Caveats and Halt/Resume History

- **No halts triggered.** All §4.1 halt conditions were checked at
  Phase 0 and at each phase boundary; none apply.
- **Caveat — F-002 remediation is text-based.** Narrowing the
  welcome-screen claim is operator-judgment-bound (what wording matches
  the actual sandboxing without losing the lesson's reassurance
  function for beginners). FF-002 covers code; F-002 needs a doc
  change.
- **Caveat — F-006 score 0 is honest, not a finding bar.** The
  project intentionally lacks agentic evals at Day-1 lifecycle; the
  score reflects rubric application, not a regression to fix urgently.
  The pre-Phase-2 manual walkthrough that ROADMAP plans is the
  appropriate next quality gate.
- **Caveat — FF-006 demotion is documented in advance.** Full lesson-
  flow pty harness is outside the bash-only runtime constraint; the
  FF-006 entry records the demotion to manual-review-only for the
  full variant. The minimal `-h` smoke remains static-analysis.

## Recommended Next Audit Cadence

The operator left `scope.audit_cadence: unknown` in the profile. The
audit's recommendation, derived from the priority distribution and
the project lifecycle:

1. **After remediating F-001 / F-002 / F-003** (the three priority-3.0
   findings), run a `focused-refresh` profile and a `focused-diff`
   audit covering Phases 1, 6, 8, 10, 10.5. This validates the
   remediations and re-scores the affected dimensions.
2. **Before the first tagged release (ROADMAP Phase 4)**, run a full
   `steady-state` audit. The release pipeline opens build/source
   provenance and the LICENSE choice as new audit surface.
3. **At lesson-surface expansion (ROADMAP Phase 3)**, re-run Phase 1
   (vocabulary), Phase 4 (contracts — lesson IDs become a new
   contract), Phase 8 (any new lesson copy), Phase 10 prioritization.

## Pointer to Detailed Phase Artifacts

```text
audit/2026-05-21/
  00-scope.{md,json}
  00-reference-anchors.json
  01-vocabulary.{md,json}
  02-context-map.{md,mmd}
  02-contexts.json
  03-runtime.{md,json}
  03-loops/EP-LOOP-001-main-dispatcher.mmd
  04-contracts.{md,json}
  05-state.{md,json}
  06-authority.{md,json}
  07-observability.{md,json}
  08-policy.{md,json}
  08-prompt-surfaces.json
  09-evals.{md,json}
  10-findings.{md,json}
  10-scores.json
  10-fitness-functions.{md,json}
  10.5-finding-smoke-test.{md,json}
  cycle-history-notes.md
  SUMMARY.md                     # this file
```

Profile inputs (also in-tree):

```text
profile/2026-05-21/
  project_profile.yaml
  profile-discovery.md
```

Authority spec (also in-tree, per Phase 0 placement decision):

```text
docs/audit/directives/agentic-architecture-audit-v3.1-package/
  agentic-audit-spec-v3.md
  audit-directive-set-manifest.md
  audit-kickoff-prompt.md
  audit-spec-friendly-explainer.md
  project-profile-directive.md
  README.md
docs/audit/references/
  shell-research.md
```
