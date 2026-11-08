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
    "LESSON_1_2": "1.2 — keyboard habits",
    "LESSON_1_3": "1.3 — where am I, who am I, when is it",
    "LESSON_1_4": "1.4 — the shell, caught in the act",
    "LESSON_1_5": "1.5 — who else types here",
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

# Stages 2-5, the finale and the full-screen-program markers. Transcribed
# from the lesson and gate heredocs in `shelltutor` and re-verified
# against the file (ANSI-stripped) at the revision the baseline cites.
# `S<N>_GATE` also occurs inside `S<N>_TASK`; the forward-only cursor
# handles the order because the gate screen renders first.
SENTINELS.update(
    {
        "S2_INTRO": "STAGE 2 — Paths and the filesystem",
        "S2_L1": "2.1 — where you are",
        "S2_L2": "2.2 — ls: what is here",
        "S2_L3": "2.3 — cd: moving",
        "S2_L4": "2.4 — names for places",
        "S2_GATE": "STAGE 2 — GATE",
        "S2_Q1": "Q1: What does cd .. do?",
        "S2_Q2": "Q2: What does ~ mean in a path?",
        "S2_Q3": "Q3: If I'm in ~/projects and I type cd notes",
        "S2_TASK": "STAGE 2 — GATE TASK",
        "S2_CLEARED": "Stage 2 cleared.",
        "S3_INTRO": "STAGE 3 — Files and operations",
        "S3_L1": "3.1 — creating: touch, mkdir",
        "S3_L2": "3.2 — reading: cat, less",
        "S3_L3": "3.3 — copy, move, delete",
        "S3_GATE": "STAGE 3 — GATE",
        "S3_Q1": "Q1: Which command creates an empty file?",
        "S3_Q2": "Q2: After rm important.txt, where is the file?",
        "S3_Q3": "Q3: What single command renames old.txt to new.txt?",
        "S3_TASK": "STAGE 3 — GATE TASK",
        "S3_CLEARED": "Stage 3 cleared.",
        "S4_INTRO": "STAGE 4 — Commands, streams, composition",
        "S4_L1": "4.1 — reading a command",
        "S4_L2": "4.2 — the pipe",
        "S4_L3": "4.3 — redirection",
        "S4_L4": "4.4 — globs",
        "S4_GATE": "STAGE 4 — GATE",
        "S4_Q1": "Q1: What does command -v vim print, if Vim is installed?",
        "S4_Q2": "Q2: What is the difference between > and >>?",
        "S4_Q3": "Q3: Why does vim my notes.txt open two files instead of one?",
        "S4_TASK": "STAGE 4 — GATE TASK",
        "S4_CLEARED": "Stage 4 cleared.",
        "S5_INTRO": "STAGE 5 — Ready for vimtutor",
        "S5_L1": "5.1 — print-and-exit vs full-screen",
        "S5_L2": "5.2 — entering and leaving Vim",
        "S5_L3": "5.3 — buffer vs file",
        "S5_L4": "5.4 — practice: discard, then save",
        "S5_L5": "5.5 — calling vimtutor",
        "S5_GATE": "STAGE 5 — GATE",
        "S5_Q1": "Q1: How do you exit man ls?",
        "S5_Q2": "Q2: After vim notes.txt, what makes Vim write your edit to the file?",
        "S5_Q3": "Q3: If you open notes.txt in vim, type some letters, and quit with :q!",
        "S5_TASK1": "STAGE 5 — GATE TASK (phase 1 of 2)",
        "S5_PHASE1_OK": "Phase 1 verified — the file was unchanged.",
        "S5_TASK2": "STAGE 5 — GATE TASK (phase 2 of 2)",
        "S5_CLEARED": "Stage 5 cleared.",
        "FINALE": "You're ready for vimtutor.",
        "MAN_LS": "LS(1)",
        "LESS_NUMBERS": "1\n2\n3\n4\n5",
        "NOT_YET": "not yet:",
        "RECALL_HINT": "Hint:",
        "RECALL_NAV": "Passed stages are saved.",
        "VIM_INTRO": "VIM - Vi IMproved",
        "VIM_PRACTICE": '"practice.txt"',
        "VIM_INSERT": "-- INSERT --",
    }
)
