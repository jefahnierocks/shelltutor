---
title: Stage 1 Density Audit
category: audit
component: stage1-density
status: active
version: 0.1.0
last_updated: 2026-05-23
tags: [audit, density, stage1, ux, slice1-prereq]
priority: high
---

# Stage 1 Density Audit (Slice 1 prereq, FF-006b)

Prerequisite audit for the simulation-design-plan §First Three Slices
ordering rule: record the density audit **before** the PTY harness
captures a `current-rc` baseline, so the harness can label known rough
edges rather than discovering them as if they were new failures.

The current Stage 1 screens are the artifact under audit (revision
`f4f0a23` of `shelltutor`, lines 471-758). Each screen is tagged with:

- **concepts introduced** — new ideas this screen asks the learner to
  hold; existing ideas re-used are not counted.
- **action requested** — the verb the screen asks the learner to do
  before advancing.
- **distinct actions** — the number of separate concrete actions the
  learner must perform to fully follow the screen's instructions.
- **recommendation** — `keep`, `split`, `merge`, or `trim` per the
  plan's rule ("two or more new concepts OR two or more distinct
  actions → split candidate").

Local-feedback provenance: this audit folds the working-tree `notes`
file written by the operator after a manual walkthrough on macOS
2026-05-22; the notes file is removed in the same commit because it is
superseded by this artifact.

## Screen-by-screen

### S1-W. `welcome()` (shelltutor:471-489, ~11 lines)

- **concepts introduced**: course identity; "five stages → vimtutor"
  framing; total time budget; pass-to-advance; sandbox folder location.
- **action requested**: "Type `next` for a quick orientation."
- **distinct actions**: 1.
- **recommendation**: **keep**. Five framing concepts is high, but each
  is a one-line declaration not a thing the learner must operate on;
  no action density. Sandbox folder text matches the F-002 closure
  (narrowed claim).

### S1-O. `orientation()` (shelltutor:491-513, ~17 lines)

- **concepts introduced**: practice prompt visual; keyboard-only input
  (no mid-line click); terminal-resize advisory; four navigation words
  (`next`, `prev`, `show`, `quit`); fifth word (`check`) deferred.
- **action requested**: "Type `next` to begin Stage 1."
- **distinct actions**: 1.
- **recommendation**: **keep with watch**. Five concepts is the
  ceiling under the rule, but orientation is intrinsically a
  one-screen reference card. Splitting risks fragmenting a card the
  learner will want to scroll back to via `show`. Operator-feedback
  item "Pressing Enter 'runs' whatever you type here" is partially
  addressed by the literal `shelltutor>` rendering on line 498; an
  inline explicit "press Enter to run it" could land in a future
  rewrite but is not blocking Slice 1.

### S1-I. `stage1_intro()` (shelltutor:519-532, ~7 lines)

- **concepts introduced**: stage scope ("three lessons + a small task,
  ~10 minutes"); per-stage shape.
- **action requested**: "Type `next` to start lesson 1.1."
- **distinct actions**: 1.
- **recommendation**: **keep**. Light intro, intentional pacing
  buffer.

### S1-L1. `stage1_lesson_1` — "1.1 running commands" (shelltutor:534-558, ~22 lines)

- **concepts introduced**: `echo` invocation; word-separation vs.
  quoting (`echo I am at the shell` vs. `echo "I am at the shell"`);
  Tab completion (single-Tab uniqueness, double-Tab list, no-cycle
  contrast with zsh/fish); `Ctrl+L` clear (and the `show`-to-redisplay
  consequence implied); Up-arrow history recall; `Ctrl+C` interrupt.
- **action requested**: "Try a few, then type `next`."
- **distinct actions**: ≥5 (run `echo hello`; try the quoted/unquoted
  forms; demo Tab on `echo p`; demo Ctrl+L; demo Up-arrow; demo
  Ctrl+C if the learner is following the keys block).
- **recommendation**: **SPLIT** (priority: highest in Stage 1).
  - Suggested split:
    - **1.1a — running commands**: `echo`, word-separation, quoting.
      One concept family; "try the three echo forms, then type
      `next`."
    - **1.1b — keyboard habits**: Tab / Tab-Tab / Ctrl+L / Up / Ctrl+C
      with explicit "try each, then type `next`".
  - Operator-feedback (notes:30-38) on Ctrl+L flow (`show` to
    re-display) is correct as written; splitting clears space to make
    that visible without competing with `echo` quoting.
  - Tab demo already uses sandbox-visible `poem.txt` filename (recent
    fix `d77c0e3`); the no-cycle note is in place.

### S1-L2. `stage1_lesson_2` — "1.2 identity / location / time" (shelltutor:560-580, ~18 lines)

- **concepts introduced**: `whoami`; `pwd`; `date`; sandbox-folder
  reason for the reported `pwd` (forward-reference to Stage 2); `clear`
  command as an alternative to `Ctrl+L`.
- **action requested**: "Run all three, then type `next`."
- **distinct actions**: 4 (three identity commands + `clear` or
  `Ctrl+L`).
- **recommendation**: **SPLIT or TRIM**.
  - The forward-reference to Stage 2 ("see Stage 2") imposes cognitive
    load: the learner is told a thing is true for a reason they will
    learn later. Either trim the sentence to a footnote-style aside or
    move the explanation to Stage 2's first lesson.
  - The `clear` block sits awkwardly mid-lesson and feels like a key
    re-introduction (Ctrl+L was already demoed in 1.1). Either move
    `clear` to 1.1b's keyboard-habits screen, or drop it entirely
    (Ctrl+L is the modern path; `clear` is informational).
  - Conservative recommendation: TRIM (drop `clear` block, soften the
    Stage-2 forward-reference) without splitting. SPLIT only if the
    1.1 split lands and the screen still feels heavy.

### S1-L3. `stage1_lesson_3` — "1.3 what just happened" (shelltutor:582-604, ~22 lines)

- **concepts introduced**: 5-step command pipeline (terminal → shell →
  program lookup → execution → stdout → re-prompt); the three-way
  distinction between **terminal**, **shell**, **program**.
- **action requested**: "Type `next` to take Stage 1's gate."
- **distinct actions**: 1 (read).
- **recommendation**: **keep with watch**. Concept density is high but
  action density is zero — this is intentional conceptual
  consolidation before the gate. Risk: information overload for a
  beginner who already did 1.1 and 1.2 actively. Watch for
  baseline-evidence signal (e.g., long pause before the next `next`
  in the PTY transcript) before deciding to split.

### S1-G. `stage1_gate_screen` (shelltutor:606-617, ~8 lines)

- **concepts introduced**: gate has two parts (recall + task); recall
  is three-questions-all-correct; task is verified; unlimited retries.
- **action requested**: implicit (next screen renders Q1 directly via
  `ask_question`).
- **distinct actions**: 0 (informational screen).
- **recommendation**: **keep**. Light, deliberate beat between lesson
  3 and the gate proper.

### S1-GT. Stage 1 gate-task screen (shelltutor:692-705, ~13 lines)

- **concepts introduced**: the task itself (run three commands, then
  the script will ask follow-ups); ordering rule ("After all three
  have run, I'll ask").
- **action requested**: "Type `check` only after running all three."
- **distinct actions**: 4 (`whoami`, `pwd`, `date`, then `check`).
- **recommendation**: **keep**. Action density of 4 is unavoidable
  here — that **is** the task. The commands-run guard at line 635
  already catches premature `check` (closure of operator-feedback
  "typing `check` just exited"). The screen now correctly states the
  ordering explicitly.

### S1-FQ. Gate follow-up questions (shelltutor:721-741, in-code prompts, no heredoc screen)

- **concepts introduced**: none new; revisits `whoami`/`pwd`/`date`
  output recall.
- **action requested**: three short typed answers.
- **distinct actions**: 3.
- **recommendation**: **keep**. Each prompt is a single question; no
  density issue. Worth noting: these are not screens with `show`/`prev`
  navigation — they are blocking `read` prompts.

## Aggregate findings

| Screen | Concepts | Actions | Rec |
|---|---:|---:|---|
| welcome (S1-W) | 5 | 1 | keep |
| orientation (S1-O) | 5 | 1 | keep with watch |
| stage1_intro (S1-I) | 2 | 1 | keep |
| 1.1 running commands (S1-L1) | 6 | 5+ | **SPLIT** |
| 1.2 identity/location/time (S1-L2) | 5 | 4 | **SPLIT or TRIM** |
| 1.3 what just happened (S1-L3) | 2 (deep) | 1 | keep with watch |
| stage1_gate_screen (S1-G) | 3 | 0 | keep |
| gate-task (S1-GT) | 2 | 4 | keep |
| follow-up questions (S1-FQ) | 0 | 3 | keep |

**Two screens fail the rule and warrant a structural fix (S1-L1, S1-L2). Two screens are borderline and warrant watch via baseline evidence (S1-O, S1-L3).**

## Slice 1 baseline ordering rule (binding)

Per simulation-design-plan §Pedagogy And UX, Stage 1 lesson text MUST
NOT change before the `current-rc` baseline is captured by the Slice 1
PTY harness. The recommendations above are catalogued as **labeled
rough edges** for the harness's `summary.md` (see
simulation-design-plan §Evidence Bundle); they remain the operator's
decision to act on after the baseline exists. The harness records the
script as-is; it does not pre-fix it.

If a separate "clean lesson baseline" slice is later chosen, that
slice authors lesson-text changes against a known prior transcript and
re-runs the harness. That is a future decision, not a Slice 1
deliverable.

## Open items for the Slice 1 harness

The harness should embed these IDs (S1-W..S1-FQ) in its
`events.jsonl` per-screen annotations so the diff between
`current-rc` and `no-system-rc-preview` can be read against this
catalogue. The `summary.md` "Known Rough Edges Labeled" section
ingests the **SPLIT / SPLIT-or-TRIM** rows by default.

## Cross-references

- `docs/simulation-design-plan.md` §First Three Slices, §Pedagogy And UX
- `shelltutor` lines 471-758 (welcome through end of `stage1_gate`)
- Audit finding `F-002` (welcome-screen sandbox claim) — closed; the
  S1-W concept "sandbox folder location" matches the narrowed wording.
- Operator local feedback (working-tree `notes`, 2026-05-22) — folded
  into S1-O, S1-L1, S1-L2, S1-GT items above; original file removed
  in the commit that introduces this artifact.
