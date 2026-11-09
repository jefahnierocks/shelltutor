# Synthetic walkthrough: Arthur, sitting 4

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/arthur.md` (Arthur, 64, retired logistics manager, `dos-literalist`); learner role: adult with some shell
- Persona sheet version: 0.2.0
- Simulation rules confirmed: zero forward knowledge, density charge only when a long screen's content later causes a rejection or wrong turn (Arthur v0.2 Reading section), friction meter (+2 rejected input not understood, +1 mode confusion, -1 gate cleared, quit at 8)
- Tutor revision: 3045f88 (script 13847ef). Invocation: `sitting.py start --persona arthur`, no `--arg` (begins at the welcome screen), Bash `/opt/homebrew/bin/bash` 5.3.20. Sitting directory `sitting-arthur-4`.
- `--info` lines shown: none.
- Process deviation: the sitting ran to 154 persona inputs (summary.md `persona_inputs: 154`), over the 120-turn hard cap. About 45 of those were raw single keystrokes (Tab, arrows, `i`, letters, Esc, `q`) inside Vim, `less` and `man`. The sitting reached the finale, not the cap's stopping point, so it was not cut off.

Screens are labelled by the header the server shows (stage and lesson id; `task` for gate screens). Monologues are condensed from the `note` calls recorded in `events.jsonl`. The login name is written `[user]`.

## Per screen

### Welcome — SHELLTUTOR, a vimtutor prerequisite course
- **Read**: all.
- **Jargon**: "a vimtutor prerequisite course" (vimtutor never defined here).
- **Monologue**: vimtutor? No idea what that is, but it says type next.
- **Input** `[nav]` `next` -> accepted.
- **Ladder**: none. **Friction**: 0.

### Orientation
- **Read**: all. **Jargon**: none new. **Input** `[nav]` `next` -> accepted. **Friction**: 0.

### Stage 1 intro
- **Read**: all. **Input** `[nav]` `next` -> accepted. **Friction**: 0.

### 1.1 — running commands
- **Read**: all. **Jargon**: "# spaces separate words" (a trailing comment on the command line; he leaves it off).
- **Monologue**: three commands to try; I leave off the part after the hash, it looks like a note.
- **Inputs** `[bash]` `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` -> output each time. `next`.
- **Ladder**: none. **Friction**: 0.

### 1.2 — keyboard habits
- **Read**: all. **Jargon**: "Ctrl+C", "less (Stage 3)" ("never been told what less is").
- **Monologue**: Tab: type `echo p`, Tab, it fills `poem.txt`, Enter. Up arrow brings the line back; Ctrl+C throws it away. Ctrl+L: everything vanished, did I break it? The screen said `show` brings the lesson back.
- **Inputs** `[bash]`: raw `echo p`, raw Tab (-> `echo poem.txt`), raw Enter, raw Up, raw Ctrl+C (-> `^C`, fresh prompt), raw Ctrl+L (screen blank), `show` (lesson returned), `next`.
- **Interpretation**: blank screen after Ctrl+L was alarming; `show` rescued it because the screen had said so.
- **Ladder**: none. **Friction**: 0.

### 1.3 — where am I, who am I, when is it
- **Read**: all. **Jargon**: none. "Where is the drive?" trigger on first `/`: pwd printed a path with no drive letter.
- **Inputs** `[bash]` `whoami` (printed `[user]`), `pwd`, `date`, `next`. **Friction**: 0.

### 1.4 — the shell, caught in the act
- **Read**: all. **Jargon**: none ("terminal -> shell -> program" is defined on screen).
- **Inputs** `[bash]` `date`, `dtae` (-> `bash: dtae: command not found`, as the screen said), `next`. **Friction**: 0.

### 1.5 — who else types here
- **Read**: all. **Input** `[nav]` `next`. **Friction**: 0.

### Stage 1 gate — recall
- Q1 "which character usually ends the prompt?" `$` -> accepted.
- Q2 "What does pwd print?" `the folder you are in` -> accepted.
- Q3 "After whoami runs, where does its output go?" Four inputs `[recall]`:
  1. `it comes back to me on the screen in the terminal window` -> "not quite. try again." + hint ("Lesson 1.4: a program's output does not go into a file by itself; it comes straight back to you."). +2 (friction 2).
  2. `it comes straight back to you` (the hint's own words) -> rejected; hint repeated plus "Answer in a few words, like the lesson did, not a full sentence." +2 (friction 4).
  3. `back to you` -> rejected; same hint and same line. +2 (friction 6).
  4. `the screen` -> accepted.
- **Monologue**: I said it comes back to me. I used its own words. It still says no. Why? Then the guess at a place name worked, and I do not know what the rule was.
- **Ladder**: hint, shown three times, never advanced. It did not resolve the confusion; the hint's wording was tried verbatim and rejected. Only a guess at a different word cleared it.

### Stage 1 gate — task
- **Inputs** `[bash]` `whoami`, `pwd` (path ends `/stage1`), `date`, `check` -> three follow-ups `[follow-up]`: `[user]`, the full path typed by hand, `Mon`. All accepted. Stage 1 cleared.
- **Friction**: 5 (gate cleared -1).

### Stage 2 intro and 2.1 — where you are
- **Read**: all. Tree shows the home folder marked "you are here"; `pwd` agreed. **Input** `[bash]` `pwd`, `next`. **Friction**: 5.

### 2.2 — ls: what is here
- **Read**: all. **Jargon**: "hidden names: those starting with ." (explained on screen, new to him).
- **Inputs** `[bash]` `ls -p` (matched his prediction), `dir` (DOS habit -> `bash: dir: command not found`, understood from 1.4, no charge), `ls /`, `next`. **Friction**: 5.

### 2.3 — cd: moving
- **Read**: all. The warning "cd.. with no space is a different word" was noticed and obeyed.
- **Inputs** `[bash]` `cd ..` (silent: "Did it do it? Nothing happened."), `pwd` (parent path), `cd -` (printed the place), `next`. **Friction**: 5.

### 2.4 — names for places
- **Read**: all. **Jargon**: "Absolute paths start from the root, /" (root of what?).
- **Inputs** `[bash]` `mkdir demo` (silent, worried), `ls -p` (`demo/` appeared), `next`. **Friction**: 5.

### Stage 2 gate
- Recall: `go up one level` ok; `your home folder` ok; `~/projects/notes` ok. No rejections.
- Task: `show`, `pwd` (stage2), `mkdir practice`, `cd practice`, `pwd`, `check` -> cleared first try. **Friction**: 4.

### Stage 3 intro, 3.1, 3.2, 3.3
- Intro **Jargon**: "touch", "timestamp". 3.1: `touch hello.txt`, `ls`, `mkdir notes`. 3.2 (about 19 lines, read in full): `cat hello.txt` (silent, "probably empty" had warned him), `cat ../poem.txt`, `less ../numbers.txt`, raw `q` -> back. 3.3: stall at "rm <only-now-that-you-are-sure>" (decided it is a reminder, not a command); `cp hello.txt backup.txt`, `ls`, `mv hello.txt hi.txt`, `mv hi.txt notes/`, `ls`, `rm backup.txt`. All accepted. **Friction**: 4.

### Stage 3 gate
- Recall: `touch`, `gone`, `mv old.txt new.txt` all accepted.
- Task step 1 "create a file notes.txt containing the word hello": `touch` makes only empty files, so he copied the lesson-3.1 aside pattern: `echo hello > notes.txt` (silent; "Nothing printed, did I break it?"), `cat notes.txt` (`hello`). Then `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `ls`, `rm backup.txt`, `check` -> cleared.
- **Friction**: 3.

### Stage 4 intro, 4.1, 4.2, 4.3, 4.4
- Intro: "chain commands together with pipes, redirects, and globs" (none defined yet). 4.1 **Jargon**: "prints the path; exits 0". `command -v ls`, `command -v vim`. 4.2 **Jargon**: "input", "grep ^a" (what is the ^). `wc -l poem.txt`, `seq 1 100 | wc -l` (100), `ls /usr/bin | sort | head`. 4.3 explained the `>` he had copied at the Stage 3 gate: `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt`, `wc -w < poem.txt` (28). 4.4: `ls *.txt` (recognised `*` from DOS wildcards; did not try `rm *`). All accepted. **Friction**: 3.

### Stage 4 gate
- Recall: `the path`, `> overwrites, >> appends`, `the shell splits on spaces` all accepted.
- Task: `seq 1 100 | wc -l > count.txt`, `ls *.txt`, `check` -> cleared. **Friction**: 2.

### Stage 5 intro, 5.1, 5.2, 5.3, 5.4, 5.5
- Intro **Jargon**: "why Vim has :w, :q, and :q!" (Vim never defined). 5.1: `man ls`, raw `q`. 5.2 **Jargon**: "discard form" (discard what?): `vim --version` (page of build text), `vim` (full-screen, splash says `:q<Enter>`; he typed `:q` and pressed Enter, not the angle brackets). 5.3: `next`. 5.4 **Jargon**: "insert mode" (says vimtutor will teach it): `vim practice.txt`, raw `i`, raw `xyz`, raw Esc (the terminal showed `^[` after it), `:q!`, `cat practice.txt` (`before`); second pass `i`, `abc`, Esc, `:wq`, `cat practice.txt` (`abcbefore`). 5.5 **Jargon**: "vimtutor may not be on PATH" (PATH never defined): `command -v vimtutor`. All accepted. **Friction**: 2.

### Stage 5 gate
- Recall: `q`, `:w`, `no` accepted, no rejections.
- Phase 1: `cat practice.txt`, `vim practice.txt`, `i`, `zzz`, Esc, `:q!`, `cat practice.txt`, `check` -> accepted. Phase 2: `vim practice.txt`, `i`, `k`, Esc, `:wq`, `cat practice.txt` (`kbefore`), `check` -> finale screen, `[exited 0]`.
- **Friction**: 1.

## Per gate

- **Stage 1**: Recall Q1 1 attempt, Q2 1 attempt, Q3 4 attempts. Rejected verbatim: `it comes back to me on the screen in the terminal window`, `it comes straight back to you`, `back to you`. Rung reached: hint (repeated, with the added "a few words" line); no facts or worked-example rung appeared. Task: 1 attempt, follow-ups all right. Cleared.
- **Stage 2**: Recall 3 of 3 first try. Task 1 attempt. Cleared.
- **Stage 3**: Recall 3 of 3 first try. Task 1 attempt (`check` did not mark any item). Cleared.
- **Stage 4**: Recall 3 of 3 first try. Task 1 attempt. Cleared.
- **Stage 5**: Recall 3 of 3 first try. Task phase 1 and phase 2, one attempt each. Cleared.

## End of sitting

- **Final friction**: 1. Did not quit; sitting ended at the finale (`[exited 0]`, "You're ready for vimtutor.").
- **Friction by source**: reading charges 0 (no long screen caused a rejection or wrong turn); rejections 3 x +2 = +6 (all Stage 1 gate Q3); mode confusion 0; gates cleared 5 x -1 = -5. Total 6 - 5 = 1. Peak friction was 6, at the Stage 1 gate Q3.
- **Stages cleared**: 1, 2, 3, 4, 5.
- **Equivalent human sitting time (estimate)**: about 60 to 75 minutes, higher than the tutor's 45 to 60 minute claim because of the long silent-command checking, the Q3 retries and hand-typing the long path.
- **Density notes (no friction charged)**: screens over 14 lines that caused no wrong turn: Orientation, 1.2, 2.3, 3.2 (about 19 lines), 4.2, 4.3, 5.2, 5.4. None produced a rejection or wrong turn, so no +1 was applied.

### Candidate F-nnn
- **F-a** (Stage 1 gate, Q3 "After whoami runs, where does its output go?"): valid answers rejected. Inputs `it comes back to me on the screen in the terminal window`, `it comes straight back to you` and `back to you` were each answered "not quite. try again."; `the screen` was accepted. The hint on screen ("it comes straight back to you") is itself rejected when typed.
- **F-b** (Stage 1 gate, same Q3): the follow-up line "Answer in a few words, like the lesson did, not a full sentence." appears only after the second rejection and the ladder never moved past the hint through four attempts.

### Candidate O-nnn
- **O-a** (Stage 3 gate task, step 1): "create a file notes.txt containing the word hello" requires redirection, which appears only as an aside in 3.1 ("To create a file with content, use redirection (Stage 4): echo \"first line\" > greeting.txt") and is taught in 4.3. He completed it by copying the aside, then the command printed nothing.
- **O-b** (1.2): Ctrl+L blanks the lesson; the instruction "show brings the lesson back" is the only recovery cue.
- **O-c** (1.1): "echo I am at the shell      # spaces separate words" shows a trailing comment inside a command the learner is told to type.
- **O-d** (undefined terms, quoted): "less (Stage 3)" (1.2), "Absolute paths start from the root, /" (2.4), "prints the path; exits 0" (4.1), "grep ^a" and "input" (4.2), "discard form" (5.2), "type i to enter insert mode (vimtutor will teach modes)" (5.4), "vimtutor may not be on PATH" (5.5), "a vimtutor prerequisite course" (Welcome).
- **O-e** (2.1): the tree marks the home folder "you are here" while the previous gate had left the prompt in `.../stage1`; `pwd` then agreed with the tree.
- **O-f** (5.4 and gate phase screens): after Esc the terminal shows `^[` on the Vim line; he proceeded but noted it as odd.
- **O-g** (silent commands): `cd ..`, `mkdir demo`, `touch`, `cp`, `mv`, `rm` all printed nothing; each time he checked with `pwd` or `ls`, as the lessons suggested. The Stage 3 `echo hello > notes.txt` was the one silent case no screen had prepared him for.
- **O-h** (pace): Stage 1 to 3 held friction between 0 and 2 until the Q3 gate; the gate -1 refund then kept friction falling to 1 even after a 6 peak.

### Debrief (out of character)
- Stage 1 Q3 is the only real friction in the sitting; the sentence "it comes straight back to you" in the hint is rejected when typed, and "the screen" was accepted without any sentence on screen using that word.
- "To create a file with content, use redirection (Stage 4): echo \"first line\" > greeting.txt" (3.1) is the only preparation for the Stage 3 gate's "containing the word hello".
- "Exit keys: man and less q · vim :q then Enter (Lesson 5.3)" (5.1) and "Memorize it." (5.2) read clearly; Stage 5 produced no rejections.
- Undefined-term stalls were many but never blocked an input: "vimtutor", "less", "PATH", "root", "exits 0", "discard form", "insert mode".
- Long screens did not cause a wrong turn anywhere in this sitting, so no density charge applies.
