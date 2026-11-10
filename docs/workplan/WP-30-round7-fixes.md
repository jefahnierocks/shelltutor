---
title: WP-30 — Round-7 fixes (F-032, F-033, O-BH..O-BO)
category: planning
component: workplan
status: ready
version: 0.2.0
last_updated: 2026-11-10
tags: [workplan, lessons, modules, recall, copy, round7]
priority: high
---

# WP-30 — Round-7 fixes

**Governing text**: `audit/2026-11-09/walkthroughs.md` round 7 (F-032,
F-033, O-BH..O-BO). **Status**: approved in full by the operator on 2026-11-10 (A16). **Tier**: core standard for the core items, module standard
for the module items; shell-detail read done per the A15 rule (each
command below was run on macOS; Linux behaviour reasoned from POSIX and
to be confirmed by the workflow).

## Proposed changes

1. **shells 1: `ps` shows this shell, not the terminal (F-033).** On
   macOS, `ps` with no selection lists every process the user has on any
   terminal (89 rows here), and even selected by terminal there are three
   shells, not two. Both claims on the screen are false outside the
   harness. New block and notice:

   ```text
     echo $BASH_VERSION       # the version of the shell running now
     ps -p $$ -o pid,comm     # this shell, as a running program

   The second line prints one row: a number and a name. The name is
   bash. The shell is a program like any other; $$ is its number.
   ```

   The cleared list follows. (`ps -p` and `-o` are POSIX; macOS prints
   the name as a full path ending in bash, Linux as `bash`: "the name is
   bash" becomes "the name ends in bash".)

2. **Stage 1 Q2 accepts a child's one-word answer (F-032).** Exact forms
   added (exact forms match only the whole answer, so they reopen no
   false accept): `folder`, `a folder`, `directory`, `a directory`,
   `path`, `a path`, `the path`, `location`, `my location`, `where`,
   `here`, `the place`. Reject phrases added for the false accepts the
   probe found: `manual|file|date|listing`. Hint reworded so it no longer
   steers to a single word: "Lesson 1.3: pwd printed one line starting
   with /. What does that line name?" Corpus rows for all of it.

3. **Leo persona v0.3.1 (simulation).** A scripted error he recovers from
   within one further input scores 0; it scores +2 only when recovery
   takes longer. Round 7's sheet followed v0.3 as written; under this rule
   he would have reached the task. Calibration history records it.

4. **The stray slash is explained where it first happens (O-BH).** 1.1's
   notice gains: "If bash answers No such file or command not found,
   look for a stray / or a missing space, and type the line again."
   1.4 keeps "bash: is the shell speaking. It looked for a program named
   dtae and found none." and drops its copy of the slash sentence.

5. **Backslash (O-BK).** 2.3's last line becomes: "cd.. with no space is
   a different word, and bash cannot find it. Folder names are joined
   with /, never \."

6. **`<Enter>` (O-BK).** 5.2's notice gains: "Vim's own screen writes
   that as :q<Enter>. <Enter> means the key, not letters to type."

7. **5.3's last line (O-BI).** "▶ Type next. The next two lessons try
   these in Vim."

8. **env 5 aside covers both cases (O-BJ).** `# [] if you never set it;
   otherwise the folder you chose`.

9. **env 2 aside (O-BL).** `# set it again: every screen starts a fresh
   shell`.

10. **3.1 aside (maya O-001).** `touch hello.txt   # an empty file; no
    spaces in the name yet`.

11. **5.6 and the finale speak to the learner first.** "No path? Vim's
    tutor is not installed here. Ask whoever looks after this computer."
    then one grey line for that person: "Linux: the full vim package.
    macOS: brew install vim."

## Considered and not proposed

- **A checklist on a passing `check` (O-BM).** The cleared screen follows
  at once and no persona stalled; the row budget is better spent
  elsewhere.
- **Renaming Stage 4 ("streams").** 4.3 now defines the word; a title
  always precedes its lesson.
- **`home` meaning two folders (O-BN)** and the 2.4 wrap (O-BO): harness
  layout artefacts, not lesson wording.
- **maya F-003** (stray `notes.txt` satisfying the Stage 3 task): not
  reproduced; the gate removes it on entry.

## Commits (after approval)

1. `fix(shells): ps shows this shell by its own number; claims true on macOS and Linux (F-033)`
2. `fix(recall): Stage 1 Q2 one-word forms, reject phrases, hint; corpus rows (F-032)`
3. `fix(copy): slash sentence in 1.1; backslash in 2.3; <Enter> in 5.2; 5.3, 3.1, env asides; 5.6 and finale (O-BH..O-BL)`
4. `chore(sim): personas and sentinels for changed blocks; density rows; records; STATUS`
5. `docs(sim): Leo persona v0.3.1 — scripted errors scored on recovery`
