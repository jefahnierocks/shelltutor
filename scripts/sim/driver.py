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
from typing import Optional

from .env import normalize
from .errors import HarnessTimeoutError, NoTTYError, PersonaRejectedError, SentinelNotFoundError
from .persona import Persona
from .recorder import Recorder
from .sentinels import PROMPT, SENTINELS

CHUNK_SIZE = 4096
TAIL_CAP = 8192
PER_SENTINEL_TIMEOUT_S = 30.0
WALL_CLOCK_CAP_S = 300.0
SELECT_TICK_S = 0.25
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


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
) -> dict:
    """Run a single variant. Returns a dict of run-level outcomes:

        {"child_exit_code": int | None,
         "gate_passed": bool,
         "duration_seconds": float,
         "wall_clock_capped": bool}
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
            os.execvpe(shelltutor_path, [shelltutor_path], env)
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
    match_cursor = 0
    gate_passed = False
    child_exit_code: Optional[int] = None
    wall_clock_capped = False

    recorder.write_event(0.0, "session-start", payload={"shelltutor_path": shelltutor_path})

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
                norm_chunk = normalize(chunk_bytes.decode("utf-8", "replace"))
                norm_tail = (norm_tail + norm_chunk)[-TAIL_CAP:]
                # Recompute cursor relative to the (possibly truncated) tail.
                if len(norm_tail) < TAIL_CAP:
                    # Cursor remains unchanged when tail has not wrapped.
                    pass
                else:
                    # Tail truncated from the left by len(norm_chunk)
                    # at most; clamp cursor so it stays inside the buffer.
                    if match_cursor < 0:
                        match_cursor = 0
                    match_cursor = max(0, min(match_cursor, len(norm_tail)))

            # Try to match the current persona action.
            current = persona.current
            if current is not None and norm_tail:
                pattern = _resolve_pattern(current.wait_for)
                # Search only forward from the cursor.
                idx = norm_tail.find(pattern, match_cursor)
                if idx >= 0:
                    matched_at_ts = time.monotonic() - start_mono
                    recorder.write_event(
                        round(matched_at_ts, 6),
                        "sentinel-matched",
                        intent=current.intent,
                        screen_id=current.screen_id,
                        payload={
                            "sentinel": current.wait_for,
                            "pattern": pattern,
                            "cursor_after": idx + len(pattern),
                        },
                    )
                    match_cursor = idx + len(pattern)
                    last_match_mono = time.monotonic()
                    if current.send:
                        payload_bytes = (current.send + "\n").encode("utf-8")
                        os.write(master_fd, payload_bytes)
                        recorder.write_terminal(
                            time.monotonic() - start_mono,
                            "in",
                            payload_bytes,
                        )
                        recorder.write_event(
                            round(time.monotonic() - start_mono, 6),
                            "persona-input",
                            intent=current.intent,
                            screen_id=current.screen_id,
                            payload={"data": current.send},
                        )
                    persona.advance()

                    if current.wait_for == "STAGE_CLEARED":
                        gate_passed = True
                        recorder.write_event(
                            round(time.monotonic() - start_mono, 6),
                            "gate-pass",
                            intent=current.intent,
                            screen_id=current.screen_id,
                            payload={},
                        )
                    # Detect persona-rejection: if the very next action
                    # waits for the same sentinel we just matched, that
                    # is fine (a new prompt). But the gate-rejection
                    # signal we care about is the recall question
                    # text re-appearing. Handle that conservatively by
                    # checking if the recently-matched cursor is far
                    # enough behind end-of-tail to allow another match
                    # of the same gate-question pattern; if such a
                    # repeat happens for GATE_Q* or TASK_Q_* before we
                    # progressed, raise.
                    # (No-op here — re-fire detection handled when the
                    # next iteration sees an unexpected pattern.)
                else:
                    # Re-fire detection: if the persona JUST advanced past
                    # a gate-question (recall Q1/Q2/Q3 or task Q whoami/
                    # pwd/day), and the same question pattern appears
                    # again ahead of the cursor before our next sentinel
                    # matches, the answer was rejected.
                    rejected = _detect_rejection(
                        persona, norm_tail, match_cursor
                    )
                    if rejected is not None:
                        recorder.write_event(
                            round(time.monotonic() - start_mono, 6),
                            "gate-fail",
                            intent=rejected,
                            screen_id="S1-G",
                            payload={"reason": "question re-asked"},
                        )
                        _drain_and_kill(master_fd, child_pid)
                        raise PersonaRejectedError(
                            "gate re-asked %s — careful-beginner answer rejected"
                            % rejected
                        )

            if child_eof:
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
    }


_REJECTION_GUARD_IDS = {
    "GATE_Q1",
    "GATE_Q2",
    "GATE_Q3",
    "TASK_Q_WHOAMI",
    "TASK_Q_PWD",
    "TASK_Q_DAY",
}


def _detect_rejection(persona: Persona, norm_tail: str, cursor: int) -> Optional[str]:
    """If the prior step was a recall/task-question answer and the
    same question pattern re-appears ahead of the cursor, the gate
    rejected the answer.

    Returns the intent string of the rejected step, or None.
    """
    if persona.cursor == 0:
        return None
    # Look at the action we just advanced past.
    prior_idx = persona.cursor - 1
    prior = persona._actions[prior_idx]  # private but stable in this module
    if prior.wait_for not in _REJECTION_GUARD_IDS:
        return None
    pattern = _resolve_pattern(prior.wait_for)
    if norm_tail.find(pattern, cursor) >= 0:
        return prior.intent
    return None


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
