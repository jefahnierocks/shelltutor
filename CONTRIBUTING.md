---
title: shelltutor Contributing
category: process
component: contributing
status: active
version: 0.1.0
last_updated: 2026-07-14
tags: [contributing, verification, change-discipline]
priority: medium
---

# Contributing

Use focused changes and keep the tutor, its lessons, and its documentation
aligned.

## Change Discipline

- **Conventional Commits**: `type(scope): description`. Common types:
  `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.
- One coherent change per commit. Do not bundle unrelated edits.
- Linear history. No merge commits.

## Local Verification

```bash
./shelltutor
```

Walk the affected stage surface. If you cannot run the tutor (no bash 3.2+,
unsupported terminal, etc.), state that verification is pending rather than
implying success.

## Quality Gates

The quality gates are wrapped in `Makefile` and run locally without external
infrastructure (CI activation is deferred per the GitHub Posture section
below). The intent is a one-command pre-commit verification for
contributors.

```bash
make check       # FF-001 + FF-002 + FF-004 + FF-007 static analysis (always runs)
make lint        # shellcheck shelltutor (FF-005; skips quietly if absent)
make smoke       # FF-006a minimal static smoke test
make verify      # check + lint + smoke (full gate)
make self-test   # exercise the checkers against built-in fixtures
make lesson-flow # FF-006b PTY harness (optional; Python 3.9+; not in verify)
```

Each enforcement target maps to one or more named audit fitness functions so
that a failure points back to a specific rule. The forbidden-pattern lists
live in the scripts themselves (canonical source); the descriptions
here are deliberately patternless so this document stays consistent
with the rules it describes.

| Target               | Rule (audit ID) | What it enforces |
| ---                  | ---             | --- |
| `check-safety`       | FF-001          | the script does not invoke privilege-escalation, network, or remote-shell commands at runtime (lesson heredocs are exempt) — see `scripts/check-safety.sh` for the pattern list |
| `check-safety`       | FF-002          | every write target resolves to a path under `$SANDBOX` or `$PROGRESS_FILE`; system paths are blocked — see `scripts/check-safety.sh` |
| `check-portability`  | FF-004          | lesson heredocs do not teach platform-specific paths (`/proc/`, `/sys/`) or platform-specific runtime commands (`free -`, `vm_stat`, `systemctl`, `launchctl`); install hints (`brew install`, `dnf install`, etc.) are allowed by nature — see `scripts/check-portability.sh` |
| `check-governance`   | FF-007          | tracked governance Markdown contains no operator-private absolute paths — see `scripts/check-governance.sh` |
| `lint`               | FF-005          | `shellcheck -s bash -S warning shelltutor` clean (when shellcheck installed) |
| `smoke`              | FF-006a         | `./shelltutor -h` runs cleanly and the script's structural invariants hold |
| `lesson-flow`        | FF-006b         | Optional contributor target. Drives the `scripts/sim/` Python 3.9+ stdlib PTY harness through a persona walkthrough of Stage 1 and emits a v1 evidence bundle (project-local `terminal.jsonl`, `events.jsonl`, `summary.md`, `result.tap`). Skips with a clear message when `python3` is missing or `<3.9`. Not part of `make verify`. Governed by `docs/simulation-design-plan.md`. |

The checkers use `# nofitness:` line annotations for legitimate
exceptions in the script. The Markdown checker skips fenced (` ``` `)
code blocks so that pedagogical examples can demonstrate path shapes
without being flagged.

## Contributor Tooling Floor

The runtime tutor (`shelltutor`) is bash-only and POSIX-userland only,
per AGENTS.md §Authority Levels. Optional contributor-side tooling
under `scripts/sim/` (FF-006b PTY harness) requires Python 3.9+ —
syntax and stdlib use must not exceed that floor so the harness runs
without a venv whenever Python 3.9+ is installed on macOS or Linux.
Third-party Python dependencies (Pexpect, pytest, etc.) are not
adopted; the harness is stdlib only by design.

## Portability Rules

`shelltutor` is **user-agnostic** by contract. A change is a portability
regression if it:

- Requires a specific operator name, hostname, distro, or shell theme.
- Depends on tools beyond `bash` (3.2+) and a standard POSIX userland.
- Makes the tutor's own code write outside its configured sandbox, asks for
  elevated privileges, or reaches the network.
- Assumes a particular `$HOME` layout, prompt, or pre-existing
  configuration.

If a lesson genuinely requires a non-portable surface, gate it on a runtime
check and degrade gracefully — do not couple the script's default path to
the non-portable surface.

## Evidence Rules

- When importing or porting material from prior-art (e.g.,
  `fedora-top:~/Projects/shelltutor`), cite the source path and commit SHA
  in the commit body.
- Keep planned, prototyped, and implemented lesson states separate in
  `ROADMAP.md` and `STATUS.md`.

## Secrets

Do not commit secrets, credentials, account identifiers, or private personal
data. The tutor is public and must remain safe to run on any stranger's
machine.

## GitHub Posture

Following the Jefahnierocks workspace posture, this repository intentionally
omits CI workflows, `CODEOWNERS`, PR templates, branch protection, and
Actions secrets until a real activation trigger exists. Until then, local
commit discipline is the enforcement layer.
