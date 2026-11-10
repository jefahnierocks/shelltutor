"""scripts/sim/childenv.py — the environment a harness child may inherit (H-4).

`run.py` and `sitting.py` both start the tutor under a pseudo-terminal. A
module's `env | head`, or a persona typing `env`, prints the practice shell's
whole environment into the transcript, so the child gets a short allowlist of
the caller's variables and nothing else; each caller then sets its own
(SHELLTUTOR_HOME, HOME, COLUMNS, ...). One constant here, so the two cannot
drift. Python 3.9+, standard library only.
"""

from __future__ import annotations

import os
from typing import Dict, Mapping, Optional

# The lessons use PATH; HOME is replaced by the caller; USER, LOGNAME and SHELL
# are what `env` and `echo $SHELL` show (the redactor replaces the login name in
# every bundle); TMPDIR and TERM keep the pseudo-terminal programs working.
ENV_PASSTHROUGH = ("PATH", "USER", "LOGNAME", "SHELL", "TMPDIR", "TERM")


def base_env(environ: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
    """The caller's allowlisted variables, and only those."""
    source = os.environ if environ is None else environ
    return {k: v for k, v in source.items() if k in ENV_PASSTHROUGH}
