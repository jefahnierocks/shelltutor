---
title: shelltutor Audit — Phase 10 Fitness Functions
category: audit
component: phase-10-fitness-functions
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-10, fitness-functions]
priority: high
---

# Phase 10 — Fitness Function Candidates

Seven future-state safeguards. Per directive §10.2 these are
independent from findings; cross-references appear in both directions
but IDs do not overlap (`F-NNN` vs `FF-NNN`). Per directive Phase 10.5
exit boundary, any fitness function whose enforcement tech is not
installable is demoted to `manual-review-only`; for shelltutor's
no-CI posture every static-analysis candidate is enforceable as a
pre-commit hook or `Makefile` target, so none are demoted on
infrastructure grounds.

CI activation per the workspace posture (CONTRIBUTING.md:72-75) is
deferred. The fitness functions below are written for adoption now via
pre-commit / Makefile / manual-review channels and for future
adoption via GitHub Actions when the posture trigger fires.

| ID | Title | Category | Related findings | Bucket |
| --- | --- | --- | --- | --- |
| FF-001 | Safety-rule static analysis (no `sudo` / `setuid` / `chmod +s` / network in script) | static-analysis | F-004 | safety-rule-enforcement |
| FF-002 | Write-scope static analysis (every write targets `$SANDBOX` or `$PROGRESS_FILE`) | static-analysis | F-004 | safety-rule-enforcement |
| FF-003 | Documentation-code drift check (STATUS/ROADMAP next-steps vs git log) | companion-doc-drift | F-001 | documentation-consistency |
| FF-004 | Lesson portability check (gate-and-fallback per CONTRIBUTING.md:51-54) | static-analysis | F-003 | lesson-portability |
| FF-005 | `shellcheck shelltutor` clean pass | static-analysis | F-006 | static-analysis |
| FF-006 | Lesson-flow smoke test (non-interactive run; final `.progress` check) | eval-coverage | F-006 | lesson-flow-smoke |
| FF-007 | Avoid absolute machine-local paths in governance citations | companion-doc-drift | F-005 | governance-citation-portability |

---

## FF-001 — Safety-rule static analysis on `shelltutor`

| Field | Value |
| --- | --- |
| Rule | The tracked `shelltutor` script must not contain any of: `sudo` (as a command, not as text inside a heredoc that demonstrates it to the learner); `setuid`; `chmod +s`; `curl`; `wget`; `nc ` (word-boundary); `ssh ` (word-boundary); `http://`; `https://` — **outside** explicitly annotated educational heredocs. |
| Enforcement category | `static-analysis` |
| Scope | `shelltutor` (the script file only, not the lesson heredocs that demonstrate `sudo dnf install` as install advice) |
| Failure condition | `grep -nE '^[^#]*\b(sudo\|setuid\|chmod \\+s\|curl\|wget\|nc\\b\|ssh\\b\|https?://)' shelltutor` returns a hit on a line that is not inside a `lesson*() { lesson <<EOF ... EOF }` heredoc *and* is not annotated `# nofitness:safety-rule`. |
| Implementation notes | One `bash` script + `grep` would be sufficient. Could live as `scripts/check-safety.sh` invoked from a pre-commit hook or `Makefile` target. No external dependency beyond standard POSIX userland — consistent with AGENTS.md:75-78. The annotation `# nofitness:safety-rule` allows explicit exceptions (e.g., the lesson 8 dnf install hint) without disabling the check. |
| Related findings | F-004 |

The harder edge case is the lesson 8 install hint
(`shelltutor:346` — `sudo dnf install cowsay figlet lolcat`). Strict
reading would flag it. The check should permit it via a comment
annotation **and** Phase 4 / Phase 1 should resolve the lesson surface
question (F-003) so that the hint is either properly gated or rewritten.

---

## FF-002 — Write-scope static analysis on `shelltutor`

| Field | Value |
| --- | --- |
| Rule | Every write target in the script must resolve to a path inside `$SANDBOX` or `$PROGRESS_FILE`. |
| Enforcement category | `static-analysis` |
| Scope | `shelltutor` |
| Failure condition | An automated check flags any of these patterns that resolve to a path outside `$SANDBOX`: `mkdir`, `touch`, `cat >`, `seq ... >`, `echo ... >`, `printf ... >`, `tee`, `>>`, `cp`, `mv`, `rm`. Current expected hits: `mkdir -p "$SANDBOX"`, four file writes inside `$SANDBOX`, one `echo > $PROGRESS_FILE`, one `rm -f $PROGRESS_FILE` — all should pass. |
| Implementation notes | The check needs minimal bash AST understanding (or a regex that resolves `$SANDBOX` and `$PROGRESS_FILE` references). For initial implementation, a simpler check: `grep -nE '(^|\\s)(mkdir\\b\|touch\\b\|cp\\b\|mv\\b\|rm\\b\|tee\\b\|>\\b\|>>\\b)' shelltutor` and verify every match's target line contains `$SANDBOX` or `$PROGRESS_FILE`. |
| Related findings | F-004 |

---

## FF-003 — Documentation-code drift check

| Field | Value |
| --- | --- |
| Rule | `STATUS.md` items labeled "Immediate Next Steps" and `ROADMAP.md` items in the *current* phase must not name work whose commit message already appears in `git log` for the current branch. |
| Enforcement category | `companion-doc-drift` |
| Scope | `STATUS.md` § "Immediate Next Steps"; `ROADMAP.md` § (current Phase) |
| Failure condition | Any "Immediate Next Steps" bullet matches (case-insensitive substring) a subject in `git log --pretty=%s` for HEAD. Example present-day match: STATUS.md item "User-agnostic refactor commit" vs git log "e6257aa refactor: remove user-specific accent branding from tutor". |
| Implementation notes | Bash + `grep` + `git log`. The matching is fuzzy; a strict implementation would maintain a `nofitness:drift` annotation for items that intentionally describe a *completed* state. A simpler implementation: pre-commit hook that errors if STATUS.md or ROADMAP.md was edited but the corresponding commit-log subjects aren't reflected. |
| Related findings | F-001 |

The matching heuristic is the hard part. An initial pass can be
manual-review-only (the audit explicitly suggests this pattern for the
remediation of F-001), then promoted to automated check once the
matching pattern stabilizes.

---

## FF-004 — Lesson portability check

| Field | Value |
| --- | --- |
| Rule | Every lesson heredoc command line that references a non-portable surface (`/proc`, `/sys`, `free`, `apt`, `dnf`, `yum`, `pacman`, `brew install`, `port install`, `vm_stat`, `top` with Linux-only flags) must be paired with a runtime gate-and-fallback per `CONTRIBUTING.md:51-54`. |
| Enforcement category | `static-analysis` (or `prompt-scan` — but lesson heredocs are not LLM prompts; static-analysis is the truer label) |
| Scope | `shelltutor` lesson functions (lines 152-409) |
| Failure condition | `grep -nE '(/proc/|/sys/|\\bfree\\b\|\\bdnf\\b\|\\bapt\\b\|\\byum\\b\|\\bpacman\\b\|\\bbrew install\\b\|\\bport install\\b\|\\bvm_stat\\b)' shelltutor` returns a match inside lesson heredoc text that is not paired with a nearby `command -v ... 2>/dev/null` gate or equivalent fallback narration. |
| Implementation notes | Initial implementation could be manual-review-only (lesson surface is small and stable). Promote when ROADMAP Phase 3 ("Lesson Surface Review") begins adding new lessons. |
| Related findings | F-003 |

---

## FF-005 — `shellcheck shelltutor` clean pass

| Field | Value |
| --- | --- |
| Rule | `shellcheck shelltutor` must exit zero. Any suppression must be inline (`# shellcheck disable=SC...`) with a one-line justification comment immediately above the suppression. |
| Enforcement category | `static-analysis` |
| Scope | `shelltutor` |
| Failure condition | `shellcheck shelltutor` exits non-zero, or any suppression lacks a justification comment. |
| Implementation notes | Listed as ROADMAP Phase 2 exit criterion (`ROADMAP.md:64`). `shellcheck` is not a bash-only dependency — but `CONTRIBUTING.md:34-38` recognizes it as "if available," and it is a standard developer-side tool not packaged with the runtime. Implementation: `Makefile` target `check: shellcheck shelltutor`, or a pre-commit hook for contributors who have `shellcheck` installed. CI activation, when it comes, picks this up. |
| Related findings | F-006 |

---

## FF-006 — Lesson-flow smoke test

| Field | Value |
| --- | --- |
| Rule | `shelltutor` must complete a full lesson sequence non-interactively in under N seconds (N to be tuned; initial budget 5s) and leave `$SANDBOX/.progress` removed on success. |
| Enforcement category | `eval-coverage` (closest fit; the test is behavioral not "eval" in the LLM sense, but the directive enum does not include "smoke-test" as a separate category) |
| Scope | end-to-end shelltutor invocation |
| Failure condition | The test driver pipes `next\n` (11 times) into the practice subshell's controlling tty via a pseudo-tty (or a bash sub-process that simulates the rcfile environment) and observes: (a) the script exits zero, (b) `$SANDBOX/.progress` does not exist at the end, (c) all 11 lesson headings appear on stdout. Any of (a)/(b)/(c) failing → smoke-test failure. |
| Implementation notes | This is the hardest of the seven to implement because `practice()` reads from `/dev/tty`. A test harness needs a pseudo-tty (e.g., `expect`, `python pty`, or `socat`). For Day-1, a simpler smoke test could run `./shelltutor -h` and verify exit code zero and known help text — minimal coverage but no pty harness needed. Promote to full lesson-flow test in a later cycle once `expect`/`pty` infrastructure is acceptable per AGENTS.md:75-78 dependency rule. |
| Related findings | F-006 |
| Demotion candidate | If `expect` / `python pty` cannot land within AGENTS.md:75-78 ("bash and a standard POSIX userland"), this FF demotes to `manual-review-only` for full lesson-flow and to `static-analysis` for the `-h` minimal version. |

---

## FF-007 — Avoid absolute machine-local paths in governance citations

| Field | Value |
| --- | --- |
| Rule | Tracked governance files (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`, `README.md`) must not contain absolute filesystem paths beginning with `/Users/`, `/home/`, `/root/`, `C:\\`, or similar operator-private prefixes. |
| Enforcement category | `companion-doc-drift` |
| Scope | the six governance files |
| Failure condition | `grep -nE '(/Users/\|/home/\|/root/\|C:\\\\)' ...` returns a match. |
| Implementation notes | One-line `grep`. Trivial. Could run as pre-commit hook. |
| Related findings | F-005 |

---

## Out-of-Scope (recorded but not proposed at this cycle)

The following are potential fitness functions named in the directive
but not proposed for shelltutor now because the underlying surface is
absent:

- `protocol-contract-registry` — no MCP/A2A/workflow surface
- `authority-manifest` — no agent runtime to declare; the AGENTS.md
  approval gates are governance, not a runtime manifest
- `approval-matrix` — covered by AGENTS.md governance; no agent
  runtime to check
- `memory-lifecycle-lint` — only `$SANDBOX/.progress` lifecycle
  matters; covered (loosely) by FF-002 write-scope
- `telemetry-lint` — no telemetry
- `provenance-attestation` — release posture deferred per ROADMAP
  Phase 4; revisit when release pipeline opens
- `adr-template` — no ADRs; ROADMAP does not call for them; revisit if
  the project adds ADRs
- `release-gate` — release posture deferred; revisit at ROADMAP Phase 4
- `eval-coverage` for agent-mediated paths — vacuous
- `dependency-boundary` — covered by AGENTS.md:75-78 + FF-001/FF-002
  combination
- `policy-as-code` — would require a non-bash dependency (e.g., OPA);
  conflicts with AGENTS.md:75-78
- `prompt-scan` — no LLM prompts

These categories remain available for promotion in a future cycle if
the corresponding surface emerges.

## Boundary Declarations Honored (Phase 10 fitness-function side)

- Did not propose a fitness function whose enforcement tech does not
  exist for the project's stack. Every FF above relies on `bash` + `grep`
  + POSIX userland, with `shellcheck` (FF-005) and `expect`/`pty`
  (FF-006) as exceptions that the FF-006 entry explicitly addresses.
- Named enforcement category and scope and failure condition for each.
- Did not collapse findings (F-NNN) and fitness functions (FF-NNN).
- Did not write `SUMMARY.md` before Phase 10.5 (still to come).
