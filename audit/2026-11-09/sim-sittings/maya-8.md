# Synthetic walkthrough — Maya, sitting 8

## Sitting

- Date: 2026-11-10
- Persona (file in `docs/sim-personas/`) and learner role: `maya.md`, Maya, 19, graphic design student (`search-first-skimmer`); adult beginner
- Persona sheet version: 0.2.0
- Scripted errors performed: none (Maya has no scripted schedule). Habits played, unscripted: Tab, Up and Ctrl+C and Ctrl+L as taught; unquoted spaced file name (3.1); `undo` as a Cmd+Z reflex (3.4); Esc then Ctrl+C inside `less` (3.3); Ctrl+C inside Vim (5.2).
- Turn cap: 240 (round 8). One turn = one `send` or one `raw`. Turns used: 168 (the client's `persona_inputs` count; the persona's own running tally drifted by a few, the bundle count is authoritative).
- Simulation rules confirmed (zero forward knowledge, reading limit of four prose lines with bold and `▶` lines always read, friction meter with density charge only when a skipped line later causes a rejection or wrong turn): yes
- Tutor revision and invocation: `35b9e26` (script `7e01410`); `sitting.py start` with no `--arg` (begins at the welcome screen), Bash `/bin/bash` 3.2.57, 80x24 pty.
- `--info` lines the persona was shown, if any: none

## Per screen

Per-screen blocks are condensed: screens where the only action was reading and typing the taught commands are grouped; screens with a stall, a habit or a rejection have their own block. The Read field is "skimmed" wherever the prose passed four lines.

### welcome, Orientation, Stage 1 intro, 1.1 — Running a command
- **Read**: welcome all; Orientation skimmed (the four steering words, the fifth `check`); 1.1 all (the "If bash answers No such file or command not found" paragraph is the fourth prose line).
- **Jargon**: "a real shell", "Four words steer the tutor instead: next, prev, show and quit"; "No such file or command not found".
- **Monologue**: Five stages, type next. Four words, got it. Three echoes, easy. Quotes just group, whatever.
- **Input** `[nav]` next x3, then `[bash]` `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` → output as shown, accepted. Then `[nav]` next.
- **Ladder rung**: none. **Friction**: 0.

### 1.2 — Four keys
- **Read**: all (short).
- **Jargon**: "Ctrl+C throws away the line you are typing; a fresh prompt".
- **Monologue**: Keys are like shortcuts, fine. Tab fills in a name like autocomplete.
- **Input** `[bash]` raw `echo p\t` → `echo poem.txt`; send Enter → `poem.txt`; raw Up → previous line returned; raw Ctrl+C → line discarded, fresh prompt; raw Ctrl+L → screen cleared, only the prompt; `[nav]` `show` → lesson returned; `[nav]` next.
- **Interpretation**: All four worked as promised.
- **Ladder rung**: none. **Friction**: 0.

### 1.3, 1.4, 1.5 — pwd/whoami/date, the shell in the act, who else types here
- **Read**: 1.3 all; 1.4 skimmed the last lines ("terminal → shell → program"); 1.5 skimmed (three habits).
- **Jargon**: "the full name of your practice folder"; "terminal → shell → program: the window, bash, and date."
- **Monologue**: pwd gives a crazy long path, not a folder I know. dtae is a typo on purpose, cute.
- **Input** `[bash]` pwd, whoami, date, date, dtae → `bash: dtae: command not found`; `[nav]` next x2.
- **Ladder rung**: none. **Friction**: 0.

### Stage 1 gate — recall
- **Read**: all.
- **Input** `[recall]`:
  - Q1 "In a normal bash window (not this tutor), which character usually ends the prompt?" → `it ends with a dollar sign` → accepted.
  - Q2 "What does pwd print?" → `it shows you which folder you're in` → rejected: "not quite. hint: Lesson 1.3: pwd printed one line starting with /. What does that line name?" → `it prints the full location of where you are right now` → accepted.
  - Q3 "After whoami runs, where does its output go?" → `it shows up on the screen right under what I typed` → accepted.
- **Interpretation**: Q2 rejection was not understood: "folder" was the word she had been given in the lesson prose ("the folder you are in") and the screen's own comment reads "where: the folder you are in".
- **Ladder rung**: hint; it named the line starting with `/` but did not say which word was missing, and she resolved it by rewording ("full location"), not by learning the expected word. **Friction**: +2 (rejection she did not understand) = 2.

### Stage 1 task
- **Input** `[bash]` whoami, pwd, date, then `[nav]` check, `[follow-up]` `[user]`, the full path typed out, `Tue` → all accepted on the first check.
- **Cleared**: yes, −1. **Friction**: 1.

### Stage 2, 2.1 to 2.6
- **Read**: 2.1 all; 2.2 all; 2.3 all (the `cd..` warning is in the first four prose lines); 2.4 skimmed the closing paragraph ("A full name works from anywhere."); 2.5 skimmed the relative/absolute paragraph ("A relative path starts where you are...", not read, no harm); 2.6 all.
- **Jargon**: "current directory", "the folder that contains this one", "A relative path", "An absolute path", "home is outside your practice folder".
- **Monologue**: A tree, like Finder's list view, ok. cd .. is the back button. cd on its own lands me somewhere else, pwd says a different folder than the practice one, and now I have to type that mile-long path to get back.
- **Input** `[bash]` pwd, ls, ls -p, ls -a, ls /, cd .., pwd, cd -, cd, pwd, `cd <full practice path>`, cd stage1, ls .., cd .., echo ~, mkdir demo, ls -p, cd demo, pwd; `[nav]` next each.
- **Interpretation**: `cd` with nothing took her to `shelltutor-sim-userhome-…`, a different folder from the practice folder named in the same lesson ("home is outside your practice folder"). The long path was typed out as printed on the screen.
- **Ladder rung**: none. **Friction**: 1.

### Stage 2 gate — recall
- **Input** `[recall]`:
  - Q1 "What does cd .. do?" → `it takes you back out to the folder that's above the one you're in` → accepted.
  - Q2 "What does ~ mean in a path?" → `it's the short way of saying my own home folder` → accepted.
  - Q3 "If I'm in ~/projects and I type cd notes, what folder am I in?" → `you'd be in the notes folder that's inside projects inside your home folder` → accepted.
- **Friction**: 1.

### Stage 2 task
- **Read**: skimmed ("This task runs in <long path>/stage2; pwd shows it" skipped as noise).
- **Input** `[bash]` mkdir practice, cd practice, pwd, `[nav]` check → passed on the first check. The tutor had already reset her to stage2, so the habit of not checking where she stood did no harm here.
- **Cleared**: yes, −1. **Friction**: 0.

### Stage 3 intro, 3.1 — Making files
- **Read**: all; "no spaces in the name yet" appears as a comment inside the command block.
- **Jargon**: "> sends what echo prints into a file instead of the screen."
- **Monologue**: I name files with spaces all the time in Finder. Try it.
- **Input** `[bash]` touch hello.txt, `echo hi > words.txt`, mkdir notes, then the habit `touch my notes.txt` → no output, no error; `ls -p` → `hello.txt	my		notes/		notes.txt	words.txt`.
- **Interpretation**: Two files, "my" and "notes.txt", and no tutor message about it. The command did not fail, so nothing told her it was wrong; she moved on unexplained. The explanation arrives at 4.2, one stage later.
- **Ladder rung**: none (no rejection). **Friction**: 0 (nothing was rejected).

### 3.2 — Reading a file; 3.3 — Reading a long file
- **Input** `[bash]` cat words.txt, cat hello.txt, `cat ../poem.txt`; `less ../numbers.txt`, raw Space (paged), raw Esc (habit: close the viewer; no effect), raw Ctrl+C (carried from 1.2; no effect, still in less), raw `q` → back at the prompt; next.
- **Interpretation**: The 3.3 prose says "Ctrl+C does nothing here; q is the way out." Maya read that line (inside her four lines) and tried it anyway as a test of what she had learned in 1.2; this is a habit performed, not a skipped-line charge, so no density charge. She stayed in `less` for two turns.
- **Ladder rung**: none. **Friction**: 0.

### 3.4 — Copy and move; 3.5 — Removing
- **Input** `[bash]` `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, then the habit `undo` → `bash: undo: command not found` (understood from 1.4, not charged), `mv hi.txt notes/`, `ls -p notes`; `ls`, `rm backup.txt`, `ls`.
- **Interpretation**: "There is no undo" in 3.5 answers the `undo` she had already tried at 3.4 one lesson earlier; she wrote it off as "the tutor guessed".
- **Ladder rung**: none. **Friction**: 0.

### Stage 3 gate — recall
- **Input** `[recall]`:
  - Q1 "Which command creates an empty file? touch mkdir new cat" → `you use touch to make a blank file` → accepted.
  - Q2 "After rm important.txt, where is the file? ~/.Trash on disk gone depends" → `it's deleted for good and doesn't go to the trash` → rejected ("not quite. hint: Lesson 3.5: what rm does, and whether it can be undone.") → `the file is gone and you can't get it back` → rejected (same hint, plus "Passed stages are saved. Type quit to leave now; the next run starts this stage from its first lesson. Type show to see the question again.") → `rm removes it and you can't undo it, so it's gone` → rejected (same) → `show` (re-displays the question and its four choices; no friction) → `it is gone` → accepted.
  - Q3 "What single command renames old.txt to new.txt?" → `you type mv old.txt new.txt` → accepted.
- **Interpretation**: Three rejections of answers that meant the same thing as the lesson ("There is no Trash and no undo", "removes a file at once and for good"). Maya had not noticed the question carried a row of four choices until `show` re-printed it. What finally worked was the exact choice word in a bare sentence.
- **Ladder rung**: hint, repeated three times without change; the hint named a lesson and a topic but never changed or narrowed. After the second miss the screen added the "Passed stages are saved / quit" menu, which Maya read as being shown the exit. **Friction**: +6 (three rejections, each not understood) = 6 on the corrected running total (see Final friction).

### Stage 3 task
- **Input** `[bash]` `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`, `[nav]` check → passed on the first check. (The `notes.txt` from the 3.1 habit already existed empty; `>` overwrote it.)
- **Cleared**: yes, −1. **Friction**: 5.

### Stage 4, 4.1 to 4.6
- **Read**: 4.1 all; 4.2 all; 4.3 skimmed ("Each piece is an ordinary command... | is Shift+Backslash"); 4.4 all; 4.5 all; 4.6 all.
- **Jargon**: "name, then options, then arguments"; "a stream of lines"; "A name with * in it is called a glob."
- **Monologue**: 4.2 is the thing that happened to me in 3.1: "touch my notes.txt # two files: my, and notes.txt". So that is why. Pipe is just "and then", a conveyor belt. `*.txt` is like a Finder search for .txt.
- **Input** `[bash]` `wc -l poem.txt`, `echo "hello world"`, `command -v vim`; `touch my notes.txt`, ls, `touch "my notes.txt"`, ls; `seq 1 100 | wc -l`, `ls /usr/bin | wc -l`, `ls /usr/bin | sort | head`; `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt`; `ls /usr/bin | wc -l > count-of-programs.txt`, `cat count-of-programs.txt`; `ls *.txt`, `wc -l *.txt`.
- **Ladder rung**: none. **Friction**: 5.

### Stage 4 gate — recall
- **Input** `[recall]`:
  - Q1 "What does command -v vim print, if Vim is installed?" → `it prints the path to where vim is on your computer` → accepted.
  - Q2 "What is the difference between > and >>?" → `the single one wipes out what was in the file and the double one adds onto the end` → accepted.
  - Q3 "Why does vim my notes.txt open two files instead of one?" → `because the space splits it into two separate names unless you put quotes around it` → accepted.
- **Friction**: 5.

### Stage 4 task
- **Input** `[bash]` `seq 1 100 | wc -l > count.txt`, `ls *.txt`, `[nav]` check → passed on the first check.
- **Cleared**: yes, −1. **Friction**: 4.

### Stage 5 intro, 5.1 to 5.6
- **Read**: 5.1 all; 5.2 skimmed the last two prose lines (`:q<Enter>` and "<Enter> means the key"); 5.3 all; 5.4, 5.5 all; 5.6 skimmed the install lines.
- **Jargon**: "Some programs take over the screen"; "working copy"; "`:q<Enter>`... <Enter> means the key, not letters to type".
- **Monologue**: man pages are a wall of text, q. A black screen of tildes in Vim: Ctrl+C, that always worked. It says type :qa. The lesson says :q, use that. :w is the save button, the "working copy" is like the autosave draft.
- **Input** `[bash]` `man ls`, raw `q`; `vim`, raw Ctrl+C (habit; Vim prints "Type  :qa  and press <Enter> to exit Vim"), `:q`; `vim practice.txt`, raw `i`, raw `hey`, raw Esc, `:q!`, `cat practice.txt` → `before`; `vim practice.txt`, raw `i`, raw `maya`, raw Esc, `:wq`, `cat practice.txt` → `mayabefore`; `command -v vimtutor` → `/usr/bin/vimtutor`.
- **Ladder rung**: none. **Friction**: 4.

### Stage 5 gate — recall
- **Input** `[recall]`:
  - Q1 "How do you exit man ls?" → `you press the q key to get out of it` → accepted.
  - Q2 "After vim notes.txt, what makes Vim write your edit to the file?" → `you have to save it by typing colon w, or colon w q to save and close` → accepted.
  - Q3 "If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?" → `no, the file stays exactly how it was because the changes get thrown away` → rejected ("not quite. hint: Lesson 5.4: the working copy is a copy; the disk only changes when you write it.") → `no, it didn't change because you only edited the copy and never wrote it back` → rejected (same hint, plus the "Passed stages are saved. Type quit to leave now..." lines).
- **Interpretation**: Both answers say the file did not change and give the reason the hint names ("the working copy is a copy; the disk only changes when you write it"). The hint repeats the lesson without saying what the checker wants.
- **Ladder rung**: hint, shown twice, identical; did not resolve it. **Friction**: +4 (two rejections, not understood) = 8. QUIT AT 8.

## Per gate

- **Stage 1 recall**: Q1 1 attempt; Q2 2 attempts (rejected verbatim: `it shows you which folder you're in`); Q3 1 attempt. Rung reached: hint. Task: first check passed (3 of 3 follow-ups: `[user]`, the path, `Tue`). Checklist `○`: none seen. Cleared.
- **Stage 2 recall**: 1, 1, 1 attempts; no rejections; no rung. Task: first check passed. Cleared.
- **Stage 3 recall**: Q1 1; Q2 4 attempts (rejected verbatim: `it's deleted for good and doesn't go to the trash`; `the file is gone and you can't get it back`; `rm removes it and you can't undo it, so it's gone`; accepted: `it is gone`); Q3 1. Rung reached: hint (x3, identical). Task: first check passed. Cleared.
- **Stage 4 recall**: 1, 1, 1 attempts; no rejections. Task: first check passed. Cleared.
- **Stage 5 recall**: Q1 1; Q2 1; Q3 2 attempts, both rejected (verbatim above), not accepted before quitting. Task not reached. Not cleared.

### The fifteen recall questions

| # | Question | Answer typed (verbatim) | Result |
| --- | --- | --- | --- |
| 1.1 | Which character usually ends the prompt? | `it ends with a dollar sign` | accepted |
| 1.2 | What does pwd print? | `it shows you which folder you're in` | rejected |
| 1.2 | (second try) | `it prints the full location of where you are right now` | accepted |
| 1.3 | After whoami runs, where does its output go? | `it shows up on the screen right under what I typed` | accepted |
| 2.1 | What does cd .. do? | `it takes you back out to the folder that's above the one you're in` | accepted |
| 2.2 | What does ~ mean in a path? | `it's the short way of saying my own home folder` | accepted |
| 2.3 | If I'm in ~/projects and I type cd notes, what folder am I in? | `you'd be in the notes folder that's inside projects inside your home folder` | accepted |
| 3.1 | Which command creates an empty file? | `you use touch to make a blank file` | accepted |
| 3.2 | After rm important.txt, where is the file? | `it's deleted for good and doesn't go to the trash` | rejected |
| 3.2 | (second) | `the file is gone and you can't get it back` | rejected |
| 3.2 | (third) | `rm removes it and you can't undo it, so it's gone` | rejected |
| 3.2 | (fourth, after `show`) | `it is gone` | accepted |
| 3.3 | What single command renames old.txt to new.txt? | `you type mv old.txt new.txt` | accepted |
| 4.1 | What does command -v vim print, if Vim is installed? | `it prints the path to where vim is on your computer` | accepted |
| 4.2 | Difference between > and >>? | `the single one wipes out what was in the file and the double one adds onto the end` | accepted |
| 4.3 | Why does vim my notes.txt open two files? | `because the space splits it into two separate names unless you put quotes around it` | accepted |
| 5.1 | How do you exit man ls? | `you press the q key to get out of it` | accepted |
| 5.2 | After vim notes.txt, what makes Vim write your edit to the file? | `you have to save it by typing colon w, or colon w q to save and close` | accepted |
| 5.3 | Quit with :q! after edits: did the file on disk change? | `no, the file stays exactly how it was because the changes get thrown away` | rejected |
| 5.3 | (second) | `no, it didn't change because you only edited the copy and never wrote it back` | rejected |

Fifteen questions, fourteen accepted, one never accepted (5.3). Of the fourteen accepted, eleven passed first time; the three that needed retries were 1.2 (one rejection), 3.2 (three rejections).

## End of sitting

- **Final friction**: 8, quit at Stage 5 gate, recall question 3 of 3 (screen id "STAGE 5 — GATE", question "If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?"). By source: rejections 6 x +2 = +12 (Stage 1 Q2 x1, Stage 3 Q2 x3, Stage 5 Q3 x2); reading-limit charges 0; mode confusions 0; gates cleared 4 x −1 = −4. Total 12 − 4 = 8. Note: during the sitting the persona's running total was kept wrong by 1 from Stage 2 onward (the Stage 2 clear was not subtracted), so it read 7, 6, 5 where the correct values were 6, 5, 4; the final correct total, 8, matches the persona's decision to quit after the last rejection (persona's own tally read 9). No decision before the end would have changed: the persona never had to choose between continuing and quitting before the last rejection.
- **Stages or module cleared**: Stages 1, 2, 3, 4 (progress 4). Stage 5 lessons 5.1 to 5.6 seen; gate recall 2 of 3, task not reached. The bundle's result.tap reports "cleared: nothing cleared; progress 4", it does not count partial default-entry sittings.
- **Equivalent human sitting time** (estimate): about 50 to 60 minutes for the 168 turns, plus roughly 5 minutes lost on the three repeated rejections in Stage 3 and the two in Stage 5.
- **Candidate F-nnn**
  - **F-a** (Stage 5 gate, question "If you open notes.txt in vim, type some letters, and quit with :q! — did the file on disk change?"): inputs `no, the file stays exactly how it was because the changes get thrown away` and `no, it didn't change because you only edited the copy and never wrote it back` both rejected, with the identical hint "Lesson 5.4: the working copy is a copy; the disk only changes when you write it." Both answers say no and give the reason the hint states. Ended the sitting at friction 8.
  - **F-b** (Stage 3 gate, question "After rm important.txt, where is the file?"): `it's deleted for good and doesn't go to the trash`, `the file is gone and you can't get it back` and `rm removes it and you can't undo it, so it's gone` all rejected with the identical hint; only `it is gone` was accepted. The first three say the same thing as "rm removes a file at once and for good. There is no Trash and no undo." on 3.5. Cost +6.
  - **F-c** (Stage 1 gate, question "What does pwd print?"): `it shows you which folder you're in` rejected; the screen on 1.3 says "pwd # where: the folder you are in" and "prints the full name of your practice folder". The hint ("pwd printed one line starting with /. What does that line name?") asks a question without giving the expected word. `it prints the full location of where you are right now` was accepted.
  - **F-d** (Stage 3, lesson 3.1, `touch my notes.txt`, after the comment "no spaces in the name yet"): command succeeds silently and creates two files ("my" and "notes.txt"); the name was reused later in the Stage 3 gate task (`notes.txt` already existed). Not a tutor defect on its own; it is a place where a learner following a real habit gets no feedback until 4.2.
- **Candidate O-nnn**
  - **O-a** (every gate hint after a rejection): "not quite. hint: Lesson 3.5: what rm does, and whether it can be undone." is shown unchanged after the second and third rejection of the same question; the ladder does not advance within the sitting (message, hint, facts, worked example never advanced past hint).
  - **O-b** (Stage 3 gate recall Q2, after the second rejection): "Passed stages are saved. / Type quit to leave now; the next run starts this stage from its first lesson." appears after two misses and reads as an invitation to leave, at friction 4 to 6.
  - **O-c** (Stage 3 gate recall Q2, first display): "~/.Trash    on disk    gone    depends" sits under the question as a row of options; the instruction at the top says "Type your answer in words", and Maya typed sentences without noticing the options until `show` re-displayed the question. The word "words" and the option row point in two directions.
  - **O-d** (2.4): "pwd # home is outside your practice folder" and "cd # with nothing after it: go home", where the practice folder was itself named "shelltutor-sim-home-…" (printed in the lesson), so "home" and "your practice folder" appear as the same thing on the page and as two different folders on the next `pwd`.
  - **O-e** (3.3, "Ctrl+C does nothing here; q is the way out." after 1.2: "Ctrl+C is the way out at a prompt."): carried-over reflex; the Ctrl+C, then Esc then q path took three inputs, no message appeared.
  - **O-f** (5.2, "To leave, type :q and press Enter." and Vim's own message "Type  :qa  and press <Enter> to exit Vim" after Ctrl+C): two different exit words on the screen within the same two inputs.
  - **O-g** (2.4/2.1, the practice-folder path, 78 characters): the `cd /var/folders/...` line wraps on an 80-column pty; typed out by hand from the screen with no Tab help, and "Tab finishes a word" from 1.2 is not mentioned again.
  - **O-h** (3.3 screen height): "Reading a long file" renders 24 lines, over the 20-line budget in the bundle's table; the less pager itself fills the screen (the `less` output, not prose).
  - **O-i** (density, informational, no friction): over-length screens noted by the bundle: the welcome screen (21 lines), 3.3 (24). Skimmed prose that caused no later problem: 2.4 closing paragraph, 2.5 relative/absolute paragraph, 4.3 closing, 5.2 `<Enter>` sentence, 5.6 install lines.
- **Debrief** (out of character):
  - 5.3 gate recall Q3: the hint "the working copy is a copy; the disk only changes when you write it" restates the lesson; neither of two answers that said exactly that was accepted.
  - 3.2 gate recall Q2: "After rm important.txt, where is the file?" with the option row "~/.Trash on disk gone depends" versus the top-of-screen sentence "Type your answer in words": four equivalent paraphrases of lesson 3.5 were rejected, and the one accepted was the bare option word in a sentence.
  - 1.2 gate recall Q2: the hint "What does that line name?" asks a question whose answer ("the folder", the word she had already typed) is what was rejected.
  - 3.1: "touch my notes.txt" produced no message, and the sentence "# an empty file; no spaces in the name yet" is a comment inside the command block, which a skimming reader passes.
  - Stage 3 recall Q2 after rejection two: "Type quit to leave now; the next run starts this stage from its first lesson."
