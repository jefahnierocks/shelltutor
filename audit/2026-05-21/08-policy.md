---
title: shelltutor Audit — Phase 8 Policy and Prompt / Context Separation
category: audit
component: phase-8
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-8, policy, prompts, skill-or-sop]
priority: high
---

# Phase 8 — Policy and Prompt / Context Separation

Per the directive: "For projects with no runtime LLM surface, Phase 8
still executes — against the runtime non-production, authoring
artifact, and skill-or-sop classes — and produces non-vacuous
findings. Phase 8 is never silently skipped." For shelltutor, two
`skill-or-sop` surfaces exist (`AGENTS.md`, `CLAUDE.md`) and two
in-script `not-a-prompt` surfaces exist (lesson heredocs, usage
text). Embedded policy in `AGENTS.md` is the substantive Phase 8
observation; it lines up with the `safety-rule code coverage gap`
identified in Phase 6 (AUTH-OBS-001).

## Phase 8.0 — Prompt-surface classification

Four prompt-shaped surfaces detected. See `08-prompt-surfaces.json`
for the structured form.

| ID | Path | Surface type | Classification | Privileged context | Untrusted input boundary |
| --- | --- | --- | --- | --- | --- |
| P-001 | `AGENTS.md` | `skill-or-sop` | `embedded-policy` | n/a (governance, not agent runtime) | n/a |
| P-002 | `CLAUDE.md` | `skill-or-sop` | `pure-instruction` | n/a | n/a |
| P-003 | `shelltutor` (welcome + lesson1–9 + finale heredocs) | `not-a-prompt` | `not-a-prompt` | n/a | n/a |
| P-004 | `shelltutor:53-64` (`usage()` heredoc) | `not-a-prompt` | `not-a-prompt` | n/a | n/a |

The "prompts" keyword across the script triggers on three concepts —
shell prompt (`$` / `>`), `shelltutor>` prompt, and pager prompt —
none of which are model-mediated. The same keyword in `README.md`
("prompt theme") refers to `$PS1` customization. No LLM prompt
surface exists.

## Phase 8.1 — Policy analysis

### P-001 — `AGENTS.md` (skill-or-sop, embedded-policy)

AGENTS.md is the project's primary governance document. It contains
six policy-bearing rules that are not expressed anywhere else as
executable contracts or fitness functions:

| Rule | AGENTS.md lines | Policy character |
| --- | --- | --- |
| "must not write outside its own working directory" | 87 | safety / write authority |
| "must not request elevated privileges" | 87-88 | safety / privilege boundary |
| "must not reach the network" | 88 | safety / outbound network |
| "do not introduce dependencies that require installation outside `bash` and a standard POSIX userland" | 75-77 | dependency policy |
| "Lessons must be runnable end-to-end on a clean Linux or macOS terminal without prerequisite installation beyond `bash`" | 91-92 | testing / portability policy |
| "Treat anything that requires a specific username, hostname, distro, or shell theme as a portability bug" | 89-90 | portability policy |

**Embedded-policy classification rationale** (per §9.4):

- These rules represent safety, dependency, portability, and testing
  policy.
- Changing them would change externally visible behavior (the tutor's
  safety surface, the install story, the platform reach).
- They appear in the `skill-or-sop` surface and **only** there — no
  pre-commit hook, no CI rule, no policy-as-code, no unit test, no
  eval rubric enforces any of them.

**Policy home (what the policy should live in, ideally):** for a
bash-only project with no CI, the appropriate policy home is a
**static-analysis fitness function** (FF-001 / FF-002 candidates in
Phase 10). A simple `grep`/`shellcheck` based check can verify:

- no `sudo`, `setuid`, `chmod +s` in the script
- no `curl`, `wget`, `nc`, `ssh`, `http://`, `https://` in the script
  outside lesson copy (or with a guard pattern for educational
  references)
- no writes outside `$SANDBOX` (every redirect/`mkdir`/`touch` target
  must include `$SANDBOX`)

The fitness functions are recorded in Phase 10. Phase 8 records the
**policy gap**: the rules live only in `skill-or-sop`, the code
currently honors them, but no automated check protects future
changes.

**Drift target:** any future change that violates one of the six rules.
This is the policy hazard.

### P-002 — `CLAUDE.md` (skill-or-sop, pure-instruction)

CLAUDE.md is a 22-line file that points Claude Code at AGENTS.md and
adds one precedence rule:

> When instructions conflict, prefer the most specific repo-local
> governance file, then ask the operator if the conflict affects
> implementation, portability claims, or authority boundaries.

This is pure-instruction: a routing rule and a precedence rule. No
embedded business policy. Classification confirmed.

### P-003 — `shelltutor` lesson heredocs (not-a-prompt)

The lesson heredocs (welcome at shelltutor:152-173, lesson1 at
shelltutor:175-195, … lesson9 at shelltutor:364-382, finale at
shelltutor:384-410) are user-facing terminal output text. They are
**not** model-mediated prompts. The directive's "documentation about
prompts" surface type covers explanatory material about LLM prompts;
these heredocs are explanatory material about the **shell** prompt
and CLI behavior. The `not-a-prompt` classification fits.

**Embedded-value scan** across the lesson heredocs (per §9.4 list:
currency, thresholds, roles, time windows, quotas, rates,
jurisdictions, approval rules, authority grants, secrets, tool
constraints, release criteria, eval rubrics):

| Category | Result |
| --- | --- |
| Currency amounts | none — grep `\$[0-9]` across heredocs returns no business amounts; the only `$` characters are bash variable references and the shell-prompt character |
| Numeric thresholds (policy-bearing) | none — numeric values present (e.g., `seq 1 1000000`, `head -n 12`) are pedagogical examples, not policy |
| Roles | none — the heredocs address one role (the learner) consistently |
| Time windows | none |
| Quotas / rates | none |
| Jurisdiction / compliance assertions | none |
| Approval rules | none (the heredocs are advisory: "type `next`", "press Ctrl+C") |
| Authority grants | none |
| Secrets-handling instructions | none |
| Tool-use constraints | one — lesson 8's "Skip any that says 'command not found'" (shelltutor:344). This is a soft fallback instruction for optional packages, not a policy. |
| Release pass/fail criteria | none |
| Eval rubrics | none |

**Sub-observation — lesson 8 install hint**: shelltutor:346 reads
`sudo dnf install cowsay figlet lolcat`. This is a CLI suggestion to
the learner, not a tutor action. The script itself never invokes
`sudo`, never invokes `dnf`. The audit reading:

- Not a privilege-escalation finding for the **tutor** (the tutor
  does not escalate).
- Is a portability finding for the **lesson surface** (single-distro
  install hint under a multi-platform claim) — already captured in
  Phase 1 (`lesson-portability-gaps`) and routed to Phase 10.

### P-004 — `shelltutor:53-64` `usage()` heredoc (not-a-prompt)

The CLI help text. Pure instruction; matches argv parsing; no embedded
values beyond the program name, argument shape, and the resolved
sandbox path. Classification confirmed.

## Retrieval-augmented surfaces

None. shelltutor has no retrieval (no embedding, no vector store, no
RAG). The directive's check for retrieval policy that encodes
business rules is **vacuous** for this project.

## Tool description policy

None. shelltutor has no tools in the agent-runtime sense. The
directive's check for tool descriptions encoding policy
("only invoke this if amount > $10,000") is **vacuous**.

## Untrusted-input boundary

shelltutor accepts learner input only at the practice subshell's
`shelltutor>` prompt. That input runs as a normal bash command in a
real bash process (Phase 6 A-002). There is no developer/system
message context to inject into. The untrusted-input boundary check is
**vacuously satisfied**: no privileged prompt context exists for the
learner to inject into, because there is no prompt context.

The directive flag `privileged-context-injection-risk` does not apply.

## Server-exposed prompts

None. The project has no MCP server, no A2A receiver, no protocol-
advertised prompt surface. The directive flag
`server-prompt-policy-leak` does not apply.

## Contradictory-guidance check

Phase 1 found one contradiction (STATUS/ROADMAP claim user-agnostic
refactor pending; commit log shows it complete). At the `skill-or-sop`
level, this is also relevant to Phase 8 because STATUS.md and
ROADMAP.md function as both project posture documents and contributor
guidance. The contradiction is documentation-as-policy drift, not
embedded policy — the rule itself ("user-agnostic") is correct in all
sources; what differs is the claim about whether the rule has been
applied yet. Captured as the audit-attention flag
`drift-status-roadmap-vs-commit`, finalized as F-001 in Phase 10.

## `documentation–code consistency` strategic theme

The selected strategic theme weights this phase at 1.5× (per Phase 0).
Phase 8 evidence supports the theme:

- Embedded policy in `AGENTS.md` (P-001) without code-level
  enforcement.
- Drift between STATUS/ROADMAP and commit log (contradictory-guidance
  observation, captured separately as F-001).

Both feed Phase 10's prioritization.

## Comparison to `docs/audit/references/shell-research.md`

The research doc is operator-supplied curriculum guidance for a
hypothetical "Shell Foundations for Vimtutor" course. As Phase 1
established, shelltutor's lesson surface is a deliberate subset; the
research doc is not a project authority. Surface type for the research
doc: `documentation-about-prompts` would be wrong (it's about shell
fundamentals, not LLM prompts); `not-a-prompt` is the honest
classification, with the role recorded in 00-scope.md as a Phase 1
reference. No Phase 8 finding derives from this comparison.

## Boundary Declarations Honored (Phase 8)

- Did not mark non-runtime prompt artifacts as vacuously safe. P-001
  is `embedded-policy`; P-003 and P-004 are `not-a-prompt` with
  explicit evidence-based reasons.
- Did not classify authoring artifacts using only runtime-prompt
  criteria. The skill-or-sop class got skill-or-sop treatment.
- Did not recommend policy extraction without naming a plausible
  policy home. The policy home for the AGENTS.md safety rules is a
  static-analysis fitness function (FF-001 / FF-002 in Phase 10),
  consistent with the project's bash-only constraint.
- Did not treat templated variables as safe. The script's `${SUB}`,
  `${CMD}`, `${KEY}` etc. are ANSI color variables (defined at
  shelltutor:35-46); they carry no policy content.
- Did not skip retrieval pipelines because they aren't prompts —
  vacuously checked.
- Did not treat server-exposed prompts as ordinary docs — vacuously
  none.

## Exit Check

| Check | Status |
| --- | --- |
| Every prompt-like surface is classified by surface type | ✅ P-001..P-004 |
| Every embedded-policy finding cites exact lines and the missing or conflicting policy home | ✅ P-001 cites AGENTS.md:75-92 and names static-analysis fitness function as policy home |
| Every stale authoring artifact cites the current source it contradicts or states that no source exists | ✅ contradictory-guidance flagged at the documentation-drift level (F-001 forecast) |
| Every server-exposed prompt and privileged-context input path is mapped to Phase 4 and Phase 6 or explicitly N/A | ✅ vacuous (none) |

Phase 8 exit check **passes**. Advancing to Phase 9.
