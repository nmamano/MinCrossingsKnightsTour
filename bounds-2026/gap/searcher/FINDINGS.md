# KT Edge Searcher - gap mission findings (gap/searcher/)

Task (gap/BRIEF.md): UPPER bound, colour-flux term (now 4n/3 in the fold construction).
Labels: OPTIMAL / CERTIFIED (exact over all periods in the stated model) / FEASIBLE (upper bound only).
All dates 2026-10-03.

## 0. Status summary (latest first)

- 2026-10-03: exact transfer matrix `corr2.cpp` (own code, F12 corridor model, all periods, widths up to 6).
  CERTIFIED: diagonal fold carrier 2/3 per (1,1) step at W = 3..6; steep edge carrier +1 per row at W <= 5;
  axis fold (midfold) 3/4 per row at W <= 5; shallow edge 11/6 per row at W = 4, 5. Wider bands give nothing.
- The flux term 4n/3 is optimal for the fold layout given these carrier rates (section 1).
- Layout B'/B (shallow side edges, no flux, estimate 37n/6) is DEAD: shallow-steep corner nests trap (section 4).
- Midfold (axis-fold) carriers cannot lower the flux term in the fold layout at any rate (section 1).

## 1. Where an axis-fold (midfold) carrier could enter the flux network (ARGUMENT)

The four corner charges (+-1 mod 3) must be joined by carriers. In the fold layout:
- A corner touches only its diagonal fold (the only free ray from a corner) and its two edges.
- The axis folds (the four midlines, field pair (1,2)|(1,-2) up to rotation = kind `mid`) join edge midpoints to
  the centre. No corner lies on them. A route corner -> axis fold must first run along an edge (edge carrier,
  +1 per row) or along the diagonal (then it is already at the centre when it meets the axis fold).
- Example: BL corner -> bottom edge to (h,0) -> vertical midline to the centre costs (1 + r_mid) n/2 >= n/2,
  against n/3 for the diagonal. So the axis folds are not useful for corner flux, even at r_mid = 0.
- Off the folds: in the BL quadrant the left region has field (2,1) and the bottom region has field (1,2).
  A route between two corners needs a net axis displacement n. Vertical motion in the (2,1) region is the
  kind `vert21` (4/3 per row, F12 interior 3/2); horizontal motion in the (1,2) region is the same by symmetry.
  Diagonal legs give 1 unit of axis displacement for 2/3, whatever the route shape (star or side pairing):
  4n/3 in total. So the flux term drops below 4n/3 only with
  (a) a diagonal carrier below 2/3 per (1,1) step, or
  (b) a carrier below 2/3 per unit of axis displacement in a region that a corner-to-corner route can use
      (in the fold layout: vert21-type bands, or the edges at +1 per row now).
  The previous "midfold < 2/3 per row" gate is real only for a layout in which charges sit on an axis fold.
  None is known.

## 2. Exact corridor transfer matrix (corr.cpp, corr2.cpp)

Model (same as KT Lower Bounds F12, re-implemented in C++ from the definition, not from corr_dp.py):
route direction (A,1); band = W cells per row (u = x - A y - OFF in [0,W)); band cells have degree exactly 2,
any knight move inside the band; outside cells keep their base field edges; an edge between a band cell and an
outside cell is allowed only if it is a base edge, and then it is forced; no finite cycle. Weight = proper
crossings among all edges with a band end. Current = sum of chi(lower end) over represented edges that cross
a horizontal cut. Sweep cell by cell; the first 3 rows are a warm-up (band degree <= 2), so every periodic
configuration of every period is a cycle of the state graph. Min mean cycle: Howard (capped), then an exact
integer refinement (Bellman-Ford with parent-graph cycle detection on weights L*w - S). CERTIFIED = the final
Bellman-Ford finds no cycle of smaller mean.
corr2.cpp = same transitions with compact storage (key arena, open hashing, CSR), warm-up layers expanded
without storage, and an optional current filter at row boundaries.
Independent check: `verify_corr.py` (rebuilds the band from the field definition, unrolls 10+ periods, checks
degrees, forced edges, no finite cycle, crossings per period by geometry, and the relative current per cut).
All witnesses below pass it.

Calibration (agrees with F12): diag W=3,4: 2/3 per row for currents not 0 mod 3, 0 for 0 mod 3;
mid W=3: 3/4 (+-1), 1 (+-2), 7/4 (+-3), 2 (+-4).

| kind | W | states | result for relative current +-1 | status |
|---|---|---|---|---|
| diag | 3 | 1.2 k | 4/6 per row | CERTIFIED |
| diag | 4 | 27 k | 4/6 | CERTIFIED |
| diag | 5 | 2.0 M (all currents) | 4/6 (also +-2: 4/6) | CERTIFIED |
| diag | 6 | 26.6 M (current filter) | 4/6 (witness period 6 rows) | CERTIFIED |
| edge (left wall, field (2,1), base U-turns) | 2..4 | <= 0.2 M | 2 per row = base 1 + 1 | CERTIFIED |
| edge | 5 | 55.6 M (all currents) | 2 per row = base 1 + 1 (+-2: +3/2, +-3: +2) | CERTIFIED |
| mid | 4 | 0.7 M | 3/4 (+-2: 1, +-3: 7/4) | CERTIFIED |
| mid | 5 | 14.7 M (current filter) | 3/4 (witness period 4 rows) | CERTIFIED |

Reading: wider bands (up to 6 for the diagonal, 5 for the edge) give exactly the F12 values. No carrier in this
model beats 2/3 per (1,1) step, +1 per edge row, or 3/4 per row on the axis fold. Edge W=6 would need about
1.5 G states (not run).

Commands: `g++ -O2 -std=c++17 -o corr2 corr2.cpp; ./corr2 diag 5 [maxstates] [current]`;
`python3 verify_corr.py out.jsonl`.

## 3. Tile picture of the diagonal carrier (tiles.py)

Witness diag W=3, current +1 (period (6,6), 4 crossings): every crossing is a two-quarter-triangle overlap.
Per period: 8 doubly covered quarter triangles + 8 holes = 16 bad triangles on a staircase of 12 unit grid
edges (the defect path of the Z_3 height). 4 of the 12 edges have bad triangles on both sides (one with two
holes, one with two doubles, twice). The Manhattan bound (1/4 per unit, conditional on Claim 17) would need
exactly one bad triangle per staircase edge: 12 bad = 3 crossings per period. The witness spends 16.

## 4. A layout outside the fold family: B'/B with one vertical fold (CANDIDATE, open)

Idea: the fold layout pays 4n (steep edges) + n (midpoint arches) + 4n/3 (corner flux). Shallow edges cost more
per unit, but the certified lane-free shallow edge (corr2 `edgeB`, depth 4 = W 4) is 11/6 per row, not the 2.6
(depth 3) that w-structures/layout3.py uses, and it has two current classes at the same cost (it carries +-1 for
free). Layout B'/B: field (1,2) for x < h, field (1,-2) for x >= h (free vertical fold at x = h).
- Bottom and top edges are steep (pattern P, 1 per unit); left and right edges are shallow (11/6 per row).
- Every line is in a nest (no ladder): one bottom midpoint chevron nest (n/2 lines, always trapped, fix with
  flips: n/2), and two corner nests TL (left <-> top) and TR (top <-> right). No steep-steep corner.
- Estimate if the corner nests are untrapped for free: 2n + 2(11/6)n + n/2 = 37n/6 = 6.167n < 19n/3 = 6.333n.
  Gate for the shallow edge cost s (corner nests free): 2 + 2s + 1/2 < 19/3, i.e. s < 23/12 = 1.917.
- Topology test (nest_test.py, nest_scan.py; n = 48, 96; both 11/6 templates; all 6 row phases): the TL nest is
  always partly trapped (1/3 or 2/3 of its lines in closed cycles). Reason (checked on the cycles' line classes):
  index lines by c = 2x - y. Top pattern P pairs {c, c+3} with c even. Both 11/6 shallow templates pair
  {c, c+3} with c in three consecutive residues mod 6 (pairs_tpl.py). A nest line class r (mod 3) is untrapped
  iff the left and top pairings alternate along it, i.e. the left edge must pair {c, c+3} for every ODD c.
  A run of three consecutive residues never contains {1, 3, 5}, so one class or two always stay trapped.
- Shallow edge with the pairing rule {c, c+3}, c odd (w-searcher/tm.cpp bottom = shallow edge, same line index
  c = a + 2b, RULE="2:1/3", W=W2=6, all periods, relaxed lower bound): depth 3 >= 2.875, depth 4 >= 2.3 (above the
  gate 1.917). The old exact result "every pair allowed except {c,c+3}, c of one parity" (w-searcher FINDINGS,
  57/26 = 2.19, or 2.1 in the other PI class) is the same rule up to a one-row shift: also above the gate.
- Top edge with the other 1-per-unit-looking U-turn (x,n-1)-(x+2,n-2) (pairs {c, c+5}, c odd): the TL nest has
  no closed cycle for all 12 (template, phase) choices, but this top pattern costs 2.0 per column (+1), measured
  on a 64-wide strip. Total about 7.2n.
- Shallow edge at W = 5 (corr2 edgeB, current class -1, 86 M states): 11/6 per row, CERTIFIED. No gain with depth.
- VERDICT (2026-10-03): DEAD. In a corner nest between a steep edge and a shallow edge, the cheap steep pattern
  pairs by parity of c and the cheap shallow pattern pairs by a run of three residues mod 6; they disagree on one or
  two of the three line classes, so 1/3 or 2/3 of the nest is trapped. Every fix found costs more than the gain
  n/6. Structural fact worth keeping: shallow-steep corner nests are trapped by cheap patterns (compare
  w-structures S10, gentle-seam nests).
