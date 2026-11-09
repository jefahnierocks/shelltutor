# Synthetic walkthrough — one sitting (maya-1)

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/maya.md` (Maya, 19, `search-first-skimmer`); learner role: adult beginner
- Simulation rules confirmed: zero forward knowledge, reading limit (four prose lines, bold and ▶ read), friction meter (quit at 8). Rule 6 applied as: +1 for any screen with more than four prose lines.
- Tutor revision a25caf7; invocation `start --bash /bin/bash --persona maya` (no `--arg`; begins at the welcome screen). Bash 3.2.57.
- `--info` lines shown: none.

## Per screen

### welcome — SHELLTUTOR — a vimtutor prerequisite course
- **Read**: skimmed (read lines 1-4; skipped "Your work happens in ..." and "Commands you run yourself have your full authority"); read the ▶ line.
- **Jargon**: "a vimtutor prerequisite course"
- **Monologue**: A what-tutor? No idea what vim is. Skipping to the arrow.
- **Input** `[context: nav]` → `next` → accepted.
- **Interpretation**: Fine.
- **Ladder rung**: none.
- **Friction**: 1 (+1 over reading limit).

### orientation — Orientation
- **Read**: skimmed (read to "Type a command, press Enter"; skipped "you can't click mid-line to move the cursor", the four-words list and "A fifth word, check").
- **Jargon**: "the shell runs it"; "keyboard-only; you can't click mid-line to move the cursor"
- **Monologue**: Wall of text again. Four words, fine.
- **Input** `[context: nav]` → `next` → accepted.
- **Ladder rung**: none.
- **Friction**: 2 (+1 reading).

### Stage 1 intro — STAGE 1 — Where am I?
- **Read**: all. **Input** `[nav]` → `next` → accepted. **Friction**: 2.

### 1.1 — running commands
- **Read**: skimmed (read "type this and press Enter: echo hello"; skipped the explanation after the three commands, "its shape is the shape of every command").
- **Jargon**: "a name, then the words you hand it"
- **Monologue**: Type the first one. Second one: I copy the whole line, including the # bit, because nothing says where the command ends.
- **Input** `[bash]` → `echo hello` → hello. → `echo I am at the shell      # spaces separate words` → I am at the shell. → `echo "I am at the shell"    # quotes group them into one` → I am at the shell. → `next` `[nav]` → accepted.
- **Interpretation**: Ok it repeats what I say. Cute. Did the # part matter? No idea.
- **Ladder rung**: none.
- **Friction**: 3 (+1 reading).

### 1.2 — keyboard habits
- **Read**: skimmed (read the Tab and ↑ lines; skipped Ctrl+L's "show brings the lesson back" and the whole Ctrl+C line, "the escape hatch").
- **Jargon**: "bash finishes a word"; "Several matches? The first Tab fills in the shared part"; "Ctrl+C the escape hatch"
- **Monologue**: Tab is autocomplete, I know that one. Up is history. Ctrl+L, whatever.
- **Input** `[bash]` → `echo p` + Tab (raw) → line became `echo poem.txt`. → Enter → `poem.txt`. → ↑ (raw) → `echo poem.txt` back on the line. → Ctrl+L (raw) → screen cleared (prompt line still showed `echo poem.txt`). → `next` `[nav]` → typed onto the still-filled line, ran `echo poem.txt next`, printed `poem.txt next`. → `next` again → accepted.
- **Interpretation**: It echoed "poem.txt next". The old line was still sitting there after I cleared the screen. I thought clear meant empty.
- **Ladder rung**: none.
- **Friction**: 5 (+1 reading, +1 mode confusion: nav word typed into a prompt holding a recalled bash line).

### 1.3 — where am I, who am I, when is it
- **Read**: all (short).
- **Jargon**: "print working directory"
- **Monologue**: Three tiny commands. pwd gives a long ugly path. "Stage 2 is all about folders" - I'll find out.
- **Input** `[bash]` → `whoami` → `[user]`; `pwd` → /var/folders/.../shelltutor-sim-home-...; `date` → date string; `next` `[nav]` → accepted.
- **Interpretation**: It printed where I am as a long path. Is that a folder? Where is it in Finder?
- **Ladder rung**: none.
- **Friction**: 5.

### 1.4 — the shell, caught in the act
- **Read**: skimmed (read "Type date. Now type dtae." and the two example lines; skipped "Read who is speaking..." paragraph and the "terminal → shell → program" explanation).
- **Jargon**: "bash: is the shell"; "terminal → shell → program"; "a program called dtae"
- **Monologue**: Type the right one, then the wrong one on purpose. Okay. Why would anyone type it wrong on purpose.
- **Input** `[bash]` → `date` → date string. → `dtae` → `bash: dtae: command not found`. → `next` `[nav]` → accepted.
- **Interpretation**: It's the error it said it would be. Fine.
- **Ladder rung**: none (the screen pre-announced the error).
- **Friction**: 6 (+1 reading).

### 1.5 — who else types here
- **Read**: skimmed (read the first two lines; skipped the AI paragraph and the three-habit list; no commands on screen).
- **Jargon**: "Everything you typed went terminal → shell → program"; "folder it will run in"
- **Monologue**: An AI thing? There is nothing to type here. Next.
- **Input** `[nav]` → `next` → accepted.
- **Friction**: 7 (+1 reading).

### gate Q1 — Which character usually ends a shell prompt? ($, ;, :, or #)
- **Read**: all. **Jargon**: "shell prompt" (the screens said "the prompt", the only prompt Maya saw ended in `>`)
- **Monologue**: Ours ends in >, which isn't an option. # showed up next to comments, so guess.
- **Input** `[recall]` → `#` → "not quite. try again." → `$` → ✓.
- **Interpretation**: A guess; it was multiple choice. Nothing I read told me the answer.
- **Ladder rung**: message ("not quite. try again."); did not help, resolved by second guess.
- **Friction**: 7 (plain wrong guess, understood as wrong, no +2).

### gate Q2 — What does pwd print?
- **Read**: all. **Jargon**: none.
- **Monologue**: This one I saw: pwd tells me the folder I'm in.
- **Input** `[recall]` → `the folder I'm in` → "not quite. try again." (rejected).
- **Interpretation**: It said no to exactly what the screen told me ("print working directory — the folder you're in"). I don't know what it wants. I'm done.
- **Ladder rung**: message only ("not quite. try again."); did not resolve.
- **Friction**: 9 (+2 rejected input not understood). Quit.

## Per gate

- Recall: Q1 two attempts (`#` rejected, `$` accepted), message rung. Q2 one attempt, `the folder I'm in` rejected, message rung, not resolved. Q3 not seen.
- Task: not reached.
- Not cleared.

## End of sitting

- Final friction: 9; quit at gate Q2 (Stage 1 gate). Hard turn cap not reached. Bundle files copied beside the sheet as `maya-1.summary.md` and `maya-1.result.tap`.
- Stages or module cleared: none (lessons 1.1-1.5 viewed; gate not cleared).
- Equivalent human sitting time: estimate 12-15 minutes (lessons, one mis-typed nav, three gate attempts, abandonment).
- **Candidate F-nnn**
  - F-a: gate Q2, input `the folder I'm in` rejected with "not quite. try again." although it restates lesson 1.3's gloss ("pwd — print working directory — the folder you're in"). Only the message rung was offered.
  - F-b: gate Q1, `$` is not taught anywhere in lessons 1.1-1.5; the prompt Maya saw ends in `>`. Answer cannot be derived from the screens (zero-forward-knowledge reading).
- **Candidate O-nnn**
  - O-a: 1.2, Ctrl+L: "clears the screen (clear too); show brings the lesson back." After Ctrl+L the recalled line stayed in the buffer and `next` ran as `echo poem.txt next` (mode confusion; nothing said the line would remain).
  - O-b: 1.2, "Ctrl+C the escape hatch. If anything feels stuck, press it and you get a fresh prompt." sits as the last line of a dense block and was skipped.
  - O-c: 1.1, `echo I am at the shell      # spaces separate words`: the `# ...` comment is on the copyable line with no statement that it is not part of the command.
  - O-d: welcome and 1.4/1.5 pace: five of seven lesson screens exceeded four prose lines; 1.5 has no command to type and was entirely skimmed.
  - O-e: welcome, "a vimtutor prerequisite course" and 1.4, "bash: is the shell" / "terminal → shell → program": undefined jargon.
  - O-f: rule 6 gap: a wrong guess at a gate question the lessons never taught does not trigger a clear "rejected and not understood" for scoring; the sitting scored Q1 as 0 and Q2 as +2.
- **Debrief** (out of character):
  - The Q2 rejection of "the folder I'm in" is the decisive sentence: gate Q2 "What does pwd print?" against the 1.3 gloss "print working directory — the folder you're in".
  - Q1 "Which character usually ends a shell prompt?" asks for `$` though no lesson shows a `$` prompt.
  - 1.2 "Ctrl+L    clears the screen (clear too); show brings the lesson back." leaves the typed line, which swallowed `next`.
  - Welcome and 1.5 prose ("Your work happens in ... full authority", "An AI assistant that "runs commands" for you ...") carry the load past the four-line limit with nothing to do.
