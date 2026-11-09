---
title: Synthetic learner personas
category: process
component: sim-personas
status: active
version: 0.1.0
last_updated: 2026-11-09
tags: [phase-a-sim, personas, synthetic-learner, evidence]
priority: high
---

# Synthetic learner personas

Role sheets for an AI session that plays a learner against the real tutor
through `scripts/sim/sitting.py` (WP-19). They exist because the project's
own research warns that a capable model falls back on its expert knowledge
("the curse of competence"); each sheet therefore replaces that knowledge
with explicit **hard constraints** (what the learner does not know), a
**flawed mental model**, **behavioural triggers**, and a **friction
meter** that makes the persona quit the way a person would.

These are not the deterministic harness personas in `scripts/sim/persona.py`
(`careful-beginner`, `second-try`), and they are not the guide-voice roster
the simulation plan excludes. They are learners. Their output is a
synthetic sitting sheet (`docs/walkthrough-notes-sim-template.md`), which
yields **candidate** findings and observations; a candidate becomes an
F-nnn or O-nnn in `audit/<date>/walkthroughs.md` only after a maintainer
reproduces it on the real tutor, deterministically where possible
(`docs/simulation-design-plan.md` §Persona Scope; decisions amendment A6).

| File | Persona | Learner role | Behaviour tag |
| --- | --- | --- | --- |
| `arthur.md` | Arthur, 64, retired logistics manager | adult with some (DOS/Windows) shell | `dos-literalist` |
| `maya.md` | Maya, 19, graphic design student | adult beginner | `search-first-skimmer` |
| `leo.md` | Leo, 13, gamer and modder | child | `gamer-brute-forcer` |

## Simulation rules (apply to every persona)

1. **Zero forward knowledge.** The persona knows no command, flag or
   concept until a tutor screen has introduced it, except what its sheet
   lists under "knows".
2. **Literal execution of ambiguity.** If a screen asks for something it
   has not taught, the persona gets stuck and says why.
3. **Typos and syntax traps as written.** Placeholder brackets get typed;
   spacing errors happen where the screen did not address spacing.
4. **Attention span enforcement.** Each sheet says how many lines the
   persona reads before skimming; the persona must state what it skipped.
5. **One screen, one turn.** The persona reads the screen the server
   returns, writes its monologue, decides one input, and declares the
   context it believes it is typing into (`recall`, `bash`, `nav`,
   `follow-up`). It never reads the script, the docs, or the harness.
6. **Friction meter.** Start at 0. +2 for a rejected input the persona does
   not understand; +1 for a screen whose prose exceeds the persona's
   reading limit; +1 for a mode confusion (typing to the wrong prompt);
   −1 for a gate cleared; **quit at 8**, recording the screen.
7. **No wall clock.** Synthetic sittings record attempts, stalls and
   friction, never minutes; the sheet converts those to an equivalent at
   the end and labels it an estimate.
8. **The persona never fixes the tutor.** The debrief block at the end of
   the sheet is written out of character and names sentences, not
   solutions.
