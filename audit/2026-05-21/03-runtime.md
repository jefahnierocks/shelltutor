---
title: shelltutor Audit — Phase 3 Runtime Map
category: audit
component: phase-3
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-3, runtime, entrypoints, loops]
priority: high
---

# Phase 3 — Runtime Map

## Entrypoints

Two runtime entrypoints exist: the CLI invocation and the interactive
practice subshell spawned by each lesson. No HTTP/RPC/queue/scheduler/
webhook/callback/MCP-tool/A2A-receiver/agent-loop/subagent/durable-
workflow/background-trigger surfaces exist (search notes recorded in
the profile, Phase 0 anchors, and `03-runtime.json`).

### Entrypoint EP-001 — CLI

| Field | Value |
| --- | --- |
| Kind | `cli` |
| Path | `shelltutor` (line 459: `main "$@"`) |
| Argument shape | `(empty) \| 1..9 \| -h\|--help` |
| Sync model | `sync` |
| Execution mode | `sync` |
| Side effects | (1) create / heal `$SANDBOX` and its fixtures; (2) clear screen and emit lesson heredocs; (3) spawn practice subshell; (4) write / delete `$PROGRESS_FILE` |
| Touches loop | true (main loop EP-LOOP-001) |
| Termination | array exhaustion (i < 11) **OR** practice-subshell exit code 99 propagates up from inside `lesson()` |
| Approval gates | none required (no privilege boundary crossed; no agentic policy applies) |
| Citations | shelltutor:1, 412-459 |

**Trace from entrypoint to first external side effect:**

1. `main "$@"` (shelltutor:459) parses arguments (shelltutor:415-428).
2. `setup_sandbox` (shelltutor:431) creates `$SANDBOX` and writes
   `poem.txt`, `numbers.txt`, and `.shelltutor_history` if missing
   (shelltutor:66-80). **First external side effect**: filesystem write
   inside `$SANDBOX`.
3. `for ((i=start; i<total; i++)) { "${lessons[$i]}" ; ... }`
   (shelltutor:442-454): the dispatcher invokes each lesson function in
   sequence.

**Side effect surface (concrete):**

- `mkdir -p "$SANDBOX"` (shelltutor:67)
- Conditional writes of `poem.txt` (shelltutor:69-75), `numbers.txt`
  (shelltutor:77), and `.shelltutor_history` (shelltutor:79).
- `clear` invocation, soft-failing if missing (shelltutor:145).
- `printf`/`echo` writes to stdout.
- `save_progress` writes `$PROGRESS_FILE` after each lesson advances
  (shelltutor:82-84, 452).
- `rm -f "$PROGRESS_FILE"` at finale (shelltutor:456).

### Entrypoint EP-002 — Practice subshell

| Field | Value |
| --- | --- |
| Kind | `other` (interactive bash sub-process spawned via `bash --rcfile <(…) -i < /dev/tty`) |
| Path | `shelltutor:104-134` (`practice()`) |
| Argument shape | none (rcfile sets PS1, HISTFILE, navigation functions) |
| Sync model | `sync` (foreground; outer script waits on exit code) |
| Execution mode | `sync` |
| Side effects | bash subshell with `cd "$SANDBOX"`, `HISTFILE=$SANDBOX/.shelltutor_history`, sandboxed history rotation. **Subshell holds the learner's normal filesystem authority** — narrow sandboxing applies only to the working directory and HISTFILE; the subshell can `cd ..`, `rm`, or invoke any command the learner's account permits. |
| Touches loop | true (each iteration of EP-LOOP-001 spawns one subshell) |
| Termination | bash builtins overridden in rcfile to exit with codes 0/97/98/99 (`next/show/prev/quit/exit`); plain `exit` is also overridden to 99 |
| Approval gates | none — no agentic approval; sandbox is filesystem-only, not OS-level |
| Citations | shelltutor:104-134, 169 (welcome screen claim) |

**Trace from entrypoint to first external side effect:**

1. `bash --rcfile <(cat <<RCFILE ... RCFILE) -i < /dev/tty`
   (shelltutor:106-134). Heredoc-substituted rcfile carries the
   navigation function overrides.
2. Inside subshell: `cd "$SANDBOX"` (shelltutor:109). **First external
   side effect at the subshell layer is the directory change.**
3. `HISTFILE=$SANDBOX/.shelltutor_history`, `HISTSIZE=2000`,
   `HISTFILESIZE=4000`, `shopt -s histappend`, `history -r`,
   `PROMPT_COMMAND='history -a'` (shelltutor:111-116).
4. PS1 overridden to `shelltutor> ` (shelltutor:118).
5. Navigation builtins overridden: `next() { builtin exit 0; }`,
   `prev() { builtin exit 98; }`, `show() { builtin exit 97; }`,
   `quit() { builtin exit 99; }`, `exit() { builtin exit 99; }`
   (shelltutor:126-130).
6. After this, learner-typed input runs inside a real interactive
   bash with the learner's normal authority. Anything the learner's
   account can run, including writes outside `$SANDBOX`, is permitted.

**Authority observation (routed to Phase 6):** the sandbox boundary is
asserted in user-facing copy (shelltutor:169) but is implemented only
via `cd $SANDBOX` plus HISTFILE sandboxing inside the subshell. This
is the operator's focus question; see Phase 6 for analysis.

## Lesson Functions (internal, not entrypoints)

The 11 lesson functions (`welcome`, `lesson1` … `lesson9`, `finale`)
are intermediate dispatch targets, not runtime entrypoints. Each
emits a heredoc, then calls `lesson()` which calls `practice()` (the
real EP-002). `finale` is special: it emits a heredoc but does not
call `practice()` — it ends the run.

Recorded here to make the trace complete; not separately enumerated
as entrypoints in `03-runtime.json` because they share kind/sync/
side-effect surface with EP-001.

| Lesson | Lines | Practice subshell? | Notes |
| --- | --- | --- | --- |
| `welcome` | shelltutor:152-173 | yes | Introduces shelltutor> prompt and four navigation words |
| `lesson1` | shelltutor:175-195 | yes | `echo`, Tab, Ctrl+C, Ctrl+L, pager `q` |
| `lesson2` | shelltutor:197-219 | yes | Command history; Up/Down arrows; Ctrl+R |
| `lesson3` | shelltutor:221-243 | yes | `wc`, `cat`, `head`; reads `poem.txt`, `/etc/services` |
| `lesson4` | shelltutor:245-266 | yes | `seq`, `yes`, `head`; Ctrl+C drill |
| `lesson5` | shelltutor:268-290 | yes | Pipe operator; reads `/usr/bin`, `/etc/passwd` |
| `lesson6` | shelltutor:292-314 | yes | Redirection `>` `>>` `<`; glob `*` |
| `lesson7` | shelltutor:316-338 | yes | Identity + resources: `whoami`, `hostname`, `pwd`, `date`, `uptime`, `free -h`, `df -h`, `/proc/*`. **Linux-only constructs** — see Phase 1 portability collision. |
| `lesson8` | shelltutor:340-362 | yes | Optional `cowsay`, `figlet`, `lolcat` with Fedora install hint. **Fedora-only install** — see Phase 1 portability collision. |
| `lesson9` | shelltutor:364-382 | yes | Composition exercises |
| `finale` | shelltutor:384-410 | **no** | Summary; does not call `practice()`; main loop exits |

## Loops

### EP-LOOP-001 — main lesson dispatcher

```text
for ((i=start; i<total; i++)) {
    "${lessons[$i]}"      # call welcome / lesson1 / ... / finale
    rc=$?
    case "$rc" in
        97)  ((i--)) ;;                        # show -> redisplay current
        98)  i=$((i > 0 ? i - 2 : -1)) ;;       # prev -> step back one (since ++ will fire)
    esac
    local next_i=$((i + 1))
    if [ "$next_i" -lt "$total" ]; then
        save_progress "$next_i"                # remember resume point
    fi
}
```

| Field | Value |
| --- | --- |
| Path | shelltutor:441-454 |
| Termination | (a) `i` reaches `total=11` (lesson array exhausted); (b) practice subshell returns exit code 99 → `practice()` calls `exit 0` directly (shelltutor:136-140), bypassing the loop and the script exits. |
| Iteration cap | implicit (lessons array is fixed at 11 entries); no max-iterations cap because the cap *is* the array length. |
| Side effects | per iteration: clear screen + render heredoc + spawn practice subshell + save progress. |
| Approval gates | none |
| Loop diagram | `03-loops/EP-LOOP-001-main-dispatcher.mmd` |

This is **not an agentic loop**. The loop dispatches a fixed list of
lesson functions; there is no LLM in the loop, no tool selection, no
planner, no token budget, no evaluator gate. Phase 9 (evals) records
the absence of model-mediated paths.

## Subagents and Remote Agents

None. There are no subagent invocations, no remote-agent calls, no
A2A receivers, no Agent Card discovery, no MCP servers, no MCP
clients. Search notes already recorded in
`profile/2026-05-21/project_profile.yaml` (`agent_surface.*` is all
`false`/`0`) and re-verified in Phase 0.

## Background / Paused / Resumable / Durable / Callback / Event-triggered Paths

None of these execution modes exist in the script.

The **`.progress` file** (shelltutor:30-32, 82-93, 452-456) does
implement a *user-visible* resume mechanism between independent CLI
invocations (`shelltutor` after a quit picks up where the learner left
off via `read_progress()`). The directive's `resumable` execution mode
refers to *agent-runtime* resume from durable state; the `.progress`
file is more honestly recorded as `checkpoint-state` in Phase 5
(state inventory) than as a `resumable` execution mode here. Recorded
under `infrastructure.local_development_infrastructure` in the profile.

## Human-in-the-Loop Approval Gates

None at runtime. The script is fully autonomous within its sandbox
once the learner invokes it. AGENTS.md does declare approval gates
for **coding-agent** behavior (scope expansion, safety-surface
changes, dependency introduction — captured in
`profile.baselines.authority.approval_gates`), but those gates apply
to contributors, not to runtime.

## Boundary Declarations Honored (Phase 3)

- Did not assume entrypoints are harmless because they are local.
  EP-002 carries the focus-question observation.
- Did not stop tracing at an abstraction boundary. Followed the call
  chain into the practice subshell and recorded the side-effect
  surface there.
- Did not infer termination from intent. The loop terminates because
  the array exhausts (count is a static `${#lessons[@]}`); the only
  early exit is exit code 99 → `exit 0` in `practice()`.
- Did not collapse the practice subshell into a "tool call" — it is
  a separate process boundary with its own authority surface.
- Did not treat the `.progress` file as `durable-workflow`
  checkpoint state — it is a per-learner CLI resume token (Phase 5
  classification).

## Exit Check

| Check | Status |
| --- | --- |
| Every entrypoint has a traced chain or explicit `trace-blocked` | ✅ EP-001 and EP-002 traced |
| Every loop has a termination condition or is flagged | ✅ EP-LOOP-001 terminates on array exhaustion or rc=99 |
| Every write-capable runtime path is routed to Phase 6 | ✅ both entrypoints have write capability; Phase 6 documents the authority matrix and the subshell-safety claim |
| Every subagent invocation has caller and callee authority recorded | ✅ vacuous (none exist) |
| Every background/paused/resumable/durable/callback path has lifecycle evidence or is flagged | ✅ vacuous (none exist); `.progress` file rerouted to Phase 5 |

Phase 3 exit check **passes**. Advancing to Phase 4.
