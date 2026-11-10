---
title: WP-27 — Welcome map inside the box; "practice folder" on screen (O-AW, O-AX; A12)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, welcome, chrome, vocabulary, a12]
priority: high
---

# WP-27 — Welcome map and on-screen vocabulary

**Governing text**: amendment A12 and
`docs/operator-review-welcome-2026-11-09.md` (the mock-up there is the
spec). **Tier**: core standard, rendering only. **Touches `shelltutor`**:
the welcome function, `-h`, `--info` labels, any on-screen "sandbox".

## Changes

1. **Welcome** exactly as the review's mock-up: title row; blank; "Five
   stages, each a few short lessons and one task to pass:"; blank; five
   rows `  ○ Stage N   <short title>` (dot grey, `Stage N` grey, title
   plain; a passed stage shows `●` green, read from the saved progress);
   blank; the three-line safety/no-score paragraph; blank; the `▶` line.
   Remove the dots-and-names row and the `Sandbox:` row under the box.
   Box rows are exactly 80 columns in both glyph forms (the review's
   mock-up has ragged right edges from hand editing; pad to the box).
   Total rendered rows ≤ 22 including footer, rule and blank.
2. **Vocabulary**: every learner-visible "sandbox" becomes "practice
   folder" (welcome copy, `-h` "Sandbox folder:" → "Practice folder:",
   `--info` label, error messages a learner sees, any lesson or gate
   line). Variable names, comments, contracts and docs keep `sandbox`.
   Report the list of changed strings and any left on purpose.
3. **ASCII form**: `-`/`#` for the map dots; same rows.

## Harness and records
`sentinels.py` only if a changed string is a sentinel (the welcome title
row is unchanged); `smoke-test.sh` strings for `-h`/`--info`; C-001/C-005
wording in `docs/contracts.md` where they quote the labels; density row
for the welcome; O-AW closed, O-AX closed for its rendering half, in
`audit/2026-11-09/walkthroughs.md`; `STATUS.md` one line.

## Acceptance
`make verify` green; careful-beginner `--stage all` on 3.2 and 5.x in both
glyph forms; `compare_heights.py` identical; the rendered welcome pasted
in the report in both forms, plus the resume form with one stage passed.

## Commits
1. `feat(welcome): course map inside the box, one stage per row; passed stages filled (O-AW)`
2. `fix(copy): "practice folder" on screen; sandbox row off the welcome (O-AX)`
3. `chore(sim): smoke strings; contracts wording; density row; findings; STATUS`
