# Gap mission: crossings 14n/3 vs 19n/3 (Chief Researcher, 2026-10-03)

STATUS: SPECULATIVE. Nothing here changes the audited results or the two blog posts.

## Goal
Narrow the gap between the bounds on the minimum number X of crossings of a closed knight's tour on an n x n board
(n even). Proved and audited (2026-10-02): 14n/3 - 407 <= X_min <= 19n/3 + 142. Nil cares about the leading
coefficient only (14/3 ~ 4.667 vs 19/3 ~ 6.333), not about additive constants. Any improvement on either side counts:
a lower bound above 14n/3, or a construction below 19n/3. A clear negative result (a proved floor or ceiling of a method)
is also a useful outcome. Turns are done (8n - 28 <= T_min <= 8n - 14); do not work on turns.

## Read first
- RESULTS.md (index of all proved results, proofs, check commands).
- The two final proofs: w-turnstheory/PROOF_fold.md (upper, 19n/3) and w-turnstheory/PROOF_crossings_lower.md (lower, 14n/3).
- The full self-contained versions are the appendices of writeup/crossings/post.mdx (audited Claim 23B).
- Conventions and code: BRIEF.md (old shared brief: geometry, move codes, kt/ code, venv), kt/core.py (validate,
  num_crossings).

## Known leads and dead ends (with pointers)
Upper bound (fold family, 19n/3 = edges 4n + arch fix n + colour flux 4n/3):
- Table of where the fold family can gain: w-structures/FINDINGS.md S9. Edges 4n: no room (proved 1/row).
- Arch fix (n): OPEN. Only route seen to o(n): 4-fold same-edge nests (S9 "Open"), untested in a crossing-free layout.
- Colour flux (4n/3): diagonal carrier 2/3 per unit x is certified optimal at width 3. Floor n/2 is CONDITIONAL on the
  unproved general theorem of Claim 17 (w-verifier/FINDINGS.md). Untested: midline (midfold) carriers at long periods
  (< 2/3 per row would beat 4n/3), convex-hull directions, layout G single-parity seam (gate c_seam < 5/3).
  Details: w-searcher/FINDINGS.md "Final state of the carrier task"; w-structures/FINDINGS.md S5-S11.
- DEAD: jog bands for 16n/3 (S8: self-carrying jog band does not exist); along-line corridor C1 (S11).
- Nobody has tried a construction OUTSIDE the fold family (all edges steep + free folds). No floor is proved for
  other designs.
Lower bound (14n/3):
- Next finite task, precisely specified: w-turnstheory/FINDINGS.md 11.3 (+ w-turnstheory/QUESTIONS.md). A strip certificate with
  beta > 1 gives X >= [4 + 2beta/(2beta+1)]n - O(1). 11.4 proves beta <= 4/3 in that strip model, so this task can
  reach at most 52n/11 ~ 4.727n.
- Beyond that the method needs new ideas: more defects per charged path, wider side windows, stronger endpoint tests,
  a tighter crossing budget, or the interior "boundary-like strip" of 11.4. Earlier false lemma: TILE_INPUTS.md 8.1
  (9.5 lemma, SAT counterexample).

## Team and assignment (each worker has a fresh session; read the files above before you start)
- KT Turns Theory (Astra): LOWER-bound theory. Find the next idea past 14n/3 (beyond 11.3), with honest status labels
  (PROVEN / ARGUMENT / CONJECTURE). Coordinate the 11.3 data with KT Lower Bounds through files.
- KT Lower Bounds (Opus): run the 11.3 finite computation (exact potential certificate, both orientations, both
  initial parities). Report beta and C, or the cycle that blocks it. Then support Turns Theory with finite checks.
- KT Structures (Opus): UPPER bound, arch term: test 4-fold same-edge nests in a crossing-free layout; and think past the
  fold family (any design with a provable rate below 19/3).
- KT Edge Searcher (Opus): UPPER bound, flux term: midfold carriers at long periods, then the open directions listed
  above. Exact or certified numbers only (OPTIMAL / CERTIFIED / FEASIBLE + bound).
- KT Integrator (Opus): first the repo migration (briefs/m_int_migrate.md); then full-tour assembly for any new design.
- KT Verifier (Astra): audits any claimed improvement, on request from the Chief Researcher.
- KT Lean: not used in this mission for now.

## Rules
- Write ONLY under gap/<your-short-name>/ (e.g. gap/turnstheory/, gap/lowerbounds/, gap/structures/, gap/searcher/).
  Everything else is READ-ONLY, in particular all audited proofs, w-*/ files, writeup/, kt/. Copy code you need.
- FINDINGS.md in your folder: dated entries, proof status labels, exact data (templates, certificates), commands.
- These files will be PUBLIC (synced to github.com/nmamano/MinCrossingsKnightsTour/bounds-2026/gap/). No secrets, no
  emails, no office URLs, no absolute /home paths in new files.
- A claim counts only after an independent check; a claimed improvement goes to the Verifier before anyone calls it a
  result.
- CPU: 8 cores shared by the whole office. At most ONE heavy job per worker, CP-SAT num_workers <= 2, check `uptime`
  first (back off if load > 10). Python venv: .venv/bin/python.
- Report to the Chief Researcher (agent-1790895858902-etft) at each milestone, at a dead end, or after about 3 hours
  without progress (verdict + what you would try next). Claude workers: POST the isomux messages API. Astra workers:
  your sandbox blocks POSTs; write the report at the top of your FINDINGS.md and end your turn.
- Do not contact Nil. Do not commit or push (the Integrator syncs the repo). Do not edit the blog posts.
- Context rule: Claude workers hand off at about 50% context at a natural break (state to your files, then POST your own
  /handoff with a short forward-looking brief).
- Use ASD-STE100 Simplified Technical English in written reports.
