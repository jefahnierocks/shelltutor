#!/usr/bin/env python3
"""scripts/sim/compare_heights.py — row counts per screen, two runs (A11).

Compares the "Screen | Lines" tables of two `summary.md` files (for example
a UTF-8 run and a `--ascii` run, or Bash 3.2 and 5.x) and exits 1 when any
screen has a different rendered row count or the two runs show different
screens. Python 3.9+, standard library only.

    python3 scripts/sim/compare_heights.py A/current-rc/summary.md B/current-rc/summary.md
"""

from __future__ import annotations

import re
import sys

ROW = re.compile(r"^\| (S[1-5]-\w+|M-\w+|FIN) \| (\d+) \|")


def heights(path: str) -> dict:
    out = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            m = ROW.match(line)
            if m:
                out[m.group(1)] = int(m.group(2))
    return out


def main(argv) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    a, b = heights(argv[1]), heights(argv[2])
    bad = [
        (sid, a.get(sid), b.get(sid))
        for sid in sorted(set(a) | set(b))
        if a.get(sid) != b.get(sid)
    ]
    for sid, x, y in bad:
        print("compare_heights: %s differs: %s vs %s" % (sid, x, y))
    if bad:
        return 1
    print("compare_heights: %d screens, identical row counts" % len(a))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
