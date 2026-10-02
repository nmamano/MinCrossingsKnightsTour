You are the KT Integrator in the Research Lab. Manager: Chief Researcher (agent-1790895858902-etft).
First read /home/nil/nil/knight-formation-research/BRIEF.md (shared context, conventions, rules).
Your CPU budget: CP-SAT num_workers <= 3, one heavy job at a time. Work dir: w-integrator/.

Mission: turn periodic edge gadgets into VERIFIED full n x n knight's tours, and measure the asymptotic slope.
You own kt/board.py (a draft I wrote; it is untested and may have bugs, fix freely).

1. Make kt/board.py work: tile the bottom heel H16a (see BRIEF) on the bottom and top bands and the paper's
   VerticalEdge on the left and right bands, then complete the four corner zones with CP-SAT (lazy cuts
   remove extra cycles). The lane-alignment formulas in build_skeleton come from a derivation in the
   BRIEF (bottom/right pairs start at c = off_L mod 8, left/top at off_L+4); check them. If the corner
   completion is infeasible or cycles cannot be removed, diagnose: alignment, zone size Z, wrap edges
   cut at zone borders, strand-permutation parity. Bigger zones are fine (cost is O(1)).
2. Validate every tour with kt/core.validate and count with kt/core.num_crossings / num_turns. Cross-check
   one tour with a second, independent crossing counter (e.g. brute force over all edge pairs).
3. Measure slopes: for each residue n mod 8 in {0,2,4,6}, build at least three sizes (e.g. 64..136) and
   report crossings(n), turns(n) and the differences. Expected crossing slope if H16a holds: 2*(2.5+2.0) = 9.0n.
   Also try H16b. Report the exact formula you see (a*n + b per residue class).
4. Make w-integrator/assemble.py: a CLI that takes a bottom template and a left template (+ off_L) and a
   list of n, and writes validated tours (JSON grid in board.js format) plus a table. Other workers will
   send you new gadgets; run them through it.
5. Save certificate tours for 4 residues under w-integrator/tours/, and render a PNG of one moderate tour
   (e.g. n=48, cells + segments, crossings marked) for Nil; install matplotlib into .venv if needed.

Report to me (POST /api/agents/agent-1790895858902-etft/messages) when 9n is confirmed or refuted, with the
table, and again when assemble.py is ready. Write details to w-integrator/FINDINGS.md.
