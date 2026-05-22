---
title: shelltutor Contributing
category: process
component: contributing
status: active
version: 0.1.0
last_updated: 2026-05-21
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

Three checks are wrapped in `Makefile` and run locally without external
infrastructure (CI activation is deferred per the GitHub Posture section
below). The intent is a one-command pre-commit verification for
contributors.

```bash
make check       # FF-001 + FF-002 + FF-007 static analysis (always runs)
make lint        # shellcheck shelltutor (FF-005; skips quietly if absent)
make smoke       # FF-006 minimal smoke test (when implemented)
make verify      # check + lint + smoke (full gate)
make self-test   # exercise the checkers against built-in fixtures
```

Each `make` target maps to a single audit fitness function so that a
failure points back to a specific rule. The forbidden-pattern lists
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
| `smoke`              | FF-006          | `./shelltutor -h` runs cleanly and the script's structural invariants hold |

The checkers use `# nofitness:` line annotations for legitimate
exceptions in the script. The Markdown checker skips fenced (` ``` `)
code blocks so that pedagogical examples can demonstrate path shapes
without being flagged.

## Portability Rules

`shelltutor` is **user-agnostic** by contract. A change is a portability
regression if it:

- Requires a specific operator name, hostname, distro, or shell theme.
- Depends on tools beyond `bash` (4+) and a standard POSIX userland.
- Writes outside the script's working directory, asks for elevated
  privileges, or reaches the network.
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
