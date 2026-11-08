#!/usr/bin/env python3
"""scripts/sim/run.py — PTY harness dispatcher (FF-006c rung 1).

Drives the careful-beginner persona through one stage, or all five
stages, of the tutor via a Python stdlib PTY harness and writes a v1
evidence bundle per variant. Optional contributor tooling — NOT part
of `make verify`.

Usage examples:

    python3 scripts/sim/run.py
    python3 scripts/sim/run.py --stage all
    python3 scripts/sim/run.py --stage 3 --variant current-rc
    python3 scripts/sim/run.py --variant no-system-rc-preview -v

Exit codes:

    0 — every requested variant green
    1 — uncaught exception (with traceback)
    2 — unsupported persona/stage/flag
    3 — PatchTargetMissingError
    4 — SentinelNotFoundError
    5 — PersonaRejectedError
    6 — NoTTYError
    7 — SandboxNotWritableError
    8 — PrerequisiteMissingError (vim absent for --stage 5/all)
"""

from __future__ import annotations

import argparse
import datetime
import difflib
import getpass
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
    PrerequisiteMissingError,
    SandboxNotWritableError,
    SentinelNotFoundError,
)
from scripts.sim.project import project_terminal_out  # noqa: E402

SUPPORTED_STAGES = ("1", "2", "3", "4", "5", "all")

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
            "PTY harness for the shelltutor careful-beginner baseline "
            "(one stage or all five). Writes a v1 evidence bundle per "
            "variant under --out."
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
        help="Only careful-beginner is supported.",
    )
    parser.add_argument(
        "--stage",
        choices=SUPPORTED_STAGES,
        default="1",
        help="Stage to drive: 1-5 or all (default: 1).",
    )
    parser.add_argument(
        "--out",
        default=None,
        help=(
            "Output directory. Defaults to audit/<UTC-date>/sim/stage<N> "
            "or audit/<UTC-date>/sim/all."
        ),
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


def _repo_relative(path: str, fallback: str) -> str:
    """Record paths relative to the repository root, never absolute (D-15)."""
    abs_path = os.path.abspath(path)
    if abs_path == _PARENT or abs_path.startswith(_PARENT + os.sep):
        return os.path.relpath(abs_path, _PARENT)
    return fallback


def _build_actions(
    stage: str, whoami_answer: str, pwd_answer: str, day_answer: str
) -> List[persona_mod.Action]:
    if stage == "1":
        return persona_mod.careful_beginner_stage1(
            whoami_answer=whoami_answer,
            pwd_answer=pwd_answer,
            day_answer=day_answer,
        )
    raise SystemExit(
        "scripts/sim/run.py: --stage %s walk not available yet" % stage
    )


def _final_gate_id(stage: str) -> str:
    return "STAGE_CLEARED" if stage == "1" else "S%s_CLEARED" % stage


def _child_args(stage: str) -> List[str]:
    # C-001: `shelltutor N` for N >= 2; no argument for stage 1 and all.
    return [stage] if stage in ("2", "3", "4", "5") else []


def _read_progress(sandbox_root: str) -> str:
    path = os.path.join(sandbox_root, ".progress")
    try:
        with open(path, "r", encoding="utf-8") as fp:
            return fp.read().strip() or "empty"
    except FileNotFoundError:
        return "absent"
    except OSError:
        return "unreadable"


def _expected_progress(stage: str) -> str:
    # `all` and `5` both run the finale, which removes .progress.
    return stage if stage in ("1", "2", "3", "4") else "absent"


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
    # Clean learner account: an empty per-run HOME so a pre-existing
    # ~/.shelltutor (or any dotfile) on the host cannot hide defects.
    user_home = env.make_shelltutor_home(prefix="shelltutor-sim-userhome-")
    _log(args.verbose, "variant=%s sandbox=%s" % (variant, sandbox_root))

    # Persona answers derived from harness host inputs.
    whoami_answer = getpass.getuser()
    pwd_answer = os.path.join(sandbox_root, "stage1")
    day_answer = time.strftime("%a")

    actions = _build_actions(args.stage, whoami_answer, pwd_answer, day_answer)
    p = persona_mod.Persona(persona_name, actions)

    started_at_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_meta = {
        "run_id": run_id,
        "persona": persona_name,
        "stage": args.stage,
        "variant": variant,
        "started_at_utc": started_at_utc,
        "harness_version": recorder.HARNESS_VERSION,
        "shelltutor_path": _repo_relative(args.shelltutor, "shelltutor"),
        "shelltutor_path_used": _repo_relative(
            shelltutor_path, "shelltutor (%s patched copy)" % variant
        ),
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
    child_env["HOME"] = user_home
    child_env.setdefault("TERM", "xterm-256color")
    child_env["COLUMNS"] = str(args.cols)
    child_env["LINES"] = str(args.rows)
    # D-03 controlled inputs.
    child_env["LC_ALL"] = "C"
    child_env["VIMINIT"] = "set nocompatible"
    child_env["PAGER"] = "less"
    child_env.pop("MANPAGER", None)
    child_env.pop("LESS", None)
    controlled_inputs = {
        "HOME": "empty per-run tempdir",
        "LC_ALL": "C",
        "VIMINIT": "set nocompatible",
        "PAGER": "less",
        "MANPAGER": "unset",
        "LESS": "unset",
        "TERM": child_env["TERM"],
        "COLUMNS": args.cols,
        "LINES": args.rows,
    }

    outcome: dict = {
        "gate_passed": False,
        "child_exit_code": None,
        "c002_meaning": "",
        "harness_exit_code": 1,
        "progress_after": "n/a",
        "progress_ok": False,
    }
    error_signatures: List[dict] = []
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
                child_args=_child_args(args.stage),
                final_gate_id=_final_gate_id(args.stage),
                display_path=run_meta["shelltutor_path_used"],
            )
        except (
            SentinelNotFoundError,
            PersonaRejectedError,
            NoTTYError,
        ) as exc:
            drive_exception = exc
        # Read before sandbox cleanup.
        outcome["progress_after"] = _read_progress(sandbox_root)
        outcome["progress_ok"] = outcome["progress_after"] == _expected_progress(
            args.stage
        )
    finally:
        if not args.keep_sandbox:
            shutil.rmtree(sandbox_root, ignore_errors=True)
            shutil.rmtree(user_home, ignore_errors=True)

    if result is not None:
        outcome["gate_passed"] = result["gate_passed"]
        outcome["child_exit_code"] = result["child_exit_code"]
        outcome["c002_meaning"] = C002_MEANING.get(
            result["child_exit_code"]
            if result["child_exit_code"] is not None
            else -1,
            "non-C-002 exit",
        )
        error_signatures = result["error_signatures"]
        run_ok = result["gate_passed"] and outcome["progress_ok"]
        outcome["harness_exit_code"] = 0 if run_ok else 4
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
        known_rough_edges=recorder.known_rough_edges(args.stage),
        stage=args.stage,
        controlled_inputs=controlled_inputs,
        error_signatures=error_signatures,
    )
    outcome["ok"] = bool(outcome["gate_passed"] and outcome["progress_ok"])
    rec.write_tap(
        ok=outcome["ok"],
        description="%s careful-beginner — variant=%s"
        % (
            "all-stages" if args.stage == "all" else "stage" + args.stage,
            variant,
        ),
    )
    if drive_exception is not None:
        # Re-raise so the dispatcher records the correct exit code,
        # but evidence for this variant has already been written.
        raise drive_exception
    return rec, host_inputs, run_meta, outcome


def _write_diff(
    out_dir: str, current_dir: str, preview_dir: str, stage: str = "1"
) -> str:
    stage_name = "all-stages" if stage == "all" else "stage" + stage
    stage_title = "Five-stage" if stage == "all" else "Stage %s" % stage
    current_terminal = os.path.join(current_dir, "terminal.jsonl")
    preview_terminal = os.path.join(preview_dir, "terminal.jsonl")
    if not (os.path.exists(current_terminal) and os.path.exists(preview_terminal)):
        return ""
    current_text = "".join(project_terminal_out(current_terminal)).splitlines(
        keepends=True
    )
    preview_text = "".join(project_terminal_out(preview_terminal)).splitlines(
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
        fp.write(
            "title: %s simulation — current-rc vs no-system-rc-preview\n"
            % stage_title
        )
        fp.write("category: audit\n")
        fp.write("component: sim-%s\n" % stage_name)
        fp.write("status: evidence\n")
        fp.write("version: %s\n" % recorder.HARNESS_VERSION)
        fp.write("last_updated: %s\n" % _utc_today())
        fp.write("tags: [audit, simulation, %s, diff]\n" % stage_name)
        fp.write("priority: medium\n")
        fp.write("---\n\n")
        fp.write("# %s baseline — variant diff\n\n" % stage_title)
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


def _write_skip(out_dir: str, variant: str, args, reason: str) -> None:
    """Record a prerequisite skip: summary note plus `# SKIP` TAP line."""
    rec = recorder.Recorder(os.path.join(out_dir, variant))
    try:
        rec.write_summary(
            host_inputs=env.host_snapshot(),
            run_meta={
                "persona": args.persona,
                "stage": args.stage,
                "variant": variant,
                "harness_version": recorder.HARNESS_VERSION,
            },
            outcome={
                "gate_passed": False,
                "child_exit_code": None,
                "harness_exit_code": 8,
                "notes": "SKIPPED: %s (PrerequisiteMissingError, exit 8)." % reason,
            },
            known_rough_edges=[],
            stage=args.stage,
            controlled_inputs={},
            error_signatures=[],
        )
        rec.write_tap(
            ok=True,
            description="%s careful-beginner — variant=%s"
            % ("all-stages" if args.stage == "all" else "stage" + args.stage, variant),
            skip_reason=reason,
        )
    finally:
        rec.close()


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
    if isinstance(exc, PrerequisiteMissingError):
        return 8
    return 1


def main(argv=None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])

    if args.persona != "careful-beginner":
        print(
            "scripts/sim/run.py: --persona %r unsupported; only "
            "careful-beginner is available." % args.persona,
            file=sys.stderr,
        )
        return 2

    stage_dir = "all" if args.stage == "all" else "stage" + args.stage
    out_dir = args.out or os.path.join("audit", _utc_today(), "sim", stage_dir)
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

    if args.stage in ("5", "all") and shutil.which("vim") is None:
        exc = PrerequisiteMissingError("vim not installed")
        for variant in variants_to_run:
            _write_skip(out_dir, variant, args, "vim not installed")
        print("sim: PrerequisiteMissingError: %s" % exc, file=sys.stderr)
        return 8

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
                    if not outcome.get("ok"):
                        aggregate_exit = max(aggregate_exit, 4)
                        print(
                            "sim: variant=%s NOT ok (gate_passed=%s "
                            "progress_after=%s child_exit=%s)"
                            % (
                                variant,
                                outcome.get("gate_passed"),
                                outcome.get("progress_after"),
                                outcome.get("child_exit_code"),
                            ),
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
                args.stage,
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
