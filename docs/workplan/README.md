---
title: shelltutor Work Plan — 2026-11 cycle
category: planning
component: workplan
status: active
version: 0.1.0
last_updated: 2026-11-07
tags: [workplan, decisions, worker-protocol, cycle-2026-11]
priority: high
---

# Work Plan — 2026-11 cycle

**Cycle status (2026-11-08):** WP-01 to WP-07, WP-09 and WP-08 part A have
landed; WP-08 part B waits on the Phase 2 results. New work follows
`docs/direction-decisions-2026-11.md` (Phases A–D, amendment A1); its
packages WP-10 onward are written in this directory in the same form, under
the evidence tier that document assigns them. The A1.9 freeze was lifted by
amendment A4 on 2026-11-08: Phase B packages land in the order WP-15,
WP-11, WP-12, WP-14, WP-10 as each passes review; sittings 2 and 3 observe
the updated script.

This directory is the executable plan for the current cycle of
`shelltutor` work. It was prepared on 2026-11-07 at revision `b2fdff7`
after a full read of the repository, a reproduction of four latent defects
(`audit/2026-11-07/findings.md`), and a measurement of the baseline gates.
It exists so that an implementation agent with less context can complete
each package without re-deriving decisions.

Two layers live here:

- **This README** — the worker protocol (binding), the decision log
  (binding for this cycle), the dependency order, the operator decisions
  still pending, and the report template.
- **`WP-NN-*.md`** — one self-contained package per unit of work: goal,
  what to read first, exact code and copy where the choice is subtle,
  acceptance criteria, validation commands, the ordered list of commits.

`AGENTS.md` remains the governing contract. If a package conflicts with
it, or with `docs/contracts.md`, stop and report rather than choose.

## Packages

| WP | Title | Depends on | Operator gate | Status |
| --- | --- | --- | --- | --- |
| [WP-01](WP-01-five-stage-harness.md) | Five-stage PTY harness (FF-006c rung 1); pre-fix baseline | — | none | **landed** c4f92c5 (2026-11-07) |
| [WP-02](WP-02-tutor-correctness-fixes.md) | Tutor correctness fixes F-010–F-013; stage-folder model; FF-008 checker | WP-01 | none | **landed** f4fb671 (2026-11-07) |
| [WP-03](WP-03-practice-shell-hardening.md) | Practice-shell hardening (Slice 2, C-007) | WP-01, WP-02 | none | **landed** 4482554 (2026-11-07) |
| [WP-04](WP-04-stage1-density.md) | Stage 1 density split (lessons 1.1–1.4) | WP-03 | none | **landed** a909d4b (2026-11-07) |
| [WP-05](WP-05-gate-feedback.md) | Gate verification alignment; escalating feedback; `second-try` persona | WP-01, WP-02 | none | **landed** ff4248b (2026-11-07) |
| [WP-06](WP-06-ci-sim-evidence.md) | Hosted Linux evidence capture (non-gating workflow) | WP-01 | **yes** — approved 2026-11-07 | **landed** a71ab76 (commits 1–2); hosted run + commit 3 with the operator |
| [WP-07](WP-07-doc-realignment.md) | Documentation realignment sweep | WP-02–WP-05 | none | **landed** eb15e41 (2026-11-07) |
| [WP-09](WP-09-landing-followups.md) | Landing follow-ups: F-014 practice-shell interpreter, harness provenance, fresh macOS baseline | WP-07 | none | **landed** bd841ae (2026-11-08) |
| [WP-15](WP-15-screen-chrome.md) | Screen chrome: panel rules, header with stage dots, key-hint footer, `┃` feedback checklist, ASCII fallback (A3) | — | none | **landed** 9c4452a (2026-11-08) |
| [WP-14](WP-14-stages-1-2-grounding.md) | Stages 1–2 grounding: the shell made visible, Stage 2 opens with position, `ls -p` (A2) | WP-15 | none | **landed** 2873636 (2026-11-08) |
| [WP-10](WP-10-recall-navigation-ladder.md) | Recall navigation, one three-rung ladder, hint-leak check, `second-try` recall misses, Phase A answer widening | Phase A summary | none | **landed** deae605 (2026-11-08); answer widening waits for sittings 2–3 |
| [WP-11](WP-11-stage-cleared-screens.md) | Four stage-cleared screens, `--info` wording fixes, D-19 redaction | Phase A summary | none | **landed** 732f9a3 (2026-11-08; includes the F-016 banner fix) |
| [WP-12](WP-12-agent-aware-beat.md) | Read-only lesson 1.5; two sentences in 3.3 and 4.3 | Phase A summary | none | **landed** 48c8355 (2026-11-08) |
| [WP-16](WP-16-module-shells.md) | Module `shells` (D1): three lessons, recall gate, zsh-lookup task | WP-13, WP-10 | none | **landed** 486e7ac (2026-11-08); Linux bundle 036948a |
| [WP-17](WP-17-module-env.md) | Module `env` (D2): five lessons, recall gate, export-and-child task | WP-13, WP-16 | none | **landed** 6331ff2 (2026-11-08); Linux bundle 036948a |
| [WP-13](WP-13-module-infrastructure.md) | Module entry by name, module standard, harness tables and screen-height check | WP-10, WP-14 | none | **landed**: A–B f47fa01, C–D 486e7ac (2026-11-08) |
| [WP-18](WP-18-stages-3-5-to-budget.md) | Stages 3–5 and the finale trimmed or split to the 22-row budget (O-J, A5) | — | approved 2026-11-08 | **landed** f372da1 (2026-11-08) |
| [WP-19](WP-19-synthetic-sittings.md) | Synthetic sittings: sitting server/client, three learner personas, telemetry sheet (A6) | — | none | **landed** d0faa48 (2026-11-09) |
| [WP-20](WP-20-stage1-gate-grounding.md) | Stage 1 gate grounding: Q1 taught, plain answers, hint on first recall miss, recall as the tutor, 1.1/1.2 traps (A7) | — | approved 2026-11-09 | **landed** 82792b6 (2026-11-09) |
| [WP-21](WP-21-recall-shape-and-stage2-grounding.md) | Recall answer shape, Q3/Stage 2 Q1 long forms, typo lines, 2.3 home/`cd -`, `ls /` (A8) | — | approved 2026-11-09 | **landed** 5d1d689 (2026-11-09) |
| [WP-22](WP-22-stage2-sequencing-and-hint-rule.md) | Stage 2 teaches mkdir and checks both items; `~` and Stage 4 Q1 forms; Ctrl+C/`q`; FF-010 hint anchors (A9) | — | approved 2026-11-09 | **landed** 13847ef (2026-11-09) |
| [WP-23](WP-23-keyword-matching.md) | Keyword-group matching with negation guard; FF-011 corpus; shape line removed; 3.1 redirection; harness hygiene (A10) | — | approved 2026-11-09 | **landed** 7e126cf (2026-11-09) |
| [WP-24](WP-24-matcher-tightening.md) | Matcher tightening after the exit test: false accepts, ordered groups, F-030 forms, three screen lines (A10) | — | approved 2026-11-09 | ready |
| [WP-08](WP-08-release-prep.md) | LICENSE (MIT, decided 2026-11-07), CHANGELOG, v0.1.0 inputs | operator inputs | **yes** | part A **landed** 7d5065f; part B blocked on Phase 2 results |

Loop paused 2026-11-09 after the exit test (synthetic sittings round 5, A10 item 4);
it resumes only when a package changes lesson content.

Execution order: WP-01 → WP-02 → WP-03 → WP-04, with WP-05 after WP-02
(it is independent of WP-03/WP-04 and may run in parallel on its own
branch), WP-06 any time after WP-01 (approved), WP-07 last, WP-08 part A
once the copyright line is confirmed and part B after the Phase 2 results.
One worker session per package.

Not in this cycle: the human five-stage Phase 2 walkthroughs (operator;
`docs/phase2-walkthrough-checklist.md`), the second profile and audit
cycle (follows Phase 2 closure), a second simulation persona beyond
`second-try` (Slice 3), any production `--simulate` mode, runtime command
blocking.

## Worker protocol (binding)

1. **Read** `AGENTS.md`, this README, your package, and the files your
   package lists under "Read first". Nothing else is required. Do not
   re-derive context that these files already settle.
2. **Branch** in a linked worktree from current `main`:
   `git worktree add .claude/worktrees/wp-NN -b wp/NN-<slug> main`
   (`.claude/worktrees/` is gitignored). Work only there.
3. **Commit** exactly the commits your package lists, in order, as
   Conventional Commits. Bodies cite the finding and fitness-function IDs
   the package names. No unrelated edits, no formatting sweeps, no
   dependency additions. Learner runtime stays Bash 3.2+ and POSIX
   userland; contributor Python stays 3.9+ stdlib for `scripts/sim/`.
   Commits are signed through the workstation's SSH agent; inside an
   agent sandbox `git commit` can fail with an agent "Operation not
   permitted" error. Run that commit outside the sandbox. Never change
   the signing configuration or pass `--no-gpg-sign`.
4. **Validate before every commit** and again before reporting:
   - `make check lint smoke` and `make self-test` — Bash-only gates.
   - `make verify` — adds the Specification 1 declaration checks. Inside
     an agent session, Git configuration overrides injected into the
     environment make the manifest check refuse with `NOT_CHECKED`
     (exit 2). Run it as:

     ```sh
     env -u GIT_CONFIG_PARAMETERS -u GIT_CONFIG_COUNT -u GIT_CONFIG_KEY_0 -u GIT_CONFIG_VALUE_0 \
         -u GIT_CONFIG_KEY_1 -u GIT_CONFIG_VALUE_1 -u GIT_EDITOR -u GIT_SSH_COMMAND make verify
     ```

     In a linked worktree also set `SHELLTUTOR_GIT_COMMON_DIR` to the main
     checkout's `.git` directory (see `docs/project-manifest.md`).
   - The harness commands your package names. They need a pseudo-terminal;
     if `pty.openpty` fails in a sandbox, run them outside it or report
     "harness not run". `make self-test` may also fail in a sandbox that
     denies `mktemp`'s directory; same rule.
   - Never report a gate as passed that you did not run. State exactly
     which Bash versions you exercised.
5. **Evidence**: only synthetic harness bundles are committed, only under
   `audit/<UTC-date>/sim/`, only when green. A red run is a finding: write
   it in `audit/<date>/findings.md`, fix it if your package covers it,
   re-run, commit the green bundle. Never commit a human transcript.
6. **Do not** push, merge, rebase onto other branches, tag, or touch
   `.github/`, `project.yaml`, `vendor/`, `.claude/settings*.json`, or
   `.codex/` unless your package says so. The operator fast-forwards
   `main` after review (linear history).
7. **Stop and report** instead of guessing when: a package instruction
   conflicts with `AGENTS.md` or `docs/contracts.md`; a validation fails
   for a reason outside your package; a lesson-copy or safety-claim choice
   arises that the package does not settle; anything would broaden the
   tutor's safety surface.
8. **Report** with the template at the end of this file.

## Starting a worker

Branch names follow the file names: `wp/01-five-stage-harness`,
`wp/02-tutor-correctness-fixes`, `wp/03-practice-shell-hardening`,
`wp/04-stage1-density`, `wp/05-gate-feedback`, `wp/06-ci-sim-evidence`,
`wp/07-doc-realignment`, `wp/08-release-prep`.

Paste this into a fresh implementation session, changing the package
name and branch:

```text
You are implementing one work package in the shelltutor repository.
Read AGENTS.md, then docs/workplan/README.md and follow its worker protocol
and decision log, then read docs/workplan/WP-01-five-stage-harness.md and the
files it lists under "Read first". Execute WP-01 completely on branch
wp/01-five-stage-harness in a linked worktree under .claude/worktrees/.
Make exactly the commits the package lists, in order. Run every validation
it names and report with the README's template. Do not push, merge or tag.
Stop and report if anything conflicts with AGENTS.md or docs/contracts.md,
or if a validation fails for a reason outside the package.
```

When the report arrives: read it against the package's acceptance
criteria, run `make verify` on the branch yourself, fast-forward `main`
(`git merge --ff-only wp/NN-<slug>`), remove the worktree, update the
status column in the table above and the `STATUS.md` landing line if the
package did not, then start the next package.

## Decision log (binding for this cycle)

Each decision records what was chosen and why. A package that wants to
deviate must say so in its report and get operator approval first.

- **D-01 Order: observe → fix → harden → shape → verify.** The design
  plan's "observe before harden" rule is applied to the whole cycle. The
  five-stage baseline (WP-01) is captured on the unfixed script so F-010
  and F-011 appear as transcript evidence; fixes (WP-02) and hardening
  (WP-03) follow with before/after bundles; lesson shaping (WP-04) and gate
  changes (WP-05) come after their surfaces have a baseline.
- **D-02 Harness coverage model.** FF-006c rung 1 is one persona
  (`careful-beginner`) across all five stages. The persona types the
  print-and-exit commands each lesson lists (curated in WP-01) and drives
  full-screen programs only where the lesson is about them. It never
  improvises. A persona that fails a gate on purpose (`second-try`,
  WP-05) exists only to observe the first rung of escalating feedback;
  `confused-novice` and confusion events remain Slice 3.
- **D-03 Harness controlled inputs.** `LC_ALL=C`, `VIMINIT='set
  nocompatible'`, `PAGER=less`, `MANPAGER` and `LESS` unset, `TERM`
  defaulted, `COLUMNS`/`LINES` forced to the PTY geometry, and (added
  2026-11-07 during WP-01) `HOME` set to an empty per-run temporary
  directory, because a pre-existing `~/.shelltutor` on the host hid F-011. Reason:
  sentinel strings for Vim (`-- INSERT --`), `man` and `date` are
  locale- and configuration-dependent; a deterministic persona needs
  deterministic programs. Everything else stays a recorded host input.
  The summary lists controlled inputs separately so reviewers do not read
  them as learner conditions.
- **D-04 Stage-folder model.** Stages 1 and 2 start every practice prompt
  in `$SANDBOX`; stages 3, 4 and 5 start lessons and gates in
  `$SANDBOX/stageN`. `setup_stage_dir N` runs on stage entry and seeds
  what that stage's lessons reference (`stage4/poem.txt`,
  `stage4/seed.txt`, `stage5/practice.txt`). Reason: F-010 — lesson copy
  must describe the folder the learner is actually in; Stage 2's teaching
  about `~` and `cd` back to the sandbox needs the sandbox itself.
- **D-05 Sandbox references in copy.** Lesson text never contains the
  literal `~/.shelltutor` or `$HOME/.shelltutor`; it renders `${SANDBOX}`
  or uses a relative path. Enforced by an FF-004 rule, because a Markdown
  "never" is not a boundary.
- **D-06 Locale.** Gate verifiers that compare against `date` output
  accept both the C-locale and the current-locale `%a`/`%A` forms,
  case-insensitively, ignoring a trailing period. Reason: F-013; the tutor
  is user-agnostic and may not assume an English locale. The practice
  shell's locale is not changed (capture, do not control).
- **D-07 POSIX text tools in script code, enforced.** F-008 and F-012 are
  the same defect class. A new fitness function FF-008 and checker
  `scripts/check-posix-tools.sh` forbid GNU-only `sed`/`grep`/`date`/
  `stat`/`readlink` syntax in script code, wired into `make check` and
  `make self-test`. The lesson heredocs are out of its scope (FF-004
  covers them).
- **D-08 `SHELLTUTOR_HOME` normalisation.** Made absolute against the
  invoking directory and stripped of trailing slashes at startup. Reason:
  observation O-C; the Stage 1 `pwd` comparison and the FF-002 write-scope
  claim both assume a canonical path.
- **D-09 Practice-shell contract (C-007).** Keep `--rcfile /dev/fd/3`
  (F-009). Stop sourcing `/etc/bashrc`. Put `INPUTRC=/dev/null` in the
  child's environment and apply Readline settings with `bind` in the
  rcfile (verified on Bash 3.2.57 and 5.3.20). Unset `CDPATH`,
  `GLOBIGNORE`, `HISTIGNORE`, `HISTCONTROL`, `HISTTIMEFORMAT`, `TMOUT`,
  `BASH_ENV`, `PROMPT_COMMAND` (then set it), and the function
  `command_not_found_handle`; `set -o emacs`, `shopt -s histappend`,
  `shopt -u cdspell`; set `PS1` and `PS2`. Do not touch `PATH`, `TERM`,
  `COLUMNS`, `LINES`, locale. Accept that Debian-family Bash reads
  `/etc/bash.bashrc` before the rcfile (only `--norc` prevents it, and
  `--norc` also disables `--rcfile`); document it in C-007 instead of
  claiming isolation. Reason: observations O-D and O-E; the plan's
  hardening sequence; `HISTIGNORE`/`TMOUT` can break the Stage 1 gate on a
  real learner's machine regardless of any `/etc/bashrc` leak.
- **D-10 Tab/bell copy lands with the hardening.** `bell-style none`
  makes lesson 1.1's "bash beeps" sentence false, so the one-line copy fix
  ships in the same commit as the Readline contract. This overrides
  `docs/sim-slice-2-sketch.md`'s "separate commit" recommendation: a
  lesson must never be false at any commit, and a one-line diff is
  trivially attributable in the transcript comparison.
- **D-11 Preview variant retired.** After Slice 2 the `/etc/bashrc` line
  no longer exists, so `no-system-rc-preview` has no target. The patcher
  is removed, `--variant` accepts only `current-rc`, and before/after
  comparisons use `scripts/sim/compare.py` on committed bundles. Slice 1
  bundles stay as history.
- **D-12 Hardening does not wait for a Linux baseline.** The sketch
  recommended capturing the Linux leak signature first. The scrub list in
  D-09 has standalone correctness value, and the macOS null signature is
  already known. The Linux comparison is captured when WP-06 or the
  operator's Phase 2 Linux session provides it, and recorded then.
- **D-13 Stage 1 renumbered to four lessons.** 1.1 running commands
  (`echo`, words, quoting), 1.2 keyboard habits (Tab, Up, Ctrl+L and
  `clear`, Ctrl+C), 1.3 where/who/when (trimmed: `clear` block removed,
  Stage 2 forward-reference softened), 1.4 what just happened. Plain
  renumbering, not "1.1a/1.1b", because learners read the numbers. The
  ROADMAP Phase 3 spec is amended in a dated subsection, not rewritten.
- **D-14 Gate verification follows the ROADMAP spec, scaled to the task
  as taught.** Stage 2 requires at least one `cd` in practice history
  (the screen asks for one); Stage 4 requires the `*.txt` glob in history.
  A shared helper gives every history check the Stage 1 "Almost — you
  still need to" shape. All gates escalate on repeated failure
  (restatement → hint → worked example) and never auto-pass, per the
  design plan.
- **D-15 Evidence must not carry operator-private paths.** Summaries
  record the tutor path relative to the repository root; sandbox roots are
  temporary directories. FF-007's rule covers governance files; its intent
  covers committed evidence too.
- **D-19 Host user name redacted from committed harness artifacts.**
  (Decisions amendment A1.8, D9, 2026-11-08.) The harness cannot control
  `whoami`, so the login name reaches `terminal.jsonl`, `events.jsonl` and
  `summary.md`. The bundle writer treats it as a host input, like temp
  paths, and replaces it with the fixed token `[user]` before writing any
  committed file. Lands before, or in the same series as, the first new
  bundle (WP-11). Existing bundles are not rewritten unless the operator
  says so: a login name is not a credential.
- **D-16 License is the operator's decision.** Decided 2026-11-07: MIT.
  WP-08 remains parameterised on the copyright line and the human Phase 2
  results. No worker executes it before those
  lines are filled in; no worker tags.
- **D-17 Hosted Linux evidence is capture, not acceptance.** A separate
  non-gating workflow uploads a harness bundle as an artifact; the
  operator reviews and commits by hand. `verify` is untouched. Required
  operator approval because it changes CI configuration; approved
  2026-11-07.
- **D-18 One package, one worker, one branch; the operator merges.**
  Linear history is preserved by fast-forwarding reviewed branches onto
  `main`. Workers never push.

## Operator decisions

- **O-1 License** (D-16): **decided 2026-11-07 — MIT**, copyright line
  `Copyright (c) 2026 Jefahnierocks` confirmed the same day. WP-08 part A
  is ready.
- **O-2 WP-06 approval** (D-17): **approved 2026-11-07**, recorded in
  WP-06.
- **O-3 Welcome/orientation safety sentence.** The welcome screen states
  the tutor never writes outside `${SANDBOX}`; the sentence that practice
  prompts run with the learner's ordinary account authority (the F-002
  closure wording in ROADMAP Phase 3) now lives only in `README.md`.
  **Resolved 2026-11-08 (A3.8): yes.** The welcome carries the sentence
  "Commands you run yourself have your full authority: this is the real
  thing, not a simulation"; lands in WP-15.
- **O-4 Linux host for Phase 2.** The human Debian/Ubuntu walkthrough is
  still the Phase 2 closure gate; WP-06 only supplies transcripts.

## Baseline measured on 2026-11-07 (revision `b2fdff7`)

- `make verify` passes (24 declaration tests; FF-001/002/004/007 clean;
  ShellCheck clean; smoke clean) when run with the Git overrides cleared
  as in the protocol; `make self-test` passes.
- Stage 1 PTY harness: `current-rc` and `no-system-rc-preview` green
  under `/bin/bash` 3.2.57 and Bash 5.3.20 (macOS, Apple Silicon).
- `./shelltutor < /dev/null` exits 1 with the documented preflight text.
- Hosted `verify` succeeded on the `main` push of `b2fdff7`.
- Local tooling present: vim and vimtutor on `PATH`, ShellCheck, Python
  3.13, Git 2.56.0.

## Report template

```
WP-NN — <title>
Branch: wp/NN-<slug> at <short-sha> (N commits, listed below)
Bash versions exercised: <e.g. 3.2.57, 5.3.20>
Gates: make check lint smoke = pass|fail; make self-test = pass|fail|not run (why);
       make verify = pass|fail|not run (why)
Harness: <commands run> → <TAP lines>; bundles committed under <path>
Acceptance criteria: <each numbered criterion → met | not met (why)>
Deviations from the package or the decision log: <none | list>
Findings surfaced: <none | F-nnn pointers>
Left for the operator: <none | list>
Commits:
  <sha> <subject>
```
