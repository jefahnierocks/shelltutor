---
title: shelltutor Audit — Phase 0 Scope
category: audit
component: phase-0
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-0, scope, first-cycle]
priority: high
---

# Phase 0 — Scope, Snapshot, and Orientation

## Snapshot Metadata

| Field | Value |
| --- | --- |
| Audit spec | `agentic-audit-spec-v3.1` (2026-05-08) |
| Profile directive | `project-profile-directive-v1.2` (2026-05-08) |
| Audit date | 2026-05-21 |
| Profile snapshot date | 2026-05-21 |
| Profile path | `profile/2026-05-21/project_profile.yaml` |
| Discovery path | `profile/2026-05-21/profile-discovery.md` |
| Current branch | `main` |
| Current revision | `e6257aa420b037139764c1f8f213853bd2574b92` |
| Profile-snapshot revision | `e6257aa420b037139764c1f8f213853bd2574b92` |
| Audit mode | `first-cycle` |

The profile and the audit are anchored to the same revision and the same
calendar date, so the smoke-test in Phase 10.5 will compare current
findings against a snapshot that was captured against the same tree.
This is a pure first-cycle audit; the directive's §1.3 diff-mode and
focused-diff fallbacks do not apply.

## In-scope Deployable Units

One unit, sourced from `profile/2026-05-21/project_profile.yaml`
(`project.deployable_units[]`):

| Name | Path | Kind | Runtime | Entrypoint |
| --- | --- | --- | --- | --- |
| `shelltutor` | `shelltutor` | `cli` | `bash 4+` | `shelltutor` |

## Include / Exclude Paths

**Include** (in-scope for the audit, from `profile.scope.include_paths`):

- `shelltutor` (script, 459 lines)
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `STATUS.md`,
  `ROADMAP.md`
- `.editorconfig`, `.gitignore`

**Exclude** (recorded in `profile.scope.exclude_paths`, plus
`docs/audit/references/` added in Phase 0):

- `.git/`
- `profile/` (the profile snapshot is an *input* to the audit, not an
  audit subject; reading is required, auditing it would be circular).
- `docs/audit/directives/agentic-architecture-audit-v3.1-package/`
  (companion authority texts, tracked separately under
  `governance.companion_artifacts`).
- `docs/audit/references/` (operator-supplied reference materials —
  e.g., `shell-research.md` — used as guidance, not as audit subject;
  see §"Reference materials" below).

## Profile Path Verification (drift check)

Per directive §0 step 3, every profile-cited path must still exist on
the current branch, with drift recorded where it does not.

| Cited path | Status |
| --- | --- |
| `shelltutor` | ✅ present, 459 lines |
| `README.md` | ✅ present, 90 lines |
| `AGENTS.md` | ✅ present |
| `CLAUDE.md` | ✅ present |
| `CONTRIBUTING.md` | ✅ present |
| `STATUS.md` | ✅ present |
| `ROADMAP.md` | ✅ present |
| `.editorconfig`, `.gitignore` | ✅ present |
| `docs/audit/directives/agentic-architecture-audit-v3.1-package/*` | ✅ all six companion files present (placed during profile run) |

No drift between profile-cited paths and current branch state. Profile
revision equals audit-time revision, so file-content drift is zero by
construction.

## Strategic Themes

Sourced from `profile.strategic_themes[]` (operator-interview, Phase G).
Default `multiplier: 1.5`, `dimensions: []` (audit applies §11.12
default mapping where available; otherwise these themes use
operator-specified scope).

### Theme 1 — Single-file portability

- **Default-mapping match**: None — this is a custom theme, not in the
  §11.12 table. Closest analogue is `sdk-extraction` (which weights
  §11.3 Contract discipline) but the project is not preparing for SDK
  release.
- **Audit-assigned weighting**: weights §11.3 (Contract discipline) and
  §11.1 (Bounded contexts) at 1.5×. Rationale: portability for a
  single-file CLI tutor depends on what contracts the script makes with
  the host environment (commands, paths, env vars, exit codes) and on
  whether lessons stay inside the claimed vocabulary boundary
  ("Linux and macOS terminal").
- **Audit-attention flag aligned**: `lesson-portability-gaps` →
  Phase 1.

### Theme 2 — Documentation–code consistency

- **Default-mapping match**: None — custom theme. Closest analogue is
  `legacy-migration` (weights §11.1, §11.2, §11.3). The shelltutor
  concern is narrower: keeping the documentation set in sync with the
  recently-merged refactor.
- **Audit-assigned weighting**: weights §11.10 (Governance and audit
  trail) and §11.8 (Policy/prompt separation) at 1.5×. Rationale:
  governance documents (STATUS.md, ROADMAP.md) currently disagree with
  commit history; skill-or-sop files (AGENTS.md, CLAUDE.md) carry the
  project's safety rules that have no enforcement layer.
- **Audit-attention flag aligned**: `drift-status-roadmap-vs-commit` →
  Phase 1.

## Focus Question

From `profile.scope.focus_question`:

> Does the sandbox-safety claim hold? The tutor tells the learner
> "Everything happens in ~/.shelltutor; you cannot break anything"
> (shelltutor:169) and the practice subshell `cd`s to $SANDBOX and
> sandboxes HISTFILE (shelltutor:109-117), but the subshell is
> otherwise a real interactive bash with the learner's normal
> filesystem authority.

Routed to Phase 6 (authority). The
`subshell-safety-claim-vs-shell-authority` audit-attention flag is the
operator's chosen focus.

## Reference Anchors

See `00-reference-anchors.json` for the machine-readable pin set. The
short version: nearly every anchor listed in spec §14 is `n/a` for this
project because no model-mediated, protocol-mediated, or workflow-
mediated surface exists. The anchors that *do* apply are bash-level:

| Anchor | Pin |
| --- | --- |
| Bash 4+ syntax (local arrays, `(( ))`, `--rcfile`) | Documented requirement in `README.md`; not version-pinned beyond the floor. |
| POSIX userland | Referenced in `AGENTS.md:75-77` ("`bash` and a standard POSIX userland"); no specific POSIX revision pinned. |
| `shellcheck` (optional, deferred) | Mentioned in `CONTRIBUTING.md:34-38`; no version pinned because the project has not yet run a pass. |
| ANSI terminal color (no-color.org) | Referenced in `shelltutor:34` (`NO_COLOR` env var); the [no-color.org](https://no-color.org) convention is the de-facto pin. |

All MCP, A2A, OpenAPI, JSON Schema, OTel semantic conventions
(GenAI/agent/MCP), workflow-description/overlay, provenance standards
(SLSA/C2PA), and computer-use/browser-use sandbox-pattern anchors are
`n/a` for this project — no corresponding surface exists in scope.

## Companion-Document Metadata (drift check)

Per directive §0 step 7, companion docs are checked against the
authority spec version they target.

| File | Target | Drift status |
| --- | --- | --- |
| `docs/audit/directives/agentic-architecture-audit-v3.1-package/project-profile-directive.md` | profile directive v1.2 (2026-05-08) | aligned |
| `docs/audit/directives/agentic-architecture-audit-v3.1-package/agentic-audit-spec-v3.md` | audit spec v3.1 (2026-05-08) | aligned |
| `docs/audit/directives/agentic-architecture-audit-v3.1-package/audit-kickoff-prompt.md` | spec v3.1 + directive v1.2 (2026-05-08) | aligned |
| `docs/audit/directives/agentic-architecture-audit-v3.1-package/audit-spec-friendly-explainer.md` | spec v3.1 + directive v1.2 (2026-05-08) | aligned |
| `docs/audit/directives/agentic-architecture-audit-v3.1-package/audit-directive-set-manifest.md` | manifest (drift-control) | aligned |
| `docs/audit/directives/agentic-architecture-audit-v3.1-package/README.md` | package overview | aligned |

No companion-doc drift. All texts declare the same authority versions
and the same package date.

## Reference Materials (operator-supplied)

- `docs/audit/references/shell-research.md` — operator-supplied
  curriculum-design reference ("Shell Foundations for Vimtutor",
  2026-05-21 copy). Not project authority; used as guidance for
  lesson-surface findings in Phase 1 and Phase 8 where lesson scope vs.
  reference curriculum is structurally relevant.

## Routed Audit-Attention Flags

Sourced from `profile.audit_attention_flags[]`. Each flag's target
audit phase is unchanged from the profile.

| Flag ID | Target phase | Brief |
| --- | --- | --- |
| `drift-status-roadmap-vs-commit` | Phase 1 | STATUS/ROADMAP claim refactor pending; commit log shows it complete. |
| `subshell-safety-claim-vs-shell-authority` | Phase 6 | Sandbox-safety claim breadth vs. actual subshell scope. |
| `lesson-portability-gaps` | Phase 1 | `/proc`, `free`, `sudo dnf install` under a Linux+macOS portability claim. |
| `agents-md-parent-reference-style` | Phase 4 | Parent AGENTS.md cited by absolute machine-local path. |

## Previous-Cycle Conventions

None. `governance.cycle_history_path` is `none` in the profile; no
prior audit exists. `profile/cycle-history.md` will be initialized only
after the operator ratifies entries proposed via
`audit/2026-05-21/cycle-history-notes.md` (Phase 11).

## Boundary Declarations Honored (Phase 0)

- Did not re-run profile discovery. The profile YAML is consumed as
  authoritative for what was *claimed*; the audit tests those claims in
  Phases 1–10.
- Did not expand scope beyond the profile's include set. The
  references directory was added under exclude, not include — it is
  guidance, not subject.
- Did not treat profile claims as findings; flags remain `claimed`
  until phase-specific evidence either confirms or rejects them.
- No profile-vs-code drift to silently discard; revisions match.
- Did not treat companion docs as authority over the spec.

## Exit-Check

| Check | Status |
| --- | --- |
| Scope is bounded and audit mode is recorded | ✅ first-cycle, single-unit scope |
| Every routed audit-attention flag has a target phase | ✅ all four routed |
| Every profile path missing from current branch is listed as drift | ✅ zero drift |
| Strategic themes are recorded or explicitly empty | ✅ two themes recorded |
| Required protocol/semconv/companion-version anchors are pinned or explicitly N/A | ✅ see `00-reference-anchors.json` |

Phase 0 exit check **passes**. Advancing to Phase 1.
