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
    python3 scripts/sim/run.py --stage all -v

Exit codes:

    0 — every requested variant green
    1 — uncaught exception (with traceback)
    2 — unsupported persona/stage/flag
    3 — retired (Slice 2; formerly PatchTargetMissingError)
    4 — SentinelNotFoundError
    5 — PersonaRejectedError
    6 — NoTTYError
    7 — SandboxNotWritableError
    8 — PrerequisiteMissingError (vim absent for --stage 5/all)
"""

from __future__ import annotations

import argparse
import datetime
import getpass
import os
import re
import secrets
import shutil
import subprocess
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

from scripts.sim import childenv, driver, env, persona as persona_mod, recorder  # noqa: E402
from scripts.sim.project import project_terminal_out  # noqa: E402
from scripts.sim.errors import (  # noqa: E402
    NoTTYError,
    PersonaRejectedError,
    PrerequisiteMissingError,
    SandboxNotWritableError,
    SentinelNotFoundError,
)

SUPPORTED_STAGES = ("1", "2", "3", "4", "5", "all")
SUPPORTED_PERSONAS = ("careful-beginner", "second-try")
# second-try fails the first gate check on purpose; only the Stage 2 and
# Stage 4 gates have a history check to trip (WP-05, decision D-14).
SECOND_TRY_STAGES = ("2", "4")
NOT_YET_TEXT = "seen: "
# Rendered-row ceilings above SCREEN_BUDGET: the welcome box (A12, 22 allowed;
# it is 21).
HEIGHT_ALLOWED = {"S1-W": 21}
# Recall ladder (A7, kept by A11). second-try at Stage 2 misses Q1 twice:
# miss 1 prints "not quite. hint: ...", miss 2 the same line plus the
# navigation facts, so "hint:" appears twice and the first navigation fact
# once. The task ladder keeps its own "Hint:" (capital), which is not counted.
RECALL_HINT_TEXT = "hint:"
RECALL_NAV_TEXT = "Passed stages are saved."
# A9 (F-022): the Stage 2 gate's first check prints both items.
# second-try makes the folder and skips the cd, so the first check shows the
# folder item done (no "seen:" reason) and the cd item todo.
GATE_CLOSE_TEXT = "Finish the step marked [ ]"
GATE_ITEM_FOLDER_TEXT = "seen: no practice folder"
GATE_ITEM_CD_TEXT = "seen: no cd in your history"
RECALL_EXPECTED = {"2": (2, 1), "4": (0, 0)}

VARIANT_CURRENT = "current-rc"
# Retired in Slice 2: the practice shell no longer sources the system
# bashrc, so there is nothing for the preview variant to isolate. The
# names stay accepted by argparse only to print the retirement message.
RETIRED_VARIANTS = ("no-system-rc-preview", "both")
RETIRED_VARIANT_MESSAGE = (
    "scripts/sim/run.py: variant retired in Slice 2 (practice shell no "
    "longer sources /etc/bashrc); use --variant current-rc"
)

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
        choices=(VARIANT_CURRENT,) + RETIRED_VARIANTS,
        default=VARIANT_CURRENT,
        help="Only current-rc is supported (the preview variant was retired in Slice 2).",
    )
    parser.add_argument(
        "--persona",
        default="careful-beginner",
        help=(
            "careful-beginner (any stage) or second-try (--stage 2 or 4 "
            "only; fails the first gate check on purpose)."
        ),
    )
    parser.add_argument(
        "--stage",
        choices=SUPPORTED_STAGES,
        default=None,
        help="Stage to drive: 1-5 or all (default: 1). Exclusive with --module.",
    )
    parser.add_argument(
        "--module",
        default=None,
        help=(
            "Drive a stand-alone module by name from its persona table "
            "(exclusive with --stage)."
        ),
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
    parser.add_argument(
        "--ascii",
        action="store_true",
        help=(
            "Run the tutor with SHELLTUTOR_ASCII=1 (the width-stable ASCII "
            "glyph set, A11). Same walk, same row counts."
        ),
    )
    parser.add_argument("--keep-sandbox", action="store_true")
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


def _bash_provenance():
    """Path and version of the `bash` the tutor will run under.

    The tutor's shebang resolves `bash` through the child's PATH, and the
    practice shell is the same binary (F-014), so one lookup under that
    PATH identifies both. A path under the operator's home is recorded
    with a leading `~` so evidence never carries a home directory (D-15).
    """
    path = shutil.which("bash", path=os.environ.get("PATH"))
    if not path:
        return "not found", "unknown"
    try:
        proc = subprocess.run(
            [path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            universal_newlines=True, timeout=10,
        )
        version = (proc.stdout.splitlines() or ["unknown"])[0]
    except (OSError, subprocess.SubprocessError):
        version = "unknown"
    home = os.path.expanduser("~")
    if home and home != "~" and path.startswith(home + os.sep):
        path = "~" + path[len(home):]
    return path, version


def _build_actions(
    stage: str,
    whoami_answer: str,
    pwd_answer: str,
    day_answer: str,
    sandbox_root: str,
    persona_name: str = "careful-beginner",
) -> List[persona_mod.Action]:
    if recorder.is_module(stage):
        name = stage[len("module:"):]
        table = persona_mod.MODULE_TABLES[name]
        return persona_mod.module_walk(
            name,
            table["lessons"],
            table["gate"],
            lesson_actions=table.get("lesson_actions"),
            prompt_after=table.get("prompt_after"),
            prompt_before_next=table.get("prompt_before_next"),
            lesson_prompts=table.get("lesson_prompts"),
        )
    return persona_mod.build_walk(
        stage,
        whoami_answer=whoami_answer,
        pwd_answer=pwd_answer,
        day_answer=day_answer,
        man_available=shutil.which("man") is not None,
        sandbox_root=sandbox_root,
        persona=persona_name,
    )


def _final_gate_id(stage: str) -> str:
    if recorder.is_module(stage):
        return "%s cleared." % stage[len("module:"):]
    if stage == "1":
        return "STAGE_CLEARED"
    return "S5_CLEARED" if stage == "all" else "S%s_CLEARED" % stage


def _child_args(stage: str) -> List[str]:
    # C-001: `shelltutor N` for N >= 2; `shelltutor <name>` for a module;
    # no argument for stage 1 and all.
    if recorder.is_module(stage):
        return [stage[len("module:"):]]
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
    # Modules never save progress: a fresh sandbox stays without .progress.
    if recorder.is_module(stage):
        return "absent"
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

    actions = _build_actions(
        args.stage, whoami_answer, pwd_answer, day_answer, sandbox_root, persona_name
    )
    p = persona_mod.Persona(persona_name, actions)

    bash_path, bash_version = _bash_provenance()
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
        "bash_path": bash_path,
        "bash_version": bash_version,
        "sandbox_root": sandbox_root,
        "pty_geometry": "%dx%d" % (args.cols, args.rows),
        "per_sentinel_timeout_seconds": args.timeout,
    }

    # Build child env: a short allowlist of the caller's variables (a module's
    # `env | head` prints the practice shell's whole environment into the
    # committed bundle, so the operator's other variables stay out), override
    # SHELLTUTOR_HOME to the fresh tempdir, set TERM if missing so terminal-aware
    # code paths (clear, ansi) work, force COLUMNS/LINES so the lesson's
    # vertical-budget assumptions hold.
    child_env = childenv.base_env()
    child_env["SHELLTUTOR_HOME"] = sandbox_root
    child_env["HOME"] = user_home
    child_env.setdefault("TERM", "xterm-256color")
    child_env["COLUMNS"] = str(args.cols)
    child_env["LINES"] = str(args.rows)
    # D-03 controlled inputs.
    child_env["LC_ALL"] = "C"
    child_env["VIMINIT"] = "set nocompatible"
    if args.ascii:
        child_env["SHELLTUTOR_ASCII"] = "1"
    else:
        child_env.pop("SHELLTUTOR_ASCII", None)
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
        "SHELLTUTOR_ASCII": "1" if args.ascii else "unset",
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
    expected_errors: List[dict] = []
    screen_heights: List[dict] = []
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
        if recorder.is_module(args.stage):
            # A module never touches the learner's own configuration: the
            # scratch HOME must hold no shell startup file afterwards.
            present = [
                n for n in (".bashrc", ".bash_profile", ".profile", ".zshrc", ".zprofile")
                if os.path.exists(os.path.join(user_home, n))
            ]
            outcome["rc_files_absent"] = not present
            if present:
                outcome["progress_ok"] = False
                outcome["notes"] = "module wrote startup files in HOME: %s" % present
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
        expected_errors = result["expected_errors"]
        screen_heights = result["screen_heights"]
        run_ok = result["gate_passed"] and outcome["progress_ok"]
        # A13/A15: the 19-row panel is enforced on the core stage screens and
        # on module screens (the budget in driver.SCREEN_BUDGET counts the
        # blank under the rule). The welcome may take one more row (A12) and
        # the finale is not a panel.
        worst: dict = {}
        for h in screen_heights:
            sid = h["screen_id"]
            worst[sid] = max(worst.get(sid, 0), int(h["lines"]))
        over = sorted(
            (sid, n)
            for sid, n in worst.items()
            if re.match(r"^(S[1-5]|M)-", sid)
            and n > HEIGHT_ALLOWED.get(sid, driver.SCREEN_BUDGET)
        )
        outcome["screens_over_budget"] = [("%s=%d" % (sid, n)) for sid, n in over]
        if over and run_ok:
            run_ok = False
            outcome["notes"] = "screens over the %d-row budget: %s" % (
                driver.SCREEN_BUDGET, ", ".join("%s=%d" % x for x in over))
        if persona_name == "second-try":
            # The deliberate first failure must show the gate's `not yet:`
            # feedback exactly once; zero or two means the gate changed.
            seen = "".join(
                project_terminal_out(os.path.join(variant_out, "terminal.jsonl"))
            ).count(NOT_YET_TEXT)
            outcome["not_yet_count"] = seen
            if seen != 1:
                run_ok = False
                outcome["notes"] = (
                    "second-try expected exactly one %r, saw %d." % (NOT_YET_TEXT, seen)
                )
            if run_ok:
                want_hint, want_nav = RECALL_EXPECTED.get(str(args.stage), (0, 0))
                text = "".join(
                    project_terminal_out(os.path.join(variant_out, "terminal.jsonl"))
                )
                got_hint = text.count(RECALL_HINT_TEXT)
                got_nav = text.count(RECALL_NAV_TEXT)
                outcome["recall_hint_count"] = got_hint
                outcome["recall_nav_count"] = got_nav
                if (got_hint, got_nav) != (want_hint, want_nav):
                    run_ok = False
                    outcome["notes"] = (
                        "second-try expected %d %r and %d %r, saw %d and %d."
                        % (want_hint, RECALL_HINT_TEXT, want_nav,
                           RECALL_NAV_TEXT, got_hint, got_nav)
                    )
            if run_ok:
                # A11 C7: a failed check prints the checklist's closing line
                # once ("Finish the step marked [ ], ...").
                got_close = text.count(GATE_CLOSE_TEXT)
                outcome["gate_close_count"] = got_close
                if got_close != 1:
                    run_ok = False
                    outcome["notes"] = (
                        "second-try expected one checklist closing line "
                        "(%r), saw %d." % (GATE_CLOSE_TEXT, got_close)
                    )
            if run_ok and str(args.stage) == "2":
                # A9 (F-022): the first Stage 2 check lists both items.
                # second-try has made the folder but not cd'd: the folder
                # reason never prints, the cd reason prints once.
                got_items = (
                    text.count(GATE_ITEM_FOLDER_TEXT),
                    text.count(GATE_ITEM_CD_TEXT),
                )
                outcome["gate_item_counts"] = list(got_items)
                if got_items != (0, 1):
                    run_ok = False
                    outcome["notes"] = (
                        "second-try expected the two-item Stage 2 checklist "
                        "(%r never, %r once), saw %d and %d."
                        % ((GATE_ITEM_FOLDER_TEXT, GATE_ITEM_CD_TEXT) + got_items)
                    )
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
        expected_errors=expected_errors,
        screen_heights=screen_heights,
    )
    outcome["ok"] = bool(
        outcome["gate_passed"]
        and outcome["progress_ok"]
        and outcome.get("not_yet_count", 1) == 1
        and outcome["harness_exit_code"] == 0
    )
    rec.write_tap(
        ok=outcome["ok"],
        description="%s %s — variant=%s"
        % (
            "all-stages" if args.stage == "all" else recorder.stage_slug(args.stage),
            persona_name,
            variant,
        ),
    )
    if drive_exception is not None:
        # Re-raise so the dispatcher records the correct exit code,
        # but evidence for this variant has already been written.
        raise drive_exception
    return rec, host_inputs, run_meta, outcome


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
            % (
                "all-stages" if args.stage == "all" else recorder.stage_slug(args.stage),
                variant,
            ),
            skip_reason=reason,
        )
    finally:
        rec.close()


def _exit_code_for(exc: BaseException) -> int:
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

    if args.stage and args.module:
        print(
            "scripts/sim/run.py: --stage and --module are mutually exclusive.",
            file=sys.stderr,
        )
        return 2
    if args.module:
        if args.module not in persona_mod.MODULE_TABLES:
            known = ", ".join(sorted(persona_mod.MODULE_TABLES)) or "none yet"
            print(
                "scripts/sim/run.py: --module %r has no persona table (known: %s)."
                % (args.module, known),
                file=sys.stderr,
            )
            return 2
        args.stage = "module:" + args.module
    elif not args.stage:
        args.stage = "1"

    if args.persona not in SUPPORTED_PERSONAS:
        print(
            "scripts/sim/run.py: --persona %r unsupported; choose from %s."
            % (args.persona, ", ".join(SUPPORTED_PERSONAS)),
            file=sys.stderr,
        )
        return 2
    if args.persona == "second-try" and args.stage not in SECOND_TRY_STAGES:
        print(
            "scripts/sim/run.py: --persona second-try supports --stage 2 or 4 "
            "only (got %r)." % args.stage,
            file=sys.stderr,
        )
        return 2

    if args.variant in RETIRED_VARIANTS:
        print(RETIRED_VARIANT_MESSAGE, file=sys.stderr)
        return 2

    stage_dir = recorder.stage_slug(args.stage)
    out_dir = args.out or os.path.join("audit", _utc_today(), "sim", stage_dir)
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    real_shelltutor = _resolve_shelltutor(args.shelltutor)

    run_id = secrets.token_hex(4)
    _log(args.verbose, "run_id=%s out=%s" % (run_id, out_dir))

    variants_to_run: List[str] = [VARIANT_CURRENT]

    aggregate_exit = 0

    if args.stage in ("5", "all") and shutil.which("vim") is None:
        exc = PrerequisiteMissingError("vim not installed")
        for variant in variants_to_run:
            _write_skip(out_dir, variant, args, "vim not installed")
        print("sim: PrerequisiteMissingError: %s" % exc, file=sys.stderr)
        return 8

    try:
        for variant in variants_to_run:
            rec = None
            try:
                rec, _, _, outcome = _run_variant(
                    variant=variant,
                    shelltutor_path=real_shelltutor,
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
                # Evidence (summary.md, result.tap) was already written
                # from inside _run_variant; record the exit code.
                print(
                    "sim: %s (variant=%s): %s"
                    % (exc.__class__.__name__, variant, exc),
                    file=sys.stderr,
                )
                aggregate_exit = max(aggregate_exit, _exit_code_for(exc))
            finally:
                if rec is not None:
                    rec.close()
    except SystemExit:
        raise
    except Exception:  # pragma: no cover — last-resort diagnostic
        traceback.print_exc()
        return 1

    return aggregate_exit


if __name__ == "__main__":
    raise SystemExit(main())
