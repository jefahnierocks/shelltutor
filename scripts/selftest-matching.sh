#!/usr/bin/env bash
# selftest-matching.sh — FF-011: the recall matcher corpus.
#
# Sources the real `normalize_answer`, `recall_matches` and RECALL_NEGATIONS
# from ./shelltutor, reads every `ask_question` call (exact forms and keyword
# groups) from the same file, and checks each line of the corpus
# (scripts/matching-corpus.tsv):
#   accept  a correct answer from the rejected-answer tables of rounds 1-4
#           (audit/2026-11-09/walkthroughs.md) must be taken;
#   reject  a distractor from a question's own option text, or a negation
#           counterexample (F-019, `only appends`), must be refused.
# The questions are keyed by their order in the script (21 today); a new
# recall question without corpus lines, or a changed count, fails the check.
#
# Usage:
#   ./scripts/selftest-matching.sh [path/to/shelltutor [corpus.tsv]]
#
# Exit codes: 0 all pass; 1 a case failed; 2 usage or structure error.

set -eu

SCRIPT=${1:-shelltutor}
CORPUS=${2:-"$(dirname "$0")/matching-corpus.tsv"}
EXPECTED_CALLS=21

# Question keys, in the order the calls appear in the script.
KEYS="S1Q1 S1Q2 S1Q3 S2Q1 S2Q2 S2Q3 S3Q1 S3Q2 S3Q3 S4Q1 S4Q2 S4Q3 S5Q1 S5Q2 S5Q3 SHQ1 SHQ2 SHQ3 ENQ1 ENQ2 ENQ3"

[ -f "$SCRIPT" ] || { printf 'selftest-matching: not a file: %s\n' "$SCRIPT" >&2; exit 2; }
[ -f "$CORPUS" ] || { printf 'selftest-matching: not a file: %s\n' "$CORPUS" >&2; exit 2; }

tmp=$(mktemp -d "${TMPDIR:-/tmp}/selftest-matching.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

# The real functions, not copies.
funcs=$(sed -n '/^normalize_lines()/,/^}/p; /^normalize_answer()/,/^}/p; /^RECALL_NEGATIONS=/p; /^recall_matches()/,/^}/p' "$SCRIPT")
[ -n "$funcs" ] || { printf 'selftest-matching: matcher not found in %s\n' "$SCRIPT" >&2; exit 2; }
eval "$funcs"

# One record per argument: call-number <TAB> kind <TAB> value. kind is
# prompt, hint, exact or group. Values are unquoted (single or double quotes;
# \$ and \" unescaped), one argument per source line as FF-009 requires.
awk '
    function unq(line) {
        sub(/^[[:space:]]+/, "", line); sub(/[[:space:]]*\\$/, "", line)
        sub(/[[:space:]]*\|\|[[:space:]]*return.*$/, "", line); sub(/[[:space:]]+$/, "", line)
        if (line ~ /^\047[^\047]*\047$/) return substr(line, 2, length(line) - 2)
        if (line ~ /^"([^"\\]|\\.)*"$/) {
            line = substr(line, 2, length(line) - 2)
            gsub(/\\"/, "\"", line); gsub(/\\\$/, "$", line)
            return line
        }
        return ""
    }
    /^[[:space:]]*#/ { next }
    collecting {
        bare = $0; sub(/^[[:space:]]+/, "", bare); sub(/[[:space:]]*\\$/, "", bare)
        if (bare == "--") { kind = "group"; if ($0 !~ /\\[[:space:]]*$/) collecting = 0; next }
        if (bare == "--ordered") { printf "%d\tflag\tordered\n", call; next }
        if (bare == "--reject") { kind = "reject"; next }
        n++
        k = (n == 1) ? "prompt" : (n == 2) ? "hint" : kind
        printf "%d\t%s\t%s\n", call, k, unq($0)
        if ($0 !~ /\\[[:space:]]*$/) collecting = 0
        next
    }
    /^[[:space:]]*ask_question[[:space:]]+\\[[:space:]]*$/ { collecting = 1; call++; n = 0; kind = "exact" }
' "$SCRIPT" > "$tmp/calls.tsv"

calls=$(cut -f1 "$tmp/calls.tsv" | sort -un | wc -l | tr -d '[:space:]')
if [ "$calls" != "$EXPECTED_CALLS" ]; then
    printf 'selftest-matching: found %s ask_question calls, expected %s: add the new question to KEYS and the corpus\n' \
        "$calls" "$EXPECTED_CALLS" >&2
    exit 2
fi

key_index() {
    local i=0 k
    for k in $KEYS; do
        i=$((i + 1))
        [ "$k" = "$1" ] && { printf '%s' "$i"; return 0; }
    done
    return 1
}

pass=0 fail=0 accepted=0 rejected=0
TAB=$(printf '\t')
while IFS="$TAB" read -r key verdict input source; do
    case "$key" in ''|'#'*) continue ;; esac
    idx=$(key_index "$key") || { printf 'selftest-matching: unknown question key %s\n' "$key" >&2; exit 2; }
    args=(); groups=(); flags=(); reject=""
    while IFS="$TAB" read -r _ kind value; do
        case "$kind" in
            exact) args+=("$value") ;;
            group) groups+=("$value") ;;
            flag) flags+=("--$value") ;;
            reject) reject=$value ;;
        esac
    done <<REC
$(awk -F'\t' -v c="$idx" '$1 == c' "$tmp/calls.tsv")
REC
    if [ "${#groups[@]}" -gt 0 ]; then
        args+=("--")
        [ "${#flags[@]}" -eq 0 ] || args+=("${flags[@]}")
        args+=("${groups[@]}")
        [ -z "$reject" ] || args+=("--reject" "$reject")
    fi
    norm=$(normalize_answer "$input")
    if recall_matches "$norm" "${args[@]}"; then got=accept; else got=reject; fi
    if [ "$got" = "$verdict" ]; then
        pass=$((pass + 1))
    else
        fail=$((fail + 1))
        printf 'selftest-matching: FAIL %s %-6s expected %s, got %s  [%s] (%s)\n' \
            "$key" "$input" "$verdict" "$got" "$norm" "$source" >&2
    fi
    if [ "$verdict" = accept ]; then accepted=$((accepted + 1)); else rejected=$((rejected + 1)); fi
done < "$CORPUS"

if [ "$fail" -gt 0 ]; then
    printf 'selftest-matching: %d of %d cases failed\n' "$fail" "$((pass + fail))" >&2
    exit 1
fi
printf 'selftest-matching: %d cases pass (%d accepted, %d rejected) over %d questions\n' \
    "$pass" "$accepted" "$rejected" "$calls"
