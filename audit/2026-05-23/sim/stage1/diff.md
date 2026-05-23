---
title: Stage 1 simulation — current-rc vs no-system-rc-preview
category: audit
component: stage1-sim
status: evidence
version: 0.1.0
last_updated: 2026-05-23
tags: [audit, simulation, stage1, diff]
priority: medium
---

# Stage 1 baseline — variant diff

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
 
-Your work happens in /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-d43txb1k; the tutor never writes
+Your work happens in /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-r__uokua; the tutor never writes
 outside that folder.
 
 ▶ Type next for a quick orientation.
@@ -152,7 +152,7 @@
 verlyn13
 shelltutor> pwd
 
-/var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-d43txb1k/stage1
+/var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-r__uokua/stage1
 shelltutor> date
 
 Sat May 23 10:31:07 AKDT 2026
@@ -164,7 +164,7 @@
   your answer: verlyn13
 
 What did pwd print? (paste the full path)
-  your answer: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-d43txb1k/stage1
+  your answer: /var/folders/jx/f_4n055973x5cwnyh_mhlw9h0000gn/T/shelltutor-sim-home-r__uokua/stage1
 
 What day of the week did date show? (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
   your answer: Sat
```
