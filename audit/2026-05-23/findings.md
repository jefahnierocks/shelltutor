---
title: shelltutor — 2026-05-23 Simulation Findings
category: audit
component: findings
status: active
version: 0.1.0
last_updated: 2026-05-23
tags: [audit, findings, simulation, ff-006b, stage1, portability]
priority: high
---

# 2026-05-23 — Simulation Findings (Slice 1 PTY Harness)

Findings surfaced by the Slice 1 `careful-beginner` PTY harness
(FF-006b) during its first `current-rc` baseline run on macOS stock
`/bin/bash` 3.2.57. Per `docs/simulation-design-plan.md` §Findings
Flow, severity 3 or 4 items also get a one-line current-truth entry
in `STATUS.md`; lower severity stays here unless release-blocking.

## F-008 — Stage 1 gate verifier broken on BSD sed (macOS)

- **Severity**: 4 (release-blocking — Stage 1 gate unpassable on
  macOS, the project's tagline-supported platform).
- **Surfaced by**: Slice 1 `careful-beginner` harness on the first
  `current-rc` baseline run; identical failure on
  `no-system-rc-preview`. Both variants exited 4
  (`SentinelNotFoundError`, sentinel `Stage 1 cleared.` never
  observed within the 30s timeout).
- **Root cause**: `shelltutor:737-741` normalizes the learner's
  day-of-week answer with `sed 's/\(.\)\(.\)\(.\)/\1\L\2\L\3/'`. The
  `\L` lowercase-modifier is a GNU sed extension. BSD sed (macOS
  `/usr/bin/sed`) renders `\L` as the literal letter `L`, so input
  `"Sat"` (after the prior tr → all-uppercase: `"SAT"`) becomes
  `"SLALT"` — five characters. The verifier at `shelltutor:627`
  compares against `$(date +%a)` (three characters, e.g. `"Sat"`).
  **No 3-character input can satisfy the comparison on macOS.**
- **Demonstration**:
  ```
  $ echo "Sat" | sed 's/\(.\)\(.\)\(.\)/\1\L\2\L\3/'
  SLaLt     # macOS BSD sed (literal L; original chars otherwise unchanged)
  Sat       # GNU sed (\L lowercases subsequent characters)

  $ echo "sat" | tr '[:lower:]' '[:upper:]' \
      | sed 's/^\(...\).*/\1/' \
      | sed 's/^./&/; s/\(.\)\(.\)\(.\)/\1\L\2\L\3/'
  SLALT     # macOS BSD sed — full pipeline
  Sat       # GNU sed — full pipeline
  ```
- **Provenance**: introduced in commit `9f61570`
  (`feat(curriculum)!: rewrite as five mastery-gated stages`,
  2026-05-21); silent in the codebase for two days. The
  curriculum-redesign commit's "verified under macOS stock
  `/bin/bash` 3.2.57" claim was about script parsing and lesson
  rendering, not gate completion.
- **Fix**: replace the second `sed` call with `awk`'s POSIX
  `toupper`/`tolower`/`substr` to produce title-case:
  ```
  | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}'
  ```
  Verified against BSD sed (macOS Darwin 25.5.0) and GNU sed (any
  Linux). Compatible with bash 3.2+ on all supported platforms; no
  dependency change.
- **Validation needed**: re-run `make lesson-flow` on macOS stock
  `/bin/bash` 3.2.57 and confirm both Stage 1 baselines reach
  `Stage 1 cleared.` and exit 0. ROADMAP Phase 2 manual walkthrough
  should also explicitly exercise the Stage 1 gate-task
  day-of-week answer to confirm.
- **Audit cross-references**:
  - Cite IDs for the fix commit: `FF-004` (lesson portability),
    `FF-006b` (first finding from the new harness).
  - Prior-art analogue: `F-003` (lesson-7/lesson-8 `/proc` and
    `dnf` portability). F-008 is a different surface (script-side
    rather than lesson-content) but the theme is the same:
    single-file portability across Linux and macOS.
- **Status**: fixed in the same commit that introduces this
  findings file (see commit body).

## Side observation — `/etc/bashrc` leak signature not observed

The plan predicted that comparing `current-rc` against
`no-system-rc-preview` on Stage 1 would expose a `/etc/bashrc` leak
signature. On this operator's host (Apple Silicon, macOS 15.5,
Darwin 25.5.0), the two baseline transcripts diverge only on:

- the per-run random sandbox UUID embedded in lesson copy that
  references `$SANDBOX`;
- the `date` command's output between back-to-back runs.

There is no visible system-rcfile-driven divergence in the
transcript content on this host. The Slice 2 practice-shell
hardening recommendation in the plan still stands — sourcing
`/etc/bashrc` is brittle by nature regardless of whether this
particular host leaks — but the hardening's user-visible payoff is
host-dependent. A re-run on a Linux host with a banner-emitting
`/etc/bashrc` (typical of distro-managed systems) would surface the
predicted signature. This is logged here as a positive null
observation, not a finding.

## Re-run plan

After the F-008 fix lands on `main` and the worktree branch
fast-forwards, the Slice 1 harness is re-run from the worktree.
Expected outcome: both baselines pass (gate_passed=true) and emit
TAP `ok`. Re-captured evidence replaces the failing bundle from the
first attempt; nothing red is committed to `audit/2026-05-23/sim/`.

## Re-cited from the harness for completeness

The Slice 1 harness recorded the failure end-to-end and wrote
truthful red `summary.md` + `result.tap` bundles for both variants
before raising at the parent. The post-fix re-run produces a green
replacement bundle in the same commit that lands the harness,
preserving the project's record-then-act discipline without
committing red baselines.
