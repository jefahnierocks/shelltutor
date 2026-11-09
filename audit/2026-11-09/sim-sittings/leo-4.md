# Synthetic walkthrough: Leo, sitting 4

## Sitting

- Date: 2026-11-09
- Persona: `docs/sim-personas/leo.md` (Leo, 13, `gamer-brute-forcer`); learner role: child
- Persona sheet version: 0.2.0
- Simulation rules confirmed: zero forward knowledge, reading limit (commands, `▶` lines, command-colour text, first sentence of each paragraph; whole screen if under eight lines), friction meter (quit at 8).
- Tutor revision 3045f88 (script 13847ef); `sitting.py start` with `/bin/bash` (3.2.57), no `--arg`, so it began at the welcome screen. This is Leo's fourth sitting; no memory of earlier ones.
- `--info` lines shown: none.

## Per screen (compact; one line of monologue per screen, all inputs verbatim)

Friction rule applied: +1 per reading-only screen after the second in a row, +2 per rejection, +1 per mode confusion, -1 per gate cleared.

| Screen | Read / did not read | Jargon quoted | Input [context] -> response | Rung | Friction |
| --- | --- | --- | --- | --- | --- |
| welcome | arrow line, first sentences; did not read stage blurb, folder paragraph | "Your work happens in ..." | `next` [nav] -> orientation | none | 0 |
| Orientation | commands, four words; skipped resize sentence | none | `next` [nav] -> Stage 1 intro | none | 0 |
| Stage 1 intro (reading-only #3 in a row) | arrow; under 8 lines, read all | "keyboard habits" | `next` [nav] -> 1.1 | none | 1 (third reading-only screen) |
| 1.1 running commands | commands; skipped last paragraph | none | `echo hello`, `echo I am at the shell`, `echo "I am at the shell"` [bash] -> printed each; `next` [nav] | none | 1 |
| 1.2 keyboard habits | Tab line; did not read Ctrl+L / Ctrl+C rows | "escape hatch" | raw `echo p<Tab>` [bash] -> filled `echo poem.txt`; Enter -> `poem.txt`; `next` [nav] | none | 1 |
| 1.3 where/who/when | commands; skipped prompt-ends-in-`>` paragraph | "print working directory" | `whoami`, `pwd`, `date` [bash]; `next` [nav] | none | 1 |
| 1.4 the shell, caught in the act | commands; first sentences | "terminal -> shell -> program" | `dtae` [bash] -> `bash: dtae: command not found`; `date`; `next` [nav] | none | 1 |
| 1.5 who else types here | arrow; first sentences only (11 lines) | "A helper", "AI assistant" | `next` [nav] | none | 1 |
| Stage 1 gate recall Q1 | n/a | none | `$` [recall] -> accepted | none | 1 |
| Q2 | n/a | none | `the folder` [recall] -> accepted | none | 1 |
| Q3 | n/a | none | `the screen` [recall] -> accepted | none | 1 |
| Stage 1 gate task | commands | none | `whoami`, `pwd`, `date`, `check` [bash]; follow-ups `[user]`, pasted pwd path, `Mon` [follow-up] -> all accepted | none | 0 (gate cleared -1) |
| Stage 1 cleared (reading-only #1) | "You can now" list skimmed | none | `next` [nav] | none | 0 |
| Stage 2 intro (#2) | arrow; first sentences | "path symbols" | `next` [nav] | none | 0 |
| 2.1 where you are | tree and `you are here`; skipped pwd paragraph | "current directory" | `pwd` [bash]; `next` [nav] | none | 0 |
| 2.2 ls | commands | "hidden names" | `ls -p`, `ls -a` [bash]; `next` [nav] | none | 0 |
| 2.3 cd | commands; skipped the long path paragraph | "your home folder, outside this practice area" | `cd ..`, `pwd`, `cd -` [bash]; `next` [nav] | none | 0 |
| 2.4 names for places | commands; skipped "Predict before you act. In ~/projects, the bare name notes means ~/projects/notes." second sentence | "Relative paths", "Absolute paths" | `mkdir demo`, `ls -p` [bash]; `next` [nav] | none | 0 |
| Stage 2 gate Q1 | n/a | none | `goes up one folder` [recall] -> accepted | none | 0 |
| Q2 | n/a | none | `your home folder` [recall] -> accepted | none | 0 |
| Q3 | n/a | "relative name" | `the notes folder` [recall] -> REJECTED, hint ("Lesson 2.4: a relative name starts from the folder you are already in."); then `~/projects/notes` [recall] -> accepted | hint (partly copied: Leo took "start from the folder you are already in" and tried the long form) | 2 (rejection +2) |
| Stage 2 gate task | commands | none | `mkdir practice`, `cd practice`, `pwd`, `check` [bash/nav] -> cleared | none | 1 (gate cleared -1) |
| Stage 2 cleared, Stage 3 intro (#1, #2) | arrow only | "immediate" | `next`, `next` [nav] | none | 1 |
| 3.1 touch/mkdir | commands | none | `touch hello.txt`, `ls` [bash]; `next` | none | 1 |
| 3.2 cat/less | commands; skipped the less paragraph | "the screen takes over" | `cat ../poem.txt`, `less ../numbers.txt` [bash]; raw `q` [bash] -> back at the shell prompt; `next` | none | 1 |
| 3.3 cp/mv/rm | commands | none | `cp hello.txt backup.txt`, `mv hello.txt hi.txt`, `rm backup.txt` [bash]; `next` | none | 1 |
| Stage 3 gate Q1-Q3 | n/a | none | `touch`, `gone`, `mv old.txt new.txt` [recall] -> all accepted | none | 1 |
| Stage 3 gate task | numbered list | none | `echo hello > notes.txt`, `cp notes.txt backup.txt`, `mv notes.txt done.txt`, `rm backup.txt`, `check` -> cleared | none | 0 (gate cleared -1) |
| Stage 3 cleared, Stage 4 intro (#1, #2) | arrow only | "glob", "redirect", "pipe" | `next`, `next` [nav] | none | 0 |
| 4.1 reading a command | commands; skipped grammar paragraph | "command options arguments" | `command -v ls`, `command -v vim` [bash] -> `/bin/ls`, `/usr/bin/vim`; `next` | none | 0 |
| 4.2 the pipe | commands | "input" | `seq 1 100 | wc -l` -> 100; `ls /usr/bin | grep ^a | wc -l` -> 41 [bash]; `next` | none | 0 |
| 4.3 redirection | commands and comments | "overwrite", "append" | `echo first > greeting.txt`, `echo second >> greeting.txt`, `cat greeting.txt` [bash]; `next` | none | 0 |
| 4.4 globs | arrow, commands | "glob" | `next` [nav] (no practice; arrow says next) | none | 0 |
| Stage 4 gate Q1 | n/a | none | `/usr/bin/vim` [recall] -> accepted | none | 0 |
| Stage 4 gate Q2 | n/a | none | `> overwrites and >> appends` [recall] -> REJECTED, hint rung 1 ("Lesson 4.3: what each arrow does to a file that already exists.") | hint (did not resolve; the answer was already correct) | 2 |
| Q2 retry | n/a | none | `one replaces the old file and two adds to the end` [recall] -> REJECTED, hint plus "Answer in a few words, like the lesson did, not a full sentence." | hint plus length cue (did not resolve) | 4 |
| Q2 retry | n/a | none | `overwrite append` [recall] -> REJECTED, same two hint lines | same | 6 |
| Q2 retry | n/a | none | `>> appends` [recall] -> accepted | none | 6 |
| Stage 4 gate Q3 | n/a | "what separates the words after vim, and what quotes do" | `the space` [recall] -> REJECTED, hint "Lesson 4.1: what separates the words after vim, and what quotes do." | hint (Leo has nothing left to try from it) | 8: QUIT |

## Per gate

- Stage 1: recall 3 of 3 first attempt (`$`, `the folder`, `the screen`); task cleared on first `check`; cleared.
- Stage 2: recall Q3 needed two attempts (`the notes folder` rejected, `~/projects/notes` accepted after the hint); task cleared; cleared.
- Stage 3: recall 3 of 3 first attempt; task cleared on first `check`; cleared.
- Stage 4: Q1 first attempt; Q2 needed four attempts (three rejected verbatim: `> overwrites and >> appends`, `one replaces the old file and two adds to the end`, `overwrite append`; accepted `>> appends`); Q3 first attempt `the space` rejected; not cleared; task not reached.

## End of sitting

- Final friction 8, quit at "Stage 4 gate, Q3 (Why does vim my notes.txt open two files instead of one?)". By source: reading charges +1 (Stage 1 intro, third reading-only screen), rejections 5 x 2 = +10, mode confusion 0, gates cleared -3 (Stages 1, 2, 3); net 8.
- Stages cleared: 1, 2, 3. Stage 4 lessons 4.1-4.4 seen, gate recall not passed.
- Equivalent human sitting time: about 20 to 25 minutes (estimate; roughly 100 turns of commands, 4 rejected recall answers on Stage 4).
- **Candidate F-nnn**
  - F-a (Stage 4 gate, Q2 "What is the difference between > and >>?"): the input `> overwrites and >> appends` was rejected although it states exactly the lesson's two words, then `>> appends` alone was accepted. A fuller correct answer is rejected while a shorter one passes. Inputs: `> overwrites and >> appends`, `overwrite append` (rejected); `>> appends` (accepted).
  - F-b (Stage 4 gate, Q2): the hint ("what each arrow does to a file that already exists") never changed across three rejections, and the added rung "Answer in a few words, like the lesson did, not a full sentence" implies length was the problem, but `overwrite append` (two words) was also rejected. The rung did not predict the working answer.
  - F-c (Stage 4 gate, Q3 "Why does vim my notes.txt open two files instead of one?"): `the space` was rejected, and the hint names "what separates the words after vim, and what quotes do" without saying the answer is expected in terms of quotes; the lesson's own comment says `opens TWO files: 'my' and 'notes.txt'`.
- **Candidate O-nnn**
  - O-a (Stage 2 gate, Q3): "If I'm in ~/projects and I type cd notes, what folder am I in?" The answer sits in the second sentence of a paragraph (2.4: "Predict before you act.  In ~/projects, the bare name notes means ~/projects/notes."), after a first sentence about prediction; a reader of first sentences misses it. The hint's "a relative name" uses a word Leo does not have.
  - O-b (Stage 1, welcome, Orientation, Stage 1 intro): three reading-only screens in a row before any practice prompt; the third costs a friction point.
  - O-c (Stage 4 gate Q2/Q3 hint text): "Answer in a few words, like the lesson did, not a full sentence." The sentence reads as a rule about length, but the lesson's words were comments on commands, not a sentence at all.
  - O-d (Stage 4, 4.4 globs): the screen ends with "Type next to take Stage 4's gate" and has no practice prompt; the arrow line offers no command to try, so a reader who obeys the arrow never types a glob before the gate.
  - O-e (Stage 3, 3.3): the second `mv` example (`mv hi.txt notes/`) refers to a folder `notes` that exists only if the learner made it in 3.1; a learner who follows the arrow with `mv` would hit an error.
- **Debrief** (out of character):
  - Stage 4 gate Q2 and Q3 produced six of Leo's eight points; the answers Leo gave were correct in meaning and were rejected.
  - Sentences that triggered it: "Answer in a few words, like the lesson did, not a full sentence." and "Lesson 4.3: what each arrow does to a file that already exists." (repeated verbatim).
  - "Lesson 4.1: what separates the words after vim, and what quotes do." does not tell a learner who answered `the space` what is missing.
  - "Predict before you act.  In ~/projects, the bare name notes means ~/projects/notes." holds the one fact Q3 of Stage 2 needs, in a second sentence.
  - Stage 1 ran clean for Leo under v0.2: no jargon rejections; the first sentence of each paragraph and the "this is not the shell" line were enough.
