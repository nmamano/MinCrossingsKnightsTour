# KT Lower Bounds - findings (w-lowerbounds/)

Coordinates here: x = column (0 = left board edge), y = row. A "row" of a left strip is one unit of edge length.

## F1 (2026-10-02, PROVEN): the strip relaxation gives exactly 1 crossing per row for every width k

Model S_k (left strip, width k):
- strip cells = columns 0..k-1: degree exactly 2; ghost cells = columns k, k+1: degree <= 2;
- edges = knight moves inside columns 0..k+1 with at least one end in the strip;
- the chosen edges contain no cycle (a proper subset of the edges of a Hamiltonian cycle is a linear forest);
- weight = number of proper crossings between chosen edges.
L_k = inf over configurations of (weight per row) as the number of rows -> infinity.

Results:
- L_1 = 1 and L_2 = 1, computed exactly (strip_dp.py builds the cell-by-cell transfer graph:
  k=1: 330 states; k=2: 82,516 states, 144,674 transitions; mmc.py: Howard policy iteration for the
  minimum mean cycle, then an exact integer Bellman-Ford certificate with lambda = 1/W per cell,
  W = k+2. The certificate gives: every walk from the empty state of L cells has weight >= L/W - 1,
  i.e. >= (rows) - O(1)). Run: `python run_k.py 1`, `python run_k.py 2`.
- L_k <= 1 for every k: explicit pattern P_k (one row, repeated for all y):
  (0,y)-(1,y+2), (0,y)-(2,y+1), and (x,y)-(x+2,y+1) for 1 <= x <= k-1.
  All strip cells have degree 2, no cycle, 1 crossing per row (each edge (0,y)-(1,y+2) crosses
  (0,y+1)-(2,y+2)). Independent check: verify_pattern.py (k = 1,2,3,5,8 -> 1.000 per row, 0 cycles).
- L_k >= L_1 for all k (restrict a width-k configuration to the edges at column 0: it is a valid
  width-1 configuration and its crossings are a subset).
So L_k = 1 for all k. Conclusion: any argument that is local to one edge strip (of any constant or
growing width, with only degree + acyclicity constraints) cannot beat 4n - O(1).
Pattern P_k is simply: all lines of the family x - 2y = c (slope +1/2, i.e. meeting the left edge
almost perpendicularly), and at the edge line c is joined to line c-3 by the move (0,y)-(1,y+2).
(The mirror image, slope -1/2, works as well.)

Consequence: an improvement of the lower bound must use a GLOBAL fact (for example: the line
directions that are cheap at the left edge are expensive at the bottom edge, so the tour must
turn its lines somewhere, or the connectivity of a single cycle).

## F1b (2026-10-02, MEASURED): lane-free edge cost when the outside is forced to one line family

Variant of S_k (strip_dp.py build(k, fam=...)): every cell in columns >= k keeps its two family
edges (+-fam); strip cells may join outside cells only by family edges. Weight = crossings among
edges that touch the strip (edges outside cannot cross strip edges, they meet only at column k).
Min crossings per row (exact min mean cycle, Howard):
| family (left edge) | k=2 | k=3 |
|---|---|---|
| (2,1), (2,-1)  (meets the edge steeply)      | 1   | 1   |
| (1,2), (1,-2)  (meets the edge at a shallow angle) | infeasible | 13/5 = 2.6 |
k=4 for the shallow family exceeded 5M states in Python (not computed). For the bottom edge with the
board's family x+2y=c, the shallow case applies (rotate). Caveat from the Chief Researcher: in a
single-family tour, pattern P on the left and its 180-degree rotation on the right give the same
line pairs {c, c+3}, which close into 2-line cycles; so left and right need different pairing classes.

## F2 (2026-10-02, MEASURED, construction side): folds

A family of parallel lines with direction dA can turn into a family with direction dB along a
straight "fold" band {t - s < n.(x,y) <= t} if n.dA = n.dB = s > 0. Every cell of the band is a
turn (in by dA, out by dB); all degrees are 2. fold_test2.py measures the crossings near the fold
(finite window, so approximate):
- (2,1) -> (1,-2), normal (3,-1): about 0.51 crossings per band cell
- (2,1) -> (1,2),  normal (1,1):  about 0.28 crossings per band cell
- (2,1) -> (-1,2), normal (1,3):  about 0.53 crossings per band cell
These are not optimized. Not a lower-bound result; reported to the Chief Researcher as a lead.

## F3 (2026-10-02, MEASURED + simple proofs): free folds and a 4n - 24 near-2-factor

Free fold lemma (PROVEN, elementary): let f(x,y) = a x + b y with integers a, b, and let dA, dB be
knight moves with f(dA) = f(dB) = 1. Put out-edge P -> P + dA on cells with f(P) <= t - 1 and
P -> P + dB on cells with f(P) >= t. Every cell has in-degree 1 and out-degree 1 (in a region that
is not cut by the board edge), and there is no crossing: all A edges lie in the closed half plane
f <= t, all B edges in f >= t, and a knight move has no lattice point inside it, so two edges can
only meet on the line f = t at a common end cell.
Examples: (2,1) -> (-1,-2) with f = x - y; (2,1) -> (-2,1) with f = y; (1,2) -> (1,-2) with f = x.

8-triangle field (fold_board.py): cut the n x n board by both diagonals and both midlines. In the
bottom-left quadrant use out-direction (2,1) above the diagonal and (-1,-2) below it; rotate by 90
degrees for the other quadrants. All 8 fold lines are free folds. Each board edge sees the family
that meets it almost perpendicularly; the line ends are joined by pattern P of F1 (rotated or mirrored).
base_stats.py (n = 48, 96, 192): exactly 4n - 24 crossings; all cells have degree 2 except 28 cells
(4 corners, 4 edge midpoints, centre 2x2).
Obstacles (measured):
- about n separate cycles (nested loops around the corners, chevron loops at the edge midpoints);
  fold offsets change the count but it stays Theta(n) (cyc_ts.py);
- colour flux: knight moves join black and white cells, so for any cell set R the edges leaving R
  satisfy sum of colours of their inner ends = 2 (black - white cells in R). Each corner window has
  an imbalance that is +-1 mod 3; a local repair is impossible (cluster_test.py: CP-SAT INFEASIBLE in
  the corner windows, feasible at the midpoints and the centre). Shifting a diagonal fold by one
  moves imbalance 3 between a corner and the centre (imb2.py). So some defect of length ~n is needed.
- On a torus there are crossing-free 2-factors with large colour flux (torus_flux.py: staircase lines
  mixing (1,2) and (2,1), flux 15 through a 10-wide cut), so interior transport is not obviously
  expensive.
Rebuild recipe (checked 2026-10-02): from w-lowerbounds/,
  from fold_board import field; v = field(48)            # dict cell -> out-direction, ts=ms=(0,0,0,0)
  from fold_complete2 import base; E, deg = base(48)      # field edges + pattern-P U-turns at all 4 edges
  python base_stats.py 48 96  ->  168 and 360 crossings (= 4n - 24), 28 cells with degree != 2.
field(n, ts, ms): ts = diagonal fold offsets per quadrant (BL, BR, TR, TL), ms = midline offsets
(bottom vertical, right horizontal, top vertical, left horizontal). Coordinates: x = column, y = row up.
Consequence for lower bounds: the 4n - O(1) argument also holds for 2-factors, and 2-factors seem
to get close to 4n. Any better lower bound for tours must use global facts (one cycle, colour flux).

## F4 (2026-10-02, PROVEN): the strip relaxation for TURNS is exactly 1 per row at widths 1 and 2

Same transfer graph, weight = number of turn cells in the strip (run_turns.py): L^T_1 = L^T_2 = 1,
with exact certificates. NOTE: this does not extend to larger widths. KT Turns Theory proved that
width 4 gives 2 turns per row (w-turnstheory/FINDINGS.md: turns >= 8n - 64 for every 2-factor; their
LP gives 1, 1.5, 2 at widths 2, 3, 4, which agrees with my width-2 value).

## F5 (2026-10-02, PROVEN by computation): the cheap edge pattern is unique (stability)

critical.py: in the width-2 strip graph (crossings), the tight edges of an optimal potential contain
exactly two strongly connected components, each one simple cycle of period one row: pattern P and
its mirror image. (Width 1: three such cycles.) Since the graph is finite, every non-tight transition
costs at least a fixed delta > 0, and tight walks outside these two cycles have bounded length. So:
a stretch of m rows of the left edge with at most m + e crossings (counted as in F1) is in pattern P
or P' except for O(e + 1) rows. Any tour with 4n + o(n) crossings is in P/P' along almost all of its
boundary.

## F6 (2026-10-02, notes): global arguments checked so far (no improvement yet)

- Euler: the drawing of a tour with X crossings is a connected plane graph with n^2 + X vertices and
  n^2 + 2X edges, so it has exactly X + 1 bounded faces (all lattice-point free). Pick's theorem on the
  faces gives only identities (sum of Pick defects is 0); no area argument forces X > 0.
- Chord model (chord.py): put the 2 line ends per unit of pattern P on a circle as ports; the edge
  U-turns are the matching M_U = {(2m, 2m+3)}. For N up to 22 there ARE non-crossing interior
  matchings M_I with M_U + M_I one single cycle. So topology alone does not force extra crossings.
- But if M_I is "nested" (a rainbow: (a-i, a+1+i)), then M_U followed by M_I is an involution on ports,
  so every cycle has only 4 ports (2 lines). This is what happens in the fold construction. A better
  lower bound would have to show that crossing-free interior structures are locally nested and that
  each "nest defect" (branch region) costs crossings. Open.

## F7 (2026-10-02, PROVEN, elementary): free-fold nests trap cycles in 2-line loops

(a) Every free fold is a mirror: if f(dA) = f(dB) = 1 and |dA| = |dB|, then dA and dB have the same
component along the normal n and opposite components across it, so family B is the mirror image of
family A in the fold line.
(b) Chord model at the depth-2 ports: pattern P gives the U-turn involution U on ports. Let a nest
(rainbow) of interior paths realise the involution I, and let the edge pattern on its second arm be
U2. A cycle of (U-edges + I-paths) visits p -> U(p) -> I(U(p)) -> U2(I(U(p))) -> I(...) -> ... If U2 = I U I
(the second arm's pattern is the mirror image of the first arm's pattern under the nest's
reflection), then after 4 steps it is back at p: every cycle has exactly 2 lines (4 ports).
(c) In the fold construction every nest is formed by free folds, so by (a) the two arms carry mirror
families; by F5 the cheap pattern is fixed by the family slope (P for one slope, P' for the other), so
U2 = I U I and (b) applies. This explains the ~n cycles.
(d) If instead the second arm carried the "wrong" pattern (I U I composed with a shift), the cycle
advances by 6 ports per round trip, so one nest would hold O(1) long cycles. With straight
port numbering, a rainbow I(p) = A - p gives the shift 6 when A is even and is trapped when A is odd.
Consequence: in any tour with 4n + o(n) crossings, connectivity must come from non-mirror
structures (non-free folds, staircase lines, branch faces, or edge defects). A lower bound above 4n
would follow from: (1) crossing-free interior structures are mirror nests up to O(1) branch faces per
..., and (2) each untrapping event costs >= c crossings. Both are open; (1) fails in general because
staircase lines (alternating (1,2) and (2,1)) are also crossing-free (torus_flux.py).

## F8 (2026-10-02, MEASURED): what crossing-free structures look like (tori)

torus_enum.py 6 6: all 252 crossing-free 2-factors of the 6x6 torus (knight moves, crossings checked
in the universal cover). Every one uses at most two of the four move types, and the two types are
neighbours in angle: (2,1)&(1,2) (staircase mixtures, e.g. 18/18, 24/12, 30/6 edges), or a mirror pair
such as (1,2)&(-1,2) or (2,1)&(2,-1) (pleats = repeated free folds). Never three types.
torus_mix.py 12 12: a band of pure (2,1) lines next to a band of exact 1:1 (2,1)/(1,2) staircase is
INFEASIBLE with zero crossings. Reason (line count): pure (2,1) lines put 2 edges per row across a
vertical cut, the 1:1 staircase puts 1.5, so lines would have to end between the bands.
So bending a bundle of lines without crossings needs either free folds (mirrors, F7: they trap cycles)
or a change of line density, which needs lines to end or turn back. Whether a curved (not straight)
transition can do this crossing-free is open; it decides whether nests can be "untrapped" for free.

## F9 (2026-10-02, PROVEN by exhaustive CP-SAT, OPTIMAL/INFEASIBLE status): local structure of crossing-free regions

local_types.py: window W x W (all cells degree 2), frame of width 2 (degree <= 2), no crossing between
edges that touch the window. Move types: a = (2,1) [slope 1/2], b = (1,2) [slope 2],
c = (1,-2) [slope -2], d = (2,-1) [slope -1/2]; angular cycle a-b-c-d-a.
- W = 5: the edges at the central 2x2 cells can use 3 types (feasible).
- W = 6, 7, 8: at most 2 types at the central 2x2 (INFEASIBLE to have 3).
- W = 8: the perpendicular pair a & c at the central 2x2 is INFEASIBLE (same holds for b & d by symmetry).
So every crossing-free region is locally in one "phase": a pure family or a pair of angular
neighbours ({a,b}, {b,c}, {c,d}, {d,a}). Free folds and pleats are {a,d}/{b,c}-type or {a,b}/{c,d}-type,
staircases are {a,b} or {c,d}. The cheap edge patterns P/P' use {a,b} or {c,d} (lines + U-turn type).
Observation: in the 8-triangle construction the phase winds twice around the cycle a-b-c-d along the
board boundary, so a crossing-free filling of the disk is impossible and some interior defect is forced,
but a point defect costs only O(1), so this gives no linear term.

## F10 (2026-10-02): when a nest traps cycles, and how to untrap it

Setup: a nest = a bundle of lines that leave edge e1 and arrive at edge e2 through free folds only.
Let g be the composition of the fold reflections (a lattice isometry); g maps arm 1 onto arm 2.
(a) Free-fold graph of directions (PROVEN by enumeration of n.dA = n.dB = 1): each knight direction
has exactly two free-fold partners, and the 8 directions form one 8-cycle:
 (2,1) - (-2,1) - (1,-2) - (1,2) - (-2,-1) - (2,-1) - (-1,2) - (-1,-2) - back to (2,1).
Axis folds (pleats/chevrons) and diagonal folds alternate along the cycle.
(b) Trapping criterion (PROVEN, elementary): the cheap pattern at e2 is the image of the pattern at
e1 under g followed by the translation tau that moves the line g(e1) onto the board edge e2 (the
cheap pattern is unique per slope, F5, and invariant under shifts by one row = two line indices).
If tau shifts the line index by an EVEN number, the U-turn pairs at e2 are the images of the pairs at
e1, and every cycle has 2 lines (trapped). If the shift is ODD, a cycle advances 6 ports per round
trip, so the nest carries only 3 long strands (one per residue mod 3).
(c) Checked: in the 8-triangle field the diagonal offset ts = -1 makes the shift odd for all four
corner nests. cyc_where.py 64/128 "(-1,-1,-1,-1)" "(0,1,0,1)": no closed cycle is left at any corner;
all corner lines join 2 long components. All remaining closed cycles are chevron loops: 11 per edge
midpoint at n = 64, 27 at n = 128 (about n/5 each).
(d) Chevrons (e2 = e1, one axis fold) are ALWAYS trapped: g fixes the edge line, the shift is 0.
A same-edge nest needs 1, 4 or 7 folds on the 8-cycle; with 4 folds g is a 180-degree rotation about
a lattice or half-lattice point, so the shift can be odd. Whether such a 4-fold nest fits in a layout
without crossings is untested.
Consequence: if all nests of a layout are untrapped, the 2-factor has O(number of nests) = O(1)
cycles, so O(1) merges. If the corner colour-flux defect also has an O(1) fix, crossings would be
4n + O(1), and 4n - O(1) would be asymptotically tight (no lower-bound improvement possible).

Missing lemmas for a lower bound 4n + c n (all OPEN):
 L1 (structure): in a tour with 4n + o(n) crossings, all but o(n) of the cells lie in crossing-free
    regions made of straight lines and free folds (F9 gives local phases, but staircase mixtures
    {(2,1),(1,2)} are also crossing-free and must be excluded or handled).
 L2 (geometry): every layout of such regions that is compatible with cheap patterns on all four
    edges contains trapped nests with Omega(n) loops in total (e.g. a chevron of size Omega(n)).
 L3 (merge cost): merging k loops of a trapped nest costs >= c k crossings.
F5 is proven; L3 is plausible (merging two nested loops needs a crossing); L2 is the real question,
and (d) shows that L2 is false unless 4-fold same-edge nests (or other untrapped layouts) are
geometrically impossible.

## F11 (2026-10-02, MEASURED, CP-SAT OPTIMAL in windows): cost of merging one trapped loop = 4

Field: n = 96, ts = (-1,-1,-1,-1), ms = (0,1,0,1) (corner nests untrapped, F10). merge_test.py fixes
everything outside a window and asks CP-SAT for the minimum crossings in the window when a given
loop must merge with another component (lazy cut on the loop's cell set).
- Interior window 10x10 at (3,26), loop through (8,32): baseline 0, after merge 4 (OPTIMAL).
  A rung swap (a,a+(2,1)),(b,b+(2,1)) -> (a,b),(a+(2,1),b+(2,1)) with b - a = (1,2) does it with
  exactly +4 (rung.py: 376 -> 380 crossings, 86 -> 85 components).
- Edge window 10x12 at (0,26) (includes the U-turns), loop through (0,30): baseline 14, after merge 18,
  so +4 again (OPTIMAL). Later rounds (merging more loops) were not run to optimality.
Estimate for the fold design with untrapped corners: about 0.21n chevron loops per edge midpoint
(27 at n = 128), so about 0.84n loops, at 4 crossings each -> about 4n + 3.4n = 7.4n + O(1), if the
corner colour-flux defect has an O(1) fix. Replacing chevrons by untrapped nests would remove this term.

## F12 (2026-10-02, EXACT within the model): colour-flux corridor costs

Model (corr_dp.py): a straight corridor along a route with translation (a,1) per row (a = 0 vertical,
a = 1 diagonal). Band of W cells across the route is free (degree 2, any knight move, no cycle);
ghost cells on both sides keep their base field edges; a band-ghost edge is allowed only if it is a
base edge, and then it is forced. Weight = crossings among represented edges. Current through the
cut between rows Y-1 and Y = sum over crossing edges of chi(lower end), chi = +1 if x+y even. For
a = 0 the current is conserved on even rows, for a = 1 on every row (proof: knight moves flip
colour, so for the band between two cuts the cut terms telescope; the lateral term equals the base).
Transfer graph restricted to the target current; Howard min mean cycle = exact min crossings/row.
Routes (fields as in the 8-triangle construction, coordinates: x right, y up):
- diag: fold x - y = 0, (2,1) where x - y <= -1, (-1,-2) where x - y >= 0; step (1,1).
- mid: (transposed) pleat fold x = 0, (1,2) where x <= -1, (1,-2) where x >= 0; step (0,1).
- edge: left board edge x >= 0, family (2,1), base U-turns (0,y)-(1,y+2); step (0,1).
- interior: family (2,1) everywhere, vertical corridor; step (0,1).
Results, extra crossings per step relative to the base (W = 3 and W = 4 agree unless noted):
| route    | flux +-1 | flux +-2 | flux +-3 | per unit length for flux 1 |
|---|---|---|---|---|
| diag     | 2/3 per (1,1) step | 2/3 | 0 (free) | 0.47 |
| mid      | 3/4 per row | 1 | 7/4 | 0.75 |
| edge (W=4) | 1 per row | 3/2 | 2 | 1.0 |
| interior (W=4) | 3/2 per row | 2 | 3 | 1.5 |
Along the diagonal fold, flux = 0 mod 3 is free (this is the fold-shift mechanism of F3), and
flux = 1 or 2 mod 3 costs 2/3 per diagonal step.
Templates and an independent unrolled check (corr_template.py ROUTE W TARGET): degrees, no cycle,
current, and total crossings over the unrolled window (diag 2 per period of 3 steps; mid 3 per 4 rows;
edge 8 per 4 rows = 1 extra per row). Diagonal template, flux +1, period (3,3), band x - y in {-1,0,1}:
 [((-2,0),(0,1)), ((-1,0),(1,1)), ((-1,1),(1,2)), ((0,2),(2,3)), ((1,0),(2,2)), ((1,2),(3,3)),
  ((2,0),(3,2)), ((2,1),(3,3)), ((2,2),(3,4)), ((3,1),(4,3)), ((3,2),(4,4)), ((4,2),(5,4))]
Consequence for the fold design: each corner sends its +-1 to the centre along its diagonal fold:
(2/3)(n/2) = n/3 per corner, 4n/3 in total (the four imbalances sum to 0 at the centre). Pairing the
corners along board edges costs n per pair, 2n in total. So the best corridor gives about 5n + 1.33n.
Toward a lower bound (ii): in this model every route carries a non-zero (mod 3) flux at a positive
cost per unit length (min 0.47). NOT a theorem for tours: bands are at most 4 wide, corridors are
straight, and the field outside is fixed.

## F13 (2026-10-02, analysis): which same-edge nests can exist

Along the free-fold 8-cycle of directions (F10a), consecutive directions differ by about 135 degrees
(alternately 126.9 and 143.1), so one full walk around the 8-cycle is 3 full turns. A line that leaves
the left edge in direction (2,1) and returns in direction (-2,+-1) after a walk on the 8-cycle has
tangent rotation +126.9 (1 fold: the chevron), +-540 (4 folds, monotone), or larger. For a simple arc
in the half plane between two boundary points the rotation must lie in (0, 720) or (-720, 0) degrees
(close it with the boundary segment: total turning +-360, two corner angles in (-180, 180)), so a
4-fold same-edge nest is not excluded, but it is a curl: right, up-left, steep down-right, steep
up-right, down-left back to the edge. The third leg must fold (vertical fold) before it meets the
first leg, so the nest is a spiral of the whole bundle. Whether such a spiral bundle fits on the
lattice without crossings, and its index-shift parity, are untested. Chevrons (1 fold) are always
trapped (F10d); so a fully untrapped layout needs spirals or opposite-edge bundles with an odd shift.

## F14 (2026-10-02): spiral experiment, jog bands, and the mod-3 flux conjecture

(a) Monotone 4-fold same-edge nests do not exist (continuous geometry, spiral_geo2.py): over all
walks on the free-fold 8-cycle with up to 6 folds that leave the left edge as (2,1) and return as
(-2,+-1), random fold positions: net 4 steps (the spiral): 490 geometrically valid arcs, 0 simple
(every one crosses itself). Net 1 step (chevron type, possibly with extra folds): simple and nestable
(spiral_geo4.py: nested pairs exist for step sequences (1), (1,-1,1), (-1,1,1), (1,1,-1), ...).
(b) Jog band (PROVEN, F3 lemma twice): in a (2,1) region put direction (-1,-2) on the cells with
t <= x - y < t + d. Both band boundaries are free folds (normal (1,-1)), so there is no crossing; every
line that crosses the band is translated by (d,-d), i.e. its index x - 2y shifts by 3d. A chevron
arm that crosses a band with odd d is untrapped (F10b: the composite isometry maps the edge line
x = 0 to x = d). Check (jog_test.py, n = 48): one band d = 1 starting at the left edge (0,12): left
chevron loops 7 -> 3, crossings 184 -> 181, defect cells +6 (band ends). A band only catches the
arm lines that start below its edge point and meet it before the midline; the caught intervals
halve toward the chevron apex, so O(log n) bands per chevron (each line must cross an odd number of
odd bands) untrap everything at O(1) cost per band. So trapping is NOT a linear obstruction:
lemma L2 of F10 is false in spirit, and a lower bound cannot come from trapping alone.
(c) Jog bands do not carry colour flux mod 3: corr_dp.py diagint (uniform (2,1) field, corridor along
(1,1), W = 3, 4): flux 0 mod 3 is free, flux 1 or 2 mod 3 costs 2/3 per step (same as along a fold).
(d) Mod-3 flux conjecture (MEASURED on all cases): every crossing-free 2-factor of the 6x6, 6x8 and 8x8
tori (252, 324, 1020 of them, all enumerated) has colour flux = 0 mod 3 through both the horizontal
and the vertical cut (torus_flux_mod3.py). Conjecture M3: crossing-free regions admit a Z_3 "height"
(flux potential), so flux that is not 0 mod 3 needs defects (crossings or edge-pattern defects).
Proposed lower-bound route: (1) define the Z_3 height locally and prove M3; (2) show that the four
corners of a board whose edges are in P/P' carry non-zero mod-3 charges (the fold design gives +-1);
(3) every curve that separates a charged corner from the other charges must meet a defect; there are
about n/2 disjoint such curves around each corner, so Omega(n) defects. Caveat: the curves end on
the board edges, where pattern P has its own crossings; step (3) must show that these do not absorb
the charge. If this works it gives 4n + c n for tours AND 2-factors.

## F15 (2026-10-02): mod-3 colour flux: local lemma PROVEN, corners charged (MEASURED), lower-bound plan

Notation: chi(x,y) = +1 if x+y even, else -1. For a directed unit dual segment s (between centres
of 2x2 cell blocks), phi(s) = sum over tour edges that cross s of chi(end on the left of s).
Flux identity (exact, any 2-factor): for a closed counter-clockwise dual loop around a cell set R,
sum of phi = 2 chi(R) (knight moves join opposite colours).
Lemma M3 (PROVEN by exhaustive CP-SAT, local_m3.py, INFEASIBLE for every other value in -6..6): let s
be a unit dual segment and let the 7x7 cell window around s (plus a frame of width 2 with degree
<= 2) have all window cells of degree 2 and no crossing between edges that touch the window. Then
  phi(s) = chi(c(s)) (mod 3),
where c(s) is the cell on the right of s next to its midpoint. Checked for horizontal and vertical s
and both colour classes (W = 7 and W = 8; W = 6 is enough for the centred position only).
Consequence: H(z) = sum of (phi - chi(c(s))) along a dual path is a single-valued Z_3 potential on the
board's dual grid (the reference family of straight lines satisfies the same loop identity), and H
is constant along every path of "good" segments (crossing-free 7x7 window). So a non-zero mod-3
charge can only be separated from its partner by a wall of bad segments, i.e. a wall of crossings.
Corners (corner_neutral.py, CP-SAT): quarter plane, window M x M, left edge in pattern P or P' for
rows >= d, bottom edge in transposed P or P' for columns >= d, no crossing anywhere in the window
except inside the d x d corner box (and the pattern's own U-turn crossings): INFEASIBLE for all 4
pattern combinations with (M,d) = (14,4), (18,6), (18,8). Sanity: a straight edge (no corner) with
the same rules is feasible. So no corner can be neutralised by any arrangement inside an 8 x 8 box.
Lower-bound plan (status):
 1. stability F5: near-optimal tours are in P/P' along almost all of each edge (PROVEN, width 2).
 2. Lemma M3 (PROVEN, local), plus a near-edge version for windows that contain pattern edges (TODO,
    same kind of finite check).
 3. Corner charge: every corner with P/P' on both sides carries a non-zero mod-3 charge (MEASURED for
    boxes up to 8; a proof for every box size needs the near-edge version of M3 and a computation of
    the charge from the edge patterns alone - TODO).
 4. Charge transport: the charge must be joined to an opposite charge (another corner, about n away)
    by a wall of bad segments or by a non-P stretch of edge; each crossing spoils only O(1) wall length
    and each non-P row costs >= delta (F5). Then the number of extra crossings >= c n with an explicit c.
    Measured transport costs (F12): >= 0.47 crossings per unit length on all tested routes.
If 2-4 are completed, crossings >= (4 + c) n - O(1) for tours AND for 2-factors.

## F16 (2026-10-02): PROOF DRAFT of crossings >= (4 + 1/7392) n - O(1) for every 2-factor

Full write-up: PROOF_crossings.md. Chain: Z_3 potential (Lemma 1, elementary) + M3 (Lemma 2) +
near-edge M3 (Lemma 3) + corner charge Q = 1 mod 3 (Lemma 4) + width-2 stability constants
(rho = 1, T* = 37) + a charging argument: for each corner and each R in [12, n/2 - 9] the square loop
L_R needs a defect (an extra crossing near its top/right side, or a non-P/P' row near row/column R).
Certificates (all PASS): M3 4/4 and NE-M3 28/28 as CNF + Glucose4 DRUP proofs checked by the
standalone check_drup.py (certs/); CP-SAT as the first method; corner charge by two separate
programs; strip constants by two separate programs. Constant c = 1/7392 (not optimised).
Status: needs independent review (the Verifier agent or KT Turns Theory).

## F17 (2026-10-02): current best, closed tours: X >= (4 + 4/15) n - 540

Chain and certificates: TILE_INPUTS.md sections 1-7 (tile framework of KT Turns Theory sections 6-7,
plus my sharp strip-stability constants 1/5, 1/2, 2/15, 2/7 and the column-0 overlap check).
Claims 10 and 11 PASS (Verifier); 4 + 1/8 is Claim 13; 4 + 4/15 is new (not yet audited).
Limit of this method with 4-row corner windows: about 4 + 1/3 (needs the 4E tile term to improve).

## 2026-10-02: jog bands (KT Lower Bounds F14b) instead of arch flips - partial
- fold_jog.py: pure fold field (t = 1, no flips) + jog bands (d = 1, direction (-1,-2) in the (2,1)
  region of every quadrant frame, from the edge point (0, h - D) to the midline).
- All chevron loops vanish for suitable band sets (runs/jog_rule2.txt): D = {5,9} (n=48), {5,13}
  (n=50..64), {7,15} (66..72), {5,9,21} (82..96), {5,13,29} (~114..128), {7,15,33} (130..144),
  {5,9,21,45} (178..192); other n not covered by these 3 sequences. n=96 greedy: {5,9,21}.
- Odd bands carry colour charge -3/+3 at their two ends (d = 2: neutral, but no untrapping).
  Free 3-wide corridors along the bands make the windows balanced; valid tours n = 132 (X = 1225),
  n = 130 (X = 1563): far from optimal (LNS local optimum on large free areas).
- Transplant +12 adds exactly 64 = (16/3)*12 crossings (slope 16/3 confirmed for the inserted
  content), but the +12 tours are not single cycles (outside matching needs step 24).
- Needed (design side): a jog band that carries its own +-3 charge at zero cost (LB F12: flux 3 along
  a diagonal is free; template diag W=3 target 3 = 3-wide strip of (1,2) cells).
