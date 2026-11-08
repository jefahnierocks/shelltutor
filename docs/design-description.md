---
title: shelltutor Design Description
category: reference
component: design-description
status: active
version: 0.1.0
last_updated: 2026-11-08
tags: [design, game-design, mda, architecture, user-journey, pedagogy, baseline]
priority: high
---

# shelltutor Design Description

A formal description of `shelltutor` as it exists, written as the baseline
for later analysis and design work. It is descriptive: it records what the
artifact is and does, names the formal terms that fit, says where they fit
only partly, and lists the tensions the framing exposes. It proposes
nothing.

## Scope and method

- **Revision described**: `main` at `bd841ae` (2026-11-08), which includes
  every package of the 2026-11 work plan except WP-08 part B
  (`docs/workplan/README.md`, status table). F-014, the practice shell
  resolving `bash` through `PATH`, is fixed in this revision (`8d2c7bf`,
  WP-09); the one human walkthrough recorded before the fix is noted where
  it matters.
- **Sources read**: `shelltutor` (2094 lines; cited as `shelltutor:N`),
  `docs/contracts.md` (C-001 to C-007), `docs/simulation-design-plan.md`,
  `docs/phase2-walkthrough-checklist.md`, `ROADMAP.md`, `STATUS.md`,
  `README.md`, `CONTRIBUTING.md`, the `audit/` tree (first cycle
  2026-05-21; findings 2026-05-23, 2026-07-14, 2026-11-07, 2026-11-08;
  simulation evidence under `audit/2026-11-08/sim/`), the harness under
  `scripts/sim/`, `.github/workflows/sim-evidence.yml`, and the research
  references under `docs/audit/references/`.
- **Two registers are kept apart throughout**: *implemented* (a line in
  the script or a committed artifact) and *intended* (ROADMAP, the
  simulation plan, the research references). Where the roadmap and the
  script disagree, both are quoted.
- **Grounding rule**: every claim names a file, and a line where the file
  is code. Line numbers are for the revision above; they move when the
  script changes, the section anchors do not.

---

## 1. Game-design lens

### 1.1 Classification

`shelltutor` is best classified as a **mastery-gated interactive tutorial
with a live practice environment**: single-player, text-only, strictly
linear, with a binary completion outcome. It is not a game in the
Salen–Zimmerman sense (no artificial conflict, no quantified outcome beyond
pass), and it is only partly a "serious game": it has rules, goals,
immediate feedback and progression gates, but no fiction, no score, no
opposition and no variable outcome. The project's own framing is "a
vimtutor prerequisite course" (`shelltutor:2`, `README.md` §Stages,
`ROADMAP.md` §Framing decision, lines 117–126), and that is the honest
genre: a drill-and-practice CBT whose distinguishing property is that the
"practice" is a real shell rather than a simulation of one
(`shelltutor:362-438`; `docs/simulation-design-plan.md` §Planning
Position, "Preserve the production contract as a real interactive Bash
tutor").

Where "game" vocabulary is used below, it is used for the analytic
leverage of MDA, not as a claim that the artifact is a game.

### 1.2 MDA

**Mechanics (rules and components, all implemented):**

- The five navigation verbs and their exit codes: `next`→0, `check`→96,
  `show`→97, `prev`→98, `quit`/`exit`→99 (`shelltutor:76-81`, `422-427`;
  contract C-002, `docs/contracts.md:58-82`). `exit` is overridden so the
  learner cannot leave the practice shell by the normal word without the
  tutor knowing (`shelltutor:427`).
- The screen unit: a heredoc rendered after `clear`, followed by a practice
  prompt (`show_screen`, `shelltutor:444-448`; `lesson`, `453-457`), with a
  mode-aware footer that names `next` at lessons and `check` at gates
  (`shelltutor:368-376`).
- The gate: three recall questions, each looping until an accepted answer
  (`ask_question`, `shelltutor:477-502`), then a task verified against the
  filesystem and, for stages 1, 2 and 4, against the practice history
  (`gate_require_history`, `shelltutor:530-548`; verifiers at `750-786`,
  `1032-1035`, `1261-1267`, `1501-1509`, `1804-1822`).
- The checkpoint: a single integer, "stages passed", written only upward
  (`save_progress`, `shelltutor:328-335`) and removed by the finale
  (`shelltutor:2028`).
- The sandbox: a directory tree the tutor creates and seeds
  (`setup_sandbox`, `shelltutor:288-303`; `setup_stage_dir`, `305-326`;
  layout in C-003, `docs/contracts.md:84-132`).
- The practice shell contract: which variables are unset, which options
  and Readline settings are forced (`shelltutor:385-430`; C-007,
  `docs/contracts.md:185-216`).

**Dynamics (run-time behaviour that emerges from the mechanics):**

- The core loop *read screen → try at the prompt → `next`* is the
  `run_stageN` dispatcher loop indexing a lesson array
  (`shelltutor:911-933`, `1138-1160`, `1353-1376`, `1624-1647`,
  `1962-1985`). `show` re-enters the same index; `prev` decrements and
  clamps at zero (`shelltutor:918-920`).
- The gate loop *attempt → `check` → verdict → retry* is a `while true`
  with an attempt counter and a `skip_screen` flag so feedback stays on
  screen (`shelltutor:831-908`, `1080-1135`, `1298-1350`, `1560-1621`,
  `1863-1959`).
- Quit-and-resume: `quit` anywhere exits 0 with a one-line farewell
  (`shelltutor:432-436`); the next plain run resumes at the first unpassed
  stage (`shelltutor:2055-2064`). Position *within* a stage is not kept,
  so a learner who quits during a gate restarts that stage's lessons.
- Free play: because the prompt is a real Bash, the learner can do
  anything their account allows, inside or outside the sandbox
  (`shelltutor:34-36`; audit `06-authority`, F-002). The design calls this
  "pedagogical containment" rather than enforcement
  (`docs/simulation-design-plan.md` §Command Policy).

MDA fits only partly here: the dynamics are almost entirely the
dispatcher's own control flow. The one genuinely emergent space is the
learner's free use of the shell, which the mechanics neither model nor
observe except through the history file at gates.

**Aesthetics (the experiences the design aims at):** in the Hunicke–LeBlanc
–Zubek taxonomy the targets are *challenge* (gates that must be cleared)
and *discovery* (exploring a filesystem that is really there); the
underlying motivational register is competence. Explicitly rejected are
*fantasy* and *narrative* (the plan forbids anthropomorphic, adversarial or
prize-like framing and keeps the six-name persona roster out of the tutor,
`docs/simulation-design-plan.md` §Pedagogy And UX, §Persona Scope) and
*fellowship* (single player; `README.md` §Non-Goals lists multi-user and
classroom features as out of scope). Tone rules are "concise, concrete,
task-focused, non-condescending, low on praise-heavy copy"
(`docs/simulation-design-plan.md` §Pedagogy And UX); the only celebratory
copy in the script is the `✓` on a correct recall (`shelltutor:497`) and
"✓ Stage N cleared." (`shelltutor:885`, `1118`, `1328`, `1600`, `1943`).

### 1.3 Core loop

`read lesson → practice → next`, repeated three or four times, then
`gate`. Each lesson screen ends with a `▶` instruction line that names the
expected action and the verb to type (`shelltutor:598`, `622`, `664`,
`686`, `705`, `729`, and so on). The footer under the prompt repeats the
verb set (`shelltutor:372-376`). Nothing in a lesson is verified; the
`next` word is accepted whether or not the learner typed the suggested
commands. Verification is deferred to the gate. This is the deliberate
split between *practice* (unchecked, exploratory) and *assessment*
(checked), stated in the welcome ("Each stage is a few short lessons
followed by a small task. Pass the task to advance.", `shelltutor:591-593`).

### 1.4 Progression and gating

- **Strictly linear stages.** `main` runs `run_stage` for
  `s = start .. 5` and exits without the finale on any non-zero return
  (`shelltutor:2082-2089`). A stage's gate must return 0 for the next
  stage to begin.
- **Linear lessons with local back-stepping.** `prev` moves back one
  lesson within a stage only; at a gate, `prev`, `show` and `next` all
  redisplay the task (`shelltutor:904-906`, `1133`, `1348`, `1619`,
  `1909`, `1957`). There is no way back from a gate to its lessons.
- **No skip, with one documented exception.** The in-flow experience has
  no skip (`shelltutor:17-18`, `131-133`), but the CLI accepts
  `./shelltutor N` to enter any stage directly for "re-take or first-time"
  (`shelltutor:2065-2067`; C-001, `docs/contracts.md:43`). Progress is
  never regressed by this, and after `./shelltutor 5` plus a passed gate
  the finale removes `.progress`, so the next plain run starts at Stage 1
  (`ROADMAP.md` §Progress model, lines 322–334; `shelltutor:2028`). The
  roadmap calls this "re-take supported"; functionally it is also a skip.
- **Mastery criterion.** All three recall answers must match an accepted
  form (no partial credit), and the task verdict is boolean. The roadmap's
  phrase is "Passing means passing" (`ROADMAP.md:110-111`).

### 1.5 Failure and feedback system

Two distinct feedback regimes exist, and they differ in richness.

**Recall questions** loop with a single non-specific message, "not quite.
try again." (`shelltutor:500`), by design: "No hints, no answer reveal"
(`shelltutor:466`). There is no attempt counter and no escalation. Accepted
answers are fixed lists per question (for example `shelltutor:806-815`,
`1045-1075`, `1519-1550`).

**Gate tasks** escalate. The first failed `check` prints what the gate
saw: the missing commands list ("Almost — you still need to:",
`shelltutor:542-546`), or the expected-versus-seen folder state
(`shelltutor:1333-1339`), or the content of `count.txt` (`shelltutor:
1603-1608`), or which of the three Stage 1 answers mismatched without
revealing the expected value (`shelltutor:890-894`). The second failure
adds a one-line hint; the third and later add a worked example the learner
must still type (`gate_escalate`, `shelltutor:554-566`; hint texts at
`861-863`, `1111-1113`, `1341-1344`, `1593-1595`, `1903-1905`,
`1951-1953`). The ladder's rule is stated in code: "There is no auto-pass"
(`shelltutor:553`) and in the contract: escalation order is part of the
curriculum design (C-006, `docs/contracts.md:181-183`). The sequence
restatement → hint → worked example is the one the simulation plan asked
for (`docs/simulation-design-plan.md` §Pedagogy And UX, "Repeated gate
failure should eventually escalate"), and the research reference
recommended ("Escalate from hint to a miniature worked example",
`docs/audit/references/educational-design-research.md` §Feedback On Wrong
Commands).

A nuance the formal term "scaffolding ladder" hides: at stages 2, 3 and 4
the task screen already displays the key command as a hint before any
attempt (`shelltutor:1094`, `1309`, `1572`), so the later rungs add little
new information there. Stage 1's ladder is the exception: its hint
("Run the command again and copy its output exactly.") addresses a
transcription task that the screen does not pre-solve.

### 1.6 Difficulty curve

Measured by what the gate task demands:

| Stage | Task shape | What can go wrong | Verification channel |
| --- | --- | --- | --- |
| 1 | Run three commands, then transcribe their outputs | Reading output; copying a path exactly; locale of `date` | history trace plus three typed answers (`shelltutor:792-797`, `750-786`) |
| 2 | Make one folder and enter it | Not using `cd` at all | history trace plus one directory test (`shelltutor:1105-1106`, `1032-1035`) |
| 3 | Four ordered file operations | Order, naming, leaving `backup.txt` | four filesystem predicates (`shelltutor:1261-1267`) |
| 4 | A pipeline with a redirect, plus a glob | Operator precedence; glob typed literally | file content equals `100` plus history trace of `*.txt` (`shelltutor:1501-1509`, `1590-1591`) |
| 5 | Two-phase modal-editor exercise | Saving when told to discard, or the reverse | file content before and after (`shelltutor:1804-1822`) |

Cognitive load rises in kind, not only in count: stages 1–3 operate on
things the learner can see (`ls` output, files), Stage 4 introduces
composition (output as input) and Stage 5 introduces a modal program whose
state is invisible from the prompt. The 45–60 minute budget is an estimate
in the welcome and roadmap (`shelltutor:589`; `ROADMAP.md:131`), not a
measurement; the harness completes all five stages in about four seconds
(`audit/2026-11-08/sim/all-linux/current-rc/summary.md`, `duration_seconds`),
which says nothing about human pacing.

### 1.7 Win condition and handoff

The win condition is passing the Stage 5 gate. The finale clears the
screen, lists every command, key, operator and idea met, and prints
`vimtutor` under "What's next" with install hints if it is absent
(`shelltutor:1991-2025`). It then removes `.progress` (`shelltutor:2028`).

Intent and implementation diverge on the handoff. The roadmap says the
final stage "hands off to `vimtutor` explicitly when present"
(`ROADMAP.md:121-123`) and `--info` says "Stage 5 finale will hand off to
this" (`shelltutor:275`); the finale does not launch `vimtutor`, it names
it. Lesson 5.4 is consistent with the implementation ("If it prints a path,
you're set.", `shelltutor:1778-1780`).

### 1.8 Safe-failure space

The sandbox is a directory, not an isolation boundary (`shelltutor:34-36`;
`docs/simulation-design-plan.md` §Command Policy, "The honest v1 stance is
pedagogical containment"). What it provides:

- a known starting directory per screen (`$SANDBOX` for stages 1–2, the
  stage folder for 3–5; `shelltutor:30-33`, C-003 `docs/contracts.md:113-115`);
- self-healing fixtures (`shelltutor:288-326`);
- a separate history file so the learner's real `~/.bash_history` is
  untouched (`shelltutor:402-406`);
- gates that reset their own state: Stage 3 removes the three task files
  on entry (`shelltutor:1295-1296`), Stage 4 removes `count.txt`
  (`shelltutor:1555`), Stage 5 reseeds `practice.txt` before every
  phase-1 attempt (`shelltutor:1865`).

What it does not provide: protection from the learner's own commands.
Stage 3 teaches `rm` as "Immediately and permanently" with "no undo"
(`shelltutor:1247-1251`), and that is literally true at the prompt. The
welcome's safety sentence is scoped to the tutor's own writes ("the tutor
never writes outside that folder", `shelltutor:595-596`); the sentence
about the learner's own authority lives in `README.md` §Run, not on screen
(the audit's F-002 history: `ROADMAP.md:336-349`; `audit/2026-05-21/06-authority.md`).

### 1.9 Player verbs

Two vocabularies coexist at the same prompt:

1. The tutor's five words (`next`, `prev`, `show`, `quit`/`exit`, `check`),
   implemented as shell functions that terminate the practice shell with a
   code (`shelltutor:422-427`). `check` at a lesson is a no-op that prints
   a one-line note and pauses two seconds (`shelltutor:921-928` and the
   same block in each `run_stageN`).
2. The whole of Bash and the user's installed programs.

Nothing distinguishes the two at the prompt except the footer text. A
learner who types `exit` expecting Bash's behaviour gets the tutor's
(`shelltutor:427`); a learner who types `help` gets Bash's.

### 1.10 Motivational model

Intrinsic, in the self-determination sense: competence through gates with
unlimited retries and no timer (`shelltutor:17-18`); autonomy through an
unconstrained prompt and free pacing; no extrinsic rewards. Flow is
supported structurally (clear goal per screen, immediate feedback at
gates, difficulty rising per stage) but not instrumented: the tutor
records nothing about time or attempts beyond the in-memory attempt
counter, and the harness cannot stand in for a human's pauses
(`audit/2026-11-08/stage1-density-followup.md` §Watch items).

### 1.11 Systems deliberately absent

| Absent system | Where the absence is stated | Design intent it encodes |
| --- | --- | --- |
| Score, points, grades | nothing in the script computes any; `ROADMAP.md:110-111` ("Passing means passing") | mastery is binary; partial credit would blur "ready for vimtutor" |
| Timer, time pressure | `shelltutor:18`, `133`; `README.md` §shelltutor | pacing belongs to the learner |
| Lives, attempt limits | `shelltutor:553` ("no auto-pass"), unlimited loops at `481`, `832` and so on | failure is information, not penalty |
| Skip | `shelltutor:17`, `133` (in-flow); exception: CLI `N` (C-001) | the gate is the only route; the CLI route serves re-take |
| Leaderboard, sharing, multi-user | `README.md` §Non-Goals | single learner, local state only |
| Badges, streaks, praise copy | `docs/simulation-design-plan.md` §Pedagogy And UX | adult-first tone; competence over reward |
| Narrative, characters, mascots | same section; §Persona Scope keeps the named roster out of the tutor | the filesystem is the content |
| Randomisation, procedural tasks | fixtures and tasks are constants (`shelltutor:291-301`, gate texts) | every learner sees the same course; evidence stays comparable |
| Hint on demand | no `hint` verb exists (C-002) | hints are earned by attempts; see §4.2 on fading |
| Sound | `bind 'set bell-style none'` (`shelltutor:415`) | Tab behaviour is taught visually (C-007) |
| Save slots, profiles | one `.progress` integer (C-003) | one learner per sandbox; `SHELLTUTOR_HOME` is the only multiplexer |

---

## 2. Software and developer lens

### 2.1 Architecture

A single Bash script of 2094 lines, `#!/usr/bin/env bash`, targeting Bash
3.2 (`shelltutor:1`, `46-56`), with `set -u` (`shelltutor:38`) and
`BASH_COMPAT=5.0` for here-document behaviour on Bash 5.1+ (`shelltutor:
40-44`; F-009, `audit/2026-07-14/findings.md`). Dependencies at learner
runtime: Bash and a POSIX userland only (`AGENTS.md` §Authority Levels;
enforced by FF-001/FF-002/FF-008).

The structure is layered by function groups rather than modules:
constants and colour roles (`shelltutor:58-103`), CLI surface (`114-282`),
sandbox and checkpoint (`288-350`), the practice shell (`362-438`),
rendering and question helpers (`444-502`), history and gate helpers
(`510-566`), five stage blocks each of intro, lessons, verifiers, gate and
runner (`583-1985`), finale (`1991-2029`), dispatcher and `main`
(`2035-2094`). The first audit cycle recorded the same two runtime
entrypoints the current code has, the CLI and the practice sub-process
(`audit/2026-05-21/03-runtime.md`, EP-001 and EP-002).

**Finite state machine.** The tutor is an FSM over
`(stage s ∈ 1..5, lesson index i, gate phase)`, but the machine is implicit:
states are positions in nested loops, transitions are the C-002 exit codes
returned by the practice shell, and only `s` is persisted (the "stages
passed" integer). Gate sub-states (recall question k, task attempt n,
Stage 5 phase 1 or 2) exist only as control-flow position and local
variables (`attempt`, `skip_screen`; `shelltutor:831`, `1080`, `1298`,
`1560`, `1863`, `1914`). The term fits as an analytic model; the code has
no state table, and a reader reconstructs the machine from five near-
identical dispatcher loops.

**Practice shell (C-007).** `practice()` starts an interactive Bash with
`INPUTRC=/dev/null`, an rcfile fed on fd 3, and `/dev/tty` on stdin
(`shelltutor:384`). The rcfile unsets behaviour-changing variables and the
distribution hook, sets `emacs` mode, `histappend` and `cdspell off`,
redirects history to the sandbox, fixes `PS1`/`PS2`, pins four Readline
settings and defines the navigation functions (`shelltutor:385-430`;
`docs/contracts.md:185-216`). Bash on Debian-family systems still reads its
compiled-in system rcfile first; the contract says so rather than claiming
isolation (`docs/contracts.md:189-194`). The interpreter is the same binary
as the outer script, `"$BASH"` (`shelltutor:384`); before WP-09 it was
whatever `bash` was first on `PATH` (F-014, `audit/2026-11-08/findings.md`,
fixed in `8d2c7bf`).

**Stage-folder model (C-003).** Stages 1 and 2 start every prompt in
`$SANDBOX`; the Stage 1 gate task starts in `$SANDBOX/stage1`; stages 3 to
5 pass their folder to `lesson` (`shelltutor:1167`, `1190`, `1383`,
`1654`, and gate calls at `851`, `1101`, `1323`, `1584`, `1890`, `1937`).
`setup_stage_dir` seeds `stage4/poem.txt`, `stage4/seed.txt` and
`stage5/practice.txt` on stage entry (`shelltutor:305-326`, called at
`1354`, `1625`, `1963`).

**Sandbox normalisation (C-004).** `SHELLTUTOR_HOME` is made absolute
against `$PWD` and stripped of trailing slashes before anything else uses
it (`shelltutor:62-73`; `docs/contracts.md:139`).

### 2.2 State and persistence

| Store | Kind | Lifecycle | Code |
| --- | --- | --- | --- |
| `$SANDBOX/.progress` | checkpoint, one integer "stages passed" | written only upward; clamped to 0 if above 5 or non-numeric; removed by the finale | `shelltutor:328-350`, `2028`; audit `05-state.md` S-004 |
| `$SANDBOX/.shelltutor_history` | practice-shell history, appended per command | read on each prompt start; used by gates as a trace | `shelltutor:402-406`, `510-523` |
| `poem.txt`, `numbers.txt` | constant fixtures | self-heal if missing | `shelltutor:288-303` |
| stage folders and seeded files | per-stage fixtures | seeded on entry; some reset at gate entry | `shelltutor:305-326`, `1295-1296`, `1555`, `1799-1802` |

Resume semantics: no argument → start at `progress + 1`, or show the
finale if all five are passed (`shelltutor:2055-2064`); `N` → start at
`N` regardless (`2065-2067`). The first audit cycle classified `.progress`
as the only `checkpoint-state` and everything else as `artifact`
(`audit/2026-05-21/05-state.md`).

### 2.3 Contracts as the formal interface

`docs/contracts.md` is the interface specification, written after the
fact ("de-facto", `docs/contracts.md:14-20`) and versioned with a pre-1.0
posture (`25-34`):

- C-001 CLI shape (`36-56`) — checked by the smoke test's `-h` and
  bad-argument probes (`scripts/smoke-test.sh`, FF-006a).
- C-002 exit codes (`58-82`) — exercised end to end by every harness run;
  `c002_meaning` is recorded in each `summary.md`.
- C-003 sandbox layout (`84-132`) and C-004 startup environment
  (`134-157`).
- C-005 help text (`159-168`) — the only contract with a direct automated
  check (`scripts/smoke-test.sh` greps).
- C-006 lesson text, non-contractual except content and the escalation
  order (`170-183`) — the escalation order is exercised by the `second-try`
  persona.
- C-007 practice-shell environment (`185-216`).

As contract testing, this is grep-level and behavioural rather than
schema-based; the audit classified all contracts `ad-hoc`
(`audit/2026-05-21/04-contracts.md`).

### 2.4 Preflight and environmental constraints

- **TTY.** `preflight` refuses when stdout or stdin is not a terminal, or
  `/dev/tty` is absent, with a one-sentence diagnostic and exit 1
  (`shelltutor:164-174`); the no-TTY negative test is a Phase 2 exit
  criterion (`ROADMAP.md:99`; checklist `docs/phase2-walkthrough-checklist.md:90-117`).
- **Writable sandbox.** Checked by creating and removing a probe file
  (`shelltutor:177-190`).
- **Not gated.** Presence of `vim`, `vimtutor`, `man`, `less` is reported
  by `--info` only (`shelltutor:152-157`, `253-279`).
- **Locale.** Not controlled; the Stage 1 day check accepts C-locale and
  current-locale forms (`shelltutor:771-786`; F-013).
- **PATH and interpreter.** `PATH` is inherited (C-007 "Not controlled",
  `docs/contracts.md:205`). The practice shell is the outer script's own
  interpreter, `"$BASH"` (`shelltutor:384`; F-014 fixed in WP-09). A bare
  `./shelltutor` still resolves that outer interpreter through `PATH` via the
  shebang (`shelltutor:1`), which is why the Phase 2 checklist says to
  invoke the Bash under test explicitly.
- **Environment scrubbing.** C-007's unset list (`shelltutor:391-394`),
  proven by a control run in which the pre-hardening script auto-logged
  out under `TMOUT=5` and the hardened one did not
  (`audit/2026-11-08/slice2-comparison.md` §Environment-scrub check).

### 2.5 Observability and test strategy

The tutor itself emits no telemetry (audit `07-observability`: absent by
design). Observation is external, through a contributor-side PTY harness
in Python 3.9+ stdlib (`scripts/sim/`, `docs/simulation-design-plan.md`
§Code Layout).

- **Personas** are deterministic action lists: each `Action` is "wait for
  sentinel, then send text", with `raw` and `delay_s` fields for keystrokes
  and Vim timing (`scripts/sim/persona.py:43-58`). `careful-beginner` types
  the print-and-exit commands each lesson lists and drives full-screen
  programs only where the lesson is about them (`persona.py:194-338`);
  `second-try` fails the first gate `check` on purpose at stages 2 and 4
  (`persona.py:154-177`; `run.py:60`). Both are listed in
  `scripts/sim/README.md` §Personas.
- **Sentinels** are ANSI-stripped substrings of screen text
  (`scripts/sim/sentinels.py`), matched forward-only so repeated prompts
  disambiguate by order. They are the harness's coupling to lesson copy:
  renaming a heading breaks the walk, which is why WP-04 changed both
  together (`audit/2026-11-08/stage1-density-followup.md`).
- **Evidence bundle**: `terminal.jsonl` (raw PTY chunks), `events.jsonl`
  (sentinel matches, inputs, `gate-pass`, `error-signature`, timeouts),
  `summary.md` (run metadata, controlled inputs, host inputs, outcome),
  `result.tap` (one TAP line) (`docs/simulation-design-plan.md` §Evidence
  Bundle; example `audit/2026-11-08/sim/all-linux/current-rc/summary.md`).
- **Test oracle.** A run is green when the expected sentinel sequence
  completed, every gate reported `gate-pass`, and `.progress` afterwards
  equals the stage number for stages 1–4 or is absent for stage 5 and
  `all` (`run.py:189-191`); `second-try` additionally requires exactly one
  "Almost — you still need to" (`run.py:64`, `330-335`). The
  `error-signature` scan (six substrings such as "No such file or
  directory", `scripts/sim/driver.py:56-62`, applied to lesson screens
  only, `driver.py:55`) is an observation channel: it records findings, it
  does not fail the run. It is how F-010 and F-011 were made visible before
  they were fixed (`audit/2026-11-08/sim/all/current-rc/summary.md`
  versus `all-postfix`).
- **Evidence baseline, not golden master.** Bundles are committed per
  change (`audit/2026-11-08/sim/all`, `all-postfix`, `all-slice2`,
  `stage1-wp04`, `second-try-stage2`, `all-linux`) and compared with
  `scripts/sim/compare.py` on normalised output. The comparison is read by
  a human and summarised (`audit/2026-11-08/slice2-comparison.md`); it is
  not byte-exact, because temp paths, dates, `ls -l` times and Vim's
  splash text differ per run. "Deterministic replay" therefore holds for
  the *input* side (the persona) and not for the transcript.
- **Controlled versus host inputs.** The harness fixes `HOME` (empty
  tempdir), `LC_ALL=C`, `VIMINIT`, `PAGER`, geometry and `TERM`
  (`run.py:245-264`; D-03 in `docs/workplan/README.md`) and records
  everything else as host inputs, so a reviewer can tell a learner-visible
  difference from a harness artifact.
- **Non-gating CI.** `.github/workflows/sim-evidence.yml` runs the
  five-stage walk on `ubuntu-24.04` on every push to `main` and on
  dispatch, with `continue-on-error` and an uploaded artifact
  (`sim-evidence.yml:4-6`, `26`, `28-34`). The gating workflow is
  `verify.yml`; `make verify` never runs the harness (`Makefile`,
  `CONTRIBUTING.md:68-69`). Intake of a hosted bundle is manual
  (`scripts/sim/README.md`, "Hosted Linux evidence intake").
- **Static gates.** FF-001 safety and FF-002 write scope
  (`scripts/check-safety.sh`), FF-004 lesson portability including the
  sandbox-path rule (`check-portability.sh`), FF-005 ShellCheck, FF-006a
  smoke (`smoke-test.sh`), FF-007 governance paths (`check-governance.sh`),
  FF-008 POSIX text tools (`check-posix-tools.sh`); the table is
  `CONTRIBUTING.md:61-69`. FF-003 (doc drift) is deferred and covered by
  manual sweeps (`STATUS.md:86-88`, `175`).

### 2.6 Portability matrix

| Surface | Harness evidence | Human walk |
| --- | --- | --- |
| macOS, Apple Silicon, `/bin/bash` 3.2.57 | green: `audit/2026-11-08/sim/all-slice2-bash32`, `stage1-wp04-bash32`; after the F-014 fix a `/bin/bash`-first run was green but not committed (WP-09 report) | reported cleared on 2026-11-08 before the F-014 fix, with the practice shell's Bash version unconfirmed; to be repeated (`audit/2026-11-08/findings.md`, `STATUS.md`) |
| macOS, Bash 5.3.20 (Homebrew) | green: `all-slice2`, `stage1-wp04`, `second-try-*`, `all-current` (post-WP-09, with `bash_version` recorded) | not a Phase 2 surface |
| Ubuntu 24.04, Bash 5.2.21, hosted runner | green: `all-linux` (no error signatures; event shapes match macOS) | pending (`STATUS.md:146-153`) |
| Fedora family | none | optional (`docs/phase2-walkthrough-checklist.md:33`) |
| No TTY | exit 1 with diagnostic, measured 2026-11-07 (`docs/workplan/README.md` §Baseline) | checklist item, pending |

---

## 3. User-journey lens

### 3.1 Personas

Three personas are grounded in project artifacts; two more are implied by
the code and listed because the journey map needs them.

- **P1 — the careful beginner.** Reads each screen, types what it says,
  types `next`. Modelled by the harness persona of the same name
  (`scripts/sim/persona.py`; `docs/simulation-design-plan.md` §Persona
  Scope). The research reference's target audience is "adult beginners
  first, child-friendly compatible second" (`docs/simulation-design-plan.md`
  §Pedagogy And UX).
- **P2 — the second-try learner.** Does most of a task, misses one step,
  reads the gate's feedback, finishes. Modelled by `second-try`
  (`persona.py:154-177`); the research reference's "Nearly correct" row
  (`educational-design-research.md` §Feedback On Wrong Commands).
- **P3 — the vimtutor-bound reader.** Has Vim, wants to start `vimtutor`
  without panic; the course's framing persona (`ROADMAP.md:117-126`;
  `shell-research.md` §The minimal "ready for vimtutor" checklist).
- **P4 (implied) — the returning learner.** Quit mid-course; relies on
  resume (`shelltutor:2055-2064`).
- **P5 (implied) — the differently-set-up learner.** Non-English locale,
  zsh or fish as login shell, `SHELLTUTOR_HOME` set, no `vim`, a narrow
  terminal. Each is handled, or not, at a specific line (§3.3).

The deferred `confused-novice` and the named six-person roster are not
personas of this description (`docs/simulation-design-plan.md` §Persona
Scope, §Deferred).

### 3.2 Journey map

Each touchpoint: the system's cue, the expected action, failure modes,
recovery.

| # | Touchpoint | Cue (implemented) | Expected action | Failure modes | Recovery |
| --- | --- | --- | --- | --- | --- |
| 1 | Discovery | `README.md` §Run; `./shelltutor -h` usage text (`shelltutor:114-143`) | run `./shelltutor` | the shebang picks the first `bash` on `PATH` as the outer interpreter (`shelltutor:1`); not knowing `--info` exists | `-h` lists `--info`; `README.md` requirements |
| 2 | Preflight (`--info`) | environment check with ok / not ok / info marks (`shelltutor:203-282`) | read, fix any "not ok" | `vim` missing (warned, `271`); sandbox unwritable (`224`, `228`) | `SHELLTUTOR_HOME` override hint (`180`, `187`) |
| 3 | Preflight (implicit) | silent on success; one-sentence diagnostic otherwise (`shelltutor:160-192`) | none | no TTY, no `/dev/tty`, unwritable sandbox | exit 1 with the fix named |
| 4 | Welcome and orientation | two screens: identity, then the prompt and four words (`shelltutor:583-625`) | type `next` twice | typing a command instead of `next` (works, nothing lost); wrapping on a narrow terminal (`612-614`) | footer repeats the verbs (`375`) |
| 5 | Stage entry | stage banner with lesson count and commands (`shelltutor:631-644`, `939-959`, `1166-1187`, `1382-1405`, `1653-1667`) | `next` | — | — |
| 6 | Lesson reading | heredoc with commands in `CMD` colour, `#` asides in `DIM`, `▶` line | try the commands, then `next` | typing `check` (one-line note, `926`); forgetting `next` | `show` redisplays; `prev` steps back |
| 7 | Practice | `shelltutor> ` prompt, real Bash (`shelltutor:408`) | run commands freely | leaving the sandbox with `cd`; `rm` of real files; stuck in `less`/`man`/`vim` | `cd ${SANDBOX}` taught in 2.2 (`998`); `q` and `:q!` taught in 3.2, 5.1, 5.2; Ctrl+C gives a fresh prompt (`683-684`) |
| 8 | Gate recall | three blue questions with "your answer:" (`shelltutor:482-483`) | type an accepted answer | synonym not in the accepted list; typo; wanting to leave (`quit` is read as an answer) | "not quite. try again." loops (`500`); Ctrl+C ends the script, resume restarts the stage (`105-108`) |
| 9 | Gate task | task screen with numbered steps and, at stages 2–4, a hint line; footer names `check` (`373`) | do the steps, type `check` | partial work; wrong order; `check` before running anything | first failure shows what the gate saw |
| 10 | Gate failure, ladder | "Almost — you still need to:" or expected-versus-seen, then hint, then worked example (`shelltutor:542-566`) | act on the feedback, `check` again | repeating the same mistake | third rung shows the commands; never auto-passes |
| 11 | Stage cleared | "✓ Stage N cleared." (`shelltutor:885`, …) then the next stage's banner immediately | continue | none; there is no pause between stages | `quit` at the next banner saves progress |
| 12 | Quit and resume | "Bye. Run 'shelltutor' again to pick up where you left off." (`shelltutor:434`) | come back later | expecting to resume mid-stage | resume is per stage (`2055-2064`) |
| 13 | Finale and handoff | summary screen; `vimtutor` named under "What's next" with install hints (`shelltutor:1991-2025`) | run `vimtutor` yourself | expecting an automatic launch (`--info` says "hand off", `275`) | `shelltutor 1` to replay (`2021`) |

### 3.3 Negative paths

| Path | Behaviour | Code |
| --- | --- | --- |
| No TTY (pipe, cron, CI) | refuses in preflight, exit 1, three-line diagnostic, no lesson copy rendered | `shelltutor:164-169`; checklist §No-TTY negative test |
| `/dev/tty` absent | refuses, exit 1 | `shelltutor:170-174` |
| Unwritable sandbox | refuses with the `SHELLTUTOR_HOME` fix | `shelltutor:177-190` |
| Non-English locale | Stage 1 day answer accepted in C or current locale, period-insensitive; question invites "exactly as date printed it" | `shelltutor:771-786`, `879`; F-013 |
| Inherited progress from an old layout | values above 5 or non-numeric clamp to 0 | `shelltutor:342-347` |
| Inherited stage files | fixtures self-heal; gates 3, 4, 5 reset their task files | `shelltutor:288-326`, `1295-1296`, `1555`, `1865` |
| Missing `vim` | lesson 5.2 says "install it before continuing"; `--info` warns; the Stage 5 gate has no alternative path | `shelltutor:1704-1707`, `268-271` |
| Missing `man` or `less` | `--info` says lesson 5.1 / 3.2 "will skip" the demo; the lessons contain no such conditional | `shelltutor:261`, `266` versus `1669-1695`, `1212-1233` |
| Login shell is zsh or fish | irrelevant: the practice shell is Bash by construction | `shelltutor:384`; `--info` note at `217` |
| Narrow terminal | orientation asks for 80×24; the script states a 20-line budget per screen, but ten screens in stages 2–5 and the finale exceed it (4.3 is 30 lines, 5.3 is 35; `audit/2026-11-08/findings.md` O-J), so their headings scroll off before the prompt on 24 rows | `shelltutor:612-614`, `576-580` |
| Ctrl+C at the outer script | the script dies; nothing between gates is lost because only passed stages are saved | `shelltutor:105-108` |

### 3.4 Highest drop-off risks

Ranked by how little the design currently offers at the moment of risk.

1. **A correct answer the recall list does not contain.** `ask_question`
   has fixed accepted forms and one unvarying message; there is no hint,
   no reveal, no attempt counter and no way out except Ctrl+C, which kills
   the script (`shelltutor:477-502`, `466`, `105-108`). Stage 2 Q3 accepts
   four spellings (`1070-1075`); Stage 1 Q1 accepts one (`802-804`). The
   escalation ladder of §1.5 does not reach recall. Nothing on screen tells
   the learner that Ctrl+C is the exit or that progress to this point is
   safe.
2. **Stage 5 without Vim.** The gate cannot be passed and the course offers
   no alternative; the learner is told to install something, which the
   project otherwise never asks (`shelltutor:1707`, `1782-1787`;
   `AGENTS.md` §Work Rules, "Lessons must be runnable … without
   prerequisite installation beyond bash").
3. **The Stage 1 follow-up prompts.** Three blocking `read` prompts with no
   navigation words (`shelltutor:869-882`); typing `show` or `quit` is
   taken as an answer; a mismatched path (for example a symlinked
   `/tmp`) fails with "The pwd answer did not match" and the task restarts
   (`892-894`). The density audit flagged these as "not screens with
   show/prev navigation" (`audit/2026-05-23/stage1-density.md`, S1-FQ).
4. **Being inside a full-screen program for the first time.** The first
   pager is in lesson 3.2 with `q` explained (`shelltutor:1224-1229`);
   Vim's `:q!` is taught in 5.2 (`1719-1723`). Between 3.2 and 5.1 a
   learner who runs `man` on their own has only lesson 3.2's sentence to
   go on.
5. **No pause after "Stage N cleared."** The next banner renders at once
   (`shelltutor:2082-2084`); the moment of completion has no screen of its
   own except at the finale.
6. **Quitting mid-gate.** Recall answers and task attempts are lost; the
   learner re-reads the stage's lessons on return (`2055-2064`).

For 1 and 3 the design currently offers nothing; for 2 it offers a warning
before the course and a pointer during it; for 4 to 6 it offers text.

---

## 4. Pedagogy and learning-cues lens

### 4.1 Learning-science placement

- **Mastery learning.** Fixed criterion (all three recall items plus a
  verified task), unlimited time and attempts, no advancement without
  passing (`shelltutor:15-18`, `131-133`; `ROADMAP.md:106-111`). The
  research reference supports the model and the high threshold
  (`educational-design-research.md` §Pacing And Mastery). What is missing
  from a full mastery-learning design is *corrective instruction* between
  attempts: the ladder gives hints and an example, but never re-teaches a
  lesson, and `prev` cannot return from a gate to its lessons (§1.4).
- **Scaffolding and fading.** Lesson copy is fully scaffolded (every
  command is shown verbatim with its outcome); gate task screens remove
  some scaffolding but keep a hint line at stages 2–4 (`shelltutor:1094`,
  `1309`, `1572`); the ladder re-adds scaffolding on failure
  (`554-566`). Fading therefore runs lesson → task → (on failure) back to
  example, which is the reverse of classical fading at the point where it
  bites. Stage 5's task screens contain the full key sequence
  (`1874-1880`, `1924-1927`), so the task tests execution more than recall.
- **Worked examples and cognitive load.** The simulation plan's split rule
  is "two or more new concepts or two or more distinct actions → split
  candidate" (`docs/simulation-design-plan.md` §Pedagogy And UX); the first
  density audit applied a working ceiling of five concepts for a reference
  card (`audit/2026-05-23/stage1-density.md`, S1-O: "Five concepts is the
  ceiling under the rule"). The two statements are not the same rule; the
  follow-up audit resolved the tension case by case ("four keys exceed the
  literal rule, but they are one family",
  `audit/2026-11-08/stage1-density-followup.md`). The 20-line vertical
  budget (`shelltutor:576-580`) is an extraneous-load control: a screen must
  fit a 24-row terminal with the prompt visible. It is met by every Stage 1
  screen and missed by ten others (O-J in `audit/2026-11-08/findings.md`),
  so as a course-wide control it is stated, not enforced. Intrinsic load is managed
  by stage order (§4.3); germane load is served by the "what just happened"
  model (`shelltutor:710-732`).
- **Retrieval practice.** The three recall questions per gate are retrieval
  of that stage's content (`shelltutor:802-824`, `1045-1075`, `1277-1291`,
  `1519-1550`, `1832-1860`). There is no interleaving or spaced retrieval
  across stages; the finale lists everything but asks nothing
  (`1996-2008`).
- **Predict–observe–explain.** Named in the copy twice: "Predict before you
  act." in 2.3 and 4.3 (`shelltutor:1024`, `1494`). The Stage 5 gate is a
  structured POE in task form: the lesson states the prediction (the file
  is unchanged after `:q!`), the task has the learner observe with `cat`,
  and recall Q3 asks for the explanation (`1852-1860`), though the explain
  step precedes the observe step in the gate's order.
- **Formative versus summative.** `check` is learner-initiated formative
  assessment inside a task: repeatable, diagnostic ("What I see in …",
  `1338-1339`), and it never records anything. The gate as a whole is the
  summative event for the stage: binary, recorded once in `.progress`
  (`328-335`). The research reference's "immediate opportunity to apply
  feedback" (`educational-design-research.md` §Pacing And Mastery) is the
  `skip_screen` behaviour that keeps feedback on screen while the prompt
  returns (`shelltutor:855-865`).
- **Feedback timing and specificity.** Immediate everywhere. Specific for
  tasks (missing commands by name, folder listings, file content, which
  Stage 1 answer missed); deliberately non-specific for recall. The
  reference's three-step shape (acknowledge intent, name the mismatch, give
  the smallest next action) is met by the task feedback at its first two
  steps and by the ladder's hint at the third.
- **Transfer.** To `vimtutor`: Stage 5 teaches exactly the moves `vimtutor`
  assumes (`:q!`, `:wq`, buffer versus file), and the finale points at it
  (`1991-2025`). To real shells: the practice shell is real Bash with
  common-Bash completion behaviour chosen "transfer-first" over a cleaner
  in-tutor behaviour (`docs/simulation-design-plan.md` §Tab Completion
  Contract; C-007). One transfer discontinuity is built in: the practice
  prompt is `shelltutor> ` (`shelltutor:408`) while Stage 1's first recall
  item teaches that a prompt usually ends in `$` (`802-804`); the learner
  never sees a `$` prompt in the tutor.
- **Error-tolerant learning.** Unlimited retries, resettable gate state,
  separate history, and `rm` scoped by instruction to lesson-created files
  (`docs/simulation-design-plan.md` §Command Policy, "Keep `rm` live in
  Stage 3, scoped to lesson-created files"). Tolerance is pedagogical, not
  enforced: the shell is the learner's own (§1.8).
- **Metacognitive prompts.** "Predict before you act." (`1024`, `1494`);
  "Things to notice while you try these" (`1457-1460`); "A safety habit:
  list before you remove." (`1253-1255`); the Stage 1 task's requirement to
  report what each command printed (`740-741`, `844`); lesson 1.4's
  terminal → shell → program model (`714-727`), which the research
  reference names as learning goal 1 (`shell-research.md` §Central
  learning goals).

### 4.2 Learning-cue catalogue

| Cue | Form | Where | Function |
| --- | --- | --- | --- |
| Action line | `▶ Type next …` in `INSTR` colour, always the last line of a screen | every screen, e.g. `shelltutor:598`, `664`, `1028` | tells the learner the one thing to do to move on |
| Mode footer | "(type check when done — or show, prev, quit)" versus "(type next to advance — …)" | `shelltutor:372-376` | signals lesson versus gate so the wrong verb is not trained |
| Colour roles | `H1` title, `SUB` concept, `CMD` typeable, `KEY` keypress, `EM` warning, `DIR` path, `INSTR` action, `DIM` aside, `OK` pass, `Q` question | `shelltutor:88-99` | semantic typography; collapses to plain text under `NO_COLOR` or a non-TTY (`100-103`), leaving `▶`, `#` and `✓` as the only remaining marks |
| Inline aside | `# comment` in `DIM` after a command | e.g. `shelltutor:657-658`, `967-969` | predicts the outcome before the learner runs it |
| Recall tick | `✓` after an accepted answer | `shelltutor:497` | confirms without praise |
| Stage marker | `✓ Stage N cleared.` | `shelltutor:885`, `1118`, `1328`, `1600`, `1943` | the single completion signal per stage |
| Missing-step list | "Almost — you still need to:" with labels | `shelltutor:542-546` | names the gap, not the answer |
| Expected / seen | "What I expected:" then "What I see in …:" with a listing | `shelltutor:1334-1339` | shows the delta the learner must close |
| Ladder rungs | "Hint:" then "Worked example — type these yourself:" | `shelltutor:557-559` | graded help; keeps the typing with the learner |
| Mismatch naming | "The pwd answer did not match." | `shelltutor:892-894` | localises the error without revealing the value |
| Misplaced verb note | "(check is only for gate tasks. …)" with a two-second pause | `shelltutor:926-927` | corrects navigation without a screen change |
| Pre-task hint | "Hint: mkdir practice creates the folder." and similar | `shelltutor:1094`, `1309`, `1572` | lowers the first-attempt barrier; see §4.1 on fading |
| Farewell | "Bye. Run 'shelltutor' again to pick up where you left off." | `shelltutor:434` | makes resume discoverable |
| Environment check | ok / not ok / info marks | `shelltutor:203-282` | self-diagnosis before the first screen |

### 4.3 Sequencing logic

**Within a stage**, each stage moves from recognition to action to model:

- Stage 1: run a command (1.1) → keyboard habits (1.2) → identity commands
  (1.3) → the terminal/shell/program model (1.4) (`shelltutor:646-732`).
- Stage 2: list (2.1) → move (2.2) → name locations (2.3) (`961-1030`).
- Stage 3: create (3.1) → read (3.2) → copy, move, delete (3.3)
  (`1189-1259`), with the destructive verb last and framed by a safety
  habit.
- Stage 4: command grammar and quoting (4.1) → pipes (4.2) → redirection
  and globs (4.3) (`1407-1499`).
- Stage 5: recognise full-screen programs (5.1) → leave Vim (5.2) →
  buffer versus file (5.3) → launching `vimtutor` (5.4) (`1669-1794`);
  leaving is taught before editing by design ("Before you edit anything,
  let's learn how to leave.", `1701-1702`).

**Across stages**, the order follows the research reference's concept
sequence (orientation → navigation → files and paths → quoting and
globbing → redirection and pipes → editor handoff;
`educational-design-research.md` §Executive Synthesis) and the stage map's
concept mapping (`ROADMAP.md:133-139`). Each stage depends on the previous:
Stage 2 needs the prompt and `pwd`; Stage 3 needs `cd` and paths; Stage 4
needs files to count and redirect into; Stage 5 needs the file model to
make "buffer versus file" meaningful.

### 4.4 Learning objectives and what the gate measures

Objectives are the roadmap's "learning goals" restated in measurable form;
the last column says where the gate measures something narrower.

| Stage | Measurable objective (from `ROADMAP.md:133-139`) | Gate measures | Narrower than the objective |
| --- | --- | --- | --- |
| 1 | Given a prompt, the learner runs a command, reads its output, and states their user name and current folder | recall ×3; `whoami`, `pwd`, `date` present in history; three transcribed outputs | "what host this is" is in the objective but no command for it is taught or measured; reading output is measured by transcription, which also tests exact copying |
| 2 | The learner lists a folder, changes folder, explains `.`, `..`, `~`, and predicts where a new file lands | recall ×3 (`cd ..`, `~`, a relative-path prediction); a `cd` in history; `practice/` exists | prediction is measured only as recall (Q3); `ls` is not measured at all |
| 3 | The learner creates, inspects, copies, moves and deletes files and knows `rm` is immediate; can tell a file from a directory | recall ×3; end state of four operations | "inspect" (`cat`, `less`) is not measured; file-versus-directory is not measured; `rm`'s immediacy is measured by `backup.txt` being gone and by recall Q2 |
| 4 | The learner reads a command's grammar, quotes a filename with spaces, checks whether a command exists, pipes, redirects and globs | recall ×3 (`command -v`, `>` versus `>>`, quoting); `count.txt` equals 100; `*.txt` in history | quoting and `command -v` are measured only as recall; the glob is measured by its presence in history, not by its effect |
| 5 | The learner distinguishes full-screen from print-and-exit programs, exits `man`, `less` and `vim` deliberately, explains buffer versus file, and knows how to launch `vimtutor` | recall ×3 (`q`, `:w`, discard semantics); file unchanged after `:q!`, changed after `:wq` | exiting `man` and `less` is measured only as recall; launching `vimtutor` is not measured; the task measures Vim's save/discard precisely |

The research reference's "minimal ready-for-vimtutor checklist" asks the
learner to do a sequence that ends with `command -v vimtutor` and
`vimtutor` (`shell-research.md` §The minimal "ready for vimtutor"
checklist); the course teaches every item and measures all but the last.

---

## 5. Glossary: project terms to formal terms

| Project term | Where defined | Formal term(s) used above | Fit |
| --- | --- | --- | --- |
| stage | `shelltutor:20-25`; `ROADMAP.md` §Stage map | level / unit of progression; mastery unit | full |
| lesson | `shelltutor:453-457`; the `stageN_lesson_k` functions | instructional screen; worked example with an unassessed practice opportunity | full |
| gate | `stageN_gate` functions; `ROADMAP.md` §Gate pattern | summative assessment with a mastery criterion; progression lock | full |
| recall question | `ask_question`, `shelltutor:477-502` | retrieval-practice item with a closed answer set | partial: no escalation, so not a scaffolded item |
| gate task | the `GATE TASK` screens | performance assessment verified by state (filesystem) and trace (history) | full |
| check | `shelltutor:423`; C-002 | learner-initiated formative check; task oracle invocation | full |
| practice prompt / practice shell | `shelltutor:362-438`; C-007 | live practice environment; real-system sandbox (not an emulator) | partial: "sandbox" implies isolation the design does not claim |
| sandbox | `$SANDBOX`; C-003 | working-directory convention plus fixtures; safe-failure space by instruction | partial, as above |
| navigation words | `shelltutor:422-427`; C-002 | player verbs; control vocabulary; FSM transition inputs | full |
| `.progress` | C-003; `shelltutor:328-350` | checkpoint state; save file with one integer | full |
| persona | `scripts/sim/persona.py` | deterministic test script; synthetic user model | full for testing, partial for UX personas (behaviour only, no goals or context) |
| sentinel | `scripts/sim/sentinels.py` | synchronisation marker; expected-output oracle fragment | full |
| variant | `scripts/sim/run.py` (`current-rc` only since Slice 2) | test configuration | full |
| evidence bundle | `docs/simulation-design-plan.md` §Evidence Bundle | test artifact; evidence baseline (not a golden master) | partial: compared by a human, not asserted |
| finding (F-nnn) | `audit/*/findings.md` | defect record with severity and provenance | full |
| fitness function (FF-nnn) | `audit/2026-05-21/10-fitness-functions.md`; `CONTRIBUTING.md:61-69` | architectural fitness function; static gate | full |
| contract (C-nnn) | `docs/contracts.md` | interface specification (informal), stability commitment | partial: no schema; grep-level checks |
| density audit | `audit/2026-05-23/stage1-density.md` | cognitive-load review per screen | full |
| hint ladder / escalation | `gate_escalate`, `shelltutor:554-566` | graded scaffolding on failure; feedback escalation | full |
| finale | `shelltutor:1991-2029` | win screen; handoff pointer | partial: "handoff" is a pointer, not a launch |

## 6. Design tensions and open questions

Each item names the files that hold the two sides. These are observations
the formal framing makes visible, not proposals.

1. **Recall has no ladder.** Task feedback escalates (`shelltutor:554-566`;
   C-006) while recall loops on one message with a closed answer list
   (`shelltutor:466`, `500`). The mastery criterion is identical for both,
   so the two regimes present the same stakes with different help.
   (`shelltutor`, `docs/contracts.md` C-006, `docs/simulation-design-plan.md`
   §Pedagogy And UX.)
2. **"No skip" and the CLI jump.** The learner-facing text promises no skip
   (`shelltutor:17`, `133`); C-001 provides `./shelltutor N` for any stage,
   and the finale advertises it for replay (`shelltutor:2021`). Both are
   intended; the vocabulary differs. (`shelltutor`, `docs/contracts.md`
   C-001, `ROADMAP.md` §Progress model.)
3. **Handoff: pointer or launch.** `ROADMAP.md:121-123` and
   `shelltutor:275` say the finale hands off to `vimtutor`; the finale
   prints the command (`shelltutor:2010-2013`). (`ROADMAP.md`, `shelltutor`.)
4. **`--info` promises conditional lessons that do not exist.** Lines 261
   and 266 say lessons 5.1 and 3.2 "will skip" their demo when `man` or
   `less` is missing; neither lesson branches. (`shelltutor`.)
5. **Prompt character taught versus prompt character shown.** Stage 1 Q1
   accepts `$` as the usual prompt ending (`shelltutor:802-804`); the
   practice prompt ends in `> ` (`shelltutor:408`, C-007). (`shelltutor`,
   `docs/contracts.md` C-007.)
6. **Objective breadth versus gate breadth.** Several roadmap learning
   goals are measured only as recall or not at all (§4.4): "what host this
   is" has no taught command; `ls`, `cat`, `less`, quoting, `command -v`
   and the `vimtutor` launch are never performed under verification.
   (`ROADMAP.md:133-139`, the `stageN_verify_*` functions.)
7. **Fading runs backwards at the gate.** Task screens pre-hint at stages
   2–4 (`shelltutor:1094`, `1309`, `1572`) and Stage 5 spells out the
   keystrokes (`1874-1880`), so the ladder's later rungs restate what is
   already on screen. (`shelltutor`, `docs/simulation-design-plan.md`
   §Pedagogy And UX.)
8. **Safety sentence location.** The on-screen welcome states what the
   tutor writes (`shelltutor:595-596`); the statement that practice
   commands carry the learner's full authority is in `README.md` §Run and
   `AGENTS.md`, not on screen. The roadmap's F-002 wording included it
   (`ROADMAP.md:343-346`); the current welcome does not. Recorded as
   operator question O-3 in `docs/workplan/README.md`.
9. **Two load rules.** The plan's split rule (two concepts or two actions)
   and the audit's five-concept ceiling are both in force and were
   reconciled case by case (`docs/simulation-design-plan.md` §Pedagogy And
   UX; `audit/2026-05-23/stage1-density.md` S1-O;
   `audit/2026-11-08/stage1-density-followup.md`).
10. **Mid-stage state is not persisted.** `.progress` records stages only
    (`shelltutor:328-350`); a quit during recall or a task restarts the
    stage's lessons. The roadmap's progress model specifies exactly this
    (`ROADMAP.md:322-334`), so it is intended, and it is also the cost side
    of risk 6 in §3.4.
11. **Practice-shell interpreter (resolved in this revision).** Until WP-09
    the practice shell was whichever `bash` was first on `PATH`, so "validated
    on Bash 3.2" described rendering and gate logic but not necessarily the
    prompt the learner typed at (F-014, `audit/2026-11-08/findings.md`).
    Since `8d2c7bf` it is `"$BASH"` (`shelltutor:384`). The one human macOS
    walk recorded before the fix is to be repeated.
12. **Coupling of observation to copy.** Sentinels are heading substrings
    (`scripts/sim/sentinels.py`), so lesson wording and the test harness
    change together (WP-04 did both). This keeps the evidence honest and
    makes copy edits a two-file change. (`scripts/sim/sentinels.py`,
    `audit/2026-11-08/stage1-density-followup.md`.)
13. **Human pacing is unobserved.** The density audits' "watch" items
    depend on a pause signal the harness cannot produce
    (`audit/2026-11-08/stage1-density-followup.md` §Watch items); the
    tutor records no timing. (`audit/`, `shelltutor`.)
15. **The screen budget is a Stage 1 fact.** The convention at
    `shelltutor:576-580` is honoured by every Stage 1 screen (maximum 18)
    and by no stage-3-to-5 lesson except the intros; `stage4_lesson_3` is
    30 lines and `stage5_lesson_3` is 35 (`audit/2026-11-08/findings.md`
    O-J). The density audits that enforce the rule covered Stage 1 only.
14. **A learner must install Vim to finish.** Stage 5 requires `vim`
    (`shelltutor:1707`) while the project's rule is no installation beyond
    Bash (`AGENTS.md` §Work Rules). The course is a `vimtutor`
    prerequisite, so the dependency is intrinsic; the rule and the
    curriculum state it differently.

## 7. Evidence versus intent

### 7.1 Confirmed by committed evidence under `audit/`

- Every stage's gate can be cleared by the `careful-beginner` walk, under
  Bash 3.2.57 and 5.3.20 on macOS and Bash 5.2.21 on Ubuntu 24.04, with
  `.progress` removed at the end and no error signatures
  (`audit/2026-11-08/sim/all-slice2`, `all-slice2-bash32`, `all-linux`,
  each `result.tap` and `summary.md`).
- The escalation ladder's first rung ("Almost — you still need to") fires
  exactly once for a one-step miss at stages 2 and 4 and the gate then
  clears (`audit/2026-11-08/sim/second-try-stage2`, `second-try-stage4`).
- The pre-fix script showed F-010 and F-011 as `error-signature` events and
  the fixed script shows none (`audit/2026-11-08/sim/all/current-rc` versus
  `all-postfix/current-rc`; `audit/2026-11-07/findings.md`).
- The C-007 environment scrub keeps the practice shell alive under
  `TMOUT=5` with `HISTIGNORE` and `CDPATH` set, where the pre-hardening
  script auto-logged out (`audit/2026-11-08/slice2-comparison.md`).
- Tab completion in lesson 1.2 completes `echo p` to `echo poem.txt` under
  both Bash generations after the Readline contract
  (`audit/2026-11-08/slice2-comparison.md` §Readline and startup
  observations; `stage1-wp04*` bundles).
- Stage 1 screens fit the 20-line budget after the split; the maximum is 18
  (`audit/2026-11-08/stage1-density-followup.md`).
- The harness records which Bash ran the tutor; the committed post-WP-09
  bundle shows Bash 5.3.20 (`audit/2026-11-08/sim/all-current/current-rc/summary.md`),
  and the WP-09 report states a `/bin/bash`-first run recorded 3.2.57 and
  `echo $BASH_VERSION` at the practice prompt changed from 5.3.20 to 3.2.57
  across the fix (reported, not committed).
- Earlier: the BSD-sed gate verifier defect and its fix (F-008,
  `audit/2026-05-23/findings.md`); the Bash 5.3 startup hang and 3.2 rcfile
  loading (F-009, `audit/2026-07-14/findings.md`); the first-cycle
  inventory of entrypoints, stores and authority (`audit/2026-05-21/`).

### 7.2 Design intent only (no committed evidence yet)

- Human experience of the course: pacing, confusion, drop-off, and the
  45–60 minute estimate (`shelltutor:589`; `ROADMAP.md:131`). The Phase 2
  human walkthroughs are pending; the one macOS walk reported on
  2026-11-08 is recorded with its practice-shell Bash version unconfirmed
  (`audit/2026-11-08/findings.md` F-014; `STATUS.md` §Immediate Next Steps).
- The hint and worked-example rungs as experienced by a human; the harness
  exercises rung one only (`scripts/sim/README.md` §Personas). The
  third-rung behaviour was checked by a scripted pty run during WP-05 and
  reported, not committed (`docs/workplan/WP-05-gate-feedback.md`
  acceptance 3).
- The learner's recovery from "stuck in a full-screen program" and from
  Ctrl+C at the outer script (`shelltutor:105-108`): described in code
  comments and copy, not observed.
- Transfer to `vimtutor` and to the learner's own shell: the course's
  purpose (`ROADMAP.md` §Framing decision), unmeasured by design.
- The "confused-novice" behaviours and confusion events
  (`docs/simulation-design-plan.md` §Confusion Events, §Deferred).
- The research references' claims about pacing, feedback and tone are
  cited as inputs (`docs/audit/references/README.md` separates their
  objective and judgment content); they are not evidence about this
  tutor's learners.

### 7.3 Confirmed by code reading in this document, not by evidence

The discrepancies in §6 items 3, 4, 5, 6 and 15, and the drop-off risks in
§3.4, are established by reading the script at the cited lines. They are
not observed behaviours of learners and should be treated as design facts
awaiting a human check.

## Cross-references

- `docs/contracts.md` — the interface this document describes as
  contracts.
- `docs/simulation-design-plan.md`, `scripts/sim/README.md` — the
  observation apparatus.
- `ROADMAP.md` Phase 3 and Amendments — the curriculum's design record.
- `STATUS.md` — current truth; where this document and STATUS disagree,
  STATUS wins and this document is corrected.
- `docs/workplan/README.md` — the decisions (D-01 to D-18) behind the
  2026-11 landings cited above.
- `audit/2026-11-07/findings.md`, `audit/2026-11-08/findings.md` — the
  defects and observations referenced.
