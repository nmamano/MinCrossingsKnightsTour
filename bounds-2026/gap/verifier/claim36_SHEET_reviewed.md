# SHEET: the connectivity piece of the 5n route, as an exact statement (for red team BEFORE proof)

KT Structures, 2026-10-03. Status: STATEMENT + CONJECTURE. Nothing here is proved except where marked PROOF.
Replaces R3 (refuted as a per-wall statement by Verifier Claim 32A). Sources: STRUCTURE.md (T1-T3, audited Claim 30),
GAP_LEMMA.md (sections 1, 6, 11), FINDINGS.md G1-G2, w-verifier Claims 28, 29, 32, 34.

## 0. Why a connectivity piece is necessary (Claim 32A, restated)

In a 2-factor, a wall absorbs side ribbon ends at zero crossing cost (pleat stack). So the 5n route cannot price wall
absorption by crossings near the wall. In the fold field the price of the walls is the ARCH term: the walls make
same-side returns, and a closed tour must repair them. This file states (B) the geometric count "walls make returns",
which holds for 2-factors, and (C) the one-cycle price of a return. (A) and (D) are the bookkeeping around them.

## 1. Objects

Board n x n, x right, y up. Collar depth d (fixed constant, d = 3 unless the red team needs more).
SLOTS: left slot y and right slot y for d <= y <= n-1-d; bottom slot x and top slot x for d <= x <= n-1-d.
There are 4n - O(1) slots. A slot is CHEAP if the tour restricted to the collar window of rows (columns) within d of
the slot is the cheap pattern P or its mirror P' (the two tight 1-per-row patterns, w-structures S9, Claim 28 setting).
Otherwise the slot is an EXCEPTION. EXC = number of exception slots.
INTERIOR = the squares at distance >= d from the boundary. Good / bad squares, halves, ribbons (chains), runs, walls,
absorbing cuts: as in STRUCTURE.md and GAP_LEMMA.md section 1.

Facts used (PROOF, from T2 and the definition of P): next to a cheap left slot the interior field is the pure
'/'-H field (all a-moves) or the pure '\'-H field (all d-moves); next to a cheap top or bottom slot it is '/'-V or
'\'-V. In that field (i) exactly one ribbon of the local split meets the collar boundary at the slot's row, and
(ii) exactly two tour strands cross the collar boundary per row (one strand line x - 2y = c through the lattice
point, one between lattice points; for the a-field). So each cheap slot carries ONE ribbon label and TWO chord ends.

LABELS (repairs of Claim 32B). The label of a cheap slot s is its ribbon, followed from s along the ribbon:
along good runs; through a bad interruption that is NOT an absorbing cut (same bit on both sides, L2) it continues
on the next run of the same ribbon. It stops at its FIRST ABSORBER:
  - a WALL face (the run ends at a good square of the other split),
  - an ABSORBING CUT (GAP_LEMMA.md section 1; one cut stops at most its two ends),
  - an EXCEPTION slot (the ribbon reaches a collar window that is not cheap).
A label cannot stop at a cheap slot: every side ribbon is frustrated (R2: H at vertical sides, V at horizontal
sides, and a '/' ribbon joins a vertical side to a horizontal side). W, D, X_E = numbers of labels of the three kinds:
    W + D + X_E = 4n - O(1).                                                       (A)
CHORDS. A chord is a maximal subpath of the tour inside the interior; its two ends are chord ends at slots (cheap or
exception). It may pass through bad squares and walls. A SAME-SIDE RETURN (SSR) is a chord with both ends at
cheap slots of one side. SSR = their number.

## 2. The folded sheet (dictionary; Lemma F is PROOF-level, short, not yet written out)

Lemma F. On each simply connected union G of good interior squares there is a continuous map phi: G -> R^2 that is
a lattice isometry on every tile, maps the tour edges in G onto edges of the reference field F0 = all a-moves
(x,y)-(x+2,y+1), and is unique up to the symmetries of F0 (the group Z^2 x {+I, -I}). Creases (where phi folds):
walls (reflection in the wall line) and H|V ribbon switches (reflection in a '/' or '\' diagonal). Around a bad
cluster the continuation of phi has MONODROMY in Z^2 x {+I, -I}: defects are the branch points of the sheet.
Consequences: (a) the STRAND LABEL c = (x - 2y) o phi is constant along every tour strand in G (a strand can reverse
its direction on its image line at a horizontal crease: that is how a chevron returns); (b) every cheap side maps to
a vertical segment (identity or a reflection for vertical sides, a diagonal reflection for horizontal sides);
(c) a chord inside G is a segment of one image line, i.e. a CHORD of the image polygon formed by the side images;
an SSR is a chord whose two ends lie on two sheets of the same side image folded over each other.
W-labels are ribbons ending on a crease that is a wall; D-labels end at branch points with nonzero bit monodromy.

## 3. The statements

**(B) Sheet Lemma (geometry; claimed for every spanning 2-factor). REVISED 2026-10-03, before red team.**
    BQ + 2 SSR + 2 EXC >= 4n - O(1),
where BQ = number of bad quarters in the interior whose overlap pairs are not in B (each has c(t) >= 1/4,
GAP_LEMMA.md 4). Proof route: (A) with a fourth label kind (below), the square Gap Lemma for D-labels (2 bad
quarters per cut, 1 per label), and the geometric core
    (B0)  2 SSR + BQ_free >= W + I - O(1),   BQ_free = bad quarters not assigned to absorbing cuts.
Why the first version "2 SSR >= W - O(1)" was withdrawn: a DEFLECTOR. Let a pleat region (horizontal walls every row)
end on a defect line, with a uniform '/'-H field between that line and the side. Side ribbons cross the line (no
bit change) and stop at the pleat walls (W) or at the '\' strips (I, below); their chords zigzag up through the
pleat and never return. So W > 0 with SSR = 0 at the cost of one defect line. The line pays through its bad
quarters: a thin defect line with displacement (dx, dy) is crossed by |dx - dy| '/' ribbons and has at least
max(|dx|, |dy|) bad squares, so >= 2 max(|dx|,|dy|) >= |dx - dy| bad quarters (equality only at slope -1). This is
why (B) must contain BQ: walls and defects trade against each other.
Fourth label kind (gap in the first version of (A)): I = labels whose run ends at a bad square after which the
ribbon's next good-square half lies in a good square of the OTHER split (a defect interface, not an absorbing cut,
not an axis wall). So (A) reads W + D + I + X_E = 4n - O(1).

**(C) Trap Lemma (the one-cycle part).** In a closed tour the SSR chords are TRAPPED by the cheap collars: the
chords and the collar pairings of P / P' close into cycles other than the tour unless chord ends are re-paired. In the
joint ledger every SSR pays >= 1/2 privately (one changed side end at >= 1/2; Claim 28 proves the changed end for
fixed P-compatible chevron nests and the price 1/2 for depth W <= 4 with the fixed (2,1) exterior).

**(D) Joint ledger.** With E = X - 4n + 2 and c_{1/2} (gap/searcher/PLAN.md (II), Claim 29), the prices
1/4 per interior bad quarter (c_{1/2}, already in identity (I)), 1/2 per exception slot over its baseline,
1/2 per SSR (C), are charged to disjoint crossing capacity above the baseline B.

**Conclusion if (B)-(D) hold.** E >= BQ/4 + SSR/2 + EXC/2 - O(1) >= n - O(1), so X >= 5n - O(1). This uses no
flux machinery. (B) is the only new combinatorial statement; (C) and (D) are pricing.

## 4. Tests the statement must pass (all by hand; numbers are exact for the idealised layouts)

| layout | W | D | X_E | SSR | (B0): 2 SSR + BQ_free >= W + I |
|---|---|---|---|---|---|
| 8-triangle fold field (corner diagonal folds, full midline walls crossing at a central defect) | 4n | 0 | 0 | 2n (n/2 per midpoint: left rows (n/4, n/2) return, 2 chords per row) | 4n >= 4n, TIGHT |
| one wall of length l from a side (chevron), wall end at a defect | 2l (l per face) | - | - | l (rows within l/2 of the wall return) | TIGHT |
| pleat stack on a board (Claim 32A) | 0: walls every row make every slot of all 4 sides an exception (a slot window is not pure P / P') | 0 | 4n | 0 | 0 >= 0 |
| pleat region in the interior | its walls end at defects; side labels reach it only through those defects or faces | | | | must be checked: red-team target 1 |
| interrupted ribbon (Claim 30B) | the interruption is an absorbing cut: D-label, priced by the Gap Lemma, not by (B) | | | | not used |
| 4-triangle seam layout (diagonal defect seams, no walls) | 0 | 4n | 0 | 0 | 0 >= 0 |
Rigidity (PROOF, T3 forcing): with no defects, walls are full lines of one direction (they cannot end or cross at
good points), say horizontal; horizontal walls force H, so the labels of the top and bottom slots cannot stop at a
wall and stop at exception slots: X_E + EXC >= 2n - O(1). The 8-triangle field shows that ONE O(1) defect suffices to have walls of both
directions. So (B) is not a defect-free statement; its content is that defects cannot convert wall labels into
returns more cheaply than the Gap Lemma prices them.

## 5. Red-team targets (please attack these first)

1. A configuration where defects DEFLECT chevron chords (a chord crosses a wall but meets a bad cluster before its
   return and leaves for another side) while the side ribbons still end at the wall. (B) has zero slack, like R5:
   one such cheap deflector breaks it. If (B) fails only by a defect term, the term must be paid by bad quarters
   that the Gap Lemma assignment does not already use.
2. Walls far from the sides (both ends at defects) reached by side labels: do their chords return?
3. (C) for SSR chords that are not chevrons of one wall (chords through defects, or nested returns from different
   walls): is the trapping still forced? Claim 28 proves it only for fixed P-compatible chevron nests.
4. The slot conventions near the corners and at wall ends on a side (a wall end makes O(1) slots exceptions).

## 6. Proof skeleton for (B0): the barrier count (2026-10-03)

**Defect-free case of (B): PROOF.** If no interior square is bad, walls cannot end or cross, so they are full lines
of one direction, say horizontal (or absent). Then every strip between walls is single-split. In the top and bottom
strips each ribbon meets the top (bottom) side and the left or right side or a wall (which forces H): its top slot
cannot be cheap; with no walls at all, each of the 2n ribbons of the single split meets a vertical and a horizontal
side, so one of its two slots is an exception. Either way EXC >= 2n - O(1), so 2 EXC >= 4n - O(1).

**Crossing fact (PROOF).** Ribbon k ('/') is the strip {k-1 <= y-x <= k}. A tour edge that meets the strip inside a
good '/' square is a present link of ribbon k (the square's quarters are covered once, by '/' tiles only). In a good
run no two consecutive links are present (n_h = 1). So a stretch of a good run with L links is crossed by at most
ceil(L/2) tour edges, i.e. by at most one edge per diagonal unit step. A wall edge carries no tile, so no tour
edge crosses it.

**Chamber count (PROOF).** Let sigma be the segment of the left collar boundary between rows r1 < r2, and pi a
simple path in the interior from the end of sigma at r1 to the end at r2, made of: diagonal ribbon pieces inside good
squares of the ribbon's split, wall pieces, and pieces through bad squares. Suppose pi is y-monotone. Then pi is
crossed by at most (r2 - r1) - (vertical wall length on pi) + extra(pi) tour edges, where extra(pi) counts the
crossings inside bad squares beyond one per unit of height (at most the sum of m_q - 1 over the bad quarters of the
path halves, plus one per bad half). Every chord with an end on sigma either returns to the left side or crosses pi
an odd number of times, with distinct chords using distinct crossing edges. A cheap slot has 2 chord ends. So
    (SSR ends on sigma) >= 2 cheap(sigma) - (r2 - r1) - extra(pi) >= cheap(sigma) - EXC(sigma) - extra(pi),
because cheap(sigma) + EXC(sigma) = r2 - r1. The bound is exact for the chevron and for the 8-triangle field.
It is also additive: the union of two chambers with crossing boundaries is a chamber, with a y-monotone boundary
made of the outer pieces (checked: crossings <= rows of the union), so the chambers can be taken disjoint on the side.

**Attached walls (PROOF modulo the price of `extra`).** Call a wall ATTACHED to a side if it reaches that side's
collar. Left W-labels end only on horizontal walls with '/' below and '\' above ("left-facing"; a '/' label
arrives from the lower left, a '\' label from the upper left), so they all come from the left side. For an
attached left-facing wall at height y_w, let r_min be its lowest lower-face label row; the barrier is that label path
followed by the wall face back to the side (y-monotone; wall edges are never crossed). A '/' label path cannot pass
through another attached wall below y_w (it would end there), so every attached wall that it encloses has its
labels inside sigma = [r_min, y_w]; with the symmetric chamber above and the union rule, the attached-wall labels
of one side lie in disjoint chambers. Hence
    2 SSR >= W_att - EXC - e_max EXC - sum extra(label paths),
where extra(label paths) comes only from the bad squares at NON-absorbing interruptions of the label paths.
Bound for one bad square S on a '/' path (half h): the tour edges meeting strip k inside S are the present links at h
and the '\' edges of S (each '\' edge in S crosses both '/' halves), so at most n_h + n_RT + n_LB =
m_q1 + m_q2 - n_h edges (q1, q2 = the quarters of h). This can exceed the good-run baseline 1/2 by up to about 2
while h's own quarters are good (the square's bad quarters sit in the parallel half), so extra is paid by the
square's bad quarters only with a coefficient > 1, and a bad square can lie on up to 4 barrier paths. Whether such
interruptions occur in tight layouts is open.
Unattached walls (both ends at defects or the far side) are the open part: the deflector of section 3 is the model.

**Barrier Lemma (OPEN; the remaining content of (B0)).** For each side, the rows of its W-labels can be covered by
disjoint side segments sigma_j that carry y-monotone barrier paths pi_j as above, with sum_j extra(pi_j) +
(I-labels) <= BQ_free + O(1). Construction to try: start at the label path of the outermost W-label (side to wall
face), walk along the wall face toward the side; at a wall end (a bad cluster) pay extra and continue along the
ribbon of the local split (or a wall) that moves away from the wall and toward the side, keeping y monotone; never
cross a good square of the other split diagonally (that costs crossings without bad quarters); stop at the side.
Then 2 SSR >= W - EXC - sum extra. Risks: (i) the barrier may be forced to the perpendicular side (then the chamber
holds cross chords, not returns); (ii) a bad quarter on a barrier may also be an assigned Gap-Lemma quarter
(double use); (iii) constants: the skeleton gives 2 SSR >= W - EXC - extra and uses X_E <= 2 EXC, so (B) comes out
with weight 4 on EXC (price 1 per exception slot) unless X_E is counted more finely. G10 (>= 1.5 per V end)
suggests the price is there, but it is not proved. (iv) A chord from a cheap slot of sigma to an EXCEPTION slot of
sigma neither crosses pi nor counts as an SSR; the count must subtract up to e_max chord ends per exception slot
(e_max = the largest number of tour edges across the collar boundary in one row), which again raises the weight on EXC.
