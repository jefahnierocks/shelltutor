---
title: shelltutor Audit — Phase 2 Bounded Context Mapping
category: audit
component: phase-2
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-2, bounded-contexts]
priority: high
---

# Phase 2 — Bounded Context Mapping

The profile recorded `claimed_bounded_contexts: []`. Per directive §7
Phase 2, this phase must confirm/reject/merge/split/retain any claimed
context, **and** must produce a context map for the system regardless
of whether the system declared contexts. For a single-file CLI tutor,
the honest output is a single confirmed context with no internal
splits.

## Confirmed Contexts

### `shelltutor-tutor` — confirmed

The whole repository constitutes one bounded context. Status:
**confirmed** by three distinct evidence types (per §7 Phase 2's
"at least three distinct evidence types support a coherent boundary").

| Field | Value | Evidence |
| --- | --- | --- |
| Name | `shelltutor-tutor` |  |
| Status | confirmed |  |
| Owner | Jefahnierocks (personal workspace) | STATUS.md:21 |
| Authority basis | `authoritative-store` (sandbox dir + script) and `stateless-policy` (heredoc lesson copy carries no business policy) | shelltutor:30-31 ($SANDBOX), shelltutor:155-409 (lesson heredocs) |
| Inbound commands | `./shelltutor`, `./shelltutor N` (N ∈ 1–9), `./shelltutor -h\|--help` | shelltutor:415-428 |
| Outbound events | None — script writes to stdout and to $SANDBOX only; no events emitted to any external listener | (search: `grep -nE 'notify\|emit\|publish\|webhook'` → 0 matches) |
| External dependencies | `bash` ≥ 4, POSIX userland (`mkdir`, `touch`, `seq`, `cat`, `rm`, `clear`, `printf`), ANSI terminal, `/dev/tty` (for re-attaching stdin) | shelltutor:1, 30, 67-79, 134 |
| Consumed contracts | bash semantics; ANSI escape sequences; `$HOME`, `$SHELLTUTOR_HOME`, `NO_COLOR`, `PATH` env vars; `/dev/tty`; (lesson content: `/etc/services`, `/etc/passwd`, `/usr/bin`, `/proc`) | shelltutor:30, 34, 109, 134; lessons 3-7 |
| Produced contracts | `-h` help text; exit codes from `practice()` (0 next, 97 show, 98 prev, 99 quit); sandbox layout (`poem.txt`, `numbers.txt`, `.progress`, `.shelltutor_history`); welcome screen / lesson screens | shelltutor:53-64, 121-130, 67-79 |
| Known policy responsibilities | Safety boundaries declared in AGENTS.md (no privilege, no network, no writes outside $SANDBOX); user-agnostic property; bash-only dependency. | AGENTS.md:75-78, 87-92 |
| Subagents consumed | none |  |
| Subagents exposed | none |  |

Evidence types supporting confirmation:

1. **Code**: one bash file (`shelltutor`, 459 lines, single executable),
   one `main()` dispatcher, one lesson array (`welcome`, `lesson1`…
   `lesson9`, `finale`), one practice-subshell helper.
2. **Governance**: six documentation files (`README.md`, `AGENTS.md`,
   `CLAUDE.md`, `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`) all
   describe a single project with a single purpose. Decision-
   Disagreement Rule (STATUS.md:65-69) names STATUS.md as the
   authoritative file for project posture.
3. **State**: one sandbox directory (`$SANDBOX`, default
   `$HOME/.shelltutor`) holding all per-learner state.

## Rejected / Merged / Split Contexts

None. There are no claimed contexts to reject, no candidate contexts
to merge, no candidate context to split.

## Candidate Internal Distinctions (not contexts)

The script has internal partitions that could be candidates for future
bounded contexts if the project grew, but at current scope none meet
the §7 Phase 2 three-evidence-type bar for "candidate" or beyond:

- **Lesson surface vs. practice subshell** — two concerns coexist
  inside the single context:
  - the `lesson*()` functions emit heredoc copy (instruction layer);
  - the `practice()` function spawns interactive bash (execution layer).

  Both share the same sandbox state, the same authority model, and the
  same governance rules. ROADMAP Phase 3 ("Lesson Surface Review")
  hints at future modularization ("Make lessons individually
  addressable so a learner can jump to one without replaying earlier
  lessons" — ROADMAP.md:75-78). Re-evaluate at next profile if the
  refactor lands.

- **Tutor script vs. governance/companion artifacts** — the
  documentation set governs the tutor but does not run with it. The
  audit treats governance files as `governance` per §6.1 category 10
  (they are inputs to the audit, not bounded contexts in the DDD
  sense).

Neither distinction reaches `candidate` status this cycle.

## Boundary Declarations Honored (Phase 2)

- Did not upgrade `claimed-only` to `confirmed` without three evidence
  types. (None were `claimed-only`; `shelltutor-tutor` is confirmed
  with explicit evidence above.)
- Did not treat shared infrastructure (bash, the sandbox dir) as proof
  of one bounded context — it is, but the evidence basis is broader
  than that.
- Did not recommend folder moves.
- Did not invent ownership; ownership cited from STATUS.md.

## Exit Check

| Check | Status |
| --- | --- |
| Every claimed bounded context is confirmed/retained/rejected/merged/split | ✅ profile had zero claims; one context confirmed from code/governance/state evidence |
| Every confirmed context has an authority basis | ✅ `authoritative-store` + `stateless-policy` |
| No context-map edge lacks evidence | ✅ see `02-context-map.mmd` |

Phase 2 exit check **passes**. Advancing to Phase 3.
