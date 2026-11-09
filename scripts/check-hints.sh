#!/usr/bin/env bash
# check-hints.sh — FF-009 and FF-010: recall hints never contain an accepted
# answer, and every hint is anchored to the lesson that taught the fact.
#
# Every `ask_question` call in shelltutor has the shape
#
#   ask_question \
#       "<prompt>" \
#       "<hint>" \
#       '<accepted 1>' \
#       '<accepted 2>' || return $?
#
# one quoted argument per line. This checker enforces, for each call:
#   - layout: `ask_question` ends its line with a backslash and every
#     argument sits alone on its own line (one quoted word, nothing else);
#   - arity: one prompt, one hint and at least one accepted form;
#   - leak: no accepted form appears inside the hint, case-insensitive
#     (colour-variable references such as ${CMD} are ignored);
#   - reserved words: `show`, `quit` and `exit` are never accepted forms;
#   - anchor (FF-010): the hint starts `Lesson N: ` or `Lesson N.k: `
#     (colour variables ignored): it says where the fact was taught and
#     names the concept, and never paraphrases the answer.
#
# Usage:
#   ./scripts/check-hints.sh                  # check ./shelltutor
#   ./scripts/check-hints.sh path/to/script   # check a specific path
#   ./scripts/check-hints.sh --self-test      # built-in fixtures
#
# Exit codes:
#   0  clean
#   1  violations found
#   2  usage error

set -eu

awk_check() {
    awk '
        function fail(msg) {
            printf "%s:%d: %s\n", FILENAME, call_line, msg
            violations++
        }

        # Strip the quotes of one argument line; sets ok=0 if the line is
        # not exactly one quoted word. Result in `val`.
        function unquote(line,    n) {
            sub(/^[[:space:]]+/, "", line)
            sub(/[[:space:]]*\\$/, "", line)
            sub(/[[:space:]]*\|\|[[:space:]]*return.*$/, "", line)
            sub(/[[:space:]]+$/, "", line)
            ok = 1
            if (line ~ /^\047[^\047]*\047$/) {
                val = substr(line, 2, length(line) - 2)
            } else if (line ~ /^"([^"\\]|\\.)*"$/) {
                val = substr(line, 2, length(line) - 2)
                gsub(/\\"/, "\"", val)
                gsub(/\\\$/, "$", val)
            } else {
                ok = 0
                val = line
            }
            return val
        }

        function finish(    i, h, a, norm) {
            if (!collecting) return
            collecting = 0
            if (nargs < 3) {
                fail("FF-009 call has " nargs " argument(s); need a prompt, a hint and at least one accepted form")
                return
            }
            h = tolower(args[2])
            gsub(/\$\{[A-Za-z_]+\}/, "", h)
            if (args[2] !~ /^(\$\{[A-Za-z_]+\})*Lesson [0-9]+(\.[0-9]+)?: /)
                fail("FF-010 hint is not anchored (start with \"Lesson N: \" or \"Lesson N.k: \"): " args[2])
            for (i = 3; i <= nargs; i++) {
                a = tolower(args[i])
                gsub(/\$\{[A-Za-z_]+\}/, "", a)
                norm = a
                gsub(/[[:space:]]+/, " ", norm)
                sub(/^ /, "", norm); sub(/ $/, "", norm)
                if (norm == "show" || norm == "quit" || norm == "exit")
                    fail("FF-009 reserved word accepted as an answer: " args[i])
                if (a != "" && index(h, a) > 0)
                    fail("FF-009 hint contains accepted answer \"" args[i] "\": " args[2])
            }
        }

        BEGIN { collecting = 0; violations = 0 }

        # Comment lines never open a call.
        /^[[:space:]]*#/ { next }

        collecting {
            line = $0
            unquote(line)
            if (!ok) {
                fail("FF-009 argument is not a single quoted word on its own line: " val)
            } else {
                args[++nargs] = val
            }
            if (line !~ /\\[[:space:]]*$/) finish()
            next
        }

        /^[[:space:]]*ask_question[[:space:]]*\(\)/ { next }

        /^[[:space:]]*ask_question[[:space:]]+\\[[:space:]]*$/ {
            collecting = 1; nargs = 0; call_line = NR
            next
        }

        /^[[:space:]]*ask_question([[:space:]]|$)/ {
            call_line = NR
            fail("FF-009 arguments must start on the next line, one per line: " $0)
            next
        }

        END {
            if (collecting) { call_line = NR; fail("FF-009 unterminated ask_question call") }
            exit (violations > 0 ? 1 : 0)
        }
    ' "$@"
}

self_test() {
    local dir
    dir="$(mktemp -d "${TMPDIR:-/tmp}/check-hints.XXXXXX")"
    # shellcheck disable=SC2064  # expand at trap-set time
    trap "rm -rf '$dir'" EXIT

    cat > "$dir/clean" <<'FIX'
ask_question \
    "Q1: What does ${CMD}pwd${RST} print?" \
    "Lesson 2.1: where you are standing, not who you are." \
    'working directory' \
    'the current folder' || return $?
FIX
    cat > "$dir/leak" <<'FIX'
ask_question \
    "Q1: Which command creates an empty file?" \
    "Lesson 3.1: it is the one that can touch a file." \
    'touch' || return $?
FIX
    cat > "$dir/letter" <<'FIX'
ask_question \
    "Q1: How do you exit man?" \
    "Lesson 3.2: the same single key quits less." \
    'q' \
    'press q' || return $?
FIX
    cat > "$dir/oneline" <<'FIX'
ask_question "Q1: Pick one" "Lesson 1: a hint." 'x' || return $?
FIX
    cat > "$dir/reserved" <<'FIX'
ask_question \
    "Q1: Pick one" \
    "Lesson 1: a hint." \
    'Show' || return $?
FIX
    cat > "$dir/noaccept" <<'FIX'
ask_question \
    "Q1: Pick one" \
    "Lesson 1: a hint." || return $?
FIX
    cat > "$dir/unanchored" <<'FIX'
ask_question \
    "Q1: Pick one" \
    "Think of where you are standing." \
    'x' || return $?
FIX
    cat > "$dir/nocolon" <<'FIX'
ask_question \
    "Q1: Pick one" \
    "Lesson 1.3 compared two prompts." \
    'x' || return $?
FIX
    cat > "$dir/colour" <<'FIX'
ask_question \
    "Q1: Pick one" \
    "${SUB}Lesson 1.3: two prompts.${RST}" \
    'x' || return $?
FIX

    local name want
    for name in clean:0 leak:1 letter:1 oneline:1 reserved:1 noaccept:1 unanchored:1 nocolon:1 colour:0; do
        want="${name##*:}"; name="${name%%:*}"
        printf 'self-test: %-9s should %-4s ... ' "$name" "$([ "$want" = 0 ] && echo pass || echo fail)"
        if awk_check "$dir/$name" >/dev/null 2>&1; then got=0; else got=1; fi
        if [ "$got" = "$want" ]; then
            printf 'PASS\n'
        else
            printf 'FAIL\n' >&2
            return 1
        fi
    done
    printf 'self-test: all cases pass.\n'
}

main() {
    if [ "${1:-}" = "--self-test" ]; then
        self_test
        return $?
    fi
    local script="${1:-shelltutor}"
    if [ ! -f "$script" ]; then
        printf 'check-hints: error: not a file: %s\n' "$script" >&2
        return 2
    fi
    if awk_check "$script"; then
        printf 'check-hints: clean (%s)\n' "$script"
        return 0
    fi
    printf 'check-hints: violations in %s\n' "$script" >&2
    return 1
}

main "$@"
