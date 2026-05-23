"""Host input snapshot + output-normalization helpers.

Slice 1 isolates only the /etc/bashrc source statement (in the
no-system-rc-preview variant). Every other host input — TERM,
geometry, PATH, locale, etc. — still bleeds into the captured
transcript unless the harness explicitly notes it. summary.md cites
this module's snapshot so later reviewers do not over-read the
current-rc vs no-system-rc-preview diff.
"""

from __future__ import annotations

import hashlib
import os
import platform
import re
import sys
import tempfile

from .errors import SandboxNotWritableError

_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
# Some lesson copy uses CSI sequences with non-standard intermediate
# bytes (`ESC [ ? 25 l`, `ESC [ K`, etc.). The Stage 1 lesson copy
# only emits SGR plus a `clear` ANSI cursor home, both of which the
# pattern above handles.


def strip_ansi(data: str) -> str:
    """Remove ANSI escape sequences from a string."""
    return _ANSI_RE.sub("", data)


def normalize(data: str) -> str:
    """Normalize PTY output for sentinel matching.

    Strips ANSI, converts CRLF and bare CR to LF. This is a sentinel-
    matching normalization, not a learner-facing transformation; the
    raw bytes still go into terminal.jsonl unchanged.
    """
    out = strip_ansi(data)
    out = out.replace("\r\n", "\n")
    out = out.replace("\r", "\n")
    return out


def host_snapshot() -> dict:
    """Capture the host inputs the run inherits.

    The fields are chosen for diff-readability between runs on the
    same machine and for at-a-glance fingerprinting across machines.
    PATH is hashed (sha256 prefix) rather than recorded verbatim so
    summary.md does not leak the operator's path environment when
    committed to audit/.
    """
    path_value = os.environ.get("PATH", "")
    path_hash = hashlib.sha256(path_value.encode("utf-8", "replace")).hexdigest()[:16]

    def _positive_env_int(name: str):
        raw = os.environ.get(name, "")
        if not raw:
            return None
        try:
            v = int(raw)
        except ValueError:
            return None
        return v if v > 0 else None

    return {
        "term": os.environ.get("TERM") or None,
        "columns": _positive_env_int("COLUMNS"),
        "lines": _positive_env_int("LINES"),
        "path_sha256_prefix": path_hash,
        "python_version": "%d.%d.%d" % sys.version_info[:3],
        "uname_system": platform.system(),
        "uname_release": platform.release(),
        "platform_machine": platform.machine(),
    }


def make_shelltutor_home(prefix: str = "shelltutor-sim-home-") -> str:
    """Create a fresh writable SHELLTUTOR_HOME for a single run.

    The caller is responsible for cleanup unless --keep-sandbox was
    passed to the CLI dispatcher.
    """
    try:
        return tempfile.mkdtemp(prefix=prefix)
    except OSError as exc:
        raise SandboxNotWritableError(
            "tempdir creation for SHELLTUTOR_HOME failed: %s" % exc
        )
