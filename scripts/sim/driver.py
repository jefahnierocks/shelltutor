"""PTY driver loop.

Forks a child that exec()s the tutor under a fresh pseudo-terminal,
streams its output back to the parent through a selectors loop, and
writes persona inputs when sentinels fire. The driver is plain stdlib
— no Pexpect, no third-party deps. Python 3.9+.

Loop discipline:

- Read up to 4 KiB per chunk; timestamp with time.monotonic() offset
  from session start.
- Append raw chunk to the normalized tail (capped at 8 KiB) for
  sentinel matching. The raw byte stream goes to terminal.jsonl
  unchanged.
- Match sentinels against the normalized tail using a search-from
  cursor so previously-consumed text never re-fires.
- On match: emit `sentinel-matched`, advance persona, write the next
  action's `send` string with a trailing newline (or, if `send` is
  empty, just advance).
- On per-sentinel timeout (default 30s): raise SentinelNotFoundError
  with the trailing 512 bytes of the normalized buffer.
- Wall-clock cap per variant: 5 minutes.
"""

from __future__ import annotations

import codecs
import errno
import fcntl
import os
import pty
import re
import selectors
import signal
import struct
import termios
import time
from typing import Dict, List, Optional, Sequence

from .env import normalize
from .errors import HarnessTimeoutError, NoTTYError, PersonaRejectedError, SentinelNotFoundError
from .persona import Action, Persona
from .recorder import Recorder
from .sentinels import PROMPT, SENTINELS

CHUNK_SIZE = 4096
TAIL_CAP = 8192
PER_SENTINEL_TIMEOUT_S = 30.0
WALL_CLOCK_CAP_S = 300.0
SELECT_TICK_S = 0.25
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")

# Lesson screens (S1-L1, S2-L3, ...): persona input typed here is scanned
# for mechanical error signatures.
_LESSON_SCREEN_RE = re.compile(r"^S[1-5]-L[0-9]$")
# Rendered screen height (Q5). A screen starts at a clear sequence and
# ends at the next practice prompt. The budget is on RENDERED lines: 22
# rendered lines before the prompt equal the 20 content lines the script
# states for itself (heredoc 20 + the blank line show_screen adds + the
# practice footer), so a 24-row terminal still shows the prompt.
SCREEN_BUDGET = 22
_CLEAR_RE = re.compile(r"\x1b\[(?:H|2J|3J)")
_PARTIAL_ESC_RE = re.compile(r"\x1b(?:\[[0-9;?]*)?$")


class ScreenHeightTracker:
    """Count rendered lines per cleared screen from the raw OUT stream.

    Feed decoded (not normalised) text. A screen opens at a clear
    sequence (`ESC[H`, `ESC[2J` or `ESC[3J`, any order, consecutive ones
    collapse into one) and closes at the next PROMPT. The count is the
    number of newline-terminated lines of normalised text between the
    two, so the blank line `show_screen` adds and the practice footer
    printed before the prompt are included. Logical lines are counted:
    a line wider than the terminal that wraps is still one line. A
    partial escape sequence or partial prompt at the end of a chunk is
    held back and joined with the next one.
    """

    def __init__(self) -> None:
        self._carry = ""
        self._open = False
        self._text = ""

    def _hold(self, data: str) -> int:
        m = _PARTIAL_ESC_RE.search(data)
        hold = len(data) - m.start() if m else 0
        for k in range(min(len(PROMPT) - 1, len(data)), 0, -1):
            if data.endswith(PROMPT[:k]):
                hold = max(hold, k)
                break
        return hold

    def feed(self, raw: str) -> List[int]:
        data = self._carry + raw
        hold = self._hold(data)
        self._carry = data[len(data) - hold:] if hold else ""
        if hold:
            data = data[: len(data) - hold]
        tokens = sorted(
            [(m.start(), m.end(), "clear") for m in _CLEAR_RE.finditer(data)]
            + [
                (i, i + len(PROMPT), "prompt")
                for i in _find_all(data, PROMPT)
            ]
        )
        done: List[int] = []
        pos = 0
        for start, end, kind in tokens:
            if self._open and start > pos:
                self._text += data[pos:start]
            if kind == "clear":
                if not (self._open and not self._text.strip("\r\n")):
                    self._open, self._text = True, ""
            elif self._open:
                done.append(self._count())
                self._open, self._text = False, ""
            pos = end
        if self._open and pos < len(data):
            self._text += data[pos:]
        return done

    def finish(self) -> Optional[int]:
        """End of run: close a screen that never reached a prompt (the
        finale), counting everything up to EOF."""
        if self._open:
            self._text += self._carry
            self._carry = ""
            n = self._count()
            self._open, self._text = False, ""
            return n
        return None

    def _count(self) -> int:
        return normalize(self._text).count("\n")


def _find_all(data: str, needle: str) -> List[int]:
    out: List[int] = []
    i = data.find(needle)
    while i >= 0:
        out.append(i)
        i = data.find(needle, i + len(needle))
    return out


ERROR_SIGNATURES = (
    "No such file or directory",
    "command not found",
    ": not found",
    "Permission denied",
    "syntax error",
    "Is a directory",
)


def _set_winsize(fd: int, rows: int, cols: int) -> None:
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))


def _resolve_pattern(sentinel_id: str) -> str:
    """Map a persona Action.wait_for id to its substring pattern."""
    if sentinel_id == PROMPT:
        return PROMPT
    try:
        return SENTINELS[sentinel_id]
    except KeyError:
        # Fall back to literal: lets a persona inline a substring
        # without registering it in sentinels.SENTINELS. This is
        # belt-and-braces; the v1 persona uses only registered ids.
        return sentinel_id


def drive(
    shelltutor_path: str,
    env: dict,
    persona: Persona,
    recorder: Recorder,
    rows: int = 24,
    cols: int = 80,
    per_sentinel_timeout: float = PER_SENTINEL_TIMEOUT_S,
    wall_clock_cap: float = WALL_CLOCK_CAP_S,
    child_args: Sequence[str] = (),
    final_gate_id: str = "STAGE_CLEARED",
    display_path: Optional[str] = None,
) -> dict:
    """Run a single variant. Returns a dict of run-level outcomes:

        {"child_exit_code": int | None,
         "gate_passed": bool,
         "duration_seconds": float,
         "wall_clock_capped": bool,
         "error_signatures": [{"screen_id", "intent", "text"}, ...]}

    `child_args` is appended to argv (C-001: `shelltutor N`).
    `final_gate_id` is the sentinel whose match counts as the run's
    gate pass; every `*CLEARED` sentinel still records a gate-pass event.
    `display_path` is what evidence records for the script (repo-relative,
    D-15); it defaults to `shelltutor_path`.
    """
    try:
        master_fd, slave_fd = pty.openpty()
    except OSError as exc:
        raise NoTTYError("pty.openpty failed: %s" % exc)

    _set_winsize(slave_fd, rows, cols)

    child_pid = os.fork()
    if child_pid == 0:
        # Child branch.
        try:
            os.close(master_fd)
            os.setsid()
            # Make the slave the controlling tty.
            fcntl.ioctl(slave_fd, termios.TIOCSCTTY, 0)
            os.dup2(slave_fd, 0)
            os.dup2(slave_fd, 1)
            os.dup2(slave_fd, 2)
            if slave_fd > 2:
                os.close(slave_fd)
            os.execvpe(shelltutor_path, [shelltutor_path] + list(child_args), env)
        except Exception as exc:  # pragma: no cover — child exec failure
            os.write(2, ("harness: exec failed: %s\n" % exc).encode("utf-8"))
            os._exit(127)

    # Parent branch.
    os.close(slave_fd)

    selector = selectors.DefaultSelector()
    selector.register(master_fd, selectors.EVENT_READ)

    start_mono = time.monotonic()
    last_match_mono = start_mono
    norm_tail = ""
    tail_base = 0  # absolute offset of norm_tail[0] in the whole stream
    match_cursor = 0  # absolute offset
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    scan: Optional[Dict[str, object]] = None
    heights = ScreenHeightTracker()
    screen_heights: List[Dict[str, object]] = []
    error_signatures: List[Dict[str, str]] = []
    last_guard: Optional[Action] = None
    gate_passed = False
    child_exit_code: Optional[int] = None
    wall_clock_capped = False

    recorder.write_event(0.0, "session-start", payload={"shelltutor_path": display_path or shelltutor_path})

    try:
        while True:
            now = time.monotonic()
            if now - start_mono > wall_clock_cap:
                wall_clock_capped = True
                recorder.write_event(
                    round(now - start_mono, 6),
                    "timeout",
                    payload={
                        "kind": "wall-clock",
                        "limit_seconds": wall_clock_cap,
                    },
                )
                break

            current = persona.current
            if current is not None:
                if now - last_match_mono > per_sentinel_timeout:
                    tail = norm_tail[-512:]
                    pattern = _resolve_pattern(current.wait_for)
                    recorder.write_event(
                        round(now - start_mono, 6),
                        "timeout",
                        intent=current.intent,
                        screen_id=current.screen_id,
                        payload={
                            "kind": "per-sentinel",
                            "sentinel": current.wait_for,
                            "pattern": pattern,
                            "tail": tail,
                        },
                    )
                    _drain_and_kill(master_fd, child_pid)
                    raise SentinelNotFoundError(current.wait_for, pattern, tail)

            events = selector.select(SELECT_TICK_S)
            chunk_bytes = b""
            child_eof = False
            if events:
                try:
                    chunk_bytes = os.read(master_fd, CHUNK_SIZE)
                except OSError as exc:
                    if exc.errno == errno.EIO:
                        child_eof = True
                    else:
                        raise
                if not chunk_bytes and not child_eof:
                    child_eof = True

            if chunk_bytes:
                ts = time.monotonic() - start_mono
                recorder.write_terminal(ts, "out", chunk_bytes)
                raw_chunk = decoder.decode(chunk_bytes)
                norm_chunk = normalize(raw_chunk)
                for n in heights.feed(raw_chunk):
                    _record_height(recorder, screen_heights, start_mono,
                                   persona, n)
                norm_tail += norm_chunk
                if len(norm_tail) > TAIL_CAP:
                    cut = len(norm_tail) - TAIL_CAP
                    norm_tail = norm_tail[cut:]
                    tail_base += cut

            # Finalize a pending error-signature scan once the next
            # prompt has appeared (before any matching, so a scan is
            # never overwritten unscanned).
            if scan is not None:
                start = max(0, int(scan["start"]) - tail_base)
                idx_p = norm_tail.find(PROMPT, start)
                if idx_p >= 0:
                    region = norm_tail[start:idx_p]
                    for line in region.split("\n"):
                        if any(sig in line for sig in ERROR_SIGNATURES):
                            text = line.strip()
                            error_signatures.append(
                                {
                                    "screen_id": str(scan["screen_id"]),
                                    "intent": str(scan["intent"]),
                                    "text": text,
                                }
                            )
                            recorder.write_event(
                                round(time.monotonic() - start_mono, 6),
                                "error-signature",
                                intent=str(scan["intent"]),
                                screen_id=str(scan["screen_id"]),
                                payload={"text": text},
                            )
                    scan = None

            # Match persona actions against the buffer. Loop so that
            # consecutive no-wait actions (raw keys, Vim sequences) and
            # already-buffered sentinels fire without a select tick.
            while True:
                current = persona.current
                if current is None or not (norm_tail or current.wait_for == ""):
                    break
                immediate = current.wait_for == ""
                pattern = "" if immediate else _resolve_pattern(current.wait_for)
                if immediate:
                    idx_abs = match_cursor
                    matched = True
                else:
                    idx = norm_tail.find(pattern, max(0, match_cursor - tail_base))
                    matched = idx >= 0
                    idx_abs = idx + tail_base
                if not matched:
                    # Re-fire detection: if the persona advanced past a
                    # gate question or gate-task header and that same
                    # text appears again ahead of the cursor before the
                    # next sentinel matches, the gate rejected us.
                    if last_guard is not None:
                        gpat = _resolve_pattern(last_guard.wait_for)
                        if norm_tail.find(gpat, max(0, match_cursor - tail_base)) >= 0:
                            recorder.write_event(
                                round(time.monotonic() - start_mono, 6),
                                "gate-fail",
                                intent=last_guard.intent,
                                screen_id=last_guard.screen_id,
                                payload={"reason": "question re-asked"},
                            )
                            _drain_and_kill(master_fd, child_pid)
                            raise PersonaRejectedError(
                                "gate re-asked %s — careful-beginner answer rejected"
                                % last_guard.intent
                            )
                    break

                matched_at_ts = time.monotonic() - start_mono
                recorder.write_event(
                    round(matched_at_ts, 6),
                    "sentinel-matched",
                    intent=current.intent,
                    screen_id=current.screen_id,
                    payload={
                        "sentinel": current.wait_for,
                        "pattern": pattern,
                        "cursor_after": idx_abs + len(pattern),
                    },
                )
                match_cursor = idx_abs + len(pattern)
                last_match_mono = time.monotonic()
                if current.send:
                    if current.delay_s > 0:
                        time.sleep(current.delay_s)
                    payload_bytes = (
                        current.send if current.raw else current.send + "\n"
                    ).encode("utf-8")
                    os.write(master_fd, payload_bytes)
                    recorder.write_terminal(
                        time.monotonic() - start_mono,
                        "in",
                        payload_bytes,
                    )
                    event_payload = {"data": current.send}
                    if current.raw:
                        event_payload["raw"] = True
                    recorder.write_event(
                        round(time.monotonic() - start_mono, 6),
                        "persona-input",
                        intent=current.intent,
                        screen_id=current.screen_id,
                        payload=event_payload,
                    )
                    if _LESSON_SCREEN_RE.match(current.screen_id) and not current.raw:
                        scan = {
                            "start": tail_base + len(norm_tail),
                            "screen_id": current.screen_id,
                            "intent": current.intent,
                        }
                persona.advance()

                if current.wait_for in _REJECTION_GUARD_IDS:
                    last_guard = current
                if (
                    current.wait_for.endswith("CLEARED")
                    or current.wait_for == final_gate_id
                ):
                    if current.wait_for == final_gate_id:
                        gate_passed = True
                    recorder.write_event(
                        round(time.monotonic() - start_mono, 6),
                        "gate-pass",
                        intent=current.intent,
                        screen_id=current.screen_id,
                        payload={"final": current.wait_for == final_gate_id},
                    )
                    last_guard = None

            if child_eof:
                last = heights.finish()
                if last is not None:
                    _record_height(recorder, screen_heights, start_mono,
                                   persona, last)
                break

            if persona.current is None and not events:
                # Persona exhausted — drain until the child closes the
                # PTY or the wall-clock cap fires.
                continue

    finally:
        try:
            selector.unregister(master_fd)
        except (KeyError, ValueError):
            pass
        try:
            os.close(master_fd)
        except OSError:
            pass

    # Reap child.
    try:
        _, status = os.waitpid(child_pid, 0)
        if os.WIFEXITED(status):
            child_exit_code = os.WEXITSTATUS(status)
        elif os.WIFSIGNALED(status):
            child_exit_code = -os.WTERMSIG(status)
    except ChildProcessError:
        child_exit_code = None

    duration = time.monotonic() - start_mono
    recorder.write_event(
        round(duration, 6),
        "child-exit",
        payload={"exit_code": child_exit_code},
    )
    recorder.write_event(
        round(duration, 6),
        "session-end",
        payload={
            "gate_passed": gate_passed,
            "wall_clock_capped": wall_clock_capped,
        },
    )
    if persona.current is not None:
        # Persona did not finish. If we got here without raising,
        # treat it as a timeout — but record it as a finding rather
        # than re-raise (the caller decides whether to commit).
        recorder.write_event(
            round(duration, 6),
            "finding",
            intent=persona.current.intent if persona.current else "",
            screen_id=persona.current.screen_id if persona.current else "",
            payload={"kind": "persona-not-completed"},
        )
    else:
        recorder.write_event(
            round(duration, 6),
            "persona-end",
            payload={},
        )

    return {
        "child_exit_code": child_exit_code,
        "gate_passed": gate_passed,
        "duration_seconds": duration,
        "wall_clock_capped": wall_clock_capped,
        "error_signatures": error_signatures,
        "screen_heights": screen_heights,
    }


def _record_height(recorder, screen_heights, start_mono, persona, lines) -> None:
    """Emit a screen-height event. Informational only (Q5): it never
    changes the TAP result or an exit code."""
    cur = persona.current
    if cur is None and persona.cursor > 0:
        cur = persona._actions[persona.cursor - 1]  # last action: finale
    screen_id = cur.screen_id if cur is not None else ""
    entry = {
        "screen_id": screen_id,
        "lines": lines,
        "budget": SCREEN_BUDGET,
        "over": lines > SCREEN_BUDGET,
    }
    screen_heights.append(entry)
    recorder.write_event(
        round(time.monotonic() - start_mono, 6),
        "screen-height",
        screen_id=screen_id,
        payload={"lines": lines, "budget": SCREEN_BUDGET, "over": lines > SCREEN_BUDGET},
    )


# Recall-question and gate-task-header sentinels. A re-fire after the
# persona advanced past one means the gate rejected the answer or task.
_REJECTION_GUARD_IDS = {
    "GATE_Q1",
    "GATE_Q2",
    "GATE_Q3",
    "TASK_Q_WHOAMI",
    "TASK_Q_PWD",
    "TASK_Q_DAY",
} | {
    "S%d_%s" % (n, k)
    for n in (2, 3, 4, 5)
    for k in ("Q1", "Q2", "Q3", "TASK")
} | {"S5_TASK1", "S5_TASK2"}


def _drain_and_kill(master_fd: int, child_pid: int) -> None:
    """Best-effort: stop the child so the caller's exception
    propagates without leaving zombie processes or open ptys.
    """
    try:
        os.kill(child_pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline:
        try:
            done_pid, _ = os.waitpid(child_pid, os.WNOHANG)
        except ChildProcessError:
            return
        if done_pid != 0:
            return
        time.sleep(0.05)
    try:
        os.kill(child_pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        os.waitpid(child_pid, 0)
    except ChildProcessError:
        pass


# Exported for symmetry with the spec's named-error catalogue.
__all__ = ["drive", "HarnessTimeoutError", "_ANSI_RE"]
