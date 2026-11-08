---
title: shelltutor Direction Decisions and Expansion Plan — November 2026
category: planning
component: direction-decisions
status: active
version: 0.2.0
last_updated: 2026-11-08
tags: [design, direction, decisions, roadmap, modules, curriculum, scope, evidence-tiers]
priority: high
---

# Direction Decisions and Expansion Plan — November 2026

This brief answers the eight decisions in the direction brief ("Design
Direction — November 2026 (draft)", §6), sets the sequencing of the work
that follows, and defines the standard under which new curriculum is
built. It is directive: the operator committed it to `main` on 2026-11-08. It replaces the path the direction brief
describes in §7 (decision session → ROADMAP phase → contract updates →
work packages) with this document plus work packages.

Two documents are cited throughout: **the baseline**
(`docs/design-description.md`, `main` at `bd841ae`) and **the direction
brief** (`docs/design-direction-2026-11.md`, now superseded by this
document). Section references are to those
unless a file is named.

## 0. Governing principle: two evidence tiers

The cost of this project is not lesson content. It is the evidence
discipline applied to every change: a copy edit touches the lesson
function, the dispatcher array, sentinels, the persona, a harness run, a
human-read comparison, a summary, a work-package report and often a
density audit (baseline §2.5, §6 item 12; direction brief §4, "the
evidence discipline scales linearly with content"). That discipline
found F-009, F-010, F-011 and F-014 and stays in force where it earned
its keep. It does not become the default price of a new lesson.

**Rule.** The five core stages, the finale and everything in
`docs/contracts.md` keep the current standard (the **core standard**:
the fitness functions in `CONTRIBUTING.md`, the evidence-bundle
discipline of `docs/simulation-design-plan.md`, density review for any
changed screen). New curriculum ships as **modules** under the **module
standard** of §5. A module is never held to the core standard unless the
operator folds it into the core line.

**Corollary for agents.** No further analytical documents about the
repository are written in this cycle. The baseline is the analysis; this
brief is the decision record; everything after it is a work package, a
lesson, or a findings summary.

## 1. The eight decisions

Numbered as in direction brief §6. Each item records the decision, the
reason, and what it rules out.

### D1. Other shells: concept-only

One screen names the shells a learner will meet (bash, zsh, fish, sh),
shows how to tell which one is running (`echo $SHELL`, `echo $0`,
`command -v zsh fish`), and separates what differs (configuration
syntax, prompts, completion) from what is the same (the programs, paths,
pipes, redirection). No second practice shell, no second rcfile
contract, no second sentinel set (direction brief T2).

Rules out: multi-shell practice; gate-and-fallback live demos of zsh or
fish.

### D2. Personalising the environment: explain and transfer

The `env` module (§6) teaches variables, `export`, `PATH` and the prompt
inside the practice shell, lets the learner change `PS1` at the prompt
and watch it revert at the next screen, names why (each screen is a
fresh shell, `shelltutor:453-457`; C-007 neutralises rc files on
purpose), and ends by handing the learner the exact lines for their real
`~/.bashrc` or `~/.zshrc` with the instruction to quit the tutor and do
it in a new terminal.

Rules out: a persistent sandbox rc file across screens (a C-007 change
that would teach a thing that does not transfer); any read or write of
the learner's real rc files by the tutor (FF-002; `AGENTS.md` §Work
Rules).

### D3. Agent-aware: a reframe and one screen, not a module

The direction brief's narrow reading (T6) is adopted. The habits the
course already teaches are the habits of reviewing an agent's shell
work: read a command before it runs, predict its effect, know the
working directory, recognise destructive verbs, read output rather than
skim it. Two changes carry it:

- a new lesson 1.5 appended to Stage 1, extending the terminal → shell →
  program model of 1.4 (`shelltutor:710-732`) to agent → shell →
  program: an AI that runs commands types into the same shell you do,
  and you can read what it typed the way you read your own;
- one sentence in 3.3 (`rm`) and one in 4.3 (`>`): this is why a command
  is read before anyone runs it, you or an agent.

The tutor does not call, simulate or integrate any agent (`AGENTS.md`
§Work Rules). The harness is an implementation detail, not a teaching
device.

### D4. Course shape: core plus modules; `vimtutor` stays the core finale

Shape 2 of direction brief §5. The five stages, their gates, the finale
and C-001's `[N]` argument are unchanged. Modules are entered by name
(`./shelltutor shells`), stand alone, require nothing passed, and save
nothing. Reasons: threads invalidate sentinels, density reviews and
evidence bundles for every stage they touch (baseline §6 item 12); a
longer line changes C-001 and moves the finale; modules leave existing
evidence valid and can be shipped one at a time.

Rules out: a Stage 0 (lesson 1.4 and the `shells` module cover "what is
a shell"); stages 6+; threads other than D3's single appended screen and
two sentences.

### D5. Audience: children first changes behaviour, not tone

The tone rules stand ("concise, concrete, task-focused,
non-condescending, low on praise-heavy copy",
`docs/simulation-design-plan.md` §Pedagogy And UX). They are the right
register for children. What changes for children are behaviours the
baseline already lists as drop-off risks (§3.4): recall with no exit,
follow-up prompts with no navigation, no pause after a stage. Those are
fixed in Phase B. The 45–60 minute promise (`shelltutor:587-589`) is
reworded after Phase A from observed sittings, not before.

Rules out: praise copy, points, badges, mascots, fiction (baseline §1.11
holds for children); a tone rewrite.

### D6. Install policy: concept-only unless in the base install

A program is demonstrated live only if it is present in the base install
on every platform the project supports (`ls -l`, `chmod`, `ps`, `env`,
and the builtins `jobs`, `fg`, `bg`, `kill` are; `tmux`, Emacs, `fish`,
and `zsh` on Linux are not). A program that is not present gets a
concept screen: what it is, what it is for, `command -v <name>` to check
for it, and nothing else. `CONTRIBUTING.md` §Portability Rules and
FF-004 apply unchanged.

### D7. Linux concepts: processes, permissions, environment in; the rest out

In, as modules: processes and job control (Ctrl+Z, `jobs`, `fg`, `bg`,
`kill`; all work in the practice shell, direction brief T4);
permissions as observable capabilities (`ls -l`, `chmod`;
`educational-design-research.md`); environment (`env`, `export`, `PATH`
as a list). Out, and added to `README.md` §Non-Goals explicitly: users
and groups, shell scripting, sysadmin, networking, editor internals
beyond the concepts of buffer, mode, pane and session.

### D8. Pace evidence: observer notes, no timing store

Pace is observed by a human sitting beside the learner (the Phase 2
mechanism, `docs/phase2-walkthrough-checklist.md`) and summarised into
findings. The tutor records no timing; no new store is added under
C-003; no transcripts are committed (`docs/simulation-design-plan.md`
§Evidence Locations). Revisit only if modules make the course long
enough that mid-stage resume (baseline §6 item 10) is observed to
matter.

## 2. Sequencing

Four phases. A and B precede any module. The operator's actions and the
agent's are separated: the agent produces runbooks, code and summaries;
the operator runs commands and sits with learners.

### Phase A — Human walkthroughs (operator; agent produces one template)

The baseline's largest gap is §7.2: no committed human evidence. One
macOS walk is recorded, before the F-014 fix, with the practice-shell
Bash version unconfirmed; it is to be repeated (baseline §2.6).

Agent:

- Write `docs/walkthrough-notes-template.md`, one page: learner role
  (child / adult beginner / adult with some shell; no names), platform
  and `--info` output including the Bash version, and per stage: pauses
  the observer judged long, inputs the tutor rejected (verbatim), moments
  the learner asked for help, wall-clock minutes, where they quit.
  Nothing else.
- Nothing else in Phase A.

Operator:

- Run at least three walkthroughs on the post-WP-09 script, one learner
  per sitting, as many stages per sitting as the learner chooses. On a
  shared machine set `SHELLTUTOR_HOME` per learner (baseline §1.11, "one
  learner per sandbox").
- Observer protocol (default, to confirm; Q4): do not intervene until
  the learner asks or has been silent for two minutes; when you
  intervene, write down what you said.
- Include one walk on macOS `/bin/bash` 3.2 to close the F-014 repeat.

Output: `audit/<date>/walkthroughs.md`, a findings-style summary (F-nnn
for defects, O-nnn for observations), no names, no transcripts.

Exit: three summarised walks; a list of rejected-but-reasonable recall
answers; the §3.4 risks re-ranked by what was observed.

### Phase B — Core dead ends (agent writes WPs; core standard)

Three packages, scoped to the risks the baseline ranks highest (§3.4).
All are core-standard changes; all are small.

**WP-10 Recall navigation and ladder** (risks 1 and 3; baseline §6 item 1)

- `ask_question` and the Stage 1 follow-up prompts accept `show`
  (redisplay) and `quit` (clean exit with the farewell; resume restarts
  the stage as today). Today both are read as answers
  (`shelltutor:477-502`, `869-882`).
- An attempt counter. Attempt 2 adds a per-question hint where one is
  written; attempt 3 and later add a line saying `quit` is available and
  the stage can be retaken. No reveal (Q1).
- Accepted-answer lists widened from the Phase A list, not from guesses.
- The Stage 1 `pwd` comparison tolerates a symlinked path (compare
  logical and physical forms).
- C-006 amended: the recall escalation order joins the task escalation
  order as contractual.

**WP-11 Stage-cleared screen** (risk 5)

- One screen after each passed gate: `✓ Stage N cleared.`, then the
  stage's commands and keys in the finale's list style (≤ 8 lines; Q3),
  then `▶ Type next for Stage N+1, or quit to stop here.` Five new
  sentinels; one added `next` in every persona that passes a gate; new
  evidence bundle.
- Fold in the two wording fixes from baseline §6 items 3 and 4: `--info`
  says the finale "names" `vimtutor` rather than "hands off"
  (`shelltutor:275`), and stops claiming lessons 3.2 and 5.1 skip
  anything (`shelltutor:261`, `266`).

**WP-12 Agent-aware beat** (D3)

- Lesson 1.5 appended to the Stage 1 array; one sentinel; one `next` in
  each persona; Stage 1 density check against the 20-line budget
  (`shelltutor:576-580`).
- One sentence each in 3.3 and 4.3; headings unchanged, so no sentinel
  change.

Exit: `careful-beginner` and `second-try` green on macOS (3.2 and 5.x)
and hosted Linux; bundles committed; `STATUS.md` updated. Phase A
findings that are defects are fixed here or filed.

### Phase C — Module infrastructure (agent; lands with the first module)

**WP-13 Module entry and standard**

- C-001 extended: `./shelltutor <module>`, where `<module>` is a
  lowercase word from a fixed list in the script; `-h` lists modules
  under their own heading; an unknown word takes the existing
  bad-argument path; `--info` unchanged.
- C-003 extended: a module's fixtures live in `$SANDBOX/<module>/`,
  seeded on entry and self-healing like stage folders.
- Modules save nothing: no `.progress` change, no marker file. A module
  ends on a `✓ <module> cleared.` screen and exits 0.
- Harness: a module persona is declared as a table (lesson count, gate
  actions) and expanded to `next × N` plus the gate script by
  `persona.py`; sentinels are the screen headings by convention, with no
  hand-maintained list. If a rendered-height check (lines between
  `clear` and the prompt ≤ 20) is cheap to add to the driver, add it; it
  replaces the density review for modules (Q5).
- `CONTRIBUTING.md` gains §Module standard (the text of §5) and the
  lesson-screen template (§6).
- `AGENTS.md` §Identity and `README.md` §Non-Goals updated per §7.

Phase C has no learner-facing output of its own; it lands in the same
commit series as the first module.

### Phase D — First modules (agent; module standard)

Default order `shells`, then `env` (Q2); the operator may swap them
after Phase A according to what learners asked for. Outlines in §6.
Each is three to five screens and one gate. After both have been walked
by at least two humans, the operator decides whether `processes` and
`permissions` follow.

## 3. What is unchanged

- The five stages' content, except WP-11's new screen, WP-12's lesson
  1.5 and two sentences, and WP-10's widened answer lists and hints.
- The `vimtutor` finale and its handoff-by-pointer (baseline §1.7).
- Stage 5's dependence on Vim (baseline §6 item 14): intrinsic to a
  `vimtutor` preparer; modules do not depend on Vim.
- C-002 exit codes, C-004, C-005, C-007.
- Minimalism as default: one idea per screen, the 20-line budget, the
  density rule, for core and modules alike.
- The rules: user-agnostic, safe on a stranger's machine, no network, no
  privilege, no installation beyond Bash for lessons (`AGENTS.md`).
- The static gates FF-001 to FF-008 run on every change, core or module;
  they are automatic and cheap.

## 4. Deferred, with the condition that reopens each

| Item | Deferred because | Reopens when |
| --- | --- | --- |
| Lessons as source files, built into the single shipped script | A refactor with its own evidence cost; pays back only across many lessons | The operator commits to three or more modules beyond `shells` and `env` |
| `processes` and `permissions` modules | Walk the first two first | Two human walks of `shells` and `env` are summarised |
| Concept screens on tmux and Emacs | Belong inside `processes` (panes, sessions) and a later editor module (buffers, modes, chords) | Those modules are scheduled |
| Module progress persistence | Modules are short and save nothing | A module grows past one sitting |
| Timing store under C-003 | D8 | Mid-stage resume is observed to matter |
| Multi-shell practice | D1 | Not planned |
| Stage 0 | D4 | Not planned |

## 5. The module standard

A module **requires**:

1. One function block in the script (intro, lessons, verifiers, gate,
   runner) following the stage pattern, and a line in the module list.
2. Fixtures under `$SANDBOX/<module>/` if any, seeded and self-healing.
3. Screens that fit the 20-line budget and end in a `▶` line; headings
   are the sentinels.
4. One gate: three recall questions with WP-10's navigation and ladder,
   plus a task verified from state or history where the content allows
   one.
5. One persona table (lesson count, gate actions).
6. One green harness run on the contributor's macOS and one on hosted
   Linux via the existing non-gating workflow; `result.tap` and
   `summary.md` committed, the rest of the bundle not.
7. The static gates FF-001 to FF-008 green.
8. A three-line entry in `STATUS.md`.

A module **does not require**: a density audit (the budget is checked
mechanically or by the author), a work-package report, a comparison
summary, a findings file unless a run goes red, a full committed
evidence bundle, a ROADMAP amendment.

A module stays at this standard. It moves to the core standard only if
the operator folds it into the core line.

**Agent context rule.** Writing a module reads `AGENTS.md`,
`CONTRIBUTING.md` §Module standard, the lesson-screen template, and one
existing stage block as a model. It does not read the whole script or
the docs tree.

## 6. Lesson-screen template and module outlines

### Template

```
<heading in H1 colour>                      # the sentinel

<one idea, in two to six lines of plain prose>

  <command>        # <what it will print or do>
  <command>        # <aside>

<optional: one line beginning "Notice that">

▶ <the one thing to do>, then type next.
```

Twenty lines including blanks, so the prompt stays visible on 24 rows.
One idea per screen; two concepts or two distinct actions is a split
candidate (`docs/simulation-design-plan.md` §Pedagogy And UX).

### `shells` (D1; direction brief T1, T2)

1. What a shell is, again: the program that reads your line, finds the
   program you named, runs it, and shows what it printed; it is itself a
   program (`echo $SHELL`, `echo $BASH_VERSION`, `ps`).
2. Other shells exist: bash, zsh, fish, sh; `command -v zsh fish`; what
   differs and what is the same.
3. Login shell versus the shell you are in now; why this tutor runs Bash
   whatever your login shell is (`--info` already says so,
   `shelltutor:216-217`).

Gate: recall ×3; task shape: find out whether `zsh` is installed and
record the answer in a file, verified by history (`command -v zsh`) and
file content.

### `env` (D2; direction brief T3)

1. Variables: `echo $HOME`, `name=value`, `echo $name`, `env | head`; a
   variable lives in this shell.
2. `export` and child programs: `export name`, `bash -c 'echo $name'`.
3. `PATH` is a list: `echo "$PATH" | tr : '\n'`, `command -v ls`; why
   Stage 4's `command -v` worked.
4. The prompt is a variable: `PS1='$ '`; watch it change; type `next`;
   watch it revert, and read why (fresh shell per screen; C-007).
5. Where this lives for real: `~/.bashrc` or `~/.zshrc`, the two lines
   to add, and "quit, open a new terminal, do it there."

Gate: recall ×3; task: set and export a variable and prove a child
process sees it (`bash -c 'echo $name' > seen.txt`), verified by file
content and history.

## 7. Edits to existing documents

| Document | Edit | When |
| --- | --- | --- |
| `ROADMAP.md` | A dated phase recording Phases A–D of §2 and the deferred table of §4 | On commit of this brief |
| `STATUS.md` | Immediate next steps = Phase A; then per phase | On commit, then per phase |
| Direction brief | `status: draft` → `superseded`, pointing here | On commit |
| `AGENTS.md` §Identity | "a vimtutor prerequisite course" → a shell course whose five-stage core hands off to `vimtutor`, with stand-alone modules; add the two-tier rule of §0 | WP-13 |
| `README.md` §shelltutor, §Non-Goals | Same reframing; non-goals gain users and groups, networking, multi-shell practice, editor internals beyond concepts; "sysadmin" and "scripting" stay | WP-13 |
| `docs/contracts.md` | C-006 recall escalation order | WP-10 |
| `docs/contracts.md` | C-001 module argument; C-003 `$SANDBOX/<module>/` | WP-13 |
| `CONTRIBUTING.md` | §Module standard; lesson-screen template; sentinel-by-heading convention | WP-13 |
| `docs/simulation-design-plan.md` §Pedagogy And UX | Note that children are named learners and the tone rules are unchanged | WP-13 |
| `shelltutor:587-589` (welcome) | Time estimate reworded from Phase A sittings | WP-11 or later |

## 8. Open questions for the operator

Defaults apply if unanswered.

- **Q1** Recall ladder, attempt 3 and later: reveal the accepted forms,
  or only offer `quit`? **Resolved 2026-11-08 (A1.1, A1.6):** no reveal; one
  ladder for all fifteen questions; the attempt-3 line states three facts.
- **Q2** First-module order: `shells` then `env`, or the reverse?
  Default: `shells`; decide after Phase A.
- **Q3** Stage-cleared recap: commands and keys only, or also the
  "ideas" the finale lists? **Resolved 2026-11-08 (A1.4):** commands and
  keys, ≤ 8 lines; four screens (stages 1–4), Stage 5 flows into the finale.
- **Q4** Observer protocol in Phase A: the two-minute rule above, or
  another? Default as written.
- **Q5** Rendered-height check in the harness: add it in WP-13 if under
  a day's work, otherwise the author counts? Default: yes if cheap.

## 9. First actions on commit

1. Apply the "On commit" rows of §7.
2. Write `docs/walkthrough-notes-template.md` (Phase A, agent).
3. Stop. Phase B begins when `audit/<date>/walkthroughs.md` exists.

## Amendments

### A1 — Phase B refinements (2026-11-08)

Recorded from the Phase B consult after Phase A's template landed. A1
resolves Q1 and Q3, adds one decision (D9), and refines WP-10 to WP-12.
Where A1 and §2 differ, A1 governs.

#### A1.1 Q1 resolved: one recall ladder, no reveal, no special cases

- Three rungs, identical for all fifteen recall questions: attempt 1
  the existing message; attempt 2 the question's hint; attempt 3 and
  later the hint plus one fixed navigation line (A1.6). No reveal of
  accepted forms at any rung.
- No per-question variation. Questions that list their options in the
  question text are not re-shown their list at attempt 3; `show` does
  that on demand. One code path, one sentinel pattern, one persona
  behaviour.
- The attempt counter is per question and resets at the next question.
  `show` redisplays the question text only and does not advance the
  counter. `quit` exits with the farewell; per-stage resume is
  unchanged (baseline §6 item 10).
- Every recall question gets a hint: fifteen one-line hints that name
  the concept without using an accepted answer. An uneven ladder would
  reproduce the asymmetry the baseline flags in §6 item 1.
- Accepted-answer lists are widened only from the Phase A
  rejected-answer list. WP-10 does not guess at widenings.

#### A1.2 Hint-leak check

A static check: for each recall question, no accepted answer string
appears in its hint, case-insensitive. Add it to `scripts/smoke-test.sh`
(FF-006a) or as its own fitness function; the agent picks the number
and adds the row to `CONTRIBUTING.md` §Fitness functions. This turns
"the hint names the concept without the word" from a copy rule into a
gate.

#### A1.3 Recall rungs in committed evidence

The task ladder's rungs 2 and 3 are design intent only (baseline §7.2)
because no persona reaches them. WP-10 does not repeat that for recall:
`second-try` gains two deliberate misses on one recall question at one
stage, so the hint rung and the navigation rung each appear once before
the correct answer. The oracle asserts each sentinel exactly once
(`run.py`, the same shape as the existing "Almost — you still need to"
assertion).

#### A1.4 Q3 resolved and WP-11 refined: four cleared screens

- Stages 1 to 4 get a cleared screen; Stage 5's gate flows into the
  finale as today, which is already the stopping point and the recap.
  Four new sentinels, not five.
- Content: `✓ Stage N cleared.`, then the stage's commands and keys in
  the finale's list style, at most eight lines, then
  `▶ Type next for Stage N+1, or quit to stop here.`
- Rendered by one function, `stage_cleared N`, called from `main`
  where the next stage's banner currently fires at once
  (`shelltutor:2082-2084` at baseline), with the recap text as
  per-stage data. Not five copies inside the `run_stageN` gates.
- It is a lesson-mode screen: lesson footer; `show` and `prev`
  redisplay it; `check` gives the existing one-line note.
- WP-11 keeps the two `--info` wording fixes of §2 (baseline §6 items 3
  and 4).

#### A1.5 WP-12 confirmed: lesson 1.5 is read-only

Lesson 1.5 has no commands; it ends in `▶ Type next.` The Stage 1
walk, gate and history checks are untouched, and the density follow-up
is one row. Watch item for the second walkthrough round, not a change
now: two concept screens back to back (1.4, 1.5) before the Stage 1
gate.

#### A1.6 The navigation line says what happens

The attempt-3 line states three facts, in whatever wording C-006 copy
review settles on: passed stages are saved; `quit` leaves now and the
next run starts this stage from its first lesson; `show` repeats the
question. "The stage can be retaken" is not used: a child reads
"retake" as losing something. The three facts are contractual under
C-006; the wording is not.

#### A1.7 Drift WP-10 must close

- The code comment at `ask_question` ("No hints, no answer reveal",
  `shelltutor:466` at baseline) and any sentence in the welcome,
  `README.md`, `ROADMAP.md` or `docs/contracts.md` that says recall has
  no hints become false when WP-10 lands and are corrected in the same
  package. Baseline §6 is a list of this kind of gap; WP-10 adds none.
- Stage 1 `pwd` comparison: trim surrounding whitespace, then accept
  the typed path if it equals either the logical `$SANDBOX/stage1` or
  its `pwd -P` form.

#### A1.8 D9: host user name redacted from committed harness artifacts

The harness fixes `HOME`, `LC_ALL`, `TERM` and geometry but cannot fix
`whoami`, so the host login name appears in `terminal.jsonl` for every
committed macOS bundle (hosted Linux shows `runner`). Decision: the
bundle writer treats the host user name as a host input, like temp
paths, and replaces it with a fixed token before writing any file that
is committed. Lands before, or in the same series as, the first new
bundle (WP-11). Rewriting history for existing bundles is the
operator's call; the default is no rewrite, since the value is a login
name and not a credential. Record the rule as a D-nn decision in
`docs/workplan/README.md` alongside D-03.

#### A1.9 Script freeze during Phase A; drafting allowed

- No change to `shelltutor` lands until `audit/<date>/walkthroughs.md`
  exists. Every Phase A walk runs on the same revision so the findings
  are comparable; that is the premise of the evidence discipline.
- WP-10, WP-11 and WP-12 may be drafted during Phase A. WP-10's
  answer-list widening section is left marked "[from Phase A]". The
  hint copy (A1.1) may be drafted now; the Phase A rejected-answer list
  may revise it.
- Landing order once Phase A is summarised: WP-11, WP-12, WP-10. The
  three are independent; the order is by learner value, not by risk.

#### A1.10 Release placement confirmed

v0.1.0 follows Phase B and precedes Phase C: the tag is the five-stage
core with human evidence behind it. Modules are 0.2.

#### A1 — edits this amendment implies

| Document | Edit | When |
| --- | --- | --- |
| This document §8 | Q1 and Q3 marked resolved, pointing at A1.1 and A1.4; Q2, Q4, Q5 remain | On commit of A1 |
| `ROADMAP.md` Phase 5 | WP-11 is four screens; A1.9 freeze and landing order; D9 | On commit of A1 |
| `STATUS.md` | Next steps: Phase A running; WP-10 to WP-12 drafted, none landed; D9 before first new bundle | On commit of A1 |
| `docs/workplan/README.md` | D9 recorded; WP-10 to WP-12 listed as drafted | On commit of A1 |
| `CONTRIBUTING.md` §Fitness functions | Hint-leak check row | WP-10 |
| `docs/contracts.md` C-006 | Recall ladder: three rungs and the three facts of A1.6 are contractual; wording is not | WP-10 |
| `scripts/sim/persona.py`, `run.py` | `second-try` recall misses and oracle (A1.3) | WP-10 |
| `scripts/sim/` bundle writer | Host user name redaction (D9) | Before WP-11's bundle |

## Cross-references

- `docs/design-direction-2026-11.md` (superseded) — the intent this brief
  decides on; its §6 numbering is reused as D1–D8.
- `docs/design-description.md` — the baseline; §3.4 (drop-off risks),
  §6 (tensions), §7.2 (evidence gap) drive Phases A and B.
- `docs/contracts.md` C-001, C-003, C-006, C-007 — the contracts this
  brief extends or leaves alone.
- `docs/phase2-walkthrough-checklist.md` — Phase A's method.
- `CONTRIBUTING.md` §Fitness functions, §Portability Rules — gates that
  apply unchanged to core and modules.
- `docs/workplan/README.md` — the work-package form Phases B–D follow.
