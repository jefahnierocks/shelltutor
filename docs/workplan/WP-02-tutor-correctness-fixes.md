---
title: WP-02 — Tutor correctness fixes (F-010 to F-013) and FF-008
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, lessons, gates, portability, locale, ff-004, ff-008]
priority: high
---

# WP-02 — Tutor correctness fixes (F-010 to F-013) and FF-008

**Depends on**: WP-01 (the pre-fix five-stage baseline must be committed
first). **Blocks**: WP-03, WP-04, WP-05. **Touches `shelltutor`**: yes.
**Operator gate**: none. Every change here keeps the script one file,
Bash 3.2+, POSIX userland, no network, no privilege, writes only under
`$SANDBOX`.

## Goal

Close the four findings in `audit/2026-11-07/findings.md`, apply the
stage-folder model (D-04) and the startup path normalisation (D-08), add the
FF-008 checker, update contracts C-003 and C-004, re-run the five-stage
harness, and commit the post-fix evidence next to the pre-fix baseline.

## Read first

- `docs/workplan/README.md` decisions D-04 to D-08.
- `audit/2026-11-07/findings.md` (all four findings and observations O-C).
- `docs/contracts.md` C-003 and C-004.
- `scripts/check-portability.sh` and `scripts/check-safety.sh` (the awk
  heredoc state machine FF-008 copies).
- `shelltutor`: `SANDBOX=` constants block, `setup_stage_dir`, `lesson`,
  `ask_question`, `stage1_verify_task`, the Stage 1 gate follow-ups,
  `stage2_lesson_2`, `stage3_*`, `stage4_gate` seed block, `stage5_*`.
- The `WP-01` bundle under `audit/<date>/sim/all/current-rc/summary.md`
  ("Error signatures observed").

## Change 1 — Startup path normalisation (D-08, observation O-C)

Replace the single `SANDBOX=` assignment with:

```bash
SANDBOX="${SHELLTUTOR_HOME:-$HOME/.shelltutor}"
# A relative SHELLTUTOR_HOME is anchored to the caller's directory once, so
# the sandbox does not move when the practice shell changes folder.
case "$SANDBOX" in
    /*) ;;
    *)  SANDBOX="$PWD/$SANDBOX" ;;
esac
# Trailing slashes would make "$SANDBOX/stage1" differ from what pwd prints.
while [ "${#SANDBOX}" -gt 1 ] && [ "${SANDBOX%/}" != "$SANDBOX" ]; do
    SANDBOX="${SANDBOX%/}"
done
PROGRESS_FILE="$SANDBOX/.progress"
```

Contract C-004: add one sentence under `SHELLTUTOR_HOME`: "Normalised at
startup: made absolute against the invoking directory and stripped of
trailing slashes; `--info` and all lesson copy show the normalised value."

## Change 2 — Portable answer normalisation (F-012)

Add above `ask_question`:

```bash
# Lower-case, collapse any run of whitespace to one space, trim the ends.
# tr -s is POSIX; GNU sed's \+ is not (audit/2026-11-07/findings.md F-012).
normalize_answer() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -s '[:space:]' ' ' \
        | sed 's/^ //; s/ $//'
}
```

In `ask_question`, replace both `tr … | sed …` pipelines with
`norm=$(normalize_answer "$ans")` and `ok_norm=$(normalize_answer "$ok")`.
Leave the Stage 1 follow-up trimming (`sed 's/^[[:space:]]*//;
s/[[:space:]]*$//'`) as it is; it contains no GNU syntax.

## Change 3 — Locale-tolerant day check (F-013, D-06)

Add next to `stage1_verify_task`:

```bash
# Accept the day as `date` printed it in the learner's locale or as the
# English form the question lists. Case-insensitive; a trailing period is
# ignored (de_DE prints "Sa."); a full name also matches by its first three
# characters ("saturday" -> "sat").
stage1_day_matches() {
    local given cand norm
    given=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' \
        | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s/\.$//')
    [ -n "$given" ] || return 1
    for cand in "$(LC_ALL=C date +%a)" "$(LC_ALL=C date +%A)" \
                "$(date +%a)" "$(date +%A)"; do
        norm=$(printf '%s' "$cand" | tr '[:upper:]' '[:lower:]' | sed 's/\.$//')
        [ -n "$norm" ] || continue
        [ "$given" = "$norm" ] && return 0
        case "$norm" in
            "$given"*) [ "${#given}" -ge 3 ] && return 0 ;;
        esac
    done
    return 1
}
```

Then:

- in `stage1_verify_task`, replace the `TASK_S1_DAY` line with
  `stage1_day_matches "${TASK_S1_DAY:-}" || return 1`;
- in `stage1_gate`, delete the `tr | sed | awk` title-case pipeline that
  rewrites `TASK_S1_DAY` (the trim line above it stays) and change the
  question to:
  `What day of the week did date show? (Mon, Tue, … — or exactly as date printed it)`.
  The harness sentinel `TASK_Q_DAY` matches the unchanged prefix.

The F-008 comment block that explains the `awk` title-case step goes with
the pipeline; keep a one-line pointer to F-008 and F-013 in the new
function's comment instead.

## Change 4 — Stage-folder model and fixtures (F-010, D-04)

1. `setup_stage_dir` becomes:

   ```bash
   setup_stage_dir() {
       local n=$1
       mkdir -p "$SANDBOX/stage${n}"
       case "$n" in
           4)  # Stage 4 lessons count lines in poem.txt from inside the
               # stage folder; seed.txt gives the *.txt glob a second match.
               [ -f "$SANDBOX/stage4/poem.txt" ] \
                   || cp "$SANDBOX/poem.txt" "$SANDBOX/stage4/poem.txt"
               if [ ! -f "$SANDBOX/stage4/seed.txt" ]; then
                   cat > "$SANDBOX/stage4/seed.txt" <<'EOF_SEED'
   a small text file
   to give the glob something to match
   EOF_SEED
               fi
               ;;
           5)  # Lesson 5.3 edits practice.txt; the gate re-seeds it to
               # exactly 'before' at gate entry (stage5_seed_practice).
               [ -f "$SANDBOX/stage5/practice.txt" ] \
                   || echo before > "$SANDBOX/stage5/practice.txt"
               ;;
       esac
   }
   ```

   Remove the `seed.txt` block from `stage4_gate` (it now lives here).
   Use a heredoc marker other than `EOF` so the checkers' state machine
   and the outer heredoc do not collide; `EOF_SEED` is fine.

2. `run_stage3`, `run_stage4`, `run_stage5`: call `setup_stage_dir N` as
   the first statement, before the lesson loop.

3. Every `lesson <<EOF` inside `stage3_*`, `stage4_*`, `stage5_*`
   (intros and lessons) becomes `lesson "$SANDBOX/stage3" <<EOF` (or 4, 5).
   Update the comment above `lesson()`; the `SC2120` disable stays.
   Stages 1 and 2 keep the `$SANDBOX` default.

4. Copy that becomes true without edits: `stage3_intro` ("inside
   `${SANDBOX}/stage3`"), `stage5_lesson_3` ("A practice.txt fixture is in
   this stage's folder").

5. Copy that must change (exact replacement lines):

   `stage2_lesson_2`, replace the three-line `${EM}This tutor's sandbox…`
   paragraph with:

   ```
   ${EM}Stages 1 and 2 start every practice prompt in${RST} ${DIR}${SANDBOX}${RST}${EM}.${RST}
   Later stages start in a stage folder inside it. If you wander off,
   ${CMD}cd ${SANDBOX}${RST} brings you back.
   ```

   `stage3_lesson_2`, replace the `cat ~/.shelltutor/poem.txt` and
   `less ~/.shelltutor/poem.txt` lines with:

   ```
     ${CMD}cat ../poem.txt${RST}        ${DIM}# the tutor's poem, one folder up${RST}
   ```

   and

   ```
     ${CMD}less ../numbers.txt${RST}    ${DIM}# 50 lines — more than one screen${RST}
   ```

   Keep every other line of those screens unchanged. Check the vertical
   budget comment still holds (no screen grows past 20 content lines).

## Change 5 — FF-004 extension and FF-008 checker (F-011, F-012, D-05, D-07)

1. `scripts/check-portability.sh`: inside the heredoc branch add, after
   the existing `vm_stat`/`systemctl`/`launchctl` rules:

   ```awk
   if (match($0, /~\/\.shelltutor|\$HOME\/\.shelltutor/)) {
       printf "%s:%d: FF-004 sandbox path hardcoded (use ${SANDBOX}): %s\n", FILENAME, NR, $0
       violations++
       next
   }
   ```

   Add a self-test fixture that fails on `cd ~/.shelltutor` and confirm the
   existing fixtures still pass. Update the header comment's rule list.

2. New `scripts/check-posix-tools.sh` (FF-008). Same skeleton as
   `check-safety.sh` (scan code lines outside heredocs; skip comment lines
   and lines containing `# nofitness:`; exit 0/1/2; `--self-test`).
   Rules, each printing `FILENAME:NR: FF-008 <label>: <line>`:

   | Label | awk condition |
   | --- | --- |
   | `GNU sed repetition/alternation` | line contains `sed` and matches `/\\[+?|]/` |
   | `GNU sed case conversion` | line contains `sed` and matches `/\\[LUlu]/` |
   | `GNU sed character class` | line contains `sed` and matches `/\\[swd]/` |
   | `sed -i` | matches `/(^|[[:space:]])sed[[:space:]]+(-[A-Za-z]*)?-i([[:space:]]|$)/` |
   | `grep -P` | matches `/(^|[[:space:]])grep[[:space:]]+(-[A-Za-z]*)?P([[:space:]]|$)/` |
   | `readlink -f` | matches `/readlink[[:space:]]+-f/` |
   | `date -d` | matches `/(^|[[:space:]])date[[:space:]]+(-d|--date)/` |
   | `stat -c` | matches `/(^|[[:space:]])stat[[:space:]]+-c/` |

   Note `\\[LUlu]` would also match `\l` in a printf format; the rule is
   scoped to lines that contain `sed`, which is why the first three rules
   test for the word `sed` first.

   Self-test fixtures: a clean file using `tr -s`, `awk`, and
   `sed 's/^[[:space:]]*//'`; a failing `sed 's/a\+/b/'`; a failing
   `sed -i 's/a/b/' file`; a file whose only hit is annotated
   `# nofitness:posix` (must pass). Heredoc bodies containing `sed -i` must
   not be flagged.

3. `Makefile`: `check: check-safety check-governance check-portability
   check-posix-tools`; new `check-posix-tools` recipe; add the
   `--self-test` line to `self-test`; update the header comment and `help`
   text ("FF-001 + FF-002 + FF-004 + FF-007 + FF-008").

4. `CONTRIBUTING.md` Quality Gates table: add the `check-posix-tools`
   row (FF-008) and extend the `check-portability` row with the sandbox
   path rule. Portability Rules: add the bullet "Uses GNU-only text-tool
   syntax in script code (`sed \+`, `sed -i`, `grep -P`, `readlink -f`,
   `date -d`, `stat -c`)".

5. `.claude/settings.json` is not touched (its allowlist already covers
   `make check`).

## Change 6 — Contracts

`docs/contracts.md`:

- C-003 tree: add `stage3/hello.txt`, `stage3/notes/` as learner-created
  lesson files (not contractual); `stage4/poem.txt` ("copy of the fixture,
  seeded on stage entry"); mark `stage4/seed.txt` and `stage5/practice.txt`
  as seeded on stage entry (`practice.txt` re-seeded to `before` at gate
  entry). Add a short "Where practice prompts start" paragraph: stages 1
  and 2 start in `$SANDBOX`; stages 3 to 5 start in their stage folder for
  lessons and gates.
- C-004: the normalisation sentence from Change 1.
- Audit cross-reference table: note C-003 and C-004 "extended 2026-11
  (WP-02)".

## Change 7 — Harness follow-through

`scripts/sim/persona.py` (and sentinels if needed) must follow the copy:

- Stage 2 lesson 2.2: replace `cd ~/.shelltutor` with `cd <sandbox_root>`
  (the persona builder already receives the sandbox root for the Stage 1
  `pwd` answer; pass it through).
- Stage 3 lesson 3.2: replace `cat ~/.shelltutor/poem.txt` with
  `cat ../poem.txt`, then add `less ../numbers.txt` → wait sentinel
  `LESS_NUMBERS` = `"1\n2\n3\n4\n5"` → raw `q` → `PROMPT`.
- Stage 5 lesson 5.3 needs no persona change; the `cat practice.txt`
  lines now print `before` or the edited text.

Re-run the five-stage harness; the `error-signature` list must be empty
on the post-fix script.

## Acceptance criteria

1. `make check lint smoke` and `make self-test` pass, including the new
   FF-004 fixture and the FF-008 self-test; `make check` on the pre-fix
   script (`git stash` or `git show main:shelltutor > /tmp/old`) reports
   the F-011 and F-012 lines, proving the new rules bite.
2. `./shelltutor -h` and `./shelltutor --info` run; `make smoke` structural
   invariants unchanged.
3. Harness `--stage all --variant current-rc` exits 0 under Bash 3.2 and
   5.x with zero `error-signature` events.
4. Manual spot-check on macOS, documented in the report:
   `LC_ALL=de_DE.UTF-8 ./shelltutor 1` reaches the Stage 1 gate and
   accepts both `Sa` and `Sat` for a Saturday run (or the equivalent for
   the day of the check).
5. `SHELLTUTOR_HOME=relative-dir ./shelltutor --info` shows an absolute
   sandbox path; `SHELLTUTOR_HOME=/tmp/x/ ./shelltutor --info` shows
   `/tmp/x`.
6. No lesson heredoc contains `~/.shelltutor`; `grep -n '\\+' shelltutor`
   finds no sed expression.

## Validation commands

```sh
make check lint smoke
make self-test
./scripts/check-posix-tools.sh --self-test
python3 scripts/sim/run.py --stage all --variant current-rc -v --out "$TMPDIR/sim-post"
python3 scripts/sim/compare.py audit/<date>/sim/all/current-rc "$TMPDIR/sim-post/current-rc"
```

## Commits (in order; cite IDs in bodies)

1. `fix(startup): normalise SHELLTUTOR_HOME to an absolute path without trailing slash`
2. `fix(gate): portable whitespace normalisation in ask_question (F-012)`
3. `fix(gate): accept the day of week as date printed it in any locale (F-013)`
4. `fix(lessons): run stage 3–5 lessons in their stage folder and seed fixtures (F-010)`
5. `fix(lessons): reference the configured sandbox instead of ~/.shelltutor (F-011)`
6. `feat(quality): FF-004 sandbox-path rule and FF-008 POSIX text-tool checker`
7. `docs(contracts): stage folder model (C-003) and sandbox normalisation (C-004)`
8. `chore(audit): post-fix five-stage evidence; resolve F-010–F-013`
   — new bundle under `audit/<date>/sim/all-postfix/current-rc/` (or the
   next UTC date's `sim/all/`), findings statuses set to resolved with the
   fixing short SHAs, `STATUS.md` one-liners updated.

## Report

Template in `docs/workplan/README.md`. Include the before/after
`compare.py` summary (which screens changed) and the locale spot-check
result.
