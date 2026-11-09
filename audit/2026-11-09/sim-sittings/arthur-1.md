# Synthetic walkthrough — one sitting (Arthur, sitting 1)

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/arthur.md` (Arthur, 64, `dos-literalist`); learner role: adult with some shell.
- Simulation rules confirmed: zero forward knowledge, reading limit (14 lines, +1 friction over it), friction meter (quit at 8). Screen length counted as body lines between the title bar and the footer, blank lines included.
- Tutor revision: a25caf7. Invocation: `sitting.py start --bash /opt/homebrew/bin/bash --persona arthur`, no `--arg` (bash 5.3.20), so the sitting began at the welcome screen. An earlier attempt with a relative `--bash bash` failed to exec and, after a restart, was stopped by the persona session in error before any turn; it is not part of this sheet. This sheet is sitting-arthur-2.
- `--info` lines shown: none.

## Per screen

### welcome — SHELLTUTOR, a vimtutor prerequisite course
- **Read**: all.
- **Jargon**: "a vimtutor prerequisite course"; "the practice prompt" (not yet shown).
- **Monologue**: It says type next. Does Enter follow? It did not say; I assume so. The folder is a very long path with a slash, not a drive letter.
- **Input** `[nav]` → `next` → accepted.
- **Interpretation**: Fine.
- **Ladder**: none.
- **Friction**: 0.

### orientation — Orientation
- **Read**: all (about 17 lines, over limit).
- **Jargon**: "the shell runs it"; "gate tasks"; "A fifth word, check, appears at gate tasks when relevant".
- **Monologue**: Four words, then a fifth that appears "when relevant". I read "or"-style lists as all required, so I wonder if I must use check.
- **Input** `[nav]` → `next` → accepted.
- **Ladder**: none.
- **Friction**: 1 (+1 density).

### stage 1 intro — STAGE 1: Where am I?
- **Read**: all. **Jargon**: none. **Input** `[nav]` → `next` → accepted. **Ladder**: none. **Friction**: 1.

### 1.1 — running commands
- **Read**: all (about 17 lines, over limit).
- **Jargon**: "its shape is the shape of every command"; "spaces separate words" / "quotes group them" (what grouping does is not shown, both lines print the same).
- **Monologue**: Typing exactly what is shown. I typed the `#` comment too because it sits on the same line. Both echoes printed identically, so I do not see what quotes do.
- **Input** `[bash]` → `echo hello` → `hello`; `echo I am at the shell      # spaces separate words` → `I am at the shell`; `echo "I am at the shell"` → `I am at the shell`; then `[nav]` `next` → accepted.
- **Ladder**: none.
- **Friction**: 2 (+1 density).

### 1.2 — keyboard habits
- **Read**: all (about 16 lines, over limit).
- **Jargon**: "bash finishes a word"; "Several matches? The first Tab fills in the shared part"; "clear too"; "the escape hatch".
- **Monologue**: Tab worked as described but the screen never said to press Enter after; I pressed Enter to see it. Ctrl+L: I know the DOS word, so I typed cls. "clear too" did not tell me that clear is a command here.
- **Input** `[bash]` → raw `echo p<Tab>` → line became `echo poem.txt`; Enter → `poem.txt`; raw Up arrow → `echo poem.txt` returned; Enter → `poem.txt`; `cls` → `bash: cls: command not found`; raw Ctrl+L → screen cleared; `[nav]` `show` → lesson redisplayed; raw Ctrl+C → `^C` and fresh prompt; `[nav]` `next` → accepted.
- **Interpretation of `cls`**: "command not found" left me thinking I did something wrong; nothing said what to type instead.
- **Ladder**: message only (bash's own error); did not resolve the confusion at that point. Lesson 1.4 explained it two screens later.
- **Friction**: 5 (+1 density, +2 `cls` rejected and not understood).

### 1.3 — where am I, who am I, when is it
- **Read**: all (short).
- **Jargon**: "print working directory"; "the tutor's own folder".
- **Monologue**: pwd printed a path starting with `/` and no drive letter. Where is C:? I will worry about it later.
- **Input** `[bash]` → `whoami` → `[user]`; `pwd` → `/var/folders/.../shelltutor-sim-home-xxxx`; `date` → date line; `[nav]` `next` → accepted.
- **Ladder**: none. **Friction**: 5.

### 1.4 — the shell, caught in the act
- **Read**: all (about 18 lines, over limit).
- **Jargon**: "bash: is the shell" vs "the program named bash"; "terminal → shell → program".
- **Monologue**: Typing a deliberate typo feels odd but I was told to. This explains my earlier `cls`.
- **Input** `[bash]` → `date` → date line; `dtae` → `bash: dtae: command not found`; `[nav]` `next` → accepted.
- **Ladder**: none. **Friction**: 6 (+1 density).

### 1.5 — who else types here
- **Read**: all (about 17 lines, over limit).
- **Jargon**: "An AI assistant that 'runs commands'".
- **Monologue**: Nothing to type. The point about reading the line before Enter I take.
- **Input** `[nav]` → `next` → accepted.
- **Ladder**: none. **Friction**: 7 (+1 density).

### stage 1 gate — Recall Q1
- **Read**: all. **Jargon**: "usually ends a shell prompt"; the options list "($, ;, :, or #)".
- **Monologue**: Nobody taught this. My own prompt ends in `>`, like the DOS prompt, and none of the four options is `>`. I answered what I see.
- **Input** `[recall]` → `>` → rejected: "not quite. try again." and the same question.
- **Interpretation**: It does not say what is wrong or what the answer is. I give up.
- **Ladder**: message only ("not quite. try again."); not a hint, did not resolve anything.
- **Friction**: 9 (+2 rejected input not understood). Quit.

## Per gate

- Recall: Q1 one attempt; rejected input verbatim `>`; rung reached: message. Q2, Q3 never seen.
- Task: not reached.
- Not cleared.

## End of sitting

- Final friction: 9 (rule 6 limit is 8). Quit at the stage 1 gate, Recall Q1.
- Stages or module cleared: none (Stage 1 lessons 1.1-1.5 read; gate not cleared).
- Equivalent human sitting time: estimate 12 to 18 minutes, driven by one DOS-bleed stall, five dense screens and one rejected answer.
- Turns used: 28 sends/raws (cap 90).

**Candidate F-nnn**
- None found with certainty. Possible: gate Q1, screen "stage 1 gate / Q1", input `>` rejected; the prompt the learner is looking at ends in `>`, so the question's answer set disagrees with the visible prompt. A maintainer must decide whether this is a false statement or an acceptable teaching gap.

**Candidate O-nnn**
- O: orientation (17 lines), 1.1 (17), 1.2 (16), 1.4 (18), 1.5 (17): each over Arthur's 14-line limit.
- O: 1.2, input `cls` -> `bash: cls: command not found`; text "clear too" does not tell a DOS reader that clear is a typed command, and the error is not explained until 1.4.
- O: 1.2, "Type echo p, press Tab" and "Enter runs it again": Tab and Up arrow lines do not say to press Enter after Tab; Arthur asked.
- O: 1.1, "# spaces separate words" and "# quotes group them into one": the two echo lines print identical output, so the claimed difference is invisible.
- O: 1.4, "bash: is the shell" and "the program named bash": two uses of the word bash.
- O: gate Q1, "Which character usually ends a shell prompt? ($, ;, :, or #)": concept never taught in lessons 1.1-1.5; visible prompt is `shelltutor>`; "not quite. try again." gives no hint on the first miss.
- O: 1.3, `pwd` output: a path starting with `/` and no drive letter; not explained until Stage 2 ("Stage 2 is all about folders").
- O: orientation, "A fifth word, check, appears at gate tasks when relevant": ambiguous whether it is required.

**Debrief (out of character)**
- "Which character usually ends a shell prompt? ($, ;, :, or #)" asks for a fact no lesson teaches, and the prompt on screen ends in `>`.
- "not quite. try again." offers nothing to go on after a first wrong answer.
- "Ctrl+L    clears the screen (clear too)" does not tell a DOS reader that `clear` is the command to type; `cls` fails with an unexplained error.
- Five of seven lesson screens run 16 to 18 lines.
