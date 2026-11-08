#!/usr/bin/env python3
"""scripts/sim/compare.py — diff two evidence bundles.

Usage:

    python3 scripts/sim/compare.py BUNDLE_A BUNDLE_B

Each argument is a bundle directory containing `terminal.jsonl` (for
example `audit/<date>/sim/all/current-rc`). Prints a unified diff of
the normalized OUT projection (CRLF-normalized, ANSI stripped) of the
two bundles. Used for before/after comparisons across work packages.

Exit codes:

    0 — projections identical
    1 — projections differ
    2 — usage error or missing terminal.jsonl
"""

from __future__ import annotations

import difflib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(os.path.dirname(_HERE))
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from scripts.sim.project import project_terminal_out  # noqa: E402


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("usage: scripts/sim/compare.py BUNDLE_A BUNDLE_B", file=sys.stderr)
        return 2
    paths = []
    for bundle in argv:
        terminal = os.path.join(bundle, "terminal.jsonl")
        if not os.path.isfile(terminal):
            print("compare: no terminal.jsonl in %s" % bundle, file=sys.stderr)
            return 2
        paths.append(terminal)
    a = "".join(project_terminal_out(paths[0])).splitlines(keepends=True)
    b = "".join(project_terminal_out(paths[1])).splitlines(keepends=True)
    diff = list(
        difflib.unified_diff(
            a,
            b,
            fromfile="%s (out, normalized)" % argv[0],
            tofile="%s (out, normalized)" % argv[1],
            n=3,
        )
    )
    if not diff:
        print("compare: no textual divergence")
        return 0
    sys.stdout.write("".join(diff))
    if not diff[-1].endswith("\n"):
        sys.stdout.write("\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
