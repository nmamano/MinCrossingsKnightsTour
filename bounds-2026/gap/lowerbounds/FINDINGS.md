# KT Lower Bounds - gap mission findings (gap/lowerbounds/)

## F (2026-10-03, phase 2d): F1 replaced by a width-two strip certificate - 5n route closes (pending audit)

Task: R4 / F1 in gap/turnstheory/PROOF_5N_PLAN.md section 4. Result: F1 is NOT needed in its R4 form (residual
nu' atoms, baseline marks, Hall bits). The deficient paths are paid by the endpoint RESERVE, through one
strengthened copy of the audited width-two stability lemma. Labels below.

**Claim V (PROVEN, by hand; inputs: (2), (3), endpoint lemma, overlap lemma (6), square identity, H1).**
Strong row test at side row r (up orientation; down by reflection): g(r) = 1 if the up test fails at r
(F != 2 mod 3 or the exception pair), or VIS(r): a crossing pair of strip edges, not both incident to column
0 (a pair in S* minus B), has a two-quarter tile overlap with a quarter in the squares (1..3, r).
Every lost candidate and every DEFICIENT retained candidate (d_i > 0) has an end row with g = 1.
Proof. Lost: uncharged or exception, so an end test fails. Deficient retained: if an end test fails, done.
Else both tests pass. Its middle squares (depth >= 4 from all sides) are good (H1), so every step of gamma_R
that crosses x >= 5 (or y >= 5) has two good adjacent quarters and omega = 0 mod 3 by (2). Hence the charge is
E_left + E_bottom, where E is the flux over the three steps crossing depth 2, 3, 4 at that end; gamma_R is
charged, so some end has E != 0. By (2) that end has a bad quarter adjacent to one of these steps, in the
squares (1..3, r) (the depth-4 square is a good middle square). If it is payable, its square has a second bad
quarter (square identity), which is unpaid, since the path has at most one payable quarter. An unpaid quarter
has m = 2 and one covering S* pair with a two-quarter overlap; that pair is not in B, because B overlaps reach
depth 1 only as pair (6) at the exception row (excluded by retention) and never depth >= 2. So VIS(r) = 1.

**F1-V (CERTIFIED, one implementation: f1v_stab.py).** The audited width-two strip graph (frac_stab.py /
strip_dp.build(2): edges incident to columns 0,1; 82,516 base states; up-test accumulator, 2,095,620
augmented arcs) with row weight 4w - 1 per cell and -4g at row end. VIS(r) is a function of the pending edges
at the end of row r (every edge whose tile meets square row r is pending then). Critical rate (Dinkelbach,
exact): **1**; at rate 1 Bellman-Ford converges, **potential range -29..0** (the same width as the audited
lemma). Critical cycle: 24 arcs, 6 rows, sum(4w - 1) = 24, sum g = 6. Hence, per half side,
    X_sigma(half) - rows >= #(rows with g = 1) - 29/4,
exactly the audited Section 5 inequality with the failed-test count replaced by the strong count.
Down orientation (certified directly, `f1v_stab.py crit 2 down`): the down test at row r pairs with square row
r - 1, so VIS of the previous row is carried as one bit (4,191,240 arcs); critical rate 1, potential range
-33..0. Constants: 4 x 29/4 + 4 x 33/4 = 62 instead of 58, so the final bound is X >= 5n - 614
(5n - 656 with the 42 small-radius allowance).

**Consequence (ARGUMENT, uses only audited constants).** As in V2: T + 1160 >= #(strong rows) >= D_loss + L_def
(distinct candidates own distinct side rows). With (1) of PROOF_5N_PLAN.md and H0:
    E + 580 = nu + (T + 1160)/2 >= sum_{non-def} 1/2 + sum_{def} (1/2 - d_i) + (D_loss + L_def)/2
            >= (L + D_loss)/2 = n - 30,
so X >= 5n - 612 with the audited constant 58; with the down constant below, X >= 5n - 614 (5n - 656 with the
42 small-radius allowance if H1 needs it). Only the SCALAR
inequality is used; nu' is not needed, and no Hall augmentation is needed, because f0 is private (H0) and
the reserve enters only as a total.
Periodic SAT cross-checks (windows/side_f1.py, deep defects and all crossings allowed): rate 1 holds for
P = 8..14 at width 6 with the exact deficient-pass test, and for P = 8, 12 at width 2 with VIS.
Needed audit: (a) Claim V and the final algebra; (b) independent rebuild of f1v_stab.py (VIS geometry, row
attribution, both orientations); (c) the down-orientation row attribution (square row r - 1).

```sh
cd gap/lowerbounds
../../.venv/bin/python f1v_stab.py crit 2 up     # CRITICAL RATE = 1, potential range -29..0 (f1v_pot_up_1_1.npy)
../../.venv/bin/python f1v_stab.py crit 2 down   # CRITICAL RATE = 1, potential range -33..0
```

## G (2026-10-03, phase 2c): Gap Lemma, square version - PROVEN (computer-assisted)

Statement (gap/structures/GAP_LEMMA.md section 2, square version): for every set K of absorbing cuts, the gap
squares of the cuts in K contain at least 2|K| bad quarters. **PROVEN**, from these inputs:
1. Lemma 0 (audited, Claim 30), L1 and L2 (Structures, GAP_LEMMA.md section 6), "every bad square has >= 2 bad
   quarters" and the reduction to tree islands (Structures, section 11). The reduction: a violation needs a
   4-component U of gap squares that is a TREE polyomino, off the board sides, with all 2|U| + 2 boundary sides
   cut ends (so every side neighbour of U is good), |U| + 1 cuts, and total excess sum (b(S) - 2) <= 1.
2. **Uniformity Lemma (PROVEN, by hand, this section).** In such an island all side neighbours have the SAME
   split. Proof by induction on |U|. Call boundary sides e, e' linked if one chain segment through U joins them
   ('/' or '\\'), or if they face the same neighbour square; a segment of the type of the label at one end must
   end at the same label, so labels are constant on linked classes. |U| = 1: the four halves join the four sides
   in a 4-cycle. Step: remove a leaf L (U' = U - L is a tree; one class by induction). The side f between L and
   its parent was a boundary side of U'; its '/' and '\\' partners g1, g2 in U' now join the sides of L via the
   two halves of L at f, and the other two halves of L join the three boundary sides of L to each other. The
   square L was the neighbour of f only (L is a leaf). Every path of links in U' through f reroutes through
   the sides of L, so U has one class. By the reflection x -> -x we may take the label '\\'.
3. **Tree automaton (CERTIFIED, exact, gaplemma/tree_automaton.py).** Bottom-up DP over rooted tree islands.
   Node = U square C with the types of its 3 x 3 block (side neighbours U or good '\\'; diagonal squares U or
   good if they touch a U side neighbour, else unconstrained). Owned constraints (a RELAXATION of the real ones):
   C bad; every good square of the block good with split '\\' (L1 n-values); degree <= 2 at the four corners of
   C. The patch keeps C's 8 side links; all other block links are local existential copies. Tree-edge key:
   the 2 links of the shared side, the types of the 2 x 3 region, the 4 links of the two cross sides, the
   partial degree sums (C part, X part) at both shared corners, and the parity state of the '\\' cut through
   the side ('/' segments are not cuts). Cuts must be absorbing (L2: y0 + yk + k odd).
   Result: 82 block types, 117,612 patches, 8,660 keys; the fixed point is reached after 6 rounds;
   **minimum total excess over all finite tree islands = 2** (no violation needs excess <= 1). Runtime 2.5 min.
   Soundness test (gaplemma/validate_automaton.py): 225 real island configurations (exact degree 2, all island
   conditions, s <= 7, up to 15 solutions per shape), every root: every real patch is in the enumerated set,
   every parent/child key pair agrees, every chain check passes (6,870 node checks, 0 failures).
   Sanity: without the key sync (SYNC=0) the automaton gives 0, so the sync is what carries the proof.
4. **Exhaustive cross-check (CERTIFIED, pysat, gaplemma/tree_islands.py):** every tree island with |U| <= 12
   (33,724 free tree polyominoes at |U| = 12) is UNSAT at <= 2|U| + 1 bad quarters. Tight islands (excess
   exactly 2) exist for every |U| <= 9: seam staircases with exactly one square of 4 bad quarters (SLACK=1).
   The exhaustive model needs only degree <= 2 at the 2|U| + 2 corners of U; every corner class is needed;
   the absorbing parity is needed; without degree constraints violations exist.

Scope: the proof uses only degree <= 2 (no connectivity, no exact degree 2), so it holds for every edge set of
maximum degree 2 that satisfies Lemma 0. Half version and per-cut form are FALSE (Verifier Claim 34, Structures
single_cut.py). Proof size for a reader: the reduction (Structures, half a page), the Uniformity Lemma (above,
10 lines) and one finite computation (tree_automaton.py, about 300 lines of Python, 2.5 min). Independent
re-implementation of the automaton by the Verifier is the recommended audit.

```sh
cd gap/lowerbounds/gaplemma
../../../.venv/bin/python tree_automaton.py 100          # ROOT: minimum total excess ... = 2 (automaton_v3.log)
SLACK=6 NSOL=15 ../../../.venv/bin/python validate_automaton.py 7     # 0 failures
../../../.venv/bin/python tree_islands.py 12             # islands_s12_slack0.log: 0 SAT for all s <= 12
```

## A (2026-10-03, phase 2b): side end-zone charge - the answer to item (a)

Question (CR): can a retained charged path keep its whole charge at depth <= 3 at an end, with the side strip
at baseline? Answer: NO, except through a failed end test, which the reserve already pays. Charge at depth
<= 3 with a passing test needs a height MISMATCH along the side. A mismatch costs at least one strip crossing
per row (finite evidence, below). Setting: left side x = 0, row line l_r = dual line y = r + 1/2, dual step
s_x crosses the grid edge (x,r)-(x,r+1) in direction +x. Q(r) = omega(s_0) + omega(s_1),
E_K(r) = omega(s_2) + ... + omega(s_K) (end-zone flux), F(r) = audited up-test value (section 3 table).
Hypothesis H (the W3 case (b)): no crossing outside S* near the end, and the quarters at depth >= 4 are
perfect (m = 1). By W3 this is the case unless a non-S* crossing is within about 6 cells.

**Lemma A1 (PROVEN, by hand from the audited (2), (3) and the endpoint lemma).** Let K >= 2. If every dual
step of the segment x = K + 1/2, r + 1/2 <= y <= r' + 1/2 has both adjacent quarters with m = 1, then
c(r) := E_K(r) - (-1)^r (F(r) - 2) and c(r') are equal mod 3.
Proof. Apply (3) to the cells {0..K} x {r+1..r'}. The bottom line gives Q(r) + E_K(r) and the top line
gives -(Q(r') + E_K(r')). The right side is 0 mod 3 by (2). The outside left side x = -1/2 meets no knight
edge, and its grid terms add to sum_{y=r+1..r'} (-1)^y. The endpoint lemma (direction +x) gives
Q(r) = -(-1)^r (F(r) + 2). Insert these terms and reduce mod 3.
Meaning: c is the mod-3 colour height of the deep region relative to the standard strip height. A crossing-
free deep region tiles exactly (W1, W3), so c is constant along a clean stretch of the side. If the test
passes at r (F = 2, no exception), the end zone carries charge (E != 0) exactly when c != 0. Then EVERY
row of that clean stretch fails the strong test defined below. Numerical check: c is constant on all rows
of all saved witnesses (windows/side_end_check.py).

**Lemma A2 (PROVEN, by hand from (2) and the audited overlap lemma (6)).** Under H at row r, if E_4(r) != 0
mod 3 and the exception pair at r is absent, l_r has, at depth 1..3, an uncovered quarter or an overlap
quarter of a pair in S* \ B. (A step with omega != 0 mod 3 has a bad adjacent quarter by (2). The only B
overlap at depth >= 1 is pair (6), and pair (6) at row r is the exception.)

**Strong test** at row r: F(r) = 2 mod 3, no exception pair, and E_4(r) = 0 mod 3. Every lost candidate
fails the joint test at an end. Every retained candidate with end-zone charge fails the strong test at
that end.

**CERTIFIED (SAT; DRUP-checked where marked; P-periodic strips only).** Model windows/side_sat.py: rows
Z_P (P even), columns 0..W+1, degree 2 for x < W, halo degree <= 2, H imposed, lazy no-finite-cycle cuts,
S* crossings counted per period (the baseline is P, one per row).
- JOINT test (J): for every P-periodic strip under H, excess >= #(rows that fail the strong test).
  UNSAT of the violation for W = 7 and P = 8, 10, 12, 14, 16, and for W = 9 and P = 8, 12. No cycle cut
  was needed, so (J) holds even without the forest condition. Equality occurs (excess 8, 8 failures, P = 8).
  P = 8, W = 7: DRUP proof (61,381 RUP steps) passes w-lowerbounds/check_drup.py.
- Mismatch alone (row 0 charged with a passing test, so c != 0 on the whole period): minimum excess per
  period 13 (P = 8), 14 (P = 10), 17 (P = 12), >= 16 (P = 14). It is always >= P (bisection, exact SAT).
- No periodic strip has every row charged at baseline (P = 8). One charged row costs 11 (P = 8) and
  >= 4 (P = 12). The pure SAT model agrees exactly with the CP-SAT model windows/side_end.py at P = 8.
Witnesses pass the independent checker windows/side_end_check.py (degrees, crossing classes, quarter
multiplicities by exact rational point tests, formula (2) on every step, F, exception, c).

**Plug-in (ARGUMENT).** Suppose (J) holds for every strip (non-periodic, with an additive constant), on the
rows where H holds. Then V2 improves to T + C' >= #(strong failures) >= D_loss + L_end. Here L_end counts
retained paths with end-zone charge in a clean stretch, so the reserve lambda*(T + C') pays lambda = 2/3
for these paths as well. Every other retained path has E = 0 at both clean ends. Its charge therefore sits
at depth >= 4 from both sides, or one of its end windows is not clean. In both cases a non-S* crossing is
within bounded distance (W3 lemmas). This is the interior allocation (item (b), KT Edge Searcher).
So item (a) reduces the side case to ONE strip inequality (J). It needs no new currency.

**PARKED (CR, 2026-10-03): the (J) certificate is not built.** Reason: the 2/3 flux route is in doubt (Edge Searcher's (1,2) wall at 1/2 per level), and the simple 5n route is primary. Resume: build the transfer graph below, and first finish the P = 14, 16 mismatch bisection (side_sat_scan.sh 7).

**Next (proposal, parked).** Certify (J) for all strips with a transfer graph: columns 0..8, no connectivity labels
(the SAT runs did not use the cycle cuts), H imposed, row-local mod-3 trackers for E_4 and F. Alternatively,
carry c in the state (Lemma A1 makes it constant between defects). Rows where H fails are defect rows with
g = 0 and free state. Risk: the state count with 9 columns is unknown; H (only S* crossings, perfect deep
quarters) should make it small, because by W1 the deep part is a fold stack.

```sh
cd gap/lowerbounds/windows
../../../.venv/bin/python side_sat.py 8 7 all 0 joint     # UNSAT: (J) at P = 8 (writes .cnf/.drup)
python3 ../../../w-lowerbounds/check_drup.py sideSAT_P8_W7_all_K0_joint.cnf sideSAT_P8_W7_all_K0_joint.drup
../../../.venv/bin/python side_sat.py 8 7 0 12 pass        # UNSAT: mismatch needs excess >= 13 at P = 8
../../../.venv/bin/python side_sat.py 8 7 0 13 pass        # SAT witness; check with side_end_check.py
./side_sat_scan.sh 7                                       # mismatch bisection (side_sat_scan_W7.log)
```

## W3 (2026-10-03, phase 2): bad quarters are local - holes need a nearby crossing

Notation: a quarter is bad if its tile multiplicity m != 1 (audited proof, section 1); a hole has m = 0. By the
audited flux lemma omega(s) = chi(a)(m_+ + m_- + 1) mod 3, a dual step with nonzero flux mod 3 is adjacent to a
bad quarter, and every charged path has such a step.

**PROVEN (elementary + finite check).** Fold stacks tile exactly: every quarter has m = 1
(windows/w3_foldstack_tiling.py: random, alternating and one-switch sequences, all four families, both
orientations, interior of a 14 x 14 region: 0 bad quarters). With W1 this explains the lemma below.

**PROVEN (SAT, DRUP checked).** Interior hole lemma: if the cells of a 7 x 7 block (lower-left cell of the unit
square at relative position (3,3)) have degree exactly 2 and a width-2 halo has degree <= 2, then a hole in any
quarter of that square forces a crossing between two edges that touch the block (windows/hole_cert.py 7; four
CNFs, Glucose DRUP proofs pass check_drup.py; k = 5 is SAT, k = 6 is UNSAT for two quarters only).

**PROVEN (SAT, DRUP checked).** Side-anchored hole lemma, board side at x = 0: allow only the width-two strip
crossings S* (both edges touch column 0, or both touch columns <= 1). A hole in a unit square at depth d >= 4
(square [d, d+1] x [c, c+1]) is impossible: it forces a crossing outside S* among edges touching the 12 x 9 block
(windows/side_hole_cert.py 12 9 d S, d = 4, 5 checked by DRUP, d = 6 UNSAT). Holes at depth <= 3 CAN be paid by
S* crossings alone (SAT witnesses). With only the outer-column set B allowed, the threshold is depth 3 (DRUP
checked; depth 2 is UNSAT for 2 of 4 quarters). An overlap quarter of an S* pair lies at depth <= 3 (tiles stay
within 2 of their endpoints), so at depth >= 4 EVERY bad quarter forces a crossing outside S* within a bounded
window. Corner regions (small depth from two sides) are an O(1) exception not covered here.

**Consequence for the private price (ARGUMENT).** The "nonlocal hole" risk of the master skeleton is removed:
every charged path either (a) has a crossing outside S* within bounded distance (about 6 cells) of one of its
vertices, or (b) has all its nonzero-flux steps next to quarters at depth <= 3, i.e. its charge sits at its two
ends inside the side zone. Case (a) gives a bounded-support price; case (b) is a side-local quantity that a
(wider) strip certificate can price. This turns L2 into a finite local allocation problem. It does not yet
give 2/3: a crossing within distance 6 of a path can be near several nested paths.

**Inconclusive (MEASURED, CP-SAT).** Corner-box crossing minimisation (w3_corner.py, w3_quarters.py): with
crossings in S* excluded, 4 nested charged corner paths in a 9 x 9 box cost 0 crossings outside S* (the
witness puts 57 crossings inside S*); total-crossing and bad-quarter minimisation give weak bounds (objective 22,
bound 3 at K = 8; 9 bad quarters for 4 paths with bound 0), so no price is certified this way.

## W1 (2026-10-03, phase 2): zero-cost phases are exactly the fold stacks

**Definition.** A fold stack (f, dA, dB): f is one of x, y, x+y, x-y, and dA, dB are the two knight moves with
f(d) = 1 ((1,2),(1,-2) for x; (2,1),(-2,1) for y; (2,-1),(-1,2) for x+y; (2,1),(-1,-2) for x-y). Each level
t of f chooses c[t] in {dA, dB}; cell P has the edges P - c[f(P)-1] and P + c[f(P)]. A constant sequence is a
parallel field, one switch is a free fold (w-lowerbounds F3), alternating switches give zigzag textures in which
every cell is a sharp turn. These four f are the only functionals in [-3,3]^2 with two knight moves at value 1.

**PROVEN (elementary).** Every fold stack is a crossing-free, cycle-free 2-factor: the in-edges of level t all
come from level t-1 with one direction; an edge from level t to t+1 lies in the slab t <= f <= t+1 and meets the
line f = t+1 only at its endpoint; edges inside one slab are parallel. f increases along every oriented path.

**PROVEN (SAT with a checked DRUP proof).** Let a 9 x 9 core have degree exactly 2 and a width-2 halo degree <= 2,
with no crossing between two edges that touch the core (no-cycle constraints not even needed). Then the central
3 x 3 block is a fold stack. CNF: windows/w1cert_k9_b3.cnf (424 variables, 7,144 clauses, one clause excludes
each of the 156 fold-stack 3 x 3 maps); UNSAT with Glucose 4 and with Lingeling; both DRUP proofs pass the
standalone checker w-lowerbounds/check_drup.py (2,942 and 2,989 RUP steps).

Corollary (ARGUMENT, follows from the 3 x 3 lemma): in a crossing-free region, at distance >= 3 from its
border, every 3 x 3 block is a fold stack; so fold lines of different families never meet (no junctions), and
two families can coexist only across a field that belongs to both (example found by SAT in an 11 x 11 window
with a 5 x 5 centre: vertical folds of f = x and a diagonal fold of f = x+y, separated by field (1,-2)).

Data: the k = 7 window (2 rings of context) admits 164 central maps: the 156 fold stacks and 8 fold-line
junctions; with 3 or 4 rings (k = 9, 11) only the 156 fold stacks remain (CP-SAT enumeration with lazy
no-cycle cuts, w1_enum.py; analytic count w1_count_stacks.py: 156 for 3 x 3, 2,172 for 5 x 5).

Consequence for the structure lemma (skeleton L1): the zero-cost phases are not only parallel fields and single
free folds; dense fold stacks (zigzags) are also crossing-free. Fold junctions (as at the centre of the
8-triangle field) are not crossing-free with exact degree 2.

```sh
cd gap/lowerbounds/windows
../../../.venv/bin/python w1_cert.py 9 3      # writes w1cert_k9_b3.cnf/.drup, prints UNSAT
python3 ../../../w-lowerbounds/check_drup.py w1cert_k9_b3.cnf w1cert_k9_b3.drup
../../../.venv/bin/python w1_cert.py 11 3     # SAT: a 5 x 5 centre with two families (not a contradiction)
```

## STATE AT THE PIVOT (2026-10-03): strip work stopped by order; nothing running

Done: L1 (11.3, beta=1 exact), L2 (field survives in a closed tour), L3 (R1, beta=4/3), L4 (combined credit,
beta=16/11, C++ match by Edge Searcher; audited by the Verifier as Claim 27). Half-done: L5 below.

## L5 (2026-10-03, HALF-DONE at the pivot): Edge Searcher's joint model (columns 0..5, exact F23/J crossings)

Spec agreed with KT Edge Searcher (their gap/searcher/FINDINGS.md 6.3): S, F23 = col2-col3, J = col3-col4/5;
cols 0,1,3 degree exactly 2, cols 2,4,5 <= 2; row weight q(4W-4)+p(4W0-4)+4q*Wx-2pt. Edge Searcher (first
implementation, up only, labels on S only) reports beta* = 2 exact, critical cycle = the period-6 field of L4.

My data (MEASURED, CP-SAT, joint/field_joint_cost.py; S fixed to a field, cheapest F23+J completion, column 3
exact on all rows but 3 at each end, lazy no-cycle cuts):
- period-6 c=0 field of L4: wx = 0, 2, 4 for 24, 36, 48 rows (all OPTIMAL): 1 crossing per 6 rows, so its
  joint ratio is (4+1)/(5/2) = 2. This agrees with Edge Searcher's critical cycle.
- saturated field: wx = 14, 38 for 24, 48 rows (FEASIBLE only, slope about 1 per row, as the interval lemma says).
- cheap field (mirror P): wx = 0.
Not done: my second implementation (joint/joint_graph.py, a from-spec state enumerator, written but never run
to completion; no state count yet), the down orientation, and the reduction (Turns Theory R3).
Resume: run `../../../.venv/bin/python joint/joint_graph.py` for the state count, then add the row-level
endpoint/parity augmentation as in combo_stab.py.

## L4 (2026-10-03): combined credit (N1)/(N2) certified at beta = 16/11; 16/11 is exact in this model

Task: gap/turnstheory/FINDINGS.md "Route past 52/11: combine the two credits". **Finite certificate:
PROVEN by one implementation (combo_stab.py); the independent second implementation is KT Edge Searcher's
C++ check (pending).** CONDITIONAL as a bound on: U1 (boundary surplus reduction), the interval lemma behind K
(Turns Theory, not yet audited), and the N1 combination argument.

Integer weights per row arc (row-level graph, 4 cell arcs per row):
q*sum(4w-1) + p*sum(4w0-1) + 4q*k - 2p*t, with k the blocked-run charge (run constant 4) and t = 2a.

| orientation | beta* | potential range (units 1/(4q) = 1/44) | C |
| --- | --- | --- | --- |
| up | 16/11 | -596..0 | 149/11 |
| down | 16/11 | -596..0 | 149/11 |

Dinkelbach from 8/3: an 18-row cycle (ratio 3/2), then the 8-row cycle below (ratio 16/11), then convergence.
Coefficient if all conditions hold: 4 + 2beta/(2beta+1) = 4 + 32/43 = 204/43, about 4.744 (vs 52/11, about 4.727).

**Blocking field (period 8, explicit check check_combo_obstruction.py, no transfer-graph code):**

    (1,y)-(0,y+2), (2,y)-(0,y+1)       every y
    (2,y)-(1,y+2)                      if y mod 8 != 2
    (3,y+1)-(1,y+2)                    if y mod 8 == 2

It is the saturated field of 11.4 with one edge moved every 8 rows. Per 8 rows: 16 crossings (excess 8),
8 boundary pairs (R = 0), blocked rows 1,2,5,6,7 mod 8, so runs of length 2 and 3 and K = 0; sum a = 11/2 in
the bad phase (both orientations). Ratio 8 / (11/2) = 16/11. The moved edge costs no crossing, breaks the
blocked runs below the run constant 4, and lowers the penalty only from 6 to 11/2 per 8 rows.

Model details: node = (phase-0 base state, parity, 4-bit history cand(r-1), cand(r), b2(r-1), b2(r),
run counter 0..4); 21,420 phase-0 states, 250,990 row paths, 40,158,400 augmented arcs, 2.5 GB, about 4 min
per orientation. All initial parities, histories and counters are start nodes. check_combo_history.py checks
the compressed automaton against the raw definition (blocked(y): d3(y)=0, d2(y-2)=d2(y+2)=2; K = sum
max(0, l-4)) on 18,000 random degree sequences, run constants 0..5.

```sh
cd gap/lowerbounds
../../.venv/bin/python combo_stab.py crit up 8/3     # combo_crit_up.log
../../.venv/bin/python combo_stab.py crit down 8/3   # combo_crit_down.log
../../.venv/bin/python combo_cycle_show.py up        # writes combo_field_up.json
python3 check_combo_obstruction.py                   # explicit field, ratio 16/11 (check_combo_obstruction.log)
python3 check_combo_history.py                       # history automaton vs raw definition
CAP=c ../../.venv/bin/python combo_stab.py crit up 8/3   # run constant c instead of 4
```

**Sensitivity to the run constant (up orientation, 2026-10-03; K = sum max(0, l - c)):**

| run constant c | beta* | blocking cycle | coefficient 4 + 2beta/(2beta+1) |
| --- | --- | --- | --- |
| 4 (current lemma) | 16/11 | period-8 field above, K = 0 | 204/43 ~ 4.744 |
| 3 | 16/11 | same | 204/43 |
| 2 | 3/2 | 6 rows, sum(4w-1) = 24, k = 0, t = 8 | 19/4 = 4.75 |
| 1 | 3/2 | 8 rows, sum(4w-1) = 24, k = 0, t = 8 | 19/4 |
| 0 (every blocked row pays) | 8/5 | period-6 field below, no blocked row | 100/21 ~ 4.762 |

So a sharper interval lemma alone can reach at most beta = 8/5 in this model. The limit at c = 0 is a field with
no blocked row at all (check_cap0_obstruction.py, explicit; same ratio in both orientations):

    (1,y)-(0,y+2), (2,y)-(0,y+1)       every y
    (2,y)-(1,y+2)                      if y mod 6 in {0, 4, 5}
    (3,y)-(1,y+1)                      if y mod 6 in {2, 3, 4}

Per 6 rows: 10 crossings (excess 4), R = 0, K = 0, max sum a = 5/2; ratio 8/5. Any credit past 8/5 must charge
this field. Logs: combo_crit_up_cap{0,1,2,3}.log, check_cap0_obstruction.log.

## L3 (2026-10-03): request R1 (boundary credit) is certified at beta = 4/3, and 4/3 is exact

Answer to gap/turnstheory/REQUESTS.md R1. **PROVEN finite certificate (two implementations).**

With w0 = new crossing pairs whose two edges both have an endpoint in column 0, the integer weights

    q*(4w-1) + p*(4w0-1) - 2p*t        (t = 2a at row end, a from w-turnstheory FINDINGS 11.2)

admit a converged potential at beta = p/q = 4/3, in both orientations, both initial parities:

| orientation | potential range (units 1/(4q) = 1/12) | C |
| --- | --- | --- |
| up | -155..0 | 155/12 |
| down | -159..0 | 159/12 = 53/4 |

So on every oriented half walk, (X_sigma - length) + (4/3)(B_sigma - length) >= (4/3) sum a - 53/4.

**beta = 4/3 is exact** (PROVEN): a Dinkelbach search started at 3/2 finds a 6-row negative cycle with
sum(4w-1) = 24, sum(4w0-1) = 0, sum t = 9 (2 crossings, 1 boundary crossing, penalty 3/4 per row: the old
saturated period-one field of 11.4), ratio 24/(18-0) = 4/3; the search then converges at 4/3.

Consequence, IF Turns Theory's reduction U1 (gap/turnstheory/FINDINGS.md, "pending external review") holds:
X >= [4 + 2beta/(2beta+1)] n - O(1) = 52n/11 - O(1), about 4.727n. The reduction itself is not checked by me.

Checks: r1_stab.py recomputes w for every base arc from the two states and asserts equality with strip_dp's
stored w; r1_independent.py does the same with strip2_independent.proper and its own set-of-edges augmented
graph. Both give the ranges above.

```sh
cd gap/lowerbounds
../../.venv/bin/python r1_stab.py crit up 4/3      # converged at 4/3, range -155..0 (r1_crit_up.log)
../../.venv/bin/python r1_stab.py crit down 4/3    # converged at 4/3, range -159..0 (r1_crit_down.log)
../../.venv/bin/python r1_stab.py crit up 3/2      # cycle -> 4/3, then converged (r1_crit_up_from32.log)
python3 r1_independent.py up 4 3                   # independent: -155..0 (r1_independent.log)
python3 r1_independent.py down 4 3                 # independent: -159..0
```

## L2 (2026-10-03): the L1 field survives in a single closed tour; connectivity does not make it expensive

**Verdict: the connectivity route is dead for this field.** A closed tour that carries the field on 64 rows of
one side (penalty a = 1 on all 64 rows) costs only 61 crossings more than the tour it came from, i.e. no more
than the field's own strip excess (64). So a single-cycle argument cannot raise the field's ratio above 1.
The obstruction is removed instead by the boundary credit of R1 (L3).

**PROVEN (parity lemma, check_field_parity.py).** Every cut between two rows is crossed by an even number of
tour edges. In the field, the edges with an end in column 0 or 1 that cross a cut are odd in number (3 or 5);
in P and mirror P they are 4. So on every row of a field run, an odd number of crossing tour edges lie wholly
in columns >= 2. The field cannot be closed near its two ends alone; the closure must cross every row of the
run. In the tour below the crossing-free folds carry it.

**VERIFIED instance (conn/FIELD_n166_92_155.json, 2026-10-03).** Start: FOLD24_n166 (X = 1179). Force the field
(phase 0) on left-side rows 92..155. CP-SAT (2 workers, 900 s, conn/field_global.py) re-solves the left band
(columns 0..5, rows 86..161) and bands of half-width 3 around the midline fold (row 83) and the anti-diagonal
fold (x+y = 166), all other edges fixed: best 2-factor +59, 13 cycles. A greedy 2-swap merge with exact
crossing deltas (conn/merge.py) joins them: 11 merges cost 0 or less, the last two cost 4 each. Result: one
closed tour, X = 1240 (+61). verify_field_tour.py (no CP-SAT code; crossings by kt/core.py crossing_list)
checks the Hamiltonian cycle, X = 1240, all field edges present, and sum a = 64 over rows 92..155 in the
top-left corner frame (original tour: 0).

Earlier band tests on 16 rows (conn/field_band.py): no closure inside columns 0..3 (INFEASIBLE, matches the
parity lemma); closure inside columns 0..5 found at +49 (not optimal). The folds are the cheap carrier.

```sh
cd gap/lowerbounds && python3 check_field_parity.py
cd conn && ../../../.venv/bin/python verify_field_tour.py FIELD_n166_92_155.json FOLD24_n166 92 155 0
# rebuild (about 20 min, 2 workers): field_global.py 92 155 0 6 6 3 900 900 one; merge.py twofactor_92_155_0.pkl
```

## L1 (2026-10-03): the fractional endpoint certificate has beta* = 1 exactly. No improvement on 14n/3.

**Verdict.** In the width-two forest strip, with the half-unit penalties a of 11.2 and the row parity in the
state, the best coefficient in (11.5) is beta = 1 for BOTH orientations and BOTH initial parities.

- **PROVEN (exact certificate, two implementations):** beta = 1 holds with integer potentials in [-29, 0]
  (units 1/4), so C = 29/4 for `up` and for `down`. This only gives back the coefficient 14/3 of 10.5.
- **PROVEN (explicit field, checked without the transfer graph):** no certificate with beta > 1 exists.
  The blocking cycle is a period-4 field with sum(w - 1/4) = 1 per row and penalty a = 1 at every row.

Consequence: (11.6) with beta = 1 gives 4 + 2/3 = 14/3. The 11.3 route does not narrow the gap.

### The blocking field (period 4 rows)

For every row y:

    (2,y)-(0,y+1),  (3,y)-(1,y+1)          long edges, all on the lines x + 2y = const
    (1,y)-(0,y+2)   if y mod 4 != 3        column 0-1 joins of the cheap pattern (mirror of P)
    (0,y)-(1,y+2)   if y mod 4 == 1        one reversed column 0-1 join per period

It is the cheap pattern (mirror P) with one column 0-1 join reversed every 4 rows. Facts (checked):

- columns 0, 1 have degree 2, columns 2, 3 have degree 1, no cycle;
- 8 proper crossings per 4 rows, so sum(w - 1/4) = 1 per row (excess 1 per row over the 4n term);
- no inward exception (one of the two EXC edges at each row);
- up test: F mod 3 = 1, 0, 1, 0, ...; with the right parity phase h = 1 at every row, so a = 1 at every row.
  The other phase gives h = 0, a = 1/2. The down test on the same field gives F = 0, 1, 0, 1, ... and
  again h = 1, a = 1 at every row for one phase (the search found this field shifted by 2 rows).
- the same field is the cycle found by the Dinkelbach search in both orientations (16 arcs = 4 rows).

Compare the 11.4 field: 2 crossings per row, a = 1, 1/2 alternately, ratio 4/3. The new field has the same
crossing rate but keeps h = 1 (penalty 1) on both parities, so its ratio is 1.

### Why this is a limit of the whole route, not of the penalty table

**PROVEN (short argument).** Any additive endpoint table a_c(h) (it can depend on the parity c) that pays
for lost paths must satisfy a_c(1) + a_c(2) >= 1 (the pair (1,2) loses the path, and both ends of gamma_R
use the same radius R, so the same c). The cheap patterns P/P' have h = 2 at every row and zero excess,
so a certificate with beta > 0 needs a_c(2) = 0. Thus a_c(1) >= 1 for both c, and the field above, with
h = 1 at every row, has ratio at most 1. So beta <= 1 for every such table.

The loss is also real, not an artifact of the split: if the left side carries this field and the bottom side
carries P/P' (h = 2), then h_left + h_bottom = 0 mod 3 at every radius and every candidate path in that range
is lost, at a cost of one excess crossing per path.

**PROVEN (explicit check): wider strips do not help.** Add (x,y)-(x+2,y-1) for 2 <= x <= k-1. For every
width k = 2..8 the result is a valid S_k configuration (strip degree 2, ghosts <= 2, no cycle) with the same
8 crossings per 4 rows and the same edges in columns 0..2, so the same endpoint data. All long edges lie on one
parallel family, so the argument holds for every k. Thus no strip certificate of any width, with this residue
test and additive penalties, reaches beta > 1.

### What would be needed to go past 14n/3 on this route (ARGUMENT, not checked)

The configuration "this field on one side, cheap pattern on the other side of the corner" satisfies all local
inputs of the 14n/3 proof with equality (one excess crossing per lost path). Any improvement must make this
configuration more expensive by a fact that is not in a single side strip, for example:
1. a joint condition on the two sides of a corner (the field needs h = 1 on one side and h = 2 on the other at
   the same radius);
2. a different charged curve for the lost radii (other path shapes through the same corner region);
3. a stronger square budget than 2L <= 4E + 44 when such fields are present;
4. global connectivity: the reversed joins change how the line ends pair up. Every reversed join is a choice
   the tour pays for; a single-cycle argument might force or forbid it.

### Data and commands (each run is about 25 s, one core)

```sh
cd gap/lowerbounds
../../.venv/bin/python frac_stab.py crit up       # Dinkelbach from 4/3 -> cycle ratio 1 -> converged at 1, range -29..0
../../.venv/bin/python frac_stab.py crit down     # same
../../.venv/bin/python frac_stab.py up 1 1        # certify one beta (writes frac_pot_*.npy)
python3 frac_independent.py up 1 1                # independent set-of-edges checker: converged, range -29..0
python3 frac_independent.py down 1 1              # same
../../.venv/bin/python frac_cycle_show.py up      # print the cycle as a field, re-check on an unrolled copy
python3 check_frac_obstruction.py                 # explicit field, no transfer-graph code: ratio exactly 1
python3 check_frac_obstruction_wide.py            # the field extends to widths 2..8 at no extra crossing
```

Logs: crit_up.log, crit_down.log, frac_independent.log, check_frac_obstruction.log,
check_frac_obstruction_wide.log. frac_cycle_{up,down}.npy are the arc lists of the found cycles (arc indices
of the frac_stab.py graph). frac_pot_{up,down}_1_1.npy (12 MB each) are the beta = 1 potentials; they can be
rebuilt with the commands above and need not be synced.

Code copied (unchanged) from w-lowerbounds/: strip_dp.py, strip2_independent.py. frac_stab.py follows
w-lowerbounds/endpoint_stab.py; frac_independent.py follows w-lowerbounds/endpoint_independent.py. Both add
the parity bit and the charge t = 2a of 11.2 (identical to score() in w-turnstheory/check_endpoint_loss.py).
Augmented graphs: frac_stab 1,112,872 used nodes (up), 2,095,620 arcs; frac_independent 188,112 nodes and
338,200 arcs (up), 335,564 nodes and 630,778 arcs (down).
