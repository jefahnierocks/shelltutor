---
title: WP-01 — Five-stage PTY harness (FF-006c, rung 1)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, simulation, pty, ff-006c, evidence]
priority: high
---

# WP-01 — Five-stage PTY harness (FF-006c, rung 1)

**Depends on**: nothing. **Blocks**: WP-02, WP-03, WP-04, WP-05, WP-06.
**Touches `shelltutor`**: no. **Operator gate**: none.

## Goal

Extend `scripts/sim/` so the `careful-beginner` persona drives every stage
of the tutor (stages 1 to 5 in one run, or any single stage) and produces
the same v1 evidence bundle per run. Commit the first five-stage baseline
of the *current* script so later work packages have a before-state to
compare against. This is the observe step: it must not fix anything it
finds.

## Read first

- `AGENTS.md`, `docs/workplan/README.md` (worker protocol, decisions
  D-02, D-03).
- `scripts/sim/README.md` and every file under `scripts/sim/`.
- `docs/simulation-design-plan.md` §Implementation Ladder, §Evidence
  Bundle, §Confusion Events.
- `docs/contracts.md` C-001 (argv), C-002 (exit codes), C-003 (sandbox
  layout).
- `audit/2026-11-07/findings.md` — F-010 and F-011 are expected to appear
  in this baseline as `error-signature` events. That is the point.
- The lesson and gate heredocs in `shelltutor` for stages 2 to 5 (search
  for `stage2_intro` through `finale`). The sentinel strings below were
  transcribed from them at revision `b2fdff7`; re-verify each against the
  file before relying on it.

## Decisions applied

- **D-02** Coverage model: one persona (`careful-beginner`) across all five
  stages. The persona types the print-and-exit commands each lesson lists
  (curated below) and drives full-screen programs only where the lesson is
  about them (`man ls` in 5.1, `vim` in 5.2 and 5.3, and the gate). It
  never improvises.
- **D-03** Controlled inputs: the harness sets `LC_ALL=C`,
  `VIMINIT='set nocompatible'`, `PAGER=less`, unsets `MANPAGER` and
  `LESS`, keeps `TERM` (defaulting to `xterm-256color`), and forces
  `COLUMNS`/`LINES` to the PTY geometry. Everything else is inherited and
  recorded as a host input. `summary.md` gains a "Controlled inputs"
  section listing exactly these.

## Scope

In:

1. `Action` gains two optional fields: `raw: bool = False` (send bytes
   exactly, no trailing newline) and `delay_s: float = 0.0` (sleep before
   sending). Python 3.9 `NamedTuple` supports defaults.
2. `--stage {1,2,3,4,5,all}`; default stays `1`. For `N >= 2` the child is
   exec'd as `shelltutor N` (C-001); for `1` and `all` with no argument.
3. Sentinel catalogue and persona walks for stages 2 to 5 and the finale
   (tables below). Screen ids follow the density-audit convention:
   `S2-I`, `S2-L1`…`S2-L3`, `S2-G`, `S2-GT`, and so on; `S5-GT1`, `S5-GT2`
   for the two Stage 5 task phases; `FIN` for the finale.
4. Rejection guards per stage: the recall question sentinels and the
   gate-task header sentinels (a re-fire after the persona advanced past
   them means the gate rejected the answer or the task).
5. `error-signature` events: after each `persona-input` whose `screen_id`
   is a lesson screen, scan the normalized OUT text up to the next `PROMPT`
   for `No such file or directory`, `command not found`, `: not found`,
   `Permission denied`, `syntax error`, `Is a directory`. Emit
   `{"kind": "error-signature", "payload": {"text": <matched line>}}`.
   Non-fatal. Listed in `summary.md` under "Error signatures observed".
6. `.progress` assertion, read before sandbox cleanup: single stage `N`
   expects the file to contain `N`; `all` expects the file absent (the
   finale removes it). Recorded in the outcome as `progress_after` and
   `progress_ok`. TAP `ok` requires `gate_passed and progress_ok`.
7. Prerequisite handling: if `--stage` is `5` or `all` and
   `shutil.which("vim")` is `None`, do not start; write
   `ok 1 - … # SKIP vim not installed` to `result.tap`, note it in
   `summary.md`, exit **8** (`PrerequisiteMissingError`, new). If `man` is
   absent, skip the 5.1 `man ls` actions with intent `skip-man-missing`
   and continue.
8. Output layout: `--out` defaults to `audit/<UTC-date>/sim/stage<N>` or
   `audit/<UTC-date>/sim/all`. Summary headings say "Stage N baseline" or
   "Five-stage baseline".
9. `known_rough_edges(stage)` replaces `stage1_known_rough_edges()`; stages
   2 to 5 return an empty list and the summary says no density audit is
   recorded for that stage yet.
10. `scripts/sim/compare.py A B`: prints a unified diff of the normalized
    OUT projection of two bundle directories (reuse the projection logic in
    `run.py`; move it to a shared module if cleaner). Used by WP-02 and
    WP-03 for before/after comparisons.
11. `make sim` target: FF-006c rung 1, runs `--stage all` with the same
    Python-availability guard as `lesson-flow`; `SIMARGS` pass-through.
    `make lesson-flow` is unchanged.
12. Docs: `scripts/sim/README.md` (flags, exit code 8, layout, persona
    coverage), `CONTRIBUTING.md` Quality Gates table (`sim` row, FF-006c),
    `Makefile` header and `help`, `docs/simulation-design-plan.md`
    Implementation State ("FF-006c rung 1 complete: one persona, five
    stages; second persona still deferred"), `STATUS.md` one-liner.
13. Evidence: commit the bundles the acceptance run produces (below).
14. `summary.md` records `shelltutor_path_used` relative to the repository
    root, never as an absolute path (D-15; the Slice 1 bundle leaked an
    operator path). `sandbox_root` is a temporary directory and may stay.

Out: any change to `shelltutor`; a second persona; confusion events beyond
the mechanical error-signature scan; asciicast output; Linux runs (WP-06).

## Harness mechanics (exact)

Child environment (on top of the current `child_env` construction):

```python
child_env["LC_ALL"] = "C"
child_env["VIMINIT"] = "set nocompatible"
child_env["PAGER"] = "less"
child_env.pop("MANPAGER", None)
child_env.pop("LESS", None)
```

Record `{"LC_ALL": "C", "VIMINIT": "set nocompatible", "PAGER": "less",
"MANPAGER": "unset", "LESS": "unset", "COLUMNS": cols, "LINES": rows}` as
`controlled_inputs` and print them in `summary.md`.

Raw sends: `os.write(master_fd, action.send.encode("utf-8"))` with no
newline. Escape is `"\x1b"`, Ctrl+L is `"\x0c"`, Ctrl+C is `"\x03"`,
Tab is `"\t"`, Up arrow is `"\x1b[A"`, Enter is `"\n"`.

Vim timing rule: after sending Escape, the next action must carry
`delay_s=0.3` so Vim's key-code timeout cannot swallow the following
colon.

## Sentinel catalogue (post-ANSI-strip substrings)

| Id | Substring |
| --- | --- |
| `S2_INTRO` | `STAGE 2 — Paths and the filesystem` |
| `S2_L1` | `2.1 — ls: what's in here` |
| `S2_L2` | `2.2 — cd and the home folder` |
| `S2_L3` | `2.3 — paths: relative, absolute, dot, dot-dot` |
| `S2_GATE` | `STAGE 2 — GATE` |
| `S2_Q1` | `Q1: What does cd .. do?` |
| `S2_Q2` | `Q2: What does ~ mean in a path?` |
| `S2_Q3` | `Q3: If I'm in ~/projects and I type cd notes` |
| `S2_TASK` | `STAGE 2 — GATE TASK` |
| `S2_CLEARED` | `Stage 2 cleared.` |
| `S3_INTRO` | `STAGE 3 — Files and operations` |
| `S3_L1` | `3.1 — creating: touch, mkdir` |
| `S3_L2` | `3.2 — reading: cat, less` |
| `S3_L3` | `3.3 — copy, move, delete` |
| `S3_GATE` | `STAGE 3 — GATE` |
| `S3_Q1` | `Q1: Which command creates an empty file?` |
| `S3_Q2` | `Q2: After rm important.txt, where is the file?` |
| `S3_Q3` | `Q3: What single command renames old.txt to new.txt?` |
| `S3_TASK` | `STAGE 3 — GATE TASK` |
| `S3_CLEARED` | `Stage 3 cleared.` |
| `S4_INTRO` | `STAGE 4 — Commands, streams, composition` |
| `S4_L1` | `4.1 — reading a command` |
| `S4_L2` | `4.2 — the pipe` |
| `S4_L3` | `4.3 — redirection and globs` |
| `S4_GATE` | `STAGE 4 — GATE` |
| `S4_Q1` | `Q1: What does command -v vim print, if Vim is installed?` |
| `S4_Q2` | `Q2: What is the difference between > and >>?` |
| `S4_Q3` | `Q3: Why does vim my notes.txt open two files instead of one?` |
| `S4_TASK` | `STAGE 4 — GATE TASK` |
| `S4_CLEARED` | `Stage 4 cleared.` |
| `S5_INTRO` | `STAGE 5 — Ready for vimtutor` |
| `S5_L1` | `5.1 — print-and-exit vs full-screen` |
| `S5_L2` | `5.2 — entering and leaving Vim` |
| `S5_L3` | `5.3 — buffer vs file` |
| `S5_L4` | `5.4 — calling vimtutor` |
| `S5_GATE` | `STAGE 5 — GATE` |
| `S5_Q1` | `Q1: How do you exit man ls?` |
| `S5_Q2` | `Q2: After vim notes.txt, what makes Vim write your edit to the file?` |
| `S5_Q3` | `Q3: If you open notes.txt in vim, type some letters, and quit with :q!` |
| `S5_TASK1` | `STAGE 5 — GATE TASK (phase 1 of 2)` |
| `S5_PHASE1_OK` | `Phase 1 verified — the file was unchanged.` |
| `S5_TASK2` | `STAGE 5 — GATE TASK (phase 2 of 2)` |
| `S5_CLEARED` | `Stage 5 cleared.` |
| `FINALE` | `You're ready for vimtutor.` |
| `MAN_LS` | `LS(1)` |
| `VIM_INTRO` | `VIM - Vi IMproved` |
| `VIM_PRACTICE` | `"practice.txt"` |
| `VIM_INSERT` | `-- INSERT --` |

`S2_GATE` also occurs inside `S2_TASK`; the cursor-forward matcher handles
the order because the gate screen renders first. Same for stages 3 to 5.

## Persona walk (careful-beginner)

Notation: `wait → send`. `PROMPT` is `shelltutor> `. Unless marked `raw`,
sends get a trailing newline. Lesson commands are the curated subset of
what the screen lists; the persona does not type `cat *.txt` or any
`rm` outside the Stage 3 gate.

**Stage 1** keeps the existing walk, with one addition in lesson 1.1 after
the three `echo` lines: `PROMPT → raw "echo p\t"`, `"echo poem.txt" →
raw "\n"`, then continue. In `all` mode the trailing `PROMPT → quit` is
dropped and the walk continues at `S2_INTRO`.

**Stage 2**

```
S2_INTRO → "" ; PROMPT → next
S2_L1 → "" ; PROMPT → ls ; PROMPT → ls -l ; PROMPT → ls -a ; PROMPT → ls /etc ; PROMPT → next
S2_L2 → "" ; PROMPT → cd /tmp ; PROMPT → pwd ; PROMPT → cd ; PROMPT → cd - ; PROMPT → cd .. ; PROMPT → cd ~/.shelltutor ; PROMPT → next
S2_L3 → "" ; PROMPT → next
S2_GATE → "" ; S2_Q1 → goes up one folder ; S2_Q2 → home folder ; S2_Q3 → ~/projects/notes
S2_TASK → "" ; PROMPT → mkdir practice ; PROMPT → cd practice ; PROMPT → pwd ; PROMPT → check
S2_CLEARED → ""
```

The `cd ~/.shelltutor` line is kept deliberately: on the pre-fix script
under a tempdir `SHELLTUTOR_HOME` it produces the F-011 error signature.
WP-02 replaces it with the real sandbox path once the lesson copy changes.

**Stage 3**

```
S3_INTRO → "" ; PROMPT → next
S3_L1 → "" ; PROMPT → touch hello.txt ; PROMPT → ls ; PROMPT → mkdir notes ; PROMPT → ls ; PROMPT → next
S3_L2 → "" ; PROMPT → cat hello.txt ; PROMPT → cat ~/.shelltutor/poem.txt ; PROMPT → next
S3_L3 → "" ; PROMPT → cp hello.txt backup.txt ; PROMPT → mv hello.txt hi.txt ; PROMPT → mv hi.txt notes/ ; PROMPT → rm backup.txt ; PROMPT → next
S3_GATE → "" ; S3_Q1 → touch ; S3_Q2 → gone ; S3_Q3 → mv
S3_TASK → "" ; PROMPT → echo hello > notes.txt ; PROMPT → cp notes.txt backup.txt ; PROMPT → mv notes.txt done.txt ; PROMPT → rm backup.txt ; PROMPT → check
S3_CLEARED → ""
```

The `less ~/.shelltutor/poem.txt` line from 3.2 is not typed in this
package (known-broken pre-fix; the `cat` already evidences F-011). WP-02
adds the pager walk when the copy changes to `less ../numbers.txt`.

**Stage 4**

```
S4_INTRO → "" ; PROMPT → next
S4_L1 → "" ; PROMPT → ls -l ; PROMPT → wc -l poem.txt ; PROMPT → echo "hello world" ; PROMPT → command -v ls ; PROMPT → command -v vim ; PROMPT → next
S4_L2 → "" ; PROMPT → seq 1 100 | wc -l ; PROMPT → ls /usr/bin | sort | head ; PROMPT → ls /usr/bin | grep ^a | wc -l ; PROMPT → next
S4_L3 → "" ; PROMPT → echo first > greeting.txt ; PROMPT → echo second >> greeting.txt ; PROMPT → cat greeting.txt ; PROMPT → wc -w < poem.txt ; PROMPT → ls *.txt ; PROMPT → next
S4_GATE → "" ; S4_Q1 → the path to vim ; S4_Q2 → > overwrites, >> appends ; S4_Q3 → because of the space
S4_TASK → "" ; PROMPT → seq 1 100 | wc -l > count.txt ; PROMPT → ls *.txt ; PROMPT → check
S4_CLEARED → ""
```

**Stage 5**

```
S5_INTRO → "" ; PROMPT → next
S5_L1 → "" ; PROMPT → man ls ; MAN_LS → raw "q" ; PROMPT → next           (skip the man pair if man is absent)
S5_L2 → "" ; PROMPT → command -v vim ; PROMPT → vim --version ; PROMPT → vim ; VIM_INTRO → ":q" ; PROMPT → next
S5_L3 → "" ; PROMPT → cat practice.txt ; PROMPT → vim practice.txt ; VIM_PRACTICE → raw "i" ; VIM_INSERT → raw "abc" ; (delay 0.1) raw "\x1b" ; (delay 0.3) ":q!" ; PROMPT → cat practice.txt
          ; PROMPT → vim practice.txt ; VIM_PRACTICE → raw "i" ; VIM_INSERT → raw "abc" ; (delay 0.1) raw "\x1b" ; (delay 0.3) ":wq" ; PROMPT → cat practice.txt ; PROMPT → next
S5_L4 → "" ; PROMPT → command -v vimtutor ; PROMPT → next
S5_GATE → "" ; S5_Q1 → q ; S5_Q2 → :w ; S5_Q3 → no
S5_TASK1 → "" ; PROMPT → cat practice.txt ; PROMPT → vim practice.txt ; VIM_PRACTICE → raw "i" ; VIM_INSERT → raw "xyz" ; (delay 0.1) raw "\x1b" ; (delay 0.3) ":q!" ; PROMPT → cat practice.txt ; PROMPT → check
S5_PHASE1_OK → ""
S5_TASK2 → "" ; PROMPT → vim practice.txt ; VIM_PRACTICE → raw "i" ; VIM_INSERT → raw "after " ; (delay 0.1) raw "\x1b" ; (delay 0.3) ":wq" ; PROMPT → cat practice.txt ; PROMPT → check
S5_CLEARED → ""
FINALE → ""                                  (all mode: child then exits 0)
```

The 5.3 `cat practice.txt` lines produce `No such file or directory` on
the pre-fix script (F-010 evidence). That is expected; the gate still
passes because the gate seeds its own file.

Single-stage mode (`--stage N`, `N` in 2..5): the walk starts at
`S<N>_INTRO` (no welcome or orientation is shown) and, after
`S<N>_CLEARED`, waits for `PROMPT` and sends `quit`, because the tutor
continues into stage `N+1` (C-001). For `--stage 5` the finale follows the
cleared line instead and the child exits on its own.

## Acceptance criteria

1. On macOS with Bash 5.x first on `PATH` **and** with `/bin/bash` 3.2
   first on `PATH` (symlink a directory containing `bash -> /bin/bash` to
   the front of `PATH`), `python3 scripts/sim/run.py --stage all
   --variant current-rc --out <scratch>` exits 0, `result.tap` is `ok`,
   `progress_after` is `absent`.
2. `--stage N` for each `N` in 1..5 exits 0 with `progress_after` equal
   to `N`.
3. The `all` run records `error-signature` events at screens `S2-L2`
   (`cd ~/.shelltutor`), `S3-L2` (`cat ~/.shelltutor/poem.txt`) and `S5-L3`
   (`cat practice.txt`), and `summary.md` lists them with a pointer to
   F-010 and F-011 in `audit/2026-11-07/findings.md`.
4. `scripts/sim/compare.py` on two `all/current-rc` bundles from
   back-to-back runs shows only per-run noise (sandbox path, timestamps,
   `ls /usr/bin` counts).
5. `shelltutor` is byte-identical to `main`.
6. `make check lint smoke` and `make self-test` pass. All Python stays
   within 3.9 syntax and stdlib.
7. Docs listed in Scope item 12 are updated in the same commits as the
   behaviour they describe.

## Validation commands

```sh
make check lint smoke
make self-test
python3 scripts/sim/run.py --stage all --variant both -v --out "$TMPDIR/sim-all"
for n in 1 2 3 4 5; do python3 scripts/sim/run.py --stage "$n" --variant current-rc --out "$TMPDIR/sim-stage$n" || echo "stage $n: rc=$?"; done
python3 scripts/sim/compare.py "$TMPDIR/sim-all/current-rc" "$TMPDIR/sim-all/no-system-rc-preview"
```

PTY allocation requires a real tty-capable environment; if `pty.openpty`
fails inside an agent sandbox (`out of pty devices`), run the harness
outside the sandbox and say so in the report.

## Evidence to commit

Run the acceptance commands with the default `--out` and commit:

- `audit/<date>/sim/all/{current-rc,no-system-rc-preview}/` and
  `audit/<date>/sim/all/diff.md`
- `audit/<date>/sim/stage{2,3,4,5}/current-rc/`

Bundles must be green (`ok`). Error-signature events inside a green bundle
are evidence, not a red baseline.

## Commits (in order)

1. `feat(sim): raw/delayed actions, --stage N|all, controlled inputs, error signatures (FF-006c)`
   — mechanics only (`driver.py`, `run.py`, `recorder.py`, `env.py`,
   `errors.py`, `persona.py` `Action` fields), plus `compare.py`.
2. `feat(sim): careful-beginner walks for stages 2–5 and the finale (FF-006c)`
   — `sentinels.py`, `persona.py` stage builders and composer, rejection
   guards.
3. `chore(sim): add make sim; document FF-006c rung 1`
   — `Makefile`, `CONTRIBUTING.md`, `scripts/sim/README.md`,
   `docs/simulation-design-plan.md`.
4. `chore(audit): five-stage careful-beginner baseline at <short-sha> (FF-006c)`
   — evidence bundles and the `STATUS.md` one-liner, citing F-010 and
   F-011 as observed.

## Report

Use the template in `docs/workplan/README.md`. Include the TAP lines for
the `all` run under both Bash generations and the list of
`error-signature` screens observed.
