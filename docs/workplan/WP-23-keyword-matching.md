---
title: WP-23 — Keyword matching for recall, Stage 3 redirection, harness hygiene (F-025..F-028, O-AN)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, recall, matching, stage3, harness, a10]
priority: high
---

# WP-23 — Keyword matching for recall

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A10
(operator approval 2026-11-09) and `audit/2026-11-09/walkthroughs.md`
round 4 (F-025..F-028, O-AN, H-1, H-2, P-1). **Tier**: core standard.
**Touches `shelltutor`**: yes: `ask_question`, `normalize_answer`, every
`ask_question` call (21: 15 core, 6 module), 3.1, the shape line.
A10 reverses A8's "no containment rule" on four rounds of evidence.

## Part A — matching model (F-025, F-026, F-027, O-AN) — worker fb

### A1. Semantics

An answer is accepted when EITHER
- its normalised form equals a normalised exact form (today's path,
  unchanged; nothing that passes today stops passing), OR
- it contains no negation word AND, for every keyword group of the
  question, at least one member of that group appears in it as whole
  words.

Negation words (fixed list, one place, documented in C-006): `not`,
`no`, `never`, `nowhere`, `nothing`, `none`, `isnt`, `doesnt`, `dont`,
`wont`, `cant`, `without`, `instead`, `rather`, `neither`, `nor`, `only`
(so `only appends` fails the two-group Q2 as intended). Questions whose
correct answer is itself a negation (Stage 3 Q2 `gone`; Stage 5 Q3 `no`)
rely on the exact list, which the guard does not touch.

### A2. Encoding (Bash 3.2, no arrays of arrays)

`ask_question "<prompt>" "<hint>" <exact>... [-- "<group>" ...]` where
each group is a `|`-separated list of phrases, e.g.
`-- 'screen|terminal|window|back to you|back to me|stdout|standard output'`.
Whole-word containment: wrap both sides in spaces and test
`case " $norm " in *" $phrase "*)`. Multi-word phrases are normalised the
same way as answers before testing. `normalize_answer` is unchanged except
that `>` and `>>` survive (they do today).

### A3. Groups per question (core; the agent may add synonyms, not remove)

| Q | Groups |
| --- | --- |
| 1.Q1 | `$|dollar` |
| 1.Q2 | `folder|directory|where i am|where you are|location|path` |
| 1.Q3 | `screen|terminal|window|back to you|back to me|straight back|stdout|standard output|display` |
| 2.Q1 | `up|parent|contains|above|back one` |
| 2.Q2 | `home` |
| 2.Q3 | `projects/notes|notes` AND... single group: `~/projects/notes|projects/notes|the notes folder|notes` (exact list already has the path) |
| 3.Q1 | `touch` |
| 3.Q2 | `gone|deleted|removed|for good|permanently|disk` (exact list keeps `gone`) |
| 3.Q3 | `mv` |
| 4.Q1 | `path|location|where|/usr/bin/vim|folder` |
| 4.Q2 | group 1 `overwrite|overwrites|replace|replaces|writes over|wipes|clobber|starts fresh|erases`; group 2 `append|appends|adds|add to|end` |
| 4.Q3 | `space|spaces|split|splits|two words|separate` |
| 5.Q1 | `q` |
| 5.Q2 | `:w|w|write` |
| 5.Q3 | exact only (`no`-type answer) |
| shells Q1 | `program` ; Q2 `command -v zsh|which zsh|type zsh|command -v` ; Q3 `login` |
| env Q1 | `export` ; Q2 `folders|directories|list|places` ; Q3 `shelltutor` (exact `shelltutor>`) |

Where a group member would make a wrong answer pass (e.g. 3.Q2 `disk`
with "on disk" as a distractor), drop that member and say so in the
report. Test every distractor listed in a question's own option text:
each must still be rejected.

### A4. Hints and FF-009

FF-009 now checks every exact form AND every keyword phrase against the
hint (case-insensitive, whole words). Reword the hints that leak (at least
1.Q3 "back to you", 4.Q3 "separates", 2.Q2 nothing, check all). Hints keep
the `Lesson N.k:` anchor (FF-010) and name the concept without answer
words, e.g. 1.Q3 "Lesson 1.4: whoami printed something; think about where
you read it."

### A5. The shape line goes (O-AN)

Remove `RECALL_SHAPE` from the script, `run.py`, `persona.py`,
`sentinels.py`; the Stage 2 `second-try` oracle drops the shape count
(Hint ×2, nav ×1 remain). C-006: rung 2 = hint + facts; no shape line.

### A6. Self-test

A new `scripts/selftest-matching.sh` (or a block in `smoke-test.sh`)
sources `normalize_answer` and the matcher and asserts: every round 1–4
rejected-correct input from `audit/2026-11-09/walkthroughs.md` (F-018,
F-019, F-020, F-021, F-023, F-025, F-026, F-027 tables) is accepted; the
negation counterexamples of F-019 and `only appends`, `not to the screen`
are rejected; each question's distractors are rejected. Add to `make check`
as FF-011 "recall matcher corpus" with a CONTRIBUTING row.

## Part B — Stage 3 redirection (F-028) — worker fb

3.1 teaches `echo hello > notes.txt  # put words in a file` as a taught
line (not an aside), with the `▶` line "Make a few, put a word in one,
then `next`." Stage 4.3 still owns `>` vs `>>`; 3.1 says only "more on
`>` in Stage 4". ≤ 18 heredoc lines.

## Part C — harness hygiene (H-1, H-2, P-1) — worker a6

- `scripts/sim/sitting.py`: replies strip ANSI CSI/OSC sequences, DEC
  private modes, and the alternate-screen residue; `^[` from a raw Esc is
  not shown as text. Self-test case with a captured `man` reply.
- `docs/walkthrough-notes-sim-template.md` Sitting block: "Turn cap: 160.
  One turn = one `send` or one `raw`." `docs/sim-personas/README.md`
  "Running a sitting": the same sentence, and "stop at the cap at the end
  of the current screen; record the count".

## Records

- `docs/contracts.md` C-006: matching semantics (exact OR keyword groups
  with negation guard), the negation list, rung 2 without shape line.
- `CONTRIBUTING.md`: FF-009 extended, FF-011 row; "how to add a recall
  question" names the two lists.
- `docs/design-description.md`: note in the recall section (one paragraph,
  cite A10).
- F-025..F-028 resolved with SHAs; O-AN addressed; H-1, H-2, P-1 closed.
- `STATUS.md` one line; `ROADMAP.md` Phase 5: A10, round 5 as the synthetic
  exit test.

## Acceptance

1. `make verify` green incl. FF-009 (extended), FF-010, FF-011.
2. careful-beginner `--stage all`, second-try 2 and 4, `--module shells`,
   `--module env` green on 3.2 and 5.x.
3. Report: the matcher corpus results (count accepted / rejected), the
   distractor table, the reworded hints.

## Commits (fb)

1. `feat(recall): keyword-group matching with negation guard; exact forms kept (A10)`
2. `feat(recall): keyword groups for all 21 questions; distractors verified`
3. `fix(recall): hints reworded for the extended FF-009; shape line removed (O-AN)`
4. `feat(check): FF-011 recall matcher corpus from rounds 1–4`
5. `fix(stage3): 3.1 teaches echo word > file before the gate needs it (F-028)`
6. `chore(sim): oracle without shape line; C-006; CONTRIBUTING; design note; findings resolved; STATUS; ROADMAP`

## Commit (a6)

`fix(sim): sitting.py strips terminal control residue; turn cap stated (H-1, H-2, P-1)`
