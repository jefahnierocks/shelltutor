---
title: Design brief for an outside consultant — shelltutor screens (November 2026)
category: design
component: screens
status: active
version: 0.1.0
last_updated: 2026-11-09
tags: [design, chrome, screens, consultant, brief]
priority: high
---

# shelltutor — design brief for an outside consultant

This brief describes what exists today, the constraints that any proposal
must respect, three changes the operator has already asked for, and the
open questions we would like a view on. It is self-contained; the
consultant does not need the repository.

## 1. What shelltutor is

A single-file Bash program that teaches a complete beginner to work in a
Unix shell. It runs in the learner's own terminal, in a real Bash, in a
sandbox folder it never leaves. Five mastery-gated stages (Where am I?
Paths; Files; Commands and streams; Ready for vimtutor) and stand-alone
modules (What a shell is; Variables and PATH). Each stage is three to five
one-screen lessons, then a gate: three recall questions answered in words
and one practical task the script verifies. Unlimited retries, no praise,
no scores, no timer. The learner leaves by typing `quit`; progress is
saved per stage.

Audience: a child of about ten with a patient adult nearby; an adult who
has only ever used a desktop; a long-ago DOS user. Design intent: the
tutor is a quiet instructor sitting beside a real shell, not a game and
not a web app. Everything the learner types is real and runs in Bash.

The course began as a vimtutor preparation course. That is no longer its
identity: it is a shell course whose fifth stage hands off to vimtutor.
The welcome still says "a vimtutor prerequisite course" and the operator
wants that gone (section 4).

## 2. Hard constraints (not up for redesign)

- **Medium**: a text terminal, 80 columns by 24 rows assumed; nothing
  probes the real size. Wider terminals simply show a shorter rule.
- **Output**: ANSI escape codes only. Sixteen-colour SGR codes; the
  learner's terminal theme picks the actual colours. No true colour, no
  images, no mouse, no cursor positioning, no alternate screen. Each new
  screen clears the terminal and redraws.
- **Characters**: UTF-8 box drawing and a small glyph set
  (`▶ ✓ ● ◉ ○ ▸ ─ │ ┃ ├ └`) with an ASCII fallback (`> ok # * - > - | | |`)
  when colour is off (`NO_COLOR`, non-TTY) or when asked
  (`SHELLTUTOR_ASCII=1`). Every design must read in the ASCII form too.
- **Height budget**: a lesson screen is at most 22 rendered rows including
  the chrome, so the shell prompt and the learner's own output fit under
  it on a 24-row terminal. Lesson bodies are at most 18 source lines.
- **Runtime**: Bash 3.2 (the macOS system Bash from 2007) and POSIX
  tools only. No Python, no curses, no external renderer. This rules out
  anything that needs a layout engine.
- **Tone rules**: no praise, no scores, no streaks, no emoji, no timers.
  Progress indicators show position, never performance.
- **Transfer**: what the learner sees under the panel is an ordinary Bash
  prompt. Nothing may make the real shell look unlike a real shell; the
  skill has to carry to a plain terminal later.

## 3. What a screen looks like today

Rows, top to bottom: header rule; blank; title; body; the `▶` instruction
line; lower rule; key-hint footer; then the real shell prompt.

Header rule (left: product name; middle: stage and title; right: stage
dots and the position):

```
─ shelltutor ─ Stage 1 · Where am I? ────────────────────────────── ◉○○○○  1.1 ─
```

A lesson (1.1), as rendered, colour removed:

```
─ shelltutor ─ Stage 1 · Where am I? ────────────────────────────── ◉○○○○  1.1 ─

1.1 — running commands

At the prompt below, type this and press Enter:

  echo hello

You'll see hello printed, then the prompt comes back. Now try:

  echo I am at the shell      # spaces separate words
  echo "I am at the shell"    # quotes group them into one
If bash says command not found or No such file, you mistyped: a stray
/ in front, or a missing space. Type it again.

echo just repeats its words back. It is the simplest command
there is, and its shape is the shape of every command you'll meet:
a name, then the words you hand it.

▶ Try all three, then type next.
────────────────────────────────────────────────────────────────────────────────
next ▸ go on   show ▸ this screen again   prev ▸ back   quit ▸ save and leave
shelltutor> 
```

The gate screen and a recall question. Tutor speech that must stay
visible while the learner types is marked with a `┃` bar at column one
instead of clearing the screen:

```
─ shelltutor ─ Stage 1 · Where am I? ───────────────────────────── ◉○○○○  task ─

STAGE 1 — GATE

Recall (three questions, all three must be correct).
First, three questions. Type your answer in words; this is not the shell.

Then a practical task: run a few commands and tell me what
they printed. The script verifies your answers.

Unlimited retries. No skip.
────────────────────────────────────────────────────────────────────────────────
┃ Q1: In a normal bash window (not this tutor), which character usually ends the prompt? ($, ;, :, or #)
┃ answer in words: 
```

Gate feedback after `check` is a checklist in the same bar:

```
┃ ○ folder exists  not yet: no practice folder in this stage's folder
┃ ○ cd into it     not yet: make the folder first, then cd into it
┃ Run the ones marked ○, then type check again.
```

A wrong recall answer gets `not quite. try again.` and a one-line hint
pointing at the lesson; from the second miss, three navigation facts
(progress is saved; `quit` leaves; `show` repeats the question).

Colour roles (ANSI code → use): bold white = screen title; cyan = a
concept being named; bright green = something you can type; bright
magenta = a key or chord and the navigation words; bright blue = a path;
bright red = a warning; bright yellow = the `▶` line, the product name
and the `┃` bar; grey = asides, footer hints, unreached dots; green =
`✓` and filled dots; bright cyan = a recall question; grey = rules.

Other screens of the same family: a welcome, a one-screen orientation
that introduces the five words, a per-stage intro, a stage-cleared screen
("✓ Stage N cleared", the commands you can now use, "Next: Stage N+1"),
and a finale.

## 4. Changes the operator has already asked for

1. **Identity line.** The welcome's "SHELLTUTOR — a vimtutor prerequisite
   course" should say what the tool is now: working in a Unix shell, or
   words to that effect. The help text and the stage-5 title carry the
   same phrase and should follow.
2. **Breathing room above the prompt.** The shell prompt sits directly
   under the key-hint footer and looks cramped. One blank row between the
   footer and the prompt is the obvious fix; the budget allows it on most
   screens, and the few at 22 rows would lose an internal blank instead.
3. **Modern polish.** The operator wants the screens to feel more modern,
   beautiful and clear, within the constraints of section 2. Candidates we
   can see ourselves: typographic hierarchy inside the body (titles,
   commands, asides are visually flat apart from colour); consistent
   indentation of typeable lines; the header's right-hand cluster; the
   footer's density; whether the `┃` speech bar and the `▶` line should
   share one visual language; whether the panel should have a left margin.
   We would like the consultant's read on where the biggest gains are.

## 5. Open questions for the consultant

1. **Hierarchy without fonts.** With one monospace face and sixteen
   colours, how should title, instruction, typeable command, aside and
   warning be told apart so a ten-year-old can scan a screen in a few
   seconds? Are we over-using colour where spacing or case would do?
2. **The `▶` line.** It is the one thing every screen asks the learner to
   do. Should it be the visually loudest element, and how, given no bold
   colour pairs beyond what ANSI gives?
3. **The header.** Product name, stage name, five position dots and a
   position code share one rule. Is that too much? Which could go, or move
   to the footer?
4. **Footer as key hints.** Four words with glosses on one line (`next ▸
   go on   show ▸ this screen again …`). Readable, or should it shrink to
   the words alone once the orientation has taught them?
5. **Tutor speech beside a live prompt.** The `┃` bar marks text the tutor
   prints while the real shell is active. Is a bar the right device, and
   should question prompts ("answer in words:") look more different from
   the shell prompt than they do?
6. **Gate checklist.** `✓` and `○` with a `not yet:` reason. Any better
   convention for "done / not done / what I see instead" in plain text?
7. **Density.** Lesson bodies run to 15–18 lines. Beginners in our
   simulated sittings skipped prose and read only commands. Where would
   you cut, and should every lesson have exactly one typeable block?
8. **ASCII fallback.** The plain form replaces glyphs with `> ok # * -`.
   Is there a better plain-text vocabulary that still reads as the same
   design?
9. **Cleared screen and finale.** Both are lists of commands. Is there a
   calmer, more memorable form for "you can now do these" that keeps the
   no-praise rule?
10. **Wide terminals.** Today the rule just gets shorter. Should the panel
    centre, cap at 80 columns, or stay left-aligned?

## 6. What we will do with the answers

Proposals come back as text or ASCII mock-ups at 80 columns (that is the
medium; a pixel mock-up would have to be translated). We implement the
agreed changes as one rendering-only package, then re-run the simulated
sittings to check nothing in the learning path moved.
