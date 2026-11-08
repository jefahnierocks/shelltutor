---
title: Slice 2 before/after comparison (practice-shell hardening)
category: audit
component: sim-slice-2
status: evidence
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, simulation, slice-2, c-007, comparison]
priority: medium
---

# Slice 2 before/after comparison

Before: `sim/all-postfix/current-rc` (WP-02, tutor before the practice-shell
change). After: `sim/all-slice2/current-rc` (Bash 5.3.20) at `6fa53d2`.
Produced with `python3 scripts/sim/compare.py`; macOS only (no Linux bundle
yet, see WP-06).

## Result

- **Only intended change:** the three lesson 1.1 Tab lines (D-10): "If several
  match, bash beeps…" and the zsh/fish remark became "Several matches? The
  first Tab fills in the shared part; Tab again lists them. (Other shells and
  setups differ.)"
- **Noise only otherwise:** temp sandbox paths, the `date` output, `ls -l`
  modification times in the Stage 2–4 listings, and Vim status-line chunking
  (`"practice.txt" 1L, 7B` appears or is split differently between runs).
- **No error signatures** in either post-hardening `all` bundle (Bash 5.3.20 and 3.2.57).
- All four post-hardening bundles are green: `all` and `stage1` under Bash
  5.3.20 and 3.2.57 (`progress_after` absent / 1 as expected).

## Readline and startup observations

- The Tab action in lesson 1.1 (`echo p` + Tab → `echo poem.txt`) completes
  under both Bash versions.
- Bells in the transcript (10) are Vim OSC terminators, identical before and
  after; no Readline bell reaches the practice prompt.
- Under Bash 3.2 the stream contains `ESC[?1034h` (29 occurrences). It is
  present on `main` before this change too, so `INPUTRC=/dev/null` adds no
  new startup bytes; it comes from Bash 3.2's Readline. Under Bash 5.3 it is
  absent. No other new startup bytes were seen.

## Environment-scrub check (acceptance item 4)

**Automated PTY check, not a human-terminal check.** The harness driver
started `shelltutor 1` with `HISTIGNORE='pwd:date'`, `TMOUT=5` and
`CDPATH=/tmp`, idled 7 s at the Stage 1 gate-task prompt, then ran `whoami`,
`pwd`, `date` and `check`: the gate passed (child exit 0). The same script
against the pre-hardening script on `main` fails with
`timed out waiting for input: auto-logout`, so the scrub is what keeps the
shell alive. The operator's real-terminal run of the same command remains
optional.
