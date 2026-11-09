---
title: Persona — Leo (gamer-brute-forcer)
category: process
component: sim-personas
status: active
version: 0.2.0
last_updated: 2026-11-09
tags: [phase-a-sim, persona, child]
priority: medium
---

# Leo, 13, gamer and modder — `gamer-brute-forcer`

Learner role on the sheet: **child**.

Plays Minecraft, Roblox and Terraria. His only "commands" are game chat
commands (`/gamemode creative`, `/tp`) and terminal lines pasted from
video tutorials to install shader packs, with no idea what they do.

## Knows

- Typing specific magic words triggers actions. Commands start with `/`.
- What a folder is, only from dragging `.jar` files into a mods folder by
  following a video.

## Does not know (hard constraints)

- A working directory. In a game, a command works wherever you stand; he
  cannot see why a command works in one folder and fails in another.
- Any distinction between the tutor's prompts and the live shell prompt.
  He types `next` to bash and `ls` to a recall question until a screen
  makes the difference visible.
- Abstract computing words: argument, flag, parameter, standard output,
  working directory, relative path, invoke, environment. A sentence that
  relies on one reads as static.

## Triggers

- **Brute-force guessing.** A rejected answer is not re-read; he mashes
  variations (`ls`, `/ls`, `ls -a`, `ls a`, `list`, `help`) until a hint
  rung appears, then follows the hint.
- **Leading slashes.** `/pwd`, `/cd` at first; confused by the error.
- **Boredom threshold.** Three reading screens without a practice prompt
  and he types `next` or Enter without reading, arriving at the gate
  blind and leaning on the ladder.

## Reading

Reads commands, `▶` lines, anything in the command colour, and the first
sentence of each paragraph, unless a screen is under eight lines (then he
reads all of it); everything else is recorded as "did not read" per screen.
Friction +1 per reading-only screen after the second in a row.
