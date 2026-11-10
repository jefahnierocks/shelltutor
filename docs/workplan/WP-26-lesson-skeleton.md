---
title: WP-26 — Lesson skeleton: one typeable block, body ≤ 12 rows (consultant §3.7) — drafted
category: planning
component: workplan
status: drafted
version: 0.1.0
last_updated: 2026-11-09
tags: [workplan, lessons, density, content, a11]
priority: medium
---

# WP-26 — Lesson skeleton (content; drafted, not scheduled)

**Governing text**: `docs/design-consultant-response-2026-11.md` §3.7 and
§5.2, adopted in principle by A11; the exact per-lesson rewrites are a
content decision the operator takes lesson by lesson after WP-25 lands.

## Principle
Every lesson: model (≤ 2 lines) · one typeable block of 1–3 commands with
short asides · one "notice" line (≤ 2) · the `▶` line. Body ≤ 12 rows. A
lesson needing two typeable blocks is two lessons. Troubleshooting prose
(command not found, stray slash, missing space) lives once, in 1.2, and on
the ladder, not in every lesson.

## Inputs
WP-25's report lists the screens over budget. For each, this package
proposes the rewrite in the WP as a before/after pair for operator
approval. Findings from the synthetic rounds that a cut would reopen
(O-R stray slash; O-AB `cd..`; F-022 `mkdir` taught in 2.4; F-028 `echo >`
taught in 3.1) must survive in the new location; cite each.

## The practice-folder thread (A12, O-AX)

The rewrites carry this thread; each beat is one or two lines in the
lesson named, within the skeleton.

| Where | Beat | Teaches |
| --- | --- | --- |
| 1.3 (`pwd`) | "The tutor made a folder for you to practise in. Type pwd to see where it is." | where am I; a location has a name |
| 2.1 (tree) | The path `pwd` printed is the full name of the "you are here" folder; every folder in the drawing has one | absolute path; tree and path are the same thing |
| 2.3 (`cd`) | After wandering off, `cd` back by the full name; then `~` as the short name for home (the default folder is `~/.shelltutor`; with `SHELLTUTOR_HOME` set elsewhere the lesson prints the real path, never a hard-coded one) | relative versus absolute; `~` |
| 2.2 (`ls -a`) | The practice folder's own name starts with a dot in the default setup; that is why plain `ls ~` does not show it | hidden names |
| 3.1 | `poem.txt` and `numbers.txt` are files the tutor put there; yours appear beside them | the folder is real; files are things |
| every gate task | One line: "This task runs in <folder>; pwd shows it." (closes O-AG/O-AV) | position before action |
| `env` module (follow-up package) | `echo $SHELLTUTOR_HOME`; the tutor reads a variable to decide where its folder goes | configuration through the environment |

## Evidence
Content changes re-run the synthetic loop (A10: the loop resumes when a
package changes lesson content): one round, all three personas, same
revision, before merge to main is declared done.

## Not yet decided
Which lessons split; whether 1.1's rewrite (§5.2) drops "You'll see hello
printed, then the prompt comes back" (a line the simulated beginners used).
