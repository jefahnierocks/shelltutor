---
title: shelltutor Audit — Phase 10 Findings
category: audit
component: phase-10-findings
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [audit, phase-10, findings]
priority: high
---

# Phase 10 — Findings

Seven current-state findings. All seven were identified by routed
audit-attention flags or by phase-specific evidence in Phases 1, 6, 8,
and 9. Smoke-test outcomes are recorded in `10.5-finding-smoke-test`
after this file is finalized; current snapshot evidence is below.

Priority formula (§10.1):
`priority = severity × confidence × strategic_weight × reversibility_factor`

| ID | Title | Sev | Conf | Strat | Rev | Priority |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| F-001 | Documentation drift: STATUS/ROADMAP claim user-agnostic refactor pending; commit `e6257aa` shows it complete | 2 | 1.0 | direct (1.5) | 1.0 | 3.0 |
| F-002 | Welcome-screen sandbox-safety claim broader than the practice subshell actually sandboxes | 2 | 1.0 | direct (1.5) | 1.0 | 3.0 |
| F-003 | Lesson portability gaps: Lesson 7 (`/proc`, `free -h`) and Lesson 8 (`sudo dnf install`) use platform-specific surfaces without the gate-and-fallback pattern from CONTRIBUTING.md:51-54 | 2 | 1.0 | direct (1.5) | 1.0 | 3.0 |
| F-004 | Safety policy rules in AGENTS.md (no privilege, no network, no writes outside `$SANDBOX`) have no code-level enforcement | 2 | 0.9 | indirect (1.2) | 1.0 | 2.16 |
| F-007 | De-facto external contracts (CLI args, exit codes, env vars, sandbox file layout) lack formal schemas | 1 | 1.0 | indirect (1.2) | 1.0 | 1.2 |
| F-005 | `AGENTS.md:22` cites parent workspace governance by absolute machine-local path | 1 | 1.0 | none (1.0) | 1.0 | 1.0 |
| F-006 | No automated eval / smoke / regression coverage for any path | 1 | 1.0 | none (1.0) | 1.0 | 1.0 |

(Priorities are ordinal hints; tied entries are listed by chronological
audit-attention order.)

---

## F-001 — Documentation drift in STATUS.md and ROADMAP.md

| Field | Value |
| --- | --- |
| Dimension | 11.10 Governance and audit trail |
| Severity | 2 |
| Confidence | 1.0 |
| Status | active |
| Strategic relevance | direct (Documentation–code consistency theme) |
| Finding bucket | documentation-consistency |
| Related fitness function | FF-003 |
| Recommendation boundary | Update `STATUS.md` (lines 33-34 and 41-46) and `ROADMAP.md` (Phase 1 section, lines 30-46) to reflect that the user-agnostic refactor commit `e6257aa` has been performed. Do not change the underlying posture, only the temporal claim. Scope: two documentation files; no script changes. |

**Substance.** `STATUS.md` line 33-34 says the imported script "still
carries two `WYN OPS` accent comments (lines 17 and 35)" and lists the
user-agnostic refactor as Immediate Next Step #1 (lines 41-46).
`ROADMAP.md` makes the same claim under Phase 1 — "User-Agnostic
Refactor" (lines 30-46). Both files are dated `2026-05-21`. But the
git log at that same date shows commit `e6257aa` ("refactor: remove
user-specific accent branding from tutor"). The current `shelltutor`
script's lines 17 and 35 carry neutral content; grep for `WYN OPS` in
the script returns zero matches.

`STATUS.md` Decision-Disagreement Rule (lines 65-69) names STATUS.md
itself as the authoritative file for project posture, so this is a
self-inconsistency that should be fixed in STATUS first, with ROADMAP
updated to match.

**Evidence (snapshot):**

```text
STATUS.md:33-34   "The imported script still carries two `WYN OPS` accent comments (lines 17 and 35); user-agnostic refactor is the next change."
STATUS.md:41-43   "**User-agnostic refactor commit** — replace `WYN OPS` accent comments with neutral wording"
ROADMAP.md:30-46  "Phase 1 — User-Agnostic Refactor ... Replace `WYN OPS` accent comments with neutral language."
shelltutor:17     "#   - Title + action footer styled with a single accent color."
shelltutor:35     "    H1=$'\\e[1;38;5;208m'      # lesson title — bold orange accent"
git log           "e6257aa refactor: remove user-specific accent branding from tutor"
```

(see `10-findings.json` for the structured citations)

---

## F-002 — Welcome-screen sandbox claim overstates actual scope

| Field | Value |
| --- | --- |
| Dimension | 11.6 Authority boundaries |
| Severity | 2 |
| Confidence | 1.0 |
| Status | active |
| Strategic relevance | direct (matches operator focus question) |
| Finding bucket | authority-claim-accuracy |
| Related fitness function | (manual-review-only — text-content claim; no automatable rule) |
| Recommendation boundary | Narrow `shelltutor:169` welcome-screen text to match implementation. Example wording: replace "you cannot break anything" with text that scopes the safety claim to the tutor's own writes (e.g., "Your tutor work happens in `~/.shelltutor`. Things you type at the practice prompt run as ordinary commands in your account."). Scope: 1 line in the script; no change to authority model. |

**Substance.** `shelltutor:169` (welcome heredoc, addressed to the
learner) reads: "Everything happens in `~/.shelltutor`; you cannot
break anything." The actual sandboxing implemented at
`shelltutor:104-134` is narrow:

- `cd "$SANDBOX"` sets the practice subshell's CWD.
- `HISTFILE="$SANDBOX/.shelltutor_history"` sandboxes bash history
  away from `~/.bash_history`.
- `PS1='shelltutor> '` re-prompts the learner.
- Five navigation builtins are overridden to exit with codes 0/97/98/99.

Everything else inside the practice subshell is a real interactive
bash with the learner's normal user-mode filesystem authority. `cd ..`
works; `rm` works; any command on `$PATH` runs as the learner.

The directive flags this as `undeclared-scope` and `ambient-authority`
(not `escalation`, because the learner already had this authority
before opening the tutor — see Phase 6 reasoning).

**Constraint.** Strengthening the implementation (Bubblewrap, firejail,
chroot, namespaces, macOS `sandbox-exec`) violates `AGENTS.md:75-78`
("Do not introduce dependencies that require installation outside
`bash` and a standard POSIX userland"). The remediation path is
narrowing the claim.

---

## F-003 — Lesson portability gaps in lessons 7 and 8

| Field | Value |
| --- | --- |
| Dimension | 11.1 Bounded contexts / 11.3 Contract discipline |
| Severity | 2 |
| Confidence | 1.0 |
| Status | active |
| Strategic relevance | direct (Single-file portability theme) |
| Finding bucket | lesson-portability |
| Related fitness function | FF-004 |
| Recommendation boundary | Either (a) apply CONTRIBUTING.md:51-54's gate-and-fallback pattern to lesson 7's `/proc` and `free -h` references and to lesson 8's `dnf` install hint, or (b) narrow the portability claim in `README.md`, `AGENTS.md`, and `CONTRIBUTING.md` to "Linux first, macOS best-effort." Scope: ~30 lines of lesson heredoc OR three lines of governance text. |

**Substance.** Repository claim (`README.md:50-63`, `AGENTS.md:91-92`,
`CONTRIBUTING.md:42-49`): clean Linux+macOS coverage with bash-only
dependency. Lesson contradictions:

- **Lesson 7 (shelltutor:319-336):** `free -h`, `cat /proc/cpuinfo`,
  `cat /proc/meminfo`, `ls /proc | grep ^[0-9] | wc -l`. `/proc` does
  not exist on macOS; `free` is not a default macOS binary. Line 330
  acknowledges Linux-only (`"/proc is Linux's self-report folder."`)
  but does not gate via runtime check.
- **Lesson 8 (shelltutor:340-362):** `sudo dnf install cowsay figlet
  lolcat` (line 346). `dnf` is Fedora/RHEL only. Line 344 instructs
  "Skip any that says 'command not found'" — this softens the runtime
  failure but does not change the single-distro install hint.

CONTRIBUTING.md:51-54 establishes the project's own remediation
pattern: "If a lesson genuinely requires a non-portable surface, gate
it on a runtime check and degrade gracefully — do not couple the
script's default path to the non-portable surface." Neither lesson 7
nor lesson 8 applies this pattern.

---

## F-004 — Safety rules in AGENTS.md have no code-level enforcement

| Field | Value |
| --- | --- |
| Dimension | 11.8 Policy/prompt separation / 11.11 Architectural fitness functions |
| Severity | 2 |
| Confidence | 0.9 |
| Status | active |
| Strategic relevance | indirect (Documentation–code consistency theme — rules are documented; the gap is enforcement) |
| Finding bucket | safety-rule-enforcement |
| Related fitness function | FF-001, FF-002 |
| Recommendation boundary | Add two static-analysis checks (FF-001 safety-rule scan; FF-002 write-scope scan). Implementation does not require CI activation; both can run as a pre-commit hook OR as a `Makefile` target OR as a manual-review checklist documented in `CONTRIBUTING.md`. Scope: one new script or section in CONTRIBUTING.md. |

**Substance.** `AGENTS.md:75-92` declares six policy-bearing rules
(no writes outside `$SANDBOX`, no privilege, no network, no
non-bash/non-POSIX deps, lessons must run on clean Linux/macOS, no
host-specific assumptions). The current script honors all six. But
the rules live exclusively in a `skill-or-sop` file with no code-level
enforcement:

- no `.git/hooks/pre-commit`
- no `.github/workflows/`
- no test asserting the absence of `sudo`/`curl`/`wget`
- no `Makefile` target with a verification step

If a future commit introduced `curl` for telemetry, or `sudo` for an
install step, only manual review at commit time would catch it. The
profile's `known_debt` records "GitHub-side automation deferred per
workspace posture"; this finding records that the **policy
verification** layer is also deferred, and that two
static-analysis fitness functions can deliver verification without
requiring full CI (a pre-commit hook or a Makefile target suffices).

---

## F-005 — AGENTS.md cites parent workspace by absolute machine-local path

| Field | Value |
| --- | --- |
| Dimension | 11.10 Governance and audit trail |
| Severity | 1 |
| Confidence | 1.0 |
| Status | active |
| Strategic relevance | none |
| Finding bucket | governance-citation-style |
| Related fitness function | FF-007 |
| Recommendation boundary | Replace the absolute path in `AGENTS.md:22` with either a relative path expression (e.g., `../AGENTS.md`) or a phrase without a filesystem citation (e.g., "the Jefahnierocks workspace contract"). The rules are restated locally on lines 24-30; the absolute path is informational. Scope: 1 line. |

**Substance.** `AGENTS.md:21-23` reads:

> "The Jefahnierocks workspace contract at
> `/Users/verlyn13/Organizations/jefahnierocks/AGENTS.md` also applies
> inside this repository."

A stranger cloning this repo cannot resolve the absolute path. The
file immediately restates the relevant rules on shelltutor's own
authority (lines 24-30), so the reference is **informational
provenance**, not load-bearing — the strict consequence is cosmetic.
Still, the project's user-agnostic contract (it does not assume an
operator name, host, distro, etc.) would benefit from removing the
machine-local citation from the canonical governance file.

Classification per §9.6: `cosmetic-or-framing-deviation`.

---

## F-006 — No automated eval / smoke / regression coverage for any path

| Field | Value |
| --- | --- |
| Dimension | 11.9 Evals and quality gates |
| Severity | 1 |
| Confidence | 1.0 |
| Status | active |
| Strategic relevance | none |
| Finding bucket | quality-gates |
| Related fitness function | FF-005, FF-006 |
| Recommendation boundary | Either (a) implement FF-005 (a `shellcheck shelltutor` clean pass, per ROADMAP Phase 2 exit criterion) and FF-006 (an end-to-end smoke test that drives the lesson dispatcher non-interactively), or (b) execute the ROADMAP Phase 2 manual walkthrough on macOS + Linux and record the result in `STATUS.md` (a non-automated quality gate is still a quality gate). Scope: new test infrastructure OR a STATUS.md update with a date-stamped validation note. |

**Substance.** No `tests/`, `evals/`, `__tests__/`, `*.test.*`,
`bats/`, or similar files exist. The project plans two quality gates
(manual lesson walkthrough on macOS/Linux; `shellcheck shelltutor`
clean — both at ROADMAP.md Phase 2), but neither is recorded as
executed. Specific uncovered surfaces (per Phase 9):

- **approval-path-untested**: three contributor-side approval gates
  (AGENTS.md:43-78) enforced only by CONTRIBUTING.md:72-75 norms.
- **memory-lifecycle-untested**: `.progress` create/append/delete
  lifecycle and `read_progress` regex parsing have no unit test.
- **lesson-end-to-end**: manual walkthrough pending; no automated
  regression for lesson screen-flow or navigation builtins.

Severity 1 because the project is correctly classified as Day-1
scaffold with no production runtime; missing evals at this lifecycle
stage are appropriate. The finding exists so that the next cycle can
distinguish "evals never set up" from "evals lapsed."

---

## F-007 — De-facto external contracts lack formal schemas

| Field | Value |
| --- | --- |
| Dimension | 11.3 Contract discipline |
| Severity | 1 |
| Confidence | 1.0 |
| Status | active |
| Strategic relevance | indirect (Single-file portability theme — formal contracts would tighten the portability surface) |
| Finding bucket | contract-formalization |
| Related fitness function | (none yet — see Recommendation boundary) |
| Recommendation boundary | Not actionable at current scope. Document the four de-facto contracts (CLI args, exit codes, env vars, sandbox layout) in a single "Contracts" section of `README.md` or in a new `docs/contracts.md`. No machine-readable schema is warranted for a single-file CLI with no public SDK. Promote to formal schema only when (a) release posture closes per ROADMAP Phase 4, (b) lessons become jump-addressable per ROADMAP Phase 3 — at which point lesson IDs become a contract, or (c) `SHELLTUTOR_HOME` becomes a documented integration point for other tools. |

**Substance.** Phase 4 inventory records six contracts, all `ad-hoc`:

- C-001 CLI args (`-h`, `1-9`, default)
- C-002 practice() exit codes (0 / 97 / 98 / 99)
- C-003 sandbox file layout
- C-004 environment variable inputs (`SHELLTUTOR_HOME`, `NO_COLOR`)
- C-005 `-h` usage text
- C-006 lesson heredoc content

For a 459-line single-file CLI with a human consumer at a terminal,
ad-hoc contracts are appropriate. Documenting them in one place would
help future maintainers and would convert "contract by code reading"
into "contract by reference," which the strategic-theme weighting on
single-file portability is sensitive to.

---

## Caveats per §9.6

- `F-002` recommendation involves text content that is hard to test
  for automatically. Caveat type: `substantive-deviation` —
  remediation is operator-judgment-bound (what wording matches the
  actual sandboxing).
- `F-005` is `cosmetic-or-framing-deviation` per §9.6. Honest signal,
  low priority.
- All other findings are `substantive-deviation`.

## Smoke-Test Forward

All seven findings cite the snapshot revision `e6257aa`, which is
also the current branch tip at audit time. Phase 10.5 will re-verify
each citation against the current branch; outcomes are expected to be
`confirmed-current` for all seven (no commits since snapshot).
