---
title: WP-23 keyword matching — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-23, recall, matching, ff-011, a10]
priority: medium
---

# WP-23 — evidence (Parts A and B)

Branch `wp/23-keyword-matching` from `382d2f7`. Governing text: amendment A10;
sources: `audit/2026-11-09/walkthroughs.md` round 4 (F-025..F-028, O-AN).

## Matcher corpus (FF-011)

`scripts/selftest-matching.sh` over `scripts/matching-corpus.tsv`:
**184 cases pass (102 accepted, 82 rejected) over 21 questions**, under Bash 3.2.57
and 5.3. It sources the real `normalize_answer` and `recall_matches` and reads
the 21 calls from `shelltutor`. Mutation check: dropping `not` from the
negation list, or adding `disk` to Stage 3 Q2, fails it.

Accepted lines: the rejected-correct inputs of the F-017, F-018, F-019,
F-020, F-021, F-023, F-025, F-026 and F-027 tables, plus exact-form samples.
Rejected lines: the distractors below and the negation counterexamples
(F-019: `not to the screen`, `nowhere, the screen stays blank`, `it does not go
up one level`, `it goes down, not to the parent folder`; F-026: `only appends`,
`>> appends only`).

## Distractors

| Question | Distractors from the option text (all rejected) |
| --- | --- |
| S3Q1 | `mkdir`, `new`, `cat`, `not touch` |
| S3Q2 | `~/.Trash`, `in the trash`, `on disk`, `depends`, `not gone`, `it is not deleted` |
| SHQ1 | `a file`, `a folder`, `a window`, `not a program` |
| SHQ3 | `the running one`, `the newest one`, `not the login shell` |
| ENQ1 | `set`, `env`, `echo`, `not export` |
| ENQ2 | `one folder`, `a file name`, `not a list` |
| ENQ3 | `me>`, `me> `, `it stays me>` |

Dropped for a distractor: `disk` from Stage 3 Q2 (`on disk` is an option of
the prompt).

## Hints reworded for the extended FF-009

| Question | Leaking phrase | Old hint | New hint |
| --- | --- | --- | --- |
| Stage 1 Q2 | where you are | Lesson 1.3: it answers where you are, not who you are. | Lesson 1.3: pwd answers a where question, not a who question. |
| Stage 1 Q3 | back to you, straight back | Lesson 1.4: a program's output does not go into a file by itself; it comes straight back to you. | Lesson 1.4: whoami printed something; think about where you read it. |
| Stage 2 Q1 | contains | Lesson 2.3: two dots name the folder that contains this one. | Lesson 2.3: the two dots are the name of one particular other folder. |
| Stage 4 Q1 | where | Lesson 4.1: it answers the question 'where does this program live?' with one line. | Lesson 4.1: command -v asks the shell about a command and answers in one line. |
| Stage 4 Q3 | separates | Lesson 4.1: what separates the words after vim, and what quotes do. | Lesson 4.1: how the shell cuts a line into words, and what quotes do. |
| env Q2 | places | Lesson 3: you split it at each colon to read it. It names several places, searched in order. | Lesson 3: you split it at each colon to read it; the order matters. |

All still start `Lesson N.k: ` (FF-010) and pass FF-009 for exact forms and
keyword phrases.

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp23-all/`,
`wp23-second-try-stage2/`, `wp23-second-try-stage4/`, `wp23-module-shells/`,
`wp23-module-env/`. Bash 3.2.57 runs: same commands, all `ok`, not committed.
No screen over budget; 3.1 is 17 heredoc lines and 21 rendered rows.
`second-try 2`: `Hint:` twice, the first navigation fact once (no shape line).
