---
title: shelltutor Contributing
category: process
component: contributing
status: active
version: 0.1.0
last_updated: 2026-05-21
tags: [contributing, verification, change-discipline]
priority: medium
---

# Contributing

Use focused changes and keep the tutor, its lessons, and its documentation
aligned.

## Change Discipline

- **Conventional Commits**: `type(scope): description`. Common types:
  `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.
- One coherent change per commit. Do not bundle unrelated edits.
- Linear history. No merge commits.

## Local Verification

```bash
./shelltutor
```

Walk the affected lesson surface. If you cannot run the tutor (no bash 4+,
unsupported terminal, etc.), state that verification is pending rather than
implying success.

If `shellcheck` is available, run it against the script:

```bash
shellcheck shelltutor
```

## Portability Rules

`shelltutor` is **user-agnostic** by contract. A change is a portability
regression if it:

- Requires a specific operator name, hostname, distro, or shell theme.
- Depends on tools beyond `bash` (4+) and a standard POSIX userland.
- Writes outside the script's working directory, asks for elevated
  privileges, or reaches the network.
- Assumes a particular `$HOME` layout, prompt, or pre-existing
  configuration.

If a lesson genuinely requires a non-portable surface, gate it on a runtime
check and degrade gracefully — do not couple the script's default path to
the non-portable surface.

## Evidence Rules

- When importing or porting material from prior-art (e.g.,
  `fedora-top:~/Projects/shelltutor`), cite the source path and commit SHA
  in the commit body.
- Keep planned, prototyped, and implemented lesson states separate in
  `ROADMAP.md` and `STATUS.md`.

## Secrets

Do not commit secrets, credentials, account identifiers, or private personal
data. The tutor is public and must remain safe to run on any stranger's
machine.

## GitHub Posture

Following the Jefahnierocks workspace posture, this repository intentionally
omits CI workflows, `CODEOWNERS`, PR templates, branch protection, and
Actions secrets until a real activation trigger exists. Until then, local
commit discipline is the enforcement layer.
