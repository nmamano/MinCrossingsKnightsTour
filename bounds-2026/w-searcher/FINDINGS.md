# KT Edge Searcher - findings (w-searcher/)

All dates 2026-10-02. "Checked" = passed w-searcher/verify.py (independent unrolled check: degrees,
every band cell on a path between two line ends, no cycle, crossings counted by geometry).

## Tools

- `lib.py` - template helpers (tile H16a / VE, template -> strip edges), CP-SAT run wrapper.
- `verify.py` - unrolled check for BOTH bottom and left gadgets (new: left). Confirms H16a, H16b
  (16 X / 8 cols), paper VerticalEdge (10 X / 4 rows, off=0).
- `search2.py` - CP-SAT strip model with a general PAIRING RULE in place of the lane rule
  (lane-free, or "every strand joins c < c' with (c mod M, c'-c) in an allowed set").
- `tm.cpp` - transfer-matrix solver. Sweeps the band column by column; state = pending edges across
  the cut + a label per pending end (terminal lane/line, partner end, or wildcard) + phase.
  Seeds = every capacity-valid cut with wildcard labels, so every state of every periodic gadget is
  reached. Min mean cycle (Howard) + exact integer Bellman-Ford certificate. Result = best rate over
  ALL periods at depth D. Modes:
  - NOLANE=1: only degree + no finite cycle (lane-free). Rigorous lower bound; the witness is checked.
  - RULE="M:r/d,...": pairing rule. Lines more than W behind the newest terminal get a wildcard
    label (no check). This is a relaxation, so the value is a rigorous LOWER BOUND for all periods;
    if the witness has wild=0, it is also attained (exact).
  - default: lane rule (s, off); same wildcard relaxation.
  - `TRACE=file` replays a template through the exact transitions (debug).
  Memory: bottom D=4 lane-aware runs need > 7 GB (not done). Lane-free bottom D=4: 4.8 M states, 2 min.
- `pairs.py` - pairing of a template as (c mod cper, d) = pair {c, c+d}.
- `menu_run.py`, `sweep_left.py`, `sweep_bottom.py`, `classes.py`, `make_menu.py` -> `MENU.md`.

## Lane rule (paper / H16 setting), s = 4

- Left, off=0: 2.5 X/row. Q=4,8 CP-SAT OPTIMAL for D=2..4. tm (relaxed lane rule, W=3, D=2..4):
  lower bound 2.5 for ALL periods, attained -> 2.5/row is optimal for every period at depth <= 4.
- Left, off=1: Q=4: 3.5/row; Q=8, D=4: 3.25/row (26 X / 8 rows, OPTIMAL, checked).
  tm D=4: 3.25 is optimal over all periods (certified, wild=0). D=2 infeasible.
  Template (Q=8, D=4, rows top first): 12 12 26 25 / 23 12 26 26 / 23 24 26 26 / 23 47 26 26 /
  03 47 26 25 / 03 17 25 25 / 01 17 25 25 / 12 17 25 25  (tm phase0=2: rotate rows to align).
- Bottom: P=8 D=5, P=8 D=6, P=16 D=4 (CP-SAT, H16a hint, 300-1200 s): no solution below
  2.0/col found; CP-SAT bound collapses to 0 at these sizes, so no proof. tm proof needs too much memory.
  STATUS: 2.0/col is optimal for P=8 D=4 only (earlier result); open for longer periods / deeper bands.

## Lane-free results (priority change, see MENU.md for the per-class menu)

- Left, any depth: 1.0 X/row (template `23 27`, D=2, pairing {c, c+3}, c odd). Matches
  w-lowerbounds F1 (1/row is also a lower bound for every strip width).
- Bottom, depth 3: >= 2.6 X/col (tm NOLANE, certified, all periods).
- Bottom, depth 4: exactly 11/6 = 1.833 X/col over ALL periods (tm NOLANE certified lower bound,
  attained by a checked P=6 gadget):
  `46 46 46 56 56 56 / 45 14 14 14 45 45 / 05 05 15 15 15 05 / 01 01 01 01 01 01`
  pairing {c, c+3} for c = 3,4,5 mod 6 (a 3-strand lane pattern; lane rule with s=3).

## Compatibility-filtered search (2026-10-02, 03:20-03:45)

Tool: `run_filtered.py` = CP-SAT (search2.py) in a loop with the Integrator's filter
(`filt.py`: w-integrator/strands.py union_profile, n=96, cycles 0 and all cuts even for some shift).
A rejected solution's pairing is forbidden and the solver runs again.
- Bottom vs left d3/odd (`23 27`): best passing gadget 19 X / 8 cols = 2.375/col (P=8 D=4, also a
  P=8 D=5 one), checked: `36 36 36 26 26 26 36 26 / 34 36 23 23 23 36 26 36 / 26 27 27 27 26 26 26 27 /
  67 67 67 67 67 67 67 06`, pairing (0,3),(2,3),(6,3),(7,5). FEASIBLE only (CP-SAT bound 0).
  Passing older rows: d=7 2.5 (period 2), d=1 3.0, d=5 3.0. Failing: d=3 (2-cycles), free 1.833.
  P=12 D=4: 26 X (2.167/col) solutions exist in the class "no {odd,odd+3} pair", the first two failed
  the filter; loop still running.
- Left vs right = rotated d3/odd (MID): every left gadget that passes must avoid all {odd, odd+3}
  pairs (K odd -> shared pair = 2-cycle). In that class the minimum is 2.0/row:
  CP-SAT OPTIMAL for Q=4,6,8 (D<=4), and tm RULE (relaxed, W=8) certifies >= 2.0/row for ALL periods
  at D=3 and D=4. So no left gadget below 2.0/row is compatible with a d3/odd right at depth <= 4.
  D=5 tm run needs > 5 GB (not done); CP-SAT Q=8 D=5 found 2.0 (bound 0).

## Transfer-matrix result for the bottom vs left d3/odd (2026-10-02, 04:30-05:20)

tm.cpp additions: PI=0/1 keeps only states of one matching-parity class (pi = #pending strand ends
that started at a terminal - newest terminal line, mod 2; invariant along valid transitions);
UNION=q tracks the union of the bottom matching with the left pairs {c, c+3}, c = q mod 2, and
rejects finite union cycles (bottom only, EXACT mode).
- EXACT, RULE "every pair allowed except {c,c+3} with c = 1 mod 2" (d <= 9), W=6 lines, W2=6 cols:
  PI=1: min 57/26 = 2.192/col (P=26). The witness PASSES the Integrator filter (odd xb, 2 strands).
  PI=0: min 2.1/col (P=10), but every PI=0 gadget gives an ODD cut count with left d3/odd at the
  cycle-free alignment (checked: UNION=1 PI=0 run, min 2.375, witness has 1 strand), so PI=0 is useless.
  So: over all periods at depth 4, among gadgets with strand drift <= 6 lines and U-turn extent
  <= 6 columns, the cheapest bottom gadget compatible with left d3/odd costs 57/26 = 2.192/col (exact).
  Template (rows top first):
  `36 56 56 56 56 56 56 56 56 56 56 56 46 46 46 56 56 56 46 36 26 26 26 36 36 36 /
   13 13 13 13 15 15 15 15 15 15 45 45 45 14 14 14 45 45 34 34 23 23 36 36 36 13 /
   27 27 12 12 12 12 12 15 15 15 15 05 05 05 15 15 25 05 25 25 27 25 26 26 27 27 /
   67 67 67 67 67 16 16 16 16 01 01 01 01 01 01 01 01 01 06 17 67 67 67 67 67 67`
- Same run with W=7, W2=7 (30 M states, 4.4 GB, 680 s): the same 57/26 gadget again. W=8/8 needs > 7 GB.
- CP-SAT with the filter in the loop (P=8..32): best 2.25 (P=12), 2.3125 (P=16), 2.375 (P=8);
  CP-SAT gives no bounds at these sizes.

## Independent certification of KT Lower Bounds window lemmas (2026-10-02, 06:00-07:05)

Method: own C++ exhaustive column sweep over ALL edge subsets (no solver), `w-searcher/cert/certify2.cpp`
(`certify.cpp` = first version, same results, slower). Instances written by my own generator
`cert/gen.py` from the statements (not their code). The frontier keeps the decided edges that can
still cross an undecided edge or touch an unfinished cell; output = full set of feasible phi values.
Tests: random small instances vs a Python backtracking enumerator (`cert/randtest.py`, `cert/brute.py`):
120 instances, 0 mismatches (many with non-empty flux sets).
- M3 (W=7, window [0,6]^2, frame [-2,8]^2 with degree <= 2, no proper crossing among candidate
  edges): all 4 instances used by the proof (h/v, OX=0/1, OY=0) plus OY=1: feasible phi sets
  {-1,2} or {-2,1}, always = chi(right cell) mod 3. Same for W=8: all 8 positions done, all agree
  (cert/m3_results.txt). Max 1.5 M frontier states (W=7), 25 s per instance; W=8 5.9 M, 90 s.
  Agrees with the CP-SAT sets in local_m3.py runs.
- NE-M3 (ne_m3.py statement, PAT in {P,P'}, r in {8,9}, j in 2..8): all 28 feasible sets are single
  values and IDENTICAL to w-lowerbounds/nem3_run.log (cert/ne_results.txt).
- Corner: the proof uses corner_charge2.py (a pure enumeration), not corner_neutral.py. Not re-checked:
  parked at 07:05 by the Chief Researcher's priority change (new proof does not use M3/NE-M3).

## Third-method certification of the finite inputs of the (4 + 1/17) n tour bound (2026-10-02, 07:10-07:40)

All code is my own C++ (`w-searcher/cert/`), written from the definitions, no solver, no reuse of
their Python. Each run takes < 1 s.
(1) Width-2 strip graph (`strip2.cpp`), model from the strip_dp.py definition (cells scanned by
  (row, column) over columns 0..3; strip cells 0,1 degree exactly 2; ghost cells 2,3 degree <= 2
  and may only go up to a strip cell; no cycle; arc weight = new proper crossings, min per target).
  - states 82,516, arcs 144,674: MATCH.
  - weights 4w-1: no negative cycle (mean >= 1/4 per transition). The zero-reduced-cost graph has
    exactly two cyclic components, each a 4-cycle (8 cycle arcs): MATCH.
  - Row certificate: the two cycles give exactly P and P' (neighbours of (0,y): (2,y+s),(1,y+2s);
    of (1,y): (3,y+s),(0,y-2s)), and the pending edges at the row start contain exactly one crossing
    pair, (0,-2)-(1,0) x (0,-1)-(2,0) for P and (1,-1)-(0,1) x (2,-1)-(0,0) for P': MATCH with
    FINDINGS section 7.2 of w-turnstheory.
  - (S) weights 20w - 5 - 4[non-cycle arc]: Bellman-Ford from a virtual source converges, potential
    range exactly [-149, 0]: MATCH. Weights 1000w - 250 - 201[non-cycle arc]: negative cycle found
    (length 12, total -10): MATCH (1/5 is sharp).
  - Note: T* (longest tight path after removing the cycle arcs) depends on the potential. With the
    virtual-source potential of 4w-1 I get 23 (acyclic), not 37. The 1/17 proof uses (S), not T*.
(2) Corner endpoint charge lemma, section 7.3 (`corner_charge.cpp`): for R = 12..15, all four
  pattern combinations, all 2,916 degree-2 choices at the 7 corner cells, sum of omega over Q_R
  = 1 mod 3 in every case (the raw sum is -2 for even R and 4 for odd R in every case). The program
  classifies every edge with a non-zero coefficient (middle boundary cell with coefficient
  -chi(cell) for ALL its possible edges / pattern cell / corner cell) and aborts otherwise: OK.
(3) Strip row certificate, section 7.1: covered by (1) (patterns and the pending crossing pair).
Result: no mismatch.

## Colour-current carriers for the fold design (2026-10-02, 08:00-10:45; STOPPED by the Chief Researcher)

Task (Chief Researcher): cheapest carrier of colour current +-1 (+-2) through a crossing-free
field, and a lower bound per unit length. Interface: KT Structures' seam model (w-structures/seam.py,
seam_flux.py); I asked KT Structures to confirm scope (no reply yet at 09:40).
Tools (w-searcher/carrier/):
- `band.cpp` + `band_gen.py`: transfer matrix for a straight band between two line fields, any
  orientation; lane-free (degree 2, no finite cycle); optional current target; BASE=<template>
  restricts to configurations reachable from and back to a given periodic family (needed: the
  current is constant along a band, and seeding all cuts is too large). Min mean cycle over all
  periods + Bellman-Ford certificate. Current = band-edge flux through a sweep cut, normalised;
  calibrated on Structures' p=6 w=3 templates (exact match for currents 0, +-1, +-2).
- `cps_band.py`: CP-SAT with Structures' Seam geometry (form checks relaxed), current through the
  transversal cut, kinds: diagfree, vert21, vert12, midfold, edgeA/B, diag21/12, anti21/12.
- `tpl2edges.py`, `fluxcal.py`: template conversion and flux calibration.

Results so far (10:20). "extra" = crossings above the plain field, per unit of Manhattan length
(diagonal kinds: per unit x / 2). CP-SAT OPTIMAL at the listed (p, w) unless noted; w <= 3, p <= 8:
| kind (cps_band.py) | +-1 extra | +-2 extra | at |
|---|---|---|---|
| diagfree (free fold A'|B') | 1/3 (= 2/3 per unit x) | 1/3 | p=6 w=3; band.cpp CERTIFIED all periods (reachable family) |
| diag21, diag12 (band along (1,1) in one family) | 1/3 | 1/3 | p=6 w=1 |
| vert12 (vertical band, steep family) | 0.75 | 1.0 | p=4 w=1 / p=2 w=1 |
| midfold (vertical midline (1,2)|(1,-2)) | 0.75 | 1.0 | p=4 w=1 / p=2 w=1 |
| vert21 (vertical band, shallow family) | 1.33 | 2.0 | p=6 w=2 |
| anti21 (band along (1,-1), family (2,1)) | 1.0 | 1.75 | p=2 w=2 / p=4 w=3 |
| edgeA (left edge, field (2,1)) | 1.0 per row | 1.5 | p=4 D=2 (matches Structures) |
| edgeB (left edge, field (1,2)) | 0 rel. to its own min, but +5/6 per row rel. to edgeA | - | band.cpp D=3 CERTIFIED (reachable families), see recheck below |
Raw rows: carrier/band_cps.jsonl; logs log_axis1.txt, log_axis2.txt (anti12 was still running).
KT Structures answers (09:50): only +-1 needed; F12 of KT Lower Bounds already has W=3,4 transfer
matrix numbers (diagonal 2/3, midline 3/4, edge 1, interior 3/2) - do not redo; useful: widths 5..6
exact, and anything below 2/3 per unit x. Their proposals (w-structures/FINDINGS.md S5): C1 along-line
corridor (band along (2,1) in the pure (2,1) field, no terminals, W=3..6, current +-1, rate per (2,1)
step; gate: < 1/3 per step beats the diagonal route), C2 diagfree W=5..8, C3 pleats (two close
parallel folds) and jog bands next to the diagonal fold, C4 lower bound per line crossed.
Lower bound (my argument, from w-turnstheory/FINDINGS.md 6.2, 6.4, 6.5; Verifier Claim 17: the counting is
sound, but the general theorem and the fold-family floor are NOT yet proved):
in a degree-2 periodic field the tiles' total area equals the cell count, so per period the
number of bad quarter triangles (uncovered or multiply covered) is at most 4X. If a band carries a
current that is not 0 mod 3 (relative to the plain field), every transversal dual path has a step
with omega != 0, hence an adjacent bad triangle, and a bad triangle serves only one of a set of
edge-disjoint paths. The max number of edge-disjoint transversal dual paths per period equals the
Manhattan length |Tx|+|Ty| of the period vector. So:
  crossings >= (Manhattan length of the route) / 4   for carrying current +-1 or +-2.
Diagonal free fold: 2/3 per unit x = 1/3 per Manhattan unit, against the bound 1/4.
Consequence: a corner charge must reach a cancelling charge; corner -> centre is Manhattan n, so
four corners via the centre cost >= n (now 4n/3); two adjacent pairs cost >= n/2 in total.

### edgeB recheck (2026-10-02 10:15-10:35, band.cpp, depth 3 = cells x in 0..3, all periods, reachable families)
Bases: OPTIMAL CP-SAT p=6 templates (eb_edgeB_p6_w3_c*.txt), NOCOREACH=1 (closure of everything reachable from the
base; current is conserved, CURHIST check: all 75,575 states have the base current).
| kind | current (cps_band value) | min per row | status |
|---|---|---|---|
| edgeA | 0 (plain) | 1.0 | CERTIFIED |
| edgeA | +1 | 2.0 | CERTIFIED |
| edgeB | -1 and 0 | 11/6 = 1.833 (period 6 rows) | CERTIFIED, both currents |
| edgeB | +1 and -2 | 2.5 | CERTIFIED |
Reading: the "0.0 extra" was real but misleading. The (1,2)-field left edge has TWO current classes at the same
minimum 11/6 per row, so it carries a relative +-1 (one sign per class) for free relative to ITSELF. But it costs
5/6 per row more than the steep edge P (edgeA, 1/row). 5/6 > 2/3, so it does not beat the diagonal route.
Depth 4: the closure did not finish in 500 s (2.1 GB); not done.

### C1 along-line corridor (2026-10-02 10:05-10:30) - closed
freeband.py: CP-SAT on the band |x - 2y| <= W in the pure (2,1) field (no fixed edges touch it), degree 2, lazy cuts
against finite cycles (quotient cycles with winding 0), current = plain + rel.
W=3: rel +-1 costs 2.0 per (2,1) step, OPTIMAL at p=2, 4 steps; p=6 FEASIBLE 2.0 (bound 0, 240 s).
band.cpp (kind c1, base = the p=2 +1 template, co-reachable family): 17 crossings per 12 steps = 1.417 per step,
CERTIFIED in that family. All values are >= 3/4 per step (the Manhattan bound) and far above the gate 1/3.
KT Structures closed C1 from the bound (w-structures S11); these numbers confirm it without Claim 17.

### Direction profile phi(v) in the uniform (2,1) field (2026-10-02 10:35, in progress)
phi(v) = min extra crossings per step v for a band along v carrying +-1. A route made of long straight legs costs
sum phi(leg) + O(1) per bend (ASSUMPTION: a bend between two legs with the same current costs O(1); not checked).
So the useful cost of a displacement is the CONVEX HULL of phi. Known (per step): phi(1,1) = 2/3, phi(1,0) = 0.75
(= vert12 by x<->y), phi(0,1) = 4/3 (vert21), phi(1,-1) = 2.0 (anti21), phi(2,1) >= 3/4 (C1: 1.417 in a family).
Corner pairing along an edge needs a horizontal displacement at < 2/3 per unit x. Candidate convex combinations:
  (3,0) = (1,1) + (2,-1): beats 2/3 per unit x iff phi(2,-1) < 4/3;  (4,0) = (1,1) + (3,-1): iff phi(3,-1) < 2.
For the steep regions (route parallel to the edge = vertical in the (2,1) field):
  (0,3) = (1,1) + (-1,2): iff phi(1,-2) < 4/3;  (0,4) = (1,1) + (-1,3): iff phi(1,-3) < 2.
Manhattan bound (if Claim 17 holds): phi(2,-1), phi(1,-2) >= 3/4; phi(3,-1), phi(1,-3) >= 1. So all four are open.
cps_band.py kinds d21_a_b (band along (a,b) in the (2,1) field, T = p (a,b)). First short-period values
(OPTIMAL): phi(2,-1) <= 3 (p=2, w=3 and 5); phi(3,-1) <= 4 (p=1, w=4).
Longer periods before the stop (10:45): phi(2,-1) = 3.0 per step OPTIMAL at w=3, p = 4, 6, 8; w=5 p=4 FEASIBLE 2.75
(bound 0, 300 s). Far above the gate 4/3. The other three directions were not run.

### Final state of the carrier task (2026-10-02 10:45, STOPPED: Nil accepts 19n/3; solidify only)
Status of each result (all numbers are extra crossings for carrying colour current +-1):
- Certified edge carriers (band.cpp, depth 3, all periods, reachable families): steep edge P (edgeA) 1/row plain and
  2/row with +-1, so +1/row extra. Shallow-field edge (edgeB) 11/6 per row for two current classes, i.e. +5/6 per row
  against P. Neither is below 2/3 per row.
- Diagonal free fold (diagfree): 2/3 per unit x = 1/3 per Manhattan unit, band.cpp CERTIFIED at width 3 (reachable
  family); KT Lower Bounds F12 has the same value at W=3,4. Width 5 was queued but not run.
- Midline (midfold) and vertical band in the steep field (vert12): best 0.75 per row, OPTIMAL at (p,w) = (4,1..3),
  (8,1); FEASIBLE only at p=6,8 with w=2,3 (60 s; p=6 w=2 also 600 s: 7/6 per row, bound 0). Not all periods: a value
  below 2/3 per row at a longer period is NOT excluded. band.cpp full closures at width 3 exceed 7 GB.
- vert21 4/3, anti21/anti12 1.0 per Manhattan unit, diag21/diag12 1/3 per Manhattan unit: CP-SAT, small (p,w) only.
- C1 (band along (2,1) in the (2,1) field): >= 1.417 per step (CERTIFIED in a family), 2.0 OPTIMAL at p <= 4. Closed.
- Lower bound (my argument, see above): crossings >= (Manhattan length of the route)/4. Verifier Claim 17: the
  counting is sound; the general theorem (every transversal dual path meets a bad triangle when the current is not
  0 mod 3, for every field and every band) is NOT yet proved. So all conclusions from it are conditional.
  If it holds: flux term >= n/2 (two adjacent-corner pairs), against 4n/3 now.
- Open questions left (not pursued, by order): midfold at long periods (< 2/3 per row would give a flux term
  below 4n/3); the convex-hull directions phi(1,-2), phi(3,-1), phi(1,-3) (gates 4/3, 2, 2 per step);
  KT Structures' layout G seam with one parity (gate c_seam < 5/3 per unit x; its CP-SAT gives 3.0 OPTIMAL at w <= 5).
Files: carrier/band_cps.jsonl (CP-SAT rows with templates), carrier/freeband.jsonl (C1), carrier/band.cpp
(+ NOCOREACH, CURHIST env options), band_gen.py kinds (diagfree, gentle, edgeA, edgeB, vert12, midfold, vert21, c1),
freeband.py (terminal-free bands, lazy cycle cuts), extend.py / run_ext.py (widen a template; not used for results).
Process note: from 10:32 to 10:42 two of my CP-SAT queues ran at the same time (a wrong PID in q_dir.sh). The brief
allows one heavy job; both are stopped now.
