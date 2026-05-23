---
title: PTY Harness Research for shelltutor
category: research
component: pty-harness
status: draft
version: 0.2.0
last_updated: 2026-05-22
tags: [research, pty, testing, evals, contributor-tooling, planning, verified]
priority: medium
---

# PTY Harness Research for shelltutor

This document ingests the operator-supplied research report
`deep-research-report (10).md` into repo-local planning form. It covers
the driver mechanism decision: how to test an interactive Bash tutor
that reads from `/dev/tty` without weakening the production script's
Bash-only contract.

The source report did not include a concrete bibliography or stable
source URLs; its citations were placeholder tokens from the research
environment. Treat its external claims as design evidence pending source
link cleanup, not as final citation-grade authority.

Reviewer note (2026-05-22): the tool-selection table below mixes
**objective facts** (what each tool does, version, license) with
**judgment** (best-default ranking, contributor-ergonomics opinion).
Objective claims have been spot-checked and corrected; ranking claims
are explicitly opinion and may be overridden by later project decisions.

## Bottom Line

The report recommends keeping `shelltutor` production behavior unchanged
and adding a contributor-only PTY harness for full lesson-flow testing.

Rationale:

- `/dev/tty` is the process's controlling terminal, not ordinary stdin.
- A pseudoterminal lets a driver program interact with a child process
  as though a human were typing at a terminal.
- Expect, Pexpect, and Python's `pty` module are built for this class of
  interactive terminal automation.
- Piping input into the tutor is not representative of the product
  behavior because the tutor intentionally uses a real interactive Bash
  subshell.

Design implication: the first full lesson-flow automation should live in
contributor tooling, not in the production control plane.

## Architecture Comparison

"Planning stance" is opinion; "Status" and "Strength/Cost" are
ground-truth facts as of May 2026.

| Option | Strength (fact) | Cost / risk (fact) | Status as of May 2026 (fact) | Planning stance (opinion) |
| --- | --- | --- | --- | --- |
| Pexpect | High-level PTY control, readable Python, `expect`/`sendline`, timeout handling, transcript logging. | Unix-only for full `spawn()`; bundles `ptyprocess`. | Last release **4.9.0, 2023-11-25**. No 2024–2026 releases; project is not archived but maintenance is effectively stalled. ([PyPI](https://pypi.org/project/pexpect/)) | Workable default if contributor Python dependencies are acceptable, with the understanding that an unmaintained dependency is now a fallback risk. |
| Python stdlib `pty` | No third-party package; exercises PTY semantics. | Lower-level; Unix-only; macOS caveat about mixing `pty.fork()` with high-level APIs. | Current in Python 3.14; no deprecation. ([docs.python.org/3/library/pty.html](https://docs.python.org/3/library/pty.html)) | Reasonable fallback if Pexpect is rejected; harness must reimplement expect/send logic. |
| Expect (Tcl) | Purpose-built terminal automation; long history. | Requires Tcl/Expect runtime. | Last official release **5.45.4, 2018-02-04** — eight years stale. ([core.tcl-lang.org/expect](https://core.tcl-lang.org/expect/index)) | Calling Expect "mature" is fair; calling it "actively maintained" is no longer accurate. Treat as legacy. |
| `script` / shell-only wrappers | Useful for recording and ad hoc manual reproduction. | Not deterministic; util-linux `script(1)` man page explicitly warns against use in pipes. **BSD `script` (macOS) and util-linux `script` are not flag-compatible** — any cross-platform recorder must branch on OS. | Both currently shipped. ([man7 script(1)](https://man7.org/linux/man-pages/man1/script.1.html)) | Supplemental recorder, not primary harness. |
| `socat` PTY mode | Real PTY driver via `pty,raw,echo=0,link=…,waitslave` address. No `expect/sendline` semantics. | Byte-level only; no pattern-matching layer. | Actively maintained. ([man7 socat(1)](https://man7.org/linux/man-pages/man1/socat.1.html)) | Legitimate low-level option; appropriate only if the harness adds its own match/timeout layer. |
| Production `--simulate` | Can be deterministic in constrained CI and bypass PTY complexity. | Creates a second product contract and may test a different path from the learner experience. | Not implemented in shelltutor today. | Add only if desired as a real product feature. |
| Narrative emulator | Useful for curriculum/content review. | Cannot test terminal semantics, shell echo, prompt behavior, completion, Ctrl+C, or `/dev/tty`. | N/A — design idea, not a tool. | Planning aid only, not acceptance evidence. |

## Contributor Dependency Boundary

The report argues that optional test-only dependencies are normal in
mature CLI projects. The relevant pattern is:

- Keep production runtime lean and portable.
- Gate optional contributor tests behind explicit prerequisites.
- Do not change production behavior solely to satisfy test harness
  convenience.

Design implication: a future `make pty-smoke` or `make lesson-flow`
target may be acceptable even if it requires Pexpect, Expect, or another
PTY driver, provided it is documented as contributor tooling and does not
become a runtime requirement for learners.

## Recommended Harness Shape

A first PTY harness should:

- Create a fresh temporary sandbox for each run with `SHELLTUTOR_HOME`.
- Launch `./shelltutor` under a PTY.
- Drive only learner-visible controls and commands.
- Assert against both terminal output and sandbox state.
- Capture a full transcript on failure.
- Normalize terminal output before text assertions.
- Skip clearly when PTY prerequisites are missing.
- Stay single-threaded and simple unless a later design need proves
  otherwise.

Potential Makefile target names:

- `pty-smoke`
- `lesson-flow`
- `sim`

Do not replace the existing `make smoke` minimal FF-006 check with this
until the dependency boundary is explicitly accepted.

## PTY Failure Modes To Design Around

The report calls out these practical failure modes:

- No controlling terminal in CI or cron-like environments.
- `\r\n` line endings from PTY sessions instead of plain `\n`.
- Prompt timing and echo races.
- Canonical-mode line length limits.
- Platform-specific PTY behavior across macOS, Linux, and older systems.
- Lost output near EOF in some PTY implementations.
- Fragile prompt matching when assertions depend on exact cursor or color
  behavior.

Harness requirements implied by those risks:

- Normalize CRLF.
- Use timeouts with useful diagnostics.
- Keep full raw output artifacts.
- Match stable screen text, not brittle incidental formatting.
- Isolate each run's sandbox.
- Treat missing PTY support as a skip, not as a mysterious failure.

## Relationship To `--simulate`

The report does not rule out a production `--simulate` flag. It narrows
the acceptable reason for one.

Acceptable reasons:

- Deterministic demos.
- Documentation generation.
- Accessibility workflow support.
- Fast validator-level checks for pure stage logic.

Weak reason:

- Avoiding PTY testing complexity while claiming coverage of interactive
  learner behavior.

Design implication: if `--simulate` is ever added, document it as a new
contract in `docs/contracts.md`; do not treat it as equivalent to the
real `/dev/tty` path.

## Design Decisions Suggested By This Research

These are planning recommendations, not accepted implementation
decisions:

1. Keep the production script Bash-only and terminal-faithful.
2. Build full lesson-flow testing as contributor-side PTY tooling.
3. Prefer Pexpect for the first implementation if contributor Python
   dependencies are acceptable — but note (May 2026) that upstream
   Pexpect has had no releases since 4.9.0 (2023-11-25), so plan a
   fallback (raw stdlib `pty` + `selectors`, or driving `ptyprocess`
   directly) before pinning the harness to it long-term.
4. Use stdlib `pty` as the dependency-free alternate. Expect (Tcl) is
   credible historically but has not had an official release since
   5.45.4 (2018), so treat it as legacy, not "modern", tooling.
5. Use `script` as a recorder/debugging layer, not the main deterministic
   driver.
6. Add explicit prerequisite/skip behavior for PTY-dependent checks.
7. Keep minimal `make smoke` separate from any future full PTY lesson-flow
   target until the project accepts the broader dependency surface.

## Open Questions For Later Research

- Is Pexpect acceptable as an optional contributor dependency in this
  repository?
- Should a future PTY target live under `scripts/sim/`, `scripts/test/`,
  `tests/`, or dated `audit/<date>/sim/` evidence?
- Should the first PTY target be Stage 1 only or full Stage 1 through
  Stage 5?
- What should be the exact prerequisite/skip message when PTY tooling is
  missing?
- Should FF-006 be split into minimal smoke, lesson-flow smoke, and
  persona simulation subchecks?

