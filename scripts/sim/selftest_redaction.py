#!/usr/bin/env python3
"""scripts/sim/selftest_redaction.py — D-19: the login name never reaches a bundle.

A module's `env | head` prints `USER=<login>` and `LOGNAME=<login>` into the
terminal stream. This feeds a Recorder those lines in the shapes a real run
produces (one chunk, a name split across two chunks, a non-UTF-8 chunk, an
event payload, a text file written afterwards) and fails if the name survives
anywhere in the output directory. Python 3.9+, standard library only.
"""

from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts.sim import recorder as R  # noqa: E402

NAME = "alice77"


def main() -> int:
    out = tempfile.mkdtemp(prefix="selftest-redaction-")
    rec = R.Recorder(out, R.Redactor(NAME))
    rec.write_terminal(0.1, "out", ("USER=%s\r\nLOGNAME=%s\r\n" % (NAME, NAME)).encode())
    rec.write_terminal(0.2, "out", b"HOME=/Users/ali")
    rec.write_terminal(0.3, "out", b"ce77/work\r\nUSER=ali")
    rec.write_terminal(0.4, "out", b"ce77\r\n")
    rec.write_terminal(0.5, "out", b"\xff\xfe USER=" + NAME.encode() + b" \xff")
    rec.write_event(0.6, "sentinel-matched", intent="x", screen_id="M-L1",
                    payload={"echo": "LOGNAME=%s" % NAME, "nested": [NAME]})
    rec.close()
    side = os.path.join(out, "side.md")
    with open(side, "w", encoding="utf-8") as fp:
        fp.write("owner: %s\n" % NAME)
    rec._redact_file(side)
    left = []
    token = 0
    for root, _, files in os.walk(out):
        for f in files:
            data = open(os.path.join(root, f), "rb").read()
            if NAME.encode() in data:
                left.append(f)
            token += data.count(R.REDACTION_TOKEN.encode())
    # base64 rows hide the bytes; decode them too
    import base64, json
    for line in open(os.path.join(out, "terminal.jsonl"), encoding="utf-8"):
        row = json.loads(line)
        if row.get("enc") == "b64" and NAME.encode() in base64.b64decode(row["data"]):
            left.append("terminal.jsonl (b64 row)")
    if left or not token:
        print("FAIL: login name survives in %s (token count %d)" % (sorted(set(left)), token))
        return 1
    print("selftest_redaction: all checks passed (%d redactions)" % token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
