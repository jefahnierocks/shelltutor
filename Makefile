# Makefile — quality-tooling targets for shelltutor.
#
# Bash-only / POSIX-userland operations per AGENTS.md "Authority Levels".
# Optional contributor-side tools (shellcheck) are invoked only when
# present. CI activation is deferred per CONTRIBUTING.md "GitHub Posture";
# these targets give contributors a one-command pre-commit verification
# without imposing a CI dependency.
#
# Targets:
#   check        FF-001 + FF-002 + FF-004 + FF-007 static analysis (default)
#   lint         shellcheck shelltutor (FF-005; warns if shellcheck absent)
#   smoke        FF-006a minimal smoke test
#   verify       check + lint + smoke (full pre-commit gate)
#   self-test    run checker self-tests against built-in fixtures
#   help         list targets

.PHONY: help check check-safety check-governance check-portability lint smoke lesson-flow verify self-test

SCRIPT := shelltutor

# Optional pass-through args for `lesson-flow`, e.g.:
#   make lesson-flow SIMARGS='--variant current-rc -v'
SIMARGS ?=

help:
	@printf 'Targets:\n'
	@printf '  check        FF-001 + FF-002 + FF-004 + FF-007 static analysis (default)\n'
	@printf '  lint         shellcheck $(SCRIPT) (FF-005)\n'
	@printf '  smoke        FF-006a minimal static smoke test\n'
	@printf '  lesson-flow  FF-006b PTY harness (optional; Python 3.9+; not in verify)\n'
	@printf '  verify       check + lint + smoke\n'
	@printf '  self-test    run checker self-tests\n'

check: check-safety check-governance check-portability

check-safety:
	@./scripts/check-safety.sh

check-governance:
	@./scripts/check-governance.sh

check-portability:
	@./scripts/check-portability.sh

lint:
	@if command -v shellcheck >/dev/null 2>&1; then \
	    shellcheck -s bash -S warning $(SCRIPT) && printf 'lint: clean (%s)\n' "$(SCRIPT)"; \
	else \
	    printf 'lint: shellcheck not installed; skipping local FF-005 run\n'; \
	fi

smoke:
	@if [ -x ./scripts/smoke-test.sh ]; then \
	    ./scripts/smoke-test.sh; \
	else \
	    printf 'smoke: scripts/smoke-test.sh not present yet (FF-006a deferred)\n'; \
	fi

# FF-006b — optional PTY harness. Skips quietly when python3 is missing
# or too old, so contributors without Python tooling are not blocked.
# Per docs/simulation-design-plan.md, this target is NOT part of
# `make verify`; the runtime tutor stays bash-only.
lesson-flow:
	@if command -v python3 >/dev/null 2>&1; then \
	    if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)' 2>/dev/null; then \
	        if [ -f ./scripts/sim/run.py ]; then \
	            python3 ./scripts/sim/run.py $(SIMARGS); \
	        else \
	            printf 'lesson-flow: scripts/sim/run.py not present yet (FF-006b deferred to Slice 1)\n'; \
	        fi; \
	    else \
	        printf 'lesson-flow: python3 too old (need 3.9+); skipping (FF-006b)\n'; \
	    fi; \
	else \
	    printf 'lesson-flow: python3 not found; skipping (FF-006b; see docs/simulation-design-plan.md)\n'; \
	fi

verify: check lint smoke

self-test:
	@./scripts/check-safety.sh --self-test
	@./scripts/check-governance.sh --self-test
	@./scripts/check-portability.sh --self-test
	@./scripts/smoke-test.sh --self-test
