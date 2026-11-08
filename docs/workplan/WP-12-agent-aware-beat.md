---
title: WP-12 — Agent-aware beat: read-only lesson 1.5 and two sentences
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-b, stage1, agent-aware, d3]
priority: medium
---

# WP-12 — Agent-aware beat: read-only lesson 1.5 and two sentences

**Governing text**: `docs/direction-decisions-2026-11.md` D3 and amendment
A1.5. **Tier**: core standard. **Depends on**: the Phase A summary
(script freeze, A1.9). **Landing order**: second, after WP-11. **Touches
`shelltutor`**: yes (Stage 1 array and three heredocs).

## Goal

Extend lesson 1.4's terminal → shell → program model to agents, as one
read-only screen; add one sentence each to 3.3 (`rm`) and 4.3 (`>`) saying
why a line is read before anyone runs it. No commands, no gate change, no
integration (D3).

## Read first

- `docs/direction-decisions-2026-11.md` D3, A1.5.
- `shelltutor`: `stage1_lesson_4` (`710-732`), `run_stage1`'s array
  (`912`), `stage3_lesson_3` (`1235-1259`), `stage4_lesson_3`
  (`1466-1499`), the vertical-budget convention (`576-580`).
- `audit/2026-11-08/findings.md` observation O-J: 3.3 is 21 content lines
  and 4.3 is 30, both already over the 20-line budget. **The two sentences
  are added net-zero**: each replaces an existing line, so neither screen
  grows.
- `scripts/sim/sentinels.py` (Stage 1 entries), `persona.py`
  (`careful_beginner_stage1`), `recorder.known_rough_edges(1)`,
  `audit/2026-11-08/stage1-density-followup.md`.

## Change 1 — Lesson 1.5 (read-only)

Append `stage1_lesson_5` to `run_stage1`'s array after `stage1_lesson_4`.
Lesson 1.4's footer becomes `▶ Type next.`; 1.5 takes the "to take Stage
1's gate" footer. `stage1_intro` says "Five short lessons". Copy
(17 content lines, under budget):

    ${H1}1.5 — who else types here${RST}

    Everything you typed went terminal → shell → program. There is no
    other way in: anything that runs a command on this machine goes
    through a shell the same way.

    An AI assistant that "runs commands" for you is no exception. It
    types a line into a shell; the shell finds the program; the program
    runs. The line it typed can be read exactly as you read your own.

    So the habits in this course count twice:
      ${SUB}read the line${RST} before anyone presses Enter — you, or a helper
      ${SUB}know the folder${RST} it will run in
      ${SUB}read the output${RST} when it comes back, instead of skimming it

    You are learning the one language every helper on this machine
    has to speak.

    ${INSTR}▶ Type ${CMD}next${INSTR} to take Stage 1's gate.${RST}

Tone check against `docs/simulation-design-plan.md` §Pedagogy And UX: no
anthropomorphism beyond "helper", no fiction, no praise.

## Change 2 — Two sentences, net zero lines

- 3.3 (`shelltutor:1250-1251`): the two-line sentence "There is no Trash to
  recover from. There is no undo. Type carefully and look before you press
  Enter." becomes "There is no Trash and no undo. Look before you press
  Enter — you, or an assistant typing for you." Same two lines.
- 4.3 (`shelltutor:1470-1471`): "A pipe sends output to another program. A
  redirect sends it to a file." becomes "A pipe sends output to another
  program. A redirect sends it to a file, and > replaces that file without
  asking, whoever typed the line." Same two lines (reflow within them).

Headings are unchanged, so no sentinel changes for 3.3 and 4.3.

## Change 3 — Harness and records

- `sentinels.py`: `LESSON_1_5` = `1.5 — who else types here`.
- `persona.py` Stage 1 walk: after lesson 1.4's `next`, wait `LESSON_1_5`,
  send `next`. Both personas.
- `audit/2026-11-08/stage1-density-followup.md`: one row for 1.5
  (concepts: agent → shell → program; actions: 0, read; recommendation:
  keep with watch — two read-only screens, 1.4 and 1.5, now precede the
  gate; A1.5 names this as a watch item for the second walkthrough round).
- `ROADMAP.md` Phase 3 Amendments: one dated line (Stage 1 has five
  lessons; 1.5 read-only).
- `STATUS.md` one line.

## Acceptance

1. `make verify`, `make self-test` green; FF-004 clean (no new
   platform-specific text).
2. Stage 1 screen heights all at or under 20 (measure with the awk
   one-liner used for O-J); 3.3 and 4.3 heights unchanged (21, 30).
3. `careful-beginner --stage 1` and `--stage all` green on Bash 3.2 and
   5.x; `second-try` unchanged.
4. `./shelltutor -h` still lists five stages; nothing outside the three
   heredocs, the intro line and the array changed in `shelltutor`.

## Commits

1. `feat(stage1): lesson 1.5 — who else types here (agent → shell → program), read-only (D3)`
2. `feat(lessons): read the line before anyone runs it — one sentence each in 3.3 and 4.3, net zero lines`
3. `chore(sim): Stage 1 sentinel and persona for lesson 1.5; density follow-up row; ROADMAP amendment; STATUS`
