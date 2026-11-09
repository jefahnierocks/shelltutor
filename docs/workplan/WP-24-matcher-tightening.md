---
title: WP-24 — Matcher tightening after the exit test (F-029, F-030, O-AR, O-AS, O-AT)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, recall, matching, gate, a10]
priority: medium
---

# WP-24 — Matcher tightening after the exit test

**Governing text**: A10 (WP-23 semantics) and `audit/2026-11-09/walkthroughs.md`
round 5 (F-029, F-030, O-AR, O-AS, O-AT). **Tier**: core standard.
**Touches `shelltutor`**: yes: keyword groups, `normalize_answer`,
`recall_matches`, the Stage 1 gate screen, the Stage 4 task line, the
finale. This closes the synthetic loop's last round; after it lands, the
loop pauses (A10 item 4).

## Change 1 — False accepts (F-029)

- Every wrong-but-passing answer in F-029's 16-question probe becomes a
  reject row in `scripts/matching-corpus.tsv`. FF-011 must fail before the
  group changes and pass after.
- One-word groups are tightened: a group member of one common word
  (`notes`, `where`, `end`, `window`, `up`) is replaced by the phrases the
  lessons use (`~/projects/notes`, `projects/notes`, `the notes folder
  inside projects`; `where vim is`, `where the program is`; `the end`,
  `to the end`; `terminal window`, `the window`; `up one`, `one up`,
  `go up`, `goes up`, `parent`). Each tightening is checked against the
  corpus's accept rows: nothing accepted today may stop being accepted.
- Ordered groups: `recall_matches` gains an optional `--ordered` flag
  before the groups; when set, each group's first match must appear after
  the previous group's match (position via `${norm%%"$phrase"*}` length).
  Stage 4 Q2 uses it, so `> appends and >> overwrites` is rejected and
  `> overwrites and >> appends` still passes. Corpus rows for both.
- Trash and parent distractors: Stage 3 Q2 group loses `gone` as a bare
  member only if `gone to the trash` cannot otherwise be rejected; prefer
  adding `trash` to the question's own negation set. Simplest: a
  per-question optional `--reject 'trash|browser|deletes'` phrase list
  checked before groups. Implement `--reject` if it is under 15 lines;
  otherwise tighten groups and say so.

## Change 2 — Punctuation and verb forms (F-030)

- `normalize_answer` also strips `(`, `)`, `;`, `:` ONLY when the colon is
  not the first character of a word (so `:w`, `:wq`, `:q!` survive);
  implement as: strip parentheses and semicolons; leave colons alone.
- Stage 5 Q2 group gains `:wq`, `writes`, `write it`, `save`, `saves`.
  Corpus accept rows: `:wq (or :w) writes the buffer to the file`,
  `:w writes the buffer to the file`, `:wq`.

## Change 3 — Screen lines (O-AR, O-AS, O-AT)

- Stage 1 gate task screen: one DIM line "Only commands you type after
  this screen count." (≤ 18 heredoc lines; drop a blank if needed.)
- Finale: the static command list is introduced with "This course
  covered:" instead of any wording that claims the learner ran them; keep
  the list.
- Stage 4 gate task: "count from 1 to 100 and save the count" becomes
  "count the lines of `seq 1 100` and save that number to `count.txt`".
  Verifier unchanged (`100` in the file, a `*.txt` glob in history).

## Records

C-006 (ordered groups, `--reject` if implemented, the normalisation
list); CONTRIBUTING "Adding a recall question" (ordered groups);
F-029, F-030 resolved; O-AR, O-AS, O-AT addressed; H-3 recorded as a
known harness limit in `scripts/sim/README.md`; `STATUS.md` one line.

## Acceptance

`make verify` green (FF-009..FF-011); careful-beginner `--stage all`,
second-try 2 and 4, both modules, on 3.2 and 5.x; corpus counts in the
report (accept rows unchanged in count or higher; reject rows +16 or
more).

## Commits

1. `fix(recall): corpus reject rows from the round-5 probe; one-word groups tightened (F-029)`
2. `feat(recall): ordered groups for Stage 4 Q2; per-question reject phrases (F-029)`
3. `fix(recall): parentheses and semicolons normalised; Stage 5 Q2 forms (F-030)`
4. `fix(screens): gate history note, finale wording, Stage 4 task wording (O-AR, O-AS, O-AT)`
5. `chore(sim): C-006; CONTRIBUTING; H-3 noted; findings resolved; STATUS`
