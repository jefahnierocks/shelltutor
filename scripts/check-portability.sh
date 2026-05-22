#!/usr/bin/env bash
# check-portability.sh — operationalize audit FF-004 against shelltutor lessons.
#
# FF-004 (lesson portability check) per audit/2026-05-21/10-fitness-functions.md:
#   Every lesson heredoc line that references a platform-specific
#   surface must either (a) demonstrate the gate-and-fallback pattern
#   per CONTRIBUTING.md:51-54, or (b) be a clearly-framed install hint
#   that names the platform context.
#
# Scope decision (this implementation):
#   Forbidden in lesson heredocs:
#     /proc/      Linux-only filesystem (audit lesson 7 closure)
#     /sys/       Linux-only filesystem
#     free -      Linux-only command (with a flag, to disambiguate
#                 from the English word "free" in lesson copy)
#     vm_stat     macOS-only command
#     systemctl   Linux systemd
#     launchctl   macOS launchd
#   Allowed:
#     brew install / dnf install / apt install / apt-get install /
#     yum install / pacman -S / port install
#     — these are install hints by nature; appear legitimately in
#     finale's "how to install vimtutor" enumeration. A lesson that
#     teaches platform-specific install IS platform-specific by
#     design; that's an operator choice, not a regression-prevention
#     concern.
#
# Heredoc detection mirrors check-safety.sh — same awk state machine.
# This script scans INSIDE heredoc bodies (the opposite of check-safety
# which scans OUTSIDE). A `# nofitness:portability` line annotation
# exempts a line; in heredocs, this is included as visible UI text so
# it should be used sparingly.
#
# Usage:
#   ./scripts/check-portability.sh                  # check ./shelltutor
#   ./scripts/check-portability.sh path/to/script   # check a specific path
#   ./scripts/check-portability.sh --self-test      # built-in fixtures
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

        # Heredoc opener — only recognized when NOT already in a heredoc.
        !in_h {
            if (match($0, /<<-?'\''?[A-Za-z_][A-Za-z0-9_]*'\''?/)) {
                m = substr($0, RSTART, RLENGTH)
                sub(/^<<-?'\''?/, "", m)
                sub(/'\''?$/, "", m)
                in_h = 1
                marker = m
                next
            }
            next            # outside heredoc: not our concern (check-safety covers code)
        }

        # Inside heredoc body. Check for non-portable surfaces.
        {
            # Allow-list pattern: install commands are platform-by-nature
            # and not regression-prevention targets here.
            if (match($0, /(brew install|dnf install|apt install|apt-get install|yum install|pacman -S|port install)/)) {
                next
            }

            # Allow-list pattern: explicit per-line exemption.
            if (match($0, /nofitness:portability/)) {
                next
            }

            # Forbidden platform-specific surfaces.
            if (match($0, /\/proc\/|\/sys\//)) {
                printf "%s:%d: FF-004 platform-only path: %s\n", FILENAME, NR, $0
                violations++
                next
            }
            if (match($0, /[[:space:]]free[[:space:]]+-[a-zA-Z]/) || match($0, /^free[[:space:]]+-/)) {
                printf "%s:%d: FF-004 Linux-only command (free): %s\n", FILENAME, NR, $0
                violations++
                next
            }
            if (match($0, /[^a-zA-Z_]vm_stat[^a-zA-Z_]/) || match($0, /^vm_stat/) || match($0, /vm_stat$/)) {
                printf "%s:%d: FF-004 macOS-only command (vm_stat): %s\n", FILENAME, NR, $0
                violations++
                next
            }
            if (match($0, /[^a-zA-Z_]systemctl[^a-zA-Z_]/) || match($0, /^systemctl/) || match($0, /systemctl$/)) {
                printf "%s:%d: FF-004 Linux-only command (systemctl): %s\n", FILENAME, NR, $0
                violations++
                next
            }
            if (match($0, /[^a-zA-Z_]launchctl[^a-zA-Z_]/) || match($0, /^launchctl/) || match($0, /launchctl$/)) {
                printf "%s:%d: FF-004 macOS-only command (launchctl): %s\n", FILENAME, NR, $0
                violations++
                next
            }
        }

        END {
            exit (violations > 0 ? 1 : 0)
        }
    ' "$@"
}

self_test() {
    local tmp_pass tmp_proc tmp_free tmp_install
    tmp_pass="$(mktemp -t check-portability-pass.XXXXXX)"
    tmp_proc="$(mktemp -t check-portability-proc.XXXXXX)"
    tmp_free="$(mktemp -t check-portability-free.XXXXXX)"
    tmp_install="$(mktemp -t check-portability-install.XXXXXX)"
    # shellcheck disable=SC2064  # expand at trap-set time
    trap "rm -f '$tmp_pass' '$tmp_proc' '$tmp_free' '$tmp_install'" EXIT

    # Known-good: portable lesson copy + install hints in heredoc
    cat > "$tmp_pass" <<'PASS'
#!/usr/bin/env bash
cat <<EOF
Stage 1 — Where am I?
Run pwd, whoami, date. Output goes to the terminal.
EOF
cat <<EOF
On macOS: brew install vim
On Linux (Fedora): sudo dnf install vim-enhanced
On Linux (Debian/Ubuntu): sudo apt install vim
EOF
PASS

    # Known-bad: lesson teaches /proc inside a heredoc
    cat > "$tmp_proc" <<'FAIL'
#!/usr/bin/env bash
cat <<EOF
Try: cat /proc/cpuinfo
EOF
FAIL

    # Known-bad: lesson teaches free -h inside a heredoc
    cat > "$tmp_free" <<'FAIL'
#!/usr/bin/env bash
cat <<EOF
Memory info: free -h
EOF
FAIL

    # Allowed: bare "free" in narration (e.g., "things are free here").
    cat > "$tmp_install" <<'PASS'
#!/usr/bin/env bash
cat <<EOF
The terminal is free to use. Type commands; the shell runs them.
EOF
PASS

    printf 'self-test: portable heredocs should pass            ... '
    if awk_check "$tmp_pass" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker rejected a clean fixture)\n' >&2
        return 1
    fi

    printf 'self-test: /proc/ in heredoc should be flagged      ... '
    if ! awk_check "$tmp_proc" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker missed /proc/)\n' >&2
        return 1
    fi

    printf 'self-test: "free -h" in heredoc should be flagged   ... '
    if ! awk_check "$tmp_free" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker missed free -h)\n' >&2
        return 1
    fi

    printf 'self-test: bare "free" in narration should pass     ... '
    if awk_check "$tmp_install" >/dev/null; then
        printf 'PASS\n'
    else
        printf 'FAIL (checker flagged a benign English word)\n' >&2
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
        printf 'check-portability: error: not a file: %s\n' "$script" >&2
        return 2
    fi

    if awk_check "$script"; then
        printf 'check-portability: clean (%s)\n' "$script"
        return 0
    else
        printf 'check-portability: violations in %s\n' "$script" >&2
        return 1
    fi
}

main "$@"
