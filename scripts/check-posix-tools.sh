#!/usr/bin/env bash
# check-posix-tools.sh — operationalize proposed fitness function FF-008
# (audit/2026-11-07/findings.md) against shelltutor.
#
# FF-008 (POSIX text-tool portability in script code):
#   Bash code in the tutor, outside lesson heredocs, must not use
#   GNU-only text-tool syntax that BSD/macOS userland lacks:
#     sed       \+ \? \|  (repetition / alternation)
#     sed       \L \U \l \u  (case conversion)
#     sed       \s \w \d  (character-class shorthands)
#     sed -i    (in-place edit; BSD requires a backup-suffix argument)
#     grep -P   (PCRE)
#     readlink -f
#     date -d / --date
#     stat -c
#   Use POSIX forms instead: tr -s, awk, [[:space:]], a temp file plus
#   mv, cd/pwd -P, and so on (F-008 2026-05-23, F-012 2026-11-07).
#
# The sed rules apply only to lines that contain the word `sed`, so a
# printf format such as '\l' or '\d' elsewhere is not flagged.
#
# Heredoc detection mirrors check-safety.sh — same awk state machine.
# Lines inside heredoc bodies are lesson copy and exempt; comment lines
# are skipped; a line containing "# nofitness:" (for example
# "# nofitness:posix") is exempted.
#
# Usage:
#   ./scripts/check-posix-tools.sh                  # check ./shelltutor
#   ./scripts/check-posix-tools.sh path/to/script   # check a specific path
#   ./scripts/check-posix-tools.sh --self-test      # run built-in fixtures
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

        {
            has_sed = match($0, /(^|[^A-Za-z0-9_])sed([^A-Za-z0-9_]|$)/)

            if (has_sed && match($0, /\\[+?|]/)) {
                printf "%s:%d: FF-008 GNU sed repetition/alternation: %s\n", FILENAME, NR, $0
                violations++
            }
            if (has_sed && match($0, /\\[LUlu]/)) {
                printf "%s:%d: FF-008 GNU sed case conversion: %s\n", FILENAME, NR, $0
                violations++
            }
            if (has_sed && match($0, /\\[swd]/)) {
                printf "%s:%d: FF-008 GNU sed character class: %s\n", FILENAME, NR, $0
                violations++
            }
            if (match($0, /(^|[^A-Za-z0-9_-])sed[[:space:]]+(-[A-Za-z]*)?-i([[:space:]]|$)/)) {
                printf "%s:%d: FF-008 sed -i: %s\n", FILENAME, NR, $0
                violations++
            }
            if (match($0, /(^|[^A-Za-z0-9_-])grep[[:space:]]+(-[A-Za-z]*)?P([[:space:]]|$)/)) {
                printf "%s:%d: FF-008 grep -P: %s\n", FILENAME, NR, $0
                violations++
            }
            if (match($0, /readlink[[:space:]]+-f/)) {
                printf "%s:%d: FF-008 readlink -f: %s\n", FILENAME, NR, $0
                violations++
            }
            if (match($0, /(^|[^A-Za-z0-9_-])date[[:space:]]+(-d|--date)/)) {
                printf "%s:%d: FF-008 date -d: %s\n", FILENAME, NR, $0
                violations++
            }
            if (match($0, /(^|[^A-Za-z0-9_-])stat[[:space:]]+-c/)) {
                printf "%s:%d: FF-008 stat -c: %s\n", FILENAME, NR, $0
                violations++
            }
        }

        END {
            exit (violations > 0 ? 1 : 0)
        }
    ' "$@"
}

self_test() {
    local tmp tmp_out rule line
    tmp="$(mktemp -t check-posix-tools.XXXXXX)"
    tmp_out="$(mktemp -t check-posix-tools-out.XXXXXX)"
    # shellcheck disable=SC2064  # expand at trap-set time
    trap "rm -f '$tmp' '$tmp_out'" EXIT

    # Known-good: POSIX text tools; GNU syntax only inside a heredoc body
    # (lesson copy) and in a comment.
    cat > "$tmp" <<'PASS'
#!/usr/bin/env bash
# sed -i and grep -P are mentioned in this comment only.
x=$(printf '%s' "$1" | tr -s '[:space:]' ' ' | sed 's/^[[:space:]]*//')
y=$(printf '%s\n' "$x" | awk '{print toupper(substr($0,1,1))}')
cat <<EOF
Lesson copy may mention: sed -i 's/a/b/' file, grep -P, readlink -f
EOF
PASS
    printf 'self-test: POSIX tools and heredoc copy should pass   ... '
    if awk_check "$tmp" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker rejected a clean fixture)\n' >&2
        return 1
    fi

    # Known-bad: one line per rule; each must be reported under its label.
    while IFS='|' read -r rule line; do
        printf '#!/usr/bin/env bash\n%s\n' "$line" > "$tmp"
        printf 'self-test: %-31s should be flagged ... ' "$rule"
        if awk_check "$tmp" > "$tmp_out"; then
            printf 'FAIL (checker missed %s)\n' "$rule" >&2
            return 1
        fi
        if ! grep -q "FF-008 $rule:" "$tmp_out"; then
            printf 'FAIL (flagged under the wrong label)\n' >&2
            return 1
        fi
        printf 'PASS\n'
    done <<'RULES'
GNU sed repetition/alternation|x=$(sed 's/a\+/b/' file)
GNU sed case conversion|x=$(sed 's/.*/\L&/' file)
GNU sed character class|x=$(sed 's/\s*$//' file)
sed -i|sed -i 's/a/b/' file
grep -P|grep -P 'a\d' file
readlink -f|p=$(readlink -f "$0")
date -d|d=$(date -d yesterday +%F)
stat -c|n=$(stat -c %s file)
RULES

    # A printf format with \l on a line that has no sed must not trip the
    # sed-scoped rules.
    cat > "$tmp" <<'PASS'
#!/usr/bin/env bash
printf '%s\l\n' x
PASS
    printf 'self-test: \\l outside a sed line should pass          ... '
    if awk_check "$tmp" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (sed-scoped rule fired on a non-sed line)\n' >&2
        return 1
    fi

    # Annotated exemption.
    cat > "$tmp" <<'PASS'
#!/usr/bin/env bash
sed -i 's/a/b/' file   # nofitness:posix
PASS
    printf 'self-test: # nofitness:posix line should pass         ... '
    if awk_check "$tmp" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (annotation was not honoured)\n' >&2
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
        printf 'check-posix-tools: error: not a file: %s\n' "$script" >&2
        return 2
    fi

    if awk_check "$script"; then
        printf 'check-posix-tools: clean (%s)\n' "$script"
        return 0
    else
        printf 'check-posix-tools: violations in %s\n' "$script" >&2
        return 1
    fi
}

main "$@"
