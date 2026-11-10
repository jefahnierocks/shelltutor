---
title: WP-31 — Matcher: local negation, yes/no questions, arrow pairing (F-034..F-039) — awaiting operator approval
category: planning
component: workplan
status: drafted
version: 0.1.0
last_updated: 2026-11-10
tags: [workplan, recall, matching, round8]
priority: high
---

# WP-31 — Matcher: local negation, yes/no questions, arrow pairing

**Governing text**: `audit/2026-11-09/walkthroughs.md` round 8 (F-034..
F-039, the matcher table, the 42 wrong-answer probes, the rule-evidence
table). **Status**: drafted for operator approval; nothing is implemented.
**Tier**: core standard. Changes C-006 (matching semantics).

## The evidence

When two personas answered every recall question as a sentence in their
own words, 10 of 39 attempts were rejected, and all 10 were correct. No
wrong answer was accepted. By rule: the negation guard 4 (all at "after
rm, where is the file?"), exact-only matching 5 (all at "did the file on
disk change?"), a missing group phrase 1, the ordering rule 1. Over all
material so far the negation guard has rejected four correct learner
answers and no wrong learner answer; it does still stop 18 constructed
wrong answers, so it cannot simply be removed.

## Proposed semantics

1. **Negation is local (F-034).** Today any negation word anywhere in the
   answer rejects it. New rule: an answer is rejected for negation only
   when a negation word stands within the three words before the phrase
   that would have matched ("not to the screen", "does not go up one
   level", "only appends"). A negation elsewhere ("it is gone and you
   can't get it back") does not count.
2. **A reject phrase is ignored when it is itself negated** (a negation
   word within the four words before it): "doesn't go to the trash" and
   "there is no Trash" pass; "it goes to the trash" is rejected.
3. **Yes/no questions get a leading-answer rule (F-035).** A question may
   declare `--starts`: the answer passes when it begins with one of the
   listed openings and contains no un-negated reject phrase. Stage 5 Q3
   uses `--starts 'no|nope|unchanged|it did not|it didnt|the file did
   not|nothing changed|it stays|the file stays|it stayed|the file stayed'`
   with rejects `yes|it changed|did change|was changed|changed the file`.
   Its exact forms stay.
4. **Arrow pairing replaces the ordering rule (F-036).** At Stage 4 Q2
   each arrow named in the answer (`>`, `>>`, or the words single/double,
   one arrow/two arrows) is bound to the first group word that follows it;
   `>` must bind to an overwrite word and `>>` to an append word, in
   either order. An answer that names no arrow passes when both groups
   appear. This also closes the limit recorded in C-006 (arrows swapped
   with the words in lesson order). `--ordered` is removed.
5. **Stage 1 Q2 phrases (F-037) and its false accepts (F-038).** Group
   gains `which folder|what folder|folder youre in|folder you are
   in|folder im in|current folder|current directory|working
   directory|directory you are|directory youre in|where you are|where i
   am|full location|full name`; rejects gain `lists|list|deletes|delete|
   changes|change|icon|files`.
6. **Stage 3 Q2 rejects (F-038).** `in the trash|to the trash|trash|
   recycle|bin|undo|comes back|come back|kept|on the disk|on disk|moved|
   another folder|until|depends`, each subject to rule 2, so "no undo"
   and "not in the trash" pass.

## Corpus (FF-011)

Every own-words answer of round 8 becomes a row with its true verdict
(the ten rejected-correct ones as accept rows), and all 42 wrong-answer
probes become reject rows, including the ten that pass today. The worker
may tune the two window sizes (three and four words) only if the corpus
demands it, and reports the final values and any row that cannot be
satisfied.

## Copy

7. **Stage intros say what is true (F-039).** Stage 3: "This stage runs in
   its own folder, stage3, empty to start; pwd shows it." Stage 4 keeps
   "a few files the tutor put there". Stage 5: "with one file the tutor
   put there".
8. **5.2 (O-BS).** Notice gains: "If Vim suggests :qa, that works too."

## Considered and not proposed

- Removing the negation guard: 18 constructed wrong answers would pass.
- A new line on repeated hints (O-BR): the earlier "answer shape" line
  was judged unhelpful by all three personas and removed; fixing the
  matcher removes the cause.
- `type words.txt` (O-BQ), stray-slash help beyond 1.1 (O-BT), the
  backslash dropped from bash's own reply (O-BU): bash's messages are not
  ours to change, and each learner recovered.

## Commits (after approval)

1. `feat(recall): negation is local to the matched phrase; negated reject phrases ignored (F-034)`
2. `feat(recall): --starts for yes/no questions; Stage 5 Q3 (F-035)`
3. `feat(recall): arrow pairing at Stage 4 Q2; --ordered removed (F-036)`
4. `fix(recall): Stage 1 Q2 phrases and rejects; Stage 3 Q2 rejects (F-037, F-038)`
5. `feat(check): corpus rows from round 8 — own-words answers and 42 wrong-answer probes`
6. `fix(copy): stage intros state their folders truthfully; :qa in 5.2 (F-039, O-BS)`
7. `chore: C-006, CONTRIBUTING, FF-009 reads --starts; records; STATUS`
