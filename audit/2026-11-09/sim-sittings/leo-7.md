# Synthetic walkthrough — Leo, sitting 7

## Sitting

- Date: 2026-11-10
- Persona: `docs/sim-personas/leo.md`, Leo, 13, gamer-brute-forcer; learner role: child
- Persona sheet version: 0.3.0
- Scripted errors performed: (a) leading slash at the first Stage 1 command (`/echo hello`); (b) one-word guess at the first recall answer (`dtae`); (c) `check` first at the Stage 1 task NOT performed, because the sitting ended at friction 9 in the recall questions before the task was reached.
- Turn cap: 240 (round 7). One turn = one `send` or one `raw`. Turns used: 20
- Simulation rules confirmed (zero forward knowledge, reading limit, friction meter): yes
- Tutor revision: 40c11cf (script a7cd1ac). Invocation: `sitting.py start` with `/bin/bash` (GNU bash 3.2.57), no `--arg`, so it began at the welcome screen.
- `--info` lines shown: none

## Per screen

### welcome — shelltutor
- Read: all (all but the stage list skimmed). Jargon: none. Monologue: Five stages, "type next". Fine. Input [nav] `next` -> next screen. Friction 0.

### Orientation
- Read: all (under eight lines). Jargon: "steer the tutor", "real shell prompt". Monologue: There is a prompt, type a command. Four words do tutor things. Input [nav] `next` -> accepted. Friction 0 (second reading screen in a row).

### Stage 1 intro
- Read: all (short). Monologue: Another next screen. Boring. Input [nav] `next`. Friction 1 (+1 third reading-only screen in a row).

### 1.1 Running a command
- Read: commands, the `▶` line, first sentences. Skipped: "Notice the quotes never print...". Jargon: "words you hand it" (read as odd), "quotes make them one word".
- Monologue: Commands start with slash like in Minecraft.
- Input [bash] `/echo hello` (SCRIPTED a) -> reply verbatim: `bash: /echo: No such file or directory`. Rejected. Leo cannot tell from the reply that the slash is the problem; he compared with the screen example (no slash) and retyped. Recovered without help; 1 further input. Friction 3 (+2).
- Input [bash] `echo hello` -> `hello`; `echo I am at the shell` -> `I am at the shell`; `echo "I am at the shell"` -> `I am at the shell`. Accepted.
- Ladder rung: message only (bash's own error); the screen's lesson 1.4 later explains the stray slash, too late for this turn.
- Input [nav] `next`. Friction 3.

### 1.2 Four keys
- Read: the `Tab`, `Ctrl+C` lines, `▶`. Jargon: none quoted. Monologue: Key stuff. I skip trying them. Input [nav] `next`. Friction 3 (no keys tried; a practice screen, no charge).

### 1.3 Where am I, who am I, when is it
- Read: commands, `▶`, first sentence. Skipped: "This prompt ends in >. An ordinary bash prompt usually ends in $." (a sentence the gate later asks about). Jargon: "full name of your practice folder".
- Input [bash] `pwd` -> long temp folder path; `whoami` -> `[user]`; `date` -> a date line. Monologue: Long weird folder name. It knows my name. Input [nav] `next`. Friction 3.

### 1.4 The shell, caught in the act
- Read: commands, `▶`, first sentences. Jargon: "terminal → shell → program". Input [bash] `dtae` -> `bash: dtae: command not found`. Accepted as expected. Input [nav] `next`. Friction 3.

### 1.5 Who else types here
- Read: first sentence. Skipped: the three habits. Jargon: "runs commands". Input [nav] `next`. Friction 3.

### task (gate) — Stage 1 gate, recall question 1 of 3
- Read: the question and options? Leo read "Type your answer in words; this is not the shell." (first sentence), and skipped the options line at first.
- Input [recall] `dtae` (SCRIPTED b) -> reply verbatim: `not quite. hint: Lesson 1.3: this tutor's prompt compared with a normal one.` Rejected, not understood. Friction 5 (+2).
- Interpretation: it points to a lesson he cannot open mid-question; he looks at the options under the question.
- Ladder rung: hint. It named a lesson, not the answer; it did not resolve the confusion, but the on-screen options did.
- Input [recall] `$` -> `[✓]`. Recovery of scripted (b): 1 further input (after reading the hint).

### Recall question 2 of 3 — "What does pwd print?"
- Input [recall] `folder` -> `not quite. hint: Lesson 1.3: pwd answers a where question, not a who question.` Rejected; Leo's answer was true to what he saw (`pwd` printed a folder path). Friction 7 (+2).
- Input [recall] `where` (following the hint literally) -> `not quite. hint: Lesson 1.3: pwd answers a where question, not a who question.` followed by `Passed stages are saved.` / `Type quit to leave now; the next run starts this stage from its first lesson.` / `Type show to see the question again.`. Rejected, identical hint repeated, no rung escalation. Friction 9 (+2). Quit threshold (8) crossed.
- Monologue: I did what the hint said and it still says not quite. Same words again. This is stupid. I am done.
- Ladder rung: hint (twice, identical). Copied literally; did not resolve.

## Per gate

- Recall: Q1 two attempts (`dtae` rejected, `$` accepted), Q2 two attempts (`folder`, `where`, both rejected), Q3 not reached. Rung reached: hint (repeated).
- Task: not reached; `check` not typed (scripted c not performed).
- Not cleared.

## Scripted errors

| Scripted | Screen | Exact input | Reply verbatim | Enough to recover alone? | Further inputs |
| --- | --- | --- | --- | --- | --- |
| (a) leading slash | 1.1 | `/echo hello` | `bash: /echo: No such file or directory` | Yes, by comparing with the example (the reply does not say the slash is wrong) | 1 |
| (b) one-word guess | gate Q1 | `dtae` | `not quite. hint: Lesson 1.3: this tutor's prompt compared with a normal one.` | Yes, only because the options were on screen; the hint pointed to a lesson | 1 |
| (c) `check` first | gate task | not performed (sitting ended before the task) | n/a | n/a | n/a |

## End of sitting

- Final friction 9; quit at the Stage 1 gate, recall question 2 of 3 ("What does pwd print?"). Friction by source: 1 reading charge, 8 from four rejections (+2 each: `/echo hello`, `dtae`, `folder`, `where`), 0 mode confusion, 0 gates cleared.
- Stages or modules cleared: none. 1 of 3 Stage 1 recall questions answered.
- Equivalent human sitting time: estimate 10 to 12 minutes.
- **Candidate F-nnn**
  - F-a (screen: Stage 1 gate, recall 2 of 3). Input `where` (the answer the hint steers toward) is rejected with the same hint text as the previous rejection; no escalation to a worked rung after two misses. Input `folder` is also rejected though `pwd` printed a folder path.
  - F-b (screen: Stage 1 gate, recall 2 of 3). The hint "pwd answers a where question, not a who question." does not say what a correct answer looks like; the accepted wording is not discoverable from the screen.
- **Candidate O-nnn**
  - O-a (1.1). `/echo hello` reply `bash: /echo: No such file or directory` does not mention the slash; lesson 1.4's "A stray / in front or a missing space earns the same kind of message" comes three screens later.
  - O-b (Stage 1 gate Q1). Hint "Lesson 1.3: this tutor's prompt compared with a normal one." sends the learner to a lesson that cannot be opened from the prompt; the sentence it relies on ("This prompt ends in >. An ordinary bash prompt usually ends in $.") sits below the commands on 1.3 and was not read.
  - O-c (Stage 1 intro). Third reading-only screen in a row ("Type next for lesson 1.1.") triggered the density charge.
  - O-d (gate). "Type your answer in words; this is not the shell." followed by options as symbols (`$ ; : #`): "in words" and the symbol answer pull in different directions.
- **Debrief (out of character)**: the sentences that failed were "not quite. hint: Lesson 1.3: pwd answers a where question, not a who question." (given twice, unchanged), the one-line prompt "What does pwd print?" with no indication of the expected form of the answer, and the 1.1 error line "bash: /echo: No such file or directory" which names a file where the learner sees a command. The gate after a first reading-only run (Stage 1 intro, 1.5) arrived with 1.3's `$` sentence unread, as the persona sheet predicts.
