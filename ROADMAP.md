---
title: shelltutor Roadmap
category: planning
component: roadmap
status: active
version: 0.1.0
last_updated: 2026-07-14
tags: [roadmap, phases, planning]
priority: medium
---

# Roadmap

Phase map for `shelltutor`. Each phase closes when its exit criteria hold;
independent implementation work may land before an earlier validation phase
closes, but the status of every phase remains explicit and inspectable.

## Phase 0 — Day-1 Scaffold (complete)

**Closed by commits `e402b58` and `f69389e` (2026-05-17).**

Goal: land the project shell with documentation set, imported prior-art
script, and a published public remote.

Exit criteria:

- Day-1 docs in place (`README`, `CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `STATUS.md`, `ROADMAP.md`).
- Prior-art script imported with provenance commit.
- GitHub remote published.
- Workspace shell records the project in `STATUS.md` and `.gitignore`.

## Phase 1 — User-Agnostic Refactor (complete)

**Closed by commit `e6257aa` (2026-05-21).**

Goal (historical): strip all user-specific framing from the imported
script so the tutor honors its core property.

Work performed:

- Replaced `WYN OPS` accent comments with neutral language.
- Swept for hostname, operator-name, distro-specific, or prompt-theme
  assumptions in the script.
- Confirmed the tutor's output names no specific operator or host.

Exit criteria (met):

- `grep -n 'WYN OPS' shelltutor` returns zero matches.
- Tutor runs cleanly on a clean account with no prior shelltutor history
  (manual run on the operator's macOS host, 2026-05-21).

Audit cross-reference: profile audit-attention flag
`drift-status-roadmap-vs-commit` (= audit finding `F-001`) was raised
because earlier revisions of `STATUS.md` and this file claimed the
refactor was still pending. STATUS.md was realigned in the same change
that marked this phase complete.

## Phase 2 — Portability Validation (current)

Goal: confirm the tutor runs correctly on macOS and Linux without
environment assumptions.

Work:

- Validate on macOS with stock `/bin/bash` (3.2). The tutor's
  documented floor is bash 3.2; Apple's vendored bash satisfies it
  with no install step required.
- Validate on a Debian/Ubuntu-family Linux distro with Bash 5.x.
- Record a no-TTY negative test. Fedora-family validation is useful but
  optional for Phase 2 closure.
- Document any bash version floor.
- Add a `shellcheck` pass; resolve or annotate findings.

Exit criteria:

- Documented run instructions and full five-stage manual walkthroughs on
  macOS Bash 3.2 and Debian/Ubuntu-family Bash 5.x.
- No-TTY invocation exits with the documented preflight diagnostic.
- `shellcheck` clean (or each suppression justified).

## Phase 3 — Curriculum Redesign: Five Mastery-Gated Stages (complete)

**Closed by commit `9f61570` (2026-05-21).**

Goal: restructure the tutor as a **vimtutor prerequisite course**
delivered as five mastery-gated stages. Each stage closes with a gate
combining recall (three questions, all correct) and a practical task
(state-change verified by the script). Passing a stage means passing
it; the next stage does not open until the gate is cleared. Retries are
unlimited; no time pressure; no skip.

This phase superseded the earlier Phase 3 framing ("decide whether the
initial command set is the right surface"). The curriculum decision and
implementation are complete; the spec below remains the durable design record.

### Framing decision

Positioning: **vimtutor prerequisite**. The tutor's purpose is to land
a learner ready to run `vimtutor` without panic. README, AGENTS, and
the script's own banner reframe accordingly. The final stage hands off
to `vimtutor` explicitly when present, or terminates cleanly with a
pointer when not.

This matches `docs/audit/references/shell-research.md` ("Shell
Foundations for Vimtutor") and its 12 concepts / 6 units.

### Stage map

Five stages. Each stage carries three or four short lessons followed by
one gate. Total time budget: 45–60 minutes for a motivated learner.

| # | Stage | Learning goals (verbatim shape) | Commands introduced | Maps to research.md |
| --- | --- | --- | --- | --- |
| 1 | Where am I? | I can identify the shell prompt. I can run a command and read its output. I can name what user I am, what host this is, and what folder I'm in. | `echo`, `pwd`, `whoami`, `date`, `clear`, `exit` | Concepts 1, 3 (Unit 1) |
| 2 | Paths and the filesystem | I can list what's in a folder. I can change folders. I know what `.`, `..`, `~` mean. I can predict where a new file will be created. | `ls`, `ls -l`, `ls -a`, `cd`, `cd ..`, `cd ~` | Concepts 3, 4 (Units 1, 2) |
| 3 | Files and operations | I can create, inspect, copy, move, and delete files safely. I know `rm` is immediate. I can tell a file from a directory. | `touch`, `mkdir`, `rmdir`, `cat`, `less`, `cp`, `mv`, `rm` | Concepts 4, 5 (Unit 2) |
| 4 | Commands, streams, composition | I can read a command (cmd + options + args). I can quote a filename with spaces. I can check if a command exists. I can pipe and redirect. I can glob with `*`. | `command -v`, `wc`, `seq`, `head`, `sort`, `grep`, `\|`, `>`, `>>`, `<`, `*` | Concepts 2, 7, 8 (Units 3, bonus) |
| 5 | Ready for `vimtutor` | I can tell full-screen programs from print-and-exit ones. I can exit `man`, `less`, `vim` deliberately. I know Vim edits a buffer; the file isn't changed until the buffer is written. I know how to launch `vimtutor`. | `man`, `less` (full-screen), `vim --version`, `vim`, `:q!`, `:wq`, `vimtutor` | Concepts 6, 9, 10, 11, 12 (Units 4, 5, 6) |

### Per-stage detail

**Stage 1 — Where am I?** (3 lessons)

- `1.1` The prompt and four navigation words: `next`, `prev`, `show`,
  `quit`.
- `1.2` Running commands: `echo`, simple output, return-to-prompt.
- `1.3` Identity: `whoami`, `pwd`, `date`. No system-resource probing
  (no `/proc`, no `free`, no `df`) — see "Out-of-band content" below.

Gate recall (all three required):

- Q1. Which character typically ends a shell prompt? (`$`, `;`, `:`, `#`)
- Q2. What does `pwd` print?
- Q3. After a command runs, where does its output go by default?

Gate task: run `whoami`, `pwd`, and `date` from the practice prompt in
any order, then type `check`. Verification: parse
`$SANDBOX/.shelltutor_history` since the gate started; each command
must appear at least once.

**Stage 2 — Paths and the filesystem** (3 lessons)

- `2.1` `ls` and what's in a folder.
- `2.2` Moving with `cd`; the home folder `~`.
- `2.3` Paths: relative vs absolute; `.`, `..`.

Gate recall:

- Q1. What does `cd ..` do?
- Q2. What does `~` mean in a path?
- Q3. If I'm in `~/projects` and I type `cd notes`, what folder am I in?

Gate task: create a `practice` directory inside `$SANDBOX`, cd into
it, cd back out, cd home, cd back to `$SANDBOX/practice`. Type
`check`. Verification: `[ -d "$SANDBOX/practice" ]` plus a history
trace showing the four `cd` operations.

**Stage 3 — Files and operations** (3 lessons)

- `3.1` Creating: `touch`, `mkdir`.
- `3.2` Reading: `cat`, `less` (exits with `q`).
- `3.3` Copy, move, delete: `cp`, `mv`, `rm`.

Stage 3 uses its own sandbox sub-directory: `$SANDBOX/stage3/`. The
script creates it on stage entry; the learner operates inside it.

Gate recall:

- Q1. How do you create an empty file? (`touch` / `mkdir` / `new` / `cat`)
- Q2. After `rm important.txt`, where is the file? (`~/.Trash` / disk
  / gone / depends)
- Q3. What single command renames `old.txt` to `new.txt`?

Gate task: starting in `$SANDBOX/stage3/`,

1. create a file `notes.txt` containing the word `hello`;
2. copy `notes.txt` to `backup.txt`;
3. rename `notes.txt` to `done.txt`;
4. remove `backup.txt`.

Type `check`. Verification:

- `[ -f "$SANDBOX/stage3/done.txt" ]`
- `[ ! -f "$SANDBOX/stage3/notes.txt" ]`
- `[ ! -f "$SANDBOX/stage3/backup.txt" ]`
- `grep -q 'hello' "$SANDBOX/stage3/done.txt"`

**Stage 4 — Commands, streams, composition** (3 lessons)

- `4.1` Command structure: `cmd options args`; quoting (research.md
  Concept 2's `vim "my notes.txt"` example); `command -v`.
- `4.2` Pipes: `seq 1 100 \| wc -l`; stacking; `sort \| head`.
- `4.3` Redirection (`>`, `>>`, `<`) and globs (`*.txt`).

Stage 4 sandbox: `$SANDBOX/stage4/`.

Gate recall:

- Q1. What does `command -v vim` print if vim is installed?
- Q2. What is the difference between `>` and `>>`?
- Q3. Why does `vim my notes.txt` open two files instead of one, and
  how do you fix it?

Gate task: inside `$SANDBOX/stage4/`,

1. use `seq` plus a pipe to count 1..100 and save the count to
   `count.txt`;
2. use a glob to list every `*.txt` file in the directory.

Type `check`. Verification:

- `[ -f "$SANDBOX/stage4/count.txt" ]`
- contents of `count.txt` is `100` (whitespace-trimmed)
- history trace contains a glob expression (`*.txt`)

**Stage 5 — Ready for `vimtutor`** (4 lessons)

- `5.1` Full-screen programs: what they are; exit `man ls` with `q`;
  exit `less file` with `q`.
- `5.2` Vim entry and exit (no editing yet): `vim --version`; `vim`
  with `:q!`.
- `5.3` Buffer vs file: open `practice.txt`, type, `:q!`; reopen,
  type, `:wq`; verify with `cat` between attempts.
- `5.4` `command -v vimtutor`; if present, hand off; if absent,
  finale tells the learner how to install it.

Stage 5 sandbox: `$SANDBOX/stage5/`.

Gate recall:

- Q1. How do you exit `man ls`?
- Q2. After `vim notes.txt`, what makes Vim write your edit to the
  file?
- Q3. If you open `notes.txt` in `vim` and type some text but quit
  without saving, did the file on disk change?

Gate task: a two-phase exercise inside `$SANDBOX/stage5/`,

1. starting from `practice.txt` containing the word `before`, open
   it in `vim`, change one letter, **quit without saving** (`:q!`).
   Confirm with `cat practice.txt` that the file still says `before`.
2. open it again, change a letter, save and quit (`:wq`).
   Confirm with `cat` that the file has changed.

Type `check`. Verification:

- before phase 1: `practice.txt` was reset to contain exactly
  `before`;
- after phase 2 completion: `practice.txt` contents differ from
  `before` and the file still exists.

### Gate pattern (canonical pseudocode)

Every stage's gate uses this pattern; only the questions and task
verification differ per stage.

```bash
gate_stage_N() {
    # --- recall: 3 questions, all must be correct, unlimited retries ---
    local i
    for i in 1 2 3; do
        while true; do
            print_question "stage_N_q${i}"
            read -r ans < /dev/tty
            if check_answer "stage_N_q${i}" "$ans"; then
                printf '✓\n\n'
                break
            fi
            printf 'Not quite. Try again.\n\n'
        done
    done

    # --- task: practice subshell until learner types `check` ---
    while true; do
        print_task_for_stage_N
        practice_until_sentinel check                # see below
        if verify_stage_N; then
            printf '✓ Task verified.\n\n'
            break
        fi
        printf 'Not yet. Re-read the task and try again.\n\n'
    done

    mark_passed "$N"     # bumps .progress if (.progress < N)
}
```

`practice_until_sentinel` is a small variant of the current
`practice()`. The rcfile's navigation functions are extended with
`check() { builtin exit 96; }`; on exit code 96 the outer helper
returns to the gate logic. Codes 0/97/98/99 (next/show/prev/quit)
retain their current meaning, so navigation still works during a
gate.

### Progress model

`.progress` semantics change but the file format does not. It still
contains a single non-negative integer, now interpreted as "number of
stages passed":

- on `./shelltutor` startup with no args: resume at stage
  `(.progress + 1)`;
- on `./shelltutor N` (N ∈ 1..5): enter stage N regardless of prior
  progress (re-take supported);
- `mark_passed N` sets `.progress = max(.progress, N)`;
- `./shelltutor 5` followed by a passed gate sets `.progress = 5` and
  the finale removes `.progress`.

### Welcome-screen rewrite (closes audit finding `F-002`)

Pre-redesign wording:

> Everything happens in `~/.shelltutor`; you cannot break anything.

Replacement landed in Phase 3:

> Your tutor work happens in `~/.shelltutor`. The practice prompts run
> as ordinary commands in your account, so usual caution applies. The
> tutor itself never reaches outside this folder.

The new wording is accurate to the actual sandboxing (Phase 6 finding
`F-002`) and does not require any change to the implementation.

### Out-of-band content (closes audit finding `F-003`)

The pre-redesign `lesson 7` (`free -h`, `/proc/cpuinfo`, `/proc/meminfo`,
`ls /proc`) and `lesson 8` (`sudo dnf install cowsay figlet lolcat`)
violated the project's portability claim because both made Linux-only
or Fedora-only assumptions. Phase 3 removed them from the gated
curriculum entirely. They may return as a separately-invoked appendix
(e.g., `./shelltutor extras`) in a future cycle if the operator wants
them, but not as a portability constraint on the main path.

The Phase 1 lesson surface (`whoami`, `pwd`, `date`, `clear`, `echo`,
`exit`) already covered the portable subset of the old lesson 7's
identity commands. No information is lost.

### Acceptance criteria (Phase 3 done)

- All five stages implemented in `shelltutor`, each with a working
  gate.
- `welcome()` rewritten per the "Welcome-screen rewrite" section above
  (audit `F-002` closed).
- The `/proc`, `free`, and `dnf install` lesson content is removed
  from the gated curriculum (audit `F-003` closed).
- `./shelltutor -h` output enumerates five stages, not nine lessons.
- `./shelltutor N` jumps to stage N for re-take or first-time entry.
- `README.md` "Run" and "Goals" sections updated to the vimtutor-
  prerequisite framing.
- `./shelltutor` invocation walkthrough recorded in `STATUS.md` (date
  + result), partial credit toward ROADMAP Phase 2's portability-
  validation exit criterion.
- The script remains a single bash file, bash 3.2+, POSIX userland
  only, no network, no privilege, no writes outside `$SANDBOX`.

### Out of scope for Phase 3

- LICENSE decision (ROADMAP Phase 4).
- `CHANGELOG.md` / first tagged release (ROADMAP Phase 4).
- GitHub-side automation / CI activation (deferred per
  CONTRIBUTING.md:72-75).
- Fitness-function implementation (`FF-001`–`FF-007`); Phase 3
  operationalizes `FF-005` opportunistically via `.claude/settings.json`
  (shellcheck-on-edit warning), but the other fitness functions land
  in a follow-on cycle.
- **Contributor-side PTY simulation harness (FF-006b / FF-006c).**
  The Slice 1..3 implementation track is governed by
  `docs/simulation-design-plan.md` (adopted 2026-05-23) and is
  independent of Phase 2 portability validation. The harness is
  optional contributor tooling and is not part of `make verify`.

## Phase 4 — Release Posture (pending)

Goal: choose a license, cut a tagged release, decide on distribution.

Work:

- License decision (see `STATUS.md` deferral).
- Create `CHANGELOG.md` and tag `v0.1.0`.
- Decide whether managed distribution (Homebrew tap, AUR, etc.) is worth
  the maintenance cost or whether `clone + run` stays the install story.

Exit criteria:

- `LICENSE` present, posture clear.
- First tagged release.
- Distribution decision recorded in `STATUS.md`.

## Out Of Scope

- Shell scripting tutorials (a separate project, if any).
- Sysadmin curriculum.
- Multi-user / classroom features.
- Network-aware lessons.
- Anything that requires the learner to install something beyond `bash`.
