---
title: shelltutor Research References
category: reference
component: research-index
status: active
version: 0.2.0
last_updated: 2026-05-22
tags: [research, references, audit, planning, verified]
priority: medium
---

# Research References

Repo-local research references used for `shelltutor` design, planning,
audit interpretation, and future implementation decisions.

These documents are planning inputs, not runtime authority. When a
reference recommends a behavior that would change the tutor's safety,
dependency, portability, or CLI contract, the implementation still has
to pass through `AGENTS.md`, `docs/contracts.md`, and the relevant
roadmap/status decisions.

**Verification pass (2026-05-22):** each reference has been audited to
separate **objective claims** (tool versions, format specs, Bash/Readline
behavior, manual citations) from **judgment** (recommended posture,
preferred persona set, pacing guidance). Objective items now carry
inline citations to current upstream sources where they exist;
judgment items are explicitly labeled as opinion so future readers
do not quote them as established fact. Notable corrections applied:

- `pty-harness-research.md` — Pexpect last release is 4.9.0
  (2023-11-25), not actively maintained; Expect (Tcl) last release is
  5.45.4 (2018-02-04). Both are flagged as legacy-risk.
- `simulation-evidence-model.md` — asciicast **v3** is the current
  format spec; v2 is still supported. Any new harness adopting a real
  asciicast container should target v3.
- `practice-shell-hardening-research.md` — env-var risks now cite the
  exact Bash manual sections; a ground-truth note describes what the
  practice rcfile in `shelltutor` actually does today.
- `shell-research.md` — `man cd` behavior on macOS (resolves to
  `builtin(1)`) noted; `help cd` flagged as the reliable beginner
  path.

| Reference | Use |
| --- | --- |
| `shell-research.md` | Curriculum basis for the five-stage `vimtutor` prerequisite course. |
| `persona-simulation-research.md` | Persona and simulation-design basis for future interactive walkthrough tooling. |
| `pty-harness-research.md` | Contributor-side PTY harness architecture for full interactive lesson-flow testing. |
| `simulation-evidence-model.md` | Evidence, logging, replay, annotation, and retention model for simulated or recorded walkthroughs. |
| `practice-shell-hardening-research.md` | Practice-shell portability, Readline/completion behavior, sandbox hardening, and command-safety policy. |
| `educational-design-research.md` | Curriculum sequence, pacing, feedback, age-appropriate framing, and pedagogy implications. |
