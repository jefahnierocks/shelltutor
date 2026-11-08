---
title: WP-11 — Four stage-cleared screens, --info wording, D-19 redaction
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-b, stage-cleared, info, redaction, d-19]
priority: high
---

# WP-11 — Four stage-cleared screens, `--info` wording, D-19 redaction

**Governing text**: `docs/direction-decisions-2026-11.md` §2 Phase B and
amendment A1 (A1.4, A1.8, A1.9). **Tier**: core standard. **Depends on**:
the Phase A summary for the script change; the D-19 harness commit touches
only `scripts/sim/` and may land during Phase A. **Landing order**: second, after
WP-15 (A2.6); the screen is authored against the chrome and follows A3.5:
title `✓ Stage N cleared` (OK tick, H1 text), "You can now:", commands in
CMD aligned in a column each with a DIM gloss (≤ 8 lines), "Next: Stage
N+1 · <title>" in DIM, and the `▶` line ending "Your place is saved.";
footer bar in `cleared` mode. **Touches `shelltutor`**: yes (frozen until
`audit/<date>/walkthroughs.md` exists).

## Goal

Close drop-off risk 5 of `docs/design-description.md` §3.4: give each of
stages 1 to 4 a stopping point after its gate, and stop the `--info` text
from promising things the lessons do not do (§6 items 3 and 4). Make
committed harness evidence free of the host login name (D-19).

## Read first

- `docs/direction-decisions-2026-11.md` A1.4, A1.8.
- `shelltutor`: `main`'s stage loop (`2082-2089`), the five "cleared"
  `printf` lines (`885`, `1118`, `1328`, `1600`, `1943`), `lesson()` and
  `practice()` (`453-457`, `364-438`), the `run_stageN` `RC_CHECK` note
  (`921-928`), the finale list style (`1996-2008`), `show_info` lines
  `261`, `266`, `275`.
- `scripts/sim/sentinels.py` (`S<N>_CLEARED`), `persona.py`
  (`careful_beginner_stage1`, `stage_walk`, `build_walk`), `recorder.py`
  (`_safe_text`, `write_event`, `write_summary`), `run.py`
  (`controlled_inputs`).

## Change 1 — `stage_cleared N` (A1.4)

One function, called from `main` between stages 1→2, 2→3, 3→4 and 4→5.
Stage 5's gate keeps its own cleared line and flows into the finale.
Rendered as a lesson-mode screen through `lesson`, so the footer names
`next` and `show`/`prev` redisplay it. The recap is per-stage data in one
`case` (`stage_recap N`), at most eight lines, in the finale's list style.
Sketch (the package uses `RECAP` as the here-document marker so the
checkers' heredoc state machine sees a distinct block):

    stage_cleared() {
        local n=$1 next=$(( $1 + 1 ))
        lesson <<RECAP
    ${OK}✓ Stage ${n} cleared.${RST}

    $(stage_recap "$n")

    ${INSTR}▶ Type ${CMD}next${INSTR} for Stage ${next}, or ${CMD}quit${INSTR} to stop here.${RST}
    RECAP
    }

Recap data:

| Stage | Lines |
| --- | --- |
| 1 | `commands  echo, pwd, whoami, date, clear` / `keys      Tab, ↑, Ctrl+L, Ctrl+C` |
| 2 | `commands  ls, ls -l, ls -a, cd, cd .., cd ~, cd -, pwd` / `symbols   .  ..  ~` |
| 3 | `commands  touch, mkdir, rmdir, cat, less (q to leave), cp, mv, rm` |
| 4 | `commands  command -v, wc, seq, head, sort, grep` / `operators |  >  >>  <  *` |

Dispatch in `main`, replacing the body of the stage loop:

    for ((s=start; s<=TOTAL_STAGES; s++)); do
        run_stage "$s"; rc=$?
        [ "$rc" -ne 0 ] && exit 0
        if [ "$s" -lt "$TOTAL_STAGES" ]; then
            while true; do
                stage_cleared "$s"; rc=$?
                case "$rc" in
                    "$RC_NEXT") break ;;
                    "$RC_SHOW"|"$RC_PREV") : ;;
                    "$RC_CHECK") printf '\n%b(check is only for gate tasks. Type next to continue.)%b\n' "$DIM" "$RST"; sleep 2 ;;
                    *) exit 0 ;;
                esac
            done
        fi
    done

Remove the four `✓ Stage N cleared.` `printf` lines from the stage 1–4
gates so the text appears once, on the screen; keep Stage 5's. `quit` at
the screen is handled inside `practice()` as everywhere else. The screen
runs with `$SANDBOX` as the working directory (the `lesson` default). Each
screen is well under the 20-line budget (count in the report).

## Change 2 — `--info` wording (baseline §6 items 3, 4)

- `shelltutor:275`: "Stage 5 finale will hand off to this" becomes "the
  finale names this as the next step".
- `shelltutor:261`: "not found — Stage 5 lesson 5.1 will skip the man demo"
  becomes "not found — lesson 5.1's man ls example will not work until it
  is installed".
- `shelltutor:266`: the same shape for `less` and lesson 3.2.

## Change 3 — D-19: host user name redacted from committed artifacts (A1.8)

In `scripts/sim/recorder.py`, a redactor built once per run from
`getpass.getuser()`: every string written to `terminal.jsonl` (utf8 `data`
rows), `events.jsonl` (all string payload values, including the
`answer-task-whoami` input) and `summary.md` has the name replaced by the
fixed token `[user]`. Base64 rows are decoded, redacted and re-encoded only
when they contain the name. Names shorter than three characters are not
redacted (too many false hits); the summary records the choice under
"Controlled inputs" as `host_user: redacted as [user]` or
`host_user: not redacted (name too short)`. The hosted runner's `runner`
is redacted the same way, so `compare.py` differs across hosts only where
it should. Mention D-19 in `scripts/sim/README.md` §Evidence. Existing
bundles are not rewritten (operator's default).

## Change 4 — Harness follow-through

- The `S<N>_CLEARED` sentinel text is unchanged (`Stage N cleared.`) and
  now comes from the screen. After it, each persona waits `PROMPT` and
  sends `next` in `all` mode, or `quit` in single-stage mode (today's
  `quit` moves from the next stage's intro prompt to the cleared screen).
  `careful-beginner` and `second-try` each gain exactly one `next` per
  passed gate at stages 1–4.
- No new sentinel is strictly required; add `S<N>_CLEARED_NEXT`
  (`for Stage N+1, or quit to stop here`) only if the walk needs to prove
  the footer rendered.

## Acceptance

1. `make verify` and `make self-test` green.
2. `careful-beginner --stage all` green on Bash 3.2 and 5.x and hosted
   Linux; `--stage N` for 1..4 ends at the cleared screen with
   `progress_after = N`; `second-try` stages 2 and 4 green.
3. Scripted pty check (reported): at the Stage 2 cleared screen, `show`
   redisplays, `check` prints the note and redisplays, `quit` prints the
   farewell and exits 0 with `.progress` = 2; a fresh run resumes at
   Stage 3.
4. Committed bundles contain zero occurrences of the host login name
   (`grep -c` on every file) and `summary.md` says so.
5. `./shelltutor --info` no longer contains "hand off" or "will skip".
6. Every new screen fits the 20-line budget (count in the report).

## Commits

1. `feat(sim): redact the host user name from committed evidence (D-19)`
   (harness only; may land during Phase A)
2. `feat(stages): stopping point after each passed gate — stage_cleared screens for stages 1–4 (A1.4)`
3. `fix(info): --info describes the finale and the man/less lessons accurately`
4. `chore(sim): personas step through the cleared screens; evidence; STATUS`
