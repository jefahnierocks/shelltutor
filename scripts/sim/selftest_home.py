#!/usr/bin/env python3
"""scripts/sim/selftest_home.py — SHELLTUTOR_HOME reaches the practice shell
exactly as the learner set it (A15; C-004, C-007).

The tutor normalises the variable for its own use (an absolute path, no
trailing slash, in $SANDBOX); the practice shell must still see the learner's
own value: unset stays unset, a relative value stays relative, a trailing
slash stays. The env module's lesson 5 prints it in brackets and says an empty
pair means "not set"; that is only true if this holds.

Starts `./shelltutor` under a pseudo-terminal in three environments, types
`echo "[$SHELLTUTOR_HOME]"` at the first practice prompt and compares the
output. Python 3.9+, standard library only. Exit 0 when all pass; the
pseudo-terminal case is skipped (exit 0) when no pty can be opened.
"""

from __future__ import annotations

import os
import pty
import re
import select
import signal
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHELLTUTOR = os.path.join(ROOT, "shelltutor")
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def run_case(env_extra: dict, unset: bool, cwd: str, home: str):
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": home,
        "TERM": "xterm-256color",
        "LC_ALL": "C",
        "COLUMNS": "80",
        "LINES": "24",
    }
    env.update(env_extra)
    try:
        pid, fd = pty.fork()
    except OSError:
        return None
    if pid == 0:
        os.chdir(cwd)
        os.execve(SHELLTUTOR, [SHELLTUTOR, "1"], env)
    out = b""

    def pump(seconds: float, until: str = "") -> str:
        nonlocal out
        end = time.time() + seconds
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.2)
            if r:
                try:
                    out += os.read(fd, 4096)
                except OSError:
                    break
            if until and until in ANSI.sub("", out.decode("utf-8", "replace")):
                break
        return ANSI.sub("", out.decode("utf-8", "replace")).replace("\r", "")

    pump(8, "shelltutor> ")
    os.write(fd, b'echo "[$SHELLTUTOR_HOME]"\n')
    text = pump(6, "]\n")
    os.write(fd, b"quit\n")
    pump(1)
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    m = re.findall(r"\n\[([^\]\n]*)\]\n", text)
    return m[-1] if m else text[-200:]


def main() -> int:
    base = tempfile.mkdtemp(prefix="selftest-home-")
    cwd = os.path.join(base, "cwd")
    home = os.path.join(base, "home")
    os.makedirs(cwd)
    os.makedirs(home)
    cases = [
        ("unset stays unset", {}, ""),
        ("relative stays relative", {"SHELLTUTOR_HOME": "practice-rel"}, "practice-rel"),
        (
            "trailing slash stays",
            {"SHELLTUTOR_HOME": os.path.join(base, "abs") + "/"},
            os.path.join(base, "abs") + "/",
        ),
    ]
    failed = 0
    for label, extra, want in cases:
        got = run_case(extra, not extra, cwd, home)
        if got is None:
            print("skip - SHELLTUTOR_HOME pass-through (no pseudo-terminal available)")
            return 0
        if got == want:
            print("ok - %s ([%s])" % (label, got))
        else:
            failed += 1
            print("FAIL - %s: want [%s], got [%s]" % (label, want, got))
    print("selftest_home: %s" % ("all checks passed" if not failed else "FAILED"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
