---
title: WP-25 — Screen chrome v2 (consultant response, rendering only)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, chrome, screens, rendering, a11]
priority: high
---

# WP-25 — Screen chrome v2

**Governing text**: `docs/design-consultant-response-2026-11.md` (the
consultant's answer to `docs/design-brief-consultant-2026-11.md`) as
adopted by amendment A11 in `docs/direction-decisions-2026-11.md`.
**Tier**: core standard (sentinels move; personas and oracles follow;
density rows; full bundles both Bash versions). **Touches `shelltutor`**:
yes, rendering only: chrome, footer, colour roles, glyph table, recall
prompt, checklist, welcome, cleared screen, finale layout, identity
strings, lesson title prefixes. **No lesson-body sentence changes** in
this package; the consultant's §5.2 body rewrite and the §3.7 skeleton
are WP-26 (content), scheduled after this lands.

## Decisions carried (A11; the consultant's five defaults all accepted)

1. Body palette: bold (SGR 1) replaces cyan/magenta for named concepts
   and keys; paths plain; grey asides; green typeable; yellow `▶`/`┃`;
   red on the word only. Footer words `1;90`.
2. Product name only on welcome, stage intro, cleared and finale headers.
3. Progressive footer: glosses in Stage 1 and on cleared screens; words
   only from Stage 2. Gate recall and task phases have their own forms.
4. Recall prompt `┃ ? `; "answer in words" said once in the gate intro.
5. `(gloss)` replaces `▸`; width-stable glyph pairs; `·`→`:`; `[✓]`/`[ ]`
   → `[x]`/`[ ]`; no tick in the cleared title.

## Changes

### C1. Skeleton and whitespace
- Footer moves ABOVE the lower rule; one blank row after the rule; the
  prompt follows. `show_screen` emits: header · blank · title · body · blank
  · `▶` line · blank · footer · rule · blank.
- The `▶` line always has one blank above and one below (collapse doubles).
- Budget: panel ≤ 19 rows (header through rule); the check in
  `scripts/` and the density rows move to this number. Lesson bodies that
  now exceed it (body > 12 rows) are NOT cut here: list them in the report
  for WP-26 and let them run to a hard cap of 21 panel rows meanwhile.

### C2. Header
`── Stage N · <title> ──…── ●◉○○○  N.k ──` (two-glyph rule ends); `gate` /
`task` in place of `N.k`; cleared screen shows dots only, no current dot;
product name only on welcome, stage intro, cleared, finale. Lesson titles
lose the `N.k — ` prefix (the header carries it).

### C3. Footer
`footer_bar MODE STAGE`: forms per the response §4. `(gloss)` not `▸`.

### C4. Colour roles
Add `BOLD='\033[1m'`; retire `SUB`, `KEY`, `DIR` from lesson bodies
(variables stay defined for modules until WP-26 sweeps them; report the
count left). Footer verbs `1;90`. Role table in `CONTRIBUTING.md` updated.

### C5. Glyph table
Pairs per response §4; `G_GLOSS_L='('` is literal in both forms; add
`G_DOT_SEP` (`·`/`:`), `G_BOX_OK='[✓]'`/`'[x]'`, `G_BOX_TODO='[ ]'`.

### C6. Recall block (response §5.4)
`┃ 1 of 3   <question wrapped at 76 under the bar>`; options on their own
bar row; input prompt `┃ ? `; misses print `┃ not quite. try again.` and,
from the second miss, `┃ not quite. hint: <hint>`; the three navigation
facts stay on the ladder as today (C-006 unchanged in substance). Hints
are reworded only where "Lesson N.k:" is now redundant? No: hints keep
their text and FF-010 anchor; the `hint:` label precedes them.

### C7. Gate checklist (response §5.5)
`┃ [✓] <item>` / `┃ [ ] <item>   seen: <observation>`; closing line
`┃ Finish the step marked [ ], then type check again.` Reasons are
observations, not instructions: rewrite each `not yet:` string
accordingly (list them in the report). The attempt-2 hint rung carries
the instruction.

### C8. Welcome (response §5.3)
Rounded box; row 1 `shelltutor` left, `working in a Unix shell` right;
the course map row of five dots and stage names under the box. The
sandbox path line is kept as one grey line under the map (the brief's
authority sentence stays, shortened as in the mock-up). Help text (`-h`)
first line and `--info` header: "shelltutor — working in a Unix shell";
the script's line-2 comment follows. Stage 5 title unchanged.

### C9. Cleared screen and finale (response §5.6, §3.9)
Capability first, command second, two-column; finale grouped by stage
plus the four-habit closing block (read before you run; predict; know
where you are; list before you remove).

### C10. Harness
`sentinels.py`: titles without prefix; WELCOME sentinel → the new row 1;
GATE feedback sentinel `[ ]`; recall prompt `? `; `not yet:` → `seen:`.
`persona.py`/`run.py`: second-try oracle asserts one `[ ]` line and
`hint:` ×1 at Stage 2 (facts ×1 unchanged). ASCII run (`SHELLTUTOR_ASCII=1`)
added to the committed evidence once per Bash version.

## Records
`docs/contracts.md` C-006 (recall rendering wording; substance unchanged),
C-005 if the ASCII variable's table is listed there; `CONTRIBUTING.md`
screen template and role table; `docs/design-description.md` chrome
section (one paragraph citing A11); density rows; `STATUS.md`.

## Acceptance
1. `make verify` green; FF-009..FF-011 unchanged in result.
2. careful-beginner `--stage all`, second-try 2 and 4, both modules, on
   3.2 and 5.x, UTF-8 and ASCII; row counts identical between the two forms
   on every screen (assert in the report).
3. Report lists: screens over the 19-row panel budget (for WP-26), the
   rewritten `seen:` strings, remaining `SUB`/`KEY`/`DIR` uses.

## Commits
1. `feat(chrome): footer above the rule; blank before the prompt; ▶ isolation; 19-row budget (A11)`
2. `feat(chrome): header without product name on lessons and gates; titles without N.k prefix`
3. `feat(chrome): progressive footer with (gloss); BOLD role; SUB/KEY/DIR out of lesson bodies`
4. `feat(chrome): width-stable glyph pairs; recall block with ? prompt; [✓]/[ ] checklist with seen:`
5. `feat(screens): welcome box and identity line; cleared and finale capability-first`
6. `chore(sim): sentinels, oracle, ASCII evidence; density rows; CONTRIBUTING; design note; STATUS`
