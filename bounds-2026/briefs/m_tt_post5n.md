Chief Researcher -> KT Turns Theory (2026-10-03). Nil approved: update the CROSSINGS blog post to the new audited lower bound
X >= 5n - 612 (Claim 42). File: writeup/crossings/post.mdx (live preview http://127.0.0.1:21019/blog/knights-tour-crossings).
1. Appendix: replace part B (14n/3 - 407 proof) by the full self-contained 5n proof adapted from gap/turnstheory/PROOF_5N.md (same
   <details> format, code-font math, blank lines inside blocks). Keep the 4n - 2 tile bound in it. Every finite fact names its
   check command, run from the bounds-2026 folder (state that f1v_stab.py needs numpy etc., with run times). Do not change part A.
2. Body: rewrite "Part 2: why every tour needs about 4.67n crossings" for 5n: the cleaner story (each corner path pays half a
   crossing through the bad quarters of its middle; the side strips pay for the paths that lose their charge). Keep it short.
   Update the result Callout, "The gap" (now 5n vs 19n/3), "Open questions", and every 14n/3 / 4.67n mention (grep). Mention
   the intermediate audited bounds only if the post already lists steps; the progression chart will show them (Integrator).
3. Style: this copy goes out under Nil's name: keep the existing voice exactly (short sentences, plain words, no em dashes, no
   hype, no new subjective claims). Change only what the new result requires.
4. Check the MDX compile (node writeup/crossings/check_mdx.mjs) and that the preview returns 200.
5. Write a change list at the top of gap/turnstheory/FINDINGS.md: sections changed, word counts before/after (body and appendix).
Then end your turn; the Verifier audits the update (completeness + faithfulness, as in Claim 23B).
