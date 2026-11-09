#!/usr/bin/env python3
"""scripts/sim/sitting.py — sitting server and client (WP-19, amendment A6).

A synthetic sitting lets an AI session play a learner persona against the
real tutor, one screen at a time, through a pseudo-terminal this project
controls. A long-lived **server** owns one tutor under a pty and writes the
usual evidence bundle; a short-lived **client** (this same file, called from
a shell, one command per turn) talks to it over a Unix socket.

    sitting.py start [--bash /bin/bash] [--cols 80 --rows 24] [--arg N|module]
                     [--out DIR] [--persona NAME]
    sitting.py screen                      # screen since the last clear
    sitting.py send "<text>"               # text + Enter, then the screen
    sitting.py raw "<escape>"              # bytes, no Enter (\\t \\x0c \\x1b \\x1b[A)
    sitting.py note "<context>" "<text>"   # a persona event; sends nothing
    sitting.py stop                        # SIGTERM the tutor, flush the bundle

Every client command except `start` finds the server through `--out`
(default `$TMPDIR/shelltutor-sitting`). One sitting per out directory:
`start` refuses when a socket already exists there.

The child environment follows `run.py` (D-03): a fresh `SHELLTUTOR_HOME`,
an empty `HOME`, `LC_ALL=C`, `VIMINIT`, `PAGER`, fixed geometry. `--bash`
selects the interpreter by running `<bash> ./shelltutor`, so the practice
shell is that same binary (F-014). The bundle (`terminal.jsonl`,
`events.jsonl`, `summary.md`, `result.tap`) is written through
`recorder.Recorder`, so D-19 redaction replaces the login name with
`[user]`. Screens returned to the client are NOT redacted: the learner has
to be able to read and type its own user name.
Screens returned to the client are also cleaned of terminal control residue
(CSI/OSC/DCS sequences, DEC private modes, a finished alternate screen, stray
ESC and `^[`); `terminal.jsonl` stays raw.

Python 3.9+, standard library only.
"""

from __future__ import annotations

import argparse
import codecs
import datetime
import errno
import fcntl
import json
import os
import pty
import re
import selectors
import shutil
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import termios
import time
from typing import Any, Dict, List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(os.path.dirname(_HERE))
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from scripts.sim import env as sim_env  # noqa: E402
from scripts.sim import recorder as sim_recorder  # noqa: E402
from scripts.sim.driver import SCREEN_BUDGET, ScreenHeightTracker  # noqa: E402

SOCKET_NAME = "sitting.sock"
SETTLE_QUIET_S = 0.4
SETTLE_CAP_S = 10.0
IDLE_LIMIT_S = 1800.0
BUFFER_CAP = 200000
_CLEAR_RE = re.compile(r"\x1b\[(?:3J|H|2J)")
_RAW_RE = re.compile(r"\\x([0-9a-fA-F]{2})|\\([tnre\\])")
_CLEARED_RE = re.compile(r"(Stage [1-5] cleared\.|[a-z]+ cleared\.)")
_RAW_NAMES = {"t": b"\t", "n": b"\n", "r": b"\r", "e": b"\x1b", "\\": b"\\"}

# Client-facing reply text only (the recorded terminal.jsonl stays raw).
# A finished full-screen program (man, less, Vim) leaves its alternate-screen
# drawing in the stream; once the program has left the alternate screen that
# drawing is dropped. A program still on it is kept so the persona can read it.
_ALT_SWITCH_RE = re.compile(r"\x1b\[\?(?:1049|1047|47)([hl])")
_ALT_BLOCK_RE = re.compile(r"\x1b\[\?(?:1049|1047|47)h.*?\x1b\[\?(?:1049|1047|47)l", re.S)
# Vim's showcmd area prints the typed Esc as the two characters `^[` right
# after a cursor-position sequence; that is control residue, not output.
_SHOWCMD_ESC_RE = re.compile(r"(\x1b\[[0-9;]*H)\^\[")
# DCS / APC / PM / SOS strings (Vim's terminal probes, e.g. ESC P z z ESC \\).
_STRING_RE = re.compile(r"\x1b[P_^X][^\x1b\x07]*(?:\x1b\\|\x07)")
_ESC_REST_RE = re.compile(r"\x1b[@-Z\\-_]|\x1b[ -/][ -~]|\x1b")
_CTRL_RE = re.compile("[\x00-\x08\x0b\x0e-\x1f\x7f\u0080-\u009f\ufffd]")


def default_out() -> str:
    return os.path.join(tempfile.gettempdir(), "shelltutor-sitting")


def parse_raw(text: str) -> bytes:
    """Turn the escape spellings `\\t \\n \\r \\e \\\\ \\xNN` into bytes."""
    out = bytearray()
    pos = 0
    for m in _RAW_RE.finditer(text):
        out += text[pos:m.start()].encode("utf-8")
        if m.group(1) is not None:
            out.append(int(m.group(1), 16))
        else:
            out += _RAW_NAMES[m.group(2)]
        pos = m.end()
    out += text[pos:].encode("utf-8")
    return bytes(out)


def client_text(raw: str) -> str:
    """Text shown to the persona for the bytes since the last clear: CSI,
    OSC, DEC private modes and DCS strings removed, a finished alternate
    screen dropped, no ESC left (and so no `^[`), other control characters
    and decoder replacement characters removed. Newlines and tabs survive."""
    text = _ALT_BLOCK_RE.sub("", raw)
    text = _SHOWCMD_ESC_RE.sub(r"\1", text)
    text = _STRING_RE.sub("", text)
    text = sim_env.normalize(text)
    text = _ESC_REST_RE.sub("", text)
    return _CTRL_RE.sub("", text)


def mark_prompt(text: str) -> str:
    """Mark the pending (unterminated) last line as `[prompt] ...`."""
    if not text or text.endswith("\n"):
        return text
    head, sep, last = text.rpartition("\n")
    return head + sep + "[prompt] " + last


def heading_of(text: str) -> str:
    """The screen's heading: first non-blank line below the header rule."""
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith(("─", "- shelltutor", "+")) or s.startswith("-" * 8):
            continue
        return s[:70]
    return ""


def _bash_provenance(bash: Optional[str]):
    path = bash or shutil.which("bash", path=os.environ.get("PATH"))
    if not path:
        return "not found", "unknown"
    try:
        proc = subprocess.run(
            [path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            universal_newlines=True, timeout=10,
        )
        version = (proc.stdout.splitlines() or ["unknown"])[0]
    except (OSError, subprocess.SubprocessError):
        version = "unknown"
    home = os.path.expanduser("~")
    if home and home != "~" and path.startswith(home + os.sep):
        path = "~" + path[len(home):]
    return path, version


def _exit_code(status: int) -> int:
    """Exit code, or the negative signal number when a signal ended it."""
    if os.WIFEXITED(status):
        return os.WEXITSTATUS(status)
    if os.WIFSIGNALED(status):
        return -os.WTERMSIG(status)
    return -1


class Sitting:
    """The server side: one tutor under a pty plus the evidence bundle."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.out = os.path.abspath(args.out)
        os.makedirs(self.out, exist_ok=True)
        self.rec = sim_recorder.Recorder(os.path.join(self.out, "bundle"))
        self.start_mono = time.monotonic()
        self.started_at = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        self.decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        self.since_clear = ""
        self.pre_alt: Optional[str] = None
        self.heights = ScreenHeightTracker()
        self.screen_heights: List[Dict[str, Any]] = []
        self.cleared: List[str] = []
        self.context = "unspecified"
        self.inputs = 0
        self.notes = 0
        self.child_exit: Optional[int] = None
        self.eof = False
        self.last_byte = time.monotonic()
        self.sandbox = tempfile.mkdtemp(prefix="shelltutor-sim-home-")
        self.user_home = tempfile.mkdtemp(prefix="shelltutor-sim-userhome-")
        self._spawn()

    # -- child -----------------------------------------------------------

    def _child_env(self) -> Dict[str, str]:
        e = dict(os.environ)
        e["SHELLTUTOR_HOME"] = self.sandbox
        e["HOME"] = self.user_home
        e.setdefault("TERM", "xterm-256color")
        e["COLUMNS"] = str(self.args.cols)
        e["LINES"] = str(self.args.rows)
        e["LC_ALL"] = "C"
        e["VIMINIT"] = "set nocompatible"
        e["PAGER"] = "less"
        e.pop("MANPAGER", None)
        e.pop("LESS", None)
        return e

    def _spawn(self) -> None:
        a = self.args
        script = os.path.join(_PARENT, "shelltutor")
        if a.bash:
            argv = [a.bash, "./shelltutor"]
            exe = a.bash
        else:
            argv = ["./shelltutor"]
            exe = script
        if a.arg:
            argv.append(a.arg)
        self.argv_display = argv[:]
        self.master_fd, slave_fd = pty.openpty()
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ,
                    struct.pack("HHHH", a.rows, a.cols, 0, 0))
        env = self._child_env()
        self.pid = os.fork()
        if self.pid == 0:  # child
            try:
                os.close(self.master_fd)
                os.setsid()
                fcntl.ioctl(slave_fd, termios.TIOCSCTTY, 0)
                for fd in (0, 1, 2):
                    os.dup2(slave_fd, fd)
                if slave_fd > 2:
                    os.close(slave_fd)
                os.chdir(_PARENT)
                os.execve(exe, argv, env)
            except Exception as exc:  # pragma: no cover
                os.write(2, ("sitting: exec failed: %s\n" % exc).encode("utf-8"))
                os._exit(127)
        os.close(slave_fd)
        self.rec.write_event(0.0, "session-start", payload={
            "invocation": " ".join(self.argv_display),
            "geometry": "%dx%d" % (a.cols, a.rows),
            "persona": a.persona,
        })

    # -- output ----------------------------------------------------------

    def _ts(self) -> float:
        return time.monotonic() - self.start_mono

    def _feed(self, data: bytes) -> None:
        ts = self._ts()
        self.rec.write_terminal(ts, "out", data)
        raw = self.decoder.decode(data)
        self.last_byte = time.monotonic()
        self._append_screen(raw)
        text = sim_env.normalize(self.since_clear)
        for m in _CLEARED_RE.finditer(sim_env.normalize(raw)):
            label = m.group(1)
            if label not in self.cleared:
                self.cleared.append(label)
        for lines in self.heights.feed(raw):
            sid = heading_of(text) or "?"
            entry = {"screen_id": sid, "lines": lines, "budget": SCREEN_BUDGET,
                     "over": lines > SCREEN_BUDGET}
            self.screen_heights.append(entry)
            self.rec.write_event(round(ts, 6), "screen-height", screen_id=sid,
                                 payload={"lines": lines, "budget": SCREEN_BUDGET,
                                          "over": lines > SCREEN_BUDGET})

    def _append_screen(self, raw: str) -> None:
        """Add decoded output to the text since the last clear. A program that
        enters the alternate screen (man, less, Vim) is remembered by the text
        before it; when it leaves, that text is restored and the program's
        drawing is dropped (client-facing only; terminal.jsonl is untouched)."""
        pos = 0
        for m in _ALT_SWITCH_RE.finditer(raw):
            self._append_plain(raw[pos:m.start()])
            if m.group(1) == "h":
                if self.pre_alt is None:
                    self.pre_alt = self.since_clear
            elif self.pre_alt is not None:
                self.since_clear = self.pre_alt
                self.pre_alt = None
            pos = m.end()
        self._append_plain(raw[pos:])

    def _append_plain(self, raw: str) -> None:
        self.since_clear += raw
        last = None
        for m in _CLEAR_RE.finditer(self.since_clear):
            last = m
        if last is not None:
            self.since_clear = self.since_clear[last.end():]
        if len(self.since_clear) > BUFFER_CAP:
            self.since_clear = self.since_clear[-BUFFER_CAP:]

    def pump(self, timeout: float) -> bool:
        """Read pending pty output for up to `timeout` s; True if any came."""
        if self.eof:
            time.sleep(min(timeout, 0.05))
            return False
        sel = selectors.DefaultSelector()
        sel.register(self.master_fd, selectors.EVENT_READ)
        got = False
        try:
            for _key, _ in sel.select(timeout):
                try:
                    data = os.read(self.master_fd, 4096)
                except OSError as exc:
                    if exc.errno == errno.EIO:
                        data = b""
                    else:
                        raise
                if data:
                    self._feed(data)
                    got = True
                else:
                    self._on_eof()
        finally:
            sel.close()
        return got

    def _on_eof(self) -> None:
        self.eof = True
        try:
            _, status = os.waitpid(self.pid, 0)
            self.child_exit = _exit_code(status)
        except ChildProcessError:
            self.child_exit = self.child_exit if self.child_exit is not None else -1
        self.rec.write_event(round(self._ts(), 6), "child-exit",
                             payload={"exit_code": self.child_exit})

    def settle(self, quiet: float = SETTLE_QUIET_S, cap: float = SETTLE_CAP_S) -> None:
        """Wait until no new bytes arrive for `quiet` s (at most `cap` s)."""
        start = time.monotonic()
        quiet_since = start
        while time.monotonic() - start < cap:
            if self.pump(0.05):
                quiet_since = time.monotonic()
            elif self.eof or time.monotonic() - quiet_since >= quiet:
                return

    # -- views -----------------------------------------------------------

    def screen(self) -> str:
        text = mark_prompt(client_text(self.since_clear))
        if self.eof:
            text = text.rstrip("\n") + "\n[exited %s]\n" % self.child_exit
        return text

    # -- commands --------------------------------------------------------

    def _write(self, payload: bytes, raw: bool, shown: str) -> None:
        self.inputs += 1
        self.rec.write_terminal(self._ts(), "in", payload)
        sid = heading_of(sim_env.normalize(self.since_clear))
        data = {"data": shown}
        if raw:
            data["raw"] = True
        self.rec.write_event(round(self._ts(), 6), "persona-input", intent=self.context,
                             screen_id=sid, payload=data)
        if not self.eof:
            try:
                os.write(self.master_fd, payload)
            except OSError:
                pass

    def handle(self, req: Dict[str, Any]) -> Dict[str, Any]:
        cmd = req.get("cmd")
        if cmd == "screen":
            self.settle(quiet=0.1, cap=2.0)
            return {"ok": True, "text": self.screen()}
        if cmd == "send":
            text = str(req.get("text", ""))
            self._write((text + "\n").encode("utf-8"), False, text)
            self.settle()
            return {"ok": True, "text": self.screen()}
        if cmd == "raw":
            text = str(req.get("text", ""))
            self._write(parse_raw(text), True, text)
            self.settle()
            return {"ok": True, "text": self.screen()}
        if cmd == "note":
            self.context = str(req.get("context", "unspecified")) or "unspecified"
            self.notes += 1
            self.rec.write_event(round(self._ts(), 6), "note", intent=self.context,
                                 screen_id=heading_of(sim_env.normalize(self.since_clear)),
                                 payload={"monologue": str(req.get("text", ""))})
            return {"ok": True, "text": "noted (context: %s)\n" % self.context}
        if cmd == "stop":
            return {"ok": True, "text": self.finish(), "stop": True}
        return {"ok": False, "text": "unknown command %r\n" % (cmd,)}

    # -- shutdown --------------------------------------------------------

    def finish(self) -> str:
        if not self.eof:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline and not self.eof:
                self.pump(0.1)
                try:
                    done, status = os.waitpid(self.pid, os.WNOHANG)
                except ChildProcessError:
                    break
                if done:
                    self.child_exit = _exit_code(status)
                    self.eof = True
            if not self.eof:
                try:
                    os.kill(self.pid, signal.SIGKILL)
                    os.waitpid(self.pid, 0)
                except (ProcessLookupError, ChildProcessError):
                    pass
        self.rec.write_event(round(self._ts(), 6), "session-end",
                             payload={"inputs": self.inputs, "notes": self.notes})
        progress = "absent"
        try:
            with open(os.path.join(self.sandbox, ".progress"), "r", encoding="utf-8") as fp:
                progress = fp.read().strip() or "empty"
        except OSError:
            pass
        self._write_summary(progress)
        cleared = ", ".join(self.cleared) if self.cleared else "nothing cleared"
        self.rec.write_tap(
            ok=True,
            description="sitting %s (%s) — cleared: %s; progress %s"
            % (self.args.persona or "unnamed", self.args.arg or "default entry",
               cleared, progress),
        )
        self.rec.close()
        shutil.rmtree(self.sandbox, ignore_errors=True)
        shutil.rmtree(self.user_home, ignore_errors=True)
        return "stopped; bundle in %s\n" % os.path.join(self.out, "bundle")

    def _exit_text(self) -> str:
        if self.child_exit is None:
            return "unknown"
        if self.child_exit < 0:
            return "ended by signal %d (stop)" % -self.child_exit
        return str(self.child_exit)

    def _write_summary(self, progress: str) -> None:
        a = self.args
        bash_path, bash_version = _bash_provenance(a.bash)
        host = sim_env.host_snapshot()
        lines = [
            "---",
            "title: Synthetic sitting summary",
            "category: audit",
            "component: sim-sitting",
            "status: candidate-evidence",
            "version: %s" % sim_recorder.HARNESS_VERSION,
            "last_updated: %s" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
            "tags: [audit, simulation, synthetic-sitting, pty]",
            "priority: medium",
            "---",
            "",
            "# Synthetic sitting — %s" % (a.persona or "unnamed persona"),
            "",
            "Generated by `scripts/sim/sitting.py` (WP-19, amendment A6). The",
            "persona is played by an AI session; everything here is candidate",
            "evidence until a maintainer reproduces it on the real tutor.",
            "",
            "## Run metadata",
            "",
            "- started_at_utc: `%s`" % self.started_at,
            "- invocation: `%s`" % " ".join(self.argv_display),
            "- bash_path: `%s`" % bash_path,
            "- bash_version: `%s`" % bash_version,
            "- pty_geometry: `%dx%d`" % (a.cols, a.rows),
            "- persona_inputs: `%d`" % self.inputs,
            "- notes: `%d`" % self.notes,
            "",
            "## Controlled inputs",
            "",
            "- HOME: `empty per-run tempdir`",
            "- SHELLTUTOR_HOME: `fresh per-run tempdir`",
            "- LC_ALL: `C`",
            "- VIMINIT: `set nocompatible`",
            "- PAGER: `less`",
            "- COLUMNS/LINES: `%d/%d`" % (a.cols, a.rows),
            "- host_user: `%s`" % self.rec.redactor.status(),
            "",
            "## Outcome",
            "",
            "- cleared: `%s`" % (", ".join(self.cleared) if self.cleared else "nothing"),
            "- child_exit_code: `%s`" % self._exit_text(),
            "- progress_after: `%s`" % progress,
            "",
            "## Host inputs",
            "",
        ]
        for key in sorted(host):
            lines.append("- %s: `%s`" % (key, host[key]))
        lines += ["", "## Screen heights", "",
                  "Informational. Rendered rows from a clear to the next prompt "
                  "(budget %d)." % SCREEN_BUDGET, "",
                  "| Screen | Lines | Over budget |", "| --- | ---: | --- |"]
        best: Dict[str, int] = {}
        order: List[str] = []
        for row in self.screen_heights:
            sid = str(row["screen_id"])
            if sid not in best:
                order.append(sid)
                best[sid] = 0
            best[sid] = max(best[sid], int(row["lines"]))
        for sid in order:
            lines.append("| %s | %d | %s |" % (sid, best[sid], "yes" if best[sid] > SCREEN_BUDGET else "no"))
        lines += ["", "## File index", "",
                  "- `terminal.jsonl` — chunk-level pty stream (out and in).",
                  "- `events.jsonl` — `persona-input` rows tagged by declared context, "
                  "`note` rows for monologue, `screen-height` rows.",
                  "- `result.tap` — what the sitting cleared.", ""]
        path = os.path.join(self.rec.out_dir, "summary.md")
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(self.rec.redactor.text("\n".join(lines)))


def serve(args: argparse.Namespace) -> int:
    out = os.path.abspath(args.out)
    sitting = Sitting(args)
    os.chdir(out)  # bind a relative path: AF_UNIX paths are short
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sitting.settle(quiet=SETTLE_QUIET_S, cap=5.0)
        listener.bind(SOCKET_NAME)
        listener.listen(1)
        listener.settimeout(0.2)
        last_use = time.monotonic()
        stopping = False
        while not stopping:
            sitting.pump(0.05)
            try:
                conn, _ = listener.accept()
            except socket.timeout:
                if time.monotonic() - last_use > IDLE_LIMIT_S:
                    sitting.finish()
                    break
                continue
            last_use = time.monotonic()
            with conn:
                conn.settimeout(30)
                buf = b""
                while not buf.endswith(b"\n"):
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    buf += chunk
                try:
                    reply = sitting.handle(json.loads(buf.decode("utf-8")))
                except Exception as exc:  # keep the sitting alive
                    reply = {"ok": False, "text": "server error: %s\n" % exc}
                stopping = bool(reply.get("stop"))
                conn.sendall((json.dumps(reply) + "\n").encode("utf-8"))
    finally:
        listener.close()
        try:
            os.unlink(os.path.join(out, SOCKET_NAME))
        except OSError:
            pass
    return 0


# -- client ----------------------------------------------------------------


def _request(out: str, req: Dict[str, Any]) -> Dict[str, Any]:
    out = os.path.abspath(out)
    if not os.path.exists(os.path.join(out, SOCKET_NAME)):
        print("sitting: no sitting is running in %s (run `start`)" % out, file=sys.stderr)
        raise SystemExit(3)
    os.chdir(out)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(40)
    try:
        s.connect(SOCKET_NAME)
    except OSError as exc:
        print("sitting: cannot reach the sitting server: %s" % exc, file=sys.stderr)
        raise SystemExit(3)
    s.sendall((json.dumps(req) + "\n").encode("utf-8"))
    buf = b""
    while not buf.endswith(b"\n"):
        chunk = s.recv(65536)
        if not chunk:
            break
        buf += chunk
    s.close()
    return json.loads(buf.decode("utf-8"))


def _emit(text: str) -> None:
    """Print a reply; end it with a newline so a pending prompt stays visible."""
    sys.stdout.write(text if text.endswith("\n") else text + "\n")


def resolve_bash(value: str) -> Optional[str]:
    """Absolute path of the interpreter named by --bash, or None.

    A name without a slash is looked up on PATH (`--bash bash`); a path must
    be an executable file.
    """
    value = os.path.expanduser(value)
    if os.sep in value:
        path = os.path.abspath(value)
        return path if os.path.isfile(path) and os.access(path, os.X_OK) else None
    return shutil.which(value, path=os.environ.get("PATH"))


def cmd_start(args: argparse.Namespace) -> int:
    if args.bash:
        resolved = resolve_bash(args.bash)
        if resolved is None:
            print("sitting: --bash %r does not name an executable (not on PATH, "
                  "or not an executable file); nothing was started" % args.bash,
                  file=sys.stderr)
            return 2
        args.bash = resolved
    out = os.path.abspath(args.out)
    if os.path.exists(os.path.join(out, SOCKET_NAME)):
        print("sitting: a sitting already exists in %s (stop it, or use another --out)" % out,
              file=sys.stderr)
        return 2
    os.makedirs(out, exist_ok=True)
    if os.path.exists(os.path.join(out, "bundle", "events.jsonl")):
        print("sitting: %s already holds a bundle; use a fresh --out" % out, file=sys.stderr)
        return 2
    cmd = [sys.executable, os.path.abspath(__file__), "_serve", "--out", out,
           "--cols", str(args.cols), "--rows", str(args.rows)]
    if args.bash:
        cmd += ["--bash", args.bash]
    if args.arg:
        cmd += ["--arg", args.arg]
    if args.persona:
        cmd += ["--persona", args.persona]
    log = open(os.path.join(out, "server.log"), "w")
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                     start_new_session=True, cwd=_PARENT)
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if os.path.exists(os.path.join(out, SOCKET_NAME)):
            break
        time.sleep(0.1)
    else:
        print("sitting: the server did not come up; see %s" % os.path.join(out, "server.log"),
              file=sys.stderr)
        return 1
    reply = _request(out, {"cmd": "screen"})
    _emit(reply["text"])
    return 0


def cmd_simple(args: argparse.Namespace) -> int:
    req: Dict[str, Any] = {"cmd": args.command}
    if args.command in ("send", "raw"):
        req["text"] = args.text
    if args.command == "note":
        req["context"] = args.context
        req["text"] = args.text
    reply = _request(args.out, req)
    _emit(reply["text"])
    return 0 if reply.get("ok") else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    def add_out(p: argparse.ArgumentParser) -> None:
        p.add_argument("--out", default=default_out(),
                       help="sitting directory (default: $TMPDIR/shelltutor-sitting)")

    p = sub.add_parser("start", help="start the server and print the first screen")
    add_out(p)
    p.add_argument("--bash", default=None, help="run `<bash> ./shelltutor` (F-014)")
    p.add_argument("--cols", type=int, default=80)
    p.add_argument("--rows", type=int, default=24)
    p.add_argument("--arg", default=None, help="a stage number or a module name")
    p.add_argument("--persona", default="", help="label for the summary")
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("_serve")
    add_out(p)
    p.add_argument("--bash", default=None)
    p.add_argument("--cols", type=int, default=80)
    p.add_argument("--rows", type=int, default=24)
    p.add_argument("--arg", default=None)
    p.add_argument("--persona", default="")
    p.set_defaults(func=serve)

    for name, helptext in (("screen", "print the current screen"),
                           ("stop", "stop the tutor and flush the bundle")):
        p = sub.add_parser(name, help=helptext)
        add_out(p)
        p.set_defaults(func=cmd_simple)
    for name, helptext in (("send", "type text and Enter"), ("raw", "type bytes, no Enter")):
        p = sub.add_parser(name, help=helptext)
        add_out(p)
        p.add_argument("text")
        p.set_defaults(func=cmd_simple)
    p = sub.add_parser("note", help="record a persona note; sends nothing")
    add_out(p)
    p.add_argument("context", help="recall | bash | nav | follow-up")
    p.add_argument("text")
    p.set_defaults(func=cmd_simple)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
