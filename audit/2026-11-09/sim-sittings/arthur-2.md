# Synthetic walkthrough — Arthur, sitting 2

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/arthur.md` (Arthur, 64, `dos-literalist`); learner role: adult with some shell.
- Simulation rules confirmed: zero forward knowledge, reading limit (14 lines; +1 for density), friction meter (+2 rejected input not understood, +1 over reading limit, +1 mode confusion, -1 gate cleared, quit at 8).
- Tutor revision: `afce3fe` (script `82792b6`). Invocation: `sitting.py start`, no `--arg` (begins at the welcome screen), Bash `/opt/homebrew/bin/bash` 5.3.20. Second Arthur sitting; no memory of the first.
- `--info` lines shown: none.
- Process note: the first two turns' `note` and `send` were issued in one shell call each (protocol slip, no effect on the record).

## Per screen

### welcome — SHELLTUTOR, a vimtutor prerequisite course
- **Read**: all. **Jargon**: "a vimtutor prerequisite course"; "this is the real thing, not a simulation".
- **Monologue**: vimtutor is not defined. It says my work happens in a long folder name; I will go on as told.
- **Input** `[nav]` -> `next` -> accepted.
- **Interpretation**: fine. **Ladder**: none. **Friction**: 0.

### orientation — Orientation
- **Read**: all. **Jargon**: "keyboard-only", "check appears at gate tasks".
- **Input** `[nav]` -> `next` -> accepted. **Friction**: 0.

### stage 1 intro — STAGE 1 — Where am I?
- **Read**: all. **Input** `[nav]` -> `next` -> accepted. **Friction**: 0.

### 1.1 — running commands
- **Read**: all. **Jargon**: "bash says command not found" (bash not yet introduced); "shape of every command".
- **Monologue**: three things to type. I type the comment after # too, since it was not said to leave it off.
- **Inputs** `[bash]` -> `echo hello` (printed hello); `echo I am at the shell      # spaces separate words` (printed the words, comment dropped); `echo "I am at the shell"    # quotes group them into one` (identical output).
- **Interpretation**: the quotes did nothing visible; I do not see what "group" meant. `[nav]` `next` accepted.
- **Ladder**: none. **Friction**: 0.

### 1.2 — keyboard habits
- **Read**: all. **Jargon**: "Tab", "Ctrl+L", "Ctrl+C", "escape hatch"; "poem.txt" appears with no word on where it came from.
- **Monologue**: Tab filled `echo poem.txt` as promised. Ctrl+L left a completely empty screen; I typed `show` and the lesson came back. Silent-looking clears worry me.
- **Inputs** `[bash]` -> `echo p` (no Enter), Tab, Enter (printed `poem.txt`); Up arrow brought the line back; Ctrl+C (fresh prompt, `^C` echoed); Ctrl+L (blank screen); `[nav]` `show` (lesson returned); `next`.
- **Ladder**: none. **Friction**: 0.

### 1.3 — where am I, who am I, when is it
- **Read**: all. **Jargon**: "working directory"; "A normal bash window's prompt usually ends in $".
- **Monologue**: `pwd` printed a path starting with `/` and no drive letter. Where is the drive? Nothing here says.
- **Inputs** `[bash]` -> `whoami`, `pwd`, `date` (all output seen); `next`.
- **Ladder**: none. **Friction**: 0.

### 1.4 — the shell, caught in the act
- **Read**: all. **Jargon**: "terminal -> shell -> program" (three words introduced in one breath).
- **Inputs** `[bash]` -> `date`, `dtae` -> `bash: dtae: command not found`, as the screen predicted. `next`.
- **Interpretation**: good, I did not break anything. **Friction**: 0.

### 1.5 — who else types here
- **Read**: all. **Jargon**: "An AI assistant that 'runs commands' for you".
- **Monologue**: why is an AI assistant mentioned in a course for me? Read it, moved on. `[nav]` `next`. **Friction**: 0.

### Stage 1 gate (recall) — STAGE 1 — GATE
- **Read**: all. Q1 `$` accepted; Q2 `the folder you are in` accepted; Q3 "After whoami runs, where does its output go?" see per-gate.
- **Monologue** (Q3): lesson 1.4 said it comes back to me. I said so, and was told "not quite". The hint repeated my own idea back.
- **Friction**: 4 (two rejections at Q3, +2 each).

### Stage 1 gate task — STAGE 1 — GATE TASK
- **Read**: all. **Inputs** `[bash]` -> `whoami`, `pwd` (path now ended `/stage1`, differing from before), `date`; `[nav]` `check`; `[follow-up]` -> `[user]`, the full pwd path, `Mon`. All accepted.
- **Friction**: 3 (-1 gate cleared).

### Stage 1 cleared
- **Read**: all. `[nav]` `next`. **Friction**: 3.

### stage 2 intro — Paths and the filesystem
- **Read**: all. **Jargon**: "the path symbols", `~`. `[nav]` `next`. **Friction**: 3.

### 2.1 — where you are
- **Read**: all (tree diagram, 12 lines). `[bash]` `pwd` matched the diagram. `[nav]` `next`. **Friction**: 3.

### 2.2 — ls: what is here
- **Read**: all. **Jargon**: "hidden names: those starting with ." (why would a name be hidden?).
- **Monologue**: ls is the dir command. Habit: I type `dir` first.
- **Inputs** `[bash]` -> `dir` -> `bash: dir: command not found` (understood from 1.4; no friction); `ls -p` (folders end in `/`); `ls -a` (shows `.`, `..`, `.progress`, `.shelltutor_history`); `ls /etc` (about 70 lines of names, over the 14-line limit, +1). `[nav]` `next`.
- **Friction**: 4.

### 2.3 — cd: moving
- **Read**: all. **Jargon**: "~ means $HOME" ($HOME undefined); screen ends "Type next to continue", never says to try the commands.
- **Monologue**: `cd /tmp` printed nothing. "Did it do it? Nothing happened." I confirmed with `pwd`. For "up one level" I typed the DOS form `cd..`, got `command not found` though `cd` had worked, rechecked the screen, saw the space. Then `cd ..` was silent; `pwd` gave `/`. Is that the drive? `cd` alone, silent; `pwd` gave a different folder (`...shelltutor-sim-userhome-...`), not the practice folder. Copied the long `cd` path back.
- **Inputs** `[bash]` -> `cd /tmp`, `pwd`, `cd..` (rejected), `cd ..`, `pwd`, `cd`, `pwd`, `cd <practice folder>`; `[nav]` `next`.
- **Ladder**: none (plain bash error). **Friction**: 6 (`cd..` +2).

### 2.4 — names for places
- **Read**: all. **Jargon**: "Absolute paths start from the root, /" (first answer to my drive question); "cat notes.txt" (cat never introduced); "~/projects" (a folder not in the tree).
- **Monologue**: so `/` is the top of everything. Slashes are forward ones. `[nav]` `next`. **Friction**: 6.

### Stage 2 gate (recall) — STAGE 2 — GATE
- **Read**: all. Q1 "What does cd .. do?"
- **Input** `[recall]` -> `it goes up one level, to the parent folder` -> "not quite. try again." with hint "Lesson 2.3: two dots name the folder that contains this one."
- **Interpretation**: that is what I said. I quit.
- **Ladder rung shown**: hint (first miss); it did not resolve the confusion, since the answer already matched the lesson's meaning.
- **Friction**: 8 (+2). QUIT.

## Per gate

- **Stage 1 recall**: Q1 1 attempt (`$`); Q2 1 attempt (`the folder you are in`); Q3 3 attempts. Rejected verbatim: `it comes back to me on the screen`, `back to me, in the window you type into`; accepted: `the terminal`. Rungs: hint on first miss, same hint repeated on second miss (plus "Passed stages are saved / Type quit / Type show" lines).
- **Stage 1 task**: 1 attempt, `check` passed; no `○` seen.
- **Stage 1**: cleared.
- **Stage 2 recall**: Q1 1 attempt, rejected verbatim `it goes up one level, to the parent folder`; hint rung only.
- **Stage 2**: not cleared.

## End of sitting

- **Final friction**: 8; quit at the Stage 2 gate, Q1 (screen id `task` under Stage 2, "STAGE 2 — GATE").
- **Stages cleared**: Stage 1 only. Sitting ended by persona quit (`stop` run; tutor not exited).
- **Equivalent human time (estimate)**: about 25 to 30 minutes for the screens and gates, plus pauses at silent commands and the empty Ctrl+L screen.
- **Friction ledger**: Stage 1 gate Q3 rejections +4; gate cleared -1; `ls /etc` density +1; `cd..` +2; Stage 2 Q1 rejection +2 = 8. `dir` -> command not found was counted 0 as understood from 1.4.

### Candidate F-nnn
- **Candidate F-001** — Stage 1 gate, Q3 "After whoami runs, where does its output go?": valid answers `it comes back to me on the screen` and `back to me, in the window you type into` were rejected, the latter being the hint's own wording. Only `the terminal` passed.
- **Candidate F-002** — Stage 2 gate, Q1 "What does cd .. do?": `it goes up one level, to the parent folder` rejected, matching the lesson 2.3 line "go up one level (to the parent folder)".
- **Candidate F-003** — Stage 2 gate, hint for Q1 ("two dots name the folder that contains this one") restates the question's idea rather than resolving why the answer failed; same pattern at Stage 1 Q3, where the hint repeated verbatim on the second miss.

### Candidate O-nnn
- **Candidate O-001** — 2.3: "cd ..  # go up one level" and the screen's silence; `cd..` -> `bash: cd..: command not found` does not say a space is missing.
- **Candidate O-002** — 2.3: "Stages 1 and 2 start every practice prompt in ..." versus `cd` landing in `...shelltutor-sim-userhome-...`, a different folder from the practice folder; "go home" and "your practice folder" diverge.
- **Candidate O-003** — 2.3: "cd ~          # also go home — ~ means $HOME": `$HOME` undefined; screen ends "Type next to continue" without telling the learner to try the commands.
- **Candidate O-004** — 2.2: `ls /etc` prints about 70 lines (host machine files, including backup names), over the reading limit; "Try a few" does not say which are needed.
- **Candidate O-005** — 1.2: "it becomes echo poem.txt": `poem.txt` is not introduced; Ctrl+L leaves an entirely empty screen ("clears the screen (clear too); show brings the lesson back").
- **Candidate O-006** — 1.1: "# quotes group them into one": the quoted line prints identically; the effect is invisible.
- **Candidate O-007** — 1.3/2.1: `pwd` ended `/stage1` in the gate task but the base folder on 2.1/2.2; unannounced change of folder.
- **Candidate O-008** — 1.3: path starting with `/` and no drive letter, unexplained until 2.4 "Absolute paths start from the root, /".
- **Candidate O-009** — welcome and 1.5: "a vimtutor prerequisite course" (vimtutor undefined); "An AI assistant that 'runs commands' for you".
- **Candidate O-010** — 2.4: "cat notes.txt" and "~/projects" used before `cat` is taught.
- **Candidate O-011** — 2.2: "hidden names: those starting with ." and `ls -a` listing `.` and `..`, unexplained.

### Debrief (out of character)
- Stage 1 Q3 "After whoami runs, where does its output go?": the lesson 1.4 sentence "what the program prints comes back to you" and the hint do not point to the accepted word `terminal`.
- Stage 2 Q1: the answer matched 2.3's "go up one level (to the parent folder)" and was rejected; the hint "two dots name the folder that contains this one" does not distinguish the failure.
- 2.3: "Stages 1 and 2 start every practice prompt in ..." and `cd` (alone) landing in a different folder; plus the absence of a try-it instruction on that screen.
- `bash: cd..: command not found` carries no pointer to the missing space.
- `ls /etc` wall of output with no stated reason to read it.
