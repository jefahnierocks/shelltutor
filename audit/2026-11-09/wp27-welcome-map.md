---
title: WP-27 welcome map and vocabulary — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-27, welcome, vocabulary, a12]
priority: low
---

# WP-27 — evidence

Branch `wp/27-welcome-map` from `c206c6c`. Governing text: A12 and
`docs/operator-review-welcome-2026-11-09.md`.

## Harness

`careful-beginner --stage all` is `ok` on Bash 5.3 (bundles
`audit/2026-11-09/sim/wp27-all/`, UTF-8, and `wp27-ascii-all/`, ASCII) and on
3.2.57 (not committed). `compare_heights.py`: 39 screens, identical row counts
between the two forms and between the two Bash versions. The welcome (S1-W) is
21 rendered rows; the 17 box rows are exactly 80 columns in both forms.

## Strings changed ("sandbox" to "practice folder")

| Where | Was | Now |
| --- | --- | --- |
| `-h` usage, `--info` line | `(bash, shell, sandbox, vim, ...)` | `(bash, shell, practice folder, vim, ...)` |
| `-h` | `Sandbox folder: <path>` | `Practice folder: <path>` |
| `--info` label | `Sandbox` | `Practice folder` |
| preflight error | `cannot create the sandbox folder at ...` | `cannot create the practice folder at ...` |
| preflight error | `the sandbox folder exists but is not writable ...` | `the practice folder exists but is not writable ...` |
| finale | `Sandbox stays at <path> ...` | `The practice folder stays at <path> ...` |
| welcome | `its own sandbox folder` and the `Sandbox: <path>` row | box paragraph: `The tutor made a practice folder for you`; row removed |

Left on purpose: the variable `$SANDBOX`, `setup_sandbox`, code comments,
`docs/contracts.md` (except the C-005 label), `CONTRIBUTING.md`, README and
ROADMAP prose. `$SHELLTUTOR_HOME` keeps its name in `--info`. A full stage
walk, both modules, `-h`, `--info` and the argv error paths print "sandbox"
zero times.
