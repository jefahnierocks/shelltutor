---
title: shelltutor Direction Decisions and Expansion Plan — November 2026
category: planning
component: direction-decisions
status: active
version: 0.15.0
last_updated: 2026-11-10
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

**WP-14 Stages 1–2 grounding** (A2) and **WP-15 screen chrome** (A3) were
added on 2026-11-08; landing order after Phase A is WP-15, WP-11, WP-12,
WP-14, WP-10 (A2.6). All five are drafted during Phase A.

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
Each is three to six lesson screens (amended by A15; it was three to five) and one gate. After both have been walked
by at least two humans, the operator decides whether `processes` and
`permissions` follow.

## 3. What is unchanged

- The five stages' content, except WP-11's new screen, WP-12's lesson
  1.5 and two sentences, and WP-10's widened answer lists and hints.
  *Qualified by A2 (2026-11-08): Stages 1 and 2 are reopened for sequencing
  and grounding (WP-14); Stages 3 to 5 are not. A3 adds screen chrome
  (WP-15), rendering only.*
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
  a day's work, otherwise the author counts? Default: yes if cheap. **Resolved: landed as WP-13 commit A (f973eb0), informational,
  budget 22 rendered rows.**
- **Q6**–**Q8** see amendment A3 ("Open questions added"); defaults apply.

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

### A2 — Stages 1–2 reopened: the grounding package (2026-11-08)

Recorded after Phase A sitting 1 (`audit/2026-11-08/walkthroughs.md`,
`1aea23b`). A2 revises §3's line that the five stages' content is fixed
apart from WP-10 to WP-12: Stages 1 and 2 are reopened for sequencing
and grounding. Stages 3 to 5 are not. The baseline's design intent
(mastery gates, minimalism, no praise, transfer-first) is unchanged.

#### A2.1 How sitting 1 is read

- The learner data (adult with some shell; Bash 5.3 via the shebang;
  quit at 2.1 after eight minutes) is one non-target data point,
  confounded by known material and by friction (F-015, O-K). It says
  little about a beginner.
- The observer notes O-L, O-M, O-N are design review by a teacher and
  stand without further sittings. They share one root: Stages 1–2 give
  verbs before the thing the verbs act on. Baseline §4.3's order within
  a stage (recognition → action → model) is reversed for a novice in
  these two stages.
- O-M is read-ahead: the learner stopped at 2.1 and never met 2.3. Label
  it observer review, not learner observation, in the findings.

#### A2.2 Decision: a grounding package, core standard

A new package, WP-14 (WP-13 is module infrastructure; the module
packages drafted earlier as WP-14/WP-15 are renumbered WP-16 `shells` and
WP-17 `env`), re-sequences
Stages 1 and 2 on one principle: **model before verbs, every model
anchored in something visible on screen.** Core standard: sentinels,
personas, density rows, full bundle. Drafted during Phase A; landed
after it (A1.9).

Not chosen: leaving the core alone and letting the `shells` module carry
O-L. A learner who quits at 2.1 never reaches a module.

#### A2.3 Scope of WP-14

- *Stage 1, the shell made visible.* Replace the abstract 1.4 with
  something the learner does. Candidates, agent to pick one after an
  FF-004/FF-008 check: type `date`, then `dtae`; the shell reports it
  could not find a program by that name, so the shell is the thing that
  finds and runs programs (the harness's error-signature scan must
  expect the deliberate error on that screen). Or `echo $BASH_VERSION`:
  the thing you are typing into is a program called bash, with a
  version like any program.
- *Stage 2 opens with position.* A new first screen draws the sandbox as
  a tree (fixtures are constants, C-003, so the drawing is exact) with
  "you are here", names the current directory, and introduces `pwd` as
  "where am I". Then `ls`, then `cd`; `.`, `..`, `~` arrive after the
  tree as names for here, up one, home.
- *File versus folder.* `ls -p` (or `-F`) marks directories with a
  trailing `/`. `ls -l` is removed from 2.1; it belongs with permissions
  (D7). Grep for downstream dependence first; the baseline says
  file-versus-directory is never measured (§4.4).
- *In-lesson checks* take the course's existing form, predict then run
  (`shelltutor:1024`, `1494`). No typed-answer prompts inside lessons.
- Stage 1 and 2 gate criteria are unchanged. Recall questions may be
  reworded to match the new screens.
- Watch item for the second walkthrough round: two concept screens back
  to back before the Stage 1 gate (the new 1.4 and WP-12's 1.5).

#### A2.4 F-015 and the follow-up prompts (WP-10)

The WP-10 draft's fix stands: the question asks for the day alone, with
an example, and the verifier accepts any answer containing the day as a
word. Add: on a mismatch at the Stage 1 follow-ups, re-ask only the
mismatched item; do not restart the task. "Had to run check several
times" was the restart compounding the wording defect.

#### A2.5 O-K, Ctrl+L

Check whether lesson 1.2 teaches Ctrl+L. Either way, one sentence in 1.2
is the fix: "Ctrl+L clears the screen; type show to bring the lesson
back." The `bind -x` rebind stays a candidate requiring harness proof on
3.2 and 5.x, not a default: Ctrl+L clearing the screen is real Bash
behaviour and the practice shell is meant to behave like real Bash.

#### A2.6 Landing order after Phase A

WP-15 (A3), WP-11, WP-12, WP-14, WP-10. WP-10 last because its hint copy
for Stages 1–2 depends on WP-14's final screens and its answer lists
depend on Phase A. All five are drafted during Phase A; none lands
before `walkthroughs.md` records three sittings.

#### A2.7 Sittings 2 and 3

At least one is a child (D5). The 3.2 sitting is invoked as
`/bin/bash ./shelltutor`; the template's invocation and `--info` fields
carry the actual command and the pasted `--info` output. Sitting 1
recorded `/bin/zsh` and `./shelltutor` there, which is how the 5.3 run
went unnoticed until the Bash line was read.

### A3 — Screen layout direction (2026-11-08)

Recorded from the design canvas "shelltutor terminal UI — screen
layouts" (eight boards; the operator holds the link). The agent works
from this text; the canvas is the operator's visual reference. Lands as
its own package, WP-15 "screen chrome", rendering only: no lesson-body
changes, so one comparison reads "the look changed, nothing else". It
precedes WP-11 so every later screen is authored and evidenced against
the final chrome once.

#### A3.1 The panel model

Every tutor screen is a panel between two rules. Everything below the
lower rule is the real shell and is never coloured by the tutor. Rows,
top to bottom: header rule; blank; title (H1); body; `▶` line (INSTR);
rule; footer. The whole panel, header through footer, is ≤ 20 rows. The
chrome costs two rows over today's screens (header, lower rule); Stage
1's current maximum is 18 (`audit/2026-11-08/stage1-density-followup.md`),
so screens at 19–20 lose a blank line, and the density check counts the
chrome.

Rationale: the panel is the tutor, one program; the prompt beneath it is
the shell. Terminal → shell → program becomes visible on every screen,
which is the substance O-L said lesson 1.4 lacked.

#### A3.2 Header rule

`─ shelltutor ─ Stage N · <stage title> ───────── ●◉○○○  N.k ─`. The
name is INSTR, the stage title DIM, the rule RULE. Dots: `●` OK for
stages passed, `◉` INSTR for the current stage, `○` DIM for stages not
reached. At a gate the lesson number reads `task`; on the cleared screen
there is no current stage (`●●○○○`). The dots are position, not score,
and stay inside baseline §1.11.

Fixed 80 columns. No `tput cols` or `COLUMNS` probing: the welcome
already asks for 80×24, the harness fixes geometry, and a wider terminal
simply shows a shorter rule.

#### A3.3 Footer as a key-hint bar

One row, DIM with the words in KEY, the mode's verb first:

- lessons: `next ▸ go on   show ▸ this screen again   prev ▸ back   quit ▸ save and leave`
- gates: `check ▸ test your work   show ▸ the task again   quit ▸ save and leave`
- cleared: `next ▸ Stage N+1   quit ▸ stop here, place saved   show ▸ this screen again`

Same content as today's footer (`shelltutor:368-376`), read faster. The
welcome shows the bar before screen 2 teaches the words; intended.

#### A3.4 Tutor speech inside the shell stream

Gate feedback keeps today's non-clearing behaviour (`skip_screen`) and
is marked by a `┃` bar in INSTR at column 1 on every line of the block.
The delta is a checklist: `✓` OK for what the gate saw done, `○` DIM for
what it did not, with a short `not yet: <what it sees instead>` in
EM/DIM on the undone line, then one line saying what to do and to type
`check` again. This replaces the prose list under "Almost — you still
need to:" (`shelltutor:542-546`); the `second-try` oracle's sentinel
moves with the new wording.

#### A3.5 Stage-cleared screen (WP-11; refines A1.4)

Title `✓ Stage N cleared` (OK tick, H1 text); "You can now:"; the
stage's commands in CMD, aligned in a column, each with a DIM gloss
(≤ 8 lines); "Next: Stage N+1 · <title>" in DIM;
`▶ Type next for Stage N+1, or quit to stop here. Your place is saved.`

#### A3.6 Colour roles → ANSI

The script's existing roles (`shelltutor:88-99`) plus one. The tutor
emits codes; the learner's terminal chooses the colours; the canvas's
hexes are one dark theme's rendering.

| Role | ANSI | Marks |
| --- | --- | --- |
| H1 | 1;97 | screen title |
| SUB | 36 | a concept being named |
| CMD | 92 | something you can type |
| KEY | 95 | a key or chord; the navigation words |
| DIR | 94 | a path or folder |
| EM | 91 | a warning; something irreversible |
| INSTR | 93 | the `▶` line, the header name, the `┃` bar |
| DIM | 90 | asides, footer hints, unreached dots, stage titles |
| OK | 92 | `✓` passed, `●` stage done |
| Q | 96 | a recall question |
| RULE (new) | 90 | box drawing only, never text |

#### A3.7 Glyphs and the plain path

UTF-8 glyphs: `▶ ✓ ● ◉ ○ ▸ ◀ ─ │ ┃ ├ └ ╭ ╮ ╰ ╯ ┌ ┐ ┘`. ASCII
substitutes: `> ok # * - > < - | | | |` and `+` for every corner. The
substitution is tied to the existing plain-text path (`NO_COLOR` or
non-TTY, `shelltutor:100-103`) and to an explicit `SHELLTUTOR_ASCII=1`,
not to locale detection: the harness runs under `LC_ALL=C` and its
sentinels already contain `▶` and `✓`, so a locale-triggered fallback
would break every green run. Board 08 says "non-UTF-8 locale"; this
paragraph corrects it.

#### A3.8 Content proposals carried by the boards

These are content decisions, not chrome. Each lands in the package
named, and each is a default the operator can overrule (Q7, Q8).

- The welcome carries the authority sentence on screen ("Commands you
  run yourself have your full authority: this is the real thing, not a
  simulation"), resolving operator question O-3 as yes. WP-15.
- Gate task screens at stages 2–4 drop the pre-task hint line and say
  what the gate checks instead ("that the folder exists, and how you
  got there"). The ladder's rung-2 hint takes the pre-hint's place, so
  fading runs forward (baseline §6 item 7). WP-10.
- `ls -p` in place of `ls -l` (A2.3). WP-14.
- Stage titles on the boards ("First commands", "Where things are",
  "Making and changing files") and the path `~/shelltutor-sandbox` are
  illustrative; the script's titles and `$SANDBOX` are used.

#### A2/A3 — edits implied

| Document | Edit | When |
| --- | --- | --- |
| This document §3 | "five stages' content unchanged" qualified: Stages 1–2 reopened per A2 | On commit |
| This document §2 Phase B | WP-14 and WP-15 added; landing order per A2.6 | On commit |
| This document §8 | Q6–Q8 added (below) | On commit |
| `ROADMAP.md` Phase 5 | WP-14, WP-15; landing order; O-3 resolved | On commit |
| `STATUS.md` | Drafting WP-10, 11, 12, 14, 15; none landed; Phase A at sitting 1 of 3 | On commit |
| `docs/workplan/README.md` | WP-14, WP-15 listed as drafted; O-3 closed | On commit |
| `audit/2026-11-08/walkthroughs.md` | O-M marked observer review | On commit |
| `CONTRIBUTING.md` | Lesson-screen template gains the chrome rows and the chrome's two-row cost | WP-15 |
| `scripts/sim/sentinels.py`, `run.py` | Feedback sentinel follows A3.4; `second-try` oracle updated | WP-15 |
| `shelltutor` plain-text path (`100-103`) | ASCII glyph substitution; `SHELLTUTOR_ASCII` | WP-15 |

#### Open questions added

Defaults apply if unanswered.

- **Q6** Chrome as its own package before WP-11 (default), or folded
  into WP-11?
- **Q7** Authority sentence on the welcome screen: yes (default), or
  keep it in `README.md` only?
- **Q8** Pre-task hints removed at stages 2–4 in favour of the ladder:
  yes (default), or keep them?

### A4 — Freeze lifted; Phase B lands before sittings 2 and 3 (2026-11-08)

Operator decision, in session, after A2/A3 were drafted: the changes are
significant enough that the remaining Phase A sittings should observe the
updated script rather than the old one. A1.9's freeze is lifted on
2026-11-08. The five Phase B packages land in the A2.6 order (WP-15,
WP-11, WP-12, WP-14, WP-10) as each passes review; sittings 2 and 3
(A2.7) then run on the post-Phase-B script and may open a second round
of fixes. WP-10's answer-list widening uses only what sitting 1 recorded
(F-015) and is widened again after sittings 2 and 3. Sitting 1's
findings remain comparable because they are recorded against the
revision they observed (`1aea23b`). Everything else in A1–A3 stands.

### A5 — Stages 3–5 and the finale to the screen budget (2026-11-08)

Operator approval, in session, of the coordinator's recommendation after
the Phase B closure check (`audit/2026-11-08/phase-b-closure.md`): nine
stage 3–5 screens and the finale exceed the 22-row rendered budget (O-J).
A2's "Stages 3 to 5 are not reopened" is relaxed for height only: WP-18
trims or splits those screens to the budget, removes no command, changes
no gate, and runs at the core standard. It lands before sittings 2 and 3
so the sittings see finished screens. Operator actions are no longer
reserved for the push and the hosted-evidence intake: the agent performs
them.

### A6 — Synthetic sittings (2026-11-09)

Operator direction: no human learners are available for sittings 2 and 3
for now. A new evidence source is added, **synthetic sittings**: an AI
session plays one of three learner personas (`docs/sim-personas/`:
Arthur `dos-literalist`, Maya `search-first-skimmer`, Leo
`gamer-brute-forcer`) against the real tutor through a project-owned
pseudo-terminal (`scripts/sim/sitting.py`, WP-19), under rules that
remove the model's expert knowledge (zero forward knowledge, reading
limits, a friction meter that quits at 8), and records a telemetry sheet
(`docs/walkthrough-notes-sim-template.md`) instead of clock time.

Evidence status: synthetic sittings yield **candidate** F-nnn and O-nnn.
A candidate is recorded in `audit/<date>/walkthroughs.md` only after a
maintainer reproduces it on the real tutor, deterministically where
possible (the simulation plan's rule that LLM-generated personas are not
acceptance evidence stands). D8 stands: pace is not measured in minutes;
the sheet's time line is an estimate. Phase A's exit (three human
sittings, one on Bash 3.2) is **not** satisfied by synthetic sittings;
it waits for people. Synthetic sittings run now, on the current script,
and may open a second round of core fixes under the core standard.

### A7 — Stage 1 gate grounding approved (2026-11-09)

After the first three synthetic sittings all quit at the Stage 1 gate
recall (`audit/2026-11-09/walkthroughs.md`, F-017, F-018, O-P..O-Y), the
operator approved all five items of the coordinator's decision set as
WP-20: Q1 taught in 1.3 and asked about a normal bash window; Q2/Q3
accepted lists widened from the reproduced inputs with apostrophes
normalised; the recall ladder shows the hint on the first miss and the
navigation facts from the second (this amends A1.1 for recall only; tasks
keep three rungs); recall rendered visibly as the tutor speaking; the 1.1
and 1.2 mechanical traps closed. A4 is extended: reproduced synthetic
findings are a valid source for answer-list widening. After WP-20 lands,
the three personas are re-run as sittings `*-2`.

### A8 — Answer shape, Stage 2 grounding, persona recalibration (2026-11-09)

After synthetic round 2 (`audit/2026-11-09/walkthroughs.md`, F-019, F-020,
O-Z..O-AG) the operator approved three items. (1) WP-21: longer plain
accepted forms and the hint's own words accepted; punctuation normalised;
the second recall miss names the expected answer shape; no containment
rule, because the negation counterexamples in F-019 are real and shaping
the answer is cheaper than guarding it. (2) Also in WP-21: 1.1 names the
stray-slash and missing-space typos; 2.3 says `cd` alone goes home and
`cd -` comes back, with a try-it line; 2.2's first outside listing is
`ls /`. (3) Persona sheets v0.2 (simulation calibration, not tutor
change): Maya's density charge applies only when skipped prose later
causes a rejection; Leo reads the first sentence of each paragraph as well
as commands. Round 3 runs after WP-21 lands with the v0.2 personas, and
the round-3 intake states both changes so the comparison is explicit.

### A9 — Stage 2 sequencing, defect fixes anywhere, hint rule, Arthur v0.2 (2026-11-09)

After synthetic round 3 (`audit/2026-11-09/walkthroughs.md`, F-021..F-024,
O-AH..O-AM) the operator approved four items. (1) WP-22: Stage 2 teaches
`mkdir` before its gate needs it; the first `check` lists both items and
the `cd` item requires the folder; `~` accepts the lessons' own gloss; the
Stage 2 gate screen carries the "not the shell" line and names the task
folder. (2) Rejected correct answers and false statements are defects and
are fixed wherever they sit, including Stages 3–5, which are otherwise not
re-sequenced (qualifies A2): Stage 4 Q1 forms and hint; Ctrl+C versus `q`
in 1.2 and 3.2; 3.3 asks the learner to type its commands. (3) FF-010:
every recall hint begins `Lesson N.k:` and names the concept; a hint never
paraphrases the answer, since FF-009 then forbids accepting it (the shared
cause of F-020 and F-023). (4) Arthur's persona sheet goes to v0.2 with the
same density-on-consequence rule as Maya. Round 4 runs after WP-22 lands.

### A10 — Keyword matching for recall; synthetic exit test (2026-11-09)

After synthetic round 4 (`audit/2026-11-09/walkthroughs.md`, F-025..F-028,
O-AN) the operator approved four items. (1) WP-23: recall answers are
accepted by exact form OR by keyword groups with a negation guard; this
reverses A8's "no containment rule": four rounds of list widening and hint
rewording did not close the class (F-018, F-019, F-020, F-021, F-023,
F-025, F-026, F-027), the shape line was judged unhelpful by all three
personas, and the guard answers the counterexamples that motivated A8.
FF-009 extends to keyword phrases; FF-011 keeps the rejected-correct corpus
from rounds 1–4 as a regression test; the shape line is removed. (2) 3.1
teaches `echo word > file` before the Stage 3 gate needs it (F-028; the
dead-end class of A9). (3) Harness: the sitting client strips terminal
control residue; the sheet template states the turn cap (160; one `send` or
`raw` is one turn). (4) Positioning: round 5 is the synthetic exit test,
all three personas reaching the finale on one revision. After it the
synthetic loop pauses and effort moves to release preparation and the
module standard. Human sittings still gate v0.1.0 (A1.10); synthetic
results remain candidate evidence.

### A11 — Screen chrome v2 from the consultant response (2026-11-09)

The operator commissioned an outside design review
(`docs/design-brief-consultant-2026-11.md`) and relayed the answer
(`docs/design-consultant-response-2026-11.md`). Adopted: the response's
§1 priorities, §2 answers to the three operator requests, §3 answers to
the ten questions, and §4 sheet, with all five of its defaults (body
palette reduced to bold/green/grey/yellow with rare red; product name off
lesson and gate headers; progressive footer; `?` recall prompt; `(gloss)`
in place of `▸`). Q10 (wide terminals: left-aligned, rule at 80) is
closed as-is. The identity phrase "a vimtutor prerequisite course" is
retired in favour of "working in a Unix shell"; the Stage 5 title stays.
Split: WP-25 is rendering only (chrome, footer, roles, glyphs, recall
block, checklist, welcome, cleared, finale, identity strings, title
prefixes); the §3.7 lesson skeleton and the §5.2 body rewrite are content
and go to WP-26, drafted now, scheduled after WP-25 with one synthetic
round as its evidence. A3's 20/22-row budgets are superseded by the
19-row panel (body ≤ 12) once WP-26 has brought the over-budget screens
down; until then WP-25 enforces a 21-row cap and reports the excess.

### A12 — Operator review of the welcome; the practice-folder thread (2026-11-09)

Recorded from `docs/operator-review-welcome-2026-11-09.md` (O-AW, O-AX in
`audit/2026-11-09/walkthroughs.md`). Where A12 differs from the consultant
response as adopted by A11, A12 governs.

- **Welcome (WP-27, rendering).** The course map is vertical, inside the
  box, one stage per row with its own dot; the dots-and-names row and the
  `Sandbox:` row under the box are removed; the lead-in, safety and no-score
  sentences are as the review's mock-up. On resume, passed stages show `●`
  in the map (adopted, not optional: it is cheap and gives the header dots
  their meaning).
- **Vocabulary.** On screen the folder is the "practice folder", never the
  "sandbox". `sandbox` stays in code (`$SANDBOX`), contracts and docs. `-h`
  and `--info` labels follow; the path stays in `--info`.
- **Curriculum thread (WP-26 and the `env` module).** The practice folder
  is a recurring teaching object: discovered with `pwd` in Stage 1; named as
  the "you are here" folder's full path at the Stage 2 tree; returned to by
  full name and by `~` in the `cd` lesson; shown to hold the tutor's files
  and the learner's own in Stage 3; and configured through
  `SHELLTUTOR_HOME` in `env`. The default is `$HOME/.shelltutor`, a hidden
  folder under home, which the `ls -a` lesson may use. The thread also closes
  O-AG/O-AV: every gate task says in one line which folder it runs in.
- **Process.** The coordinator's suggested review command now uses the
  default folder or a path under `$HOME`, not `mktemp`, so what the operator
  sees is what a learner sees.

### A13 — Lesson skeleton approved in full (2026-11-09)

The operator approved `docs/workplan/WP-26-lesson-skeleton.md` as drafted:
28 lessons in place of 21 (one typeable block each, body ≤ 12 rows); the
cuts of its §2 (`grep` pipelines, `<`, `vim --version`, `ls /usr/bin` in
Stage 2, `cd /tmp`, `rmdir`, the intro command tables); "working copy" for
"buffer" on screen; spaces and quotes taught with `touch`; each gate task
rehearsed in the lesson before it; the practice-folder thread of A12
without the hidden-folder beat. The synthetic loop resumes for one round
after it lands. Modules follow in WP-28.

### A14 — Round-6 copy fixes approved (2026-11-09)

After synthetic round 6 (all three personas at the finale on the 28-lesson
course; every gate task passed on the first `check`; F-031, O-AY..O-BG in
`audit/2026-11-09/walkthroughs.md`) the operator approved
`docs/workplan/WP-29-round6-copy-fixes.md` in full: the 2.3–2.5 copy, the
small wording and defined terms, the stage-folder line in the Stage 3–5
intros, the cleared-list corrections, the Stage 5 Q3 exact forms, and Leo
persona v0.3 with a scripted error schedule (round 6 was a weak test of
the child persona). WP-28 (modules, `SHELLTUTOR_HOME` beat) follows, and
one synthetic round covers both packages.

### A15 — Module package approved with review corrections (2026-11-10)

The operator approved `docs/workplan/WP-28-modules-skeleton.md` subject to
a twelve-point review, all adopted and written into the package: no bare
brackets in a child's `echo`; the harness follows the prompt change in
env 4; `SHELLTUTOR_HOME` reaches the practice shell as the learner's own
value, never the normalised one (C-004, C-007); the env task requires
`export` in the history; no path placeholder on task screens;
`ps -o pid,comm` in shells 1; module titles lose the position prefix and
the header shows `<module>  k/n`; both intros carry an assumption line;
env 6 shows the prompt line. The module standard is amended from three to
five lesson screens to three to six. Review rule recorded for future
module packages: module content gets a shell-detail read (globbing,
quoting, what a command really prints, what the harness waits for) before
approval.

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
