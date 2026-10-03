# KT Structures - gap mission findings (gap/structures/)

Role: UPPER bound. Arch term (n) of the fold design, and designs outside the fold family.
Conventions as in w-structures/FINDINGS.md (x right, y up; free-fold 8-cycle of LB F10a).
Run scripts from this folder with ../../.venv/bin/python.

## G1 (2026-10-03, PROOF; repaired after Verifier Claim 24): a simple free-fold same-edge return with steep ports has net cycle step +1

Statement (Claim 24 wording). Let P be a finite polygonal arc of knight moves, with no geometric self-intersection,
from A=(0,a) to a distinct B=(0,b), contained in x >= 0. Its first direction is (2,1), its last direction is (-2,1)
or (-2,-1), and every non-straight transition is a free fold on the 8-cycle of LB F10a (oriented as printed there).
Then b > a, the last direction is (-2,1), the total tangent rotation is 180 - 2 theta deg (theta = atan(1/2)), and the
signed net step count on the cycle is +1. (The free-fold hypothesis is needed: the simple arc
(0,2),(2,3),(4,2),(2,1),(0,0) starts (2,1), ends (-2,-1) and returns below its start.)

Proof. (1) Close P by the segment B->A if P meets it only at its ends; otherwise by the outside detour
B -> (-eps,b) -> (-eps,a) -> A. The closed polygon is simple, so its rotation is +360 (b > a) or -360 (b < a).
(2) The closing turns are fixed by the directions, so the rotation of P is fixed:
end (-2,1): 180 - 2 theta (b > a) or -180 - 2 theta (b < a); end (-2,-1): 180 or -180.
(3) The positive cycle increments alternate 180 - 2 theta and 90 + 2 theta (total 1080); reverse steps give the
negatives. So the rotation depends only on the net displacement k: R(2m) = 270m, R(2m+1) = 270m + 180 - 2 theta,
for every integer m. (4) All increments are positive, so |R(k)| >= 270 for |k| >= 2, while every table entry lies
strictly between -270 and 270. Only k = -1, 0, 1 remain, with end directions (-1,-2), (2,1), (-2,1); only k = +1
has a steep left-facing end, and its rotation forces b > a. This holds for every length.
Consequences. Reduced 4-step and 7-step steep same-edge returns (the "4-fold spiral" of S9 / LB F13) are impossible;
this upgrades LB F14a from measurement to proof. Extra cancelling fold pairs remain possible: seven TOTAL folds with
net +1 exist (Claim 24 example: alternating (2,1)/(-2,1) layers, leg endpoints (0,0),(8,4),(6,5),(8,6),(6,7),(8,8),
(6,9),(8,10),(0,14)). The composite fold isometry has linear part (x,y) -> (x,-y), so it is a horizontal reflection
or glide reflection g(x,y) = (x + t_x, -y + t_y).
Not proved here: whether every glide forces a defect structure, and what crossing cost such structures need. That
needs a separate proof (a corridor decomposition with the S8 hypotheses and an endpoint charge budget). G1 does not
by itself give a lower bound on the arch term; the arch conclusion rests on G2 (ARGUMENT).
Commands: `python turning.py 11` (prints the steep-end table and asserts that only net step +1 occurs);
independent check: `python3 ../verifier/claim24_check.py`.

## G2 (2026-10-03, ARGUMENT): with chevrons, every untrapping mechanism pays at the edge; arch >= n/4 per midpoint

Setting: the left midpoint chevron nest, lower ends at rows [h/2, h), upper ends at rows (h, 3h/2], cheap patterns
P (lower) and P' (upper). L_u = arch line u closed by the edge segment OUTSIDE the board.
1. [PROOF] The deviation current J (tour colour flux minus base flux) is divergence-free away from base defects:
   for every cell set R, flux(R) = 2 chi(R) for every 2-factor (each cell has degree 2), so the difference is 0.
   L_u encloses no base defect, so the total J that crosses the arch line u is 0, for every design.
2. [PROOF, w-structures S8] In a uniform (2,1) region a corridor's line shift = its current (mod 2).
   So interior corridors that cross u with total odd shift carry total odd current, and by step 1 an odd
   current must also cross u inside the edge strip (where u ends). A current in the edge strip at row y means
   the edge pattern at row y is not P (every 1.0/row pattern carries the base current, w-structures S3).
   Edge flips (the arch fix) are non-P rows with zero current.
   So: line u can be untrapped only if the edge strip is NOT pattern P at row h-u or at row h+u.
   (Local merges of two loops by rung swaps avoid this, but cost 4 per loop = 2 per line, LB F11.)
3. Two line ends per row, n/2 arch lines per midpoint, so >= n/4 non-P rows per midpoint.
   [FINITE CHECK, not a proof for all depths] The cheapest non-P edge pattern costs 2/row (+1): w-structures S9
   (D = 3..5 OPTIMAL), LB F12 W = 4 exact. So the arch term is >= n - O(1) for all mechanisms of steps 2-3.
Consequence: with chevrons, the arch flips (n) are optimal up to the measured edge rate. A design that beats
19n/3 through the arch term must have NO chevrons (total chevron length < 2n), not a better arch fix.
Combined flux + arch routes (corner charge along the edge past the arch ends, then out through the interior)
were costed with the F12 rates: BL corner -> edge to (0,h) -> midline -> centre = n/2 + 3n/8 = 7n/8 per corner,
against n/3 + n/4 = 7n/12 in the fold design. Worse.

## G3 (2026-10-03, PROOF in the stated scope): the d|c bend cannot be crossing-free (coset obstruction)

Families d = (2,-1) (lines k = x+2y) and c = (1,-2) (lines k' = 2x+y). Scope: a crossing-free structure whose
edges are only +-d and +-c moves (the {c,d} staircase phase of LB F9), with pure d lines on one side and pure c lines
on the other (any shape, slope, width; no periodicity needed).
- The moves d, c generate a sublattice of index 3 (det = -3). Its cosets are the classes of x+2y mod 3, and
  2x+y = -(x+2y) (mod 3). A path of +-d, +-c moves stays in its coset. So a line that enters as d-line k and leaves
  as c-line k' has k' = -k (mod 3); a path that enters as d-line k1 and returns as d-line k2 has k1 = k2 (mod 3).
- Returns are impossible: returning paths of a crossing-free structure form a non-crossing matching of the d-lines
  they use; every such matching has an innermost pair of adjacent lines (k, k+1), and k != k+1 (mod 3).
- So every d-line passes through, and the line map is an order-preserving bijection of Z, hence a translation
  k' = k + D. Then k + D = -k (mod 3) for every k: impossible.
So the gentle bend d -> c (37 deg) always costs crossings in this phase. Its measured price is 1.0 per unit x
(w-structures S1). This also proves the S1 lane rule c + c' = 0 (mod 3) for every crossing-free part, which is why
seam nests stay trapped per residue class (w-structures S10). A bend through other move types (the long way,
d -> a -> b -> c) is outside this scope.

## G4 (2026-10-03, FINITE CHECK): class-selective edge phase is expensive, so layout G stays above 19n/3

Question: gentle-seam corner nests (layout G, w-structures S10) trap one residue class (lines c = r mod 3).
Can the edge re-pair ONLY that class (even c with c+3 instead of c-3) cheaply?
Model (classphase.py): left edge strip x < D, period p rows, free cells, pure (2,1) lines fixed for x >= D,
exact target pairing (labels + lazy strand checks), crossings per period. Independent unrolled check:
cp_verify.py (degrees, all strands traced in the cover, crossings recounted).
| target pairing | p | D | crossings/period | per row | status |
|---|---|---|---|---|---|
| P (base) | 3 | 3 | 3 | 1.0 | OPTIMAL |
| full flip (c -> c+5) | 6 | 3, 4, 5 | 12 | 2.0 | OPTIMAL, unrolled check ok (D=5) |
| all classes c -> c+3 | 6 | 3, 4 | - | - | INFEASIBLE |
| class 0 only c -> c+3 | 6 | 3, 4 | - | - | INFEASIBLE |
| class 0 only c -> c+3 | 6 | 5 | 17 | 2.83 | OPTIMAL, unrolled check ok |
(D = 6 did not finish in 25 min with 2 workers.)
Reason for the high price: the re-paired class pairs have equal-colour ends (chi sum +-2, alternating every 3 rows),
so the strip must carry a colour current on about half of its rows, and it must do so under a fixed pairing.
Consequence for layout G: each seam nest has 3n/4 rows per arm; +1.83/row on one arm gives about 1.4n per seam
corner, far above the 3n/4 edge estimate of S10. Layout G (4 + 1 + flux + seam-nest fixes) does not beat 19n/3.
Note on the flux of G (UNCHECKED, corner charges of G not computed): in the fold-field convention the two fold
corners BL, TR both carry -1, so the seam corners must carry +1 each (total 0). A gentle seam carries +-1 at no
extra cost (w-structures S3), so all four charges can still meet at the centre for 2n/3; the G flux estimate
stands if these charges are right. The trapping cost above is what kills G.
Commands: `python classphase.py 6 5 0 300 2`, `python cp_verify.py 6 5 0`, `python classphase.py 6 5 F`.

## G5 (2026-10-03): status of "designs outside the fold family" (summary of G1-G4 and w-structures S1-S11)
- Steep same-edge free-fold returns have net cycle step +1, i.e. chevron type up to cancelling fold pairs (G1, PROOF). Chevrons cost >= 1/2 per arch line by any mechanism (G2, ARGUMENT).
- Free-fold layouts with all edges steep: only the 8-triangle field on k x k grids, k <= 8 (S10, FINITE CHECK);
  its chevrons have total edge length 2n, so arch = n.
- Removing chevrons needs non-free bends. The gentle bend is never crossing-free (G3, PROOF); its optimal price
  1/3 crossing per line (one transposition per lane of 3, S1) matches the coset obstruction; its nests trap a
  residue class, and the class-selective fix costs +1.83/row (G4). Single-parity seams cost 3.0/unit x (S10).
- A-family pleats (stacks of horizontal free folds) keep every line monotone in y and compose to shift 0, so they
  add no new nest types (consequence of G1).
Verdict: in the space "line fields + free folds + measured seams + edge patterns", 19n/3 is the minimum found,
and the arch term is tight by G2. A gain must come from the flux term (Edge Searcher) or from structures that are
not line fields (no candidate known).

## G6 (2026-10-03, FINITE CHECK): no cheap edge fix for gentle-seam nests; layout G is closed

Budget: layout G costs 4n (edges) + n (anti-diagonal gentle seam) + 2n/3 (flux, if the charges are as in the
G4 note) = 17n/3 before its two seam nests are untrapped. Each seam nest has 3n/2 lines and 3n/4 rows per arm.
G beats 19n/3 iff the two fixes cost < 2n/3 together, i.e. < 4/9 extra per row on one arm.
Chord model (seamnest.py): left pairing lam, seam map c -> c + s(c mod 3), top pairing P. With s = (0,1,-1)
(one transposition per lane, the cheapest seam, S1) P traps exactly 1/3 of the lines; the full flip untraps all;
s = (3,1,-1) (single parity, 3 transpositions per lane = the measured 3.0/unit x) untraps with P.
Seam prices (ARGUMENT + exhaustive check): by G3 a seam has s(r) = r (mod 3) for each class r; two lines whose order
changes must cross, so the cost is >= the inversions per lane of 3. Over all vectors with |s(r)| <= 11 the minimum
is 1 for mixed parities (these trap 1/3 or 2/3 of the lines) and 3 for all-odd (untrapping) vectors; larger
shifts only add inversions. These meet the measured optima 1.0 and
3.0 per unit x of w-structures S1/S10, so both prices are exact.
Search (seamsearch.py): all periodic left pairings with period 6 lines (48) and 12 lines (720), |shift| <= 5;
untrapping ones: 20 and 108. Exact strip price (classphase.py with the pairing as target, D = 4 and 5):
- period 6 lines: the full flip 2.0/row (OPTIMAL) is the cheapest; the other 19 are INFEASIBLE or cost
  2.83-5.67/row (seamsearch_P6_D5.log).
- period 12 lines, the 6 pairings closest to P (from 4 changed entries up): 2.83/row or INFEASIBLE
  (seamsearch_P12_D5.log).
So the cheapest tested edge fix is the full flip, +1/row on 3n/4 rows per seam corner: G = 17n/3 + 3n/2 = 43n/6.
Verdict: layout G and its relatives (seam corners) cannot beat 19n/3 with edge fixes or seam choices.
Commands: `python seamnest.py`, `python seamsearch.py 6 5 5 150 20`, `python seamsearch.py 12 5 5 200 6`.

## G7 (2026-10-03, PROOF via the audited 14n/3 lower bound, Section 3): no corner type with cheap edges is neutral

Question (CR): is there a corner type whose colour charge is 0 mod 3 (so it drops out of the flux network)?
Answer: NO, for every corner type whatsoever (any interior structure, folds, seams, gadgets of any size), as long
as the two edges are in the cheap patterns P or P' near the scan rows.
- The audited lower-bound proof (w-turnstheory/PROOF_crossings_lower.md, Section 3, finite endpoint lemma + flux
  identity (3)) shows: for every R in [12, n/2 - 4], if the endpoint tests pass at both ends of the L-shaped dual
  path gamma_R around a corner, then gamma_R is charged (flux = 1 mod 3). The tests read only edges within
  distance 2 of the two end cells (0,R) and (R,0).
- corner_test.py: P and P' (both line families, every scan row) pass the up test and the down test (F = 2 mod 3,
  forbidden pair absent). So every gamma_R whose two ends lie on P/P' stretches is charged, whatever the corner
  contains.
Consequence: a corner's charge can leave the region inside gamma_R only through gamma_R itself, that is, through
an interior carrier that crosses every gamma_R, or through edge rows that FAIL the test (non-P rows, i.e. an edge
carrier, measured +1/row). Changing the corner type cannot remove a corner from the flux network; only carrier
rates matter (Edge Searcher; Claim 17 floor). This closes option (b). Command: `python corner_test.py`.
