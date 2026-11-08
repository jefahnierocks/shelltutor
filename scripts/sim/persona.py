"""careful-beginner persona — Stage 1.

A persona is a deterministic, ordered list of Actions. Each Action
says "wait for sentinel X, then send string S" (S may be empty to
mark a checkpoint without typing). The driver advances through the
list on each sentinel match.

Some sentinels naturally repeat (PROMPT shows up every time a
practice subshell opens). The driver disambiguates by maintaining a
match-offset cursor into the normalized buffer; the persona itself
never asks "which prompt is this?" — it just walks forward.

Stages 2-5 and the finale are built by `stage_walk()`; `build_walk()`
composes the walk for `--stage N` or `--stage all` (decision D-02: one
persona across all five stages, print-and-exit commands from each
lesson, full-screen programs only where the lesson is about them, never
improvising).

The careful-beginner walk for Stage 1:

    welcome → orientation → 1-intro → 1.1 → 1.2 → 1.3 → 1.4
    → gate recall Q1/Q2/Q3 → gate task screen
    → whoami / pwd / date in practice → check
    → follow-up Q1 (whoami text) / Q2 (pwd path) / Q3 (day)
    → "Stage 1 cleared." → quit

The follow-up answers are computed at session start from harness host
inputs (getpass.getuser(), the harness's $SHELLTUTOR_HOME, and the
day from time.strftime("%a")). The persona is dispatch-deterministic:
if the gate re-asks a question (a sentinel re-fires after the
matching cursor advanced past it), the driver raises
PersonaRejectedError.
"""

from __future__ import annotations

import os
from typing import List, NamedTuple, Optional

from .sentinels import PROMPT


class Action(NamedTuple):
    """One persona step.

    wait_for  sentinel id (or literal substring); "" means "no wait":
              the action fires as soon as the persona reaches it.
    send      text to send; "" marks a checkpoint without typing.
    raw       send the bytes exactly, with no trailing newline.
    delay_s   sleep this long before sending (Vim key-code timeout).
    """

    wait_for: str
    send: str
    intent: str
    screen_id: str
    raw: bool = False
    delay_s: float = 0.0


def careful_beginner_stage1(
    whoami_answer: str,
    pwd_answer: str,
    day_answer: str,
    with_quit: bool = True,
) -> List[Action]:
    """Return the careful-beginner Stage 1 action list.

    Parameters are the captured host inputs the persona needs to
    answer the gate follow-up questions correctly. The harness reads
    them at session start (see env.host_snapshot and the run.py
    dispatcher) so the persona stays inert and deterministic.
    """
    walk = [
        Action("WELCOME", "", "render-welcome", "S1-W"),
        Action(PROMPT, "next", "leave-welcome", "S1-W"),
        Action("ORIENTATION", "", "render-orientation", "S1-O"),
        Action(PROMPT, "next", "leave-orientation", "S1-O"),
        Action("STAGE1_INTRO", "", "render-stage1-intro", "S1-I"),
        Action(PROMPT, "next", "leave-stage1-intro", "S1-I"),
        Action("LESSON_1_1", "", "render-lesson-1-1", "S1-L1"),
        Action(PROMPT, "echo hello", "run-echo", "S1-L1"),
        Action(PROMPT, "echo I am at the shell", "run-echo-words", "S1-L1"),
        Action(PROMPT, 'echo "I am at the shell"', "run-echo-quoted", "S1-L1"),
        Action(PROMPT, "next", "leave-lesson-1-1", "S1-L1"),
        Action("LESSON_1_2", "", "render-lesson-1-2", "S1-L2"),
        # Tab completion: `echo p<Tab>` completes to poem.txt.
        Action(PROMPT, "echo p\t", "tab-complete-echo", "S1-L2", raw=True),
        Action("echo poem.txt", "\n", "run-completed-echo", "S1-L2", raw=True),
        # Ctrl+L clears the screen; the prompt is redrawn.
        Action(PROMPT, "\x0c", "ctrl-l-clear", "S1-L2", raw=True),
        # Up arrow recalls `echo poem.txt`; Enter runs it again.
        Action(PROMPT, "\x1b[A", "up-arrow-recall", "S1-L2", raw=True),
        Action("", "\n", "run-recalled-echo", "S1-L2", raw=True, delay_s=0.1),
        # Ctrl+C at an empty prompt gives a fresh prompt.
        Action(PROMPT, "\x03", "ctrl-c-fresh-prompt", "S1-L2", raw=True),
        Action(PROMPT, "next", "leave-lesson-1-2", "S1-L2"),
        Action("LESSON_1_3", "", "render-lesson-1-3", "S1-L3"),
        Action(PROMPT, "whoami", "run-whoami", "S1-L3"),
        Action(PROMPT, "pwd", "run-pwd", "S1-L3"),
        Action(PROMPT, "date", "run-date", "S1-L3"),
        Action(PROMPT, "next", "leave-lesson-1-3", "S1-L3"),
        Action("LESSON_1_4", "", "render-lesson-1-4", "S1-L4"),
        Action(PROMPT, "date", "run-date", "S1-L4"),
        Action(PROMPT, "dtae", "run-dtae-mistyped", "S1-L4"),
        Action(PROMPT, "next", "leave-lesson-1-4", "S1-L4"),
        Action("LESSON_1_5", "", "render-lesson-1-5", "S1-L5"),
        Action(PROMPT, "next", "leave-lesson-1-5", "S1-L5"),
        Action("GATE_HEADER", "", "render-gate", "S1-G"),
        Action("GATE_Q1", "$", "answer-q1", "S1-G"),
        Action("GATE_Q2", "the current working directory", "answer-q2", "S1-G"),
        Action("GATE_Q3", "stdout", "answer-q3", "S1-G"),
        Action("GATE_TASK_HEADER", "", "render-gate-task", "S1-GT"),
        Action(PROMPT, "whoami", "run-whoami", "S1-GT"),
        Action(PROMPT, "pwd", "run-pwd", "S1-GT"),
        Action(PROMPT, "date", "run-date", "S1-GT"),
        Action(PROMPT, "check", "run-check", "S1-GT"),
        Action("TASK_Q_WHOAMI", whoami_answer, "answer-task-whoami", "S1-FQ"),
        Action("TASK_Q_PWD", pwd_answer, "answer-task-pwd", "S1-FQ"),
        Action("TASK_Q_DAY", day_answer, "answer-task-day", "S1-FQ"),
        Action("STAGE_CLEARED", "", "stage1-cleared", "S1-FQ"),
    ]
    # The tutor now stops at the Stage 1 cleared screen (A1.4): `next`
    # continues into Stage 2, `quit` stops here with .progress = 1.
    if with_quit:
        walk.append(Action(PROMPT, "quit", "quit-tutor", "S1-C"))
    else:
        walk.append(Action(PROMPT, "next", "leave-stage1-cleared", "S1-C"))
    return walk


def _cmds(screen_id: str, commands: List[str]) -> List[Action]:
    """One practice-shell command per prompt."""
    return [Action(PROMPT, c, "run-" + c.split()[0], screen_id) for c in commands]


def _lesson(n: int, k: int, commands: List[str]) -> List[Action]:
    sid = "S%d-L%d" % (n, k)
    return (
        [Action("S%d_L%d" % (n, k), "", "render-lesson-%d-%d" % (n, k), sid)]
        + _cmds(sid, commands)
        + [Action(PROMPT, "next", "leave-lesson-%d-%d" % (n, k), sid)]
    )


def _intro(n: int) -> List[Action]:
    sid = "S%d-I" % n
    return [
        Action("S%d_INTRO" % n, "", "render-stage%d-intro" % n, sid),
        Action(PROMPT, "next", "leave-stage%d-intro" % n, sid),
    ]


def _recall(n: int, answers: List[str], misses: bool = False) -> List[Action]:
    """Recall walk for stage `n`.

    `misses` (second-try, Stage 2 only) answers Q1 wrong three times so
    each rung of the recall ladder appears in the evidence (A1.3): miss 2
    prints the hint, miss 3 the hint again plus the three navigation
    facts. Each wait for the question text matches its re-display after
    the previous miss.
    """
    sid = "S%d-G" % n
    walk = [Action("S%d_GATE" % n, "", "render-gate", sid)]
    for i, ans in enumerate(answers, 1):
        q = "S%d_Q%d" % (n, i)
        if i == 1 and misses:
            walk += [
                Action(q, "it lists files", "miss-q1-1", sid),
                Action(q, "it lists files again", "miss-q1-2", sid),
                Action("RECALL_HINT", "", "observe-recall-hint", sid),
                Action(q, "it lists files once more", "miss-q1-3", sid),
                Action("RECALL_NAV", "", "observe-recall-nav", sid),
                Action(q, ans, "answer-q%d" % i, sid),
            ]
            continue
        walk.append(Action(q, ans, "answer-q%d" % i, sid))
    return walk


def _gate_commands(
    screen_id: str, first: List[str], rest: List[str], second_try: bool
) -> List[Action]:
    """Gate-task commands followed by `check`.

    careful-beginner runs `first + rest` and checks once. `second-try`
    runs only `first`, checks, observes the gate's "not yet:" feedback
    (sentinel NOT_YET), then runs `rest` and checks again. It never improvises: the missing step is the one the gate named.
    """
    if not second_try:
        return _cmds(screen_id, first + rest) + [
            Action(PROMPT, "check", "run-check", screen_id)
        ]
    return (
        _cmds(screen_id, first)
        + [
            Action(PROMPT, "check", "run-check-first", screen_id),
            Action("NOT_YET", "", "observe-not-yet", screen_id),
        ]
        + _cmds(screen_id, rest)
        + [Action(PROMPT, "check", "run-check", screen_id)]
    )


def _vim_edit(screen_id: str, typed: str, quit_cmd: str) -> List[Action]:
    """Open practice.txt, insert text, leave insert mode, quit.

    After Escape the next action carries delay_s=0.3 so Vim's key-code
    timeout cannot swallow the following colon.
    """
    return [
        Action(PROMPT, "vim practice.txt", "run-vim", screen_id),
        Action("VIM_PRACTICE", "i", "vim-insert-mode", screen_id, raw=True),
        Action("VIM_INSERT", typed, "vim-type", screen_id, raw=True),
        Action("", "\x1b", "vim-escape", screen_id, raw=True, delay_s=0.1),
        Action("", quit_cmd, "vim-quit", screen_id, delay_s=0.3),
    ]


def stage_walk(
    n: int,
    pwd_answer: str = "",
    man_available: bool = True,
    sandbox_root: str = "",
    second_try: bool = False,
) -> List[Action]:
    """Walk for stage `n` (2-5), from its intro to its cleared line.

    `second_try` (stages 2 and 4 only) makes the first `check` of the gate
    task fail on purpose so the gate's "not yet:" feedback is observed once.

    Follows the stage-folder lesson copy (F-010, F-011; WP-02): lesson 2.2
    ends with `cd <sandbox_root>` and lesson 3.2 reads `../poem.txt` and
    pages `../numbers.txt`, because stage 3-5 practice prompts start in
    their stage folder. `sandbox_root` defaults to the parent of the
    Stage 1 `pwd_answer` (`<sandbox>/stage1`).
    """
    if not sandbox_root:
        sandbox_root = os.path.dirname(pwd_answer)
    if n == 2:
        return (
            _intro(2)
            + _lesson(2, 1, ["pwd"])
            + _lesson(2, 2, ["ls", "ls -p", "ls -a", "ls /etc"])
            + _lesson(2, 3, ["cd /tmp", "pwd", "cd", "cd -", "cd ..", "cd " + sandbox_root])
            + _lesson(2, 4, [])
            + _recall(2, ["goes up one folder", "home folder", "~/projects/notes"], second_try)
            + [Action("S2_TASK", "", "render-gate-task", "S2-GT")]
            + _gate_commands(
                "S2-GT", ["mkdir practice"], ["cd practice", "pwd"], second_try
            )
            + [Action("S2_CLEARED", "", "stage2-cleared", "S2-GT")]
        )
    if n == 3:
        return (
            _intro(3)
            + _lesson(3, 1, ["touch hello.txt", "ls", "mkdir notes", "ls"])
            + [Action("S3_L2", "", "render-lesson-3-2", "S3-L2")]
            + _cmds("S3-L2", ["cat hello.txt", "cat ../poem.txt"])
            + [
                Action(PROMPT, "less ../numbers.txt", "run-less", "S3-L2"),
                Action("LESS_NUMBERS", "q", "leave-less-pager", "S3-L2", raw=True),
                Action(PROMPT, "next", "leave-lesson-3-2", "S3-L2"),
            ]
            + _lesson(
                3,
                3,
                ["cp hello.txt backup.txt", "mv hello.txt hi.txt", "mv hi.txt notes/", "rm backup.txt"],
            )
            + _recall(3, ["touch", "gone", "mv"])
            + [Action("S3_TASK", "", "render-gate-task", "S3-GT")]
            + _cmds(
                "S3-GT",
                ["echo hello > notes.txt", "cp notes.txt backup.txt", "mv notes.txt done.txt", "rm backup.txt"],
            )
            + [
                Action(PROMPT, "check", "run-check", "S3-GT"),
                Action("S3_CLEARED", "", "stage3-cleared", "S3-GT"),
            ]
        )
    if n == 4:
        return (
            _intro(4)
            + _lesson(
                4,
                1,
                ["ls -l /etc", "wc -l poem.txt", 'echo "hello world"', "command -v ls", "command -v vim"],
            )
            + _lesson(
                4,
                2,
                ["seq 1 100 | wc -l", "ls /usr/bin | sort | head", "ls /usr/bin | grep ^a | wc -l"],
            )
            + _lesson(
                4,
                3,
                [
                    "echo first > greeting.txt",
                    "echo second >> greeting.txt",
                    "cat greeting.txt",
                    "wc -w < poem.txt",
                ],
            )
            + _lesson(4, 4, ["ls *.txt"])
            + _recall(4, ["the path to vim", "> overwrites, >> appends", "because of the space"])
            + [Action("S4_TASK", "", "render-gate-task", "S4-GT")]
            + _gate_commands(
                "S4-GT", ["seq 1 100 | wc -l > count.txt"], ["ls *.txt"], second_try
            )
            + [Action("S4_CLEARED", "", "stage4-cleared", "S4-GT")]
        )
    if n == 5:
        l1 = [Action("S5_L1", "", "render-lesson-5-1", "S5-L1")]
        if man_available:
            l1 += [
                Action(PROMPT, "man ls", "run-man", "S5-L1"),
                Action("MAN_LS", "q", "leave-man-pager", "S5-L1", raw=True),
            ]
        else:
            l1 += [Action("", "", "skip-man-missing", "S5-L1")]
        l1 += [Action(PROMPT, "next", "leave-lesson-5-1", "S5-L1")]
        l2 = [Action("S5_L2", "", "render-lesson-5-2", "S5-L2")] + _cmds(
            "S5-L2", ["command -v vim", "vim --version"]
        )
        l2 += [
            Action(PROMPT, "vim", "run-vim", "S5-L2"),
            Action("VIM_INTRO", ":q", "vim-quit", "S5-L2"),
            Action(PROMPT, "next", "leave-lesson-5-2", "S5-L2"),
        ]
        # 5.3 is the idea (read only); 5.4 practises both sequences; 5.5
        # probes for vimtutor.
        l3 = _lesson(5, 3, [])
        l4 = (
            [Action("S5_L4", "", "render-lesson-5-4", "S5-L4")]
            + _cmds("S5-L4", ["cat practice.txt"])
            + _vim_edit("S5-L4", "abc", ":q!")
            + _cmds("S5-L4", ["cat practice.txt"])
            + _vim_edit("S5-L4", "abc", ":wq")
            + _cmds("S5-L4", ["cat practice.txt"])
            + [Action(PROMPT, "next", "leave-lesson-5-4", "S5-L4")]
        )
        l5 = (
            [Action("S5_L5", "", "render-lesson-5-5", "S5-L5")]
            + _cmds("S5-L5", ["command -v vimtutor"])
            + [Action(PROMPT, "next", "leave-lesson-5-5", "S5-L5")]
        )
        gate = _recall(5, ["q", ":w", "no"])
        task1 = (
            [Action("S5_TASK1", "", "render-gate-task-1", "S5-GT1")]
            + _cmds("S5-GT1", ["cat practice.txt"])
            + _vim_edit("S5-GT1", "xyz", ":q!")
            + _cmds("S5-GT1", ["cat practice.txt"])
            + [
                Action(PROMPT, "check", "run-check", "S5-GT1"),
                Action("S5_PHASE1_OK", "", "phase1-verified", "S5-GT1"),
            ]
        )
        task2 = (
            [Action("S5_TASK2", "", "render-gate-task-2", "S5-GT2")]
            + _vim_edit("S5-GT2", "after ", ":wq")
            + _cmds("S5-GT2", ["cat practice.txt"])
            + [
                Action(PROMPT, "check", "run-check", "S5-GT2"),
                Action("S5_CLEARED", "", "stage5-cleared", "S5-GT2"),
            ]
        )
        return _intro(5) + l1 + l2 + l3 + l4 + l5 + gate + task1 + task2
    raise ValueError("stage_walk: unsupported stage %r" % (n,))


# Persona tables for stand-alone modules. A module's walk is expanded from
# a small table, not hand-written (`module_walk`). Keys: `lessons` (count),
# `gate` ({"recall": [...], "task": [...]}), and optionally `lesson_actions`
# ({k: [commands typed at lesson k]}), `prompt_before_next` ({k: prompt text
# left by lesson k's commands, awaited before its `next`}) and `prompt_after`
# ({k: prompt text expected after lesson k's `next`}).
MODULE_TABLES: dict = {
    # shells (WP-16): intro + 3 lessons, three recall answers, one task.
    "shells": {
        "lessons": 3,
        "gate": {
            "recall": ["a program", "command -v zsh", "login shell"],
            "task": ["command -v zsh > zsh.txt"],
        },
    },
    # env (WP-17): intro + 5 lessons. Lesson 4 sets PS1; the walk types
    # `next` at the changed prompt and then asserts the next screen's prompt
    # is the tutor's own again (the module's central claim: it reverts).
    "env": {
        "lessons": 5,
        "gate": {
            "recall": ["export", "a list of folders", "shelltutor>"],
            "task": ["TOPIC=shell", "export TOPIC", "bash -c 'echo $TOPIC' > seen.txt"],
        },
        "lesson_actions": {4: ["PS1='me> '"]},
        "prompt_before_next": {4: "\nme> "},
        "prompt_after": {4: "shelltutor> "},
    },
}


def module_walk(
    name: str,
    lessons: int,
    gate: dict,
    lesson_actions: Optional[dict] = None,
    prompt_after: Optional[dict] = None,
    prompt_before_next: Optional[dict] = None,
) -> List[Action]:
    """Expand a module table into a careful-beginner walk.

    Sentinels come from the module heading convention, so sentinels.py
    carries no per-module entries (the driver treats an unregistered
    `wait_for` as a literal substring):

        intro    ``MODULE — <name>:``
        lesson   ``<name> <k> — ``            (prefix, no title text)
        gate     ``<name> — gate``
        task     ``<name> — task``
        cleared  ``✓ <name> cleared.``

    `gate` is ``{"recall": [answers...], "task": [commands...]}``; either
    list may be empty. Recall answers wait for ``Q<i>:``. A non-empty task
    list waits for the task heading, types each command at the practice
    prompt, then `check`. The walk ends at the cleared screen with `quit`;
    modules never save progress.

    `lesson_actions` maps a lesson number to commands typed at that
    lesson's prompt before `next`. `prompt_after` maps a lesson number to
    the prompt text expected at the first prompt after that lesson's
    `next`: that wait uses the text instead of the generic prompt, so a
    prompt that should have reverted (or changed) is asserted, not assumed.
    `prompt_before_next` maps a lesson number to the prompt text the lesson's
    own commands leave behind: the wait before that lesson's `next` uses it
    (a lesson that changes `PS1` types `next` at the new prompt).
    """
    gate = gate or {}
    lesson_actions = lesson_actions or {}
    prompt_after = prompt_after or {}
    prompt_before_next = prompt_before_next or {}
    recall = list(gate.get("recall") or [])
    task = list(gate.get("task") or [])
    pending = {"text": None}

    def prompt() -> str:
        text, pending["text"] = pending["text"], None
        return text if text is not None else PROMPT

    walk = [
        Action("MODULE — %s:" % name, "", "render-module-intro", "M-I"),
        Action(prompt(), "next", "leave-module-intro", "M-I"),
    ]
    for k in range(1, lessons + 1):
        sid = "M-L%d" % k
        walk.append(Action("%s %d — " % (name, k), "", "render-lesson-%d" % k, sid))
        for cmd in lesson_actions.get(k, []):
            walk.append(Action(prompt(), cmd, "run-" + cmd.split()[0], sid))
        wait_next = prompt()
        if k in prompt_before_next:
            wait_next = prompt_before_next[k]
        walk.append(Action(wait_next, "next", "leave-lesson-%d" % k, sid))
        if k in prompt_after:
            pending["text"] = prompt_after[k]
    walk.append(Action("%s — gate" % name, "", "render-gate", "M-G"))
    for i, answer in enumerate(recall, 1):
        walk.append(Action("Q%d:" % i, answer, "answer-q%d" % i, "M-G"))
    if task:
        walk.append(Action("%s — task" % name, "", "render-task", "M-GT"))
        for cmd in task:
            walk.append(Action(prompt(), cmd, "run-" + cmd.split()[0], "M-GT"))
        walk.append(Action(prompt(), "check", "run-check", "M-GT"))
    walk.append(Action("✓ %s cleared." % name, "", "module-cleared", "M-C"))
    walk.append(Action(PROMPT, "quit", "quit-tutor", "M-C"))
    return walk


def build_walk(
    stage: str,
    whoami_answer: str,
    pwd_answer: str,
    day_answer: str,
    man_available: bool = True,
    sandbox_root: str = "",
    persona: str = "careful-beginner",
) -> List[Action]:
    """Compose the walk for `--stage` (`1`..`5` or `all`).

    `persona` is `careful-beginner` (any stage) or `second-try` (stages
    2 and 4 only; run.py rejects other combinations with exit 2).

    Single stage N >= 2 starts at the stage intro and, after the cleared
    screen (stages 1-4), waits for its prompt and quits there. In `all`
    mode each of stages 1-4 sends `next` at the cleared screen instead.
    Stage 5 and `all` end at the finale, after which the child exits on
    its own.
    """
    second_try = persona == "second-try"
    if second_try and stage not in ("2", "4"):
        raise ValueError("second-try supports stages 2 and 4 only, not %r" % (stage,))
    finale = [Action("FINALE", "", "render-finale", "FIN")]
    if stage == "1":
        return careful_beginner_stage1(whoami_answer, pwd_answer, day_answer)
    if stage == "all":
        walk = careful_beginner_stage1(
            whoami_answer, pwd_answer, day_answer, with_quit=False
        )
        for n in (2, 3, 4, 5):
            walk += stage_walk(n, pwd_answer, man_available, sandbox_root)
            if n < 5:
                walk.append(
                    Action(PROMPT, "next", "leave-stage%d-cleared" % n, "S%d-C" % n)
                )
        return walk + finale
    n = int(stage)
    walk = stage_walk(n, pwd_answer, man_available, sandbox_root, second_try)
    if n == 5:
        return walk + finale
    return walk + [Action(PROMPT, "quit", "quit-tutor", "S%d-C" % n)]


class Persona:
    """Iterator-like wrapper around an Action list.

    Keeps a cursor and exposes `current` / `advance`. The driver calls
    `current` to know what to wait for and what to send; on a match,
    it calls `advance`. When the list is exhausted, `current` is
    None.
    """

    def __init__(self, name: str, actions: List[Action]):
        self.name = name
        self._actions = actions
        self._cursor = 0

    @property
    def current(self) -> Optional[Action]:
        if self._cursor >= len(self._actions):
            return None
        return self._actions[self._cursor]

    @property
    def cursor(self) -> int:
        return self._cursor

    def advance(self) -> None:
        self._cursor += 1
