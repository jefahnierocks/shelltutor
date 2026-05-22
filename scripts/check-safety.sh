#!/usr/bin/env bash
# check-safety.sh — operationalize audit FF-001 + FF-002 against shelltutor.
#
# FF-001 (safety-rule static analysis) per audit/2026-05-21/10-fitness-functions.md:
#   The tracked shelltutor script must not invoke sudo / setuid /
#   chmod +s / curl / wget / nc / ssh, and must not contain http(s)://
#   URLs, when the offending token is in the bash code itself. The same
#   tokens *are allowed inside lesson heredocs* — the lesson copy that
#   *teaches the learner about* sudo (e.g. the finale's vimtutor install
#   hint).
#
# FF-002 (write-scope static analysis):
#   Every filesystem write operation in the bash code must target a path
#   under $SANDBOX or $PROGRESS_FILE. Writes to /tmp, /var, /etc, /root,
#   /usr, /home are forbidden. Heuristic: scan write-command lines
#   outside heredocs for forbidden absolute prefixes. A semantic check
#   ("does this redirect target evaluate to a path under $SANDBOX?")
#   would require a bash AST; the prefix-blocklist catches every obvious
#   class of violation without that complexity.
#
# Heredoc detection is a small awk state machine: <<MARKER opens a body
# and the next line that exactly equals MARKER closes it. Both quoted
# (<<'EOF') and unquoted (<<EOF) forms are recognised; <<- (tab-strip)
# is recognised at the opener.
#
# Annotations: a line containing "# nofitness:" is exempted from checks.
#
# Usage:
#   ./scripts/check-safety.sh                  # check ./shelltutor
#   ./scripts/check-safety.sh path/to/script   # check a specific path
#   ./scripts/check-safety.sh --self-test      # run built-in fixtures
#
# Exit codes:
#   0  clean
#   1  violations found
#   2  usage error

set -eu

awk_check() {
    awk '
        BEGIN {
            in_h = 0
            marker = ""
            violations = 0
        }

        # Heredoc terminator: line is exactly the marker (column 0).
        in_h && $0 == marker {
            in_h = 0
            marker = ""
            next
        }

        # Lines inside a heredoc body are exempt.
        in_h { next }

        # Heredoc opener: <<MARKER / <<-MARKER / <<'\''MARKER'\'' / <<-'\''MARKER'\''.
        {
            if (match($0, /<<-?'\''?[A-Za-z_][A-Za-z0-9_]*'\''?/)) {
                m = substr($0, RSTART, RLENGTH)
                sub(/^<<-?'\''?/, "", m)
                sub(/'\''?$/, "", m)
                in_h = 1
                marker = m
                next
            }
        }

        # Pure-comment lines: skip.
        /^[[:space:]]*#/ { next }

        # Annotated exempt lines: skip.
        /# nofitness:/ { next }

        # FF-001: forbidden runtime commands or URLs.
        {
            if (match($0, /(^|[[:space:]]|;|&&|\|\|)(sudo|curl|wget|nc|ssh)[[:space:]]/) \
                || match($0, /chmod[[:space:]]+\+s/) \
                || match($0, /setuid/) \
                || match($0, /https?:\/\//)) {
                printf "%s:%d: FF-001 safety-rule: %s\n", FILENAME, NR, $0
                violations++
            }

            # FF-002: write to a forbidden absolute prefix.
            if (match($0, /(>|>>|tee|mkdir|touch|cp|mv|rm)[[:space:]]/) \
                && match($0, /[[:space:]]("|'\''?)?(\/tmp\/|\/var\/|\/etc\/|\/root\/|\/usr\/|\/home\/)/)) {
                printf "%s:%d: FF-002 write-scope: %s\n", FILENAME, NR, $0
                violations++
            }
        }

        END {
            exit (violations > 0 ? 1 : 0)
        }
    ' "$@"
}

self_test() {
    local tmp_pass tmp_ff1 tmp_ff2
    tmp_pass="$(mktemp -t check-safety-pass.XXXXXX)"
    tmp_ff1="$(mktemp -t check-safety-ff1.XXXXXX)"
    tmp_ff2="$(mktemp -t check-safety-ff2.XXXXXX)"
    # Use parameter-default expansion so the trap survives `set -u` even
    # after these locals have gone out of scope at script exit.
    # shellcheck disable=SC2064  # expand $tmp_* at trap-set time so the paths are captured
    trap "rm -f '$tmp_pass' '$tmp_ff1' '$tmp_ff2'" EXIT

    # Known-good fixture: writes only under $SANDBOX; heredoc body
    # mentions sudo/dnf legitimately (lesson copy).
    cat > "$tmp_pass" <<'PASS'
#!/usr/bin/env bash
SANDBOX="$HOME/.shelltutor"
mkdir -p "$SANDBOX"
echo hello > "$SANDBOX/file.txt"
cat <<EOF
Inside a heredoc body these are not violations:
  sudo dnf install something
  curl https://example.com
  write to /tmp/scratch
EOF
PASS

    # Known-bad FF-001: invokes sudo in real bash code.
    cat > "$tmp_ff1" <<'FAIL'
#!/usr/bin/env bash
sudo dnf install something
FAIL

    # Known-bad FF-002: writes to /tmp.
    cat > "$tmp_ff2" <<'FAIL'
#!/usr/bin/env bash
echo data > /tmp/leaks.txt
FAIL

    printf 'self-test: known-good fixture should pass        ... '
    if awk_check "$tmp_pass" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker rejected the clean fixture)\n' >&2
        return 1
    fi

    printf 'self-test: known-bad FF-001 should be flagged    ... '
    if ! awk_check "$tmp_ff1" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker missed an FF-001 violation)\n' >&2
        return 1
    fi

    printf 'self-test: known-bad FF-002 should be flagged    ... '
    if ! awk_check "$tmp_ff2" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker missed an FF-002 violation)\n' >&2
        return 1
    fi

    printf 'self-test: all cases pass.\n'
}

main() {
    if [ "${1:-}" = "--self-test" ]; then
        self_test
        return $?
    fi

    local script="${1:-shelltutor}"
    if [ ! -f "$script" ]; then
        printf 'check-safety: error: not a file: %s\n' "$script" >&2
        return 2
    fi

    if awk_check "$script"; then
        printf 'check-safety: clean (%s)\n' "$script"
        return 0
    else
        printf 'check-safety: violations in %s\n' "$script" >&2
        return 1
    fi
}

main "$@"
