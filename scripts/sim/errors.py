"""Harness exception classes.

Each class maps to an exit code defined in run.py. The mapping is
documented in scripts/sim/README.md so contributors do not have to
read the dispatcher to learn what a non-zero exit means.
"""


class HarnessError(Exception):
    """Base class for all harness-side failures."""


class HarnessTimeoutError(HarnessError):
    """Wall-clock or per-sentinel timeout. Surfaced as SentinelNotFound."""


class SentinelNotFoundError(HarnessError):
    """A sentinel did not appear before its timeout.

    The driver attaches the trailing normalized buffer as diagnostic
    so reviewers do not need to replay the run to see what the tutor
    was rendering at the moment of failure.
    """

    def __init__(self, sentinel_id, pattern, tail):
        super().__init__(
            "sentinel %r (pattern %r) not seen; tail=%r"
            % (sentinel_id, pattern, tail)
        )
        self.sentinel_id = sentinel_id
        self.pattern = pattern
        self.tail = tail


class PatchTargetMissingError(HarnessError):
    """no-system-rc-preview substitution target was absent or non-unique."""


class NoTTYError(HarnessError):
    """PTY allocation failed."""


class SandboxNotWritableError(HarnessError):
    """SHELLTUTOR_HOME tempdir could not be created or written to."""


class PersonaRejectedError(HarnessError):
    """A persona action was refused by the tutor (e.g., gate re-asked a
    question). The persona is dispatch-deterministic; a re-fire of a
    previously-matched sentinel means the answer was rejected.
    """
