---
title: WP-29 — Round-6 copy fixes (F-031, O-AY..O-BG) — awaiting operator approval
category: planning
component: workplan
status: drafted
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, lessons, copy, recall, round6]
priority: medium
---

# WP-29 — Round-6 copy fixes

**Governing text**: `audit/2026-11-09/walkthroughs.md` round 6 (F-031,
O-AY..O-BG). **Status**: drafted for operator approval; nothing is
implemented. **Tier**: core standard; no synthetic round of its own (it
rides with WP-28's). WP-28 (modules) follows this package.

## Proposed wording

1. **2.5 Names for places (O-AY).** `ls ..` and `ls ~` both list the
   learner's whole home folder in the default layout. New block, which
   stays inside the practice folder and prints one short line each:

   ```text
     cd stage1      # step into a folder
     ls ..          # look one level up: your practice folder
     cd ..          # go back up
     echo ~         # ~ is a name: echo prints what it stands for
   ```

   `▶ Try all four, then type next.`

2. **2.4 Home and back (O-AZ).** The full-name line wraps beyond a
   32-character path. The path goes on its own line with no aside, and
   the aside moves into the notice:

   ```text
     cd                 # with nothing after it: go home
     pwd                # home is outside your practice folder
     cd <folder>
   ```

   Notice: "The last line uses your practice folder's full name. A full
   name works from anywhere."

3. **3.1 Making files (O-BA).** "Now make your own beside them." becomes
   "This stage has a folder of its own. Make your files here."

4. **2.3 Moving (O-BB).** "It prints nothing; pwd shows that it worked."
   becomes "It usually prints nothing; pwd shows where you are." and the
   `cd -` aside becomes `# back to where you just were (it prints the place)`.

5. **Cleared lists (O-BC).** Stage 1 drops `clear`; Stage 2 shows
   `cd   cd ..   cd -` in place of `cd ~`.

6. **5.3 (O-BD).** "▶ Type next to try both." becomes "▶ Type next to try
   them in Vim."

7. **Terms (O-BE).** 4.3's first aside: `# seq prints 1 to 100; wc -l
   counts the lines`. 4.6 notice gains "A name with * in it is called a
   glob." so the Stage 4 task's "Use a glob" is defined. 4.3's model
   becomes "What a command prints is a stream of lines. A pipe, |, sends
   that stream into the next command." so the stage title's "streams" has
   a referent. 5.6: "On macOS with Homebrew, brew install vim adds it."

8. **1.3 (O-BF).** "pwd printed the full name…" becomes "pwd prints the
   full name of your practice folder."

9. **Stage folders (O-BG).** The Stage 3, 4 and 5 intros gain one line:
   "This stage runs in its own folder, stageN, with a few files the tutor
   put there; pwd shows it."

10. **Stage 5 Q3 (F-031).** Exact forms added (the question stays
    exact-only; the negation guard never applies to exact forms): `no the
    changes were thrown away`, `no it is unchanged`, `no it did not`,
    `no it did not change`, `the file did not change`, `it did not
    change`, `unchanged`, `no nothing changed`. Corpus accept rows for
    each; reject rows `yes`, `yes it changed`, `it changed`.

## Simulation (not the tutor)

11. **Leo persona v0.3.** Round 6's sheet says the model "could not
    honestly produce" Leo's errors once the lessons were short. The
    persona gains a scripted schedule so the behaviour is mandatory, not
    optional: the first command of each stage is typed with a leading
    slash; the first recall answer at each gate is a one-word guess taken
    from the last command he typed; the first gate task is attempted with
    `check` before doing anything. Calibration history records the reason.

## Commits (after approval)

1. `fix(stage2): 2.3–2.5 copy — cd prints, full name on its own line, short listings (O-AY, O-AZ, O-BB)`
2. `fix(copy): 1.3 tense, 3.1 folder, 5.3 line, terms defined, stage-folder line (O-BA, O-BD..O-BG)`
3. `fix(recall): Stage 5 Q3 exact forms and corpus rows (F-031); cleared lists (O-BC)`
4. `chore(sim): personas and sentinels for the changed blocks; density rows; records; STATUS`
5. `docs(sim): Leo persona v0.3 — scripted error schedule`
