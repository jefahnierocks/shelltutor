---
title: Consultant response — shelltutor screens (November 2026)
category: design
component: screens
status: proposal
version: 0.1.0
last_updated: 2026-11-09
tags: [design, chrome, screens, consultant, response, mockups]
priority: high
---

# Consultant response — shelltutor screens

Answers the design brief of 2026-11-09 ("Design brief for an outside
consultant — shelltutor screens"). Everything here fits the brief's §2
constraints: 80×24, sixteen-colour SGR, UTF-8 glyphs with a width-stable
ASCII form, Bash 3.2 and POSIX tools, no cursor positioning. Mock-ups are
80-column text; §6 gives every one of them in ASCII, generated from the
UTF-8 form by a fixed substitution so the two cannot drift. This is one
rendering-only package, as the brief's §6 asks; §7 lists what it touches.

## 1. Where the biggest gains are, in order

1. **Whitespace discipline.** A blank row between the lower rule and the
   prompt; blank rows around the one typeable block; a blank row above
   the `▶` line. Costs nothing, changes the feel more than anything else.
2. **Fewer colours in the body.** Seven roles on one lesson today. Four
   are enough: bold for a concept or key being named, green for
   typeable, grey for asides and the footer, yellow for the tutor's
   voice (`▶` and `┃`). Red stays, rarely, on the word not the sentence.
3. **De-duplicate the header and title.** The product name leaves lesson
   and gate headers; the title loses its `1.1 —` prefix because the
   header's right-hand `1.1` already says it.
4. **Width-stable glyph pairs**, so the ASCII form is the same layout:
   `[✓]`/`[x]`, `(gloss)` in the footer, `▶`/`>`.
5. **Progressive footer.** Glosses through Stage 1 and on every cleared
   screen; words only from Stage 2.
6. **Capability-first recap.** "find where you are   pwd", not "pwd".

## 2. The three changes the operator asked for (brief §4)

1. **Identity line.** `shelltutor` left, `working in a Unix shell` right,
   on the welcome box's first row (§5.3). Help text follows. The stage-5
   title "Ready for vimtutor" stays: that stage does hand off; the phrase
   to retire is "prerequisite course".
2. **Breathing room above the prompt.** Yes, and move the footer *above*
   the lower rule, then one blank row between the rule and the prompt.
   Today the footer sits under the rule, in the shell's zone, which blurs
   the panel model's one idea: everything below the rule is the real
   shell. Rule last; blank; prompt.
3. **Modern polish.** Items 1–3 of §1 are most of it. The `┃` bar and the
   `▶` line already share a language (yellow, column 1, "the tutor
   speaking"); keep that and say it as a rule. No left margin on the
   panel: the prompt has none, so an indented panel would look offset
   from the shell it sits above.

## 3. The ten questions (brief §5)

1. **Hierarchy without fonts.** Yes, colour is over-used. Hierarchy comes
   from position and whitespace first, glyph prefixes second, colour
   third, because colour is the channel that vanishes (`NO_COLOR`,
   colour-blind learners, light themes). Body palette: bold, green, grey,
   yellow; red rarely; paths plain. Cyan, magenta and blue leave the
   body. §5.2 and §6.2 are the same screen with and without colour; it
   scans either way because the typeable block is the only indented
   thing and `▶` is the only line between a blank and the footer.
2. **The `▶` line.** It should be the loudest element and already has the
   right tools: the glyph, yellow, and isolation. Give it the isolation:
   a blank row above and below, always. Bold no other whole line, so it
   is the only bright line between body and footer.
3. **The header.** Drop the product name on lesson and gate screens; keep
   it on welcome, stage intro, cleared and finale, where the learner
   pauses. Drop the position prefix from the title. The header then
   carries two facts: where you are, how far along. Nothing moves to the
   footer.
4. **Footer.** Glosses through Stage 1 and on cleared screens (a pause
   with a changed primary verb); words only from Stage 2. Use parentheses
   for the gloss, not `▸`: its ASCII form is `>`, which the learner meets
   as redirection in Stage 4, and `check > test your work` is a bad thing
   to print beside a prompt. `(gloss)` is width-stable in both forms.
5. **Tutor speech beside a live prompt.** A left bar is right; it is the
   terminal's quotation mark. Two changes: the recall input prompt becomes
   `┃ ? ` (a question-mark prompt is a known CLI convention and looks
   nothing like `shelltutor> `), with "answer in words" said once in the
   gate intro, not on every line; and questions wrap at 76 columns under
   the bar with the options on their own row. The brief's Q1 is 105
   characters and wraps badly today. §5.4 shows `1 of 3`, two misses, and
   the hint arriving on the second miss.
6. **Gate checklist.** Brackets: `[✓]` / `[ ]`, which become `[x]` / `[ ]`
   at the same width. Align the reason in a column and label it `seen:`,
   which states what the gate observed, in the baseline's own "What I
   see" register. Reasons are observations ("still in the stage folder"),
   never instructions ("make the folder first, then cd into it" names
   the answer and belongs on the ladder's hint rung).
7. **Density.** One skeleton: framing or model (≤ 2 lines); one typeable
   block of 1–3 commands, each with a short aside; one "notice" line
   (≤ 2); the `▶` line. Body ≤ 12 rows. Exactly one typeable block per
   lesson; a lesson that needs two is two lessons, which is the split
   rule already in force. Troubleshooting prose ("if bash says command
   not found…") leaves every lesson and lives once, in 1.2 or on the
   ladder. The brief's 1.1 goes from 15 body rows to 10 (§5.1 → §5.2)
   with nothing taught lost.
8. **ASCII fallback.** Choose glyphs whose ASCII twin has the same width,
   so only the texture changes: `▶ >`, `┃ |`, `─ -`, `● #`, `◉ *`, `○ -`,
   `[✓] [x]`, `(gloss)`. Drop `✓ → ok` wherever it would shift a column;
   the cleared title is "Stage 2 cleared" with no tick. The header's `·`
   becomes `:`.
9. **Cleared screen and finale.** Lead with what the learner can do,
   command second. Calmer, memorable (capability is what a ten-year-old
   keeps), and a statement of competence rather than a reward. The finale
   is the same table grouped by stage, plus one closing block for the
   four habits the course taught: read before you run, predict, know
   where you are, list before you remove.
10. **Wide terminals.** Left-aligned, rule fixed at 80. Centring fights
    the prompt, which is always at column 1. What you do now is right;
    close the question.

## 4. The sheet

**Lesson skeleton** (panel ≤ 19 rows; prompt lands on row 21):
header · blank · Title · blank · model (≤ 2) · blank · one typeable block
(1–3) · blank · notice (≤ 2) · blank · `▶` line · blank · footer · rule ·
blank · prompt. Body ≤ 12 rows.

**Colour in the body**

| Role | SGR | Marks | Change |
| --- | --- | --- | --- |
| bold | 1 | a concept or key being named | replaces cyan and magenta in the body |
| green | 92 | something you can type | unchanged |
| grey | 90 | `#` asides, footer glosses, unreached dots, stage title in header | unchanged |
| bold grey | 1;90 | the navigation words in the footer | replaces magenta |
| yellow | 93 | `▶`, `┃`, current-stage dot: the tutor speaking | unchanged |
| red | 91 | the word that matters, not the line | rare |
| bold white | 1;97 | screen title | unchanged |
| green | 92 | `✓` in `[✓]`, filled dots | unchanged |
| plain | — | paths | was blue |
| grey | 90 | rules and box drawing, never text | unchanged |

**Width-stable pairs** (UTF-8 → ASCII): `▶ >`, `┃ │ |`, `─ -`, `● #`,
`◉ *`, `○ -`, `[✓] [x]`, `[ ] [ ]`, `(gloss) (gloss)`, `· :`, corners `+`.
The substitution is tied to the plain-text path (`NO_COLOR`, non-TTY) and
`SHELLTUTOR_ASCII=1`, never to locale detection: the harness runs under
`LC_ALL=C` and its sentinels contain `▶` and `✓`.

**Footer forms**

- lessons, Stage 1: `next (go on)   show (this screen again)   prev (back)   quit (save and leave)`
- lessons, Stage 2 on: `next   show   prev   quit`
- gate, recall phase: `show (the question again)   quit (save and leave)`
- gate, task phase: `check (test your work)   show (the task again)   quit (save and leave)`
- cleared: `next (Stage N+1)   quit (stop here, place saved)   show (this screen again)`

**Header**: `── Stage N · <title> ──…── ●◉○○○  N.k ──`; `gate` or `task` in
place of `N.k` at gates; no code and no current dot on the cleared screen.
Fixed 80 columns, left-aligned. Product name only on welcome, stage intro,
cleared and finale.

## 5. Mock-ups at 80 columns (UTF-8)

### 5.1 Today — lesson 1.1 as the brief renders it (23 rows)

```text
─ shelltutor ─ Stage 1 · Where am I? ────────────────────────────── ◉○○○○  1.1 ─

1.1 — running commands

At the prompt below, type this and press Enter:

  echo hello

You'll see hello printed, then the prompt comes back. Now try:

  echo I am at the shell      # spaces separate words
  echo "I am at the shell"    # quotes group them into one
If bash says command not found or No such file, you mistyped: a stray
/ in front, or a missing space. Type it again.

echo just repeats its words back. It is the simplest command
there is, and its shape is the shape of every command you'll meet:
a name, then the words you hand it.

▶ Try all three, then type next.
────────────────────────────────────────────────────────────────────────────────
next ▸ go on   show ▸ this screen again   prev ▸ back   quit ▸ save and leave
shelltutor> 
```

### 5.2 Proposed — lesson 1.1, same content, new skeleton (17-row panel)

```text
── Stage 1 · Where am I? ───────────────────────────────────────── ◉○○○○  1.1 ──

Running a command

A command is a name, then the words you hand it. echo is the simplest
one: it repeats its words back to you.

  echo hello                   # prints hello, then the prompt returns
  echo I am at the shell       # spaces separate the words
  echo "I am at the shell"     # quotes make them one word

Notice the quotes never print. They only group.

▶ Try all three, then type next.

next (go on)   show (this screen again)   prev (back)   quit (save and leave)
────────────────────────────────────────────────────────────────────────────────

shelltutor> echo hello
hello
shelltutor> 
```

### 5.3 Welcome — identity line and course map

> Superseded 2026-11-09 by `docs/operator-review-welcome-2026-11-09.md`
> (O-AW, O-AX; amendment A12): the course map is vertical and inside the
> box, the dots row and the sandbox row are removed, and on-screen copy says
> "practice folder". The mock-up below is kept as the record of the proposal.

```text
╭──────────────────────────────────────────────────────────────────────────────╮
│  shelltutor                                         working in a Unix shell  │
│                                                                              │
│  Five stages. Each is a few short lessons, then one task you have to pass.   │
│  No timer, no score. Try as many times as you like.                          │
│                                                                              │
│  Everything you type runs in a real shell. The tutor only writes inside      │
│  its own sandbox folder; what you run yourself is really run.                │
│                                                                              │
│  ▶ Type next to begin.                                                       │
╰──────────────────────────────────────────────────────────────────────────────╯

 ○○○○○  Where am I?  Paths  Files  Commands and streams  Ready for vimtutor

next (go on)   show (this screen again)   prev (back)   quit (save and leave)
────────────────────────────────────────────────────────────────────────────────

shelltutor> 
```

### 5.4 Gate — recall in the bar, `?` prompt, two misses

```text
── Stage 1 · Where am I? ──────────────────────────────────────── ◉○○○○  gate ──

Stage 1 gate

Three questions, then one task. Answer the questions in words; here you
are talking to the tutor, not to the shell. All three must be right.
Take as many tries as you need.

▶ Answer below.

show (the question again)   quit (save and leave)
────────────────────────────────────────────────────────────────────────────────

┃ 1 of 3   In an ordinary bash window (not this tutor), which character
┃          usually ends the prompt?
┃          $    ;    :    #
┃
┃ ? ;
┃ not quite. try again.
┃ ? :
┃ not quite. hint: picture a plain terminal, not the tutor's own prompt.
┃ ? 
```

### 5.5 Gate — task, then the checklist after `check`

```text
── Stage 2 · Paths ────────────────────────────────────────────── ●◉○○○  task ──

Task: make a folder and step into it

Starting in the stage folder.

  1. Make a folder called practice.
  2. Step into it.
  3. Type check.

▶ Do the steps, then type check.

check (test your work)   show (the task again)   quit (save and leave)
────────────────────────────────────────────────────────────────────────────────

shelltutor> mkdir practice
shelltutor> check
┃ [✓] a folder called practice exists
┃ [ ] you are inside it                 seen: still in the stage folder
┃ Finish the step marked [ ], then type check again.

shelltutor> 
```

### 5.6 Stage cleared — capability first, command second

```text
── Stage 2 · Paths ──────────────────────────────────────────────────── ●●○○○ ──

Stage 2 cleared

You can now

  find where you are           pwd
  see what is here             ls        ls -p
  move                         cd        cd ..     cd ~
  make a folder                mkdir

Next: Stage 3 · Files

▶ Type next to go on, or quit to stop here. Your place is saved.

next (Stage 3)   quit (stop here, place saved)   show (this screen again)
────────────────────────────────────────────────────────────────────────────────

shelltutor> 
```

### 5.7 A Stage 2 lesson with the short footer

```text
── Stage 2 · Paths ─────────────────────────────────────────────── ●◉○○○  2.3 ──

What's here

ls lists what is in the folder the shell is standing in. Folders are
marked with a slash so you can tell them apart from files.

  ls                           # the names, side by side
  ls -p                        # the same, with / after each folder

Notice stage1/ in the second listing: the slash means a folder you
could step into.

▶ Run both, then type next.

next   show   prev   quit
────────────────────────────────────────────────────────────────────────────────

shelltutor> ls -p
numbers.txt   poem.txt   stage1/
shelltutor> 
```

## 6. The same mock-ups in ASCII (`SHELLTUTOR_ASCII=1`, colour off)

Generated from §5 by the substitution table in §4. Columns are identical.

### 6.1 Today — lesson 1.1

```text
- shelltutor - Stage 1 : Where am I? ------------------------------ *----  1.1 -

1.1 — running commands

At the prompt below, type this and press Enter:

  echo hello

You'll see hello printed, then the prompt comes back. Now try:

  echo I am at the shell      # spaces separate words
  echo "I am at the shell"    # quotes group them into one
If bash says command not found or No such file, you mistyped: a stray
/ in front, or a missing space. Type it again.

echo just repeats its words back. It is the simplest command
there is, and its shape is the shape of every command you'll meet:
a name, then the words you hand it.

> Try all three, then type next.
--------------------------------------------------------------------------------
next > go on   show > this screen again   prev > back   quit > save and leave
shelltutor> 
```

### 6.2 Proposed — lesson 1.1

```text
-- Stage 1 : Where am I? ----------------------------------------- *----  1.1 --

Running a command

A command is a name, then the words you hand it. echo is the simplest
one: it repeats its words back to you.

  echo hello                   # prints hello, then the prompt returns
  echo I am at the shell       # spaces separate the words
  echo "I am at the shell"     # quotes make them one word

Notice the quotes never print. They only group.

> Try all three, then type next.

next (go on)   show (this screen again)   prev (back)   quit (save and leave)
--------------------------------------------------------------------------------

shelltutor> echo hello
hello
shelltutor> 
```

### 6.3 Welcome

> Superseded 2026-11-09 by `docs/operator-review-welcome-2026-11-09.md`
> (O-AW, O-AX; amendment A12): the course map is vertical and inside the
> box, the dots row and the sandbox row are removed, and on-screen copy says
> "practice folder". The mock-up below is kept as the record of the proposal.

```text
+------------------------------------------------------------------------------+
|  shelltutor                                         working in a Unix shell  |
|                                                                              |
|  Five stages. Each is a few short lessons, then one task you have to pass.   |
|  No timer, no score. Try as many times as you like.                          |
|                                                                              |
|  Everything you type runs in a real shell. The tutor only writes inside      |
|  its own sandbox folder; what you run yourself is really run.                |
|                                                                              |
|  > Type next to begin.                                                       |
+------------------------------------------------------------------------------+

 -----  Where am I?  Paths  Files  Commands and streams  Ready for vimtutor

next (go on)   show (this screen again)   prev (back)   quit (save and leave)
--------------------------------------------------------------------------------

shelltutor> 
```

### 6.4 Gate — recall

```text
-- Stage 1 : Where am I? ---------------------------------------- *----  gate --

Stage 1 gate

Three questions, then one task. Answer the questions in words; here you
are talking to the tutor, not to the shell. All three must be right.
Take as many tries as you need.

> Answer below.

show (the question again)   quit (save and leave)
--------------------------------------------------------------------------------

| 1 of 3   In an ordinary bash window (not this tutor), which character
|          usually ends the prompt?
|          $    ;    :    #
|
| ? ;
| not quite. try again.
| ? :
| not quite. hint: picture a plain terminal, not the tutor's own prompt.
| ? 
```

### 6.5 Gate — checklist

```text
-- Stage 2 : Paths ---------------------------------------------- #*---  task --

Task: make a folder and step into it

Starting in the stage folder.

  1. Make a folder called practice.
  2. Step into it.
  3. Type check.

> Do the steps, then type check.

check (test your work)   show (the task again)   quit (save and leave)
--------------------------------------------------------------------------------

shelltutor> mkdir practice
shelltutor> check
| [x] a folder called practice exists
| [ ] you are inside it                 seen: still in the stage folder
| Finish the step marked [ ], then type check again.

shelltutor> 
```

### 6.6 Stage cleared

```text
-- Stage 2 : Paths ---------------------------------------------------- ##--- --

Stage 2 cleared

You can now

  find where you are           pwd
  see what is here             ls        ls -p
  move                         cd        cd ..     cd ~
  make a folder                mkdir

Next: Stage 3 : Files

> Type next to go on, or quit to stop here. Your place is saved.

next (Stage 3)   quit (stop here, place saved)   show (this screen again)
--------------------------------------------------------------------------------

shelltutor> 
```

### 6.7 Stage 2 lesson, short footer

```text
-- Stage 2 : Paths ----------------------------------------------- #*---  2.3 --

What's here

ls lists what is in the folder the shell is standing in. Folders are
marked with a slash so you can tell them apart from files.

  ls                           # the names, side by side
  ls -p                        # the same, with / after each folder

Notice stage1/ in the second listing: the slash means a folder you
could step into.

> Run both, then type next.

next   show   prev   quit
--------------------------------------------------------------------------------

shelltutor> ls -p
numbers.txt   poem.txt   stage1/
shelltutor> 
```


## 7. Implementation notes

- **Package.** One rendering-only package, as the brief's §6 says. If the
  chrome package (WP-15) has not landed, these replace its spec; if it has,
  this is the next package number.
- **Sentinels that change.** Lesson titles lose the `N.k — ` prefix, so
  every title sentinel is re-pointed. The gate feedback's first line is no
  longer "Almost — you still need to"; the `second-try` oracle asserts the
  `[ ]` checklist line instead. The recall prompt text becomes `? `.
  Nothing in lesson bodies changes in this package.
- **Row budget.** Panel ≤ 19 rows including header, footer and rule; the
  prompt lands on row 21 after the blank. Body ≤ 12. The ASCII form has the
  same row count by construction.
- **Footer** is a function of (stage, screen kind): full glosses for stage
  1 and for cleared screens; otherwise words only. The gate's recall and
  task phases have their own forms (§4).
- **Colour roles.** `SUB`, `KEY` and `DIR` retire from lesson bodies; a
  `BOLD` role (SGR 1) replaces them for named concepts and keys. Footer
  words are `1;90`. Nothing else in the role table moves.
- **Glyph substitution** lives in one function on the existing plain-text
  path, plus `SHELLTUTOR_ASCII=1`. Add `·`→`:` and the brackets to the
  table the brief lists.
- **Identity.** Welcome row 1 as in §5.3; `-h` text and `--info` follow;
  the stage-5 title is unchanged.

Defaults the operator can overrule: retire cyan, magenta and blue from the
body (default yes); product name off lesson and gate headers (default off);
progressive footer (default yes); `?` as the recall prompt (default yes);
`(gloss)` in place of `▸` (default yes).
