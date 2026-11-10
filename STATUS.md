---
title: shelltutor Status
category: status
component: project-status
status: active
version: 0.6.0
last_updated: 2026-11-09
tags: [status, posture, deferrals]
priority: high
---

# Status

Current truth for the `shelltutor` repository.

## Posture

- **Lifecycle**: pre-release implementation. The five-stage core is complete
  and the 2026-11 work plan has landed. Direction from 2026-11-08:
  `docs/direction-decisions-2026-11.md` (core plus modules; Phases A–D).
  Now in Phase A (human walkthroughs), which also closes ROADMAP Phase 2;
  the Phase 4 release steps (CHANGELOG, `v0.1.0`) follow.
- **Semantic owner**: Jefahnierocks (personal workspace).
- **Current host**: local workstation; GitHub remote at
  `github.com/jefahnierocks/shelltutor` (public).
- **Secrets authority**: none required; the tutor handles no secrets.
- **Review cadence**: ad-hoc until a release cadence stabilizes.
- **PaC status**: local static analysis only — `scripts/check-*.sh`
  driven from `Makefile`; no PaC engine, no enforcing control plane.
- **IaC status**: none — no live infrastructure.
- **Bash floor**: 3.2 (stock macOS `/bin/bash` 3.2.57 satisfies it;
  no install step required on any supported platform).

## What Is True Now

### Current state (2026-11-09)

- The five-stage core, the finale at the screen budget (WP-18) and the modules
  `shells` and `env` are on `main`; recall answers match by exact form or keyword
  groups with a negation guard (WP-23).
- `make check` runs FF-001 to FF-011; the matcher corpus (FF-011) and the hint
  rules (FF-009, FF-010) guard the recall questions.
- Synthetic sittings, rounds 1–5: all three personas reach the finale at `7e126cf`.
  They are candidate evidence only (`audit/2026-11-09/walkthroughs.md`); Phase A's
  human exit (three sittings, one on Bash 3.2) is still open, one of three recorded.
- The synthetic loop is paused (2026-11-09) and resumes only when a package
  changes lesson content (ROADMAP Phase 5); WP-24 landed at `7489d50`.
- Amendment A11 (2026-11-09) adopted the outside design review (chrome v2).
  WP-25 (rendering only) landed at `dd297d2`; WP-26 (lesson skeleton and body
  rewrite) is drafted and is next, with per-lesson approval.
- The identity line is closed: "working in a Unix shell" in the script, the
  harness sentinel and the docs (WP-25). Open: WP-08 part B (CHANGELOG,
  `v0.1.0`), which human sittings gate (A1.10).

### The 2026-11 cycle, in one place

The work plan (`docs/workplan/README.md`, adopted 2026-11-07) ran in the
order observe → fix → harden → shape → verify. Outcome: the tutor's four
known correctness defects are fixed with before/after PTY evidence, the
practice shell is hardened and contracted, Stage 1 is split into four
lessons, every gate escalates feedback without ever auto-passing, and the
documents agree with the code.

| Package | Landed | What it delivered |
| --- | --- | --- |
| WP-01 | `c4f92c5` | Five-stage PTY harness (`make sim`, FF-006c rung 1) and the pre-fix baseline, which showed F-010 and F-011 as transcript evidence. |
| WP-02 | `f4fb671` | F-010 to F-013 resolved; stage-folder model (C-003); `SHELLTUTOR_HOME` normalised (C-004); FF-004 sandbox-path rule and the FF-008 POSIX text-tool checker; post-fix evidence. |
| WP-03 | `4482554` | Slice 2 practice-shell hardening (C-007); the `no-system-rc-preview` variant retired. |
| WP-04 | `a909d4b` | Stage 1 density split: four lessons (1.1 running commands, 1.2 keyboard habits, 1.3 where/who/when, 1.4 what just happened). |
| WP-05 | `ff4248b` | Stage 2 (`cd`) and Stage 4 (`*.txt` glob) verified from practice history; escalating hint/worked-example feedback on every gate; `second-try` persona. |
| WP-06 | `a71ab76` | Non-gating `sim-evidence` workflow for hosted Linux transcripts (commits 1–2); the first hosted run and its evidence commit remain with the operator. |
| WP-07 | this sweep | Documents realigned with the code and with this file; the governance check covers `docs/` and the harness README. |
| WP-08 part A | `7d5065f` | MIT `LICENSE` and the script's SPDX header; part B (CHANGELOG, `v0.1.0` inputs) waits for the Phase 2 results. |
| WP-09 | `bd841ae` | F-014 fixed: the practice shell runs under the outer script's own Bash (`"$BASH"`); the harness records the Bash path and version; post-WP-04/05 macOS baseline `all-current`. |
| WP-12 | `48c8355` | Stage 1 lesson 1.5 (read-only agent beat) and one sentence each in 3.3 and 4.3, net zero lines. |
| WP-14 | `2873636` | Stages 1–2 grounding: 1.4 shows the shell speaking (`dtae`); Stage 2 has four lessons and opens with a drawn tree and `pwd`; `ls -p` replaces `ls -l`; expected-error screens in the harness. |
| WP-18 | `f372da1` | Stages 3–5 and the finale to the screen budget (A5, O-J): every screen at most 18 heredoc lines and 22 rendered rows; 4.3 split (Stage 4 has four lessons), 5.3 split (Stage 5 has five); no command removed, gates unchanged. |
| WP-13 C–D, WP-16 | `486e7ac` | Module entry (`./shelltutor shells`; C-001, C-003), the module standard and screen template in `CONTRIBUTING.md`, identity and non-goals reframed, and the `shells` module. Module bundle `audit/2026-11-08/sim/module-shells/`: macOS only (hosted Linux pending). |
| WP-27 | branch `wp/27-welcome-map` | Welcome map and vocabulary (A12; O-AW, O-AX rendering half): the course map inside the box, one stage per row with a dot each (passed stages green on a retake), the `Sandbox:` row off the welcome, and every learner-visible "sandbox" now "practice folder" (`-h`, `--info`, preflight errors, finale). Bundles `audit/2026-11-09/sim/wp27-*`. |
| WP-25 | `dd297d2` | Screen chrome v2 (A11; consultant response), rendering only: footer above the rule, blank before the prompt, `▶` isolated, 19-row panel budget; header without the product name on lessons and gates, titles without `N.k —`; progressive footer with `(gloss)`; BOLD role (SUB/KEY/DIR out of core bodies); width-stable glyph pairs; recall `┃ N of 3` with a `┃ ? ` prompt (the hint stays on the first miss, A7); `[✓]`/`[ ]` checklist with `seen:`; welcome box and identity line; capability-first cleared screens and finale; "answer in words" on every gate intro. `run.py --ascii`, `compare_heights.py`. Bundles `audit/2026-11-09/sim/wp25-*`. |
| WP-24 | `7489d50` | Matcher tightening after the exit test (A10; F-029, F-030, O-AR, O-AS, O-AT): 36 probe reject rows (FF-011 now 235 cases), one-word groups replaced by lesson phrases, `--ordered` groups for Stage 4 Q2, `--reject` phrases on fifteen questions, parentheses and semicolons normalised, Stage 5 Q2 forms, three screen lines. Bundles `audit/2026-11-09/sim/wp24-*`. |
| WP-23 | `7e126cf` | Keyword matching for recall (A10; F-025..F-028, O-AN): `ask_question` takes exact forms or keyword groups with a negation guard, groups for all 21 questions, FF-009 extended to keyword phrases, six hints reworded, shape line removed, **FF-011** matcher corpus (184 cases) in `make check`; 3.1 teaches `echo hello > notes.txt`. Part C (sitting hygiene) is a6's. Bundles `audit/2026-11-09/sim/wp23-*`. |
| WP-22 | `13847ef` | Stage 2 sequencing and defect fixes (A9; F-021..F-024, O-AG, O-AI, O-AK): 2.4 teaches `mkdir`; the first gate `check` lists both items and needs the folder; `~` and Stage 4 Q1 take the lessons' words; Ctrl+C truth in 1.2, `q` in 3.2's try-it, 3.3 asks to type `cp`/`mv`/`rm`; **FF-010** (every recall hint starts `Lesson N: `) in `make check`, eleven hints reworded. Bundles `audit/2026-11-09/sim/wp22-*`. |
| WP-21 | `5d1d689` | Recall answer shape and small Stage 1–2 grounding (A8; F-019, F-020, O-Z, O-AB, O-AC, O-AD): longer plain forms and punctuation dropped (no containment rule); one fixed answer-shape line from the second miss; typo lines in 1.1/2.3; 2.3 `cd` home and `cd -`; 2.2 `ls /`. Bundles `audit/2026-11-09/sim/wp21-*`. |
| WP-20 | `82792b6` | Stage 1 gate grounding (A7; F-017, F-018, O-P, O-Q, O-S, O-U, O-V): Q1 taught in 1.3 and asked about a normal bash window; plain answers and apostrophes accepted at Q2/Q3; recall ladder hint on miss 1, facts from miss 2; recall in the `┃` block as "answer in words"; 1.1/1.2 mechanical lines. Bundles `audit/2026-11-09/sim/wp20-*`. |
| WP-17 | `6331ff2` | Module `env` (variables, `export`, `PATH`, the prompt): five lessons, a recall gate and an export-and-child task; the persona observes the `PS1` revert across screens. The real `~/.bashrc` and `~/.zshrc` are named in text only. Bundle `audit/2026-11-08/sim/module-env/` (macOS only; hosted Linux pending). |

### Curriculum and tutor

- `shelltutor` is a course in working in a Unix shell, whose five mastery-gated
  stages hand off to `vimtutor`:
  each closing with three recall questions and one practical task, on a
  Bash 3.2 runtime floor (ROADMAP Phase 3 is complete, `9f61570`,
  2026-05-21; Phase 1, the user-agnostic refactor, is complete, `e6257aa`).
- Stage 1 has five lessons, Stage 2 four, Stage 3 three, Stage 4 four and
  Stage 5 five. Stages 1
  and 2 start practice prompts in `$SANDBOX`; stages 3 to 5 start in their
  stage folder (C-003). Fixtures are seeded on stage entry.
- Gates verify the filesystem; Stages 1, 2 and 4 also check the practice
  history. A second miss shows a hint, a third a worked example; nothing
  auto-passes (D-14, C-006).
- The practice shell does not source the system bashrc, resets the
  behaviour-changing variables and fixes the Readline defaults (C-007). The
  Linux before/after comparison for Slice 2 remains pending until the hosted
  run or the operator's Phase 2 Linux session.
- Contracts C-001 to C-007 are in `docs/contracts.md`.
- The tutor was imported from prior-art at `fedora-top:~/Projects/shelltutor`
  (commit `136f6a3`, 2026-05-17); the companion `wyn-setup/` directory is
  intentionally not carried forward.

### Quality gates and fitness functions

- `make check | lint | smoke | verify | self-test` (all offline), plus the
  optional `make lesson-flow` and `make sim` PTY harness targets, which are
  not part of `verify`. All five checker self-test suites pass locally.
- Seven of eight proposed fitness functions are implemented: FF-001 safety,
  FF-002 write-scope, FF-004 lesson portability (now also rejecting a
  hardcoded `~/.shelltutor`), FF-005 shellcheck, FF-006 smoke and PTY harness
  (a, b and c rung 1), FF-007 governance citations (now covering `docs/*.md`,
  `docs/workplan/*.md` and `scripts/sim/README.md`), and FF-008 POSIX
  text-tool portability. FF-003 (STATUS/ROADMAP drift) stays deferred; the
  WP-07 sweep is its manual stand-in and the next audit cycle covers it.
  FF-008 is to be admitted to the catalogue at the next audit cycle.
- `.claude/settings.json` carries a PostToolUse shellcheck hook so Claude
  Code sessions get the FF-005 warning on script edits.
- Last full local gate run, 2026-11-07: `make verify` (24 declaration tests
  plus the static, lint and smoke checks), `make self-test`, and the PTY
  harness (`careful-beginner` across all five stages; `second-try` on stages 2
  and 4) passed under Bash 3.2.57 and 5.3.20 with no `error-signature`
  events. Inside an agent session the manifest check refuses inherited
  `GIT_CONFIG_*` overrides and reports NOT_CHECKED; the work plan's worker
  protocol gives the environment-clearing command that restores the verdict.

### Simulation ladder

- FF-006a static smoke (`make smoke`); FF-006b Stage 1 PTY harness (Slice 1,
  `29dc0d3`); FF-006c rung 1 (`careful-beginner`, five stages, plus
  `second-try` on stages 2 and 4). Slice 2 hardening is complete.
  `confused-novice` and the confusion events (Slice 3) remain deferred. The
  harness is contributor tooling on Python 3.9+ stdlib only
  (`docs/simulation-design-plan.md`, `scripts/sim/README.md`).
- Evidence is under `audit/2026-11-08/` (pre-fix baseline, post-fix,
  Slice 2, Stage 1 split, `second-try`); only synthetic bundles are committed.

### Findings and audit cycles

- First profile and audit cycle complete (snapshot 2026-05-21): see
  `profile/2026-05-21/` and `audit/2026-05-21/SUMMARY.md`. All seven findings
  (F-001 to F-007) closed.
- F-008 (BSD-sed gate verifier, caught by the first PTY baseline) and F-009
  (Bash 5.3 startup hang, Bash 3.2 rcfile loading) are fixed; see
  `audit/2026-05-23/findings.md` and `audit/2026-07-14/findings.md`.
- F-010 to F-013 (stage-5 fixture, hardcoded sandbox path, GNU-sed `\+`,
  English-only day check) surfaced by static review on 2026-11-07 and are
  resolved by WP-02 (`audit/2026-11-07/findings.md`).
- F-014 (the practice shell was whichever `bash` was first on `PATH`, not the
  interpreter running the script) surfaced on 2026-11-08 and is resolved by
  WP-09 (`audit/2026-11-08/findings.md`): `practice()` launches `"$BASH"`, and
  run metadata records `bash_path` and `bash_version`. The 2026-11-08 macOS
  Phase 2 walk did not confirm the practice shell's Bash version, so it should
  be repeated with `/bin/bash ./shelltutor` and `echo $BASH_VERSION` recorded;
  the operator re-records it. The like-for-like macOS baseline is
  `audit/2026-11-08/sim/all-current/`.
- Recall navigation and ladder (WP-10, A1.1-A1.7) landed at `deae605`: `show`/`quit` at
  every recall question and Stage 1 follow-up, one three-rung ladder with fifteen hints
  (re-read against the WP-14 screens), FF-009 hint-leak check in `make check`, F-015 day
  question, pre-task hints removed at stages 2-4, Stage 2 `$HOME` accepted forms fixed.
  Answer-list widening waits for sittings 2 and 3 (A4).
  Evidence: `audit/2026-11-08/sim/wp10-*`.
- Stage-cleared screens (WP-11, A1.4/A3.5) give stages 1-4 a stopping point after each gate
  (`next` continues, `quit` saves and leaves, `show` redisplays); `--info` no longer promises
  a finale hand-off or demo skips; F-016 (Apple's Bash 3.2 notice) is silenced on the
  practice launch line, so Bash 3.2 and 5.x screen heights now match
  (`audit/2026-11-08/wp11-screen-heights.md`, `audit/2026-11-08/sim/wp11-*`).
- Screen chrome (WP-15, amendment A3) is built on `wp/15-screen-chrome`: panel header and
  lower rule, key-hint footer bar, `┃` feedback checklist, ASCII glyph fallback
  (`SHELLTUTOR_ASCII`). Evidence: `audit/2026-11-08/wp15-screen-heights.md` and
  `audit/2026-11-08/sim/wp15-*`.
- The Stage 1 density audit (`audit/2026-05-23/stage1-density.md`) preceded
  the first baseline as required; its follow-up
  (`audit/2026-11-08/stage1-density-followup.md`) records the WP-04 split.

### Declaration and license

- Root `project.yaml` follows Specification 1 and projects this file as a
  public-available, linkable working prototype. Required operational state is
  `unverified`; it makes no deployed-system claim. The development check points
  to `scripts/verify-project.sh`, which delegates to the existing `make verify`.
- Owner-directed adoption source is prepared with the public immutable Release 1
  bundle and separate bootstrap. Contributor Python/Git prerequisites are
  separate from the Bash/POSIX learner runtime. Hosted qualification, adoption
  acceptance and effective branch enforcement remain pending; local source
  validation is not runtime acceptance.
- **License**: MIT, SPDX id `MIT`, `Copyright (c) 2026 Jefahnierocks`
  (operator decision and copyright line of 2026-11-07). `LICENSE` is at the
  repo root and `shelltutor` carries the SPDX header. Distribution is
  unchanged: clone + run. No `CHANGELOG.md` yet (see Deferrals).
- Day-1 documentation set (`README.md`, `CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`) plus `docs/contracts.md` is in
  place.

### Design record

- `docs/design-description.md` (2026-11-08) is the formal design baseline:
  game-design, software, user-journey and pedagogy lenses, a glossary, the
  design tensions the framing exposes, and which claims are backed by
  evidence under `audit/`. Descriptive only.
- `docs/direction-decisions-2026-11.md` (directive, 2026-11-08) answers the
  eight direction decisions (D1–D8), sets Phases A–D and the two evidence
  tiers (core standard, module standard), and schedules the identity,
  contract and curriculum edits by phase. `docs/design-direction-2026-11.md`
  is superseded by it and kept as the record of intent. No tutor or contract
  change has been made yet on its account; the first are WP-10 to WP-12 in
  Phase B.

### Synthetic sittings (A6, 2026-11-09)

- With no human learners available, AI-played learner personas
  (`docs/sim-personas/`) will walk the real tutor through a project-owned
  pseudo-terminal (WP-19) and record `docs/walkthrough-notes-sim-template.md`
  sheets. Their findings are candidates until a maintainer reproduces them;
  Phase A's human exit still stands.

## Immediate Next Steps

1. **WP-26 — lesson skeleton and body rewrite**
   (`docs/workplan/WP-26-lesson-skeleton.md`; drafted): per-lesson approval,
   then one synthetic round as its evidence.
2. **WP-08 part B — release prep**: `CHANGELOG.md` and the `v0.1.0` inputs. The
   tag waits for human evidence (A1.10): the Phase A sittings (one on macOS
   `/bin/bash` 3.2 with `echo $BASH_VERSION` recorded) and the Phase 2 items that
   need a person (Debian/Ubuntu walk, no-TTY negative test, the
   `LC_ALL=de_DE.UTF-8` day check).
3. **Module standard going forward**: modules `shells` and `env` are in;
   `processes` and `permissions` follow only after two human walks of both
   (`docs/direction-decisions-2026-11.md` §4), under the module standard in
   `CONTRIBUTING.md`.

## Deferrals

| Deferred surface | Reason | Trigger to revisit |
|------------------|--------|--------------------|
| `CHANGELOG.md` | Nothing released yet; no tagged history | First tagged release (WP-08 part B) |
| Second profile and audit cycle | The direction decisions' corollary: no further analytical documents this cycle; the design baseline stands in | After Phase D, or a recurring drift finding |
| Items deferred by the direction decisions (lessons as source files, `processes`/`permissions` modules, tmux/Emacs concept screens, module progress, timing store) | Each has a stated reopening condition | `ROADMAP.md` Phase 5, deferred table |
| `CODEOWNERS`, PR templates and unrelated GitHub automation | Not needed by the declaration migration | A project-specific need |
| Hosted `verify` qualification and branch enforcement | Specification 1 adoption supplies the activation trigger; source is prepared | Actual hosted checks and effective protection readback |
| Cross-platform CI | Hosted cross-platform *acceptance* remains deferred; `sim-evidence` captures Linux transcripts only and is non-gating | When manual validation stops scaling |
| Slice 3 personas and confusion events (`confused-novice`, mechanical confusion triggers) | The two implemented personas cover the gate and escalation surfaces; confusion modelling needs stable evidence first | After the Phase 2 results |
| FF-003 (STATUS/ROADMAP drift heuristic) | Periodic audit cycles and the manual WP-07 sweep cover it better than a fuzzy CI check | A recurring drift finding |
| Package distribution (Homebrew tap, AUR, etc.) | Single-file script; install is `clone + run` | If users ask for managed install |

## Blockers

- None.

## Decision-Disagreement Rule

If `STATUS.md`, `ROADMAP.md`, and `CONTRIBUTING.md` disagree about
project-level posture, fix the disagreement here first; downstream
documents defer to this file for current truth.
