---
title: shelltutor Audit — Phase 4 Contract Inventory
category: audit
component: phase-4
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-4, contracts]
priority: high
---

# Phase 4 — Contract Inventory

shelltutor exposes no machine-readable schemas, no protocol surfaces,
and no public SDK. What it *does* expose is a small set of **de-facto
contracts** with human consumers (the learner and the contributor) and
process-internal consumers (the practice subshell, the main loop).
Each is recorded honestly as `ad-hoc` per the §8.5 Contract schema's
`format` enum.

The profile audit-attention flag `agents-md-parent-reference-style` is
routed here. It is addressed below under "Cross-document authority
references."

## Inventoried Contracts

### C-001 — CLI argument shape

| Field | Value |
| --- | --- |
| Name | `shelltutor CLI args` |
| Format | `ad-hoc` (informal `case` statement; no man page; no `--help` parser library) |
| Surface | `cli` |
| Location | `shelltutor:415-428` (argument parsing); `shelltutor:53-64` (help text) |
| Versioning | `none` |
| Schema dialect | n/a |
| Protocol version | n/a |
| Advertised capabilities | `<empty>`, `1..9`, `-h\|--help` |
| Auth scheme | n/a |
| Producer | `shelltutor` (the script itself) |
| Consumers | the operator invoking `./shelltutor`; secondary: the learner who reads the help text |
| Validation | inline `case` statement; emits a stderr error and `exit 1` for anything outside `[1-9]\|''\|-h\|--help` (shelltutor:425-428) |
| Compatibility policy | none documented |
| Flags | `route-without-spec` (this is the closest match — the CLI surface has no formal spec like a man page or `--help` autogen) |

**Evidence:**

- `shelltutor:53-64` — `usage()` heredoc with usage lines.
- `shelltutor:415-428` — `case "${1:-}" in -h\|--help) ... [1-9]) ... *) echo \"shelltutor: lesson must be 1 through 9.\" >&2; ... esac`.

Severity: low (this is appropriate for a single-file CLI tutor; no
public SDK consumer exists). Captured as a Phase 4 observation; will
be promoted to a finding in Phase 10 only if Phase 9 / Phase 8
analysis surfaces a need.

### C-002 — Practice subshell exit-code protocol

| Field | Value |
| --- | --- |
| Name | `practice() exit codes` |
| Format | `ad-hoc` |
| Surface | `cli` (internal) |
| Location | `shelltutor:120-131, 136-141` |
| Versioning | `none` |
| Producer | the practice subshell's overridden `next/prev/show/quit/exit` functions |
| Consumers | `practice()` (which exits 0 from outside if rc=99) and the outer `for` loop (which uses `case` on `$?` for 97/98) |
| Validation | implicit (only the four named overrides return non-zero; any other normal subshell exit returns the bash default) |
| Flags | none — small internal protocol with documented in-comment intent (shelltutor:120-130) |

**Evidence:**

- `shelltutor:120-130` — comment block explaining the codes:
  - `0 = next`, `97 = show`, `98 = prev`, `99 = quit`.
- `shelltutor:135-141` — `practice()` interprets rc=99 specifically.
- `shelltutor:444-449` — outer loop's `case "$rc" in 97) ((i--)) ;; 98) i=$((i > 0 ? i - 2 : -1)) ;;`.

This is the closest thing to a typed contract in the project. Honest
classification: `ad-hoc` with strong in-comment documentation.

### C-003 — `$SANDBOX` file layout

| Field | Value |
| --- | --- |
| Name | `shelltutor sandbox file layout` |
| Format | `ad-hoc` (filesystem layout) |
| Surface | `persisted-format` |
| Location | `shelltutor:30-32, 66-80, 82-93, 109-117, 452-456` |
| Versioning | `none` |
| Producer | `setup_sandbox()` writes fixtures; `save_progress()` writes the progress file; the practice subshell appends to `.shelltutor_history` |
| Consumers | `read_progress()`; the practice subshell's `cd $SANDBOX` + `HISTFILE=…`; lesson heredocs that refer to `poem.txt` and `numbers.txt` by relative path |
| Validation | `read_progress()` enforces integer regex (`[[ "$n" =~ ^[0-9]+$ ]] \|\| n=0`) on the progress file (shelltutor:88-92); other files are unvalidated content |
| Flags | `persisted-format-without-versioning` — the sandbox layout is not versioned. If a future change renamed a fixture or moved the progress file, existing sandboxes could surface stale content. Low severity for a Day-1 scaffold; raise on next cycle if the layout changes. |

**Evidence:**

- `shelltutor:30-32` — `SANDBOX`, `PROGRESS_FILE` constants.
- `shelltutor:66-80` — `setup_sandbox()` creates `poem.txt`, `numbers.txt`, `.shelltutor_history`.
- `shelltutor:82-93` — `save_progress()`, `read_progress()`.
- `shelltutor:111-116` — `HISTFILE` and history options inside the practice subshell.

### C-004 — Environment-variable inputs

| Field | Value |
| --- | --- |
| Name | `shelltutor environment variables` |
| Format | `ad-hoc` |
| Surface | `config` |
| Location | `shelltutor:30, 34, 109` |
| Versioning | `none` |
| Producer | the operator's environment |
| Consumers | the script: `SHELLTUTOR_HOME` overrides sandbox root (shelltutor:30); `NO_COLOR` disables ANSI styling (shelltutor:34, no-color.org convention); `HOME` is the default sandbox parent (shelltutor:30) |
| Validation | none beyond bash's default parameter substitution semantics |
| Flags | `config-without-validation` — `SHELLTUTOR_HOME` is consumed verbatim; if set to a path the script cannot create (read-only, root-owned, etc.), `mkdir -p` will fail and propagate. Low severity, but worth surfacing because the env-var contract is not documented anywhere except in the `usage()` help text. |

**Evidence:**

- `shelltutor:30` — `SANDBOX="${SHELLTUTOR_HOME:-$HOME/.shelltutor}"`.
- `shelltutor:34` — `if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then ... fi`.
- `shelltutor:62` — usage text says "Sandbox folder: $SANDBOX" so the operator can see the resolved path.

### C-005 — Help / usage text

| Field | Value |
| --- | --- |
| Name | `shelltutor -h\|--help usage` |
| Format | `ad-hoc` (static heredoc) |
| Surface | `cli` |
| Location | `shelltutor:53-64` |
| Versioning | `none` |
| Producer | `usage()` |
| Consumers | the operator |
| Validation | none |
| Flags | none — usage text matches argument shape (C-001) at the current revision; no drift detected. |

### C-006 — Welcome and lesson screen text

| Field | Value |
| --- | --- |
| Name | `lesson heredoc content` |
| Format | `ad-hoc` (in-script bash heredocs with ANSI color variables interpolated) |
| Surface | `cli` (user-facing terminal output) |
| Location | `shelltutor:152-409` (welcome through finale) |
| Versioning | `none` |
| Producer | the lesson functions |
| Consumers | the learner reading the terminal |
| Validation | none |
| Flags | `prompt-args-without-schema` — closest match — but classified `not-a-prompt` in Phase 8. These are CLI UI heredocs, not LLM prompts. Recorded here for completeness; Phase 8 owns the prompt-surface classification. |

The lesson heredocs are also the carrier for the user-facing claim
that the practice subshell is a complete sandbox (shelltutor:169). The
authority observation belongs to Phase 6; the contract layer simply
notes that the welcome screen makes a safety claim with no machine-
readable contract behind it.

## Cross-document authority references

The audit-attention flag `agents-md-parent-reference-style` lands here.

**The reference:** `AGENTS.md:21-30` says:

> The Jefahnierocks workspace contract at
> `/Users/verlyn13/Organizations/jefahnierocks/AGENTS.md` also applies
> inside this repository. Rules in that file and rules restated here
> are stated on shelltutor's own authority, on Jefahnierocks's own
> authority — they are not inherited from a parent organization at
> runtime.

**Audit reading:**

- The reference cites an **absolute machine-local path**.
- AGENTS.md immediately follows with an explicit restatement of the
  parent contract's rules on shelltutor's own authority (lines 24-30).
- The restatement is the **load-bearing** clause; the absolute path is
  informational provenance.
- A stranger cloning the repository cannot resolve the path. But
  since the rules are restated locally and AGENTS.md explicitly says
  they are not inherited at runtime, the stranger does not lose any
  governance information.

**Classification**: `cosmetic-or-framing-deviation` per §9.6. Not a
substantive contract gap; the rules carry their own authority inside
AGENTS.md. Recommendation in Phase 10 will be a small, optional
fitness-function candidate (avoid absolute machine-local paths in
governance citations) rather than a substantive finding.

## Absent Contracts (explicit-absent per §0 / §14)

These are surfaces that the directive lists and that **do not exist**
in this project. Recording their absence here keeps the audit honest:

| Surface | Status | Reason |
| --- | --- | --- |
| HTTP / RPC API descriptions | absent | No HTTP/RPC surface. |
| Workflow descriptions / Arazzo / overlays | absent | No workflow surface. |
| Event payload schemas | absent | No events. |
| Tool/action/skill schemas | absent | No tools (in agent sense). |
| Resource manifests | absent | No resources. |
| MCP tools/resources/templates/prompts/roots/sampling/elicitation/completion/authorization | absent | No MCP surface. |
| Prompt manifests / parameter schemas | absent | No LLM prompts. |
| Database migration contracts / persisted document formats (machine-readable) | absent | No DB; sandbox file layout (C-003) is ad-hoc. |
| Retrieval chunk metadata | absent | No retrieval. |
| SDK / API public surface | absent | No SDK. |
| Device or hardware protocol definitions | absent | No device interfaces. |
| A2A Agent Cards / advertised skills / task-state contracts | absent | No A2A. |
| Subagent boundary message contracts | absent | No subagents. |
| Callback / webhook schemas | absent | No callbacks. |
| Provenance manifests (runtime/action, content, build/source) | absent | No agent runtime; no LLM content; no signed release pipeline (release posture deferred per ROADMAP Phase 4). |
| Eval dataset schemas | absent | No eval suites (Phase 9). |
| Policy-as-code input/output schemas | absent | No policy engine; safety rules are in `skill-or-sop` files (Phase 8). |

## Boundary Declarations Honored (Phase 4)

- Did not equate "has schemas" with contract discipline. The de-facto
  contracts are recorded honestly as `ad-hoc`.
- Did not require a particular schema technology. The CLI surface
  doesn't need JSON Schema; the absence is recorded with severity
  context.
- Did not treat lesson heredoc comments as machine-readable contracts.
- Did not flatten any protocol surface — there are none to flatten.

## Exit Check

| Check | Status |
| --- | --- |
| No unflagged ad-hoc external contract remains | ✅ all six de-facto contracts recorded with explicit `ad-hoc` format |
| Every tool/action/skill has a schema reference or is flagged | ✅ vacuous (no tools) |
| Every MCP/A2A surface has its protocol object inventoried separately or a missing-contract flag | ✅ vacuous (none present) |
| Every public interface has producer and consumer evidence or `consumer-unknown` | ✅ all six contracts have producer + consumer |
| Every subagent boundary has a typed message contract or a flag | ✅ vacuous (no subagents) |

Phase 4 exit check **passes**. Advancing to Phase 5.
