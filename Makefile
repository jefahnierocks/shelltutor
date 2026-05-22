# Makefile — quality-tooling targets for shelltutor.
#
# Bash-only / POSIX-userland operations per AGENTS.md:75-78.
# Optional contributor-side tools (shellcheck) are invoked only when
# present. CI activation is deferred per CONTRIBUTING.md "GitHub Posture";
# these targets give contributors a one-command pre-commit verification
# without imposing a CI dependency.
#
# Targets:
#   check        FF-001 + FF-002 + FF-007 static analysis (default)
#   lint         shellcheck shelltutor (FF-005; warns if shellcheck absent)
#   smoke        FF-006 minimal smoke test
#   verify       check + lint + smoke (full pre-commit gate)
#   self-test    run checker self-tests against built-in fixtures
#   help         list targets

.PHONY: help check check-safety check-governance check-portability lint smoke verify self-test

SCRIPT := shelltutor

help:
	@printf 'Targets:\n'
	@printf '  check        FF-001 + FF-002 + FF-004 + FF-007 static analysis (default)\n'
	@printf '  lint         shellcheck $(SCRIPT) (FF-005)\n'
	@printf '  smoke        FF-006 minimal smoke test\n'
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
	    printf 'lint: shellcheck not installed; skipping (FF-005 deferred)\n'; \
	fi

smoke:
	@if [ -x ./scripts/smoke-test.sh ]; then \
	    ./scripts/smoke-test.sh; \
	else \
	    printf 'smoke: scripts/smoke-test.sh not present yet (FF-006 deferred)\n'; \
	fi

verify: check lint smoke

self-test:
	@./scripts/check-safety.sh --self-test
	@./scripts/check-governance.sh --self-test
	@./scripts/check-portability.sh --self-test
	@./scripts/smoke-test.sh --self-test
