---
title: WP-09 — Landing follow-ups (F-014 practice-shell interpreter, harness provenance, baseline)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-08
tags: [workplan, practice-shell, harness, evidence, f-014]
priority: high
---

# WP-09 — Landing follow-ups

**Depends on**: WP-07 (landed). **Touches `shelltutor`**: yes, one line in
`practice()`. **Operator gate**: none. Source:
`audit/2026-11-08/findings.md` (F-014, O-F, O-G, O-H).

## Changes

1. **F-014.** In `practice()`, replace the bare `bash` in the launch line
   with `"$BASH"`, keeping everything else byte-identical:
   `INPUTRC=/dev/null "$BASH" --rcfile /dev/fd/3 -i 3<<RCFILE < /dev/tty`.
   Add one comment line above it: the practice shell is the same binary
   as the outer script, never whatever `bash` is first on `PATH`. In
   `docs/contracts.md` C-007, change the first sentence to say the
   practice shell is started as `INPUTRC=/dev/null "$BASH" --rcfile …`
   and add a row "Interpreter | `$BASH`, the binary running the outer
   script". In `docs/phase2-walkthrough-checklist.md`, under "How to run
   a stage walkthrough", add step 0: invoke the tutor with the Bash under
   test explicitly (`/bin/bash ./shelltutor` for 3.2), and at the first
   practice prompt run `echo $BASH_VERSION` and record it in the STATUS
   line. Also state that a bare `./shelltutor` resolves `#!/usr/bin/env
   bash` through `PATH`.
2. **O-G.** Harness: in `run_meta`, record `bash_path` (`shutil.which("bash")`
   under the child's `PATH`) and `bash_version` (first line of
   `bash --version` from that path). Print both in `summary.md` Run
   metadata. The hosted `sim-evidence` "Record host inputs" step may stay.
3. **O-F.** `scripts/sim/README.md` intake step: pipe the pre-commit
   grep through a `grep -v` that excludes the exact example path shown in
   `stage2_lesson_3` (the notes file under the fictional user's home), with
   one sentence explaining why. Put the command in a top-level fenced
   block so the governance checker skips it.
4. **O-H.** Run `python3 scripts/sim/run.py --stage all --variant current-rc`
   on macOS under Bash 5.x and once with `/bin/bash` first on `PATH`
   (outside the sandbox), after change 1, and commit the Bash 5.x bundle
   as `audit/2026-11-08/sim/all-current/current-rc/` (or the next UTC
   date's `sim/all/`). Confirm the recorded `bash_version` differs
   between the two runs, which is the proof of F-014's fix. Compare the
   new bundle against `all-linux/current-rc` and note the result in the
   commit body: Stage 1 content should now match.
5. `audit/2026-11-08/findings.md`: F-014 resolved with the short SHA;
   O-F/O-G/O-H marked done. `STATUS.md`: one landing line, plus correct
   the 2026-11-08 macOS walkthrough line to say the practice shell's Bash
   version was not confirmed and the walk should be repeated after this
   fix (the operator re-records it).

## Acceptance

1. `make verify` green (use the protocol wrapper); smoke structural
   invariants hold; ShellCheck clean.
2. Harness `--stage all` green on both Bash generations with
   `bash_version` recorded and differing between the runs.
3. `grep -c ' bash --rcfile' shelltutor` is 0 and `"$BASH" --rcfile` is 1.
4. Governance checker clean on every doc touched.

## Commits

1. `fix(practice): run the practice shell with the same bash as the outer script (F-014)`
   — includes C-007 and checklist text.
2. `feat(sim): record bash path and version in run metadata; intake grep excludes the lesson example`
3. `chore(audit): post-WP-04/05 macOS five-stage baseline; resolve F-014`
