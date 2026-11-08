---
title: WP-13 — Module entry, module standard, harness support
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-c, modules, c-001, c-003, harness, screen-height]
priority: high
---

# WP-13 — Module entry, module standard, harness support

**Governing text**: `docs/direction-decisions-2026-11.md` §2 Phase C, §5,
§6, §7 and Q5. **Tier**: core standard for the script changes (they touch
`main`, C-001, C-003); module standard for everything a module brings.
**Depends on**: WP-10 (module gates use the recall ladder) and the first
module (WP-16 `shells`), since Phase C lands in the same commit series as
the first module. **Harness-only commits A and B may land during the
Phase A freeze.** **Touches `shelltutor`**: yes, after Phase B.

## Goal

Let a learner enter a stand-alone module by name, give module authors a
standard that costs less than the core's, and give the harness a way to
drive any module from a small table instead of a hand-written walk.

## Commit A — rendered screen height in the harness (Q5; harness only)

`scripts/sim/driver.py`: after each `clear` sequence in the OUT stream
(`ESC[H`, `ESC[2J`, or `ESC[3J` in any order) and before the next `PROMPT`,
count the lines of normalised output. Emit one `screen-height` event per
screen with the current `screen_id` and `{"lines": N, "budget": 20,
"over": N > 20}`. The practice footer line printed by the rcfile is part
of the count only if it precedes the prompt on the same screen; state in
the summary exactly what is counted. `summary.md` gains a "Screen heights"
table (screen id, lines, over-budget flag). **Informational only**: no TAP
change, no exit code change. The first run on the current script should
reproduce observation O-J (`audit/2026-11-08/findings.md`) within one
line per screen; report any difference and explain it. Two sentences in
`scripts/sim/README.md`.

## Commit B — module persona tables (harness only)

`persona.py`: `module_walk(name, lessons, gate)` builds a walk from a
table: wait for the module intro heading, `next`; for `k` in `1..lessons`
wait for the heading `"<name> <k> — "` (prefix match, no title text),
`next`; then the gate per a small gate spec (recall answers list; wait
`"<name> — task"`; task commands list; `check`); then wait
`"✓ <name> cleared."`. The table may carry an optional
`lesson_actions={k: [commands]}` typed at lesson `k`'s prompt, and an
optional `prompt_after={k: "text"}` asserting the prompt text seen after
that lesson's `next` (the `env` module uses both to observe the prompt
reverting, WP-17 [decision] 6). Sentinels are
derived from the convention below, so `sentinels.py` gains no per-module
entries. `run.py`: `--module <name>` is accepted when `--stage` is absent;
`--stage` and `--module` together exit 2. Until a module exists, a unit
check with a fake transcript proves the expansion; no bundle.

## Commit C — module entry in the script (after Phase B, with WP-16)

- `MODULES="shells env"` next to `TOTAL_STAGES`; `main`'s `case` gains
  `shells|env) preflight || exit 1; setup_sandbox; run_module "$1"; exit 0 ;;`
  before the `*)` branch. An unknown word keeps the existing bad-argument
  path (C-001).
- `usage()` gains, after the Stages list:

      Modules (stand alone; nothing saved):
        shells   What a shell is; other shells; your login shell
        env      Variables, PATH, the prompt, and where they live for real

- `setup_module_dir NAME` mirrors `setup_stage_dir`: `$SANDBOX/<name>/`,
  seeded on entry, self-healing (C-003).
- A module block follows the stage pattern: `module_<name>_intro`,
  `module_<name>_lesson_k`, verifiers, `module_<name>_gate`,
  `run_module_<name>`, ending on a cleared screen (`✓ <name> cleared.` plus
  the same recap style as WP-11, then `▶ Type quit to leave, or next to
  return to the start of this module.`). Modules call `save_progress`
  never and write only under `$SANDBOX/<name>/`.
- **Heading convention** (binding for modules; the harness depends on it):
  intro heading `MODULE — <name>: <title>`; lesson headings
  `<name> <k> — <title>`; gate heading `<name> — gate`; task-screen
  heading `<name> — task`; cleared line `✓ <name> cleared.`. The gate
  opening screen has no `▶` line (the first question follows at once), as
  in the stages; every other screen ends in one. "Three to five screens"
  in the module standard counts lessons only.

## Commit D — documents (with Commit C)

- `docs/contracts.md`: C-001 gains the module argument and the fixed
  list; C-003 gains `$SANDBOX/<module>/`; a one-line note that modules
  never touch `.progress`.
- `CONTRIBUTING.md`: new §Module standard (the text of decisions §5) and
  the lesson-screen template (decisions §6), plus the heading convention
  above and the sentence "module screens are height-checked by the
  harness's `screen-height` events; a module author counts by hand only
  when the harness is unavailable".
- `AGENTS.md` §Identity: "a single-file interactive tutor for the Unix
  shell" stays; the vimtutor sentence becomes "a shell course whose
  five-stage core hands off to `vimtutor`, with stand-alone modules",
  and the two-tier evidence rule (decisions §0) is added under
  §Validation.
- `README.md` §shelltutor and §Non-Goals: the same reframing; non-goals
  gain users and groups, networking, multi-shell practice, editor
  internals beyond the concepts of buffer, mode, pane and session.
- `docs/simulation-design-plan.md` §Pedagogy And UX: one sentence that
  children are named learners and the tone rules are unchanged (D5).

## Acceptance

- A, B: `make check lint smoke`, `make self-test` green; Python 3.9
  syntax; a scratch `--stage all` run shows the "Screen heights" table and
  O-J is reproduced.
- C, D: `make verify` green; `./shelltutor -h` lists the modules;
  `./shelltutor bogus` exits 1 as today; `./shelltutor shells` runs to the
  cleared screen with `.progress` unchanged and only `$SANDBOX/shells/`
  written; the harness drives it from the table with a green TAP on macOS
  and hosted Linux; `summary.md` and `result.tap` committed (module
  standard item 6).

## Commits

- A `feat(sim): record rendered screen height per screen (informational; Q5)`
- B `feat(sim): module persona tables and --module; heading-convention sentinels`
- C `feat(modules): module entry by name, module sandbox folders, module block pattern (C-001, C-003)`
- D `docs(modules): module standard, lesson-screen template, identity and non-goals reframed`
