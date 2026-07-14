---
title: shelltutor — 2026-07-14 Portability Findings
category: audit
component: findings
status: evidence
version: 0.1.0
last_updated: 2026-07-14
tags: [audit, findings, portability, ff-006a, ff-006b, bash]
priority: high
---

# 2026-07-14 — Portability Findings

Finding surfaced while reverifying the repository before publishing its
project-intelligence manifest. The repository was clean at baseline; this
finding was reproduced against the then-current default-branch revision
`9536b11`.

## F-009 — Practice startup fails across supported Bash generations

- **Severity**: 4 (release-blocking). With Bash 5.3.15 first on `PATH`, even
  `./shelltutor -h` could hang before argument dispatch. With macOS stock
  Bash 3.2.57, help worked but the Stage 1 PTY flow entered a practice shell
  without the navigation functions from the generated rcfile.
- **Surfaced by**: `make verify`, direct `-h` probes under both Bash versions,
  and the FF-006b `current-rc` Stage 1 PTY variant.
- **Observed causes**:
  1. Bash 5.1+ can write small here-documents to a pipe before starting the
     reader. On this macOS validation surface, the parent was observed blocked
     in `heredoc_write`; compatibility level 5.0 selects the prior
     temporary-file-backed path.
  2. Bash 3.2 parsed the process-substitution expression used for `--rcfile`
     but did not reliably load that generated rcfile. Supplying the same
     here-document on fd 3 and passing `/dev/fd/3` to `--rcfile` worked on
     both tested Bash generations.
- **Fix**: commit `d893ea8` sets `BASH_COMPAT=5.0`, supplies the practice
  rcfile on fd 3, and makes the compatibility assignment a smoke-test
  invariant. The two changes are intentionally paired: either change alone
  left one of the supported Bash generations failing.
- **Validation** (2026-07-14):
  - `make verify` — pass under Bash 5.3.15.
  - `make self-test` — all four checker suites pass.
  - `/bin/bash ./scripts/smoke-test.sh` — pass under Bash 3.2.57.
  - FF-006b Stage 1 `both` variants — gate passed and exit 0 under Bash
    3.2.57 and Bash 5.3.15.
  - `./shelltutor < /dev/null` — exit 1 with the documented no-TTY preflight
    diagnostic.
- **Limits**: this closes the locally reproduced regression. It does not
  close ROADMAP Phase 2: the full five-stage human walkthrough on macOS and
  Debian/Ubuntu-family Linux remains pending.
- **Status**: resolved by `d893ea8`.

Technical background: `BASH_COMPAT` is Bash's supported compatibility-level
control ([GNU Bash manual]); Bash's redirection implementation uses the
temporary-file path for compatibility levels through 5.0
([Bash 5.2 `redir.c`]).

[GNU Bash manual]: https://www.gnu.org/software/bash/manual/bash.html#index-BASH_005fCOMPAT
[Bash 5.2 `redir.c`]: https://sources.debian.org/src/bash/5.2.15-2/redir.c/
