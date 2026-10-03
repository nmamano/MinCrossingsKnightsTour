# KT Edge Searcher - gap mission findings (gap/searcher/)

Task (gap/BRIEF.md): UPPER bound, colour-flux term (now 4n/3 in the fold construction).
Labels: OPTIMAL / CERTIFIED (exact over all periods in the stated model) / FEASIBLE (upper bound only).
All dates 2026-10-03.

## 0. Status summary (latest first)

- 2026-10-03 10:00: WALL12.md (CR request). (1,2) wall with margins restricted to one field type (W=4, lambda=1):
  1/2 per row needs mixed-word '/' fields (zigzag) on both sides; next to straight knight-line fields the cheapest
  (1,2) wall costs 1 per row ('\' H|V or '/'H|'\'V) or does not exist. wall.cpp: FIELDL/FIELDR, warm-layer hash dedupe,
  compact key (-DNOLABK). W=5 does not fit in 8 GB (relaxed warm layer > 90 M states): stopped, low value.

- 2026-10-03 09:30: Structures' metric on the wall witnesses (section 7.3): the (1,2) and (1,1) walls absorb 0 ribbon
  ends (same split, same bits both sides); (1,3) 1.25 and (2,3) 2.33 crossings per absorbed end.

- 2026-10-03 STEP A KEY RESULT: a straight defect wall of direction (1,2) between PERFECT regions, psi jump != 0,
  costs 1/2 crossing per level (section 7.1; witness checked by Python and extended by CP-SAT). So P1(2/3) is
  FALSE for straight walls; and if it fits a layout, it is a cheaper flux carrier than the diagonal 2/3.
- 2026-10-03 PIVOT (gap/PIVOT_BRIEF.md): phase-1 plan for piece 1 is gap/searcher/PLAN.md. New exact identity
  E = X - 4n + 2 = (G + X1 + W3)/2 (PLAN section 1), checked on the n = 166 tour (check_identity.py).
- 2026-10-03 LOWER side: R2 second implementation MATCHES KT Lower Bounds: beta* = 16/11 exact, both orientations
  (section 6). New C++ engine `lower/jr.cpp` reproduces R1 exactly (beta* = 4/3). Joint model (columns 0..5,
  inner boundary strip counted exactly, R3 weights): beta* = 2 EXACT in BOTH orientations (section 6.4).
  Budget confirmed by Turns Theory (R3). Second implementation pending (Lower Bounds). No claim before audit.
- 2026-10-03 HANDOFF: upper-side work closed (CR). Next role: C++ engine for the LOWER side, second implementation
  of KT Lower Bounds' combined-credit certificate N1/N2 (gap/turnstheory/FINDINGS.md "Route past 52/11").
  Binaries are not kept: build with `g++ -O2 -std=c++17 -o corr2 corr2.cpp` (same for arch.cpp).
- 2026-10-03: certified edge re-pairing price X >= rows + N_re/2 (W <= 4), section 5; sent to the Verifier by the CR.

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

## 5. Edge re-pairing price: certified input for KT Structures G2 step 3 (2026-10-03)

Quantity certified. Edge strip model `edge` of corr2 (left wall, free cells 0 <= x < W, each with degree 2, field
(2,1) fixed for x >= W, base U-turns P = (0,y)-(1,y+2), no finite cycle). Index lines by c = x - 2y. Every line
has exactly one end in the strip (its last edge into the strip is forced). In P the strip joins line c to its
P-partner: c+3 if c is odd, c-3 if c is even. For a configuration, N_re = number of line ends whose strip partner
is NOT their P-partner. Claim:
    X >= rows + N_re / 2                          (per period, every period; base current class)
CERTIFIED for W = 2, 3, 4 (arch.cpp: corr2 transitions plus the origin line of every open strand end; transition
weight 2X - (number of ends of a strand just closed that are not P-paired); minimum mean per row = 2, exact
integer Bellman-Ford certificate, LAMBDA=2/1, current filter = base class: W=3 current -1, W=4 current 0).
Relaxation (keeps the bound valid): an end whose origin is older than RMAX/2 rows, or comes from the warm-up, counts
as re-paired. Results equal for RMAX = 10 and 16 at W = 4 (18.6 M states without the current filter).
For finite stretches the same certificate gives X >= rows + N_re/2 - C on paths between steady core states,
C = potential range / 2: C = 6 (W=3), 6.5 (W=4) crossings.
Sharp: P (X = rows, N_re = 0) and the full flip (X = 2 rows, N_re = 2 per row) both meet it with equality.
Other current classes (same runs, all periods): 2X - N_re >= 3 per row at W = 3, 4, so they are more expensive.
Use in G2. For the left-midpoint chevron nest with P on both arms, line u is trapped with partner P(u) at both
ends, so every arch line that is untrapped by edge re-pairing needs at least one re-paired end. With the claim,
each untrapped arch line costs >= 1/2 crossing; n/2 arch lines per midpoint give >= n/4 per midpoint, n in total.
This replaces the G2 step-3 "measured +1 per non-P row" by a certified per-end price for every depth W <= 4 and
every period, and it also covers partial re-pairings (rows that are only partly non-P). Mechanisms through
non-base current are the other case of G2 step 2: those classes cost >= +1 per row (corr2 edge, W <= 5).
Not covered: W >= 5 for the pairing claim (state count about 500 M); the junction constants between stretches
of different classes; interior mechanisms other than the S8 corridors of G2 step 2.
Independent check: not yet; the Chief Researcher sent it to the Verifier (2026-10-03). Suggested: CP-SAT with exact pairing labels for fixed periods (w-structures
classphase-style), minimise 2X - N_re for p <= 8, W = 4.
Commands: `g++ -O2 -std=c++17 -o arch arch.cpp; RMAX=16 LAMBDA=2/1 ./arch edge 4 100000000 0`
(without LAMBDA: Howard, witness = P).

## 6. LOWER side: independent C++ checks of R1/R2 and the joint model (2026-10-03)

All code in `gap/searcher/lower/`, written from the written definitions (w-lowerbounds F1; w-turnstheory
FINDINGS 10.2, 10.4, 11.1-11.2, QUESTIONS.md; gap/turnstheory/REQUESTS.md R1, R2). No code of KT Lower Bounds
was read. Base strip graph = my audited `w-searcher/cert/strip2.cpp` (82,516 states, 144,674 arcs).

### 6.1 R2 (combined boundary and interval credit): beta* = 16/11, PROVEN (second implementation)

`r2.cpp`: augmented state = (base state, mask of listed edges pending at row start, parity, g history 4 bits,
z history 2 bits, run counter s <= 4, current g bit). The endpoint test of row R is evaluated at the row end
from the SET of listed edges: (pending at the start of row R) U (pending at the start of row R+1). Every listed
edge straddles row R, so this is the full set. Weight q(4w-1) + p(4w0-1) + 4qk - 2pt. Exact integer
Bellman-Ford with negative-cycle extraction from the parent graph; Dinkelbach steps to the critical ratio;
final re-check of all reduced costs.

| orientation | starts | nodes | arcs | beta* | potential range at 16/11 (units 1/44) |
| --- | --- | ---: | ---: | --- | --- |
| up | zero history | 13,791,098 | 26,554,646 | 16/11 | [-667, 0] |
| up | all histories | 13,817,578 | 26,603,962 | 16/11 | [-667, 0] |
| down | zero history | 20,619,156 | 40,081,158 | 16/11 | [-687, 0] |
| down | all histories | 20,645,732 | 40,130,652 | 16/11 | [-687, 0] |

Blocking cycle (8 rows): (1,y)-(0,y+2), (2,y)-(0,y+1) for all y; (2,y)-(1,y+2) for y != 7 mod 8;
(3,y)-(1,y+1) for y = 0 mod 8. Per period sum(4w-1) = 32, sum(4w0-1) = 0, k = 0, sum t = 11: ratio 32/22.
This is KT Lower Bounds' field shifted by 5 rows. The ranges differ from their row-level -596 (cell-level
graph: walks can start and end inside a row); beta* and the cycle agree.

```sh
cd gap/searcher/lower && g++ -O2 -march=native -std=c++17 -o r2 r2.cpp
./r2 up crit 8 3            # 25 s, 1.2 GB: 8/3 -> 11/7 -> 16/11 converged   (crit_up.log)
./r2 down crit 8 3          # 32 s: 8/3 -> 16/7 -> 32/17 -> 16/11 converged  (crit_down.log)
./r2 up crit 8 3 allhist    # same with every initial history and counter    (crit_*_allhist.log)
```

### 6.2 Joint engine jr.cpp, validated on R1

`jr.cpp`: generic strip (DEG per column E = exactly 2 / L = at most 2, allowed column pairs, path labels on
all edges or on S edges only), compact 16-byte state keys, augmented variants (lost listed-edge bits, parity)
as a bit set per base state, arcs generated from the base CSR. Weight q(4w-1) + p(4w0-1) + 4q*wx - 2pt,
wx = new crossing pairs with at least one edge outside S.
Validation: `./jr EELL 01,02,12,13 full up crit 3 2` gives beta* = 4/3, range [-155,0] (down: [-159,0]), with
188,112 / 338,200 (up) and 335,564 / 630,778 (down) augmented nodes / arcs: identical to KT Lower Bounds L3
and to their frac_independent counts.

Normalisation of the baseline: the "-1 per transition" of the 4-column graph is moved to the row end as
-4q - 4p per row, so the per-row totals are q(4W-4) + p(4W0-4) + 4q*Wx - 2pt for any number of columns.
(First joint run used -1 per cell with 6 cells per row: wrong, discarded.) With this placement the R1
check still gives beta* = 4/3; its ranges become [-176,0] up and [-180,0] down (walks may stop inside a row).

### 6.3 Joint model (columns 0..5): HALF-DONE, stopped by the CR's pivot (2026-10-03, 06:25)

Model (agreed with KT Lower Bounds and the CR): edges S (an end in column 0 or 1), F23 (column 2 - column 3),
J (column 3 - columns 4, 5); not modelled: column 2 - column 4, column 4 - column 5. Degrees: columns 0, 1, 3
exactly 2 (all 8 neighbours of a column-3 cell are in columns 1, 2, 4, 5), column 2 at most 2, columns 4, 5 at
most 2. Path labels on S edges only (relaxation: acyclicity of the width-two part, as in the base model).
Weight per row q(4W-4) + p(4W0-4) + 4q*Wx - 2pt, Wx = crossing pairs with at least one edge in F23 u J.

Result so far (ARGUMENT-level, not a claim):
- UP orientation: beta* = 2/1 EXACT in this model. Base 35,372,696 states / 71,090,636 arcs; augmented
  83,780,188 nodes / 171,579,088 arcs; 4 min, 3.1 GB. Dinkelbach 8/3 -> 5/2 -> 2, Bellman-Ford converges at 2,
  potential range [-104, 0] (units 1/(4q) = 1/4), 0 violated arcs (joint_up.log).
- Critical cycle at 2: period 6 rows, per period W = 10, W0 = 6, Wx = 1, sum t = 5 (a = 5/2):
  ratio (16 + 4)/10 = 2. KT Lower Bounds reports the same ratio 2 for its period-6 field with a CP-SAT completion
  cost of 1 J crossing per 6 rows (independent agreement; I did not print the edge list of my cycle).
- IF the budget argument holds (Turns Theory must confirm: per-side edge sets with an end in columns 0..3 are
  disjoint up to O(1) corner pairs) AND the down orientation also gives beta >= 2, then
  X >= [4 + 2beta/(2beta+1)] n - O(1) = 24n/5 - O(1) (4.8n). This is CONDITIONAL and not checked.

To resume:
```sh
cd gap/searcher/lower && g++ -O2 -march=native -std=c++17 -o jr jr.cpp
./run_wd.sh joint_down.log 11 ./jr EELELL 01,02,12,13,23,34,35 slab down crit 8 3   # about 5 min, about 3-4 GB
./jr EELELL 01,02,12,13,23,34,35 slab up cert 2 1                                    # certificate only
```
Then: print the edge list of the critical cycle (printCycle shows only base ids and weights: add the decode
of the introduced edges, as in r2.cpp); optional stronger variant with column 2 - column 4 edges
(DEG EEEELL, PAIRS 01,02,12,13,23,24,34,35): measure the state count first (CR condition: under 8 GB).

### 6.4 Joint model completed at the CR's request (2026-10-03, 06:30-06:45): beta* = 2 in both orientations

Weights: exactly R3row of gap/turnstheory/REQUESTS.md R3 (q(4W-4) + p(4W0-4) + 4q*WX - 2p*t per row; the -4q-4p
baseline is charged at the column-5 row end; w = S/S pairs only, wx = every other pair in T once). The 6.3 UP
run already used these weights. Both initial parities are start states. Path labels on S edges only (a
relaxation of R3.1's forest rule on T, so a valid certificate for R3; the exact R3 beta* can only be >= 2).

| orientation | augmented nodes | arcs | beta* | range at 2 (units 1/4) | peak RSS | Dinkelbach |
| --- | ---: | ---: | --- | --- | ---: | --- |
| up | 83,780,188 | 171,579,088 | 2 | [-104, 0] | 3.6 GB | 8/3 -> 5/2 -> 2 |
| down | 162,690,236 | 343,695,792 | 2 | [-104, 0] | 5.3 GB | 8/3 -> 5/2 -> 2 |

Bellman-Ford converges at 2 in both; 0 violated arcs on re-check. Critical cycles (edges listed by lower end,
rows relative to the cycle start; joint_up.log, joint_down.log):
- UP, period 6: W = 10, W0 = 6, WX = 1, sum t = 5: (16 + 4)/10 = 2. Columns 0..2 as in the R2 field
  ((1,y)-(0,y+2), (2,y)-(0,y+1), (2,y)-(1,y+2) on rows 0, 4, 5), column 3 joined by F23/S/J edges; one J crossing
  (5,4)-(3,5) per period.
- DOWN, period 4: W = 7, W0 = 4, WX = 0, sum t = 3: 12/6 = 2. Edges: (1,y)-(0,y+2) and (2,y)-(0,y+1) all y;
  (2,y)-(1,y+2) for y = 0, 3; (3,0)-(2,2), (5,0)-(3,1), (5,1)-(3,2), (3,2)-(1,3), (4,2)-(3,4), (3,3)-(1,4),
  (3,3)-(2,5), (4,3)-(3,5) (mod 4). It has NO crossing outside S: the joint credit does not touch it, so
  beta = 2 is the limit of this model in the down orientation.
Conditional consequence (if audited): X >= [4 + 2beta/(2beta+1)] n - O(1) = 24n/5 - O(1).

```sh
cd gap/searcher/lower && g++ -O2 -march=native -std=c++17 -o jr jr.cpp
./run_wd.sh joint_up.log 8 ./jr EELELL 01,02,12,13,23,34,35 slab up crit 8 3     # 4 min, 3.6 GB
./run_wd.sh joint_down.log 8 ./jr EELELL 01,02,12,13,23,34,35 slab down crit 8 3 # 5 min, 5.3 GB
```

## 7. Step A of PLAN.md: wall tension of straight defect bands (2026-10-03, IN PROGRESS)

Engine `wall/wall.cpp` (own code). Model: band of direction (A,1); scan cell (u,y) = board cell (u + A*y, y);
modeled cells 0 <= u < WM have degree exactly 2; ghost cells = all their other knight neighbours, degree <= 2,
edges only to modeled cells (so every edge with a modeled end is represented). Complete squares (every covering
tile has a modeled end) form an interval per square row; the KM outermost on each side are MARGIN squares and must
be perfect (all quarters m = 1); the others are COST squares. psi jump (sum of chi(a)(m_+ + m_- + 1) over the
transversal, audited formula (2)) must be != 0 mod 3 at every row end. Cost per row: crossings Xc of represented
edges and waste G + W3 (cost squares) + X1; weight lambda*Xc + (1-lambda)(waste)/2 in E units (PLAN (II)).
Warm-up: rows 0 and 1 relax modeled degrees; checks start at square row 1 (fully represented there); warm-up
layers are expanded one cell position at a time and not stored. Exact min mean cycle per row (Dinkelbach + integer
Bellman-Ford). Per level = per row / max(|A|, 1) (L-infinity levels crossed per row). NOLAB=1 drops path labels
(no acyclicity): a relaxation, valid for lower bounds. A wider band can only help the wall (more room).
Calibration: MODE zero (psi jump 0) gives cost 0 (A=0, WM=3).

Results (CERTIFIED for the stated model and width; E units per level crossed):

| wall | WM | labels | states | lambda=0 (waste) | lambda=1/2 | lambda=1 (crossings) |
| --- | --- | --- | ---: | --- | --- | --- |
| vertical A=0 | 3 | yes | 2.6 M | 2/3 | 2/3 | 2/3 |
| vertical A=0 | 4 | no (relaxed) | 13.5 M | 2/3 | 2/3 | 2/3 |
| diagonal A=1 | 3 | yes | 2.6 M | 1/2 | 3/4 | 1 |
| diagonal A=1 | 4 | no (relaxed) | 20.0 M | 0 | 1/2 | 2/3 |
| direction (1,2) (shear 1/2) | 4 | no (relaxed) | 10.6 M | 1/2 | 1/2 | **1/2** |
| direction (1,3) (shear 1/3) | 4 | no (relaxed) | 22.2 M | - | 5/9 | 5/9 |
| direction (2,3) (shear 2/3) | 4 | no (relaxed) | 23.0 M | - | 5/8 | 7/12 |

WM=4 with labels exceeds 100 M strict states (not run to the end; 8 GB rule).
Note: one early pilot (A=0, WM=3, old warm-up) peaked at 16.6 GB without the watchdog; all later runs use
run_wd.sh (kill by PID above 7 GB).

Reading (2026-10-03, 08:20):
- The waste currency alone (lambda = 0) prices a diagonal wall at 0 (WM=4): a psi jump made of doubly covered
  quarters only, with no local gap. So the identity E = waste/2 cannot be used alone for walls. The doubles are
  paid globally through E >= X_int + R - O(1) (crossings outside B).
- lambda = 1/2 (today's accounting) gives exactly 1/2 per level on the diagonal: the method's 1/2 is locally tight.
- lambda = 1 (crossings only) gives 2/3 per level for BOTH the vertical (axis) and the diagonal wall (WM=4,
  relaxed), equal to the certified fold carrier. So the right currency for P1 is crossings outside B (lambda = 1).
- Slopes 2 and 3 (A = 2, 3) need WM >= 5 (geometry: no complete squares below), 82+ slots; the A=2, WM=5 warm-up
  passed 7.5 GB and was stopped by the watchdog. Next engine step: rational shear x = u + floor(a*y/b) with the
  row phase in the state (direction (a,b), a < b), equivalent by transposition and much narrower per row.
Commands: `cd gap/searcher/wall && g++ -O2 -march=native -std=c++17 -o wall wall.cpp`;
`NOLAB=1 ./run_wd.sh LOG 7 ./wall A WM 1 nz 8 1 CAP` (LAMS=0/1,1/2,1/1 default). DRY=1 prints the geometry only.

### 7.1 The (1,2) wall: 1/2 crossing per level (2026-10-03, 09:00)

Engine: rational shear (wall.cpp, cell (u,y) = board cell (u + floor(a*y/b), y), row phase in the state);
regression: A=0, A=1 results unchanged; MODE zero gives 0. Shear 1/2, WM=4, NOLAB: min mean = 1/2 crossing per
row for lambda = 1 and also 1/2 for lambda = 0, 1/2 (CERTIFIED in that relaxed model; 10.6 M states, 85 s).

Witness (period 4 rows, period vector (2,4); board coordinates; modeled cells 0 <= x - floor((1+y)/2) < 4):

    (-1,0)-(1,1)  (1,0)-(3,1)  (1,0)-(2,2)  (2,0)-(3,2)  (3,0)-(5,1)  (3,0)-(4,2)
    (0,1)-(2,2)   (2,1)-(4,2)  (2,1)-(3,3)  (4,1)-(6,2)  (4,1)-(5,3)
    (1,2)-(3,3)   (1,2)-(2,4)  (3,2)-(5,3)
    (0,3)-(2,4)   (2,3)-(4,4)  (2,3)-(3,5)  (4,3)-(6,4)  (4,3)-(5,5)

Checks:
- `python3 gap/searcher/wall/verify_witness.py` (independent Python, own tiles): modeled degrees 2, no cycle,
  2 crossings per period (0.5 per row), per period 4 doubly covered and 4 uncovered quarters (area balanced);
  margin squares perfect; psi jump nonzero (one grid edge with m_+ + m_- = 2 + 1).
- `.venv/bin/python gap/searcher/wall/extend_witness.py 2 8` (CP-SAT, 2 workers, < 1 s): with the witness fixed,
  the exterior on a cylinder (8 rows, 5 inner square columns per side) has a solution in which EVERY exterior
  quarter is covered exactly once (OPTIMAL = feasible). So the wall separates two perfect regions.
Meaning: per L-infinity level (one row in the y > x region), the wall costs 1/2 crossing, and its waste is also
1/2 per level. A wall from a corner in direction (1,2) crosses every gamma_R once. Hence:
- LOWER side: P1(p) with p > 1/2 is FALSE for straight walls; the private flux price of straight walls is at most
  1/2 per path, the value the audited method already gets. The 16n/3 route via flux alone fails as stated.
- UPPER side (UNCHECKED): if such a wall fits a full tour layout (side and corner compatibility, exterior fields
  that match the fold layout, one cycle), the flux term would drop from 4n/3 to n (19n/3 -> 6n). Not tested.
Other directions (WM=4, relaxed, lambda=1): (1,3) 5/9, (2,3) 7/12, (1,1) 2/3, (0,1) 2/3.

### 7.3 Ribbon ends and integer current of the wall witnesses (KT Structures' request, 2026-10-03, 09:30)

Tool `wall/ribbon_ends.py LOG...` (output `wall/ribbon_ends.out`). It reads the optimal witness of each lambda
section, rebuilds the periodic edge set (old logs printed x without the row phase; the tool rebuilds x from u and
takes the phase for which every margin square is good), and reads the two margin columns: split, and the H/V bit of
each ribbon run that meets the band (a run that crosses the band as one good run has no end). Absorbed ends per
period by Structures' G11 rule. Integer current: I(Y) = sum of chi(a)(m_+ + m_- - 3g + 1) along square row Y between
the margins (I(Y) != 0 mod 3 at every row for MODE nz, by construction). Caveat: the margins are ONE square column;
the exterior beyond them is free (ghost cells), so it is not forced to be a ribbon field.

| wall (WM=4, relaxed) | lambda | crossings per period / rows | splits L, R | absorbed ends per period | crossings per end |
| --- | --- | --- | --- | ---: | --- |
| vertical (0,1) | 0, 1/2, 1 | 4 / 6 | mixed, mixed (horizontal split walls cross the band) | n/a | n/a |
| diagonal (1,1) | 1 | 2 / 3 | '/', '/' (ribbons parallel to the band) | 0 | no end |
| diagonal (1,1) | 0, 1/2 | 2 / 1, 2 / 2 | '\', '\' (equal bits) | 0 | no end |
| (1,2) | 0, 1/2, 1 | 2 / 4 | '/', '/' (bits VH, VH) | **0** | no end |
| (1,3) | 1/2, 1 | 5 / 9 | '/', '/' | 4 | 1.25 |
| (2,3) | 1/2, 1 | 14 / 24 | '/', '/' | 6 | 2.33 |

Reading: the cheapest psi walls ((1,2) at 1/2 per level, (1,1) at 2/3) absorb NO ribbon end: both sides have the
same split and the same bit on every ribbon. So a nonzero psi jump does not need an absorbed end, and the G11/R5
"price per absorbed end" does not see these walls; they carry an integer colour current along the band (I(Y) values
in ribbon_ends.out, e.g. (1,2): 5, 2, 2, 2 per row, = 2 mod 3). The optimal vertical wall uses mixed-split margins.

### 7.2 State for the next session (2026-10-03, 10:10; supersedes the 09:00 version)

- DONE: Structures' ribbon-end metric (7.3, sent); WALL12.md (field-restricted (1,2) wall, sent to CR + Integrator);
  Integrator's question (straight (2,1)|(2,1) and (2,1)|(1,2)) answered: none below 4 per level at W=4.
- Width 5 (NOLAB, compact key, warm hash dedupe): relaxed warm layer > 90 M states, stopped (nl_s12_W5c.log). Do not retry.
- B1 (P1 with p = 2/3) is moot: straight (1,2) walls give p <= 1/2.
- NEW TASK (CR, 10:05): decide whether a 6n layout with (1,2) walls can exist. Certify interface prices (lambda=1):
  (1) zigzag field | straight knight-line field, every interface slope that can occur (crossings per unit length);
  (2) zigzag field next to a board side (Structures C2: infeasible in their model; confirm or find the cheapest side
  pattern); (3) break-even: walls at 1/2 per level (BL-TL, BR-TR pairs, total n); zigzag zones + transitions must
  cost < n/3 in total to beat 19n/3. Coordinate with KT Integrator (agent-1790897628991-tlfe).
  Tool idea: wall.cpp with FIELDL/FIELDR and MODE any (no psi jump) prices a straight interface between two fields of
  given types: run shears 0, 1/2, 1, 1/3, 2/3 (and transposed directions by symmetry). Side: a new one-sided variant
  (modeled strip next to the side, margin on one side only).
