"""careful-beginner persona — Stage 1.

A persona is a deterministic, ordered list of Actions. Each Action
says "wait for sentinel X, then send string S" (S may be empty to
mark a checkpoint without typing). The driver advances through the
list on each sentinel match.

Some sentinels naturally repeat (PROMPT shows up every time a
practice subshell opens). The driver disambiguates by maintaining a
match-offset cursor into the normalized buffer; the persona itself
never asks "which prompt is this?" — it just walks forward.

The careful-beginner walk for Stage 1:

    welcome → orientation → 1-intro → 1.1 → 1.2 → 1.3
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

from typing import List, NamedTuple, Optional

from .sentinels import PROMPT


class Action(NamedTuple):
    wait_for: str
    send: str
    intent: str
    screen_id: str


def careful_beginner_stage1(
    whoami_answer: str,
    pwd_answer: str,
    day_answer: str,
) -> List[Action]:
    """Return the careful-beginner Stage 1 action list.

    Parameters are the captured host inputs the persona needs to
    answer the gate follow-up questions correctly. The harness reads
    them at session start (see env.host_snapshot and the run.py
    dispatcher) so the persona stays inert and deterministic.
    """
    return [
        Action("WELCOME", "", "render-welcome", "S1-W"),
        Action(PROMPT, "next", "leave-welcome", "S1-W"),
        Action("ORIENTATION", "", "render-orientation", "S1-O"),
        Action(PROMPT, "next", "leave-orientation", "S1-O"),
        Action("STAGE1_INTRO", "", "render-stage1-intro", "S1-I"),
        Action(PROMPT, "next", "leave-stage1-intro", "S1-I"),
        Action("LESSON_1_1", "", "render-lesson-1-1", "S1-L1"),
        Action(PROMPT, "next", "leave-lesson-1-1", "S1-L1"),
        Action("LESSON_1_2", "", "render-lesson-1-2", "S1-L2"),
        Action(PROMPT, "next", "leave-lesson-1-2", "S1-L2"),
        Action("LESSON_1_3", "", "render-lesson-1-3", "S1-L3"),
        Action(PROMPT, "next", "leave-lesson-1-3", "S1-L3"),
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
        Action(PROMPT, "quit", "quit-tutor", "S1-FQ"),
    ]


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
