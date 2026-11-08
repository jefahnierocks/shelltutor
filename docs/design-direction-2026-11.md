---
title: shelltutor Design Direction — November 2026 (draft)
category: planning
component: design-direction
status: draft
version: 0.1.0
last_updated: 2026-11-08
tags: [design, direction, curriculum, scope, draft, decisions-pending]
priority: high
---

# Design Direction — November 2026 (draft)

The operator stated a broader direction for `shelltutor` on 2026-11-08.
This brief records that direction as given, measures it against the design
baseline (`docs/design-description.md`), names the constraints and
tensions it meets in the repository as it stands, and lists the decisions
that have to be made before any curriculum change is specified. It
decides nothing. Nothing here changes `AGENTS.md`, the contracts, the
roadmap or the script.

## 1. The direction as stated

Paraphrased from the operator's three messages of 2026-11-08, kept close
to the wording:

1. The tool should become **more than a vimtutor preparer**: a
   general-purpose shell learning tool. The first aim stays **confidence
   doing the basic starting work**, with a **modern, 2026, future-forward
   and agent-aware bent**, covering **the concepts of Linux** and,
   eventually, the concepts behind **Emacs, tmux and other advanced parts
   of editors**, where "things are managed properly at a lower level".
   Start simple.
2. **What is a shell, anyway?** The operator's children may want to use
   other shells, personalise their own shell environments, understand
   what it means to have a shell, control a shell, and know about other
   shell types.
3. Keep **starting very basic**, as the current course does, but give
   **pace and experience more attention**. This will **fight a bit against
   the minimalism**, which stays the default for the most part because the
   skills should **transfer to real shell work**, while admitting that it
   is November 2026 and the world is changing.

## 2. What the direction changes, and what it keeps

### Changes to the project's stated identity

| Statement today | Where | Effect of the direction |
| --- | --- | --- |
| "a vimtutor prerequisite course" | `shelltutor:2`, `README.md` §shelltutor, `ROADMAP.md` §Framing decision | `vimtutor` becomes one milestone inside a larger course rather than the destination |
| Non-goals: "Teach shell scripting, sysadmin, or shell programming patterns"; "Teach the inside of Vim" | `README.md` §Non-Goals | Partly reopened: Linux concepts, process control, editor internals at a conceptual level. Scripting is not mentioned by the operator and stays out unless decided otherwise |
| Research guidance: defer process and job control, permissions as a late topic, editor handoff last | `docs/audit/references/educational-design-research.md` §Executive Synthesis | The later topics move into scope; the ordering advice still applies |
| Target audience "adult beginners first, child-friendly compatible second" | `docs/simulation-design-plan.md` §Pedagogy And UX | Children are now named learners; the tone rules may need a second look without losing "non-condescending" |
| Win condition: Stage 5 passed, finale points at `vimtutor` | `docs/design-description.md` §1.7 | A longer course needs an interim milestone marker where the finale is today |

### Kept, as the operator asked

- Minimalism as default: one idea per screen, the 20-line budget, the
  density rule (`docs/design-description.md` §4.1).
- Transfer-first choices (real Bash prompt, common-Bash completion,
  C-007).
- Mastery gates, unlimited retries, no praise copy, no score or timer
  (`docs/design-description.md` §1.11).
- User-agnostic, safe on a stranger's machine, no network, no privilege
  (`AGENTS.md` §Identity, §Work Rules).
- The evidence discipline: observe before changing, findings before fixes,
  personas and sentinels move with copy (`docs/simulation-design-plan.md`).

## 3. Theme by theme: what the baseline already has, and what resists

### T1 — "What is a shell?"

- **Already present**: lesson 1.4's terminal → shell → program model
  (`shelltutor:710-732`); the research reference's learning goal 1
  (`shell-research.md` §Central learning goals); `--info` already shows
  the login shell and says the tutor spawns Bash regardless
  (`shelltutor:216-217`).
- **Resists**: nothing structural. This is the most natural extension:
  the model exists and is the stage's capstone.
- **Open question**: whether "what a shell is" becomes a Stage 0, a
  thread revisited at each stage, or a module after the foundations.

### T2 — Other shells

- **Already present**: `README.md` §Run notes that practice runs in Bash
  "regardless of your login shell (bash, zsh, fish)".
- **Resists**: the practice shell is Bash by construction, and since WP-09
  it is the same Bash as the outer script (`shelltutor:384`; C-007). On
  macOS the default login shell is zsh; `fish` is not installed by
  default anywhere the project supports; the work rule forbids lessons
  that require installing anything beyond Bash (`AGENTS.md` §Work Rules).
  A per-shell practice prompt would mean a second rcfile contract per
  shell and a second set of sentinels.
- **Open question**: concept-only (name the shells, show `echo $SHELL`,
  `command -v zsh`, explain what differs) versus gate-and-fallback live
  demos (`CONTRIBUTING.md` §Portability Rules: "gate it on a runtime
  check and degrade gracefully") versus genuine multi-shell practice.

### T3 — Personalising the shell environment

- **Already present**: Stage 1 teaches the prompt and Stage 2 `~`; the
  practice shell sets `PS1` and history variables itself
  (`shelltutor:402-409`).
- **Resists, strongly**: C-007 exists to neutralise the learner's rc
  files so the practice prompt is identical on every host
  (`docs/contracts.md:185-216`); teaching `~/.bashrc`, aliases, `PS1` and
  `PATH` edits inside that prompt means teaching the thing the tutor
  deliberately suppresses. Second, every screen is a fresh practice shell
  (`practice()` is called per screen, `shelltutor:451-455`), so an alias
  or variable the learner defines vanishes at the next `next`. Third, the
  tutor's write scope is `$SANDBOX` only (FF-002), so it must never edit
  the learner's real rc files.
- **Options the baseline leaves open** (not decided): a sandbox rc file
  the learner edits and `source`s inside one screen; a lesson that only
  explains and then hands the learner to their real shell with exact
  transfer instructions; a practice mode that persists one sandbox rc
  across screens (a C-007 change).

### T4 — Controlling a shell: processes, jobs, multiplexers

- **Already present**: Ctrl+C as "the escape hatch" (`shelltutor:681-682`);
  "take over the screen" programs and how to leave them (lesson 5.1,
  `1669-1695`); `q`, `:q!`.
- **Resists**: the research reference deferred process and job control
  (`educational-design-research.md` §Design Decisions, item 3); `tmux` is
  not installed by default on macOS or most Linux bases, so it falls under
  gate-and-fallback or concept-only; job control (`Ctrl+Z`, `jobs`, `fg`,
  `bg`, `kill`) works in the practice shell but needs tasks the gate can
  verify from history or state.
- **Open question**: how far "control a shell" goes before it becomes the
  sysadmin curriculum the non-goals exclude.

### T5 — Linux concepts

- **Already present**: `/etc`, `/usr/bin` as places (`shelltutor:970-973`);
  `command -v` as the first touch of `PATH` (`1428-1431`); pipes and
  redirection as the stream model; `man` (`1675`).
- **Resists**: permissions have no lesson (the research says teach them
  "as observable capabilities, not as a game or security drama"); users
  and processes have none; environment variables appear only as `$HOME`
  (`990`). None of these violate the portability rule if taught with
  commands present on both platforms (`ls -l`, `chmod`, `ps`, `env`).
- **Open question**: which Linux concepts are "concepts of Linux" for this
  audience versus Unix concepts the course already teaches under another
  name.

### T6 — Agent-aware

The operator's phrase is new to the repository; this section interprets it
narrowly and flags the interpretation as pending.

- **Plausible meaning**: learners in 2026 will delegate shell commands to
  AI agents and review what agents did. The skills that implies are
  already the course's habits: read a command before running it, predict
  its effect ("Predict before you act.", `shelltutor:1024`, `1494`), know
  the working directory, recognise destructive verbs (`rm`, `>`), and read
  output rather than skim it (the Stage 1 transcription task). The
  terminal → shell → program model extends to agent → shell → program.
- **Resists**: the tutor may not reach the network or call any agent
  (`AGENTS.md` §Work Rules), so agent-awareness can be taught as concepts
  and habits, not as integration. The harness is itself an example of an
  agent driving the shell deterministically (`scripts/sim/persona.py`);
  whether that is a teaching device or an implementation detail is a
  design choice.
- **Open question**: what "agent-aware" should mean in lesson terms, and
  whether it is a thread through existing stages or its own module.

### T7 — Editors and terminals at a lower level (Emacs, tmux)

- **Already present**: buffer versus file (`shelltutor:1729-1767`); modal
  editing named ("vimtutor will teach modes", `1754`).
- **Resists**: Emacs is not guaranteed on macOS or minimal Linux; the
  non-goals exclude teaching the inside of Vim; "eventually, start
  simple" is the operator's own pacing. Concepts that are editor-agnostic
  (buffers, modes, key chords, panes and sessions) can be taught without
  requiring the programs, with gate-and-fallback demos where present.

### T8 — Pace and experience

- **Already present**: the baseline's drop-off risks (`docs/design-description.md`
  §3.4) and its evidence gap: human pacing is unobserved and the harness
  cannot supply it (§7.2; `audit/2026-11-08/stage1-density-followup.md`
  §Watch items).
- **Resists**: the project records no timing and commits no human
  transcripts by rule (`docs/simulation-design-plan.md` §Evidence
  Locations). Attention to pace therefore needs either human walkthrough
  notes (the Phase 2 mechanism) or local-only, never-committed session
  timing, which would be a new store under C-003.
- **Open question**: what evidence about pace the project is willing to
  collect, and from whom.

## 4. Constraints that a broader course would press on

| Constraint | Where it lives | Pressure from the direction |
| --- | --- | --- |
| Five stages, `1..5` argv range | `shelltutor:74`, `2065`; C-001 | More content means either more stages (a C-001 change, allowed pre-1.0) or a second entry axis (modules by name; the roadmap already floated `./shelltutor extras`, `ROADMAP.md:357-359`) |
| One file | `AGENTS.md` §Identity; `README.md` §Goals ("readable as a single script") | 2094 lines today; each stage is roughly 200–400 lines; a doubling is still one file but no longer a quick read |
| Bash 3.2 floor for the tutor's own code | `shelltutor:46-56`; `STATUS.md` §Posture | Unaffected by teaching modern concepts; affected only if the tutor's code wanted Bash 4+ features |
| No installation beyond Bash for lessons | `AGENTS.md` §Work Rules | tmux, Emacs, fish, zsh-on-Linux all need gate-and-fallback or concept-only treatment |
| Practice shell is Bash, rc files neutralised | C-007 | T2 and T3 above |
| Fresh practice shell per screen | `shelltutor:451-455` | Any lesson whose state must survive `next` (aliases, background jobs, tmux sessions) needs a different screen model |
| Sentinels and personas track copy | `scripts/sim/sentinels.py`, `persona.py` | Every new screen is also a harness change; the evidence discipline scales linearly with content |
| 45–60 minute framing | `shelltutor:587`, `ROADMAP.md:131` | A general-purpose course is longer; the welcome's promise and the finale's meaning change |
| Tone rules | `docs/simulation-design-plan.md` §Pedagogy And UX | Children as named learners; "future-forward" voice versus "concise, concrete, task-focused" |

## 5. Structural shapes the baseline admits

Three shapes are compatible with the constraints above. They are listed
for comparison, not chosen.

1. **Longer line.** Add stages 6+ to the same linear course. Simplest
   mentally; changes C-001 and the `TOTAL_STAGES` invariants the smoke
   test checks; pushes the finale and the `vimtutor` milestone later or
   turns them into a mid-course marker.
2. **Core plus modules.** Keep the five foundations as the core with its
   own finale; add named modules (`shelltutor shells`, `shelltutor env`,
   `shelltutor processes`) that require the core to be passed or stand
   alone. Keeps the existing contract for the core; needs a module
   progress model beyond one integer.
3. **Threads.** Weave the new concepts into the existing stages as short
   interludes (a "what is a shell" beat after 1.4, an "agents run commands
   too" beat after 4.1). Least structural change; most pressure on the
   density rule and the 45–60 minute framing.

## 6. Decisions needed before a specification

1. Scope of "other shells": concept-only, gate-and-fallback demos, or
   multi-shell practice (T2).
2. Where personalisation is practised: sandbox rc file within a screen, a
   persistent sandbox rc (C-007 change), or explain-and-transfer only (T3).
3. The meaning of "agent-aware" in lesson terms (T6).
4. Course shape: longer line, core plus modules, or threads (§5), and
   whether `vimtutor` stays the core's finale.
5. Audience priority: children first or adults first, and what that does
   to tone and to the time framing (T8, §4).
6. Install policy for demonstrations of `tmux`, Emacs, `fish`:
   gate-and-fallback versus concept-only (T4, T7).
7. Which Linux concepts are in (permissions, processes, users,
   environment) and which stay out (sysadmin, scripting) (T5).
8. What evidence about pace the project will collect, and the rule for
   storing it (T8).

## 7. How this brief is meant to be used

It is the record of operator intent as of 2026-11-08. The next step in
the project's own process is a decision session that answers §6; its
outcomes would then be written as a dated ROADMAP phase (the curriculum's
design record lives in `ROADMAP.md` Phase 3 and its Amendments), followed
by contract updates and work packages under `docs/workplan/`. Until then,
`docs/design-description.md` describes what exists and this brief
describes what is wanted; neither is a specification.

## Cross-references

- `docs/design-description.md` — the baseline every "already present" and
  "resists" claim above points into.
- `AGENTS.md` §Identity, §Work Rules — the rules a broader course must
  either honour or explicitly change.
- `docs/contracts.md` C-001, C-003, C-007 — the contracts most exposed.
- `docs/audit/references/educational-design-research.md`,
  `shell-research.md` — the research the current ordering rests on.
- `docs/workplan/README.md` — the process shape (decisions, then
  packages) that produced the 2026-11 cycle.
