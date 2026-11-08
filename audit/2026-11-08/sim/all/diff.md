---
title: Five-stage simulation — current-rc vs no-system-rc-preview
category: audit
component: sim-all-stages
status: evidence
version: 0.1.0
last_updated: 2026-11-08
tags: [audit, simulation, all-stages, diff]
priority: medium
---

# Five-stage baseline — variant diff

Unified diff of the OUT-direction UTF-8 chunks of each variant's
`terminal.jsonl`, CRLF-normalized. Per
`docs/simulation-design-plan.md` §Slice 1, this diff is the
input to the Slice 2 hardening decision: the predicted
divergence is the `/etc/bashrc` leak signature when the host
rcfile injects banner output, aliases, or prompt-affecting state
into the practice subshell.

```diff
--- current-rc/terminal.jsonl (out, normalized)
+++ no-system-rc-preview/terminal.jsonl (out, normalized)
@@ -7,7 +7,7 @@
 task to advance. Retry as much as you like — no time pressure, no
 skip.
 
-Your work happens in /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh; the tutor never writes
+Your work happens in /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j; the tutor never writes
 outside that folder.
 
 ▶ Type next for a quick orientation.
@@ -155,10 +155,10 @@
 verlyn13
 shelltutor> pwd
 
-/var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh/stage1
+/var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j/stage1
 shelltutor> date
 
-Sat Nov  7 16:54:00 AKST 2026
+Sat Nov  7 16:54:04 AKST 2026
 shelltutor> check
 
 Three short follow-ups based on what you saw.
@@ -167,7 +167,7 @@
   your answer: verlyn13
 
 What did pwd print? (paste the full path)
-  your answer: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh/stage1
+  your answer: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j/stage1
 
 What day of the week did date show? (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
   your answer: Sat
@@ -285,7 +285,7 @@
   cd ..         # go up one level (to the parent folder)
 
 This tutor's sandbox is the practice subshell's starting folder,
-so you'll always start at /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh when a lesson opens.
+so you'll always start at /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j when a lesson opens.
 If you wander, cd ~/.shelltutor brings you back.
 
 ▶ Type next to continue.
@@ -305,7 +305,7 @@
 
 shelltutor> cd ~/.shelltutor
 
-bash: cd: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-userhome-ax_3au4d/.shelltutor: No such file or directory
+bash: cd: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-userhome-l1vn1_e6/.shelltutor: No such file or directory
 shelltutor> next
 
 2.3 — paths: relative, absolute, dot, dot-dot
@@ -373,7 +373,7 @@
 
 shelltutor> pwd
 
-/var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh/stage2/practice
+/var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j/stage2/practice
 shelltutor> check
 
 
@@ -383,7 +383,7 @@
 
 Three lessons, then a gate. You'll create, read, copy, move, and remove
 files. rm is immediate. It does not move things to a trash.
-We'll do everything inside /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh/stage3 so practice is
+We'll do everything inside /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j/stage3 so practice is
 contained.
 
 Commands this stage:
@@ -458,7 +458,7 @@
 
 shelltutor> cat ~/.shelltutor/poem.txt
 
-cat: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-userhome-ax_3au4d/.shelltutor/poem.txt: No such file or directory
+cat: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-userhome-l1vn1_e6/.shelltutor/poem.txt: No such file or directory
 shelltutor> next
 
 3.3 — copy, move, delete
@@ -513,7 +513,7 @@
 
 STAGE 3 — GATE TASK
 
-You will work inside /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh/stage3.
+You will work inside /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j/stage3.
 
 Do these, in order:
 
@@ -731,7 +731,7 @@
 
 STAGE 4 — GATE TASK
 
-Work inside /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh/stage4.
+Work inside /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j/stage4.
 
 Do these:
 
@@ -911,7 +911,7 @@
 Linking: gcc   -L/usr/local/lib -o vim        -lm -lncurses  -liconv -framework Cocoa           
 shelltutor> vim
 
-~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               VIM - Vi IMprovedversion 9.1.1752by Bram Moolenaar et al.Vim is open source and freely distributableHelp poor children in Uganda!type  :help iccf<Enter>       for information type  :q<Enter>               to exit         type  :help<Enter>  or  <F1>  for on-line helptype  :help version9<Enter>   for version info:q
+~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               VIM - Vi IMprovedversion 9.1.1752by Bram Moolenaar et al.Vim is open source and freely distributableBecome a registered Vim user!type  :help register<Enter>   for information type  :q<Enter>               to exit         type  :help<Enter>  or  <F1>  for on-line helptype  :help version9<Enter>   for version info:q
 shelltutor> next
 
 5.3 — buffer vs file
@@ -1072,7 +1072,7 @@
 (type check when done — or show, prev, quit)
 shelltutor> vim practice.txt
 
-"practice.txt" 1L, 7Bbefore
+"practice.txt"before
 ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               ~                                                                               i -- INSERT --after before^[  :wq
 "practice.txt" 1L, 13B written
 
@@ -1116,5 +1116,5 @@
 Re-take any stage at any time:
   shelltutor 1   # replay Stage 1
 
-Sandbox stays at /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-ef9gu0qh if you want to keep playing.
-
+Sandbox stays at /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-1f8b8m7j if you want to keep playing.
+
```
