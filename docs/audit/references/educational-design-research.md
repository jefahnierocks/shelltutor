---
title: Educational Design Research for shelltutor
category: research
component: educational-design
status: draft
version: 0.2.0
last_updated: 2026-05-22
tags: [research, curriculum, feedback, pacing, mastery, pedagogy, planning, verified]
priority: medium
---

# Educational Design Research for shelltutor

This document ingests the operator-supplied research report
`deep-research-report (13).md` into repo-local planning form. It covers
curriculum sequence, mastery learning, pacing, feedback on wrong
commands, age-appropriate explanations, and the relationship between
pedagogy and interactive testing.

The source report did not include a concrete bibliography or stable
source URLs; its citations were placeholder tokens from the research
environment. Treat its external claims as design evidence pending source
link cleanup, not as final citation-grade authority.

Reviewer note (2026-05-22): pedagogy is largely a judgment domain.
Mastery learning, scaffolding, and "feedback should be specific and
actionable" are well-established educational principles with a real
research base (Bloom; Chi; Anderson & Krathwohl; Ericsson), but the
specific applications in this document — exact screen length, the
mapping of misconceptions to feedback moves, age-appropriate metaphors,
and the praise-cautious tone — are **opinion grounded in those
principles, not externally proven facts about shell tutoring
specifically.** Treat them as defensible defaults, not citations.

The one operational fact the document anchors against is the existing
shelltutor stage map (Stages 1–5), which is verifiable from the script
source. The pedagogy claims should not be quoted as if they are
established findings about shell learners.

## Executive Synthesis

The report supports two high-level choices already present in
`shelltutor` planning:

- Preserve the production contract as a real interactive Bash tutor.
- Use mastery-gated stages with specific, actionable feedback and a
  chance to retry immediately.

It also reinforces the curriculum ordering:

1. terminal/shell/prompt orientation
2. navigation and current working directory
3. files, directories, and paths
4. quoting, escaping, and globbing
5. redirection and pipes
6. minimal permissions and diagnosis
7. editor handoff once the shell foundation is stable

Design implication: the project should avoid expanding early lessons
into process control, sysadmin, package management, or shell scripting
before the core filesystem and stream concepts are stable.

## Curriculum Scope Before `vimtutor`

The report finds strong cross-curriculum support for these beginner shell
topics:

| Topic | Recommendation |
| --- | --- |
| Navigation and working directory | Must appear early. |
| Files, directories, and paths | Must appear early. |
| Quoting and escaping | Introduce before filenames with spaces or special characters. |
| Globbing and wildcard expansion | Introduce before pattern-based tasks. |
| Redirection and pipes | Core stage material. |
| Basic permissions semantics | Teach minimally and concretely when useful. |
| Process/job control | Not an early prerequisite; optional or post-core. |

Design implication: a five-stage `vimtutor` prerequisite course should
front-load navigation, files, paths, and stream concepts. Process control
should not displace those topics in the first release.

## Pacing And Mastery

The report did not find strong shell-specific evidence for an exact
screen length. It did find broader support for these principles:

- Learners should demonstrate mastery before progressing.
- The threshold for progression should be high enough to make "passed"
  meaningful.
- Novices benefit from explicit modeling and scaffolding.
- Feedback should be specific enough to act on immediately.
- Learners need an immediate opportunity to apply feedback.

Design implication: each lesson screen should generally teach one new
command idea, show a small model, ask for one immediate action, then use
the gate or practice feedback to decide whether the learner is ready to
move on.

## Feedback On Wrong Commands

The report recommends distinguishing wrong-command cases rather than
responding with one generic failure message.

| Learner state | Best feedback move |
| --- | --- |
| Nearly correct | Confirm the intent, name the one missing detail, and give a tiny next step. |
| Wrong command family but safe | Re-state the task concretely and suggest the relevant command family only. |
| Repeated same mistake | Escalate from hint to a miniature worked example. |
| Unsafe or out of bounds | Block, explain the boundary briefly, and redirect to the lesson task. |

Recommended feedback shape:

1. Acknowledge what the learner appears to be trying to do.
2. Name the exact mismatch with the current task.
3. Give the smallest useful next action.

Design implication: gate failures should not only say "try again." They
should identify the learner's likely intent and provide the next concrete
repair step without flooding the screen.

## Encouragement And Tone

The report cautions against praise-heavy tutoring. It favors calm,
task-linked support:

- Encourage the action or recovery, not the learner's identity.
- Keep praise short.
- Put longer explanations behind `show`, repeated failure, or a hint
  path.
- Prefer "what to do next" over generic reassurance.

Design implication: guide voices such as Echo or Pippin may be useful
later, but the default tutor voice should stay concise and task-focused.

## Age-Appropriate Concept Framing

The report treats child-facing shell research as thin and therefore
recommends conservative, observable explanations.

Good filesystem framing:

- The shell is showing places and names.
- `pwd` tells where you are.
- `ls` shows the names here.
- `cd` changes your place.

Good permissions framing:

- Who may look here.
- Who may change things here.
- Who may enter here.

Avoid:

- Magical explanations.
- Anthropomorphic explanations where the computer "wants" or "thinks"
  something.
- Adversarial or prize-like framing around root privileges.
- Metaphors that are hard to outgrow.

Design implication: use concrete language that maps to observable shell
behavior. Avoid metaphors that make permissions or root access sound like
a game reward.

## Testing And Review Implications

The report links pedagogy back to the simulation/testing lane:

- Automated PTY checks should verify real lesson flow, not just parser
  outcomes.
- Human-readable transcripts are needed because a tutor can pass while
  still being confusing.
- Event logs should capture hint level, wrong-command category, mastery
  outcome, and recovery behavior.
- If production observability is ever added, the least invasive form is
  an opt-in environment variable writing structured logs inside the
  sandbox, not a full simulation branch.

Design implication: future simulation evidence should measure learning
friction, not just technical completion.

## Relationship To Existing Curriculum

This report broadly supports the current five-stage direction:

- Stage 1: prompt, running commands, and identity/current location.
- Stage 2: paths and filesystem navigation.
- Stage 3: local file operations.
- Stage 4: command structure, streams, redirection, pipes, and globs.
- Stage 5: full-screen programs and `vimtutor` readiness.

The main caution is pacing: if a screen cannot be acted on immediately,
it may be explanation overload. Dense screens should be candidates for
splitting, especially in Stage 1 where the learner is still learning what
the prompt is.

## Design Decisions Suggested By This Research

These are planning recommendations, not accepted implementation
decisions:

1. Keep the five-stage mastery-gated model.
2. Keep early content focused on navigation, files, paths, quoting,
   globbing, redirection, and pipes.
3. Defer process/job control unless it is necessary for `vimtutor`
   readiness.
4. Make gate feedback specific, actionable, and short.
5. Escalate hints gradually rather than dumping full explanations early.
6. Use concrete "places and names" filesystem language.
7. Teach permissions as observable capabilities, not as a game or
   security drama.
8. Use transcripts and event logs to detect pacing and feedback problems
   that pass/fail checks miss.

## Open Questions For Later Research

- Which Stage 1 screens should be split to preserve one actionable idea
  per screen?
- Should wrong-command handling be centralized into a reusable feedback
  helper?
- How should repeated mistakes escalate from hint to worked example?
- Which child-friendly metaphors are accurate enough to keep, and which
  should be avoided?
- Should the tutor add opt-in structured logs inside the sandbox, or
  should all observability remain external through PTY tooling?

