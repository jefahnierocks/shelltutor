"""Generate the no-system-rc-preview script copy.

The preview is a temporary patched copy of the production script with
exactly one substitution applied: the literal `/etc/bashrc` source
statement is replaced with a provenance comment. The substitution is
exact-string (not regex), the needle must appear exactly once, and
the result is written to a tempdir with mode 0755.

Per docs/simulation-design-plan.md §Slice 1: do not add a fixed
line-number patch; do not add an environment-gated branch in the real
script. Fail loudly if the needle is missing.
"""

from __future__ import annotations

import os
import stat
import tempfile

from .errors import PatchTargetMissingError

PATCH_NEEDLE = "[ -r /etc/bashrc ] && . /etc/bashrc"
PATCH_REPLACEMENT = (
    "# shelltutor-sim: /etc/bashrc source disabled in no-system-rc-preview baseline"
)


def make_preview_copy(src_path: str, prefix: str = "shelltutor-sim-preview-") -> str:
    """Read src, substitute the exact /etc/bashrc source statement,
    write to a temp dir, chmod 0755, return path.

    Raises PatchTargetMissingError if the needle is absent or appears
    more than once.
    """
    with open(src_path, "r", encoding="utf-8") as src_file:
        original = src_file.read()

    count = original.count(PATCH_NEEDLE)
    if count != 1:
        raise PatchTargetMissingError(
            "expected exactly one occurrence of %r in %s; found %d"
            % (PATCH_NEEDLE, src_path, count)
        )

    patched = original.replace(PATCH_NEEDLE, PATCH_REPLACEMENT)

    dst_dir = tempfile.mkdtemp(prefix=prefix)
    dst_path = os.path.join(dst_dir, os.path.basename(src_path))
    with open(dst_path, "w", encoding="utf-8") as dst_file:
        dst_file.write(patched)
    # 0755: rwxr-xr-x — same permission shape as the production script.
    os.chmod(
        dst_path,
        stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
    )
    return dst_path
