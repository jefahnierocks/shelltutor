---
title: WP-05 — Gate verification alignment and escalating feedback
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, gates, feedback, roadmap, pedagogy]
priority: medium
---

# WP-05 — Gate verification alignment and escalating feedback

**Depends on**: WP-01, WP-02 (baseline and stage-folder model).
**Blocks**: nothing. **Touches `shelltutor`**: yes (gate functions).
**Operator gate**: none. Independent of WP-03 and WP-04; if run after
them, rebase on their result.

## Goal

Bring the Stage 2 and Stage 4 gates up to the ROADMAP Phase 3 spec
(history-trace checks), share one helper for "which commands did the
learner actually run", and add the design plan's escalating retry feedback
to every gate. Never auto-pass.

## Read first

- `docs/workplan/README.md` decision D-14.
- `audit/2026-11-07/findings.md` observation O-A.
- `ROADMAP.md` Phase 3 per-stage gate specs and the "Gate pattern"
  pseudocode.
- `docs/simulation-design-plan.md` §Pedagogy And UX ("Repeated gate
  failure should eventually escalate").
- `shelltutor`: `history_mark`, `history_since`,
  `stage1_check_commands_run`, every `stageN_gate` and `stageN_verify_*`.

## Change 1 — Shared history helper

Add next to `history_since`, and rewrite `stage1_check_commands_run` to
call it (same labels and patterns as today):

```bash
# gate_require_history MARK LABEL ERE [LABEL ERE ...]
# Looks at the practice-shell commands recorded since MARK (a history_mark
# value). Each ERE is matched with grep -E against the recorded lines.
# Prints the "Almost — you still need to" list for every LABEL whose ERE
# never matched and returns 1; returns 0 when everything was seen.
gate_require_history() {
    local mark="$1"; shift
    local recent label pattern
    local missing=()
    recent=$(history_since "$mark")
    while [ "$#" -ge 2 ]; do
        label="$1"; pattern="$2"; shift 2
        printf '%s\n' "$recent" | grep -qE "$pattern" || missing+=("$label")
    done
    [ "${#missing[@]}" -eq 0 ] && return 0
    printf '\n%bAlmost — you still need to:%b\n' "$EM" "$RST"
    for label in "${missing[@]}"; do
        printf '  %b%s%b\n' "$CMD" "$label" "$RST"
    done
    printf '\nDo that at the prompt below, then type %bcheck%b again.\n' "$CMD" "$RST"
    return 1
}
```

Bash 3.2 note: `"${missing[@]}"` on an empty array fails under `set -u`;
the early `return 0` above keeps the loop unreachable in that case. Keep
that order.

## Change 2 — Stage 2 and Stage 4 history checks

- Stage 2: take `hist_mark=$(history_mark)` once before the gate-task
  loop. On `RC_CHECK`, first
  `gate_require_history "$hist_mark" "cd into it (cd practice)" '^[[:space:]]*cd([[:space:]]|$)'`;
  if it fails, re-enter the practice prompt without redisplaying the task
  screen (the `skip_screen` pattern from Stage 1), otherwise run
  `stage2_verify_task` as today.
- Stage 4: same shape with
  `"list the .txt files with a glob (ls *.txt)" '\*\.txt'`. History
  records the typed line, not the expansion, so the literal `*.txt`
  is what to look for.
- Stage 3 and Stage 5 verify filesystem state only (as specified).

## Change 3 — Escalating feedback

```bash
# gate_escalate ATTEMPT HINT EXAMPLE...
# attempt 1: nothing extra (the gate already printed what it saw).
# attempt 2: HINT. attempt 3+: HINT plus the worked EXAMPLE lines, which
# the learner still has to type themselves. There is no auto-pass.
gate_escalate() {
    local attempt="$1" hint="$2"; shift 2
    [ "$attempt" -ge 2 ] || return 0
    printf '%bHint:%b %s\n' "$SUB" "$RST" "$hint"
    if [ "$attempt" -ge 3 ]; then
        printf '%bWorked example — type these yourself:%b\n' "$SUB" "$RST"
        local line
        for line in "$@"; do
            printf '  %b%s%b\n' "$CMD" "$line" "$RST"
        done
    fi
    printf '\n'
}
```

Each gate keeps `local attempt=0`, increments it on every failed
verification (history miss or state miss), and calls `gate_escalate`
after its existing failure message with these texts:

| Gate | Hint | Worked example |
| --- | --- | --- |
| 1 | "Run the command again and copy its output exactly." Also name which of the three answers did not match (not the expected value): "The whoami/pwd/day answer did not match." | `whoami`, `pwd`, `date` |
| 2 | "mkdir makes the folder; cd moves into it; pwd shows where you are." | `mkdir practice`, `cd practice`, `pwd` |
| 3 | "echo hello > notes.txt writes a file; cp copies; mv renames; rm removes." | `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt` |
| 4 | "A pipe feeds seq into wc -l; > saves the count; *.txt is the glob." | `seq 1 100 \| wc -l > count.txt`, `ls *.txt` |
| 5 phase 1 | ":q! throws the change away; :wq would write it." | `vim practice.txt`, `i`, type a letter, `Esc`, `:q!` |
| 5 phase 2 | ":wq writes the buffer to the file, then quits." | `vim practice.txt`, `i`, type a letter, `Esc`, `:wq` |

For Stage 1, "which answer did not match" means splitting
`stage1_verify_task` into three checks and reporting the failing label(s);
do not print the expected value.

## Change 4 — Harness: `second-try` persona

Add persona `second-try` for stages 2 and 4 only (`--persona second-try
--stage 2|4`; other combinations exit 2 with a message):

- Stage 2 task: `mkdir practice`, `check` → wait sentinel `ALMOST` =
  `Almost — you still need to` → `cd practice`, `pwd`, `check` →
  `S2_CLEARED`.
- Stage 4 task: `seq 1 100 | wc -l > count.txt`, `check` → `ALMOST` →
  `ls *.txt`, `check` → `S4_CLEARED`.
- Recall answers as careful-beginner. TAP `ok` requires `ALMOST` observed
  exactly once and the stage cleared. Record the walk in
  `scripts/sim/README.md` under "Personas".

## Records

- `ROADMAP.md` Phase 3 `### Amendments`: "2026-11 (WP-05): Stage 2 gate
  requires at least one `cd` in the practice history (the task as taught),
  not the four-step trace in the original spec; Stage 4 gate verifies the
  `*.txt` glob from history as specified; all gates escalate feedback on
  repeated failure (restatement, hint, worked example) and never
  auto-pass."
- `docs/contracts.md` C-006: one sentence that gate feedback wording is
  not contractual but the escalation order is part of the curriculum
  design.
- `STATUS.md` one-liner; new harness bundles for `second-try` stages 2
  and 4 under `audit/<date>/sim/`.

## Acceptance criteria

1. careful-beginner `--stage all` still passes under Bash 3.2 and 5.x.
2. `second-try --stage 2` and `--stage 4` pass, with exactly one `ALMOST`
   each.
3. Manual: at the Stage 3 gate, type `check` three times without doing the
   task; the second attempt shows the hint, the third shows the worked
   example; the gate still does not pass.
4. `make check lint smoke` and `make self-test` pass.

## Commits (in order)

1. `refactor(gate): shared gate_require_history helper (Stage 1 unchanged in behaviour)`
2. `feat(gate): verify cd (Stage 2) and the *.txt glob (Stage 4) from practice history`
3. `feat(gate): escalating retry feedback — restatement, hint, worked example`
4. `feat(sim): second-try persona for stages 2 and 4`
5. `docs(roadmap): Phase 3 amendments for gate alignment; STATUS; evidence`

## Report

Template in `docs/workplan/README.md`; include the TAP lines for both
personas.
