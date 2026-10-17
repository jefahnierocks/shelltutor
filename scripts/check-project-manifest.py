"""Shelltutor's offline Release 1 binding; never a learner dependency."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "56e3920089726e585eaa0fd7f4dc94e6938a1e0c"
TABLE_DIGEST = "f7ff9dd0972af5d3a6a3348c3e092de1a6acd97fa3975e13e522cf80ce5e7df2"
BOOTSTRAP_DIGEST = "2ccf58e0da97bbbd9dae173d1cca047d465c4a2d950ee6e56052309a9689cf4f"
BINDING_FORMAT = "project-manifest-release-1"
PROTOCOL = "project-manifest-git-observation-1"
NAMESPACE = "_shelltutor_project_manifest"
RUNTIME_MODULES = ("candidate", "validation", "acquire")
MAX_FILE_BYTES = 1_048_576


class Refused(Exception):
    def __init__(self, code, exit_code=2):
        self.code, self.exit_code = code, exit_code


def require(condition, code, exit_code=2):
    if not condition:
        raise Refused(code, exit_code)


def identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def capture(path):
    """Bounded no-follow read, including every directory component."""
    path = Path(path)
    require(path.is_absolute() and ".." not in path.parts, "SOURCE_PATH")
    parent = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    descriptor = None
    try:
        for part in path.parts[1:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=parent)
            previous, parent = parent, child
            os.close(previous)
        descriptor = os.open(path.name, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW,
                             dir_fd=parent)
        before = os.fstat(descriptor)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                and before.st_size <= MAX_FILE_BYTES, "SOURCE_FILE")
        chunks, count = [], 0
        while True:
            chunk = os.read(descriptor, min(65_536, MAX_FILE_BYTES + 1 - count))
            if not chunk:
                break
            chunks.append(chunk)
            count += len(chunk)
            require(count <= MAX_FILE_BYTES, "SOURCE_BOUND")
        require(count == before.st_size and identity(before) == identity(os.fstat(descriptor))
                == identity(os.stat(path.name, dir_fd=parent, follow_symlinks=False)),
                "SOURCE_CHANGED")
        return b"".join(chunks)
    finally:
        try:
            if descriptor is not None:
                os.close(descriptor)
        finally:
            os.close(parent)


def execute_module(name, data, filename, *, package=False):
    require(name not in sys.modules, "MODULE_COLLISION")
    module = ModuleType(name)
    module.__file__ = str(filename)
    module.__package__ = name if package else name.rpartition(".")[0]
    if package:
        module.__path__ = []
    sys.modules[name] = module
    try:
        exec(compile(data, str(filename), "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


@contextmanager
def released_api(root):
    """Import only captured bytes from an independently pinned public release."""
    root = Path(root)
    bootstrap_path = root / "vendor/project-manifest/release_verifier.py"
    bundle = root / "vendor/project-manifest/release-1"
    bootstrap_data = capture(bootstrap_path)
    require(hashlib.sha256(bootstrap_data).hexdigest() == BOOTSTRAP_DIGEST,
            "BOOTSTRAP_DIGEST", 1)
    loaded = []
    try:
        verifier_name = NAMESPACE + "_bootstrap"
        verifier = execute_module(verifier_name, bootstrap_data, bootstrap_path)
        loaded.append(verifier_name)
        verified = verifier.verify_release(str(bundle), expected_digest=TABLE_DIGEST,
                                           expected_format=BINDING_FORMAT)
        require(verified.exit_code == 0, "RELEASE_BINDING", verified.exit_code)
        descriptor = verified.descriptor
        require(descriptor["source_revision"] == SOURCE
                and descriptor["observation_protocol"] == PROTOCOL,
                "RELEASE_IDENTITY", 1)
        rows = {row["path"]: row for row in descriptor["files"]}
        captured = {}
        for name in RUNTIME_MODULES:
            path = "src/project_manifest/" + name + ".py"
            data = capture(bundle / path)
            require(len(data) == rows[path]["bytes"]
                    and hashlib.sha256(data).hexdigest() == rows[path]["sha256"],
                    "PAYLOAD_CHANGED", 1)
            captured[name] = data
        execute_module(NAMESPACE, b"", bundle / "src/project_manifest", package=True)
        loaded.append(NAMESPACE)
        for name, data in captured.items():
            full_name = NAMESPACE + "." + name
            execute_module(full_name, data, bundle / "src/project_manifest" / (name + ".py"))
            loaded.append(full_name)
        yield sys.modules[NAMESPACE + ".acquire"]
        require(capture(bootstrap_path) == bootstrap_data, "BOOTSTRAP_CHANGED", 1)
        repeated = verifier.verify_release(str(bundle), expected_digest=TABLE_DIGEST,
                                           expected_format=BINDING_FORMAT)
        require(repeated.exit_code == 0 and repeated.descriptor == descriptor,
                "RELEASE_CHANGED", 1)
    finally:
        for name in reversed(loaded):
            sys.modules.pop(name, None)


def native_shape(record):
    """Match this repo's declared entrypoint; this does not execute native checks."""
    expected = {role: None for role in
                ("setup", "check", "test", "build", "dev", "format_check", "format_write")}
    expected["check"] = {"runner": "script", "target": "scripts/verify-project.sh"}
    development = record["development"]
    return (development["commands"] == expected
            and development["environment"] == {
                "owner": "none", "template": None, "secret_launcher": None}
            and development["stacks"] == {} and development["host_requirements"] == [])


def check(root, *, mode="worktree", rev=None, common_dir=None):
    require(sys.version_info >= (3, 11) and sys.flags.isolated
            and sys.flags.no_site and sys.dont_write_bytecode, "PYTHON_RUNTIME")
    require(mode in {"worktree", "staged", "rev"}, "SOURCE_SELECTION")
    require((mode == "rev" and isinstance(rev, str)
             and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", rev))
            or (mode != "rev" and rev is None), "SOURCE_SELECTION")
    day = datetime.now(timezone.utc).date().isoformat()
    with released_api(root) as api:
        result = api.observe_released_repository(str(root), mode=mode, rev=rev,
                                                common_dir=common_dir, reference_date=day)
        require(result.diagnostics.get("scope") == PROTOCOL, "OBSERVATION_PROTOCOL")
        report = dict(result.diagnostics)
        report.update(consumer="shelltutor", release_id="1", release_source=SOURCE,
                      release_table_digest=TABLE_DIGEST, native_contract="not_checked",
                      native_gate="not_checked", runtime_acceptance="not_checked")
        if result.exit_code == 0:
            require(mode != "rev" or report["commit_oid"] == rev, "REVISION_CHANGED")
            matched = native_shape(result.record)
            report["native_contract"] = "matched" if matched else "mismatch"
            if not matched:
                report["exit_code"] = 1
                report["consumer_findings"] = ["NATIVE_DECLARATION_MISMATCH"]
        return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--staged", action="store_true")
    selection.add_argument("--rev")
    parser.add_argument("--git-common-dir", default=os.environ.get("SHELLTUTOR_GIT_COMMON_DIR"))
    args = parser.parse_args(argv)
    try:
        environment_rev = os.environ.get("SHELLTUTOR_MANIFEST_REV")
        require(not (args.staged and environment_rev), "SOURCE_SELECTION")
        require(not (args.rev and environment_rev and args.rev != environment_rev), "SOURCE_SELECTION")
        rev = args.rev or environment_rev or None
        mode = "staged" if args.staged else "rev" if rev else "worktree"
        report = check(ROOT, mode=mode, rev=rev, common_dir=args.git_common_dir)
    except Refused as error:
        report = {"consumer": "shelltutor", "exit_code": error.exit_code,
                  "declaration_checks": "not_checked", "consumer_findings": [error.code]}
    except (OSError, ValueError, TypeError, KeyError, RuntimeError, RecursionError):
        report = {"consumer": "shelltutor", "exit_code": 2,
                  "declaration_checks": "not_checked", "consumer_findings": ["CONSUMER_UNAVAILABLE"]}
    print(json.dumps(report, sort_keys=True))
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
