---
title: WP-06 — Hosted Linux evidence capture (non-gating sim workflow)
category: planning
component: workplan
status: ready
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, ci, simulation, linux, evidence]
priority: medium
---

# WP-06 — Hosted Linux evidence capture (non-gating sim workflow)

**Depends on**: WP-01. **Blocks**: the Linux before/after comparison in
WP-03. **Touches `shelltutor`**: no. **Operator gate**: **yes** — adding a
workflow is "sensitive work" (deployment configuration) under `AGENTS.md`.
The operator approved this package on 2026-11-07 (Decision line below);
it may start as soon as WP-01 has landed on `main`.

**Decision**: Approved: 2026-11-07 (operator, in session).

## Goal

Capture the five-stage `careful-beginner` transcript on a Debian-family
Bash 5.x host without waiting for a human Linux session, as evidence the
operator reviews and commits by hand. The workflow is not a gate, does not
affect `verify`, and claims nothing about acceptance.

## Read first

- `docs/workplan/README.md` decision D-17.
- `.github/workflows/verify.yml` (style: pinned runner, read-only
  permissions, `persist-credentials: false`).
- `CONTRIBUTING.md` §GitHub Posture; `STATUS.md` deferral row
  "Cross-platform CI".
- `docs/sim-slice-2-sketch.md` §Reordering (why a Linux baseline matters).

## Change 1 — Workflow

`.github/workflows/sim-evidence.yml`:

```yaml
name: sim-evidence

on:
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  sim:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6
        with:
          persist-credentials: false
      - name: Record host inputs
        run: |
          bash --version | head -1
          python3 --version
          for c in vim man less; do printf '%s: %s\n' "$c" "$(command -v "$c" || echo missing)"; done
          locale || true
      - name: Five-stage careful-beginner walk (evidence only, never a gate)
        continue-on-error: true
        run: python3 scripts/sim/run.py --stage all --variant current-rc -v --out sim-out
      - name: Upload evidence bundle
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: sim-evidence-${{ github.sha }}
          path: sim-out
          retention-days: 30
```

If the first run shows `skip-man-missing` or a `MAN_LS` timeout, add
`sudo apt-get update && sudo apt-get install --no-install-recommends -y man-db`
before the walk and note it in the summary. The runner's Python 3.12
satisfies the harness floor; do not add `setup-python`.

## Change 2 — Intake procedure (documented in `scripts/sim/README.md`)

1. Download the artifact for the run.
2. Read `summary.md` and `events.jsonl`; confirm `gate_passed=true`,
   `progress_after=absent`, and list any `error-signature` events.
3. Copy the bundle to `audit/<UTC-date>/sim/all-linux/current-rc/` and
   add a two-line provenance note (run id, runner image, Bash version)
   to that directory's `summary.md` under "Provenance".
4. Commit as `chore(audit): Linux five-stage evidence from hosted run <run-id>`.
5. Compare against the same-revision macOS bundle with
   `scripts/sim/compare.py`; record the signature (if any) in
   `audit/<date>/findings.md` as an observation.

## Records

- `CONTRIBUTING.md` §GitHub Posture: one paragraph — "`sim-evidence`
  runs the optional PTY harness on Ubuntu and uploads the bundle as an
  artifact. It is evidence capture, not a required check; failures do not
  block anything, and artifacts are reviewed by hand before any of them
  are committed."
- `STATUS.md` deferral "Cross-platform CI": reword to "Hosted
  cross-platform *acceptance* remains deferred; `sim-evidence` captures
  Linux transcripts only."
- `docs/project-manifest.md`: no change (the declaration maps only
  `check`).

## Acceptance criteria

1. Workflow runs green on `workflow_dispatch`; artifact downloads; TAP
   `ok`.
2. The `verify` workflow is untouched.
3. Intake procedure executed once, with the first Linux bundle committed.

## Commits

1. `ci(sim): non-gating sim-evidence workflow (Ubuntu, artifact upload)`
2. `docs(sim): hosted evidence intake procedure; STATUS deferral wording`
3. `chore(audit): Linux five-stage evidence from hosted run <run-id>`

## Report

Template in `docs/workplan/README.md`; include the run URL and the
`compare.py` signature summary.
