#!/usr/bin/env bash
# smoke-test.sh — operationalize audit FF-006 (minimum-viable variant).
#
# Full audit FF-006 calls for a non-interactive lesson-flow harness that
# drives the practice subshell via pty (expect / python pty / socat). That
# variant is demoted to manual-review-only per Phase 10.5 because it
# requires a non-bash dependency forbidden by AGENTS.md:75-78.
#
# This script implements the static / -h-flag variant that remained at
# enforcement_category: static-analysis. It does three things:
#
#   1. bash-syntax check          (`bash -n shelltutor`)
#   2. help-text content check    (./shelltutor -h | grep …)
#   3. structural invariants      (grep for required functions, constants)
#   4. error-path behaviour       (./shelltutor <bad-arg> exits non-zero)
#
# Together these catch the obvious regression classes: syntax break,
# accidental help-text drift, dropped stage function, dispatcher logic
# rewritten to silently accept invalid input.
#
# Self-test (`--self-test`) verifies the smoke harness itself by running
# it against a known-good copy of the script AND a tampered copy.
#
# Usage:
#   ./scripts/smoke-test.sh                 # smoke ./shelltutor
#   ./scripts/smoke-test.sh path/to/script  # smoke a specific path
#   ./scripts/smoke-test.sh --self-test     # exercise the smoke harness
#
# Exit codes:
#   0  all smoke checks pass
#   1  one or more checks failed
#   2  usage error

set -eu

# ---------------------------------------------------------------------
# Smoke checks
# ---------------------------------------------------------------------

smoke_run() {
    local script="$1"
    local failed=0
    local out

    if [ ! -f "$script" ]; then
        printf 'smoke: error: not a file: %s\n' "$script" >&2
        return 2
    fi
    if [ ! -x "$script" ]; then
        printf 'smoke: error: not executable: %s\n' "$script" >&2
        return 2
    fi

    # Normalize the path for direct invocation: a bare filename needs the
    # ./ prefix because the repository root is not typically on $PATH.
    # An absolute path or any path with a / component is used as-is.
    local invoke_path="$script"
    case "$invoke_path" in
        /*|*/*) ;;
        *) invoke_path="./$invoke_path" ;;
    esac

    # 1. bash syntax
    if bash -n "$script" 2>/dev/null; then
        printf '  ✓ bash -n             %s\n' "$script"
    else
        printf '  ✗ bash -n             %s — parse error\n' "$script" >&2
        bash -n "$script" >&2 || true
        failed=1
    fi

    # 2. help-text content
    if out=$("$invoke_path" -h 2>&1); then
        local h_failed=0
        printf '%s\n' "$out" | grep -q 'vimtutor prerequisite' \
            || { printf '  ✗ -h missing: "vimtutor prerequisite"\n' >&2; h_failed=1; }
        printf '%s\n' "$out" | grep -q '1\.\.5' \
            || { printf '  ✗ -h missing: stage range "1..5"\n' >&2; h_failed=1; }
        printf '%s\n' "$out" | grep -qi 'Stages:' \
            || { printf '  ✗ -h missing: "Stages:" header\n' >&2; h_failed=1; }
        printf '%s\n' "$out" | grep -q 'check' \
            || { printf '  ✗ -h missing: "check" navigation word\n' >&2; h_failed=1; }
        if [ "$h_failed" -eq 0 ]; then
            printf '  ✓ -h content         "vimtutor prerequisite", "1..5", "Stages:", "check"\n'
        else
            failed=1
        fi
    else
        printf '  ✗ -h exited non-zero\n' >&2
        failed=1
    fi

    # 3. structural invariants — required functions and constants
    local s_failed=0
    local missing=""
    local n
    for n in 1 2 3 4 5; do
        grep -q "^stage${n}_intro()" "$script" \
            || { missing+=" stage${n}_intro"; s_failed=1; }
        grep -q "^stage${n}_gate()" "$script" \
            || { missing+=" stage${n}_gate"; s_failed=1; }
        grep -q "^run_stage${n}()" "$script" \
            || { missing+=" run_stage${n}"; s_failed=1; }
    done
    grep -q '^main()' "$script"        || { missing+=" main"; s_failed=1; }
    grep -q '^main "\$@"$' "$script"   || { missing+=" main\"\$@\"-call"; s_failed=1; }
    grep -q '^TOTAL_STAGES=5$' "$script" || { missing+=" TOTAL_STAGES=5"; s_failed=1; }
    grep -q '^finale()' "$script"      || { missing+=" finale"; s_failed=1; }
    if [ "$s_failed" -eq 0 ]; then
        printf '  ✓ structural         5 stage_intro, 5 stage_gate, 5 run_stage, main, finale, TOTAL_STAGES=5\n'
    else
        printf '  ✗ structural         missing:%s\n' "$missing" >&2
        failed=1
    fi

    # 4. error-path behaviour
    local rc6 rcbad
    "$invoke_path" 6 >/dev/null 2>&1 && rc6=0 || rc6=$?
    "$invoke_path" xyzzy >/dev/null 2>&1 && rcbad=0 || rcbad=$?
    if [ "$rc6" -ne 0 ] && [ "$rcbad" -ne 0 ]; then
        printf '  ✓ error path         out-of-range and bogus argv both rejected\n'
    else
        printf '  ✗ error path         rc6=%s rcbad=%s (both should be non-zero)\n' "$rc6" "$rcbad" >&2
        failed=1
    fi

    return "$failed"
}

# ---------------------------------------------------------------------
# Self-test: smoke vs a clean copy and a tampered copy
# ---------------------------------------------------------------------

self_test() {
    local source="${1:-shelltutor}"
    if [ ! -f "$source" ]; then
        printf 'self-test: cannot find source script %s\n' "$source" >&2
        return 2
    fi

    local tmp_clean tmp_broken
    tmp_clean="$(mktemp -t smoke-clean.XXXXXX)"
    tmp_broken="$(mktemp -t smoke-broken.XXXXXX)"
    # shellcheck disable=SC2064  # expand at trap-set time to survive set -u after locals exit
    trap "rm -f '$tmp_clean' '$tmp_broken'" EXIT

    cp "$source" "$tmp_clean"
    chmod +x "$tmp_clean"

    # Make the broken copy by removing the stage5_gate function body. Use
    # sed to delete the block from `^stage5_gate() {` through the matching
    # closing `^}` line. Simple removal: blank out the line that defines
    # the function name; the smoke check looks for `^stage5_gate()` so a
    # rename suffices to demonstrate failure.
    sed 's/^stage5_gate()/stage5_GONE()/' "$source" > "$tmp_broken"
    chmod +x "$tmp_broken"

    printf 'self-test: smoke vs clean copy should pass        ...\n'
    if smoke_run "$tmp_clean" >/dev/null 2>&1; then
        printf 'self-test:   PASS\n'
    else
        printf 'self-test:   FAIL (smoke rejected a clean copy)\n' >&2
        return 1
    fi

    printf 'self-test: smoke vs tampered copy should fail     ...\n'
    if ! smoke_run "$tmp_broken" >/dev/null 2>&1; then
        printf 'self-test:   PASS (smoke flagged missing stage5_gate)\n'
    else
        printf 'self-test:   FAIL (smoke missed the tampered copy)\n' >&2
        return 1
    fi

    printf 'self-test: all cases pass.\n'
}

# ---------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------

main() {
    if [ "${1:-}" = "--self-test" ]; then
        self_test "${2:-shelltutor}"
        return $?
    fi

    local script="${1:-shelltutor}"
    printf 'smoke: %s\n' "$script"
    if smoke_run "$script"; then
        printf 'smoke: all checks pass\n'
        return 0
    else
        printf 'smoke: one or more checks failed\n' >&2
        return 1
    fi
}

main "$@"
