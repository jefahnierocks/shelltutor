---
title: shelltutor Audit — Phase 6 Authority Boundaries
category: audit
component: phase-6
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-6, authority, sandbox, focus-question]
priority: high
---

# Phase 6 — Authority Boundaries

The operator's focus question lands in this phase:

> Does the sandbox-safety claim hold?

The short answer is **no, not as stated to the learner**. The
sandboxing the script performs is narrow (CWD + HISTFILE inside the
practice subshell) and intentional under the project's bash-only
dependency constraint. The user-facing welcome claim
("Everything happens in ~/.shelltutor; you cannot break anything"
— shelltutor:169) overstates that narrow sandboxing as a complete
safety guarantee. Detailed authority matrix below; finding text
synthesized in Phase 10.

Five principals are inventoried: the shelltutor script process,
the practice subshell, the operator, the learner, and the coding
agent (when this repository is under coding-agent direction).

## Principal A-001 — shelltutor script process

| Facet | Value |
| --- | --- |
| Readable scopes | The learner's full filesystem authority (it is a normal user process); `$HOME`, `$SHELLTUTOR_HOME`, `NO_COLOR`, `PATH` env vars; stdin from `/dev/tty` |
| Writable scopes | **declared**: `$SANDBOX` only (shelltutor:67, 69, 76, 79, 83). **observed**: matches declaration. The script does not `mkdir`/`touch`/`echo >` outside `$SANDBOX`. |
| Callable capabilities | `bash` builtins (`mkdir`, `touch`, `printf`, `echo`, `cat`, `clear`, `seq`, `rm`); spawns one sub-process (`bash --rcfile <(...) -i < /dev/tty` — A-002 below). No external API. No tool/MCP/A2A surface. |
| Callable subagents | none |
| Callable externals | none |
| Workspace roots | `$SANDBOX` (default `$HOME/.shelltutor`; operator override `$SHELLTUTOR_HOME`) |
| Browser scope | n/a |
| Filesystem scope | **declared**: `$SANDBOX` (write-side). **observed**: matches. Read side is wider (script reads `$HOME`, `/dev/tty`, the OS environment), but that is conventional for any CLI. |
| Secrets access | none. Script never reads secrets, never expects API keys, never accesses `~/.ssh`, `~/.aws`, etc. |
| Approval policy | none required at runtime — no privilege boundary is crossed. Approval gates at AGENTS.md:43-47, 71-74, 75-78 govern **contributor-side** changes, not runtime. |
| Approval mode | `none-required` (runtime); for contributor changes, see A-005. |
| Approval precedence | n/a |
| Bypass modes | none |
| Protected paths | implicit: everything outside `$SANDBOX` is "protected" by the script's discipline (it never writes there). No enforcement mechanism beyond the script's own code. |
| Secondary credentials | none |
| Outbound network scope | **none**. Grep returned no `curl`/`wget`/`nc`/`ssh`/`http://`/`https://`/`fetch` references in shelltutor. Documented in AGENTS.md:87-88, README.md:58, CONTRIBUTING.md:47-48. |
| Callback auth | n/a |
| Hosted-or-local | `local` |
| Token delegation | n/a |
| Sandbox model | filesystem-only; the script confines its **own** writes to `$SANDBOX`. There is no kernel-level isolation (no `bwrap`, `firejail`, `chroot`, `unshare`, or macOS `sandbox-exec`); none could be added without breaking the bash-only dependency constraint (AGENTS.md:75-78). |
| Flags | none |
| Citations | shelltutor:30, 67-79, 95-103 (sandbox intent comment), 134; AGENTS.md:75-78, 87-92; CONTRIBUTING.md:42-49 |

### Trace evidence — the script's writes are confined

Every filesystem write in the script targets `$SANDBOX`:

- `mkdir -p "$SANDBOX"` (shelltutor:67)
- `cat > "$SANDBOX/poem.txt"` (shelltutor:69)
- `seq 1 50 > "$SANDBOX/numbers.txt"` (shelltutor:77)
- `touch "$SANDBOX/.shelltutor_history"` (shelltutor:79)
- `echo "$1" > "$PROGRESS_FILE"` (shelltutor:83; `$PROGRESS_FILE = $SANDBOX/.progress`)
- `rm -f "$PROGRESS_FILE"` (shelltutor:456)
- Inside practice subshell: `cd "$SANDBOX"`, `HISTFILE="$SANDBOX/.shelltutor_history"` — both relative to `$SANDBOX`.

`grep -nE 'mkdir|touch|>\s|tee\s|cp\s|mv\s|rm\s'` across the script
shows every write path is `$SANDBOX`-relative or to `$PROGRESS_FILE`
(also inside `$SANDBOX`). No writes leak to `/tmp`, `/var`, `$HOME/`
outside `$SANDBOX`, or any other path.

**A-001 honors its declared sandbox.**

## Principal A-002 — practice subshell

The practice subshell is the **load-bearing principal for the focus
question**. It is a separate process boundary from A-001.

| Facet | Value |
| --- | --- |
| Readable scopes | the learner's **full** filesystem authority (it is a real interactive bash with the learner's UID/GID) |
| Writable scopes | **claimed by user-facing copy**: `~/.shelltutor` only (shelltutor:169 "Everything happens in ~/.shelltutor; you cannot break anything"). **actual**: the learner's full filesystem authority — `cd ..`, `rm`, writes to `$HOME`, etc. all work. |
| Callable capabilities | every command on the learner's `$PATH`. Anything bash can launch. |
| Callable subagents | none |
| Callable externals | anything the learner's account can run (`curl`, `wget`, `ssh`, `sudo` if the learner has the password, `vim`, `man`, etc.) |
| Workspace roots | starts at `$SANDBOX` (one `cd $SANDBOX` in the rcfile at shelltutor:109); no enforcement keeps PWD there |
| Browser scope | n/a |
| Filesystem scope | **stated narrow**: `$SANDBOX` (per shelltutor:169 user-facing claim). **actual wide**: the learner's normal user-mode filesystem authority. The narrowing applied by the rcfile is CWD only (`cd $SANDBOX`) plus HISTFILE binding; neither restricts where the learner can `cd` next or what they can read/write thereafter. |
| Secrets access | the learner can read anything their user account can read (e.g., `~/.ssh`, `~/.aws/credentials`, `~/.bash_history`, etc.) from inside the subshell. The script does not introduce additional secret access, but it does not block existing access either. |
| Approval policy | **none** — the subshell is a learner-controlled bash; no agentic approval applies. The directive's `approval_mode: none-required` is honest, but the gap between the user-facing claim and the actual scope is the substantive concern. |
| Approval mode | `none-required` (correct for a learner-controlled shell) |
| Approval precedence | n/a |
| Bypass modes | the entire subshell is effectively a "bypass" of the implied sandbox if "sandbox" is read at the level the welcome screen suggests |
| Protected paths | none enforced |
| Secondary credentials | none acquired by the script. If the learner enters `sudo`, the system will prompt them per the host's normal sudo policy; the script neither facilitates nor blocks this. |
| Outbound network scope | the learner's normal network access. If the learner types `curl http://example.com`, the system runs it. The script does not block. |
| Callback auth | n/a |
| Hosted-or-local | `local` |
| Token delegation | n/a |
| Sandbox model | **filesystem-only at the directory layer**; the rcfile sets CWD and HISTFILE but does not restrict the learner's subsequent commands. The welcome screen's "you cannot break anything" claim implies a stronger sandbox than the implementation provides. |
| Flags | `undeclared-scope` (subshell write scope is wider than the user-facing claim); `ambient-authority` (the subshell inherits the learner's full user authority by design, not by explicit declaration) |
| Citations | shelltutor:104-134 (practice() implementation); shelltutor:109 (cd); shelltutor:111-117 (HISTFILE etc.); shelltutor:118 (PS1); shelltutor:126-130 (navigation overrides); shelltutor:169 (user-facing claim) |

### Why this is `undeclared-scope`, not `escalation`

The subshell does not **escalate** privileges. The learner already had
this authority before opening the tutor. The subshell simply does not
**restrict** the learner's existing authority while presenting the
illusion that it does. Per §6 category 6 ("approval gate present in
code or comments but not connected to enforcement") this is a
documentation-vs-enforcement gap rather than a privilege escalation.

The directive's flag list (Phase 6 procedure step 2 + §8.7
Authority.flags enum) offers `undeclared-scope` and `ambient-authority`
as the right matches.

### Resolution paths consistent with project constraints

Per AGENTS.md:75-78, the project forbids adding dependencies beyond
`bash` + POSIX userland. Strengthening the implementation (adding
bubblewrap / firejail / chroot / namespaces / macOS sandbox-exec)
violates that constraint. The remediation that fits the project's
posture is **narrowing the welcome-screen claim** to match what the
script actually guarantees, e.g.:

- "Your tutor work happens in `~/.shelltutor`. Things you type inside
  the practice prompt run as normal commands in your account, so the
  usual cautions apply."

This sketches the recommendation; Phase 10 owns the precise finding
text, and remediation belongs to a separate directive.

## Principal A-003 — operator

| Facet | Value |
| --- | --- |
| Readable scopes | the operator's full user filesystem |
| Writable scopes | the operator's full user filesystem |
| Callable capabilities | whatever the host shell offers; the operator can invoke `./shelltutor`, `./shelltutor 7`, or `./shelltutor -h`. The operator can also `SHELLTUTOR_HOME=/some/path ./shelltutor` to relocate the sandbox. |
| Approval policy | n/a (the operator's permissions are governed by the host OS) |
| Sandbox model | none from the script's side. The operator opens the tutor; the operator is not the audit's principal in the agentic-runtime sense, but recorded for completeness because the operator's environment supplies `SHELLTUTOR_HOME` (C-004) which determines the sandbox root. |
| Citations | shelltutor:30 (SHELLTUTOR_HOME consumption) |

## Principal A-004 — learner

The learner is the same OS principal as the operator in the typical
single-user scenario, but the role is distinct. Their *operator* role
ends when they invoke the script; their *learner* role is what happens
at the `shelltutor>` prompt inside A-002.

| Facet | Value |
| --- | --- |
| Authority surface | identical to A-002 once they are inside the practice subshell |
| Authority claim | "you cannot break anything" (shelltutor:169) |
| Authority reality | normal user-mode authority |
| Citations | shelltutor:155-173 (welcome screen addressed to the learner) |

## Principal A-005 — coding agent / contributor

This is the **non-runtime** authority surface — agents and humans
making changes to the repository. Sourced from AGENTS.md and from
profile `baselines.authority`.

| Facet | Value |
| --- | --- |
| Readable scopes | the repository (`/Users/verlyn13/Organizations/jefahnierocks/shelltutor/`) |
| Writable scopes | the repository (with the boundary restrictions in AGENTS.md §Scope and §Authority Levels) |
| Callable capabilities | running `./shelltutor` for validation (`AGENTS.md:96-97`); reading governance docs; making focused commits |
| Approval gates (3) | (a) scope-expansion outside the repo — `human-in-loop`, `ask`, no bypass (AGENTS.md:43-47); (b) safety-surface changes — `human-in-loop`, `ask`, no bypass (AGENTS.md:71-74); (c) introduce dependency outside bash + POSIX — `blocked`, `deny`, no bypass (AGENTS.md:75-78) |
| Approval mode | `ask` for sensitive work; `deny` for restricted work |
| Approval precedence | AGENTS.md §Authority Levels + STATUS.md §Decision-Disagreement Rule |
| Bypass modes | none documented |
| Protected paths | external workspace (anything outside `/Users/verlyn13/Organizations/jefahnierocks/shelltutor/`) |
| Secondary credentials | none |
| Outbound network scope | none documented as in-scope for agent operations |
| Callback auth | n/a |
| Hosted-or-local | `local` (Claude Code or Codex running on the operator's machine) |
| Token delegation | n/a |
| Sandbox model | the AGENTS.md-declared repo boundary; coding agents must pause and ask before traversing it |
| Flags | none. The three approval gates are explicit, with `bypass_modes: []` and clear precedence. |
| Citations | AGENTS.md:43-47, 71-74, 75-78; CLAUDE.md:14-22; CONTRIBUTING.md:72-75 |

**Audit observation about this layer**: the approval gates are
explicit and well-defined, but their **enforcement** is via norms
(CONTRIBUTING.md: "local commit discipline is the enforcement layer")
rather than code-level mechanisms (no pre-commit hook, no CI, no
policy-as-code). This is intentional per the deferred GitHub-side
automation posture and is documented in profile `known_debt`.

## Cross-cutting Observations

### Safety-rule code coverage gap

The three safety rules from AGENTS.md:87-88 ("must not write outside
its own working directory, must not request elevated privileges, and
must not reach the network") are honored by the current script but
have no enforcement mechanism:

- No `pre-commit` hook scans for `sudo|curl|wget|nc |ssh |chmod \+s`.
- No CI workflow runs static analysis.
- No fitness function exists.

The rules live only in the `skill-or-sop` file. If a future change
violates one of them, only manual review catches it. This is a
candidate for fitness functions FF-001 / FF-002 in Phase 10.

### Sandbox enforcement vs sandbox claim

A-001 (script) honors its declared write scope exactly. A-002
(subshell) cannot enforce the welcome-screen's wider safety claim
because:

1. Strengthening enforcement requires non-bash dependencies (forbidden
   per AGENTS.md:75-78).
2. The subshell **is** a real interactive bash by design — that is
   what makes it a useful teaching tool (lessons 1, 4, etc. depend on
   real Ctrl+C, real Up arrow, real Tab completion).

Therefore the sandbox claim must narrow to match the implementation,
not the other way around. This is the substantive Phase 10 finding
F-002 (forecast; finalized in Phase 10).

## Boundary Declarations Honored (Phase 6)

- Did not assume least privilege because the tool name (`shelltutor`)
  sounds narrow. Walked the actual subshell behavior at lines 104-134.
- Did not infer approval policy from comments. The approval gates at
  AGENTS.md cite line ranges and are explicit; no enforcement was
  imagined that did not exist.
- Did not broaden scope while investigating one authority issue.
  Stayed inside the script and the AGENTS.md governance text.
- Did not score "approval exists" as sufficient. The three
  AGENTS.md gates are documented; the matrix records them and notes
  that the enforcement layer is norms (CONTRIBUTING.md:72-75), not
  code. Norm-based enforcement is honest for a Day-1 scaffold but is
  recorded explicitly.

## Exit Check

| Check | Status |
| --- | --- |
| Every write-capable path has an approval policy value (even `none-required`) | ✅ A-001 and A-002 carry `none-required` runtime + AGENTS.md contributor-side gates |
| Every authority escalation is either explained or flagged | ✅ A-002's wide scope is flagged `undeclared-scope`, `ambient-authority` |
| Every principal has readable and writable scopes recorded | ✅ A-001 through A-005 |
| Every browser-use / computer-use / filesystem-use agent has a declared scope | ✅ vacuous for browser/computer-use; filesystem-use scope recorded for A-001 (declared+observed) and A-002 (claimed narrow vs actual wide — the flag) |
| Every callback-capable / hosted-tool / remote-agent principal has authentication & token-scope evidence or a flag | ✅ vacuous (none exist) |

Phase 6 exit check **passes**. Advancing to Phase 7.
