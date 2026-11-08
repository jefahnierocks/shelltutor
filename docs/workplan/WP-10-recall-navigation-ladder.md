---
title: WP-10 — Recall navigation, one three-rung ladder, hint-leak check
category: planning
component: workplan
status: drafted-frozen
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, phase-b, recall, ladder, c-006, ff-009, second-try]
priority: high
---

# WP-10 — Recall navigation, one three-rung ladder, hint-leak check

**Governing text**: `docs/direction-decisions-2026-11.md` §2 Phase B and
amendment A1 (A1.1, A1.2, A1.3, A1.6, A1.7). Where this package and A1
differ, A1 governs. **Tier**: core standard. **Depends on**: Phase A
summary (`audit/<date>/walkthroughs.md`) for the answer-list widening only;
everything else may be built now. **Landing order**: fifth and last (A2.6), after WP-15, WP-11, WP-12 and
WP-14, because the Stage 1–2 hints depend on WP-14's final screens. **Script freeze**: nothing here lands on `main` before the Phase A
summary exists (A1.9). **Touches `shelltutor`**: yes.

## Goal

Close drop-off risks 1 and 3 of `docs/design-description.md` §3.4: a
learner at a recall question or a Stage 1 follow-up prompt can leave or
re-read, gets one hint on the second miss, and from the third miss is told
what `quit` and `show` do. One ladder, one code path, no reveal.

## Read first

- `AGENTS.md`; `docs/workplan/README.md` (protocol, D-19).
- `docs/direction-decisions-2026-11.md` A1.1–A1.3, A1.6, A1.7.
- `shelltutor`: `ask_question` (`477-502`), the Stage 1 follow-up prompts
  (`869-882`), `gate_escalate` (`554-566`), every `ask_question` call
  (`802-824`, `1045-1075`, `1277-1291`, `1519-1550`, `1832-1860`),
  `practice()` footer and quit handling (`370-378`, `432-436`).
- `docs/contracts.md` C-006; `scripts/sim/persona.py` (`_recall`,
  `_gate_commands`), `scripts/sim/run.py` (`ALMOST_TEXT` oracle).
- `scripts/check-portability.sh` as the model for a new checker.

## Change 1 — `ask_question` signature and ladder

New signature, one argument per source line (the hint-leak checker relies
on this layout):

```bash
ask_question "<prompt>" \
    "<hint>" \
    '<accepted 1>' \
    '<accepted 2>' ...
```

Behaviour per attempt (A1.1):

| Attempt | After a miss, print |
| --- | --- |
| 1 | the existing `not quite. try again.` |
| 2 | `Hint: <hint>` |
| 3 and later | `Hint: <hint>` then the navigation line of Change 2 |

Rules: the counter is per question and resets when the next question
starts; `show` re-prints the question text only and does not advance the
counter; `quit` prints the farewell and exits 0 exactly as `practice()`
does (`shelltutor:432-436`); no accepted form is ever printed. Sketch:

```bash
ask_question() {
    local prompt="$1" hint="$2"; shift 2
    local accept=("$@")
    local ans norm ok_norm matched attempt=0
    while true; do
        printf '%b%b%b\n' "$Q" "$prompt" "$RST"
        printf '  %byour answer:%b ' "$CMD" "$RST"
        IFS= read -r ans < /dev/tty || { printf '\n'; return 1; }
        case "$(normalize_answer "$ans")" in
            show) continue ;;
            quit|exit) recall_quit ;;        # farewell + exit 0, see below
        esac
        norm=$(normalize_answer "$ans"); matched=0
        for ok in "${accept[@]}"; do
            ok_norm=$(normalize_answer "$ok")
            [ "$norm" = "$ok_norm" ] && { matched=1; break; }
        done
        if [ "$matched" -eq 1 ]; then printf '  %b✓%b\n\n' "$OK" "$RST"; return 0; fi
        attempt=$((attempt + 1))
        printf '  %bnot quite. try again.%b\n' "$EM" "$RST"
        [ "$attempt" -ge 2 ] && printf '  %bHint:%b %s\n' "$SUB" "$RST" "$hint"
        [ "$attempt" -ge 3 ] && recall_navigation_line
        printf '\n'
    done
}
```

`recall_quit` clears the screen and prints the same farewell as
`practice()`; factor that text into one helper used by both so C-006's
"farewell" is one string. `show` and `quit` are matched after
normalisation, so `Show` and ` quit ` work; they are never accepted
answers (no recall question accepts those words today; the hint-leak
checker also fails if one ever does).

Bash 3.2 note: keep `"${accept[@]}"` behind the non-empty guarantee (every
call passes at least one accepted form).

## Change 2 — The navigation line (A1.6)

Three facts, in this order, one line each. Wording is not contractual;
the facts are (C-006):

```
  Passed stages are saved.
  Type quit to leave now; the next run starts this stage from its first lesson.
  Type show to see the question again.
```

Do not use the word "retake" (A1.6).

## Change 3 — Fifteen hints (A1.1, A1.2)

One hint per question, naming the concept without containing any accepted
answer as a substring, case-insensitive. Two questions accept a single
character or a two-letter word (`q`; `no`), so their hints avoid that
letter sequence entirely. Drafted copy; the Phase A rejected-answer list
may revise it:

| Stage, Q | Hint |
| --- | --- |
| 1, Q1 | It is the symbol that also goes in front of a variable's name. |
| 1, Q2 | Think of where you are standing in the filesystem, not who you are. |
| 1, Q3 | Where did the letters appear when you pressed Enter? |
| 2, Q1 | Two dots name the folder that contains this one. |
| 2, Q2 | It is where `cd` with nothing after it takes you. |
| 2, Q3 | A relative name is added onto the folder you are already in. |
| 3, Q1 | It is the one that can also update a file's timestamp. |
| 3, Q2 | Lesson 3.3 said this command has no undo and no Trash. |
| 3, Q3 | Renaming and moving are the same action in the shell. |
| 4, Q1 | It answers with the folder and name of the program file. |
| 4, Q2 | One of them starts the file fresh; the other keeps what was there and adds. |
| 4, Q3 | Look at what separates the two words after `vim`, and what quotes would have done. |
| 5, Q1 | The same single key leaves `less`. |
| 5, Q2 | A colon command whose letter is the first letter of "write". |
| 5, Q3 | Lesson 5.3: the buffer is a copy; the disk only changes when you write it. |

The checker in Change 4 is the arbiter; if a hint trips it, change the
hint, not the accepted list.

## Change 4 — Hint-leak check (A1.2): FF-009

New `scripts/check-hints.sh`, same shape as the sibling checkers
(`--self-test`, exit 0/1/2), wired into `make check` and `make self-test`,
with a `CONTRIBUTING.md` §Quality Gates row:

| Target | Rule | What it enforces |
| --- | --- | --- |
| `check-hints` | FF-009 | for every `ask_question` call, no accepted answer appears in the hint, case-insensitive; the call has exactly one prompt, one hint and at least one accepted form, one argument per line; `show`, `quit` and `exit` are never accepted forms |

Parsing: an awk state machine that starts at a line matching
`^[[:space:]]*ask_question[[:space:]]+\\?$` or
`ask_question "`, collects one quoted argument per continuation line until
a line without a trailing backslash, strips the quotes, and evaluates the
rule. Argument 1 is the prompt, 2 the hint, 3+ accepted forms. Self-test
fixtures: a clean call; a hint containing an accepted word; a hint
containing `q` where `q` is accepted; a call with the arguments on one
line (must fail the layout rule). Record FF-009 in
`audit/2026-11-08/findings.md` under a "Proposed fitness function"
heading like FF-008's.

## Change 5 — Stage 1 follow-up prompts (A1.1, A1.7)

The three `read` prompts at `shelltutor:869-882` accept `show` (re-print
the three-question block header and the current question) and `quit`
(farewell, exit 0) after normalisation, through one small helper so the
behaviour matches `ask_question`. They have no ladder (they are
transcription prompts, not recall), but a mismatch already names the
failing answer (`890-892`).

The `pwd` comparison trims surrounding whitespace, then accepts the typed
path if it equals `$SANDBOX/stage1` or `$(cd "$SANDBOX/stage1" && pwd -P)`.

**F-015 (Phase A sitting 1).** The day question becomes
"What day of the week did `date` show? Type just the day, for example
Sat." (the F-013 phrase "or exactly as date printed it" is removed; it
invited the whole date line). `stage1_day_matches` additionally accepts an
answer that *contains* the day as a whole word in either locale form, so
a learner who pastes the entire `date` output still passes: split the
normalised answer on whitespace and test each word with the existing
comparison before failing. The harness sentinel `TASK_Q_DAY` matches the
unchanged prefix.

## Change 5b — Follow-ups re-ask only the mismatched item (A2.4)

On a Stage 1 follow-up mismatch, re-ask only the item(s) that failed
(`stage1_verify_whoami`, `stage1_verify_pwd`, `stage1_day_matches`), not
the whole task; the task restarts only if the learner types `quit` or if
the history check fails. Sitting 1's "had to run check several times" was
the restart compounding F-015.

## Change 5c — Pre-task hints removed at stages 2–4 (A3.8, Q8 default)

The gate task screens at stages 2, 3 and 4 drop their pre-task hint lines
(`shelltutor:1094`, `1309`, `1572`) and instead say what the gate checks
(for example "I will check that the folder exists, and how you got
there"). The rung-2 hint takes the pre-hint's place so fading runs forward
(baseline §6 item 7). Hint texts for Stages 1–2 are finalised against
WP-14's screens before this package lands.

## Change 6 — Harness: `second-try` observes the recall rungs (A1.3)

At Stage 2 only, `second-try` answers Q1 wrong three times, then
correctly. Under A1.1 the hint prints at miss 2 and again at miss 3 with
the navigation facts, so the oracle asserts `Hint:` exactly twice and the
first navigation fact (`Passed stages are saved.`) exactly once in a Stage
2 `second-try` run; Stage 4 `second-try` asserts zero of each (its task
misses once and prints no hint). *Corrected 2026-11-08 at review: the
earlier text asked for one `Hint:` over two misses, which cannot reach
the navigation rung.*

## Change 7 — Drift to close (A1.7)

- `shelltutor:466` comment "No hints, no answer reveal" → "Hints on the
  second miss, navigation facts from the third; never a reveal."
- `docs/contracts.md` C-006: add "Recall escalation: three rungs
  (message, hint, hint plus the three navigation facts); no reveal.
  Contractual: the rung order and the three facts. Not contractual: the
  wording."
- Search `README.md`, `ROADMAP.md`, `docs/contracts.md`, `shelltutor`
  heredocs for any sentence saying recall has no hints; correct each in
  this package.
- Answer-list widening: **[from Phase A]** — take the rejected-but-
  reasonable list from `audit/<date>/walkthroughs.md`; add forms only from
  it; cite the summary in the commit body.

## Acceptance

1. `make verify`, `make self-test` (including FF-009) green; smoke
   invariants hold.
2. FF-009 passes on the final script and fails on each self-test
   fixture.
3. `careful-beginner --stage all` green on Bash 3.2 and 5.x;
   `second-try --stage 2` green with `RECALL_HINT`, `RECALL_NAV` and
   `Hint:` each exactly once; `second-try --stage 4` unchanged.
4. Scripted pty check (reported, not committed): at Stage 3 Q1, typing
   `show` re-prints the question without counting; typing a wrong answer
   three times shows the message, then the hint, then the hint plus the
   three facts; typing `quit` prints the farewell and exits 0 with
   `.progress` unchanged.
5. No accepted form appears anywhere in the transcript before the correct
   answer is typed.

## Commits

1. `feat(gate): recall questions accept show and quit; one three-rung ladder with hints (A1.1, A1.6)`
2. `feat(quality): FF-009 hint-leak check`
3. `fix(gate): Stage 1 follow-ups accept show and quit; pwd compares logical and physical paths`
4. `feat(sim): second-try observes the recall hint and navigation rungs`
5. `docs(contracts): C-006 recall ladder; drift corrections (A1.7)`
6. `fix(gate): widen accepted recall answers from the Phase A list` **[from Phase A]**
7. `chore(audit): post-WP-10 evidence; STATUS`
