---
title: shelltutor Agents Contract
category: governance
component: agents-contract
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [agents, claude, codex, authority, boundary]
priority: high
---

# AGENTS.md — shelltutor

This file provides Codex, Claude Code, and other coding agents with local
guidance for:

```text
/Users/verlyn13/Organizations/jefahnierocks/shelltutor
```

The Jefahnierocks workspace contract at
`/Users/verlyn13/Organizations/jefahnierocks/AGENTS.md` also applies inside
this repository. Rules in that file and rules restated here are stated on
shelltutor's own authority, on Jefahnierocks's own authority — they are not
inherited from a parent organization at runtime. Where a parent
organizational spec is the original source of a rule, the parent is cited as
a reference, not a runtime authority.

When guidance conflicts, the closest local rule wins inside this repository,
while the Jefahnierocks workspace boundary still applies.

## Identity

`shelltutor` is a single-file interactive tutor for the Unix shell. The
project's defining property is that it is **user-agnostic**: no operator
name, distro, hostname, theme, home-directory layout, or pre-existing shell
setup is assumed by the script or by any document in this repository.

When a change would couple the tutor to a specific user, host, or
operator-private environment, pause and propose a portable alternative
before applying.

## Scope

Stay inside `/Users/verlyn13/Organizations/jefahnierocks/shelltutor` for
normal work. Reading or modifying material outside this repository requires
explicit user scope expansion.

The prior-art repository at `fedora-top:~/Projects/shelltutor` is intake
provenance only. Do not treat its current state as ambient truth, and do not
silently re-import its user-specific surfaces (`wyn-setup/`, theme branding,
operator-named comments).

## Agent Roles

- **Builder** — Implement scoped changes to the tutor script, lessons, and
  documentation.
- **Maintainer** — Keep portability claims, lesson surface, and docs
  coherent across changes.
- **Reviewer** — Surface portability regressions, hidden host assumptions,
  unsafe shell idioms, lessons that would mislead beginners, and any
  re-introduction of user-specific content.
- **Operator** — Run the tutor locally during validation; prefer
  reproducible invocations over interactive demos.

## Authority Levels

- **Routine work** — Read and edit files inside this repository, run the
  tutor for validation, edit lessons, update documentation, and adjust
  portability shims.
- **Sensitive work** — Change the tutor's safety surface (file writes,
  network access, privilege handling, sandbox boundaries) only when the
  user request clearly calls for it.
- **Restricted work** — Do not introduce dependencies that require
  installation outside `bash` and a standard POSIX userland; do not access
  files outside this repository during normal operation; do not perform
  account, billing, or credential changes.

When authority is unclear, ask before acting.

## Work Rules

- Use Conventional Commits for any commits created (`type(scope):
  description`).
- Keep each change focused and inspectable; one coherent change per commit.
- Preserve linear history; do not rewrite unrelated history.
- The tutor must not write outside its own working directory, must not
  request elevated privileges, and must not reach the network.
- Treat anything that requires a specific username, hostname, distro, or
  shell theme as a portability bug.
- Lessons must be runnable end-to-end on a clean Linux or macOS terminal
  without prerequisite installation beyond `bash`.

## Validation

- Run the tutor (`./shelltutor`) and complete at least the lesson surface
  affected by a change.
- For portability changes, validate on both Linux and macOS when possible,
  or state which surface was tested and which is pending.
- For documentation-only changes, check links, paths, and that frontmatter
  fields remain accurate.

## Active Artifacts

Read these before any substantive change. They are the durable record of
prior decisions and ongoing direction; not reading them means re-deriving
context that already exists.

- `audit/2026-05-21/SUMMARY.md` — first audit cycle (Agentic Architecture
  Audit Spec v3.1). Seven active findings (`F-001`–`F-007`) all
  smoke-tested `confirmed-current` at revision `e6257aa`. Seven proposed
  fitness functions (`FF-001`–`FF-007`).
- `profile/2026-05-21/project_profile.yaml` and `profile-discovery.md` —
  first profile snapshot (Project Profile Discovery Directive v1.2).
- `ROADMAP.md` Phase 3 — curriculum redesign spec: five mastery-gated
  stages, vimtutor-prerequisite framing, 3/3 recall + task gates.
- `docs/audit/references/shell-research.md` — operator-supplied
  curriculum reference (Shell Foundations for `vimtutor`). The Phase 3
  spec maps to its 12 concepts and 6 units.
- `docs/audit/directives/agentic-architecture-audit-v3.1-package/` —
  authority texts the profile and audit were generated against;
  not modified, treated as an in-repo snapshot.

If a change touches one of the findings or fitness functions, cite the
ID in the commit body (e.g., `refactor(welcome): narrow sandbox claim
(F-002)`).

## Secrets And Sensitive Data

Do not commit secrets, credentials, account identifiers, private financial
data, or sensitive personal data. The tutor is public and reads from a
public repository; it must remain safe to run on any stranger's machine.

Use placeholders in examples. If sensitive data is found in tracked content,
stop and tell the user before making broader changes.

## Escalation

Pause and ask the user when:

- A change would re-introduce user-specific framing, theme branding, or
  operator-named content.
- A change would broaden the tutor's safety surface (filesystem writes,
  network calls, privileged operations).
- A change would couple the tutor to a particular host, distro, or shell
  ecosystem.
- License posture comes up in a way that requires a decision.
- Local instructions conflict or the correct authority level is unclear.

When escalating, give the smallest useful summary: what is blocked, why it
matters, and the exact decision needed.
