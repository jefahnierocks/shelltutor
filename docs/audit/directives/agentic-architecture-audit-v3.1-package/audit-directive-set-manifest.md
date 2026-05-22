# Audit Directive Set Manifest

**Manifest date:** 2026-05-08
**Status:** Companion drift-control manifest

This manifest records the intended relationship among the directive-set files in this directory. The authority texts are the profile directive and audit specification. The kickoff prompt and friendly explainer are derived guidance and must be updated when the authority texts change.

## Authority Texts

| File | Role | Current target |
| --- | --- | --- |
| `project-profile-directive.md` | Profile snapshot authority | Project Profile Discovery Directive v1.2, 2026-05-08 |
| `agentic-audit-spec-v3.md` | Audit authority | Agentic Architecture Audit Specification v3.1, 2026-05-08 |

## Derived Companions

| File | Role | Must target |
| --- | --- | --- |
| `audit-kickoff-prompt.md` | Copy/paste operational prompt for audit agents | Audit Spec v3.1 and Profile Directive v1.2 |
| `audit-spec-friendly-explainer.md` | Operator-facing explainer | Audit Spec v3.1 and Profile Directive v1.2 |

## Research Source

| File | Role | Treatment |
| --- | --- | --- |
| `recent-research.md` | Current research brief used for v3.1/v1.2 modernization | Not bundled in this package; input evidence only, not an authority text |
| `Untangling_AI_Architecture.mp4` | Supporting source material present in the original working directory | Not bundled in this package and not consumed by this revision unless separately transcribed or cited |

## Drift Check

Before publishing a new directive-set revision:

1. Confirm `project-profile-directive.md` and `agentic-audit-spec-v3.md` declare the intended versions and dates.
2. Confirm `audit-kickoff-prompt.md` and `audit-spec-friendly-explainer.md` declare the same target authority versions.
3. Search all markdown files for stale prior-version references, old filenames, and outdated section numbers.
4. Confirm companion docs do not introduce rules that contradict the authority texts.
5. If the authority spec changes behavior, update this manifest and the derived companions in the same revision.

## v3.1 / v1.2 Revision Intent

This revision preserves the v3 audit philosophy and adds targeted coverage for:

- protocol-specific contract surfaces, especially MCP and A2A;
- workflow descriptions, overlays, schema dialects, and protocol versions;
- background, paused, resumable, durable, callback-mediated, and event-triggered execution;
- authority matrices covering approval mode, precedence, bypass modes, protected paths, secondary credentials, callbacks, hosted/local boundaries, and token delegation;
- separate state and memory classes;
- separate runtime/action, content, and build/source provenance classes;
- semantic-convention version and stability pinning;
- server-exposed prompts and privileged-context injection boundaries;
- eval coverage for protocol surfaces, approval paths, async lifecycle, and memory lifecycle.
