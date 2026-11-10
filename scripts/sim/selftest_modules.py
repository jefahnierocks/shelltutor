#!/usr/bin/env python3
"""scripts/sim/selftest_modules.py — self-test for module persona tables.

Usage:

    python3 scripts/sim/selftest_modules.py

No module exists yet, so this proves the machinery without one:

1. `persona.module_walk()` expands a table into the expected walk, using
   the module heading convention (no per-module sentinels), including the
   task heading.
2. An empty gate spec expands without error, and the optional
   `lesson_actions` and `prompt_after` keys expand as documented.
3. A fake tutor that follows the heading convention is driven end to end
   through `run.py --module` with a table injected for the test: green
   TAP, the cleared line counts as the gate pass, `.progress` stays absent
   and `screen-height` events carry the 20-line rendered budget. This part
   needs a pseudo-terminal; without one it is skipped with a message.

Python 3.9 stdlib only. Nothing is written outside a temporary directory.

Exit codes: 0 — all checks passed (the PTY part may be skipped); 1 — a
check failed.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(os.path.dirname(_HERE))
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from scripts.sim import persona as P  # noqa: E402
from scripts.sim import run as R  # noqa: E402

TABLE = {"lessons": 2, "gate": {"recall": ["a", "b", "c"], "task": ["echo hi"]}}
# Optional keys: a command typed at lesson 2's prompt, and the prompt text
# the fake tutor shows after lesson 1's `next`.
DRIVE_TABLE = dict(TABLE, lesson_actions={2: ["echo x"]}, prompt_after={1: "p2> "})

FAKE_TUTOR = r"""#!/usr/bin/env bash
# Fake module tutor following the heading convention (test fixture only).
name="$1"
clr() { printf '\033[3J\033[H\033[2J'; }
prompt_until() { local want="$1" line; while :; do read -r -p "shelltutor> " line || exit 1; [ "$line" = "$want" ] && return; done; }
clr; printf 'MODULE — %s: A demo\n\nintro line\n\n' "$name"; prompt_until next
clr; printf '%s 1 — Lesson title\n\nbody\n\n' "$name"; prompt_until next
clr; printf '%s 2 — Lesson title\n\nbody\n\n' "$name"
read -r -p "p2> " line || exit 1   # changed prompt for the first command only
prompt_until next
clr; printf '%s — gate\n\n' "$name"
for i in 1 2 3; do read -r -p "Q$i: question? " ans || exit 1; done
clr; printf '%s — task\n\nTask: run echo hi then check\n\n' "$name"
while :; do read -r -p "shelltutor> " line || exit 1; case "$line" in check) break;; esac; done
clr; printf '✓ %s cleared.\n\nrecap\n\n▶ Type quit to leave.\n\n' "$name"; prompt_until quit
exit 0
"""


def _fail(msg):
    print("FAIL: %s" % msg)
    return 1


def check_expansion() -> int:
    walk = P.module_walk("demo", TABLE["lessons"], TABLE["gate"])
    got = [(a.wait_for, a.send, a.screen_id) for a in walk]
    want = [
        ("MODULE — demo:", "", "M-I"),
        (P.PROMPT, "next", "M-I"),
        ("demo 1 — ", "", "M-L1"),
        (P.PROMPT, "next", "M-L1"),
        ("demo 2 — ", "", "M-L2"),
        (P.PROMPT, "next", "M-L2"),
        ("demo — gate", "", "M-G"),
        ("Q1:", "a", "M-G"),
        ("Q2:", "b", "M-G"),
        ("Q3:", "c", "M-G"),
        ("demo — task", "", "M-GT"),
        (P.PROMPT, "echo hi", "M-GT"),
        (P.PROMPT, "check", "M-GT"),
        ("✓ demo cleared.", "", "M-C"),
        (P.PROMPT, "quit", "M-C"),
    ]
    if got != want:
        return _fail("expansion differs:\n got  %r\n want %r" % (got, want))
    print("ok - expansion (%d actions)" % len(got))

    empty = [a.wait_for for a in P.module_walk("m", 0, {})]
    if empty != ["MODULE — m:", P.PROMPT, "m — gate", "✓ m cleared.", P.PROMPT]:
        return _fail("empty-gate expansion differs: %r" % (empty,))
    print("ok - empty gate spec expands")

    extra = P.module_walk(
        "m", 2, {}, lesson_actions={2: ["echo x"]}, prompt_after={1: "p2> "}
    )
    got = [(a.wait_for, a.send) for a in extra]
    want = [
        ("MODULE — m:", ""),
        (P.PROMPT, "next"),
        ("m 1 — ", ""),
        (P.PROMPT, "next"),
        ("m 2 — ", ""),
        ("p2> ", "echo x"),
        (P.PROMPT, "next"),
        ("m — gate", ""),
        ("✓ m cleared.", ""),
        (P.PROMPT, "quit"),
    ]
    if got != want:
        return _fail("lesson_actions/prompt_after expansion differs:\n got  %r\n want %r" % (got, want))
    print("ok - lesson_actions and prompt_after expand")

    before = P.module_walk(
        "m", 1, {}, lesson_actions={1: ["PS1='x> '"]},
        prompt_before_next={1: "\nx> "}, prompt_after={1: "p> "},
    )
    got = [(a.wait_for, a.send) for a in before]
    want = [
        ("MODULE — m:", ""),
        (P.PROMPT, "next"),
        ("m 1 — ", ""),
        (P.PROMPT, "PS1='x> '"),
        ("\nx> ", "next"),
        ("m — gate", ""),
        ("✓ m cleared.", ""),
        (P.PROMPT, "quit"),
    ]
    if got != want:
        return _fail("prompt_before_next expansion differs:\n got  %r\n want %r" % (got, want))
    print("ok - prompt_before_next expands")
    return 0


def check_drive() -> int:
    work = tempfile.mkdtemp(prefix="selftest-modules-")
    saved = dict(P.MODULE_TABLES)
    try:
        fake = os.path.join(work, "fake-tutor")
        with open(fake, "w", encoding="utf-8") as fp:
            fp.write(FAKE_TUTOR)
        os.chmod(fake, os.stat(fake).st_mode | stat.S_IXUSR)
        P.MODULE_TABLES["demo"] = DRIVE_TABLE
        out = os.path.join(work, "out")
        rc = R.main(
            ["--module", "demo", "--shelltutor", fake, "--out", out, "--timeout", "10"]
        )
        if rc == 6:
            print("skip - fake-tutor drive (no pseudo-terminal available)")
            return 0
        if rc != 0:
            return _fail("run.py --module demo exited %s" % rc)
        bundle = os.path.join(out, "current-rc")
        with open(os.path.join(bundle, "result.tap"), encoding="utf-8") as fp:
            tap = fp.read().strip().splitlines()[-1]
        if not tap.startswith("ok 1 - module-demo"):
            return _fail("unexpected TAP line: %r" % tap)
        with open(os.path.join(bundle, "events.jsonl"), encoding="utf-8") as fp:
            events = [json.loads(line) for line in fp]
        passes = [e for e in events if e["kind"] == "gate-pass"]
        if not passes or not passes[-1]["payload"].get("final"):
            return _fail("no final gate-pass event")
        heights = [e for e in events if e["kind"] == "screen-height"]
        if not heights or any(e["payload"]["budget"] != 20 for e in heights):
            return _fail("screen-height events missing or wrong budget")
        with open(os.path.join(bundle, "summary.md"), encoding="utf-8") as fp:
            summary = fp.read()
        if "progress_after: `absent`" not in summary:
            return _fail("modules must leave .progress absent")
        print("ok - fake tutor drive (%s; %d screen-height events)" % (tap, len(heights)))
        return 0
    finally:
        P.MODULE_TABLES.clear()
        P.MODULE_TABLES.update(saved)
        shutil.rmtree(work, ignore_errors=True)


def check_expected_errors() -> int:
    """Routing of error lines: a screen listed in the allowance yields
    `expected` lines, any other screen yields `unexpected` ones."""
    from scripts.sim import driver as D

    region = "$ dtae\nbash: dtae: command not found\nplain line\n"
    allow = frozenset({"S1_L4"})
    got = D.classify_error_lines(region, "S1_L4", allow)
    if got != ([], ["bash: dtae: command not found"]):
        return _fail("listed screen should route to expected: %r" % (got,))
    got = D.classify_error_lines(region, "S1_L3", allow)
    if got != (["bash: dtae: command not found"], []):
        return _fail("unlisted screen should route to unexpected: %r" % (got,))
    if D.classify_error_lines(region, "S1-L4") != (
        [],
        ["bash: dtae: command not found"],
    ):
        return _fail("S1-L4 must be in the default allowance (WP-14)")
    if D.classify_error_lines(region, "S1-L3")[1]:
        return _fail("no other lesson screen may be allowed by default")
    if D.classify_error_lines("clean\n", "S1_L4", allow) != ([], []):
        return _fail("a clean region must yield nothing")
    if D.should_scan("S1-L3", "leave-lesson-1-3", False):
        return _fail("a leave-* input must not start a scan")
    if not D.should_scan("S1-L4", "run-dtae-mistyped", False):
        return _fail("a command at a lesson screen must start a scan")
    if D.should_scan("S1-L2", "ctrl-l-clear", True):
        return _fail("raw keys are not scanned")
    print("selftest_modules: expected-error routing ok")
    return 0


def main() -> int:
    failures = check_expansion() + check_drive() + check_expected_errors()
    if failures:
        print("selftest_modules: FAILED")
        return 1
    print("selftest_modules: all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
