#!/usr/bin/env python3
"""scripts/sim/selftest_sitting.py — scripted probe of sitting.py (WP-19).

Not a persona. Drives `start`, `screen`, `send next` x3, `send whoami`,
`note`, `raw \\t` and `stop` against the real tutor and checks the bundle:
typed inputs and notes are recorded with their declared context, the login
name is replaced by `[user]` in every file, and `result.tap` says what was
cleared. Skips with a message when no pseudo-terminal is available.
Exit 0 on success or skip, 1 on failure. Python 3.9+, stdlib only.
"""

import getpass
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SITTING = os.path.join(HERE, "sitting.py")


def run(out, *args):
    proc = subprocess.run(
        [sys.executable, SITTING] + list(args), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True, timeout=60,
    )
    return proc.returncode, proc.stdout, proc.stderr


def fail(msg):
    print("selftest_sitting: FAIL — %s" % msg)
    return 1


def main():
    try:
        import pty
        m, s = pty.openpty()
        os.close(m)
        os.close(s)
    except OSError:
        print("selftest_sitting: skip - no pseudo-terminal available")
        return 0
    user = getpass.getuser()
    if len(user) < 3:
        print("selftest_sitting: skip - login name too short to redact")
        return 0
    out = os.path.join(tempfile.mkdtemp(prefix="selftest-sitting-"), "s")
    try:
        rc, text, err = run(out, "start", "--out", out, "--persona", "probe")
        if rc != 0 or "SHELLTUTOR" not in text:
            return fail("start rc=%s err=%r text=%r" % (rc, err, text[:200]))
        if "[prompt] shelltutor> " not in text:
            return fail("first screen lacks the marked prompt: %r" % text[-120:])
        rc2, _, err2 = run(out, "start", "--out", out)
        if rc2 != 2:
            return fail("second start should refuse (rc 2), got %s" % rc2)
        for _ in range(3):
            rc, text, err = run(out, "send", "--out", out, "next")
            if rc != 0:
                return fail("send next: %s" % err)
        if "1.1" not in text and "Stage 1" not in text:
            return fail("three nexts did not reach a Stage 1 screen: %r" % text[:200])
        run(out, "note", "--out", out, "bash", "I will ask who I am")
        rc, text, _ = run(out, "send", "--out", out, "whoami")
        if user not in text:
            return fail("the learner must see its own user name in the screen")
        rc, text, _ = run(out, "raw", "--out", out, "ec\\t")
        rc, text, _ = run(out, "stop", "--out", out)
        if "stopped" not in text:
            return fail("stop: %r" % text)
        bundle = os.path.join(out, "bundle")
        for name in ("terminal.jsonl", "events.jsonl", "summary.md", "result.tap"):
            path = os.path.join(bundle, name)
            if not os.path.isfile(path):
                return fail("missing %s" % name)
            with open(path, encoding="utf-8") as fp:
                body = fp.read()
            if user in body:
                return fail("%s contains the login name" % name)
        with open(os.path.join(bundle, "events.jsonl"), encoding="utf-8") as fp:
            rows = [json.loads(line) for line in fp if line.strip()]
        inputs = [r for r in rows if r["kind"] == "persona-input"]
        notes = [r for r in rows if r["kind"] == "note"]
        if len(inputs) != 5:
            return fail("expected 5 persona-input rows, saw %d" % len(inputs))
        if [r["intent"] for r in inputs[-2:]] != ["bash", "bash"]:
            return fail("inputs after the note should carry context 'bash'")
        if not inputs[-1]["payload"].get("raw") or len(notes) != 1:
            return fail("raw flag or note row missing")
        with open(os.path.join(bundle, "terminal.jsonl"), encoding="utf-8") as fp:
            if "[user]" not in fp.read():
                return fail("whoami output was not redacted to [user]")
        print("selftest_sitting: all checks passed")
        return 0
    finally:
        run(out, "stop", "--out", out)
        shutil.rmtree(os.path.dirname(out), ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
