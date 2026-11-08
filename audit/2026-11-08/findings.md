---
title: shelltutor — 2026-11-08 Landing Findings
category: audit
component: findings
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, findings, portability, practice-shell, bash-floor]
priority: high
---

# 2026-11-08 — Landing Findings

Surfaced by the operator while landing the 2026-11 cycle (push, hosted
evidence intake, first macOS Phase 2 walk). Recorded here before any fix,
per the findings flow in `docs/simulation-design-plan.md`.

## F-014 — The practice shell is whichever `bash` is first on `PATH`

- **Severity**: 3. The project's Bash 3.2 validation claims rest on the
  practice shell, and the practice shell was not necessarily 3.2.
- **Where**: `practice()` launches `INPUTRC=/dev/null bash --rcfile
  /dev/fd/3 -i …`. The bare `bash` resolves through `PATH`, not to the
  interpreter running the script. On a workstation with Homebrew Bash
  first on `PATH`, `/bin/bash ./shelltutor` renders lessons under 3.2.57
  but every practice prompt (and every gate task) runs under Bash 5.x.
- **Effect**: the 2026-11-08 macOS walkthrough "under Bash 3.2" exercised
  a 3.2 outer script and a 5.x practice shell. The harness avoided this
  only because it puts the chosen Bash first on `PATH`. F-009's fd-3
  rcfile fix was validated the same way, so it is not in doubt; the
  Readline/`bind` behaviour in C-007 is proven on both generations by the
  2026-11-07 pty probe.
- **Fix**: launch the practice shell with `"$BASH"` (the absolute path of
  the running interpreter, set by Bash itself), so the outer script and
  the practice shell are always the same binary. Document in C-007; the
  Phase 2 checklist asks the walker to run `echo $BASH_VERSION` at the
  first practice prompt and record it.
- **Status**: open; fix scheduled in `WP-09`.

## Observations

- **O-F** The hosted-evidence intake grep for home-directory prefixes hits
  lesson 2.3's absolute-path example (a notes file under a fictional
  user's home) on every intake. The intake text should exclude that known
  string. (`WP-09`)
- **O-G** `summary.md` does not record the Bash version that ran the
  tutor; the workflow log does. The harness should capture
  `bash --version` (first line) of the `bash` it will resolve, in run
  metadata. (`WP-09`)
- **O-H** No macOS `--stage all` bundle exists after WP-04/WP-05; the
  `all-slice2` baseline predates the Stage 1 split, so Linux intakes
  compare against stale Stage 1 content. A fresh macOS bundle is needed
  as the like-for-like baseline. (`WP-09`)
- **O-I** `sim-evidence` runs on every push to `main` (about 13 s each)
  and produces an artifact per commit; only reviewed bundles are intaken.
  Acceptable as designed (D-17); the operator may narrow the trigger to
  `workflow_dispatch` later if the noise bothers.
