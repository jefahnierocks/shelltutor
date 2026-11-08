---
title: shelltutor Contributing
category: process
component: contributing
status: active
version: 0.2.0
last_updated: 2026-11-08
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
make check       # FF-001 + FF-002 + FF-004 + FF-007 + FF-008 + FF-009 static analysis (always runs)
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
| `check-hints`        | FF-009          | for every `ask_question` call, no accepted answer appears in the hint (case-insensitive); the call has exactly one prompt, one hint and at least one accepted form, one argument per line; `show`, `quit` and `exit` are never accepted forms — see `scripts/check-hints.sh` |
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

## Screen Chrome

Every tutor screen is a panel between two rules (A3, `docs/direction-decisions-2026-11.md`):
a header rule with the stage dots and position, a blank, the heredoc content,
a lower rule, then the practice shell's footer bar and prompt. `show_screen`
draws the header and lower rule; the runners set `PANEL_STAGE` and `PANEL_POS`
first. The chrome costs two rows over a bare screen, so heredoc content is at
most 19 rows and authored to 18 (22 rendered rows before the prompt). Rules
are built by a loop at a fixed 80 columns; never `tr` on a multibyte glyph or
`${s:0:n}`, and never `tput`. Use the glyph variables (`${G_PLAY}`, `${G_OK}`, ...),
not literal `▶` or `✓`; ASCII substitutes are selected by the plain-text path or
`SHELLTUTOR_ASCII=1`, never by locale. Gate feedback goes through `fb_ok`,
`fb_todo` and `fb_note`.
The lesson-screen template is under Module Standard below.

## Module Standard

New curriculum ships as a **module** under this standard, not the core
standard (`docs/direction-decisions-2026-11.md` §0, §5). A module is entered by
name (`./shelltutor shells`), stands alone, requires nothing passed and saves
nothing.

A module **requires**:

1. One function block in the script (intro, lessons, verifiers, gate,
   runner) following the stage pattern, and a line in `MODULES`.
2. Fixtures under `$SANDBOX/<module>/` if any, seeded and self-healing.
3. Screens that fit the 20-line budget (authored to 18 heredoc lines under
   the chrome) and end in a `▶` line; headings are the harness sentinels.
4. One gate: three recall questions with the recall ladder, plus a task
   verified from state or history where the content allows one.
5. One persona table (lesson count, gate actions) in
   `scripts/sim/persona.py` (`MODULE_TABLES`).
6. One green harness run on the contributor's macOS and one on hosted Linux
   via the existing non-gating workflow; `result.tap` and `summary.md`
   committed, the rest of the bundle not.
7. The static gates FF-001 to FF-008 green.
8. A three-line entry in `STATUS.md`.

A module **does not require**: a density audit, a work-package report, a
comparison summary, a findings file unless a run goes red, a full committed
evidence bundle, or a ROADMAP amendment. It stays at this standard unless the
operator folds it into the core line. Writing a module reads `AGENTS.md`,
this section and one existing stage block as a model, not the whole script.

**Heading convention** (binding; the harness derives its sentinels from it):

| Screen | Heading |
| --- | --- |
| intro | `MODULE — <name>: <title>` |
| lesson `k` | `<name> <k> — <title>` |
| gate (opening screen; no `▶` line, the first question follows) | `<name> — gate` |
| task | `<name> — task` |
| cleared | `✓ <name> cleared.` |

Module screens are height-checked by the harness's `screen-height` events;
a module author counts by hand only when the harness is unavailable.

**Lesson-screen template** (one idea per screen; two concepts or two distinct
actions is a split candidate):

```
<heading in H1 colour>                      # the sentinel

<one idea, in two to six lines of plain prose>

  <command>        # <what it will print or do>
  <command>        # <aside>

<optional: one line beginning "Notice that">

▶ <the one thing to do>, then type next.
```

Recall questions go through `ask_question "<prompt>" "<hint>" <accepted>...`;
no accepted answer may appear in its hint (case-insensitive), and none is one
or two characters. Every command a module demonstrates must exist in the base
install on macOS and Linux; other programs get a concept screen and
`command -v <name>` (D6).

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
