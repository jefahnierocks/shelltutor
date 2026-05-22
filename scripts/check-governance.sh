#!/usr/bin/env bash
# check-governance.sh — operationalize audit FF-007 against tracked governance.
#
# FF-007 (avoid absolute machine-local paths in governance citations) per
# audit/2026-05-21/10-fitness-functions.md:
#   Governance Markdown files must not contain absolute filesystem paths
#   beginning with operator-private prefixes:
#     /Users/    /home/    /root/    C:\
#   A contributor cloning the repository should be able to read the
#   governance docs without operator-local context.
#
# Within fenced code blocks (```...```) the rule is relaxed because
# fences are commonly used to demonstrate path-shapes pedagogically.
# Inline backtick spans are NOT skipped — a `/Users/...` inline still
# counts as operator-private content for the purposes of this check.
#
# Default file set: README.md AGENTS.md CLAUDE.md CONTRIBUTING.md
# STATUS.md ROADMAP.md. Pass explicit paths to check other files.
#
# Usage:
#   ./scripts/check-governance.sh                  # default set
#   ./scripts/check-governance.sh file.md ...      # explicit files
#   ./scripts/check-governance.sh --self-test      # built-in fixtures
#
# Exit codes:
#   0  clean
#   1  violations found
#   2  usage error

set -eu

DEFAULT_FILES=(README.md AGENTS.md CLAUDE.md CONTRIBUTING.md STATUS.md ROADMAP.md)

awk_check() {
    awk '
        BEGIN {
            in_fenced = 0
            violations = 0
        }

        # Toggle fenced-code-block state on triple-backtick lines.
        /^```/ {
            in_fenced = !in_fenced
            next
        }
        in_fenced { next }

        # Forbidden absolute path prefixes.
        match($0, /\/Users\/|\/home\/[a-zA-Z]|\/root\/[a-zA-Z]|C:\\/) {
            printf "%s:%d: FF-007 absolute path: %s\n", FILENAME, NR, $0
            violations++
        }

        END {
            exit (violations > 0 ? 1 : 0)
        }
    ' "$@"
}

self_test() {
    local tmp_pass tmp_fail
    tmp_pass="$(mktemp -t check-governance-pass.XXXXXX)"
    tmp_fail="$(mktemp -t check-governance-fail.XXXXXX)"
    # Expand at trap-set time so paths survive set -u after locals exit scope.
    # shellcheck disable=SC2064
    trap "rm -f '$tmp_pass' '$tmp_fail'" EXIT

    cat > "$tmp_pass" <<'PASS'
# Title

Stay inside this repository.

Inside a fenced block, path-shapes are demonstrative and skipped:
```
/Users/example/path
```

But the text above the fence carries no operator-local paths.
PASS

    cat > "$tmp_fail" <<'FAIL'
# Title

Stay inside /Users/verlyn13/Organizations/shelltutor for normal work.
FAIL

    printf 'self-test: known-good fixture should pass        ... '
    if awk_check "$tmp_pass" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker rejected the clean fixture)\n' >&2
        return 1
    fi

    printf 'self-test: known-bad fixture should be flagged   ... '
    if ! awk_check "$tmp_fail" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker missed an FF-007 violation)\n' >&2
        return 1
    fi

    printf 'self-test: all cases pass.\n'
}

main() {
    if [ "${1:-}" = "--self-test" ]; then
        self_test
        return $?
    fi

    local files=()
    if [ $# -eq 0 ]; then
        files=("${DEFAULT_FILES[@]}")
    else
        files=("$@")
    fi

    # Filter to existing files.
    local existing=()
    local f
    for f in "${files[@]}"; do
        [ -f "$f" ] && existing+=("$f")
    done

    if [ ${#existing[@]} -eq 0 ]; then
        printf 'check-governance: no files to check\n' >&2
        return 2
    fi

    if awk_check "${existing[@]}"; then
        if [ ${#existing[@]} -eq 1 ]; then
            printf 'check-governance: clean (1 file)\n'
        else
            printf 'check-governance: clean (%d files)\n' "${#existing[@]}"
        fi
        return 0
    else
        printf 'check-governance: violations found\n' >&2
        return 1
    fi
}

main "$@"
