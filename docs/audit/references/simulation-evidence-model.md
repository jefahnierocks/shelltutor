---
title: Simulation Evidence Model for shelltutor
category: research
component: simulation-evidence
status: draft
version: 0.2.0
last_updated: 2026-05-22
tags: [research, evidence, logging, asciicast, jsonl, privacy, planning, verified]
priority: medium
---

# Simulation Evidence Model for shelltutor

This document ingests the operator-supplied research report
`deep-research-report (11).md` into repo-local planning form. It covers
evidence format, logging granularity, UX annotations, replay artifacts,
and privacy/retention boundaries for future `shelltutor` simulation or
walkthrough tooling.

The source report did not include a concrete bibliography or stable
source URLs; its citations were placeholder tokens from the research
environment. Treat its external claims as design evidence pending source
link cleanup, not as final citation-grade authority.

Reviewer note (2026-05-22): format/version claims (asciicast schema,
TAP, JUnit) are objective and have been spot-checked. Bundle structure,
log vocabulary, severity scale, and retention rules are **judgment** —
useful defaults for the project's privacy and review needs, but they
are recommendations, not external facts.

## Evidence Bundle

The report recommends a layered artifact bundle rather than one overloaded
file:

| Artifact | Purpose |
| --- | --- |
| Replayable terminal record | Source of truth for what the learner saw over time. |
| Structured event stream | Searchable UX annotations, stage context, and findings. |
| Machine verdict | Pass/fail status for local automation or future CI dashboards. |
| Markdown summary | Human review narrative and next-action context. |

Design implication: do not force transcript, findings, CI status, and
review summary into one file. They answer different questions.

## Preferred Canonical Format

If only one new evidence format is standardized first, the report
recommends an asciicast-like newline-delimited JSON event stream.

Useful properties (objective):

- One metadata header followed by timed events.
- Appendable and streamable during long interactive runs.
- Can represent output events, optional input events, markers, and
  terminal resize events.
- Can be converted into derived text or summary views.
- Keeps timing and replay semantics available for later review.

Current asciicast format (fact, May 2026): **asciicast v3** is the
current spec; v2 is still supported and widely used. The format is
JSONL — a header object on line 1, then 3-element JSON arrays per
event. v3 adds event codes `"i"` (input), `"m"` (marker), `"r"`
(resize), `"x"` (exit) on top of v2's `"o"` and `"i"`. asciinema is
actively maintained (latest release v3.2.0, 2026-03-01).

Sources:
[asciicast v3 spec](https://docs.asciinema.org/manual/asciicast/v3/),
[asciicast v2 spec](https://docs.asciinema.org/manual/asciicast/v2/),
[asciinema releases](https://github.com/asciinema/asciinema/releases).

Design implication: even if the first harness does not use the
`asciinema` binary, the repo can still adopt an asciicast-like event
shape as the center of gravity. If shelltutor adopts a real asciicast
container, target **v3** (or explicitly document a project-local JSONL
schema that does not claim asciicast compatibility).

## Minimum Captured Session Data

A useful session record should include:

- run id
- persona id or walkthrough id
- command/invocation metadata
- terminal width and height
- resize events
- timestamps or offsets
- output stream
- selected input events according to policy
- stage/lesson/gate context
- result status
- reason or diagnostic text on failure
- reviewer-facing finding tags

Terminal geometry is not incidental. Line wrapping and visible screen
budget are part of the beginner UX surface, especially for lessons that
try to fit in a small terminal.

## Input Capture Policy

The report recommends selective input capture:

- For synthetic persona runs, capture the scripted control-plane and test
  commands needed to explain the run.
- For real human walkthroughs, default to capturing control-plane inputs
  only: `next`, `check`, `show`, `prev`, `quit`, and `exit`.
- Do not capture arbitrary raw shell input from real users by default.
- Enable raw-key or full-input capture only for explicit contributor
  debugging or synthetic-agent runs.

Design implication: input capture is a policy decision, not just a logger
implementation detail.

## Structured Event Sidecar

A small JSONL sidecar can carry the UX semantics that a terminal stream
does not know.

Example shape:

```json
{"ts":0.000,"kind":"session-start","run_id":"abc123","cols":80,"rows":24,"stage":1}
{"ts":1.422,"kind":"input","channel":"control","text":"check","stage":1}
{"ts":1.430,"kind":"finding","tags":["observed","confusion"],"severity":2,"text":"Learner used check before completing the task","stage":1}
{"ts":3.120,"kind":"finding","tags":["recovery"],"text":"Learner used show, then corrected command","stage":1}
{"ts":4.002,"kind":"status","tags":["gate-pass"],"result":"passed","stage":1}
```

Recommended fields:

- `ts`
- `kind`
- `run_id`
- `persona`
- `stage`
- `lesson`
- `gate`
- `channel`
- `text`
- `tags`
- `severity`
- `expected`
- `observed`
- `result`

Design implication: event logs should explain why a walkthrough mattered,
not merely replay terminal bytes.

## UX Annotation Vocabulary

The report did not find a universal UX-log tag standard. It recommends a
small documented taxonomy borrowing from test reporting, bug reporting,
and usability practice. **The tag list and 0–4 severity scale below are
project judgment, not external convention.**

Initial vocabulary:

- `expected`
- `observed`
- `confusion`
- `recovery`
- `blocked`
- `skipped`
- `hint-used`
- `gate-pass`
- `gate-fail`
- `timeout`
- `interrupt`
- `wrong-context`

Severity should be lightweight. A 0-4 scale is enough:

| Severity | Meaning |
| --- | --- |
| 0 | Note only. |
| 1 | Cosmetic or low-friction issue. |
| 2 | Moderate confusion; learner can recover. |
| 3 | Repeated or stage-blocking confusion. |
| 4 | Release-blocking issue or unsafe behavior. |

Design implication: simulation evidence should make beginner friction
greppable. A transcript without finding tags is too slow to review at
scale.

## Raw, Stripped, Screenshots, And Screen State

The report recommends this evidence hierarchy:

1. Raw timed terminal stream as source of truth.
2. Stripped text transcript as a convenience view.
3. Structured screen states as derived assertions, indexed back to event
   offsets.
4. Screenshots only as supporting exhibits for visual issues such as
   wrapping, clipping, contrast, or cursor placement.

Design implication: do not store screenshots or stripped text instead of
the replayable terminal stream.

## Machine Verdict Sidecar

TAP or JUnit-style output is useful, but only as a sidecar:

- TAP is small and readable for local test producers.
- JUnit XML integrates with CI dashboards if CI is later activated.
- Neither format preserves enough context for UX review by itself.

Design implication: a future PTY harness can emit `results.tap` or JUnit
for automation while keeping replay and JSONL artifacts as the review
evidence.

## Privacy And Retention Boundaries

Terminal logs can expose sensitive or user-specific data: usernames,
home paths, hostnames, environment variables, source code, secrets, and
typed input that did not echo on screen.

Future logging should follow these boundaries:

- Capture the minimum needed for the stated review purpose.
- Avoid real participant names; use run ids or pseudonyms.
- Redact local home paths, hostnames, and other user-specific details in
  shareable summaries.
- Do not capture arbitrary raw input from real users by default.
- Do not capture secrets, tokens, passwords, or credentials.
- Define retention periods for real-user walkthrough artifacts.
- Delete or anonymize old artifacts when they are no longer needed.
- Treat synthetic-agent logs with the same masking discipline, because
  they can still contain local paths or fixture data.

Design implication: dated audit evidence is appropriate for synthetic
persona runs, but human walkthrough artifacts need a stricter retention
and redaction rule before being committed or shared.

## Design Decisions Suggested By This Research

These are planning recommendations, not accepted implementation
decisions:

1. Use a replayable terminal event stream as the authoritative evidence.
2. Add JSONL findings/annotations as a structured sidecar.
3. Generate Markdown summaries from evidence rather than treating them as
   the source of truth.
4. Use TAP or JUnit only for machine verdicts.
5. Capture terminal geometry and timing as first-class evidence.
6. Capture inputs selectively and differently for synthetic versus human
   sessions.
7. Make UX tags and severity part of the first log schema.
8. Define redaction and retention before recording real human sessions.

## Open Questions For Later Research

- Should shelltutor use a literal `.cast` format, an asciicast-like JSONL
  variant, or a simpler project-local JSONL schema first?
- Should evidence live under dated `audit/<date>/sim/` directories or a
  reusable `tests/fixtures/` area?
- What fields are mandatory for v1 logs versus optional later fields?
- Should summary Markdown be generated by the harness or hand-written by
  the reviewer after reading the artifacts?
- What redaction rules are required before any real-user transcript can
  be committed?
