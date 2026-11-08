"""Shared projection of a terminal.jsonl bundle file.

Used by run.py (variant diff) and compare.py (before/after diff).
"""

from __future__ import annotations

import json
from typing import List

from . import env


def project_terminal_out(jsonl_path: str) -> List[str]:
    """Project a terminal.jsonl to the list of UTF-8 OUT-direction
    chunks, normalized for diff-readability.

    Normalization here is more aggressive than the sentinel-matching
    pass: CRLF→LF, bare CR→LF, and ANSI escape sequences stripped.
    The raw bytes still live in terminal.jsonl; this projection
    exists only to make diffs human-readable. Base64 (`enc=b64`) rows
    are skipped — they indicate a binary spill worth keeping in the raw
    file but pointless for a human diff.
    """
    lines: List[str] = []
    with open(jsonl_path, "r", encoding="utf-8") as fp:
        for raw in fp:
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if row.get("dir") != "out":
                continue
            if row.get("enc") != "utf8":
                continue
            lines.append(env.normalize(row.get("data", "")))
    return lines
