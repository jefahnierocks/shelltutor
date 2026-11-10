# Synthetic walkthrough: Arthur, sitting 6 (round 6, 28-lesson course)

## Sitting

- Date: 2026-11-09
- Persona (file in `docs/sim-personas/`) and learner role: `arthur.md`, Arthur, 64, retired logistics manager, `dos-literalist`; adult with some shell
- Persona sheet version: 0.2.0
- Turn cap: 220 (round 6). One turn = one `send` or one `raw`. Turns used: 179 (bundle `persona_inputs`)
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes. Arthur reads every line; the density charge (+1) applies only at a later turn where a long screen's content caused a wrong turn or rejection; plain long screens are in the density notes. Friction: +2 per rejected input not understood, +1 per mode confusion, -1 per gate cleared (unfloored), quit at 8. Silent commands are verified with ONE check (ls or pwd), or by the next listed command when the lesson itself lists a check.
- Tutor revision and invocation: revision 2579f68 (script 2cb3f53); `sitting.py start` with no `--arg` (begins at the welcome screen); Bash `/opt/homebrew/bin/bash` 5.3.20
- `--info` lines the persona was shown, if any: none

Login name is written `[user]` below. The sitting ran at 80x24 in the order Stage 1 to Stage 5; the finale ended with `[exited 0]`.

## Per screen

Format: id, heading; Read; Jargon; Monologue; Input and response; Interpretation; Ladder; Friction. Friction is 0 at the start and moves only where stated; running totals appear at every gate.

### welcome — shelltutor
- **Read**: all. **Jargon**: none ("working in a Unix shell" is a subtitle only).
- **Monologue**: Five stages, a practice folder that only it writes in, no timer. "Type next to begin." is plain.
- **Input** `[nav]` `next` -> accepted. **Ladder**: none. **Friction**: 0.

### orientation — Orientation
- **Read**: all. **Jargon**: "Below this panel is a real shell prompt." ("shell" not yet defined).
- **Monologue**: A prompt is below; four words steer the tutor and `check` appears later.
- **Input** `[nav]` `next` -> accepted. **Friction**: 0.

### Stage 1 intro — Stage 1: Where am I?
- **Read**: all. **Input** `[nav]` `next` -> accepted. **Friction**: 0.

### 1.1 — Running a command
- **Read**: all. **Jargon**: none.
- **Monologue**: Three to try. I leave off the `# ...` remark, it looks like a note to me.
- **Input** `[bash]` `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` -> each printed as the screen said; quotes did not print. `[nav]` `next`.
- **Interpretation**: Quotes only group, as promised. **Ladder**: none. **Friction**: 0.

### 1.2 — Four keys
- **Read**: all. **Jargon**: "Inside a full-screen program (you'll meet one in Stage 3) the way out is q." Full-screen program is undefined here and the promise points to Stage 3 (the first one actually appears in 3.3).
- **Monologue**: Tab: I did `echo p` + Tab (no Enter), it filled `poem.txt`, then Enter. Up arrow brought the line back; I did not press Enter. Ctrl+C: I sent the control character, `^C` and a fresh prompt. Ctrl+L: screen went blank, I typed `show`, lesson returned.
- **Input** `[bash]` raw `echo p\t`; send `` (Enter); raw `\x1b[A`; raw `\x03`; raw `\x0c`; `[nav]` `show`; `[nav]` `next` -> all behaved as described.
- **Interpretation**: Blank screen after Ctrl+L looked briefly like breakage; the lesson had said how to get back. **Ladder**: none. **Friction**: 0.

### 1.3 — Where am I, who am I, when is it
- **Read**: all. **Jargon**: "pwd printed the full name of your practice folder." (past tense, before the learner has run it); "This prompt ends in >. An ordinary bash prompt usually ends in $."
- **Monologue**: The path has forward slashes and no drive letter. Where is C:? Moving on. `whoami` gave my login; `date` gave a date.
- **Input** `[bash]` `pwd`, `whoami`, `date`, then `[nav]` `next`. **Friction**: 0.

### 1.4 — The shell, caught in the act
- **Read**: all. **Jargon**: "terminal → shell → program: the window, bash, and date." (first and only definition of terminal, shell and program, by example).
- **Input** `[bash]` `date`, `dtae` -> `bash: dtae: command not found`; `[nav]` `next`.
- **Interpretation**: The error was announced on screen beforehand, so it did not alarm me. **Friction**: 0.

### 1.5 — Who else types here
- **Read**: all. **Jargon**: "An AI assistant that 'runs commands' for you goes the same way."
- **Monologue**: Three habits; sensible. **Input** `[nav]` `next`. **Friction**: 0.

### Stage 1 gate — recall (3 questions) then task
- **Read**: all.
- **Q1** (prompt ends in which character): `$` -> accepted. **Q2** (what does pwd print): "the full name of the folder you are in" -> accepted. **Q3** (after whoami runs, where does its output go): "to the screen" -> accepted. "Output" as a place was not taught; I answered from what I saw.
- **Task** (whoami, pwd, date, then check): named the folder (ends `/stage1`; "pwd shows it"). Ran all three, `check` -> first check passed. Follow-ups: whoami name, full pwd path typed by hand (no way to paste), day `Mon` -> accepted.
- **Ladder**: none. **Friction after Stage 1 cleared: -1** (gate cleared).

### Stage 1 cleared — summary
- **Jargon**: the list shows `clear` (never taught; only Ctrl+L was). **Input** `[nav]` `next`.

### Stage 2 intro, 2.1 — Where you are
- **Read**: all. **Jargon**: "the current directory" in the same sentence as "folder" (Arthur treats them as one). The tree marked "you are here" was clear.
- **Input** `[bash]` `pwd` (matched the tree), `[nav]` `next`. **Friction**: -1.

### 2.2 — What is here
- **Jargon**: "ls /  # a folder you are not in: the top of everything" (the drive-letter question; no sentence says there is only one top).
- **Input** `[bash]` `ls`, `ls -p`, `ls -a`, `ls /`. `ls -a` showed `.` and `..` with no gloss in this lesson (`..` known from DOS).
- **Interpretation**: `/` is where everything hangs, like the root of C:. **Friction**: -1.

### 2.3 — Moving
- **Read**: all. **Jargon**: none; the screen answered both of Arthur's triggers ("It prints nothing"; "cd.. with no space is a different word").
- **Input** `[bash]` `cd ..`, `pwd` (ends one level up), `cd -` -> printed the practice folder path, although the lesson says `cd` prints nothing (see O-6). `[nav]` `next`. **Friction**: -1.

### 2.4 — Home and back
- **Read**: all. **Jargon**: "~ is its short name." (not used anywhere on this screen).
- **Input** `[bash]` `cd`, `pwd` (a different folder, ending `userhome`), `cd <full practice path>` typed from the screen (the display wrapped the line; silent), `pwd` to verify. `[nav]` `next`. **Friction**: -1.

### 2.5 — Names for places (20 lines)
- **Read**: all. **Jargon**: "relative path", "absolute path" (both defined in the same paragraph).
- **Input** `[bash]` `ls ..` -> hundreds of names from the parent folder scrolled by (the practice folder's parent is the host temp area). `ls ~` -> printed nothing. `ls -a ~` (my one check) -> `.` and `..` only. `[nav]` `next`.
- **Interpretation**: After `ls ..` I could not tell whether I had made a mess; after `ls ~` I could not tell whether it had worked, because no sentence said home is empty. No rejection occurred, so no charge. **Ladder**: none. **Friction**: -1.

### 2.6 — Making a folder
- **Input** `[bash]` `mkdir demo`, `ls -p` (lists `demo/`), `cd demo`, `pwd` (ends `/demo`). The lesson's own list served as the check. **Friction**: -1.

### Stage 2 gate
- **Q1** "What does cd .. do?" -> "goes up one level, to the folder that contains this one" accepted. **Q2** "~" -> "your home folder" accepted. **Q3** (in ~/projects, cd notes) -> `~/projects/notes` accepted.
- **Task** (mkdir practice, cd into it, confirm with pwd; "runs in .../stage2; pwd shows it"): I ran `pwd` first because I had been in `demo`; it ended `/stage2`, so the tutor had moved me. `mkdir practice`, `ls`, `cd practice`, `pwd`, `check` -> first check passed.
- **Friction after Stage 2 cleared: -2**.

### Stage 2 cleared — summary
- Lists `cd ~` although only `ls ~` was run (see O-8). **Input** `[nav]` `next`.

### Stage 3 intro — Stage 3: Files
- "rm removes for good. There is no Trash." Noted, will be careful. **Friction**: -2.

### 3.1 — Making files (20 lines)
- **Read**: all. **Jargon**: "The tutor put poem.txt and numbers.txt one folder up. Now make your own beside them." and "> sends what echo prints into a file instead of the screen."
- **Monologue**: Which folder am I standing in? `pwd` -> `.../stage3`. The listed commands have no `cd`, so I typed them as written. `ls -p` showed `hello.txt notes/ words.txt`, with no `poem.txt`, so my files are not "beside" them.
- **Input** `[bash]` `pwd`, `touch hello.txt`, `echo hi > words.txt`, `mkdir notes`, `ls -p`; `[nav]` `next`. Three silent commands in a row; the screen had warned about `>`; the final `ls -p` was my one check.
- **Friction**: -2 (a wrong turn did not occur; see O-3).

### 3.2 — Reading a file
- **Input** `[bash]` `cat words.txt` -> `hi`; `cat hello.txt` -> nothing (screen said so); `cat ../poem.txt` -> four lines. The `../` here explained "one folder up" from 3.1. **Friction**: -2.

### 3.3 — Reading a long file
- **Read**: all. **Input** `[bash]` `less ../numbers.txt` (prompt replaced by the file name), raw ` ` (Space; paged to 46), raw `q` (prompt returned), `[nav]` `next`. **Friction**: -2.

### 3.4 — Copy and move
- **Input** `[bash]` `cp hello.txt backup.txt`, `ls` (one check), `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls -p notes` -> `hi.txt`. **Friction**: -2.

### 3.5 — Removing
- **Input** `[bash]` `ls`, `rm backup.txt` (no "are you sure"), `ls` (gone). **Friction**: -2.

### Stage 3 gate
- **Q1** "Which command creates an empty file?" `touch` accepted. **Q2** (where is the file after rm) `gone` accepted. **Q3** "What single command renames old.txt to new.txt?" -> `mv old.txt new.txt` accepted.
- **Task** (notes.txt with hello; copy to backup.txt; rename to done.txt; remove backup.txt): `echo hello > notes.txt`, `ls`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`, `ls` (one check on the whole folder), `check` -> first check passed. The existing folder `notes` has a name close to `notes.txt`; I took care not to confuse them.
- **Friction after Stage 3 cleared: -3**.

### Stage 4 intro, 4.1 — The parts of a command
- **Read**: all. **Jargon**: "streams" in the stage title and intro (no definition anywhere in Stage 4); "option", "argument", "wc", "command -v" are glossed in the comments.
- **Input** `[bash]` `wc -l poem.txt` -> `4 poem.txt` (worked, the screen did not say which folder), `echo "hello world"`, `command -v vim` -> `/usr/bin/vim`. **Friction**: -3.

### 4.2 — Spaces and quotes
- **Input** `[bash]` `touch my notes.txt`, `ls` (two files `my`, `notes.txt`, plus a `seed.txt` I did not make), `touch "my notes.txt"`, `ls` (one file with a space). **Friction**: -3.

### 4.3 — The pipe
- **Jargon**: "seq 1 100 | wc -l  # 100: wc counted seq's lines" (`seq` never described; also "sort" and "head" only by the comment "list, sort, first ten").
- **Input** `[bash]` `seq 1 100 | wc -l` -> 100; `ls /usr/bin | wc -l` -> 932; `ls /usr/bin | sort | head` -> ten names. **Friction**: -3.

### 4.4 — Into a file
- **Input** `[bash]` `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt` -> two lines. **Friction**: -3.

### 4.5 — Pipe, then file
- **Input** `[bash]` `ls /usr/bin | wc -l > count-of-programs.txt`, `cat count-of-programs.txt` -> 932. **Friction**: -3.

### 4.6 — Many names at once
- **Jargon**: "The shell fills in the names before the command runs." (not needed).
- **Input** `[bash]` `ls *.txt`, `wc -l *.txt`. I did not type `rm *`. **Friction**: -3.

### Stage 4 gate
- **Q1** (what does command -v vim print) "a path to the program, such as /usr/bin/vim" accepted. **Q2** (> versus >>) accepted. **Q3** (why does `vim my notes.txt` open two files) "the shell splits the line on spaces, so my and notes.txt are two names unless you put quotes around them" accepted.
- **Task**: "1. Use seq and a pipe: count the lines of seq 1 100 and save that number to count.txt. 2. Use a glob to list every *.txt file in this folder." Stall: "a glob" (word not taught; I guessed it meant the star pattern, since `*.txt` is in the same sentence). `seq 1 100 | wc -l > count.txt`, `ls *.txt` (shows count.txt, doubles as my check), `check` -> first check passed.
- **Friction after Stage 4 cleared: -4**.

### Stage 5 intro, 5.1 — Programs that take over the screen
- **Input** `[bash]` `man ls`, raw `q`. **Friction**: -4.

### 5.2 — Leaving Vim
- **Jargon**: "Vim is a text editor." (defined), "vimtutor" (named in stage intro only).
- **Input** `[bash]` `vim`, then `:q` -> back at the prompt. **Friction**: -4.

### 5.3 — The copy and the file
- **Read**: all. **Jargon**: "working copy". The closing line "Type next to try both." has nothing to try on this screen (see O-9). **Input** `[nav]` `next`. **Friction**: -4.

### 5.4 — Throw it away
- **Input** `[bash]` `vim practice.txt`, raw `i`, raw `abc`, raw `\x1b`, `:q!`, `cat practice.txt` -> `before`. The `-- INSERT --` line was hard to read in the client's rendering, so I could not tell whether Esc had worked; I continued as the screen said and it did. **Friction**: -4.

### 5.5 — Keep it
- **Input** `[bash]` `vim practice.txt`, raw `i`, raw `xyz`, raw `\x1b`, `:wq`, `cat practice.txt` -> `xyzbefore`. **Friction**: -4.

### 5.6 — vimtutor
- **Jargon**: "brew install vim adds it." (`brew` unexplained). **Input** `[bash]` `command -v vimtutor` -> `/usr/bin/vimtutor`; `[nav]` `next`. **Friction**: -4.

### Stage 5 gate — recall then two-phase task
- **Q1** "How do you exit man ls?" -> "press q" accepted. **Q2** "After vim notes.txt, what makes Vim write your edit to the file?" -> "typing :w or :wq writes the copy back to the file" accepted.
- **Q3** "If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?" -> **"no, the changes were thrown away"** -> REJECTED with: "not quite. hint: Lesson 5.4: the working copy is a copy; the disk only changes when you write it."
  - **Interpretation** (in character): I said no. The hint repeats what I said in other words. I do not know what was wrong with my answer, so I shortened it to one word. **Friction +2** (rejection not understood).
  - **Ladder rung shown**: hint. It did not resolve the confusion (it does not say which word was missing); the next input `no` was a guess and was accepted.
- **Task phase 1** (cat practice.txt; vim, i, letters, Esc, :q!; cat practice.txt shows `before`): done; `check` -> first check passed.
- **Task phase 2** (vim, i, letters, Esc, :wq; cat practice.txt differs from `before`): `okbefore`; `check` -> first check passed. Both phases named the folder ("runs in .../stage5; pwd shows it").
- **Friction at finale**: -5 (gates) + 2 (one rejection) = **-3**.

### finale — You're ready for vimtutor
- Reply ended `[exited 0]`; sitting stopped at the finale. The summary shows the habit list, the install note and "The practice folder stays at ..." line.

## Per gate

| Gate | Recall attempts per question | Rejected verbatim | Rung | Task attempts and first `check` | Cleared |
| --- | --- | --- | --- | --- | --- |
| Stage 1 | 1, 1, 1 | none | none | 1 check; first check passed (three follow-ups answered correctly first time) | yes |
| Stage 2 | 1, 1, 1 | none | none | 1 check; first check passed | yes |
| Stage 3 | 1, 1, 1 | none | none | 1 check; first check passed | yes |
| Stage 4 | 1, 1, 1 | none | none | 1 check; first check passed | yes |
| Stage 5 | 1, 1, 2 | Q3: `no, the changes were thrown away` | hint (Lesson 5.4 pointer) | phase 1 first check passed; phase 2 first check passed | yes |

The checklist `○` markers were never shown unfinished; every `check` was run only after all steps.

## Terms met before a screen defined them

1. 1.2: "Inside a full-screen program (you'll meet one in Stage 3) the way out is q." Full-screen program; promised for later.
2. 1.3: "pwd printed the full name of your practice folder." Said before the learner has run `pwd`.
3. 1.4: "terminal → shell → program: the window, bash, and date." The first mention of terminal and program; "shell" first appears in the Orientation screen ("a real shell prompt").
4. Stage 1 cleared: the list names `clear`, which no lesson taught (1.2 teaches Ctrl+L only).
5. 2.2: "ls /  # a folder you are not in: the top of everything." No sentence says there is a single top or no drive letter.
6. 2.4: "Every user has a home folder. ~ is its short name." `~` is not used on that screen.
7. 4 (stage title and intro): "Commands and streams" / "join commands together and send what they print into files"; streams are never named in a lesson.
8. 4.3: "seq 1 100 | wc -l  # 100: wc counted seq's lines." `seq` is never described. Stage 4 cleared later lists "count lines, count out numbers  wc  seq".
9. Stage 4 gate task: "Use a glob to list every *.txt file in this folder." The word glob appears nowhere in 4.6 ("* matches any run of characters in a file name").
10. 5.6: "brew install vim adds it." and "install the full vim package"; `brew` and package are unexplained.
11. 5.3: "Type next to try both." There is nothing to try on 5.3 (the tries are 5.4 and 5.5).
12. Stage 1 gate Q3: "After whoami runs, where does its output go?" Output as a destination was not taught; "to the screen" was accepted.

## Did each screen say which folder he was in when it mattered?

- Stage 1 lessons: not stated; not needed. Stage 1 task: stated (`/stage1`).
- 2.1: tree with "you are here". 2.2 to 2.4: `pwd` was the check. 2.5: not stated; the `ls ..` result depended on it (parent of the practice folder, a crowded host folder). Stage 2 task: stated (`/stage2`); I ran `pwd` first because I had last been in `demo`, and the tutor had moved me.
- 3.1: not stated. "poem.txt and numbers.txt one folder up ... make your own beside them" is ambiguous: I was in `stage3`, the commands carry no `cd`, and the files appeared in `stage3`, not beside the poem. I needed `pwd` to find out. 3.2 clarified with `../poem.txt`. 3.3 to 3.5 and the Stage 3 task: stated by the task (`/stage3`).
- 4.1 to 4.6: not stated. `wc -l poem.txt` worked without `cd`, and `ls` in 4.2 showed `seed.txt`, which I did not make. Stage 4 task: stated (`/stage4`).
- 5.1 to 5.6: not stated ("A file called practice.txt is in this folder" does not name it). Stage 5 task: stated (`/stage5`), both phases.

## End of sitting

- **Final friction and where the persona quit**: -3 (unfloored); did not quit. Ended at the finale ("You're ready for vimtutor"; `[exited 0]`).
- **Friction by source**: reading/density charges 0; rejections +2 (one: Stage 5 gate Q3); mode confusion 0; gates cleared -5.
- **Stages or module cleared**: Stages 1, 2, 3, 4, 5; finale reached. Turns used 179 of 220.
- **Equivalent human sitting time (estimate)**: about 50 to 60 minutes: roughly 28 lessons at 1 to 2 minutes of reading each, retyping long paths, two stalls on dense screens, and five gate tasks with one or two checks per silent command.
- **Density notes (no friction charged; no long screen caused a rejection or wrong turn)**: the sitting summary reports only the welcome screen over its 20-row budget (21). Screens at 19 to 20 rows: 1.2, 1.3, 1.4, 2.1, 2.5, 3.1, the gate tasks. 2.5 (20 rows, relative versus absolute, two commands) was the densest teaching screen and was followed by the 300-row `ls ..` dump, but the dump did not cause a rejection.

### Candidate F-nnn

- **F-1** (a valid answer rejected). Screen: Stage 5 gate, recall 3 of 3 ("If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?"). Input: `no, the changes were thrown away`. Reply: "not quite. hint: Lesson 5.4: the working copy is a copy; the disk only changes when you write it." The shorter input `no` was then accepted. The reply gives no hint which word was missing, and the answer given agrees with the hint.

### Candidate O-nnn

- **O-1** Screen 2.5, input `ls ..`: the lesson says "look one level up without moving"; the output is several hundred unrelated names from the host's temp area, which also exposes the host's file names. Arthur could not tell whether he had caused it.
- **O-2** Screen 2.5, input `ls ~`: prints nothing; no sentence says the home folder is empty. Arthur needed `ls -a ~` to be sure the command had worked.
- **O-3** Screen 3.1: "The tutor put poem.txt and numbers.txt one folder up. Now make your own beside them." The commands that follow have no `cd` and create the files in `stage3`, not beside the poem; the screen never names the current folder (`pwd` was needed). Input: `pwd`, then `touch hello.txt`.
- **O-4** Screen 4.3: "seq 1 100 | wc -l  # 100: wc counted seq's lines." `seq` is never introduced. Stage 4 gate task: "Use a glob to list every *.txt file in this folder." The word "glob" is not taught in 4.6.
- **O-5** Screen "Stage 1 cleared": the list names `clear`, which was not taught.
- **O-6** Screen 2.3: "cd changes the folder you are standing in. It prints nothing", but input `cd -` printed the practice folder path.
- **O-7** Screen 1.3: "pwd printed the full name of your practice folder." is in the past tense before the learner has run `pwd`.
- **O-8** Screens 2.4 and "Stage 2 cleared": 2.4 introduces "~ is its short name" without a command that uses it (the commands are `cd` and a full path); the cleared list shows `cd ~`, which was not run.
- **O-9** Screen 5.3: "Type next to try both." There is nothing to try on 5.3; the tries are 5.4 and 5.5.
- **O-10** Screens 4.1 to 4.6 and 5.x lessons: the current folder is never named. In 4.2 `ls` showed a `seed.txt` that Arthur did not make, with no explanation.
- **O-11** Screen 5.6: "brew install vim adds it." (`brew` unexplained) and Stage 4 title "streams" (never named in a lesson).
- **O-12** Screens 5.4 and 5.5 under the sitting client: the `-- INSERT --` indicator was run together with the text typed ("i -- INSERT --xyzbefore"), so Arthur could not see when Esc had changed mode. This may be a client rendering artifact rather than a tutor defect.

## Debrief (out of character)

1. Stage 5 gate Q3: the hint sentence ("the working copy is a copy; the disk only changes when you write it") restates a correct answer and does not say what the checker wanted; `no` passed where `no, the changes were thrown away` did not.
2. 2.5 `ls ..` and `ls ~`: "look one level up without moving" is followed by the host's whole temp folder, and `ls ~` returns nothing; neither sentence prepares the learner for either result.
3. 3.1: "make your own beside them" does not match the folder where the commands run.
4. Stage 4 gate: "Use a glob" and 4.3 "seq 1 100" use words no screen defined.
5. The course otherwise worked for this persona: every silent command was announced or verifiable, `cd..` with no space and the `rm` warning were addressed before they could hurt, and all five tasks passed on the first `check`.
