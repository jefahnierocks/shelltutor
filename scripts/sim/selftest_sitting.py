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


# Bytes captured from a real run (Bash 3.2.57 on macOS, Stage 5 practice
# prompt): `man ls` then `q`, and the start of `vim practice.txt` with the
# typed Esc echoed by Vim's showcmd as `^[`. The man page is cut short by the
# pager; the escape sequences are verbatim.
CAPTURED_MAN = b'shelltutor> man ls\r\n\x1b[?1049h\x1b[24;1H\x1b[?1h\x1b=\rLS(1)                       General Commands Manual                      LS(1)\r\n\r\n\x1b[1mNAME\x1b[0m\r\n     \x1b[1mls\x1b[0m - list directory contents\r\n\r\n\x1b[1mSYNOPSIS\x1b[0m\r\n     \x1b[1mls\x1b[0m [\x1b[1m-@ABCFGHILOPRSTUWabcdefghiklmnopqrstuvwxy1%,\x1b[0m] [\x1b[1m--color\x1b[0m=\x1b[4mwhen\x1b[24m]\r\n        [\x1b[1m-D\x1b[0m \x1b[4mformat\x1b[24m] [\x1b[4mfile\x1b[24m \x1b[4m...\x1b[24m]\r\n\r\n\x1b[1mDESCRIPTION\x1b[0m\r\n     For each operand that names a \x1b[4mfile\x1b[24m of a type other than directory, \x1b[1mls\x1b[0m\r\n     displays its name as well as any requested, associated information.  For\r\n     each operand that names a \x1b[4mfile\x1b[24m of type directory, \x1b[1mls\x1b[0m displays the names\r\n     of files contained within that directory, as well as any requested,\r\n     associated information.\r\n\r\n     If no operands are given, the contents of the current directory are\r\n     displayed.  If more than one operand is given, non-directory operands are\r\n     displayed first; directory and non-directory operands are sorted\r\n     separately and in lexicographical order.\r\n\r\n     The following options are available:\r\n\r\n:\x1b[K\r\x1b[K\x1b[?1l\x1b>\x1b[?1049lshelltutor> '
CAPTURED_VIM = b'vim practice.txt\r\n\x1b[?1049h\x1b[>4;2m\x1b[?1h\x1b=\x1b[?2004h\x1b[?1004h\x1b[1;24r\x1b[?12h\x1b[?12l\x1b[22;2t\x1b[22;1t\x1b[27m\x1b[23m\x1b[29m\x1b[m\x1b[H\x1b[2J\x1b[?25l\x1b[24;1H"practice.txt" 1L, 7B\x1b[2;1H\xbd\x1b[6n\x1b[2;1H  \x1b[3;1H\x1bPzz\x1b\\\x1b[0%m\x1b[6n\x1b[3;1H           \x1b[1;1H\x1b[>c\x1b]11;?\x07\x1b]10;?\x07\x1b[1;1Hbefore\r\n\x1b[94m~                                                                               \x1b[3;1H~                                                                               \x1b[4;1H~         \x1b[24;70H^[\x1b[1;1H\x1b[?25h\x1b[?25l\x1b[24;1H:q!\x1b[?1049lshelltutor> '


def check_client_text():
    """The persona-facing reply drops control residue (H-1, H-2)."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
    from scripts.sim.sitting import client_text

    man = CAPTURED_MAN.decode("utf-8", "replace")
    inside = client_text(man[: man.index("\x1b[?1049l")])
    if "LS(1)" not in inside or "NAME" not in inside or "\x1b" in inside:
        return fail("man still on the alternate screen must stay readable: %r" % inside[:120])
    done = client_text(man)
    if "LS(1)" in done or "\x1b" in done or not done.endswith("shelltutor> "):
        return fail("finished man screen must be dropped: %r" % done)
    vim_raw = CAPTURED_VIM.decode("utf-8", "replace")
    if client_text(vim_raw) != "vim practice.txt\nshelltutor> ":
        return fail("a finished vim screen must leave only the shell lines")
    vim = client_text(vim_raw[: vim_raw.index("\x1b[?1049l")])
    for bad in ("Pzz", "^[", "\x1b", "\ufffd", "[6n", "11;?"):
        if bad in vim:
            return fail("vim reply still holds %r: %r" % (bad, vim[:160]))
    if 'practice.txt" 1L, 7B' not in vim or "before" not in vim:
        return fail("vim reply lost its text: %r" % vim[:160])
    # The alternate screen is dropped even when the program clears it (Vim
    # sends ESC[H ESC[2J), because the text before it is restored on exit.
    import types
    from scripts.sim import sitting as sit

    stub = types.SimpleNamespace(since_clear="", pre_alt=None)
    stub._append_plain = types.MethodType(sit.Sitting._append_plain, stub)
    for chunk in ("shelltutor> vim x\r\n\x1b[?1049h\x1b[H\x1b[2Jtildes ~ ~", " drawing", "\x1b[?1049lshelltutor> "):
        sit.Sitting._append_screen(stub, chunk)
    if client_text(stub.since_clear) != "shelltutor> vim x\nshelltutor> " or stub.pre_alt is not None:
        return fail("alternate screen with a clear must be dropped on exit: %r" % stub.since_clear)
    if client_text("a\x1b\x07b\r\n\tc\x00") != "a" + "b\n\tc":
        return fail("lone ESC and control characters must go, newline and tab stay")
    return 0


def main():
    rc = check_client_text()
    if rc:
        return rc
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
    # A missing interpreter is refused before anything is created.
    rc, _, err = run(out, "start", "--out", out, "--bash", "no-such-bash-xyz")
    if rc != 2 or "does not name an executable" not in err or os.path.exists(out):
        return fail("missing --bash: rc=%s err=%r exists=%s" % (rc, err, os.path.exists(out)))
    rc, _, err = run(out, "start", "--out", out, "--bash", "/no/such/bash")
    if rc != 2 or os.path.exists(out):
        return fail("missing --bash path: rc=%s err=%r" % (rc, err))
    try:
        rc, text, err = run(out, "start", "--out", out, "--persona", "probe", "--bash", "bash")
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
