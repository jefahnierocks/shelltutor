---
title: WP-14 — Stages 1–2 grounding: model before verbs
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-b, stage1, stage2, grounding, a2]
priority: high
---

# WP-14 — Stages 1–2 grounding: model before verbs

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A2
(A2.2, A2.3, A2.5) and `audit/2026-11-08/walkthroughs.md` (O-L, O-M, O-N,
O-K). **Tier**: core standard (sentinels, personas, density rows, full
bundle). **Depends on**: the Phase A summary at three sittings; WP-15
(authored against the chrome). **Landing order**: fourth, before WP-10.
**Touches `shelltutor`**: yes, Stages 1 and 2 only; gate criteria
unchanged.

## Principle

Model before verbs, every model anchored in something visible on screen
(A2.2). The learner sees the thing, then the command that acts on it.

## Read first

- A2 in full; `docs/design-description.md` §4.1, §4.3, §4.4.
- `shelltutor`: `stage1_lesson_2` and `stage1_lesson_4` (`669-689`,
  `710-732`), `run_stage1` (`912`), all of Stage 2 (`939-1160`),
  `setup_stage_dir` (`307-328`), C-003 fixtures.
- `scripts/sim/sentinels.py`, `persona.py` (Stage 1 and 2 walks),
  `driver.py` (`ERROR_SIGNATURES`, lesson-screen scan),
  `audit/2026-11-08/stage1-density-followup.md`.

## Change 1 — Stage 1: the shell made visible (replaces 1.4; A2.3)

Choice (agent confirmed against FF-004/FF-008: nothing platform-specific,
no GNU syntax): the **mistyped command**. New 1.4, heading
`1.4 — the shell, caught in the act`, content ≤ 18 lines, in this shape:

- "Type `date`. Now type `dtae`." Expected lines shown as DIM asides:
  the date, then `bash: dtae: command not found`.
- "Read who is speaking. `bash:` is the shell. It looked for a program
  called dtae, found none, and told you. When the name is right, it finds
  the program and runs it; what the program prints comes back to you."
- The three-word model kept from the old screen, now anchored:
  `terminal → shell → program`, with "the terminal is the window; the
  shell is the program named bash that read your line; `date` is the
  program it ran".
- `▶ Try both, then type next.`

The old 1.4's five-step list is dropped; its content survives in the
three-word model. Lesson 1.5 (WP-12) follows unchanged. A2.3's watch
item (two concept screens before the gate) is recorded in the density
follow-up.

**Harness**: the `error-signature` scan would flag `command not found`
on S1-L4. Add an `expect_error` flag to the lesson table (per screen id)
so the driver records the signature as `expected-error`, not
`error-signature`, on that screen only; the summary lists it under
"Expected errors". Persona: `date`, `dtae`, `next`.

## Change 2 — Stage 2 opens with position (A2.3)

Stage 2 becomes four lessons:

1. **New 2.1, `2.1 — where you are`.** Draws the sandbox as a tree with
   "you are here" and introduces `pwd`. `run_stage2` calls
   `setup_stage_dir 1` and `setup_stage_dir 2` first so the drawing is
   exact (fixtures are constants, C-003):

       ${DIR}${SANDBOX}${RST}     ${INSTR}◀ you are here${RST}
       ├── poem.txt
       ├── numbers.txt
       ├── stage1/
       └── stage2/

   Copy: "A folder can hold files and other folders. You are always
   standing in one folder; the shell calls it the current directory.
   `pwd` prints its name." Predict-then-run: "Predict what `pwd` will
   print, then run it." `▶ Run pwd, then type next.`
2. **2.2, `2.2 — ls: what is here`.** `ls`, then `ls -p` ("folders end
   in `/`"), then `ls -a` ("names starting with `.` are hidden; this
   tutor keeps two"). Predict-then-run: "Predict which names end in `/`."
   `ls -l` is removed from this stage (A2.3); it belongs with permissions
   (D7). `ls /etc` and `ls /usr/bin` stay as "a folder you are not in".
3. **2.3, `2.3 — cd: moving`.** Today's 2.2 content (`cd /tmp`, `pwd`,
   `cd`, `cd ~`, `cd -`, `cd ..`) with the sandbox sentence kept.
4. **2.4, `2.4 — names for places`.** Today's 2.3 content, opened with
   the three names as names for positions in the tree the learner has
   seen: `.` here, `..` up one, `~` home; then relative and absolute
   paths and "Predict before you act." Trim to ≤ 18 lines (today's 2.3 is
   23 content lines, O-J): drop one example from each list and the
   `./notes.txt` line.

Stage 2 intro says "Four lessons" and lists `pwd`, `ls`, `cd` and the
three names in that order. Gate recall and task unchanged; Q1–Q3 may be
reworded to the new screens' words.

**Downstream check for `ls -l`**: it remains taught in 4.1 and 4.2 as an
example of an option; those references stand (Stage 4 is closed). The
Stage 2 persona drops `ls -l` and adds `ls -p`. No gate depends on it
(`docs/design-description.md` §4.4).

## Change 3 — O-K, one sentence in 1.2 (A2.5)

Lesson 1.2 already teaches Ctrl+L and says "Type show to bring this
lesson back afterwards" (`shelltutor:679-680`). Reword to the A2.5
sentence, "Ctrl+L clears the screen; type `show` to bring the lesson
back.", on one line. The `bind -x` rebind stays a candidate
(`audit/2026-11-08/walkthroughs.md`), not done here.

## Change 4 — Records

- `sentinels.py`: `LESSON_1_4` → `1.4 — the shell, caught in the act`;
  `S2_L1`..`S2_L4` to the new headings.
- `persona.py`: Stage 1 1.4 actions (`date`, `dtae`); Stage 2 walk for
  four lessons (`pwd`; `ls`, `ls -p`, `ls -a`, `ls /etc`; the `cd` set;
  `next`).
- `audit/<date>/stage1-density-followup.md` (append) and a new
  `audit/<date>/stage2-density.md` in the original audit's table shape.
- `ROADMAP.md` Phase 3 Amendments: one dated line (Stage 1's 1.4
  replaced; Stage 2 has four lessons; `ls -l` moved out of Stage 2).
- `README.md` Stages table: Stage 2 commands gain `ls -p` and lose
  `ls -l`.
- `STATUS.md` one line.

## Acceptance

1. `make verify` green; FF-004 clean (the tree uses `${SANDBOX}`;
   `/etc`, `/usr/bin` as today).
2. Every Stage 1 and 2 screen ≤ 18 heredoc lines and ≤ 22 rendered rows
   in the harness table (report both).
3. `careful-beginner --stage all`, `--stage 1`, `--stage 2` and
   `second-try --stage 2` green on Bash 3.2 and 5.x and hosted Linux;
   `dtae` recorded as `expected-error`, zero `error-signature` events.
4. Gate criteria unchanged: the Stage 1 and 2 verifiers are byte-identical
   to `main` except for recall wording.
5. Density rows for every changed screen.

## Commits

1. `feat(sim): expected-error screens in the lesson scan`
2. `feat(stage1): 1.4 — the shell, caught in the act (dtae); Ctrl+L sentence in 1.2 (A2.3, A2.5)`
3. `feat(stage2): open with position — tree, pwd, ls -p; four lessons; names for places (A2.3)`
4. `chore(sim): Stage 1–2 sentinels and personas; density rows; ROADMAP amendment; README table; evidence; STATUS`
