#!/usr/bin/env python3
"""scripts/sim/run.py — Slice 1 dispatcher.

Drives the careful-beginner persona through Stage 1 of the tutor via
a Python stdlib PTY harness and writes a v1 evidence bundle per
variant. Optional contributor tooling — NOT part of `make verify`.

Usage examples:

    python3 scripts/sim/run.py
    python3 scripts/sim/run.py --variant current-rc
    python3 scripts/sim/run.py --variant no-system-rc-preview -v

Exit codes:

    0 — both variants green
    1 — uncaught exception (with traceback)
    2 — unsupported persona/stage/flag
    3 — PatchTargetMissingError
    4 — SentinelNotFoundError
    5 — PersonaRejectedError
    6 — NoTTYError
    7 — SandboxNotWritableError
"""

from __future__ import annotations

import argparse
import datetime
import difflib
import getpass
import json
import os
import secrets
import shutil
import sys
import time
import traceback
from typing import List, Optional, Tuple

# Allow running as `python3 scripts/sim/run.py` (no `-m`) by adding
# the parent of the package to sys.path.
_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(os.path.dirname(_HERE))
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from scripts.sim import driver, env, patcher, persona as persona_mod, recorder  # noqa: E402
from scripts.sim.errors import (  # noqa: E402
    NoTTYError,
    PatchTargetMissingError,
    PersonaRejectedError,
    SandboxNotWritableError,
    SentinelNotFoundError,
)

VARIANT_CURRENT = "current-rc"
VARIANT_PREVIEW = "no-system-rc-preview"
SUPPORTED_VARIANTS = (VARIANT_CURRENT, VARIANT_PREVIEW, "both")

C002_MEANING = {
    0: "next (lesson advance / stage cleared)",
    96: "check (gate verify)",
    97: "show (redisplay)",
    98: "prev (back one lesson)",
    99: "quit/exit (tutor exit, progress saved)",
}


def _utc_today() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def _parse_args(argv) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="scripts/sim/run.py",
        description=(
            "Slice 1 PTY harness for the shelltutor Stage 1 careful-beginner "
            "baseline. Writes a v1 evidence bundle per variant under --out."
        ),
    )
    parser.add_argument(
        "--variant",
        choices=SUPPORTED_VARIANTS,
        default="both",
    )
    parser.add_argument(
        "--persona",
        default="careful-beginner",
        help="Only careful-beginner is supported in Slice 1.",
    )
    parser.add_argument(
        "--stage",
        type=int,
        default=1,
        help="Only stage 1 is supported in Slice 1.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output directory. Defaults to audit/<UTC-date>/sim/stage1.",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--cols", type=int, default=80)
    parser.add_argument("--rows", type=int, default=24)
    parser.add_argument("--shelltutor", default="./shelltutor")
    parser.add_argument("--keep-sandbox", action="store_true")
    parser.add_argument("--keep-patched-script", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args(argv)


def _log(verbose: bool, msg: str) -> None:
    if verbose:
        print("sim: %s" % msg, file=sys.stderr)


def _run_variant(
    variant: str,
    shelltutor_path: str,
    out_dir: str,
    run_id: str,
    persona_name: str,
    args: argparse.Namespace,
) -> Tuple[recorder.Recorder, dict, dict, dict]:
    """Run a single variant. Returns (recorder, host_inputs, run_meta, outcome).

    The caller is responsible for closing the recorder.
    """
    variant_out = os.path.join(out_dir, variant)
    os.makedirs(variant_out, exist_ok=True)
    rec = recorder.Recorder(variant_out)

    host_inputs = env.host_snapshot()

    sandbox_root = env.make_shelltutor_home()
    _log(args.verbose, "variant=%s sandbox=%s" % (variant, sandbox_root))

    # Persona answers derived from harness host inputs.
    whoami_answer = getpass.getuser()
    pwd_answer = os.path.join(sandbox_root, "stage1")
    day_answer = time.strftime("%a")

    actions = persona_mod.careful_beginner_stage1(
        whoami_answer=whoami_answer,
        pwd_answer=pwd_answer,
        day_answer=day_answer,
    )
    p = persona_mod.Persona(persona_name, actions)

    started_at_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_meta = {
        "run_id": run_id,
        "persona": persona_name,
        "stage": args.stage,
        "variant": variant,
        "started_at_utc": started_at_utc,
        "harness_version": recorder.HARNESS_VERSION,
        "shelltutor_path": args.shelltutor,
        "shelltutor_path_used": shelltutor_path,
        "sandbox_root": sandbox_root,
        "pty_geometry": "%dx%d" % (args.cols, args.rows),
        "per_sentinel_timeout_seconds": args.timeout,
    }

    # Build child env: inherit, override SHELLTUTOR_HOME to the fresh
    # tempdir, set TERM if missing so terminal-aware code paths
    # (clear, ansi) work, force COLUMNS/LINES so the lesson's vertical-
    # budget assumptions hold.
    child_env = dict(os.environ)
    child_env["SHELLTUTOR_HOME"] = sandbox_root
    child_env.setdefault("TERM", "xterm-256color")
    child_env["COLUMNS"] = str(args.cols)
    child_env["LINES"] = str(args.rows)

    outcome: dict = {
        "gate_passed": False,
        "child_exit_code": None,
        "c002_meaning": "",
        "harness_exit_code": 1,
    }
    drive_exception: Optional[BaseException] = None
    result: Optional[dict] = None
    try:
        try:
            result = driver.drive(
                shelltutor_path=shelltutor_path,
                env=child_env,
                persona=p,
                recorder=rec,
                rows=args.rows,
                cols=args.cols,
                per_sentinel_timeout=args.timeout,
            )
        except (
            SentinelNotFoundError,
            PersonaRejectedError,
            NoTTYError,
        ) as exc:
            drive_exception = exc
    finally:
        if not args.keep_sandbox:
            shutil.rmtree(sandbox_root, ignore_errors=True)

    if result is not None:
        outcome["gate_passed"] = result["gate_passed"]
        outcome["child_exit_code"] = result["child_exit_code"]
        outcome["c002_meaning"] = C002_MEANING.get(
            result["child_exit_code"]
            if result["child_exit_code"] is not None
            else -1,
            "non-C-002 exit",
        )
        outcome["harness_exit_code"] = 0 if result["gate_passed"] else 4
        if result["wall_clock_capped"]:
            outcome["notes"] = "Run hit the 5-minute wall-clock cap."
        run_meta["duration_seconds"] = round(result["duration_seconds"], 3)
    elif drive_exception is not None:
        outcome["notes"] = (
            "Run aborted by %s: %s"
            % (drive_exception.__class__.__name__, drive_exception)
        )
        outcome["harness_exit_code"] = _exit_code_for(drive_exception)

    rec.write_summary(
        host_inputs=host_inputs,
        run_meta=run_meta,
        outcome=outcome,
        known_rough_edges=recorder.stage1_known_rough_edges(),
    )
    rec.write_tap(
        ok=outcome.get("gate_passed", False),
        description="stage1 careful-beginner — variant=%s" % variant,
    )
    if drive_exception is not None:
        # Re-raise so the dispatcher records the correct exit code,
        # but evidence for this variant has already been written.
        raise drive_exception
    return rec, host_inputs, run_meta, outcome


def _project_terminal_out(jsonl_path: str) -> List[str]:
    """Project a terminal.jsonl to the list of UTF-8 OUT-direction
    chunks, normalized for diff-readability.

    Normalization here is more aggressive than the sentinel-matching
    pass: CRLF→LF, bare CR→LF, and ANSI escape sequences stripped.
    The raw bytes still live in terminal.jsonl; this projection
    exists only to make the variant diff human-readable. Base64
    (`enc=b64`) rows are skipped — the Stage 1 transcript should not
    contain non-UTF-8 bytes; if a row is base64 it indicates a binary
    spill worth keeping in the raw file but pointless for the human
    diff.
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
            data = row.get("data", "")
            data = env.normalize(data)
            lines.append(data)
    return lines


def _write_diff(out_dir: str, current_dir: str, preview_dir: str) -> str:
    current_terminal = os.path.join(current_dir, "terminal.jsonl")
    preview_terminal = os.path.join(preview_dir, "terminal.jsonl")
    if not (os.path.exists(current_terminal) and os.path.exists(preview_terminal)):
        return ""
    current_text = "".join(_project_terminal_out(current_terminal)).splitlines(
        keepends=True
    )
    preview_text = "".join(_project_terminal_out(preview_terminal)).splitlines(
        keepends=True
    )
    diff_lines = list(
        difflib.unified_diff(
            current_text,
            preview_text,
            fromfile="current-rc/terminal.jsonl (out, normalized)",
            tofile="no-system-rc-preview/terminal.jsonl (out, normalized)",
            n=3,
        )
    )
    diff_path = os.path.join(out_dir, "diff.md")
    same = not diff_lines
    with open(diff_path, "w", encoding="utf-8") as fp:
        fp.write("---\n")
        fp.write("title: Stage 1 simulation — current-rc vs no-system-rc-preview\n")
        fp.write("category: audit\n")
        fp.write("component: stage1-sim\n")
        fp.write("status: evidence\n")
        fp.write("version: %s\n" % recorder.HARNESS_VERSION)
        fp.write("last_updated: %s\n" % _utc_today())
        fp.write("tags: [audit, simulation, stage1, diff]\n")
        fp.write("priority: medium\n")
        fp.write("---\n\n")
        fp.write("# Stage 1 baseline — variant diff\n\n")
        fp.write(
            "Unified diff of the OUT-direction UTF-8 chunks of each variant's\n"
            "`terminal.jsonl`, CRLF-normalized. Per\n"
            "`docs/simulation-design-plan.md` §Slice 1, this diff is the\n"
            "input to the Slice 2 hardening decision: the predicted\n"
            "divergence is the `/etc/bashrc` leak signature when the host\n"
            "rcfile injects banner output, aliases, or prompt-affecting state\n"
            "into the practice subshell.\n\n"
        )
        if same:
            fp.write(
                "**No textual divergence on this host.** The `/etc/bashrc` either\n"
                "did not exist or sourced no observable output into the practice\n"
                "subshell. Slice 2 still hardens by removing the source line so\n"
                "future hosts cannot inject behavior, but this host produced no\n"
                "leak signature to point at.\n"
            )
        else:
            fp.write("```diff\n")
            fp.write("".join(diff_lines))
            if not diff_lines[-1].endswith("\n"):
                fp.write("\n")
            fp.write("```\n")
    return diff_path


def _resolve_shelltutor(path: str) -> str:
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        raise SystemExit(
            "scripts/sim/run.py: --shelltutor path not found: %s" % abs_path
        )
    if not os.access(abs_path, os.X_OK):
        raise SystemExit(
            "scripts/sim/run.py: --shelltutor path not executable: %s" % abs_path
        )
    return abs_path


def _exit_code_for(exc: BaseException) -> int:
    if isinstance(exc, PatchTargetMissingError):
        return 3
    if isinstance(exc, SentinelNotFoundError):
        return 4
    if isinstance(exc, PersonaRejectedError):
        return 5
    if isinstance(exc, NoTTYError):
        return 6
    if isinstance(exc, SandboxNotWritableError):
        return 7
    return 1


def main(argv=None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    if args.persona != "careful-beginner":
        print(
            "scripts/sim/run.py: --persona %r unsupported; Slice 1 only "
            "supports careful-beginner." % args.persona,
            file=sys.stderr,
        )
        return 2
    if args.stage != 1:
        print(
            "scripts/sim/run.py: --stage %d unsupported; Slice 1 only "
            "supports stage 1." % args.stage,
            file=sys.stderr,
        )
        return 2

    out_dir = args.out or os.path.join("audit", _utc_today(), "sim", "stage1")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    real_shelltutor = _resolve_shelltutor(args.shelltutor)

    run_id = secrets.token_hex(4)
    _log(args.verbose, "run_id=%s out=%s" % (run_id, out_dir))

    variants_to_run: List[str]
    if args.variant == "both":
        variants_to_run = [VARIANT_CURRENT, VARIANT_PREVIEW]
    else:
        variants_to_run = [args.variant]

    aggregate_exit = 0
    preview_script_path = None
    try:
        for variant in variants_to_run:
            script_path: str
            if variant == VARIANT_CURRENT:
                script_path = real_shelltutor
            else:
                try:
                    preview_script_path = patcher.make_preview_copy(real_shelltutor)
                except PatchTargetMissingError as exc:
                    print(
                        "sim: PatchTargetMissingError (variant=%s): %s"
                        % (variant, exc),
                        file=sys.stderr,
                    )
                    aggregate_exit = max(aggregate_exit, _exit_code_for(exc))
                    continue
                script_path = preview_script_path
                _log(args.verbose, "preview script at %s" % script_path)

            rec = None
            try:
                try:
                    rec, _, _, outcome = _run_variant(
                        variant=variant,
                        shelltutor_path=script_path,
                        out_dir=out_dir,
                        run_id=run_id,
                        persona_name=args.persona,
                        args=args,
                    )
                    if not outcome.get("gate_passed"):
                        aggregate_exit = max(aggregate_exit, 4)
                        print(
                            "sim: variant=%s gate NOT passed (child_exit=%s)"
                            % (variant, outcome.get("child_exit_code")),
                            file=sys.stderr,
                        )
                    else:
                        _log(
                            args.verbose,
                            "variant=%s gate_passed=true child_exit=%s"
                            % (variant, outcome.get("child_exit_code")),
                        )
                except (
                    SentinelNotFoundError,
                    PersonaRejectedError,
                    NoTTYError,
                    SandboxNotWritableError,
                ) as exc:
                    # Per-variant evidence (summary.md, result.tap) was
                    # already written from inside _run_variant; the
                    # outer dispatcher records the worst exit and
                    # continues to the next variant.
                    print(
                        "sim: %s (variant=%s): %s"
                        % (exc.__class__.__name__, variant, exc),
                        file=sys.stderr,
                    )
                    aggregate_exit = max(aggregate_exit, _exit_code_for(exc))
            finally:
                if rec is not None:
                    rec.close()
                if (
                    variant == VARIANT_PREVIEW
                    and preview_script_path is not None
                    and not args.keep_patched_script
                ):
                    tmp_dir = os.path.dirname(preview_script_path)
                    shutil.rmtree(tmp_dir, ignore_errors=True)
                    preview_script_path = None

        if args.variant == "both":
            diff_path = _write_diff(
                out_dir,
                os.path.join(out_dir, VARIANT_CURRENT),
                os.path.join(out_dir, VARIANT_PREVIEW),
            )
            if diff_path:
                _log(args.verbose, "wrote %s" % diff_path)

    except SystemExit:
        raise
    except Exception:  # pragma: no cover — last-resort diagnostic
        traceback.print_exc()
        return 1
    finally:
        if (
            preview_script_path is not None
            and not args.keep_patched_script
        ):
            tmp_dir = os.path.dirname(preview_script_path)
            shutil.rmtree(tmp_dir, ignore_errors=True)

    return aggregate_exit


if __name__ == "__main__":
    raise SystemExit(main())
