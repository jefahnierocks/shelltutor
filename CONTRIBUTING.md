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
make check       # FF-001 + FF-002 + FF-004 + FF-007 + FF-008 + FF-009 + FF-010 + FF-011 static analysis (always runs)
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
| `check-hints`        | FF-009          | for every `ask_question` call, no accepted answer appears in the hint (case-insensitive), and, since A10, no keyword-group phrase appears in it as whole words; the call has exactly one prompt, one hint and at least one accepted form, one argument per line; `show`, `quit` and `exit` are never accepted forms — see `scripts/check-hints.sh` |
| `check-hints`        | FF-010          | the hint of every `ask_question` call starts `Lesson N: ` or `Lesson N.k: ` (colour variables ignored). A hint says where the fact was taught and names the concept; it never paraphrases the answer, because a paraphrase invites the learner to type it back and FF-009 then forbids accepting it — same script, `scripts/check-hints.sh` |
| `check-matching`     | FF-011          | the recall matcher corpus: `scripts/selftest-matching.sh` sources the real `normalize_answer` and `recall_matches` and the 21 `ask_question` calls from `shelltutor`, then checks every line of `scripts/matching-corpus.tsv` — correct answers from the rejected-answer tables of rounds 1–4 must be accepted; distractors from a question's option text and the negation counterexamples must be rejected. A new recall question needs its key in the script and corpus lines (the call count is asserted) |
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

Every tutor screen is a panel between a header and a lower rule, with the
practice shell below it (A3, A11; `docs/design-consultant-response-2026-11.md`).
`show_screen [MODE]` draws, in order: the header, a blank, the body, a blank,
the `▶` line, a blank, the footer, the lower rule and a blank row; the prompt
follows. The `▶` line is the body's last paragraph and always has one blank
row above and below it. The footer sits above the rule, so everything below
the rule is the real shell. The header is `── Stage N · <title> ──…── ●◉○○○  N.k ──`
(`gate` or `task` in place of `N.k`); the product name leads it only on the
welcome, orientation, stage-intro, cleared and finale screens. Lesson titles
carry no `N.k —` prefix. The runners set `PANEL_STAGE` and `PANEL_POS` first.

**Budget.** The panel (header through rule) is at most 19 rows; the harness
counts 20 rendered rows (the blank under the rule included), so the prompt
lands on row 21 of a 24-row terminal. The harness fails a core stage run when
a screen passes the budget (the welcome box may take one more row). A lesson is
a model of at most two lines, one typeable block of one to four commands, a
notice of at most three lines and the `▶` line (WP-26, A13). Rules are built
by a loop at a fixed 80 columns; never `tr` on a multibyte glyph or `${s:0:n}`, and never `tput`.

**Footer.** Words in bold grey (`NAVW`) with the gloss in parentheses: glosses
through Stage 1, in modules and on cleared screens, words only from Stage 2.
The gate's recall and task phases have their own forms.

**Colour roles** (the tutor emits the codes; the terminal picks the colours):

| Role | SGR | Marks |
| --- | --- | --- |
| `BOLD` | 1 | a concept or key being named (replaces cyan and magenta in the body) |
| `CMD` | 92 | something you can type |
| `DIM` | 90 | `#` asides, footer glosses, unreached dots, the stage title in the header |
| `NAVW` | 1;90 | the navigation words in the footer |
| `INSTR` | 93 | `▶`, `┃`, the current-stage dot: the tutor speaking |
| `EM` | 91 | the word that matters, not the line; rare |
| `H1` | 1;97 | the screen title |
| `OK` | 92 | `[✓]`, filled dots |
| (plain) | | paths; box drawing and rules are `RULE` (90), never text |

`SUB` and `DIR` stay defined for the modules and `--info` until WP-26 sweeps
them; do not use them in core screens.

**Glyphs.** Use the glyph variables (`${G_PLAY}`, `${G_BOX_OK}`, `${G_DOT_SEP}`,
...), not literal `▶` or `✓`. Each UTF-8 glyph has an ASCII twin of the same
width, so only the texture changes: `▶ >`, `┃ |`, `─ -`, `● #`, `◉ *`, `○ -`,
`[✓] [x]`, `· :`, corners `+`; `(gloss)` and `[ ]` are the same in both. ASCII
is selected by the plain-text path (`NO_COLOR`, non-TTY) or `SHELLTUTOR_ASCII=1`,
never by locale. The harness has `run.py --ascii`; `scripts/sim/compare_heights.py`
asserts two runs have the same row counts.

**Recall and gate feedback.** A recall question prints once as
`┃ N of 3   <question>` wrapped under the bar, options on their own row, then
`┃ ? ` for the answer; every miss prints `not quite. hint: …` (A7: the hint is on the first
miss), and from the second miss the three navigation facts follow. A gate checklist is
`┃ [✓] item` and `┃ [ ] item   seen: <what the gate saw>`, closed by
`Finish the step marked [ ], then type check again.`. The `seen:` text is an
observation, never an instruction; the instruction belongs to the hint rung.
Use `fb_ok`, `fb_todo`, `fb_close` and `fb_note`.
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

**Adding a recall question.** A recall question is one `ask_question` call:
the prompt, a hint that starts `Lesson N.k: ` (FF-010) and names the concept
without the answer's words (FF-009), then **two lists**: the exact forms
(short, specific answers that must always pass, including answers that are
themselves negations), and after a bare `--` line the keyword groups
(`a|b|c` per line; every group must be hit as whole words, and no negation
word may appear). Add synonyms, never remove them; drop a phrase that lets a
distractor from the prompt's option text through. Prefer multi-word phrases
the lesson uses over one common word (`notes`, `where`, `window`). When the
answer has two parts in a fixed order, put `--ordered` first after `--`; when
a wrong answer shares the right words, list its tell-tale words after a
`--reject` line (checked before the groups, never against an exact form). Then add the question's key
to `scripts/selftest-matching.sh` and its accepted and rejected inputs to
`scripts/matching-corpus.tsv` (FF-011 asserts the call count).

**Heading convention** (binding; the harness derives its sentinels from it):

| Screen | Heading |
| --- | --- |
| intro | `<name>: <title>` |
| lesson `k` of `n` | the title alone; the header's right-hand text is `<name>  k/n` (A15) |
| gate (opening screen; no `▶` line, the first question follows) | `<name> — gate` (header: `<name>  gate`) |
| task | `<name> — task` (header: `<name>  task`) |
| cleared | `<name> cleared.` |

A module has three to six lesson screens (A15). Every module screen is within
the 20-row harness budget, like the core; a module run fails when one is not.

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
