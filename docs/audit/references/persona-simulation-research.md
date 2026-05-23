---
title: Persona Simulation Research for shelltutor
category: research
component: persona-simulation
status: draft
version: 0.2.0
last_updated: 2026-05-22
tags: [research, personas, simulation, pty, evals, planning, verified]
priority: medium
---

# Persona Simulation Research for shelltutor

This document ingests the operator-supplied research report
`deep-research-report (9).md` into repo-local planning form. It covers
the research questions about persona categories, beginner terminal
failure modes, the smallest useful persona set, and deterministic versus
LLM-driven personas.

The source report did not include a concrete bibliography or stable
source URLs; its citations were placeholder tokens from the research
environment. Treat its external claims as design evidence pending source
link cleanup, not as final citation-grade authority.

Reviewer note (2026-05-22): essentially everything in this document
below the "Fit To Current Stack" section is **judgment** — persona
naming, persona categorization, the recommended minimum set, and the
deterministic-first ordering are design opinions, not external facts.
The only objective claims worth verifying are:

- LLM agents are non-deterministic in their outputs absent fixed seeds
  and identical model snapshots. True; widely documented across model
  providers.
- PTY automation can drive interactive Bash without changing the
  production binary. True; see [pty-harness-research.md](pty-harness-research.md).

Persona names, behavior taxonomies, and "start with two" recommendations
are working defaults for this project, not industry consensus.

## Fit To Current Stack

The research is relevant because `shelltutor` is a real interactive
terminal program. It expects a terminal, launches an interactive Bash
practice subshell, reads from `/dev/tty`, records practice history in
the sandbox, and advances via navigation words whose exit codes are
interpreted by the outer dispatcher.

The report's central stack conclusion is consistent with the repo's
current boundary:

- External interactive testing should be compared to terminal/PTY
  automation, not web E2E, GUI automation, or heavyweight agent
  frameworks.
- PTY automation is the highest-fidelity external path for testing the
  current script without changing production behavior.
- A production `--simulate` mode would be a new product contract, not
  just an internal test trick.
- A narrative emulator could help with content review, but it cannot
  test terminal behavior such as prompt parsing, completion, Ctrl+C, or
  `/dev/tty` handling.

Design implication: preserve the production Bash-only runtime by
default. If simulation work proceeds, bias toward contributor-side PTY
tooling unless a later planning decision explicitly accepts a new
runtime contract.

## Persona Categories

The report distinguishes four artifact types that should not be
collapsed:

| Category | Meaning for shelltutor |
| --- | --- |
| Learner persona | A representation of a real learner type: prior knowledge, misconceptions, attention, confidence, and recovery behavior. |
| Test persona | An operationalized learner profile that can drive repeatable evaluation and expose a specific failure grammar. |
| Guide persona | The tutor's voice, stance, or pedagogical role. This is not a simulated learner. |
| Adversarial persona | A stress profile for edge behavior, misuse, interruption, or assumption-heavy commands. |

Design implication: do not let one named persona simultaneously mean
"how the learner behaves" and "how the tutor speaks." If the same label
is needed in both places, use explicit namespaces such as
`learner.root` and `guide.root`.

## Current Six-Name Roster

The report treats the six proposed names as provisional because the
research artifact did not include complete local definitions. Its
conservative recommendation is to split them across learner/test
behavior and guide/narrator style before using them for evaluation.

| Name | Safer provisional role | Rationale |
| --- | --- | --- |
| Old-School Sal | Guide voice or expert reviewer style | Reads more like a teaching stance than a beginner learner behavior. |
| Echo | Guide voice | The high-encouragement pattern is tutor tone, not a learner model. |
| Root | Test/adversarial behavior or guide voice, depending on spec | Security-focused behavior can stress unsafe commands, but as a narrator it becomes a tutor stance. |
| Splat | Test/adversarial behavior | Useful for recovery, wrong-path, typo, and disrupted-state testing. |
| Syntax | Test behavior or strict reviewer style | Useful for exact-input and grammar sensitivity; keep separate from learner empathy. |
| Pippin | Guide voice | Visual metaphor framing is a teaching style rather than a user behavior. |

Design implication: the six-name roster is useful, but not as the first
acceptance suite. Start with behaviorally precise learner/test personas,
then map named guide styles separately if the project later explores
voice variants.

## Beginner Failure Modes To Optimize For

The research report identifies the highest-value beginner terminal
failure modes as:

- Typing commands, options, or arguments incorrectly.
- Acting in the wrong directory or against the wrong path.
- Confusing prompt text with text to type.
- Not understanding whether output should appear on screen.
- Misunderstanding stdin/stdout states where a command appears to do
  nothing.
- Expecting Tab to always complete the command rather than sometimes
  list choices or fall back to another completion mode.
- Carrying GUI expectations into a CLI where available choices are not
  visibly presented.
- Using Ctrl+C as a recovery mechanism when stuck, waiting, or unsure.

Repo-specific implication: this aligns with existing Stage 1 UX notes:
prompt wording, command visibility, `next` cadence, and Tab behavior
are not polish-only issues. They are first-tier beginner-failure
surfaces.

## Minimum Useful Persona Set

The report recommends starting with five behaviorally distinct personas:

| Persona | Primary coverage |
| --- | --- |
| Careful beginner | Baseline cooperative run; reads instructions, types requested commands, retries when told. |
| Confused novice | Misreads prompts, checks `pwd`, types `next` or `check` at the wrong time, loses track of where output went. |
| Skimmer | Reads only the most visible instruction and misses dense middle text. |
| Interrupting user | Uses Ctrl+C, `quit`, `exit`, or session restart as normal recovery behavior. |
| Overconfident user | Guesses commands, jumps ahead, uses extra flags, avoids help, and assumes familiar shell behavior. |

Design implication: if the first implementation must be smaller, use
`careful-beginner` and `confused-novice` first. Do not collapse them
permanently: "new but cooperative" and "lost in interface state" are
different risks for a shell tutor.

## Implementation Model

The report recommends deterministic state machines as the first testing
model, with optional seeded randomness later.

| Model | Usefulness | Risk |
| --- | --- | --- |
| Deterministic state machine | Reproducible, diffable, cheap, easy to debug. Best first acceptance layer. | Only tests behaviors encoded by maintainers. |
| Seeded-random state machine | Expands coverage while preserving replay when seed and transcript are saved. | Can become noisy if added before a stable log schema. |
| LLM-driven persona | Good for exploratory ideation and discovering surprising complaints. | Non-deterministic, model-sensitive, harder to debug, weak as regression authority. |
| Hybrid | Useful later: use LLMs to propose traces, then convert valuable traces to deterministic replays. | Premature if used before the first deterministic harness exists. |

Design implication: LLM personas should not be the first acceptance
layer for `shelltutor`. If used, their output should be reviewed and
distilled into deterministic replay personas.

## Harness And Logging Implications

The report's recommended future harness shape is:

- Contributor-only PTY driver, not a production dependency.
- One fresh sandbox per run via `SHELLTUTOR_HOME`.
- A human-readable transcript for UX review.
- A machine-readable event log for diagnosis and diffing.
- Separate capture of what the tutor printed and what the persona sent.
- Explicit event tags for `confusion`, `expected`, `observed`,
  `recovery`, `timeout`, `interrupt`, and `wrong-context`.

Potential log fields:

- timestamp
- persona id
- stage/lesson expectation
- screen text or normalized screen boundary
- persona read/interpretation of the screen
- action sent
- intent/why annotation
- observed prompt or timeout
- shell/control exit code when available
- sandbox path snapshot or relevant state diff
- finding tags

Design implication: the first useful artifact should be readable enough
for a human walkthrough review, even if the underlying source of truth
eventually becomes JSONL.

## Design Decisions Suggested By This Research

These are planning recommendations, not accepted implementation
decisions:

1. Treat PTY automation as contributor tooling unless the project
   explicitly accepts a new production `--simulate` contract.
2. Keep learner/test personas separate from guide/tutor voice personas.
3. Start with `careful-beginner` and `confused-novice` if only two
   personas can be implemented first.
4. Grow toward the five-persona set before using named narrator styles
   as test actors.
5. Use deterministic scripts as acceptance evidence; reserve LLM
   personas for exploratory research and trace generation.
6. Make persona actions carry intent annotations so later logs explain
   why the simulated learner acted.
7. Tag UX confusion explicitly so simulation output becomes reviewable
   evidence rather than just a transcript.

## Open Questions For Later Research

- Which PTY driver is the best contributor-tool fit for this repo:
  Expect, Python `pty`, Pexpect, `script`, or another option?
- Where should simulation artifacts live once implemented:
  `scripts/sim/`, `tests/`, or dated `audit/<date>/sim/` evidence?
- What is the exact boundary between FF-006 "full lesson-flow smoke" and
  broader persona simulation?
- Which source links support the report's claims strongly enough to cite
  in release-facing or audit-facing documents?
- How much of the Tab-completion behavior should be tested as terminal
  fidelity versus redesigned as shelltutor-specific UX?

