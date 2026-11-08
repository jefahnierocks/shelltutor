"""Evidence-bundle writer.

One Recorder per variant. Writes terminal.jsonl, events.jsonl,
summary.md, and result.tap into <out>/<variant>/. The terminal log is
the project-local v1 format described in
docs/simulation-design-plan.md §Evidence Bundle — it is NOT asciicast
v3 and does not use a .cast extension.

terminal.jsonl rows:
    {"ts": float, "dir": "in"|"out", "enc": "utf8"|"b64",
     "data": str, "len": int}

events.jsonl rows:
    {"ts": float, "kind": str, "intent": str, "screen_id": str,
     "payload": object}

A pair-of-runs diff is the dispatcher's job; this module only writes
single-variant artifacts.
"""

from __future__ import annotations

import base64
import datetime
import getpass
import json
import os
from typing import Any, Dict, Iterable, List, Optional


HARNESS_VERSION = "0.1.0"

# D-19: the host login name is a host input the harness cannot control
# (`whoami` is the host's), so it is replaced with a fixed token before
# any committed file is written. Names shorter than this are left alone
# (too many false hits) and the summary says so.
REDACTION_TOKEN = "[user]"
MIN_REDACT_LEN = 3


class Redactor:
    """Replace the host user name with REDACTION_TOKEN in written evidence.

    Built once per run. It only touches what is written to disk; the
    driver keeps matching against the unredacted stream. Terminal chunks
    are redacted as bytes, so base64 rows (non-UTF-8 chunks) are covered
    too. A chunk that ends with a partial name is held back and joined
    with the next chunk of the same direction, so a name split across two
    PTY reads is still caught.
    """

    def __init__(self, name: Optional[str]):
        self.name = name or ""
        self.enabled = len(self.name) >= MIN_REDACT_LEN
        self._name_b = self.name.encode("utf-8")
        self._token_b = REDACTION_TOKEN.encode("utf-8")
        self._carry: Dict[str, bytes] = {}

    @classmethod
    def for_host(cls) -> "Redactor":
        try:
            return cls(getpass.getuser())
        except Exception:  # no login name available: nothing to redact
            return cls("")

    def status(self) -> str:
        if self.enabled:
            return "redacted as %s" % REDACTION_TOKEN
        return "not redacted (name too short)"

    def text(self, value: str) -> str:
        if not self.enabled:
            return value
        return value.replace(self.name, REDACTION_TOKEN)

    def obj(self, value: Any) -> Any:
        """Redact every string in a JSON-shaped value."""
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, dict):
            return {k: self.obj(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self.obj(v) for v in value]
        return value

    def chunk(self, key: str, data: bytes) -> bytes:
        if not self.enabled:
            return data
        buf = self._carry.pop(key, b"") + data
        buf = buf.replace(self._name_b, self._token_b)
        for k in range(min(len(self._name_b) - 1, len(buf)), 0, -1):
            if buf.endswith(self._name_b[:k]):
                self._carry[key] = buf[-k:]
                buf = buf[:-k]
                break
        return buf

    def flush(self) -> Dict[str, bytes]:
        carried, self._carry = self._carry, {}
        return carried


def _safe_text(data: bytes) -> Dict[str, Any]:
    """Encode arbitrary bytes for terminal.jsonl.

    Plain UTF-8 is recorded verbatim. Anything that does not round-trip
    UTF-8 cleanly is base64-encoded; reviewers can still reconstruct
    the byte stream without a separate raw recording. Each row carries
    the original byte length so a downstream consumer can verify it.
    """
    try:
        as_text = data.decode("utf-8")
    except UnicodeDecodeError:
        return {
            "enc": "b64",
            "data": base64.b64encode(data).decode("ascii"),
            "len": len(data),
        }
    return {"enc": "utf8", "data": as_text, "len": len(data)}


class Recorder:
    """Per-variant evidence writer.

    The Recorder is append-only and synchronous: each terminal chunk
    or event is fsynced-by-implication via the OS write buffer. v1
    does not promise crash-consistency.
    """

    def __init__(self, out_dir: str, redactor: Optional[Redactor] = None):
        os.makedirs(out_dir, exist_ok=True)
        self.redactor = redactor if redactor is not None else Redactor.for_host()
        self._last_ts = 0.0
        self.out_dir = out_dir
        self._terminal_path = os.path.join(out_dir, "terminal.jsonl")
        self._events_path = os.path.join(out_dir, "events.jsonl")
        self._terminal_fp = open(self._terminal_path, "w", encoding="utf-8")
        self._events_fp = open(self._events_path, "w", encoding="utf-8")
        self._closed = False

    def write_terminal(self, ts: float, direction: str, data: bytes) -> None:
        if self._closed:
            return
        self._last_ts = ts
        data = self.redactor.chunk(direction, data)
        if not data:
            return
        row = {"ts": round(ts, 6), "dir": direction}
        row.update(_safe_text(data))
        self._terminal_fp.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._terminal_fp.flush()

    def write_event(
        self,
        ts: float,
        kind: str,
        intent: str = "",
        screen_id: str = "",
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        if self._closed:
            return
        row = {
            "ts": round(ts, 6),
            "kind": kind,
            "intent": intent,
            "screen_id": screen_id,
            "payload": payload or {},
        }
        row = self.redactor.obj(row)
        self._events_fp.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._events_fp.flush()

    def write_summary(
        self,
        host_inputs: Dict[str, Any],
        run_meta: Dict[str, Any],
        outcome: Dict[str, Any],
        known_rough_edges: Iterable[Dict[str, str]],
        stage: str = "1",
        controlled_inputs: Optional[Dict[str, Any]] = None,
        error_signatures: Optional[List[Dict[str, str]]] = None,
        screen_heights: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        label = stage_label(stage)
        path = os.path.join(self.out_dir, "summary.md")
        with open(path, "w", encoding="utf-8") as fp:
            fp.write("---\n")
            fp.write("title: %s simulation summary\n" % label)
            fp.write("category: audit\n")
            fp.write("component: sim-%s\n" % stage_slug(stage))
            fp.write("status: evidence\n")
            fp.write(
                "version: %s\n" % HARNESS_VERSION,
            )
            fp.write(
                "last_updated: %s\n"
                % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
            )
            fp.write(
                "tags: [audit, simulation, %s, pty]\n"
                % ("all-stages" if stage == "all" else stage_slug(stage))
            )
            fp.write("priority: medium\n")
            fp.write("---\n\n")

            fp.write(
                "# %s — variant `%s`\n\n" % (label, run_meta.get("variant", ""))
            )
            fp.write(
                "Generated by `scripts/sim/run.py` (harness v%s), FF-006c of\n"
                "`docs/simulation-design-plan.md`.\n\n" % HARNESS_VERSION
            )

            fp.write("## Run metadata\n\n")
            for key in (
                "run_id",
                "persona",
                "stage",
                "variant",
                "started_at_utc",
                "duration_seconds",
                "harness_version",
                "shelltutor_path",
                "shelltutor_path_used",
                "bash_path",
                "bash_version",
                "sandbox_root",
                "pty_geometry",
                "per_sentinel_timeout_seconds",
            ):
                if key in run_meta:
                    fp.write("- %s: `%s`\n" % (key, run_meta[key]))
            fp.write("\n")

            fp.write("## Controlled inputs\n\n")
            fp.write(
                "Set by the harness for every run (decision D-03); everything\n"
                "else is inherited and listed under Host inputs.\n\n"
            )
            for key, val in (controlled_inputs or {}).items():
                fp.write("- %s: `%s`\n" % (key, val))
            fp.write("- host_user: `%s`\n" % self.redactor.status())
            fp.write("\n")

            fp.write("## Host inputs\n\n")
            fp.write(
                "The practice shell is project-controlled since Slice 2 (C-007); the\n"
                "host inputs below still reach the transcript.\n\n"
            )
            for key in (
                "term",
                "columns",
                "lines",
                "path_sha256_prefix",
                "python_version",
                "uname_system",
                "uname_release",
                "platform_machine",
            ):
                if key in host_inputs:
                    val = host_inputs[key]
                    val_str = "unset" if val is None else str(val)
                    fp.write("- %s: `%s`\n" % (key, val_str))
            fp.write("\n")

            fp.write("## Outcome\n\n")
            gate_passed = outcome.get("gate_passed", False)
            child_exit = outcome.get("child_exit_code")
            c002 = outcome.get("c002_meaning", "")
            fp.write("- gate_passed: `%s`\n" % str(gate_passed).lower())
            fp.write("- child_exit_code: `%s`\n" % child_exit)
            if c002:
                fp.write("- c002_meaning: `%s`\n" % c002)
            if "progress_after" in outcome:
                fp.write("- progress_after: `%s`\n" % outcome["progress_after"])
                fp.write(
                    "- progress_ok: `%s`\n" % str(outcome.get("progress_ok")).lower()
                )
            if "harness_exit_code" in outcome:
                fp.write("- harness_exit_code: `%s`\n" % outcome["harness_exit_code"])
            if "notes" in outcome and outcome["notes"]:
                fp.write("\n%s\n" % outcome["notes"])
            fp.write("\n")

            fp.write("## Error signatures observed\n\n")
            sigs = error_signatures or []
            if not sigs:
                fp.write("None.\n\n")
            else:
                fp.write(
                    "Mechanical scan of practice-shell output after persona input on\n"
                    "lesson screens (non-fatal; see `events.jsonl` `error-signature`).\n"
                    "Expected on the pre-fix script: F-010 (missing lesson fixture)\n"
                    "and F-011 (hardcoded `~/.shelltutor` path) in\n"
                    "`audit/2026-11-07/findings.md`.\n\n"
                )
                for sig in sigs:
                    fp.write(
                        "- **%s** (`%s`): `%s`\n"
                        % (sig["screen_id"], sig["intent"], sig["text"])
                    )
                fp.write("\n")

            if screen_heights:
                fp.write("## Screen heights\n\n")
                fp.write(
                    "Informational only (Q5): it changes neither the TAP result nor\n"
                    "any exit code. A screen starts at a clear sequence and ends at\n"
                    "the next practice prompt (or at the end of the run for the\n"
                    "finale). The count is the newline-terminated lines of normalised\n"
                    "output in between, so the blank line the screen helper adds and\n"
                    "the practice footer printed just before the prompt are included.\n"
                    "Logical lines are counted; a long line that wraps is one line.\n"
                    "Where one screen id has several clears (Ctrl+L, `clear`), the\n"
                    "largest is shown. Budget: 22 rendered lines before the prompt,\n"
                    "which equals the script's stated 20 content lines (heredoc 20 +\n"
                    "the blank line the screen helper adds + the practice footer), so\n"
                    "a 24-row terminal still shows the prompt. `Lines` is the raw\n"
                    "rendered count.\n\n"
                )
                fp.write("| Screen | Lines | Over budget |\n| --- | ---: | --- |\n")
                order: List[str] = []
                best: Dict[str, int] = {}
                budget = 22
                for row in screen_heights:
                    sid = str(row.get("screen_id") or "?")
                    budget = int(row.get("budget", budget))
                    if sid not in best:
                        order.append(sid)
                        best[sid] = 0
                    best[sid] = max(best[sid], int(row.get("lines", 0)))
                for sid in order:
                    fp.write(
                        "| %s | %d | %s |\n"
                        % (sid, best[sid], "yes" if best[sid] > budget else "no")
                    )
                fp.write("\n")

            fp.write("## Known rough edges labeled\n\n")
            fp.write(
                "Sourced from `audit/2026-05-23/stage1-density.md` — the audit\n"
                "ordering rule requires these be labeled (not pre-fixed) on the\n"
                "current-rc baseline. The IDs below are embedded in the per-event\n"
                "annotations in `events.jsonl`.\n\n"
            )
            if stage != "1":
                fp.write(
                    "No density audit is recorded for stages 2–5 yet.\n\n"
                    if stage in ("2", "3", "4", "5")
                    else "Stage 1 rows only; no density audit is recorded for stages 2–5 yet.\n\n"
                )
            for row in known_rough_edges:
                fp.write(
                    "- **%s** (%s): %s\n"
                    % (
                        row.get("id", "?"),
                        row.get("recommendation", "?"),
                        row.get("note", ""),
                    )
                )
            fp.write("\n")

            fp.write("## File index\n\n")
            fp.write(
                "- `terminal.jsonl` — chunk-level PTY stream (v1 project-local format).\n"
            )
            fp.write(
                "- `events.jsonl` — sentinel matches, persona inputs, gate result.\n"
            )
            fp.write("- `result.tap` — TAP 13 single-test outcome line.\n")
        self._redact_file(path)

    def _redact_file(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as fp:
            content = fp.read()
        redacted = self.redactor.text(content)
        if redacted != content:
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(redacted)

    def write_tap(
        self, ok: bool, description: str, skip_reason: Optional[str] = None
    ) -> None:
        path = os.path.join(self.out_dir, "result.tap")
        with open(path, "w", encoding="utf-8") as fp:
            fp.write("TAP version 13\n")
            fp.write("1..1\n")
            line = "%s 1 - %s" % ("ok" if ok else "not ok", description)
            if skip_reason:
                line += " # SKIP %s" % skip_reason
            fp.write(line + "\n")
        self._redact_file(path)

    def close(self) -> None:
        if not self._closed:
            # Partial-name suffixes held back at the end never completed
            # a name, so they are written unchanged.
            for direction, tail in self.redactor.flush().items():
                row = {"ts": round(self._last_ts, 6), "dir": direction}
                row.update(_safe_text(tail))
                self._terminal_fp.write(json.dumps(row, ensure_ascii=False) + "\n")
            self._closed = True
            try:
                self._terminal_fp.close()
            finally:
                self._events_fp.close()


def is_module(stage: str) -> bool:
    return stage.startswith("module:")


def stage_slug(stage: str) -> str:
    """Directory and tag form: `all`, `stage3` or `module-<name>`."""
    if stage == "all":
        return "all"
    if is_module(stage):
        return "module-" + stage[len("module:"):]
    return "stage" + stage


def stage_label(stage: str) -> str:
    if stage == "all":
        return "Five-stage baseline"
    if is_module(stage):
        return "Module %s baseline" % stage[len("module:"):]
    return "Stage %s baseline" % stage


def known_rough_edges(stage: str) -> List[Dict[str, str]]:
    """Per docs/simulation-design-plan.md §Evidence Bundle — labeled
    rough edges sourced from the SPLIT / SPLIT-or-TRIM rows of the
    Stage 1 density audit. Stages 2 to 5 have no density audit yet.
    """
    if stage not in ("1", "all"):
        return []
    return [
        {
            "id": "S1-L1",
            "recommendation": "resolved in WP-04",
            "note": (
                "Resolved in WP-04 (see `audit/2026-11-08/stage1-density-followup.md`): "
                "the old 1.1 split into 1.1 running commands and 1.2 keyboard habits."
            ),
        },
        {
            "id": "S1-L2",
            "recommendation": "resolved in WP-04",
            "note": (
                "Resolved in WP-04 (see `audit/2026-11-08/stage1-density-followup.md`): "
                "the identity lesson (now 1.3) dropped the `clear` block and softened "
                "the Stage 2 forward reference."
            ),
        },
        {
            "id": "S1-O",
            "recommendation": "keep with watch",
            "note": (
                "Orientation hits the 5-concept ceiling but is intrinsically a "
                "one-screen reference card. Watch baseline evidence before deciding "
                "to split."
            ),
        },
        {
            "id": "S1-L4",
            "recommendation": "keep with watch",
            "note": (
                "1.4 (formerly 1.3) concept density is high but action density is "
                "zero (read only). Risk: information overload after 1.2 and 1.3. "
                "Watch for long PTY pauses before deciding to split."
            ),
        },
    ]
