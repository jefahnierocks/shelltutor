---
title: shelltutor Contributing
category: process
component: contributing
status: active
version: 0.2.0
last_updated: 2026-11-07
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

The quality gates are wrapped in `Makefile` and run locally without network
access or tool installation. Prepare contributor Python 3.11+ and Git 2.56+
first; `make verify` refuses unavailable declaration prerequisites. CI runs the
same gate on every push and pull request. The learner runtime remains Bash-only.

```bash
make check       # FF-001 + FF-002 + FF-004 + FF-007 + FF-008 static analysis (always runs)
make lint        # shellcheck shelltutor (FF-005; skips quietly if absent)
make smoke       # FF-006a minimal static smoke test
make verify      # released manifest check/tests + check + lint + smoke
make manifest-check # declaration only; not a substitute for make verify
make manifest-self-test # declaration-check regression tests
make self-test   # exercise the checkers against built-in fixtures
make lesson-flow # FF-006b PTY harness (optional; Python 3.9+; not in verify)
make sim         # FF-006c five-stage PTY harness (optional; Python 3.9+; not in verify)
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
| `check-portability`  | FF-004          | lesson heredocs do not teach platform-specific paths (`/proc/`, `/sys/`) or platform-specific runtime commands (`free -`, `vm_stat`, `systemctl`, `launchctl`); install hints (`brew install`, `dnf install`, etc.) are allowed by nature; lesson heredocs also do not hardcode the default sandbox path (`~/.shelltutor`, `$HOME/.shelltutor`) — they render `${SANDBOX}` or a relative path — see `scripts/check-portability.sh` |
| `check-posix-tools`  | FF-008          | script code outside lesson heredocs uses no GNU-only text-tool syntax (`sed` repetition/alternation escapes such as `\+` and `\?`, `\L` `\U` `\s` `\w` `\d`, `sed -i`, `grep -P`, `readlink -f`, `date -d`, `stat -c`); `# nofitness:posix` exempts a line — see `scripts/check-posix-tools.sh` |
| `check-governance`   | FF-007          | tracked governance Markdown contains no operator-private absolute paths — see `scripts/check-governance.sh` |
| `lint`               | FF-005          | `shellcheck -s bash -S warning shelltutor` clean (when shellcheck installed) |
| `smoke`              | FF-006a         | `./shelltutor -h` runs cleanly and the script's structural invariants hold |
| `lesson-flow`        | FF-006b         | Optional contributor target. Drives the `scripts/sim/` Python 3.9+ stdlib PTY harness through a persona walkthrough of Stage 1 and emits a v1 evidence bundle (project-local `terminal.jsonl`, `events.jsonl`, `summary.md`, `result.tap`). Skips with a clear message when `python3` is missing or `<3.9`. Not part of `make verify`. Governed by `docs/simulation-design-plan.md`. |
| `sim`                | FF-006c rung 1  | Optional contributor target. Runs `scripts/sim/run.py --stage all`: the `careful-beginner` persona drives all five stages in one PTY run and writes the same v1 evidence bundle, plus mechanical `error-signature` events and a `.progress` assertion. `SIMARGS` passes extra flags (for example `--persona second-try --stage 2`, which fails the first gate check on purpose). Same Python guard as `lesson-flow`; needs a real pseudo-terminal; not part of `make verify`. The non-gating `sim-evidence` workflow runs it on hosted Linux. |

The checkers use `# nofitness:` line annotations for legitimate
exceptions in the script. The Markdown checker skips fenced (` ``` `)
code blocks so that pedagogical examples can demonstrate path shapes
without being flagged.

## Contributor Tooling Floor

The runtime tutor (`shelltutor`) is bash-only and POSIX-userland only,
per AGENTS.md §Authority Levels. Required contributor declaration verification
uses Python 3.11+ (stdlib only) and Git 2.56+; select an already prepared Python
with `make verify PYTHON=/absolute/path/to/python3` and put the prepared Git
first on command-scoped `PATH`. No global tool pin, mise trust, environment
activation or package installation is performed by the gate. The hosted setup
uses Python 3.13.16 and checksum-pinned Git 2.56.0; see
[the preparation and verdict contract](docs/project-manifest.md).

Optional contributor-side tooling
under `scripts/sim/` (FF-006b/FF-006c PTY harness) requires Python 3.9+ —
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
- Uses GNU-only text-tool syntax in script code (`sed \+`, `sed -i`,
  `grep -P`, `readlink -f`, `date -d`, `stat -c`).

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

Owner-directed Specification 1 adoption is the activation trigger for the
`verify` workflow. It runs on push and pull request without path or branch
filters, job conditions or allowed failures. Its source preparation is separate
from actual hosted qualification and branch-protection readback; record those
results in `STATUS.md` before claiming enforcement. No deployment or secrets
are needed. `CODEOWNERS`, PR templates and unrelated automation remain deferred.

`sim-evidence` runs the optional PTY harness on Ubuntu and uploads the bundle
as an artifact. It is evidence capture, not a required check; failures do not
block anything, and artifacts are reviewed by hand before any of them are
committed (intake: `scripts/sim/README.md`).
