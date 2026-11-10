---
title: Operator review — welcome screen (2026-11-09)
category: design
component: screens
status: active
version: 0.1.0
last_updated: 2026-11-09
tags: [design, chrome, welcome, review, findings, curriculum-thread]
priority: high
---

# Operator review — welcome screen

The operator reviewed the new welcome screen as rendered (screenshot,
2026-11-09, macOS, 80 columns). Two observations, each with a fix and
where it lands. IDs continue the walkthroughs file's letter series;
renumbered on check-in: O-AW and O-AX (O-P and O-Q were taken).

## O-AW — the course-map line runs together

**Observed.** The row under the box reads
`○○○○○  Where am I?  Paths  Files  Commands and streams  Ready for vimtutor`.
Five stage names separated only by double spaces, some of them multi-word,
read as one run-on sentence. The dots at the left have no label, so their
purpose is unclear. The operator's words: disorganised, hard to tell where
one ends and the next starts, purpose not clear.

**Cause.** The consultant response (§5.3) proposed this line. The proposal
was wrong: a horizontal list needs separators the eye can find, and 80
columns do not hold five names plus numbers plus separators (the numbered
form with `·` separators comes to 81).

**Fix.** Make the map vertical, inside the box, one stage per row, each
with its own dot. This also gives the header's `●◉○○○` its definition: the
learner has now seen one dot beside each stage name, so the five dots at
the top of every later screen are legible without a legend. The standalone
dots-and-names row under the box is removed. The "Five stages…" sentence
becomes the map's lead-in, and the safety and no-score sentences merge, so
the screen stays within 24 rows (22 including the prompt).

```text
╭──────────────────────────────────────────────────────────────────────────────╮
│  shelltutor                                        working in a Unix shell  │
│                                                                              │
│  Five stages, each a few short lessons and one task to pass:                │
│                                                                              │
│    ○ Stage 1   Where am I?                                                   │
│    ○ Stage 2   Paths                                                         │
│    ○ Stage 3   Files                                                         │
│    ○ Stage 4   Commands and streams                                          │
│    ○ Stage 5   Ready for vimtutor                                            │
│                                                                              │
│  Everything you type runs in a real shell. The tutor made a practice        │
│  folder for you and only ever writes there. No timer, no score; try as      │
│  many times as you like.                                                    │
│                                                                              │
│  ▶ Type next to begin.                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯

next (go on)   show (this screen again)   prev (back)   quit (save and leave)
────────────────────────────────────────────────────────────────────────────────

shelltutor>
```

Colour: `○` grey, `Stage N` grey, the stage name plain. On a return visit
(resume), stages already passed show `●` in green in this same map, which
is the one place the welcome changes between runs. Optional, not required
for this fix.

**Lands in.** The rendering package (chrome). Sentinel: the welcome's
title row is unchanged; the removed dots row was not a sentinel.

## O-AX — the sandbox path is jargon on the welcome, and a missed lesson

**Observed.** A row `Sandbox: /var/folders/jx/…/T/tmp.C8hvX9G6aw` appears
under the box. The operator's view: the information is useful, but a
learner does not yet know what a sandbox is, and understanding it is part
of understanding the shell and its configuration. It is an opportunity for
learning rather than a status line.

**Assessment.** Agreed on both counts. On the welcome the row is sixty
characters of path a beginner cannot read, under a label the baseline's
own glossary flags as over-claiming ("sandbox" implies isolation the design
does not provide). The right home for the fact is the moment the learner
can do something with it.

**Fix, rendering (this package).**

- Remove the `Sandbox:` row from the welcome. The path stays in `--info`,
  which is where an observer or a support question looks for it.
- On-screen vocabulary: "practice folder", never "sandbox". The word
  `sandbox` stays in code (`$SANDBOX`), contracts and docs. The consultant
  response's welcome copy said "its own sandbox folder"; corrected above.

**Fix, curriculum (a thread, not a screen).** The practice folder becomes
a recurring object the course returns to, each time with a new idea
attached. File this against WP-14 (Stages 1–2) and the `env` module.

| Where | The beat | What it teaches |
| --- | --- | --- |
| Stage 1, the `pwd` lesson | "The tutor made a folder for you to practise in. Type pwd to see where it is." The learner discovers the path rather than being shown it. | where am I; a location has a name |
| Stage 2, the tree screen | The path `pwd` printed is the full name of the "you are here" folder in the drawing; every folder in the tree has one. | absolute path; the tree and the path are the same thing |
| Stage 2, `cd` | `cd` to the practice folder by its full name after wandering off; then `~` as the short name for home. | relative versus absolute; `~` |
| Stage 3 | `poem.txt` and `numbers.txt` are files the tutor put in the folder; the learner's own files appear beside them. | the folder is really there; files are things |
| `env` module | `echo $SHELLTUTOR_HOME`: the tutor reads a variable to decide where its folder goes, and the learner can set it before running. | a program's behaviour is configured by its environment, which is the module's whole point |

One check for the agent before writing the Stage 2 beat: the screenshot's
path is a `mktemp` directory under `/var/folders`, which looks like a
harness or test invocation. Confirm the default `SHELLTUTOR_HOME` in a
learner's real run and whether it sits under `$HOME`; the `~` lesson
depends on the answer.

## Edits implied

| Document | Edit | When |
| --- | --- | --- |
| Consultant response §5.3, §6.3 | Welcome mock-up replaced by the one above | On commit |
| Rendering package spec | Remove the dots-and-names row and the `Sandbox:` row; add the in-box map; "practice folder" vocabulary | This package |
| WP-14 draft | The Stage 1 `pwd` and Stage 2 tree/`cd` beats from the table | WP-14 |
| `env` module outline (decisions doc §6) | `SHELLTUTOR_HOME` as screen 1's variable example, or a screen of its own | Phase D |
| `audit/2026-11-09/walkthroughs.md` | O-AW, O-AX recorded as operator review of the rendered screen | On commit |
