"""Stable substring patterns the driver matches against normalized
PTY output. Patterns are post-CRLF/ANSI-stripped substrings; the
driver normalizes the read buffer before matching.

The pattern set is deliberately narrow:

- Each sentinel id maps to a single substring.
- Substrings are stable across the current Stage 1 lesson copy
  (shelltutor lines 471-758) and have been verified against an
  actual current-rc capture.
- ANSI sequences embedded inside lesson copy (e.g., dim/cmd wrappers
  around `whoami`, `pwd`, `date`) are stripped before matching, so
  the patterns refer to the bare words.

Note: PROMPT is matched ad-hoc by the persona loop. The catalogue
below carries lesson screen and gate-screen sentinels only.
"""

PROMPT = "shelltutor> "

# Stage 1 screen-and-question sentinels, ordered along the careful-beginner walk.
SENTINELS = {
    "WELCOME": "SHELLTUTOR  —  a vimtutor prerequisite course",
    "ORIENTATION": "Orientation",
    "STAGE1_INTRO": "STAGE 1 — Where am I?",
    "LESSON_1_1": "1.1 — running commands",
    "LESSON_1_2": "1.2 — where am I, who am I, when is it",
    "LESSON_1_3": "1.3 — what just happened",
    "GATE_HEADER": "STAGE 1 — GATE",
    "GATE_Q1": "Q1: Which character usually ends a shell prompt",
    "GATE_Q2": "Q2: What does pwd print?",
    "GATE_Q3": "Q3: After whoami runs, where does its output go?",
    "GATE_TASK_HEADER": "STAGE 1 — GATE TASK",
    "TASK_Q_WHOAMI": "What did whoami print? (just the username)",
    "TASK_Q_PWD": "What did pwd print? (paste the full path)",
    "TASK_Q_DAY": "What day of the week did date show?",
    "STAGE_CLEARED": "Stage 1 cleared.",
}
