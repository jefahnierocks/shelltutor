---
title: WP-15 — Screen chrome (panel, header, footer bar, feedback checklist, ASCII path)
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-b, chrome, rendering, c-007, a3]
priority: high
---

# WP-15 — Screen chrome

**Governing text**: `docs/direction-decisions-2026-11.md` amendment A3
(A3.1–A3.8) and A2.6. **Tier**: core standard. **Depends on**: the Phase A
summary at three sittings. **Landing order**: first of Phase B, so every
later screen is authored and evidenced against the final chrome once.
**Rendering only**: no lesson-body text changes except the welcome's
authority sentence (A3.8, Q7 default). **Touches `shelltutor`**: yes.

## Goal

Make every tutor screen a panel between two rules with a header that shows
position and a footer that shows the verbs, so terminal → shell → program
is visible on every screen; render gate feedback as a checklist; give the
plain path ASCII glyphs.

## Read first

- A3 in full; `docs/design-description.md` §4.2 (cue catalogue), §1.11.
- `shelltutor`: colour roles (`88-103`), `practice()` footer and rcfile
  footer print (`370-378`, `429`), `show_screen` (`444-448`), `lesson()`
  (`453-457`), `gate_require_history` (`530-548`), the gate failure
  messages (`890-898`, `1123-1129`, `1333-1344`, `1605-1616`,
  `1899-1906`, `1948-1954`), `welcome` (`583-601`), the vertical-budget
  comment (`576-580`).
- Harness: `scripts/sim/driver.py` (screen-height segment, ANSI strip),
  `sentinels.py` (`ALMOST`), `run.py` (`ALMOST_TEXT` oracle).

## Change 1 — Roles and glyphs (A3.6, A3.7)

Replace the role block with the A3.6 table (`H1=1;97`, `SUB=36`,
`CMD=92`, `KEY=95`, `DIR=94`, `EM=91`, `INSTR=93`, `DIM=90`, `OK=92`,
`Q=96`, new `RULE=90`). Add glyph variables set in the same `if`:

| Variable | UTF-8 | ASCII |
| --- | --- | --- |
| `G_PLAY` | `▶` | `>` |
| `G_OK` | `✓` | `ok` |
| `G_DONE` `G_CUR` `G_TODO` | `●` `◉` `○` | `#` `*` `-` |
| `G_HINT` | `▸` | `>` |
| `G_BACK` | `◀` | `<` |
| `G_RULE` `G_VBAR` `G_BAR` | `─` `│` `┃` | `-` `|` `|` |
| corners and tees | `├ └ ╭ ╮ ╰ ╯ ┌ ┐ ┘` | `+` |

ASCII is selected by the existing plain-text condition (`NO_COLOR` set or
stdout not a TTY) **or** `SHELLTUTOR_ASCII=1`; never by locale (A3.7).
Every heredoc that today writes `▶` or `✓` literally uses `${G_PLAY}` and
`${G_OK}` instead (mechanical; the sentinels are unchanged on the harness
path because it runs with a pty and colours on). Document `SHELLTUTOR_ASCII`
in C-004.

## Change 2 — Panel (A3.1, A3.2)

- `panel_header` prints one 80-column row:
  `─ shelltutor ─ Stage N · <title> ─…─ ●◉○○○  N.k ─` (name INSTR, title
  DIM, rule RULE, dots OK/INSTR/DIM). Position comes from two globals set
  by the runners before each screen: `PANEL_STAGE` (1–5) and `PANEL_POS`
  (`1.1`, `task`, or empty on the cleared screen, where the dots show no
  current stage). Dots: stages below `read_progress` are `●`. Build
  repeated rules with a loop (no `tr` on multibyte, no `${s:0:n}`, which
  counts bytes under `LC_ALL=C`); fixed 80 columns, no `tput`.
- `show_screen` becomes: `clear`; `panel_header`; blank; `cat`; lower
  rule. The trailing `echo` is dropped.
- `practice()` prints the footer bar (Change 3) in place of today's
  footer string.
- Recall screens (gate header plus questions) get the header and lower
  rule; no footer follows because the question prompt does.
- **Budget**: the harness budget stays 22 rendered rows before the prompt.
  The chrome adds the header and the lower rule and drops the blank, so
  heredoc content is ≤ 19; author to ≤ 18 to keep one row of margin. Stage
  1's maximum is 18 today. Screens over budget (O-J) are not fixed here;
  they are measured again after this lands and handled where A2/WP-14 or
  a later package touches them. Update the comment at `576-580`.

## Change 3 — Footer bar (A3.3)

One DIM row, words in KEY, mode's verb first:

- lesson: `next ▸ go on   show ▸ this screen again   prev ▸ back   quit ▸ save and leave`
- gate: `check ▸ test your work   show ▸ the task again   quit ▸ save and leave`
- cleared (WP-11): `next ▸ Stage N+1   quit ▸ stop here, place saved   show ▸ this screen again`

`practice()` gains a third mode value `cleared`.

## Change 4 — Feedback checklist (A3.4)

Gate feedback keeps `skip_screen` and is rendered by three helpers, each
line prefixed `┃ ` in INSTR:

```
┃ ✓ whoami
┃ ○ pwd        not yet: not in your history
┃ ○ date       not yet: not in your history
┃ Run the ones marked ○, then type check again.
```

`gate_require_history` prints its result through them (`✓` for seen,
`○` plus `not yet: not in your history` for missing). The state-based
failures (stage 3 expected/seen, stage 4 count.txt, stage 5 phases,
stage 1 mismatched answers) are rewritten as one checklist each: a `✓`/`○`
line per predicate with `not yet: <what it sees>` on misses (for example
`○ done.txt contains hello   not yet: no done.txt in this folder`), then
the one-line instruction. `gate_escalate`'s hint and worked example follow
inside the same `┃` block. Wording is not contractual (C-006); the
checklist shape is recorded there.

Harness: the `ALMOST` sentinel (`Almost — you still need to`) is replaced
by `NOT_YET` = `not yet:`; the `second-try` oracle asserts it exactly once
per run (Stage 2 and Stage 4 each miss one item). `run.py`'s
`ALMOST_TEXT` follows.

## Change 5 — Welcome authority sentence (A3.8, Q7)

Insert after "the tutor never writes outside that folder." the sentence
"Commands you run yourself have your full authority: this is the real
thing, not a simulation." Keep the welcome within budget (it is 13 lines).
Closes operator question O-3.

## Change 6 — Records

- `docs/contracts.md`: C-004 gains `SHELLTUTOR_ASCII`; C-006 gains "gate
  feedback is a `┃` checklist (`✓`/`○`, `not yet:`)"; C-007 unchanged.
- `CONTRIBUTING.md` lesson-screen template (lands with WP-13 D; until
  then, the decisions §6 text): the chrome rows and the two-row cost.
- `docs/design-description.md` §4.2 cue table: add header dots, footer
  bar, `┃` checklist (a one-paragraph "Amended" note; the baseline stays
  descriptive).
- `STATUS.md` one line.

## Acceptance

1. `make verify` green; FF-008 clean (the rule-building loop uses no GNU
   tools); ShellCheck clean.
2. `careful-beginner --stage all` and `second-try` 2 and 4 green on Bash
   3.2 and 5.x and hosted Linux, with `NOT_YET` exactly once per
   `second-try` run; `compare.py` against `all-current` shows only chrome
   lines and the welcome sentence.
3. `NO_COLOR=1` and `SHELLTUTOR_ASCII=1` runs (scratch pty, reported)
   render ASCII glyphs and no escape codes; `./shelltutor -h` unchanged.
4. Screen-height table: no screen that fit before exceeds 22 rendered rows
   after; report the full table.
5. In a real 80×24 terminal (operator or scripted pty at 80×24), the
   header, panel, footer and prompt are all visible on Stage 1 screens.

## Commits

1. `feat(ui): colour roles per A3.6; glyph variables with ASCII fallback on the plain path and SHELLTUTOR_ASCII (A3.7)`
2. `feat(ui): panel header with stage dots, lower rule, key-hint footer bar (A3.1–A3.3)`
3. `feat(gate): feedback rendered as a ┃ checklist (A3.4); harness sentinel NOT_YET`
4. `feat(welcome): authority sentence on screen (A3.8, O-3)`
5. `docs(contracts,status): SHELLTUTOR_ASCII, feedback checklist shape; evidence`
