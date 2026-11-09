---
title: WP-21 recall shape and Stage 2 grounding — evidence
category: audit
component: sim
status: evidence
version: 0.1.0
last_updated: 2026-11-09
tags: [audit, wp-21, gate, recall, a8]
priority: medium
---

# WP-21 — evidence

Branch `wp/21-recall-shape` from `f8fab62`. Governing text: amendment A8;
sources: `audit/2026-11-09/walkthroughs.md` round 2 (F-019, F-020, O-Z, O-AB,
O-AC, O-AD).

## Harness

Bash 5.3 bundles (committed): `audit/2026-11-09/sim/wp21-all/`,
`wp21-second-try-stage2/`, `wp21-second-try-stage4/`. Bash 3.2.57 runs (`/bin/bash`
first on `PATH`): same commands, `ok`, not committed. `second-try 2`: `Hint:`
twice, the answer-shape line once, the first navigation fact once, one
`not yet:` (oracle-enforced). `cd -` after `cd ..` works under 3.2.57.

Rendered heights (both Bash versions, unchanged from WP-20): 1.1 22, 1.2 18,
1.3 19, 2.2 20, 2.3 22. Heredoc lines: 1.1 18, 2.2 16, 2.3 16 (was 18).

## `normalize_answer` against the real lists

Real function and lists read from `shelltutor`; identical output under 3.2.57,
5.3 and `LC_ALL=C`. The four F-019 negation counterexamples stay rejected.

| Q | typed | normalised | result |
| --- | --- | --- | --- |
| S1 Q3 | `it shows up on the screen` | `it shows up on the screen` | accept |
| S1 Q3 | `it comes back to me on the screen` | `it comes back to me on the screen` | accept |
| S1 Q3 | `back to me, in the window you type into` | `back to me in the window you type into` | accept |
| S1 Q3 | `the window` | `the window` | accept |
| S1 Q3 | `to the screen` | `to the screen` | accept |
| S1 Q3 | `standard out` | `standard out` | accept |
| S1 Q3 (neg) | `not to the screen` | `not to the screen` | REJECT |
| S1 Q3 (neg) | `nowhere, the screen stays blank` | `nowhere the screen stays blank` | REJECT |
| S2 Q1 | `it goes up one level, to the parent folder` | `it goes up one level to the parent folder` | accept |
| S2 Q1 | `Goes up one level to the parent folder.` | `goes up one level to the parent folder` | accept |
| S2 Q1 | `up a level` | `up a level` | accept |
| S2 Q1 | `goes up one!` | `goes up one` | accept |
| S2 Q1 (neg) | `it does not go up one level` | `it does not go up one level` | REJECT |
| S2 Q1 (neg) | `it goes down, not to the parent folder` | `it goes down not to the parent folder` | REJECT |
