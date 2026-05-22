---
title: shelltutor Audit — Phase 1 Vocabulary
category: audit
component: phase-1
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-1, vocabulary, collisions]
priority: high
---

# Phase 1 — Domain Vocabulary Extraction

This phase extracts the project's working vocabulary, groups terms by
unit, and tests for same-term-different-meaning collisions and
different-term-same-meaning synonyms. Two profile audit-attention flags
were routed here:
`drift-status-roadmap-vs-commit` and `lesson-portability-gaps`. Both
are confirmed by vocabulary evidence below; the findings themselves are
synthesized in Phase 10.

## Working Vocabulary

### `user-agnostic`

The project's stated defining property. The word "user" inside this
phrase refers to the **operator** (project owner / installer / coding
agent's user), not the **learner** (the person at the practice
prompt) — see "operator vs learner" below.

| Unit | Definition | Citation |
| --- | --- | --- |
| `README.md` | "The tutor is intentionally user-agnostic: it does not assume a particular operator name, home layout, distro, hostname, prompt theme, or pre-existing shell setup." | README.md:20-23 |
| `AGENTS.md` | "The project's defining property is that it is user-agnostic: no operator name, distro, hostname, theme, or pre-existing shell setup is assumed by the script or by any document in this repository." | AGENTS.md:34-37 |
| `CONTRIBUTING.md` | "`shelltutor` is user-agnostic by contract." (preceded by the same list of forbidden assumptions) | CONTRIBUTING.md:42-49 |
| `STATUS.md` | "User-agnostic refactor commit — replace WYN OPS accent comments with neutral wording" (lists this as the next step) | STATUS.md:41-43 |

Collision: **same-term-different-meaning** between the property
("user-agnostic") and the implied subject of "user." In all four files
the operative meaning is "operator-private detail-agnostic", not
"learner-input-agnostic." The script does react to the learner (their
key presses, lesson choices, sandbox state) — so it is not literally
"learner-agnostic." Vocabulary is consistent within its own meaning,
but the term itself is mild policy-masquerade: a strict reader could
infer the wrong "user."

### `WYN OPS`

Historical accent comment from the prior-art import (`fedora-top`
branch, 2026-05-17). Removed in commit `e6257aa` ("refactor: remove
user-specific accent branding from tutor"). Currently:

| Unit | Definition / claim | Citation |
| --- | --- | --- |
| `shelltutor` | (no occurrence — refactor removed all accent comments) | grep across `shelltutor`: 0 matches |
| `STATUS.md` | "The imported script still carries two `WYN OPS` accent comments (lines 17 and 35); user-agnostic refactor is the next change." | STATUS.md:33-34 |
| `STATUS.md` | "User-agnostic refactor commit — replace `WYN OPS` accent comments with neutral wording…" (listed as Immediate Next Step #1) | STATUS.md:41-43 |
| `ROADMAP.md` | "Replace `WYN OPS` accent comments with neutral language." (listed as Phase 1 work) | ROADMAP.md:37 |
| `README.md` | "The prior-art repo carried user-specific framing (`WYN OPS` accent comments and a sibling `wyn-setup/` installer); the user-specific surface is intentionally not carried forward into this repository." (provenance note, accurate) | README.md:79-83 |
| `git log` | `e6257aa refactor: remove user-specific accent branding from tutor` | `git log --oneline` |

Collision: **different-term-same-meaning** in time. The same project
artefact has two non-overlapping claim sets:

- README's provenance note (line 81) treats `WYN OPS` as historical and
  removed. Accurate.
- STATUS.md (lines 33-34 and 41-43) and ROADMAP.md (line 37) treat
  `WYN OPS` as currently present and as pending work. Inaccurate.

The script's named lines (17 and 35) carry neutral content (`#   -
Title + action footer styled with a single accent color.` and `H1=…
# lesson title — bold orange accent`). The "WYN OPS" tokens are absent
from `shelltutor` entirely.

**Confirms profile flag `drift-status-roadmap-vs-commit`.** STATUS.md
is named by its own Decision-Disagreement Rule (STATUS.md:65-69) as
the authoritative file for project posture; the rule is currently
violated by STATUS.md itself. This is the documentation–code consistency
theme's exemplar.

### `sandbox` / `$SANDBOX`

Used in two senses that share a substrate but differ in scope.

| Unit | Definition | Citation |
| --- | --- | --- |
| `shelltutor` | `$SANDBOX` is the per-learner working directory, default `$HOME/.shelltutor`, override `SHELLTUTOR_HOME`. `setup_sandbox()` creates fixture files and HISTFILE. | shelltutor:30, 66-80 |
| `shelltutor` | The practice subshell is launched inside `$SANDBOX` with HISTFILE bound to `$SANDBOX/.shelltutor_history`. | shelltutor:104-134 |
| `shelltutor` (welcome screen, user-facing) | "Everything happens in ~/.shelltutor; you cannot break anything." | shelltutor:169 |
| `README.md` | "lessons paired with safe, sandboxed practice." | README.md:18 |
| `AGENTS.md` | Lists "sandbox boundaries" as a "safety surface" element ('sensitive work' requires user direction) | AGENTS.md:71-73 |

Collision: **same-term-different-meaning** between two scopes:

- **Narrow scope** ($SANDBOX directory only) — accurate; tutor writes
  only inside `$HOME/.shelltutor`.
- **Wide scope** (overall safety guarantee that "you cannot break
  anything") — overstated; the practice subshell is a real interactive
  bash with the learner's normal user filesystem authority. Inside the
  subshell, `cd ..`, `rm`, and any normal user command remain
  available.

**Confirms profile flag `subshell-safety-claim-vs-shell-authority`**
(routed to Phase 6 for full analysis; Phase 1 records the vocabulary
basis).

### `operator` vs `learner`

Two distinct human roles, used consistently within their spheres.

| Unit | Term | Refers to | Citation |
| --- | --- | --- | --- |
| `AGENTS.md` | `operator` | Project owner / contributor / coding-agent's user | AGENTS.md:34-37, 71-73, 116-118 |
| `CLAUDE.md` | `operator` | Same | CLAUDE.md:19-22 |
| `CONTRIBUTING.md` | `operator name` | Forbidden assumption | CONTRIBUTING.md:42-46 |
| `ROADMAP.md` | `operator-name`, `operator or host` | Forbidden assumption | ROADMAP.md:38, 40, 44 |
| `README.md` | `operator name` | Forbidden assumption | README.md:20-23 |
| `README.md` | `learner` | Tutor's end user; person at the practice prompt | README.md:22, 62-65 |
| `ROADMAP.md` | `learner` | Same | ROADMAP.md:76, 107 |

No collision. The distinction is principled: `operator` = "person who
installs/runs the tutor on their machine"; `learner` = "person being
taught by the tutor." The script does not name either role in its
output (it addresses the learner with `you`).

The phrase **user-agnostic** elides this distinction by using `user`
to mean `operator`. See vocabulary entry for `user-agnostic`.

### `prompt`

Twelve occurrences across `shelltutor`; one each in `README.md`,
`CONTRIBUTING.md`, and `ROADMAP.md`. **All meanings are shell-related**;
the project carries zero LLM-prompt surface, so no audit-vocabulary
collision exists at the project level.

| Sense | Definition | Citation |
| --- | --- | --- |
| Shell prompt (`$` / `>`) | The text the shell displays when ready for input | shelltutor:155-161 (welcome screen explains it) |
| `shelltutor>` prompt | Practice subshell's PS1 | shelltutor:118 |
| `(reverse-i-search)` prompt | Bash history search prompt | shelltutor:208-216 |
| "prompt theme" | $PS1 customization (operator preference) | README.md:20-21, ROADMAP.md:38 |
| Pager prompt | `:` or `--More--` prompt inside `man` | shelltutor:188 |

Recorded as `not-a-prompt` in Phase 8 (these are CLI UI surfaces and
documentation about CLI UI; not model-mediated prompts). Vocabulary
entry exists to make the absence of LLM-prompt surface explicit.

### `portable` / `portability`

Claim: the tutor is portable across Linux and macOS terminals with no
prerequisite installation beyond bash 4+.

| Unit | Claim | Citation |
| --- | --- | --- |
| `README.md` | "Stay portable across Linux and macOS without environment assumptions." | README.md:63 |
| `README.md` | "Requirements: A POSIX-ish terminal (any modern Linux or macOS terminal works). `bash` 4+ on `PATH`." | README.md:50-55 |
| `AGENTS.md` | Defines portability regressions; lists requiring a specific username/hostname/distro/shell theme as a portability bug | AGENTS.md:89-90 |
| `AGENTS.md` | "Lessons must be runnable end-to-end on a clean Linux or macOS terminal without prerequisite installation beyond `bash`." | AGENTS.md:91-92 |
| `CONTRIBUTING.md` | "`shelltutor` is **user-agnostic** by contract. A change is a portability regression if it: Depends on tools beyond `bash` (4+) and a standard POSIX userland." | CONTRIBUTING.md:42-49 |
| `CONTRIBUTING.md` | Conditional rule: "If a lesson genuinely requires a non-portable surface, gate it on a runtime check and degrade gracefully — do not couple the script's default path to the non-portable surface." | CONTRIBUTING.md:51-54 |

Drift evidence inside lesson content (this is what the
`lesson-portability-gaps` audit-attention flag captures):

| Lesson | Construct | Why not portable | Citation |
| --- | --- | --- | --- |
| Lesson 7 | `free -h` | `free` is Linux-only; macOS ships `vm_stat` instead | shelltutor:328 |
| Lesson 7 | `cat /proc/cpuinfo`, `cat /proc/meminfo`, `ls /proc \| grep ^[0-9]` | The `/proc` filesystem does not exist on macOS | shelltutor:331-334 |
| Lesson 7 | "`/proc` is Linux's self-report folder." (text acknowledges Linux-only) | Acknowledged but not gated per the conditional rule | shelltutor:330 |
| Lesson 8 | `sudo dnf install cowsay figlet lolcat` | `dnf` is Fedora/RHEL; absent on macOS, Debian, Arch, etc. | shelltutor:346 |
| Lesson 8 | "Skip any that says 'command not found'." | Soft fallback at runtime; doesn't change the single-distro install hint | shelltutor:344 |

**Confirms profile flag `lesson-portability-gaps`.** Lesson 7's
acknowledgement ("Linux's self-report folder") is honest but not gated;
Lesson 8's install hint references one distro under a Linux+macOS
claim. The CONTRIBUTING.md:51-54 conditional rule provides the
remediation pattern.

### `single-file`

| Unit | Definition | Citation |
| --- | --- | --- |
| `README.md` | "The tutor is a single bash script with no installation step." | README.md:43-44 |
| `README.md` | "Be readable as a single script — a learner can open it and inspect the code that just ran them through a lesson." | README.md:64-66 |
| `README.md` | "Bundle into a package manager or framework. The tutor is one file on purpose." (in Non-Goals) | README.md:73-74 |
| (de-facto) | One executable file, 459 lines, no companion scripts or modules | `wc -l shelltutor`; `git ls-files` |

No collision. The single-file property is held by code state and by
governance text in agreement.

### Other coherent terms (no collision, no synonym)

| Term | Meaning | Status |
| --- | --- | --- |
| `lesson` | Bash function (`lesson1` … `lesson9`, `welcome`, `finale`) + the screen it renders | Consistent across script and docs (README, ROADMAP). |
| `tutor` | The script `shelltutor` and the experience it delivers | Consistent. |
| `practice subshell` / `practice()` | The interactive bash spawned at shelltutor:104-134 with rcfile that sets `cd "$SANDBOX"`, `PS1`, navigation functions | Consistent within the script; not separately defined in user-facing docs. |
| `Day-1 scaffold` | Current lifecycle posture (no tagged release; first audit cycle) | STATUS.md:18, consistent. |
| `Jefahnierocks` | Workspace owner / "semantic owner" of the repo | STATUS.md:21, consistent. |
| `prior-art` | The `fedora-top:~/Projects/shelltutor` source carried at commit `136f6a3` from 2026-05-17 | README.md:77-83, AGENTS.md:49-53, STATUS.md:31-33; consistent. |

## Comparison to `docs/audit/references/shell-research.md`

The operator supplied a curriculum reference targeting a different
goal: Shell Foundations for Vimtutor. The reference proposes 12
concepts and 6 units. shelltutor's lesson surface (welcome, lessons
1–9, finale) covers a subset:

| Reference concept | shelltutor coverage |
| --- | --- |
| Terminal / shell / command / program (Concept 1) | welcome + lesson 1 (`echo`, command structure) |
| Shell reads text in a structured way (Concept 2) | lesson 1 (commands, options, quoting via `echo "I am at the shell"`) |
| Current working directory (Concept 3) | partial — `pwd` introduced in lesson 7 only |
| Files, directories, pathnames (Concept 4) | partial — `cat`, `ls` used; `cp`/`mv`/`rm`/`mkdir`/`rmdir` not in lesson surface |
| Text files vs rendered documents (Concept 5) | not covered (out of scope per README non-goals) |
| Opening vs changing a file / buffer (Concept 6) | not covered — relevant only to a Vim-prereq goal, not shelltutor's stated goal |
| Command lookup / PATH (Concept 7) | not covered — `PATH` is named in the heredocs only when contrasting "prompt theme" |
| stdin / stdout / stderr (Concept 8) | implicit via lesson 5 pipes and lesson 6 redirection; not named explicitly |
| Full-screen programs (Concept 9) | implicit (`man` mentioned in lesson 1 as a pager via `q`) |
| Keyboard interpreted by current program (Concept 10) | implicit via Ctrl+C, Ctrl+R, Ctrl+L |
| Process control / Ctrl-C, Ctrl-D, Ctrl-Z (Concept 11) | partial — Ctrl+C only; Ctrl+D, Ctrl+Z absent |
| Man pages / built-in help (Concept 12) | partial — `man ls`, "man wc", "vimtutor" reference at finale |

**The vocabulary gap is intentional, not a defect.** shelltutor's
README explicitly lists shell-scripting, sysadmin-curriculum,
multi-user features, and network-aware lessons as non-goals
(README.md:67-75). The research doc targets a different downstream
goal (preparing for `vimtutor`); the project owner has not declared
that goal as in-scope. Vocabulary subset is recorded for Phase 8
authoring-artifact context, not as a finding.

## Boundary Declarations Honored (Phase 1)

- Did not infer term definitions from filenames alone.
- Did not propose renames (e.g., separating "user" in "user-agnostic"
  from "user" in "learner") — that is a Phase 10 fitness-function
  candidate, not a vocabulary fix.
- Did not collapse technical CLI terms (`prompt` = shell prompt) into
  audit-domain terms (`prompt` = LLM prompt). Both meanings recorded;
  no LLM-prompt surface exists.

## Exit Check

| Check | Status |
| --- | --- |
| Every term has at least one citation | ✅ |
| Every collision candidate has citations for each conflicting use | ✅ (3 collisions: user-agnostic, sandbox, WYN OPS) |
| Unsupported terms removed or marked `unclassified` | ✅ |

Phase 1 exit check **passes**. Advancing to Phase 2.
