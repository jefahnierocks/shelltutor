---
title: shelltutor Audit — Phase 9 Evals and Quality Gates
category: audit
component: phase-9
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-9, evals]
priority: high
---

# Phase 9 — Evals and Quality Gates

shelltutor has no eval suites at the snapshot revision. The directive
allows recording absence with a cited justification; the justification
here is that the project has no model-mediated path, no production
runtime, and no public SDK to gate. The project does intend two
non-eval quality gates per `ROADMAP.md` Phase 2 (manual lesson
walkthrough and `shellcheck`); both are deferred to known-debt status
per the profile.

## Eval Inventory

| Suite | Status |
| --- | --- |
| (none) | — |

No `tests/`, `evals/`, `__tests__/`, `*.test.*`, `bats/`, `assert*.sh`
or equivalent files exist. Search:
`find . -type f -name '*test*' -o -name '*spec*' -o -name '*eval*'`
returns the directive set and the profile snapshot only — both audit
infrastructure, not project evals.

| Eval mode | Status | Citation |
| --- | --- | --- |
| `offline` (golden-data regression) | absent | — |
| `online` (production sampling) | absent | no production runtime |
| `live` (canary / A-B / shadow) | absent | no deployment |
| `calibration` (judge ↔ human agreement) | absent | no judges |

## Coverage Map (what *would* be covered if evals existed)

The directive asks the audit to map each suite to the surface it
covers (agent / tool / action / prompt / retrieval / subagent /
protocol / lifecycle). Because suites are absent, the map records
**uncovered surfaces** for completeness:

| Surface | Surface present? | Coverage status |
| --- | --- | --- |
| Agent/tool/model-mediated path | absent | vacuously covered (nothing to cover) |
| Tool with write authority | absent | vacuously covered |
| Subagent boundary | absent | vacuously covered |
| Protocol-advertised tool/resource/prompt/skill/task | absent | vacuously covered |
| Retrieval surface | absent | vacuously covered |
| Approval path | present (3 contributor-side gates at AGENTS.md:43-78) | **uncovered by evals**; norms-only enforcement via CONTRIBUTING.md:72-75 |
| Async / resume / durable / callback lifecycle | absent | vacuously covered |
| Memory retention / deletion path | present (sandbox + .progress) | **uncovered by evals**; behavioral check exists implicitly (read_progress regex; finale removes .progress) but no test asserts this |
| Lesson behavior end-to-end | present (10 lessons + welcome + finale) | **uncovered**; manual walkthrough planned per ROADMAP Phase 2 |
| Portability across Linux / macOS | claimed (CONTRIBUTING.md:42-49) | **uncovered**; ROADMAP Phase 2 lists "Validate on macOS with Homebrew bash 5+" and "Validate on a generic Linux distro (Fedora and Debian/Ubuntu families at minimum)" as exit criteria |
| Static-analysis (`shellcheck`) | claimed as "if available" (CONTRIBUTING.md:34-38) | **uncovered**; ROADMAP Phase 2 lists "Add a shellcheck pass" as exit criterion; not yet performed |

## Why Absence is Justified at this Snapshot

Per the directive: "Do not assume no eval is required; require an
operator or artifact justification."

Justification for the no-eval state at revision `e6257aa`:

1. **No agentic surface to eval.** Phases 3, 4, 5, 6, 7, 8 all
   confirm: no model calls, no tools (in agent sense), no
   subagents, no protocol surfaces, no prompts, no observability —
   nothing for an offline / online / live / calibration suite to
   exercise.

2. **No production deployment.** STATUS.md lists the lifecycle as
   `foundation / Day-1 scaffold` (STATUS.md:18). No semver tag, no
   CHANGELOG, no release pipeline (deferred per ROADMAP Phase 4).
   Online / live evals require something running in production.

3. **No public SDK.** The CLI is consumed by a human at a terminal;
   no library API consumers exist.

4. **Quality gates planned, not yet implemented.** ROADMAP Phase 2
   already names the intended quality gates:
   - manual walkthrough on macOS (Homebrew bash 5+) — pending;
   - manual walkthrough on Fedora and Debian/Ubuntu — pending;
   - `shellcheck` pass — pending;
   - "Lesson list and order documented in `README.md`. Lessons jump-
     addressable from the tutor's menu." (Phase 3 exit criteria) —
     not yet a regression test.

   Profile records all of these under `known_debt`.

The absence is honest, but **not vacuous in the rubric sense**:
dimension 11.9 scores 0 on the 0–3 scale because no eval coverage
exists for model/agent/automation paths. Score context (Phase 10):
score 0 here means "no evals on a Day-1 scaffold with no agentic
runtime," which is appropriate for current scope.

## Flags

| Flag | Status | Note |
| --- | --- | --- |
| `model-path-uncovered` | n/a | no model-mediated paths exist |
| `write-tool-untested` | n/a | no agent-runtime tools; the only writes are to `$SANDBOX` from the script itself, governed by the AGENTS.md safety rules |
| `prompt-untested` | n/a | no LLM prompts |
| `no-golden-data` | n/a | no suite to evaluate |
| `no-ci` | applies | the project intentionally has no CI per CONTRIBUTING.md:72-75 |
| `no-release-gate` | applies | release posture deferred per ROADMAP Phase 4 |
| `regression-silenced` | n/a | no regression infrastructure to silence |
| `unversioned-evaluator` | n/a | no evaluator |
| `judge-uncalibrated` | n/a | no judges |
| `retrieval-surface-uncovered` | n/a | no retrieval |
| `subagent-surface-uncovered` | n/a | no subagents |
| `protocol-surface-uncovered` | n/a | no protocol surfaces |
| `approval-path-untested` | applies | three approval gates exist (AGENTS.md:43-78) with norms-only enforcement |
| `async-lifecycle-untested` | n/a | no async lifecycle |
| `memory-lifecycle-untested` | applies (low) | the `.progress` file's create/append/delete lifecycle and the `read_progress` regex parsing are not unit-tested |

## Recommendations Forecast (finalized in Phase 10 as fitness functions)

Static analysis gates appropriate for a single-file bash CLI:

- **FF-001** (safety-rule static analysis): grep-based check on
  `shelltutor` for `sudo`, `setuid`, `chmod +s`, `curl`, `wget`,
  `nc `, `ssh `, `http://`, `https://` — fail CI if any appear
  outside `# nofitness:network` / `# nofitness:privilege` annotated
  lines (the four lesson references are educational).
- **FF-002** (write-scope static analysis): every `>`/`>>`/`mkdir`/
  `touch`/`rm` in the script must target a path expression that
  resolves under `$SANDBOX` or `$PROGRESS_FILE`.
- **FF-003** (documentation-code drift): a check that STATUS.md
  immediate-next-step entries do not name work whose `git log` entry
  already exists for the current branch.
- **FF-004** (lesson portability check): every `cat`/`ls`/`/proc`/
  `free`/`sudo dnf`/`apt`/`brew install` in lesson heredocs has a
  paired runtime-gate-and-fallback per CONTRIBUTING.md:51-54.
- **FF-005** (shellcheck pass): `shellcheck shelltutor` clean per
  ROADMAP.md Phase 2.
- **FF-006** (lesson-flow smoke test): record current end-of-lesson
  state of `.progress` after a non-interactive script run (e.g., feed
  `next\nnext\n...\nquit\n` to the practice subshells; capture exit
  code and final `.progress` content).

Each of these is a candidate fitness function; Phase 10 selects which
are warranted now versus on future cycles.

## Boundary Declarations Honored (Phase 9)

- Did not require LLM judges; classified scoring methods actually used
  (none).
- Did not treat the absent unit tests as evals — they don't exist
  anyway.
- Recorded operator-cited justification for no-eval state (ROADMAP
  Phase 2 / STATUS Lifecycle; not yet executed).
- Did not credit a single passing eval as coverage (vacuous).
- Did not treat protocol schema validation as behavior coverage
  (vacuous).

## Exit Check

| Check | Status |
| --- | --- |
| Every model-mediated / agent-mediated entrypoint maps to an eval suite or a cited no-eval-required justification | ✅ no such entrypoints; justification recorded |
| Every write-capable tool/action has some quality, safety, or policy gate identified or flagged | ✅ AGENTS.md:75-92 safety rules act as policy gate; norms-only enforcement flagged for fitness functions |
| Every protocol-advertised remote capability and async/resume path has conformance or lifecycle coverage identified or flagged | ✅ vacuous |
| CI and release-gate integration status are recorded separately | ✅ `no-ci` applies (intentional posture); `no-release-gate` applies (deferred) |

Phase 9 exit check **passes**. Advancing to Phase 10.
