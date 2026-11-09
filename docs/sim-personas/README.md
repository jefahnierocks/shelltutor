---
title: Synthetic learner personas
category: process
component: sim-personas
status: active
version: 0.2.0
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
   reading limit (the charge follows each persona's own Reading section);
   +1 for a mode confusion (typing to the wrong prompt);
   −1 for a gate cleared; **quit at 8**, recording the screen.
7. **No wall clock.** Synthetic sittings record attempts, stalls and
   friction, never minutes; the sheet converts those to an equivalent at
   the end and labels it an estimate.
8. **The persona never fixes the tutor.** The debrief block at the end of
   the sheet is written out of character and names sentences, not
   solutions.

## Calibration history

The sheets are tuned from evidence, and each change is dated so a round's
numbers are read against the version that produced them. A sheet records its
own version in the sitting block ("Persona sheet version").

- **v0.1, rounds 1 and 2** (`audit/2026-11-09/walkthroughs.md`). Round 1 ended
  at friction 8 (Leo), 9 (Maya) and 9 (Arthur), all at the Stage 1 gate. Round 2
  friction by source:

  | Sheet | Final | Reading-limit charges | Rejections (+2 each) | Other |
  | --- | ---: | ---: | ---: | --- |
  | leo-2 | 8 | 1 | 6 | 1 mode confusion |
  | maya-2 | 9 | 7 | 2 | 0 |
  | arthur-2 | 8 | 1 | 8 | -1 gate cleared |

- **v0.2** (amendment A8, simulation calibration only; no tutor change).
  Maya: the density charge applies only when a skipped line later causes a
  rejection or wrong turn, because seven of her nine round-2 points were
  length charges that measured her four-line limit, not a tutor defect. Leo:
  he also reads the first sentence of each paragraph, because skipping all
  prose made him miss the one sentence ("this is not the shell") that
  separated recall from the shell. Arthur stayed at v0.1 for rounds 1 to 3.
  Round 3 states both changes so the comparison with rounds 1 and 2 is
  explicit.

- **Round 3** (`audit/2026-11-09/walkthroughs.md`, WP-21 tutor; Leo and Maya on
  v0.2, Arthur on v0.1). Friction by source:

  | Sheet (persona version) | Final | Reading charges | Rejections (+2 each) | Mode confusion | Gates cleared |
  | --- | ---: | ---: | ---: | ---: | ---: |
  | leo-3 (v0.2) | 8 | 1 | 8 | 0 | -1 |
  | maya-3 (v0.2) | 8 | 1 | 8 | 2 | -3 (unfloored) |
  | arthur-3 (v0.1) | 9 | 8 | 2 | 0 | -1 |

- **Arthur v0.2** (amendment A9, simulation calibration only). The density
  charge applies only when a long screen's content later causes a rejection or
  wrong turn, because eight of Arthur's nine round-3 points came from the
  14-line limit before Stage 2 began. Round 4 states the change.

## Running a sitting

A sitting is run by a **separate Claude Code session** (the persona
session), not by the session that maintains the repository. The persona
session is given exactly four things and nothing else:

1. one persona sheet from this directory;
2. the eight simulation rules above;
3. `docs/walkthrough-notes-sim-template.md`, which it fills in;
4. the client commands of `scripts/sim/sitting.py` (below).

It must **not** read `shelltutor`, anything under `docs/` other than the
three items above, `audit/`, or the harness source. Everything it knows
about the tutor comes from the screens the server returns. The maintainer
who launches the session starts the sitting and states, in the session's
first instruction, the tutor revision, the Bash to use and the entry
(`--arg`), which the session copies into the sheet's "Sitting" block.

### Commands

```
python3 scripts/sim/sitting.py start [--bash /bin/bash] [--arg N|module] --out DIR --persona NAME
python3 scripts/sim/sitting.py screen --out DIR
python3 scripts/sim/sitting.py send --out DIR "<text>"        # types text and Enter
python3 scripts/sim/sitting.py raw  --out DIR "<escape>"      # no Enter: \t  \x0c  \x1b  \x1b[A
python3 scripts/sim/sitting.py note --out DIR <context> "<monologue>"
python3 scripts/sim/sitting.py stop --out DIR
```

**Turn cap: 160. One turn = one `send` or one `raw`.** Stop at the cap at the end
of the current screen; record the count in the sheet's Sitting block.

`--out` is the sitting directory; use one fresh directory per sitting
(`start` refuses a directory that already holds a sitting or a bundle).
`screen` and `send` return the text since the last clear sequence, with
colour codes removed and the pending prompt line marked `[prompt] ...`.
`send` waits until the tutor has been quiet for 0.4 s (10 s at most).
A reply ending in `[exited N]` means the tutor has ended; run `stop`.

### Per turn

1. `screen` (or the reply of the previous `send`/`raw`) is the only thing
   the persona sees. It applies the sheet's reading limit and says what it
   skipped.
2. Write the sheet's per-screen block: read / skimmed, jargon quoted
   verbatim, monologue in character (two to six lines).
3. Decide **one** input and the context the persona believes it is typing
   into: `recall` (a question prompt), `bash` (the `shelltutor>` prompt),
   `nav` (a navigation word such as `next`, `show`, `prev`, `quit`) or
   `follow-up` (a question after a task).
4. `note <context> "<monologue>"` records the monologue and the declared
   context; it sends nothing. The next `send` or `raw` is tagged with that
   context in `events.jsonl`.
5. `send` or `raw` the input, then record the tutor's response, the ladder
   rung shown and the friction total in the block.

Update the friction meter after every turn (rule 6). The persona stops at
8, on a cleared module or the finale, or when the tutor exits. Any one of
those ends the sitting: run `stop`.

### After `stop`

1. Finish the sheet: the per-gate block, the end-of-sitting block (final
   friction, what was cleared, the human-time **estimate**, candidate
   F-nnn and O-nnn with screen ids and exact inputs, the out-of-character
   debrief).
2. The login name appears on screen (`whoami`, paths). Write it as
   `[user]` in the sheet; the bundle's own files are already redacted.
3. Save the sheet as `audit/<date>/sim-sittings/<persona>-<n>.md` and copy
   `bundle/summary.md` and `bundle/result.tap` beside it as
   `<persona>-<n>.summary.md` and `<persona>-<n>.result.tap`. The raw
   `terminal.jsonl` and `events.jsonl` stay out of git unless a maintainer
   asks for them.
4. Report the candidates in the session's final message. **None is
   promoted.** A maintainer reads each one, reproduces it on the real tutor
   (by hand, or as a `second-try`-style persona step), and only then records
   an F-nnn or O-nnn in `audit/<date>/walkthroughs.md`, citing the sheet.
