---
title: Phase A Walkthroughs — summaries
category: audit
component: walkthroughs
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [phase-a, walkthrough, observer, findings, pace]
priority: high
---

# Phase A Walkthroughs

Summaries of observed sittings per `docs/direction-decisions-2026-11.md`
§2 Phase A and the sheet `docs/walkthrough-notes-template.md`. No names,
no transcripts. Phase A exits at three summarised sittings including one
on macOS `/bin/bash` 3.2; the Phase B packages land only after that.

**Status: 1 of 3 sittings recorded.** The 3.2 sitting is still pending.

## Sitting 1 — 2026-11-07, adult with some shell, macOS, Bash 5.3.20

- Platform: macOS 27.0.1, iTerm2 3.7.7. Invoked as `./shelltutor` from
  zsh, so the shebang chose the first `bash` on `PATH`: `echo $BASH_VERSION`
  at the first prompt printed 5.3.20(1)-release. Script revision: the
  post-WP-09 `main` (practice shell follows the outer interpreter).
- Stage 1: 19:22 to 19:29, seven minutes, gate cleared. Stage 2 entered;
  the learner stopped at lesson 2.1 after about eight minutes total,
  having lost interest.
- Observer interventions: one, when the learner had pressed Ctrl+L and
  did not remember that `show` brings the lesson back.
- Ladder rungs seen: not recorded.

### Findings

- **F-015 — The Stage 1 day question invites the whole date.** The
  question reads "What day of the week did `date` show? (Mon, Tue, … — or
  exactly as `date` printed it)" (`shelltutor:877-879`). The learner read
  "exactly as date printed it" as the full `date` line and typed parts of
  it; several `check` rounds followed before `Sat` was accepted. The
  highlighting of `date` in the command colour added to the confusion.
  Severity 3 (gate friction on a clean host). The wording was introduced
  by the F-013 fix (WP-02) to admit localized day names. Fix scheduled in
  WP-10: ask for "just the day" and accept any answer that contains the
  day as a word, so pasting the whole `date` line also passes.

### Observations

- **O-K — Ctrl+L removes the only reminder of the navigation words.**
  After Ctrl+L (taught in lesson 1.2) the screen is empty except the
  prompt; the footer that names `next`, `show`, `prev`, `quit` is gone,
  and this learner did not recall `show`. Mitigation candidate: rebind
  Ctrl+L in the practice rcfile to clear and reprint the footer
  (`bind -x`); see the note below on what was and was not verified. Candidate for WP-11 or WP-12; operator's call.
- **O-L — "The shell is a program" lands as empty words.** Lesson 1.4 says
  terminal, shell and program differ but gives the learner nothing to hold
  the idea with; the observer judged it undemystifying. This is the gap
  the `shells` module (WP-14) addresses in Phase D; whether part of it
  belongs in the core Stage 1 is a curriculum decision for the operator.
- **O-M — Stage 2 names "path", `.`, `..` and `~` before the learner knows
  what a path or a current directory is.** The intro screen presents the
  symbols as a list; the concept of a position in a tree of folders, and
  the difference between a file and a folder in `ls` output, is assumed.
  A conceptual screen before 2.1, or a reordering of Stage 2, is a core
  curriculum change and an operator decision.
- **O-N — `ls -l` output is unexplained.** Lesson 2.1 asks the learner to
  run `ls -l` and the long form (permissions, link count, owner, group,
  size, date, name) is new; the lesson gives one aside. The observer asked
  for a brief introduction and a confirming question. Core change;
  operator decision.
- **O-O — Pace and engagement.** Eight minutes to loss of interest at the
  start of Stage 2, after a seven-minute Stage 1. One sitting is not a
  trend; the next two sittings should record the same moment.

### Note on the Ctrl+L mitigation

`bind -x` (run a shell command on a key) is documented for Bash 3.2 and
later. On 2026-11-08 a pty probe confirmed Bash 5.3.20 registers the
binding (`bind -X` lists it); Bash 3.2 has no `bind -X`, and a keystroke
injected through `script(1)` did not fire the command on either version,
so the probe is inconclusive about the keystroke path. Any package that
adopts the rebinding must prove it with the PTY harness (a raw `\x0c`
action followed by the footer sentinel) on both Bash generations. It is a
C-007 change (a key binding the contract currently avoids) and is recorded
here as a candidate, not scheduled.

## Carry-forward for the next sittings

- Use `/bin/bash ./shelltutor` for the 3.2 sitting and record
  `echo $BASH_VERSION` (F-014 repeat).
- Record which ladder rungs appeared at each gate failure.
- Record the exact answers typed at the Stage 1 day question.
- Watch for the O-O moment: the first screen where attention drops.
