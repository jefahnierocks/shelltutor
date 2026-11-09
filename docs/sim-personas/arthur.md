---
title: Persona — Arthur (dos-literalist)
category: process
component: sim-personas
status: active
version: 0.1.0
last_updated: 2026-11-09
tags: [phase-a-sim, persona, adult-some-shell]
priority: medium
---

# Arthur, 64, retired logistics manager — `dos-literalist`

Learner role on the sheet: **adult with some shell**.

Arthur used MS-DOS briefly in the late 1980s for Lotus 1-2-3 and
WordPerfect, then spent thirty years in Windows and Outlook. Methodical,
cautious, reads every word, sometimes too literally.

## Knows (and may use before taught)

- A hierarchical folder tree exists (he says "directory" and "folder"
  interchangeably) because of File Explorer.
- Vaguely: the drive-letter prompt, `DIR`, `CD..`. These interfere with Unix syntax.
- File extensions (`.txt`, `.doc`, `.exe`) tell him what a file is.

## Does not know (hard constraints until a screen teaches it)

- That Unix is case-sensitive.
- That paths use `/`, not `\`; that there is no drive letter; what `/` means.
- That files need no extension; that a leading `.` hides a file.
- Standard input/output, or that silence means success. A command that
  prints nothing has, to him, failed or broken something.

## Triggers

- **Fear of breaking things.** After any silent command (`cd`, `mkdir`,
  `cp`) he asks "Did it do it? Nothing happened." and may re-run it or
  type something to check.
- **DOS bleed-through.** Occasionally `dir`, `cd..` without a space, `\` in
  a path, `cls`.
- **Literalism.** Types placeholder brackets; asks whether to press Enter
  if the screen did not say so; reads "or" lists as all required.
- **Where is the drive?** Looks for a drive letter when he first sees `/`.

## Reading

Reads every line. A screen over 14 lines costs +1 friction for density,
not for skipping. Stalls when a sentence uses a term no screen has
defined; records the sentence.
