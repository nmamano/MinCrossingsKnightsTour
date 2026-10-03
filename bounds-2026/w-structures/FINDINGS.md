# KT Structures - findings (w-structures/)

Coordinates: x = column (right), y = row (up). Families: A = lines x+2y=c (dir (2,-1)), A' = x-2y=c (dir (2,1)),
B = 2x+y=c (dir (1,-2)), B' = 2x-y=c (dir (1,2)). "Shallow" = 1 line end per unit of edge, "steep" = 2.
All results dated 2026-10-02. Proof status: OPTIMAL = CP-SAT proved optimum for that period/band; FEASIBLE = upper bound.

## S1. Periodic seam model (seam.py, unroll.py)

seam.py: general periodic seam between two line families (or a family and a wall), any period vector T,
band of free cells around the seam, lines fixed outside. Options: lane bijection (lanes of s lines, shift),
no lane rule, wall mode (edge heel). No cycles (flow), crossings and turns per period.
unroll.py: independent check (unrolls 8 periods, checks degrees, traces strands, counts crossings by geometry).
Sanity: H16a (bottom heel) evaluates to 16 crossings / 25 turns per 8 columns in both the model and the check.

Seam costs (no lane rule, which is a lower bound for any lane rule; OPTIMAL unless noted):
| seam | bend | lines per unit | crossings | turns | checked |
|---|---|---|---|---|---|
| A\|B on slope +1 ("gentle") | 37 deg | 3 per unit x | 1.0 per unit x (p=1..6, w<=8) | 3 per unit x | unroll ok |
| A\|A' vertical | 53 deg | 2 per unit y | 1.0 per unit y (p=1,2,4, w<=8) | 2 per unit y | unroll ok |
| A\|B on slope -1 ("sharp") | 143 deg | 1 per unit x | 0 | 3 per unit x | unroll ok |
| A\|A' horizontal | 127 deg | 1 per unit x | 0 | 3 per unit x | unroll ok |
By symmetry also free: A'\|B' on slope +1, B\|B' vertical. These four are the free folds of KT Lower Bounds F3.
Reason: a free seam is a lattice line that meets every line of both families once, so the bends are stacked chevrons.

Lanes: lanes of 4 can NOT cross the gentle seam (INFEASIBLE for all offsets, p=4,8, w<=5). Every solution maps
A-line c to B-line c' with c + c' = 0 (mod 3) (a cell on diagonal y = x + j holds A-line = -j and B-line = j mod 3).
Lanes of 3, 6, 12 cross it (cost 1.0 per unit x, same as no lanes). The sharp seam keeps lanes of 4 (off2 = 0 or 3).

## S2. Idea A (four triangles, all edges shallow) cannot beat 9n

Design A = 8n (shallow heels at 2.0) + gentle seam on the main diagonal (length n in x, 1.0 per unit) + sharp seam
on the anti-diagonal (0) = 9n. Its centre region is nested closed loops (needs a spiral shift).
Coarse layout search (layout.py): k x k grid, each square cut by both diagonals, any of the 4 families per triangle,
shallow edge 2.0, steep 2.5, seam rates of S1, forbidden pairs where line densities differ. Minimum = 9.0 for k=2,3
(OPTIMAL) and k=4,6 (best found). So with these ingredients no layout beats 9n.

## S3. Fold field (all edges steep, free folds) - toward one tour

Base: field(n, ts, ms) of w-lowerbounds/fold_board.py, cheap U-turn (pattern P, line c to c-3) at every edge.
fold3.py rebuilds it with a per-row choice of the U-turn (cheap or flipped = (0,y)-(1,y-2), i.e. c to c+5).
U-turn costs (left edge, A' family, measured): cheap 1.0/row, flipped (both row parities) 2.0/row, mixed 2.5/row.

Topology:
- Corner nests: diagonal fold offset t odd untraps them (chord offset 3t-1 must be even). Agrees with LB F10.
- Midpoint chevrons (arches): a midline shift changes the chord offset by 4, so they are always trapped (LB F7).
  Fix used here: flipped U-turn on ONE side of each midpoint (n/4 rows per edge, +1.0/row) -> +n in total.
  Cheaper than rung merges (about +3n, LB F11).
- Result (t=1, flip on y in [n/2 - n/4, n/2) of every edge frame): X = 192, 432, 672 for n = 48, 96, 144
  (slope exactly 5.0), 0 closed cycles, 32 path components and 52 defect cells for ALL three n (constant).

Colour flux (imbal.py: black-minus-white residual demand of a window):
- Corner windows: -1, +1, -1, +1 (BL, TL, TR, BR) for t odd; +-2 for t even. Midpoints, centre, flip ends: 0.
- Diagonal fold shift moves 3 between corner and centre; midline shift moves 0; flipping both U-turn parities moves 0;
  flipping one parity moves 2 (at +1.5/row).
- Edge strip (A' steep, depth 3-5, period 2-12): every 1.0/row pattern carries the same colour current. Current +-1
  costs 2.0/row (+1.0), current +-2 costs 2.5/row. Those patterns are the cheap pairing with a periodic slip (c to c+-5).
- Free diagonal fold band (w=3): currents 0 mod 3 are free; current +-1 costs 6/2, 6/4, 4/6 (OPTIMAL), 8/12 (FEASIBLE)
  crossings per period -> about 0.67 per unit x.
- Gentle seam: two different currents at the same minimum cost (1.0 per unit x), so it carries +-1 for free.

Estimates (not yet validated): fold field + arch fix + flux along 2 edges = about 6.5n; flux along the 4 diagonals
to the centre = about 6.3n. Layout G (bottom/top B', left/right A', main diagonal free fold, anti-diagonal gentle seam,
no arches) = 4n + n + flux of the two free corners along the main diagonal (about 0.67n) = about 5.7n.

## S4. Validated tours
- n=24: valid single tour from global CP-SAT completion (edge strips free), X = 220 (not optimised). tours/fold_n24_D3.json
- n=96: valid single tour from my own pipeline (paste.py templates + circuit.py AddCircuit + window LNS), X=1067
  after 2 LNS passes (poorly optimised). Superseded by KT Integrator: 19n/3 + O(1) exact for all even n >= 96
  with this field (w-integrator/fold_period.py), and jog bands toward 16n/3.

## S5. Flux term: the flux-network argument (2026-10-02)

STATUS: ARGUMENT, not a proof. Steps 1-2 lean on KT Lower Bounds F16 (proof draft, needs review: Z_3 potential,
corner charge Q = 1 mod 3). Step 3 is a cost estimate over the measured carriers below, not a bound over all carriers.

1. A window's colour imbalance depends only on the fixed structure outside it (counting identity, proven).
   Every 1/row steep edge pattern is unique per family (LB F4) and carries one fixed current; free folds move flux
   only in multiples of 3 (fold shift 3, midline shift 0, jog band 0 mod 3; measured, imbal.py / LB F14b).
2. A corner between two steep-cheap edges with only free folds leaving it has the 45 deg diagonal fold (the only free
   ray into the board from a corner). An O(1) gadget (e.g. a short gentle seam ending in a junction with rays at
   0, 135, 270 deg) leaves the same far structure as the 8-triangle corner, so the imbalance stays +-1 mod 3.
   The other corner type keeps a gentle seam of length Theta(n) (layout G: about 4n + n + 2n/3 = 5.67n).
3. The flux network joins the 4 corners; each corner is a leaf with a nonzero value mod 3, so its branch carries
   nonzero flux up to the first junction. With the carriers below, the cheapest network is the 4 half-diagonals:
   4 x (n/2) x 2/3 = 4n/3. So 16n/3 + o(n) is the floor of this design family UNLESS a cheaper carrier/route exists.
   Topological fact: every route from a corner window to a point where its flux cancels must cross all lines of
   that corner's nest (n/2 nested V lines), so cost >= (n/2) x (min cost per line crossed) + (cost of the rest).

Measured carrier costs (extra crossings, flux +-1):
| route | cost | per line crossed | status |
|---|---|---|---|
| diagonal fold, band W=3,4 | 2/3 per (1,1) step = 2/3 per unit x | 2/3 | EXACT over all periods for W=3,4 (LB F12 transfer matrix); my CP-SAT: 6/2, 6/4 OPTIMAL, 4/6 OPTIMAL, 8/12 best found |
| midline fold | 3/4 per row | - | EXACT W=3,4 (LB F12) |
| board edge, U-turn pattern | 1 per row | 1/2 per line end | EXACT W=4 (LB F12); my CP-SAT D=3,4,5, p=4..8: 2.0/row OPTIMAL vs 1.0 base |
| interior, across (2,1) lines | 3/2 per row | 3/4 | EXACT W=4 (LB F12) |
| gentle seam (A\|B on slope +1) | 0 extra (two currents at its 1.0/unit x cost) | - | OPTIMAL p=3,6 w=3 (seam_flux.py) |
Flux +-3 along the diagonal is free (fold shift). Flux +-2: diagonal 2/3, edge 3/2, midline 1.

Open carrier ideas (handed to KT Edge Searcher for exhaustive search, 2026-10-02): wider diagonal bands (W=5..8);
an ALONG-LINE corridor (translation (2,1) in a pure (2,1) field, no lines crossed); diagonal corridors riding a fold
pair / jog band. Route that uses the along-line corridor: escape the corner nest along the edge (n/2 line ends at
1/2 each = n/4 per corner), then ride the nest's outer V arm (a field line from (0,n/4) to the centre, length
about 0.56n) to the centre. Total n + 2.24 c n, where c = along-line cost per unit length; beats 4n/3 iff c < 0.149.

## S6. Edge + outer-V-arm flux route: assembly spec ready (2026-10-02)
ROUTE_ARM.md + route_arm.py (entry arm_route(n, E) -> free route cells). Tested on fold_jog.build_jog at n=96, 144:
the arm is n/4 - 1 moves of (2,1) plus one fold move, ending 5 cells from the centre. Flux term (1 + c_step) n,
break-even c_step = 1/3 per (2,1) step (0.149 per unit length); with c_step = b the total is (5 + b) n + O(log n).

## S7. Along-line carrier (C1): structure note (2026-10-02, ARGUMENT, waiting for Edge Searcher numbers)
- A band along (2,1) in a pure A' field is a set of W whole lines x - 2y = c. No fixed edge touches it, and no band
  edge can cross an outside line. So all extra crossings are internal, and the current is conserved along the band.
- On line c the cells have a = 2x + y = 2c + 5y, so exactly one cell per 5 a-units. At a cut where every line has
  exactly one straddling edge and all straddlers are (2,1) moves, F equals the pure-field value I0.
  So a band with current I0 +- 1 needs, at EVERY cut, a non-(2,1) straddler or a line with no straddler.
  Non-(2,1) knight moves span at most 4 a-units (one (2,1) step = 5), so non-(2,1) moves appear at every step.
- No free fold is parallel to (2,1) (free folds: horizontal, vertical, +-45 deg), so these moves cannot all be
  crossing-free fold moves. Expectation: c_step is well above 1/3, so the edge + V-arm route will not beat 4n/3.
  Decision waits for the band.cpp numbers.

## S8. Jog bands: current parity = shift parity (2026-10-02, PROOF + CP-SAT check at p=2 w=2)
Question from KT Integrator: a jog band (odd d) has charges -+3 at its edge end and midline end. Is there a
band design that untraps (odd line shift) and carries its own charge (net current 0) at zero cost?
Answer: NO, in any corridor of a uniform (2,1) region. Lemma: rel. current = line shift (mod 2).
Proof: current through a cut window = sum of chi(lower end) over straddling edges, chi = +-1, so current = number of
straddlers (mod 2). Every strand is bi-infinite (left end on side 2, right end on side 1, no cycles), so it crosses the
full transversal line an odd number of times. Strand c -> c+s crosses outside the window above iff c in A, below iff
c+s in B (A, B = index sets of the pure lines that cross above / below the window). So it crosses the window an odd
number of times iff [c in A] = [c+s in B]. The number of such c is |c_Q - c_P + s + const|, so its parity moves with s.
Untrapping needs odd d, so odd shift 3d, so odd current: the net current can never be 0, and +-1 is not 0 mod 3.
Best is +-3 (free along the band); the +-3 must reach another charge.
Check (jog_flux.py p=2, w=2 and w=3, same result, OPTIMAL): shift -3 -> rel current +-3 at 0 crossings, +-1 at 12, 0 / +-2 / +-6 INFEASIBLE.
Cost of the band charges (F12 rates for flux 3: edge 2/row, midline 7/4/row, interior vertical 3/row; free only along
slope +1 inside the (2,1) or (1,2) regions, and the band itself is that path). Band j has its ends at (0, h-2^j) and
(2^j, h) (BL frame); slope +1 paths from them end on the edge or the midline again. Cheapest pairing found: adjacent
bands j, j+1 pair edge ends along the edge and midline ends along the midline, (2 + 7/4) 2^j per pair -> about 1.25h per
edge midpoint, 2.5n per board. That is worse than the arch flips (+n, charge 0). So jog bands with geometric spacing do
NOT give 16n/3; 19n/3 (arch flips) stays the best exact value of the fold family unless the charges can pair at O(1) distance.
Pairing at O(1) distance does not help (ARGUMENT, straight slope +1 bands, F12 flux-3 rates): a band with edge end at
distance a below the midpoint catches arch lines u = h - y0 in [a/2, a]. If every band end pairs with another end at
distance <= delta, bands come in near pairs (a, a + delta'), and a pair catches an odd number of times only
u in [a/2, (a+delta')/2) and (a, a+delta'] (measure 1.5 delta'). Its charge transport costs about (2 + 7/4) delta'.
All arch lines u in (0, h/2] need odd coverage, so the cost is >= 3.75/1.5 * h/2 = 1.25h per edge midpoint for ANY
spacing. Arch flips cost 1 per arch line (h/2 per midpoint). So arch flips beat jog bands, and 19n/3 stays.

## S9. Where the fold family can still gain (2026-10-02)
19n/3 + O(1) (KT Integrator, exact, fold_period.py) = edges 4n + arch fix n + flux 4n/3.

| term | now | best known floor | room | status of the floor |
|---|---|---|---|---|
| edges (steep, cheap U-turn pattern P) | 4n (1 per row per edge) | 4n - O(1) | 0 | PROVEN: published 4n - O(1); LB F1/F5 strip relaxation = exactly 1/row, P and its mirror P' are the only tight patterns |
| arch fix (untrap the 4 midpoint chevron nests) | n (arch flips: P' on one side of each midpoint, n/4 rows per edge, +1/row) | none proven; edge-only fixes >= n (argument below) | up to n | OPEN |
| colour flux (4 corner charges +-1 mod 3) | 4n/3 (4 half-diagonals, 2/3 per (1,1) step) | n/2 if Claim 17 holds (>= 1/4 per Manhattan unit, two adjacent-corner pairs of length n) | up to 5n/6 | diagonal W=3 rate 2/3 certified optimal (Edge Searcher, LB F12); Claim 17 NOT YET PROVED (Verifier) |

Arch term, what is known:
- Chevrons are always trapped with P on both arms (LB F10d). Untrapping arch line u (ends at rows h-u, h+u) needs an
  ODD relative index shift between its two ends.
- Edge-only fixes: along an edge the pattern phase s(y) can change only at defects; rows with odd phase are not in
  pattern P, and the best non-P pattern costs 2/row (+1; LB F12 edge, my edge strips D=3..5 OPTIMAL). Each arch line
  needs exactly one end row with odd phase, so >= h/2 odd rows per midpoint -> >= n/4 per midpoint = n. The arch flips
  meet this. (ARGUMENT: it assumes a defect costs >= 0 and the 2/row value holds over all depths.)
- Interior fixes: an untrapping corridor has odd shift, so odd current (S8 lemma), so its ends carry odd charges that
  must be moved (flux 3 rates: edge 2/row, midline 7/4/row). Straight slope +1 bands cost >= 1.25h per midpoint (S8).
- Mixed idea checked and rejected: route a corner's +-1 flux through the arch triangle so that its odd-shift corridor
  also untraps arch lines. The detour (up the edge to (0,e), slope +1 to the midline, along the midline to the centre)
  costs (13/12) e more than the diagonal and catches u in [(h-e)/2, h-e]; flips do the same lines for (h-e)/2.
- Open: 4-fold same-edge nests (LB F10d/F13) would be untrapped by geometry, with no defect per line. Their
  existence in a crossing-free layout is untested. This is the only route I see to an arch term of o(n).
Flux term: the Edge Searcher (fresh session) searches axis-parallel carriers; pairing adjacent corners along the
edges at rate r per row costs 2rn, so it beats 4n/3 only if r < 2/3 per row (edge pattern carriers measured: 1/row).

## S10. Layout search and layout G (2026-10-02)
- layout2.py (continuous geometry on a k x k grid of 4-triangles, families A, A', B, B', FREE folds only, all edges
  steep, line tracing): for k = 2, 4, 6, 8 the ONLY layout is the 8-triangle fold field (arch cost exactly n, traced).
  So with free folds only, the midpoint chevrons are forced (evidence for LB lemma L2 within this grid family).
- layout3.py (adds the measured non-free seams: gentle 1.0/unit x, A|A' vertical and B|B' horizontal 1.0/unit,
  shallow edges 2.6/unit; seams treated as untrapping): k=2 minimum of edges + seams + arch = 5.0n, with 31 ties:
  (4.0 + arch 1.0, 4 fold corners) x1, (4.5 + 0.5, 3 fold corners) x12, (5.0 + 0, 2 fold corners) x18.
  Best with flux counted: layout G (left/right A', bottom/top B', main diagonal free fold, anti-diagonal gentle seam):
  estimate 4n + n + 2n/3 = 17n/3 IF the seam corners are untrapped.
- Layout G test (layoutG.py free seam band, layoutG_paste.py pasted templates): n=32 valid single tour with a FREE
  seam band (CP-SAT + 3 LNS rounds, X = 277, not optimised). With pasted optimal gentle-seam templates (seam_shift2.py:
  lanes of 3, p=6, w=3: classes (off2,shift,current) = (0,0,-1), (2,-1,0), (2,0,-1); w=4: (0,0,0), (2,0,0), all 6
  crossings per period), the TL and BR seam nests are TRAPPED (closed fixed cycles, n=96) for every class and every
  seam position offset delta in -2..2. So the seam corner behaves like a chevron: no tested seam bijection untraps it.
  Fixing it on an edge costs about 3n/4 per seam corner, so layout G does NOT beat 19n/3 with these templates.
  Status: MEASURED (6 templates x 5 offsets), not proven. Open: a seam template with a different line bijection
  (wider w, longer p) or a proof that gentle-seam nests are always trapped.
- WHY the seam nest is trapped (ARGUMENT + measurement): a gentle seam maps A-line c to B-line c + s(c) with
  c + c' = 0 (mod 3) (S1), so s(c) = c (mod 3). The edge patterns pair c with c +- 3 (same residue), so trapping is
  decided per residue class r by the parity of s_r. Lanes-of-3 seams have s_0 = D, s_1 = D + 1, s_2 = D - 1:
  parities always mixed, so 1/3 or 2/3 of the nest lines stay trapped. Board check: closed cells 552-586 (1/3) or
  1088-1222 (2/3) of the TL nest, as predicted. A seam with ONE parity for all lines (seam_par.py) costs
  3.0 per unit x, OPTIMAL for (p,w) = (6,3), (6,4), (6,5), (12,3), both parities (vs 1.0 for the trapped seam).
  Two seams in series compose to a single parity (s_r + s'_{-r} = D + D'), so a nest that crosses 2 seams can be
  untrapped at 1.0 + 1.0 per unit x, but in layout G that is >= 2n of seams: 4 + 2 + 2/3 = 6.67n > 19n/3.
  Conclusion: layout G and its k=2 variants do not beat 19n/3. All layouts found so far pay >= n for untrapping.

## S11. C1 closed (2026-10-02, conditional on Claim 17)
Edge Searcher bound (w-searcher/FINDINGS.md; counting sound per Verifier Claim 17, general theorem NOT yet proved):
carrying +-1 costs >= 1/4 crossing per Manhattan unit. One (2,1) step has Manhattan length 3, so c_step >= 3/4,
far above the break-even 1/3. The edge + V-arm route (S6, ROUTE_ARM.md) gives >= (1 + 3/4) n > 4n/3: dropped.
Agrees with the S7 structure note. No band.cpp run for C1 is needed.
Measured too (Edge Searcher, 10:30): band |x-2y| <= 3, current +-1: 2.0 per (2,1) step OPTIMAL at p=2,4 (CP-SAT,
freeband.py); band.cpp reachable family 17/12 = 1.417 per step CERTIFIED in that family. C1 closed by measurement.
Open threshold for the Edge Searcher (low priority): layout G with a single-parity gentle seam totals
4 + c_seam + 2/3, so it beats 19n/3 iff c_seam < 5/3 per unit x (measured 3.0 for p <= 12, w <= 5, seam_par.py).
