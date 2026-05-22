---
title: shelltutor Audit — Phase 5 State and Memory Inventory
category: audit
component: phase-5
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-5, state, memory]
priority: high
---

# Phase 5 — State and Memory Inventory

shelltutor has exactly one state surface: the per-learner sandbox
directory at `$HOME/.shelltutor` (or `$SHELLTUTOR_HOME` if set). Inside
that directory, four files exist; each is classified separately
because their lifecycles and roles differ. None of the nine agentic
memory classes (request-local-ephemeral, session-state,
durable-conversation-state, long-term-memory, operator-rules-memory,
retrieval-corpus, retrieval-index, eval-dataset, agent-scratchpad)
apply — there is no agent runtime to own such state. Two non-agentic
classes from §6 apply: `artifact` (educational fixtures, bash
history) and `checkpoint-state` (the lesson-resume integer).

## Stores

### S-001 — `$SANDBOX/poem.txt`

| Field | Value |
| --- | --- |
| Classification | `artifact` |
| Owner context | `shelltutor-tutor` |
| Retention | Until learner deletes `$SANDBOX` (or `$SHELLTUTOR_HOME`). Self-heals if missing: `setup_sandbox()` re-creates with the same 4-line content. |
| Read authority | learner via lesson copy (`cat poem.txt`, `wc poem.txt`, etc. in lessons 3 and 6) |
| Write authority | `setup_sandbox()` (shelltutor:68-75); a learner inside the practice subshell can also write/overwrite it (it lives inside `$SANDBOX` which the learner owns) |
| Invalidation trigger | none (idempotent setup; learner edits persist across restarts because `setup_sandbox` only writes if missing) |
| Deletion / reset path | `rm $SANDBOX/poem.txt` → next run recreates; or `rm -rf $SANDBOX` resets the whole sandbox |
| Lifecycle | `stable` — content is fixed; no version churn |
| Sensitivity | none |
| Citations | shelltutor:68-75 |

### S-002 — `$SANDBOX/numbers.txt`

| Field | Value |
| --- | --- |
| Classification | `artifact` |
| Owner context | `shelltutor-tutor` |
| Retention | Same as S-001 |
| Read authority | learner via lessons 5, 6, 9 (`cat numbers.txt`, `sort numbers.txt`) |
| Write authority | `setup_sandbox()` via `seq 1 50 > "$SANDBOX/numbers.txt"` (shelltutor:76-78); learner inside the practice subshell can overwrite |
| Invalidation trigger | none |
| Deletion / reset path | Same as S-001 |
| Lifecycle | `stable` |
| Sensitivity | none |
| Citations | shelltutor:76-78 |

### S-003 — `$SANDBOX/.shelltutor_history`

| Field | Value |
| --- | --- |
| Classification | `artifact` |
| Owner context | `shelltutor-tutor` |
| Retention | Accumulates across runs (the file is `touch`-ed if missing, then bash's `history -a` appends each command from the practice subshell). HISTSIZE=2000, HISTFILESIZE=4000. |
| Read authority | the practice subshell (`history -r`); the learner via bash history surface (Up arrow, Ctrl+R) |
| Write authority | the practice subshell via `PROMPT_COMMAND='history -a'` (shelltutor:111-116); the learner via bash builtins |
| Invalidation trigger | when HISTFILESIZE is exceeded, oldest commands are dropped |
| Deletion / reset path | `rm $SANDBOX/.shelltutor_history` (or `rm -rf $SANDBOX`); next run `touch`es it back into existence |
| Lifecycle | `stable` |
| Sensitivity | low — bash history of the learner's tutor commands; sandboxed away from `~/.bash_history` |
| Citations | shelltutor:79 (touch), 102-103 (intent comment), 111-116 (HISTFILE config) |

### S-004 — `$SANDBOX/.progress`

| Field | Value |
| --- | --- |
| Classification | `checkpoint-state` |
| Owner context | `shelltutor-tutor` |
| Retention | Written each time the dispatcher advances; removed when `finale` runs (script-level `rm -f "$PROGRESS_FILE"` at shelltutor:456). |
| Read authority | `read_progress()` on script startup (shelltutor:86-93) |
| Write authority | `save_progress()` only (shelltutor:82-84). Soft-fails (`2>/dev/null \|\| true`) so a write failure does not abort the lesson. |
| Invalidation trigger | (a) finale completes → `rm -f`; (b) explicit lesson jump (`./shelltutor 7`) — the loop overwrites the file with each save_progress call; (c) the regex `[[ "$n" =~ ^[0-9]+$ ]]` rejects non-integer content (read_progress falls back to 0) |
| Deletion / reset path | Run the tutor to completion (finale removes it); or `rm $SANDBOX/.progress`; or `rm -rf $SANDBOX` |
| Lifecycle | `stable` |
| Sensitivity | none — a single non-negative integer |
| Citations | shelltutor:30-32 (constant), 82-93 (save/read), 452-456 (loop save + finale remove) |

### S-DIR — `$SANDBOX` (the directory itself)

| Field | Value |
| --- | --- |
| Classification | `artifact-store` |
| Owner context | `shelltutor-tutor` (created by `setup_sandbox()`) |
| Retention | Persistent until learner deletes |
| Read authority | the learner (their normal user permissions); the script and the practice subshell |
| Write authority | the script (`setup_sandbox`, `save_progress`); the practice subshell (bash history appends, plus any command the learner runs inside the subshell while CWD is `$SANDBOX`) |
| Invalidation trigger | none |
| Deletion / reset path | `rm -rf "$SANDBOX"` (or `rm -rf "$SHELLTUTOR_HOME"` if overridden) |
| Lifecycle | `stable` |
| Sensitivity | none |
| Citations | shelltutor:30, 67 |

## Non-existent State Surfaces (explicit-absent)

For audit clarity, the agentic memory taxonomy classes that are
absent from this project:

| Class | Status | Notes |
| --- | --- | --- |
| `request-local-ephemeral` | absent | No request lifecycle. |
| `session-state` (agentic) | absent | The practice subshell maintains its own session-internal state, but the script does not own a runtime session model. |
| `durable-conversation-state` | absent | No conversation. |
| `long-term-memory` | absent | No long-term memory store. |
| `operator-rules-memory` | absent | AGENTS.md and CLAUDE.md are skill-or-sop files (Phase 8), not runtime memory. |
| `retrieval-corpus` / `retrieval-index` | absent | No retrieval. |
| `eval-dataset` | absent | No evals (Phase 9). |
| `agent-scratchpad` | absent | No agent scratchpad. |
| `prompt-policy-config` | absent | No prompt policy config — no prompts. |
| `tenant-memory` / `user-memory` (multi-tenant) | absent | Single-user CLI; no tenant model. |
| `cache` | absent | No cache. |
| `index` | absent | No index. |
| `audit-log` | absent | No audit log emission. |
| `derived-durable` | absent | No derived-from-authoritative store. |
| `authoritative-durable` (relational/document DB) | absent | The `.progress` file is the only persisted single-record state; classified `checkpoint-state` because it is per-learner CLI resume token, not an authoritative business-data store. |

## Boundary Declarations Honored (Phase 5)

- Did not multi-classify a store without explanation. `.shelltutor_history`
  could superficially look like `session-state`, but the directive's
  taxonomy is agent-runtime-flavoured. Recording as `artifact` is more
  honest for a bash history file written across runs and shared
  between the practice subshell and the learner.
- Did not treat any of the four files as `authoritative-durable`.
  None hold business-level truth; the script's authoritative store is
  the script itself.
- Did not merge classes. The four files have distinct lifecycles and
  distinct write authorities; each gets its own record.
- Did not infer retention from defaults. Each file's retention is
  evidenced from the code that creates/writes/deletes it.
- Did not skip the sandbox directory itself; recorded as `S-DIR` so
  the deletion path is one cited place.

## Exit Check

| Check | Status |
| --- | --- |
| Every store has an owner or `owner-unknown` flag | ✅ all five owned by `shelltutor-tutor` |
| Every writable store has write-authority evidence or `missing-authority` flag | ✅ all five cite the write path |
| Every memory surface is classified by purpose, durability, owner, and deletion/reset semantics | ✅ |

Phase 5 exit check **passes**. Advancing to Phase 6.
