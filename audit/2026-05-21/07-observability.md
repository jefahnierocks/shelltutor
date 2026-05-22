---
title: shelltutor Audit — Phase 7 Observability Semantics
category: audit
component: phase-7
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-7, observability, telemetry]
priority: high
---

# Phase 7 — Observability Semantics

shelltutor emits no telemetry. There is no tracing, no metrics
infrastructure, no logging framework, no audit log, no OpenTelemetry
adoption, no GenAI or agent or MCP semantic-convention surface. The
absence is by design for a single-file CLI tutor with no model-mediated
runtime, no public API, and no production deployment.

Recording the absence honestly is the substance of this phase. Score
recorded in Phase 10 reflects "0 — Logs only or no meaningful
telemetry" with the context that there is no agentic or production
runtime to instrument.

## Telemetry Inventory

| Signal class | Status | Evidence / search |
| --- | --- | --- |
| Tracing (OTel / vendor) | absent | grep `otel\|opentelemetry\|tracer\|span` → 0 matches across tracked files |
| Metrics | absent | grep `metric\|counter\|gauge\|histogram` → 0 matches (other than the lesson copy that says "count" in everyday English about `wc`) |
| Structured logs | absent | the script uses `printf`/`echo` for user-facing output only; no log levels, no log files |
| Audit log | absent | no audit trail emitted from any path |
| Event emission | absent | no event bus, no message publication |
| Eval-result correlation | absent | no evals (Phase 9) |
| Token / cost accounting | absent | no model calls; nothing to account |
| Latency attribution | absent | no instrumentation; lesson advancement is human-paced |
| Quality attribution | absent | no quality scoring |
| Provenance — runtime/action | absent | no agent runtime |
| Provenance — content | absent | no LLM-generated content |
| Provenance — build/source | absent | no signed-release pipeline yet (deferred per ROADMAP Phase 4) |
| Callback / resume events | absent | no callbacks |
| Protocol-specific events | absent | no MCP/A2A/workflow surfaces |

## Cost / Latency / Quality / Provenance Quartet

For projects with model-mediated paths, the directive Phase 7
inventories the quartet per agentic span / per loop iteration / per
subagent invocation. For shelltutor, the quartet is **vacuously
satisfied** by the absence of model-mediated paths:

| Attribute | Status | Note |
| --- | --- | --- |
| Cost | n/a | No model calls. Nothing to account. |
| Latency | n/a | No agent loop iterations to time. Lesson advancement is learner-paced. |
| Quality | n/a | No model output to evaluate. |
| Provenance | n/a | No agentic output to provenance-emit; no content provenance; no release provenance (deferred). |

Phase 10 scoring records this honestly: dimension 11.7 scores 0 on
the rubric, **but** the score should be read with context — score 0
here means "no telemetry by design, on a CLI tutor with no agentic
or production runtime," not "telemetry expected and missing."

## Semantic-Convention Status

| Convention | Adopted? | Version | Stability |
| --- | --- | --- | --- |
| OTel GenAI conventions | not applicable | n/a | n/a |
| OTel agent / MCP conventions | not applicable | n/a | n/a |
| OTel trace / metric / log core conventions | not applicable | n/a | n/a |

`baselines.observability.semantic_convention_version: n/a` and
`semantic_convention_stability: n/a` in the profile — N/A because the
capability is absent, not because the version is unknown.

## What the Project Does Instead (and why it's appropriate)

The current "observability" of shelltutor is the script itself:

- The learner's terminal shows the lesson screen + the practice prompt.
- The `.progress` file is a single integer (S-004 in Phase 5) that an
  operator can `cat` to see where the learner left off.
- The bash history file (`.shelltutor_history`, S-003) records the
  learner's commands in the practice subshell.
- Commit history is the changelog (no `CHANGELOG.md` yet).

For a Day-1 single-file CLI tutor with no agentic runtime, no
production deployment, and no SLA, this is appropriate. The audit
records no flags here.

## When Telemetry Would Become Appropriate

These are trigger events the next profile/audit cycle should check for:

- The tutor adds telemetry by intent (e.g., to study learner drop-off
  per lesson).
- The tutor adds a runtime LLM surface (e.g., a "ask the tutor"
  helper) — this triggers OTel GenAI semantic-convention adoption.
- The tutor adopts a release pipeline — this triggers build/source
  provenance (SLSA) consideration.
- The tutor adds an eval suite — this triggers eval-result correlation
  with telemetry.

None of these trigger events have fired at the snapshot revision
(`e6257aa`).

## Boundary Declarations Honored (Phase 7)

- Did not require a specific observability vendor.
- Did not treat the script's stdout output as "logging" — it is user-
  facing UI.
- Did not claim convention alignment without checking; alignment is
  n/a here.
- Did not credit absent token logging as cost attribution; both are
  absent.
- Did not conflate runtime/action, content, and build/source
  provenance — all three are recorded separately as absent with
  reasons.
- Did not penalize missing development-stage conventions; n/a is the
  honest classification.

## Exit Check

| Check | Status |
| --- | --- |
| Naming inconsistencies flagged | ✅ vacuous (no telemetry to be inconsistent) |
| Convention alignment scored with citations | ✅ all conventions n/a with reason |
| Agentic paths have cost/latency/quality/provenance coverage or explicit gaps | ✅ vacuous; no agentic paths |
| Semantic-convention version and stability recorded when conventions are claimed | ✅ vacuous; nothing claimed |

Phase 7 exit check **passes**. Advancing to Phase 8.
