# Agentic Architecture Audit Package

**Package version:** Audit Spec v3.1 / Profile Directive v1.2
**Package date:** 2026-05-08
**Purpose:** Copy this folder into a project workspace or hand it to a project agent to run the profile and audit workflow.

## Files

| File | Role |
| --- | --- |
| `project-profile-directive.md` | Run this first. Produces the dated `profile/<date>/` snapshot the audit consumes. |
| `agentic-audit-spec-v3.md` | Authority spec for the audit itself. The audit agent must read this in full. |
| `audit-kickoff-prompt.md` | Copy/paste prompt for the audit agent after the profile exists. |
| `audit-spec-friendly-explainer.md` | Human-facing explanation of what the audit does and how to coordinate it. |
| `audit-directive-set-manifest.md` | Version and drift-control manifest for this package. |

## Run Order

1. Place this package in or near the target project workspace.
2. Run `project-profile-directive.md` against the target project.
3. Review the generated `profile/<date>/project_profile.yaml` and `profile/<date>/profile-discovery.md`.
4. Use `audit-kickoff-prompt.md` to start the audit agent.
5. The audit agent must read `agentic-audit-spec-v3.md` and `audit-directive-set-manifest.md` before Phase 0.
6. The audit output lives under `audit/<date>/`; `SUMMARY.md` is written last.

## Authority

The authority texts are:

- `project-profile-directive.md`
- `agentic-audit-spec-v3.md`

The kickoff prompt and friendly explainer are derived guidance. If they conflict with the authority texts, the authority texts win.

## Not Included

The research brief and source MP4 from the working directory are intentionally not included in this package. They informed the v3.1/v1.2 revision, but project agents should not treat them as operational authority during an audit run.
