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

## 7. Version 2 after Verifier Claim 36 (2026-10-03)

**(A) repaired.** Only cheap slots carry labels, so the identity is W + D + I + X_E = (cheap slots) = 4(n - 2d) - EXC
(d = 3: 4(n-6) - EXC), provided the stopping rule (W, D, I, X_E) is exhaustive.

**Barrier step repaired (36E is right).** A wall edge carries no tile, but strands pass through wall VERTICES
((x-2,-1)-(x,0)-(x-2,1) in the A|A' fold), so a wall is not a barrier. This is exactly how a chevron chord returns.
So the half-chamber "label path + wall face" and the attached-wall statement of section 6 are WITHDRAWN. What stays:
barrier pieces must avoid lattice points. Ribbon pieces are taken along the strip MIDLINES (y - x = k - 1/2 for '/'),
which hold no lattice point; then the crossing fact holds as stated (a tour edge meets the strip inside a good square of
its split only as a present link). A barrier may cross a wall line only transversally at a unit-edge midpoint
(free: no tile, no vertex). The FULL-TRIANGLE chamber (lower label midline and upper label midline meeting at one wall
edge midpoint) is valid, with the count of section 6. It needs the partner (upper) ribbon to reach the side as a
ribbon path; the pleat deflector is the case where it does not. The defect-free proof of (B) is not affected.

**Exact FOLD measurement (Verifier exact P/P' windows, `fold_exact_scan.py` = claim36_scan.py without its JSON write).**
| n | E | BQ | EXC | SSR (two cheap ends) | E - BQ/4 - EXC |
|---|---|---|---|---|---|
| 96 | 338 | 622 | 155 | 47 | 27.5 |
| 144 | 450 | 878 | 203 | 79 | 27.5 |
| 192 | 562 | 1134 | 251 | 111 | 27.5 |
| 240 | 674 | 1390 | 299 | 143 | 27.5 |
| 288 | 786 | 1646 | 347 | 175 | 27.5 |
So E = BQ/4 + EXC + 27.5 exactly on the whole family (slopes 7/3 = 16/3 / 4 + 1): the flux corridors are paid exactly by
1/4 per interior bad quarter and the arch flips by 1 per exception slot. Consequences:
1. A price of 1/2 per exception slot is too low and 1/2 per SSR is too high: with the corridor returns (SSR = 2n/3)
   priced separately, BQ/4 + EXC/2 + SSR/2 does not describe the budget; BQ/4 + EXC + SSR/2 would exceed E.
   Returns through bad squares must not get a separate price. (C) is restated below for CLEAN returns only.
2. The revised (B) (weight 2 on EXC) holds on FOLD only because of the corridor bad quarters (8.67n vs 4n). Its idealised
   tight case "8-triangle field + arch flips" (BQ = O(1), EXC = n) gives BQ + 2 EXC = 2n < 4n. That layout is not a
   tour (the corner charges need flux corridors), so this is not a counterexample, but weight 2 on EXC has no margin
   argument behind it.

**Restated target (T5), for closed tours.**
    (B_T)  BQ + 4 EXC >= 4n - O(1),          (D_T)  E >= BQ/4 + EXC - O(1).
Then E >= n - O(1). (D_T) is tight on FOLD with constant 27.5; (B_T) is tight for the idealised arch-flip layout and for
gentle seams (BQ = 4n). In (D_T) the exception count should be replaced by N_re/2 (N_re = side ports whose collar
partner differs from P / P'), because overlapping windows make one changed row several exception slots (36D); Claim 28
certifies 1/2 per changed end (fixed exterior, depth <= 4). NOT YET MEASURED: N_re on FOLD (expected 2n).
Route to (B_T): (B) restricted to clean returns, BQ + 2 SSR_clean + 2 EXC >= 4n, for 2-factors (SSR_clean = returns
whose interior lies in good squares), plus
**(C') Clean Return Lemma (CONJECTURE).** In a closed tour, SSR_clean <= EXC + O(1) (each clean return with two
cheap ends would be a free-fold return, hence chevron type (G1, PROOF), hence P-trapped in its nest (Claim 28C), so a
nest of clean returns forces changed ends). This replaces the trapping premise refuted in 36C, which concerned returns
through corridor bad squares. With (C'), (B) restricted to clean returns gives BQ + 4 EXC >= 4n.

## 8. Clean returns, the trap parity, and N_re (2026-10-03, KT Structures, third session)

Scripts (gap/structures/): `chord_census.py` (all same-side chords: clean or not, end fields, shift parity),
`nre_scan.py` (changed port ends N_re; changed ends per clean return), `census_run.sh` (reruns both on 13 tours,
log `census.log`). Exact Verifier P/P' windows (`fold_exact_scan.run`), d = 3.

**Definitions.** A RETURN is a chord whose two ports are on one side (any port type). It is CLEAN if every interior
vertex of the chord is a good point (its four squares are good). RET_clean = number of clean returns (no condition
on the ends). SSR_clean = clean returns with two cheap ends. A port is CHANGED if its collar partner (follow the tour
outside the interior until it re-enters) is not its P / P' partner. N_re = number of changed ports.
Line labels in the side frame: c = x - 2y for a '/' port (inner vertex), c = x + 2y for a '\' port.
The P rule, read off from all ports in cheap windows of 13 tours, on all four sides, both fields, no conflict:
partner(c) = c - 3 for even c, c + 3 for odd c.

**8.1 Clean returns are chevrons (PROOF; this checks the G1 hypothesis).** At a good point v of a 2-factor the two
edges at v lie in opposite octants (straight) or adjacent octants (a free fold). Proof: by T3 v is single-split or on
a straight wall. In a '/' word field the edges at v are one of {a-out, b-in} and one of {a-in, b-out} (T2(b)); the
four pairs are straight (a-out + a-in, b-in + b-out) or adjacent ((2,1)+(1,2), (-1,-2)+(-2,-1)). On a horizontal wall
the edges are (-2,-1), (-2,1) (or the mirror), adjacent across the ray 180 deg; vertical walls likewise. []
So a clean return, cut at the collar boundary line x = 5/2 (no lattice point, crossed only by its two port edges),
is a simple arc (its tiles lie in good squares, so no edge crosses it) whose turns are free folds: G1 applies.
Consequence: a clean return goes from a P port ('/'-H) to a P' port ('\'-H) ABOVE it (or the mirror), never P to P,
and its composite fold isometry is g(x, y) = (x + t_x, t_y - y). Its SHIFT s = c_up - c_low = t_x + 2 t_y.
Caution: requiring only that the chord's tiles lie in good squares is NOT enough; at a bad point two good tiles can
meet at a non-free angle (e.g. (2,1) and (-1,2) with a wall edge between them). Keep the good-POINT definition.

**8.2 Trap parity (PROOF).** Let rho run from lower line c to upper line c + s and rho' from P(c) to P(c) + s', with
all four collar pairs unchanged. If s' = s and s is even, then partner'(c + s) = P(c) + s (the parity rule is the
same in both labels and s keeps the parity), so rho, rho' and the two collar U-turns close into a cycle of four
pieces: a closed tour cannot contain it (n large). If s is odd, partner'(c + s) = P(c) + s +- 6: the alternating
chord / collar path advances by 6 lines (this is the opposite matching of Claim 36C). For a single horizontal wall
at y_w, g is the reflection in y = y_w and s = 4 y_w: even, trapped (Claim 28C).

**8.3 Development (PROOF modulo Lemma F, which is still not written out).** Two clean returns rho, rho' with P / P'
windows at their ports: if the region Q between them (bounded by the two chords and the two short side pieces)
contains no bad square, then g' = g. (Develop around the loop rho -> upper window -> rho' -> lower window; it lies in
a simply connected good region, so the monodromy is trivial.) Hence, in a closed tour, a clean return with NO changed
end has (i) a P-partner chord rho' that is not a clean return, or (ii) a bad square in Q(rho, rho') where g changes,
or (iii) odd s. To break a trapped pair one collar pair must change, and that changes one end of BOTH rho and rho'.

**8.4 Measurements (CHECK, all 2026-10-03).**
| tour | n | RET_clean | of these: odd s | SSR_clean | clean returns with 0 / 1 / 2 changed ends | N_re | E - BQ/4 - N_re/2 |
|---|---|---|---|---|---|---|---|
| FOLD | 96 | 138 | 0 | 0 | 0 / 135 / 3 | 194 | 85.5 |
| FOLD | 144 | 234 | 0 | 0 | 0 / 231 / 3 | 290 | 85.5 |
| FOLD | 192 | 330 | 0 | 0 | 0 / 327 / 3 | 386 | 85.5 |
| FOLD | 240 | 426 | 0 | 0 | 0 / 423 / 3 | 482 | 85.5 |
| FOLD | 288 | 522 | 0 | 0 | 0 / 519 / 3 | 578 | 85.5 |
| FIELD | 166 | 219 | 0 | 0 | 0 / 217 / 2 | 486 | 107 |
| FOLDB1 | 144 | 227 | 0 | 0 | 0 / 225 / 2 | 308 | 106.75 |
| FOLDP | 96 | 133 | 0 | 0 | 0 / 131 / 2 | 192 | 96.75 |
| FOLDX | 100 | 135 | 0 | 0 | 0 / 132 / 3 | 208 | 90.75 |
| FJOG | 130 | 0 | - | 0 | - | 148 | 335 |
| LF4 | 96 | 0 | - | 0 | - | 362 | 143 |
| TT16 | 72 | 0 | - | 0 | - | 264 | 264 |
Facts: (1) all 2,364 clean returns are chevrons P -> P' with EVEN shift (FOLD: s = 4 y_w = 2n); none is P -> P (G1).
(2) Every clean return has a changed end; none has two cheap unchanged ends, so SSR_clean = 0 on every tour: (C')
holds trivially on all data. The tour pays for each trapped pair exactly as 8.2-8.3 predict (arch flips).
(3) N_re = 2n + 2 exactly on FOLD, and E = BQ/4 + N_re/2 + 85.5 exactly (n = 96..288). E >= BQ/4 + N_re/2 holds on
all 13 tours. So the exception price "1 per exception slot" of section 7 is "1/2 per changed end", as Claim 28 prices it.
(4) Odd shifts exist only on DIRTY returns: FJOG has 37 + 30 chevrons with odd s (n = 130, 132); the ones with all
turns free (11 at n = 130) each have 6-10 bad tile quarters on the chord: they cross a jog band. (Throwaway
diagnostic, not saved; the parity counts are in census.log.)

**8.5 Parity Lemma (CONJECTURE).** Every clean return has even shift.
Why it should hold: s = t_x + 2 t_y = x_up - x_low (mod 2) = number of |dx| = 1 edges (b, c moves) on the chord
(mod 2), i.e. the parity of the number of V ribbon steps the chord crosses. An odd count means the chord crosses a
V run whose one end lies in the disk D(rho) between rho and the side. A V run in an H field shifts strand lines by 3:
by S8 it carries odd current, and by G2 step 1 (current conservation; the pushed copy of a clean chord is crossed by
no tour edge) the current must leave D(rho) through the collar, i.e. through a non-P row WITH current in rho's side
segment. So odd s costs a current-carrying collar row plus a carrier for the far end of the run. Not yet a proof:
nested returns share their inner side segment, so ONE such row would serve a whole nest; the price must come from the
carrier of the run's far end. This is exactly where flux (Turns Theory route) and connectivity meet: a corner-charge
carrier routed as a V run through a chevron nest would untrap the whole nest. The data show no such layout; G2's
costing of "corner charge along the edge, then through the interior" (7n/8 vs 7n/12 per corner) says it is worse.

**8.6 Consequence for the route (restatement of T5; CONJECTURE, no proof yet).** The (B) statement with SSR_clean
(two cheap ends) is the wrong object: an arch flip of L rows turns about 2L clean SSRs into about L exception slots,
so "BQ + 2 SSR_clean + 2 EXC >= 4n" loses 2L under a purely local collar change and cannot come from a local
(barrier) argument; on real tours SSR_clean = 0 anyway. Use the flip-invariant RET_clean (the repair Claim 36B
suggests: count reference returns) and price changed ENDS:
    (B') BQ + 2 RET_clean + 2 N_re' >= 4n - O(1),   N_re' = changed ports that are not ends of clean returns;
    (C*) in a closed tour, every clean return has a changed end, except O(1) and the boundary cases (i)-(iii) of 8.3;
    (D*) E >= BQ/4 + N_re/2 - O(1)   (tight on FOLD with constant 85.5; Claim 28 certifies 1/2 per changed end).
Then E >= BQ/4 + RET_clean/2 + N_re'/2 >= n - O(1). (B') is a pure 2-factor statement in which flips move nothing
(a flip changes ends of clean returns, which (B') does not count); with no changed ports it reads BQ + 2 RET_clean >=
4n, the original Sheet Lemma with returns counted geometrically; the 8-triangle field is tight. Data: (B') holds on
all 13 tours (FOLD n=96: 622 + 276 + 106; LF4: 4 + 0 + 724; TT16: 0 + 0 + 528; all >= 4n), but only the idealised
layouts test it near equality. Open: (B') itself (Barrier Lemma, section 6), the boundary terms of (C*) (each must
be paid by bad squares on rho' or in Q with a coefficient that keeps E >= n), the Parity Lemma 8.5, and (D*) as one
allocation (Claim 36D).

## 9. (B') by run ends: an exact identity and three lemmas (2026-10-03, KT Structures)

Script: `barrier_scan.py` (uses `nre_scan.py`). Side frame, interior squares with lower-left corner in [3, n-5].

**9.1 Identity (PROOF).** Each interior boundary square on a side is bad, or good; if good, exactly one of its halves
has a leg on the boundary edge (TL for split '/', LB for '\' on the left side), and that half is an end of its run
(T2: one bit per run). The bit is H iff the boundary unit edge CARRIES a tile (the tile of an a / d port (2,y)-(4,y+-1)),
V iff it carries none. Follow the run inward; its other end is (i) at the boundary again (a THROUGH run), (ii) at a wall
face (next square good, other split), or (iii) at a bad square. A '/' or '\' ribbon joins a vertical side to a
horizontal side, and a vertical side wants H, a horizontal side V (R2), so a through run has EXACTLY one frustrated
end. Counting boundary unit edges:
    4(n - 7) = bdry_bad + 2 T + W' + D',     T = through runs = F = frustrated run ends,
W' = runs from a side to a wall face, D' = runs from a side to a bad square. (Checked: exact on all 13 tours.)
Note: W' runs are good from the side to the wall, so the deflector of section 3 (side ribbons cross a defect line)
gives D' runs, not W' runs: the deflector is a Gap-Lemma (bad-square) case in this bookkeeping, not a wall case.

**9.2 Reduction (PROOF given the lemmas).** (B') BQ + 2 RET_clean + 2 N_re' >= 4n - O(1) follows from
    (R2) frustrated ends:  F <= N_re' + O(1)   (each frustrated boundary edge gives its own changed port that is not
         the end of a clean return);
    (R3) bad ends:         bdry_bad + D' + (R4 excess) <= BQ + O(1)   (Gap-Lemma territory, Lower Bounds);
    (R4) wall ends:        W' <= 2 RET_clean + (R4 excess) + O(1)   (the Barrier Lemma in run form).

**9.3 Data (CHECK, 2026-10-03).**
| tour | n | bdry_bad | 2T | W' | D' | RET_clean | W' - 2 RET_clean | F | N_re' |
|---|---|---|---|---|---|---|---|---|---|
| FOLD | 96 | 25 | 0 | 295 | 36 | 138 | 19 | 0 | 45 |
| FOLD | 144 | 25 | 0 | 487 | 36 | 234 | 19 | 0 | 45 |
| FOLD | 288 | 25 | 0 | 1063 | 36 | 522 | 19 | 0 | 45 |
| FIELD | 166 | 27 | 0 | 449 | 160 | 219 | 11 | 0 | 259 |
| FOLDB1 | 144 | 34 | 0 | 479 | 35 | 227 | 25 | 0 | 73 |
| FOLDX | 100 | 41 | 0 | 303 | 28 | 135 | 33 | 0 | 63 |
| FJOG | 130 | 88 | 0 | 244 | 160 | 0 | 244 | 0 | 140 |
| LF4 | 96 | 2 | 352 | 0 | 2 | 0 | 0 | 176 | 359 |
| TT16 | 72 | 0 | 260 | 0 | 0 | 0 | 0 | 130 | 261 |
(R4) holds with a CONSTANT excess on the FOLD family (19 at n = 96, 144, 288) and small constants on the other fold
tours. FJOG is the R4 stress case: its 244 wall runs have NO clean return, because the returning strands cross jog
bands (dirty chords); the excess must be paid by those bad squares (BQ = 2544 there). (R2): on LF4 and TT16 the
frustrated ends sit on the two horizontal sides, and per side F = 88 / 88 against 89 / 90 changed ports (LF4) and
65 / 65 against 65 / 64 (TT16): one changed port per frustrated boundary edge, up to O(1) at corners.

**9.4 What each lemma needs.**
(R2) is local: a V boundary half means the boundary unit edge carries no tile; in a pure V field the side is crossed by
one non-steep (b / c) port per row. To prove: within O(1) rows of a frustrated boundary edge there is a changed port,
and the map is injective. Plan: a finite CP-SAT check on a window (collar columns 0-2 with the board edge, interior
columns 3-6), encoding "no changed port in the window" by steep ports plus lifted pairing labels (as in Claim 28B).
(R4) is the Barrier Lemma. Run form: each wall unit edge receives at most one run per face, and each good wall vertex
carries exactly one strand passage (the A|A' fold), so W' <= 2 (wall vertices reached) + O(walls). The excess over
2 RET_clean comes from wall vertices whose chord is dirty (FJOG), is a cross chord, or is a clean return through
several reached vertices (pleat stacks: the inner faces of a pleat receive no side run, so a pleat stack still gives
W' = 2 RET there). A cross chord through a reached wall vertex needs V ribbons on the far side of the wall that
cannot touch the wall (T3 forcing), so they end at bad squares (D') or at the side (frustrated, F): this is the case
analysis to write. The coefficient of BQ in the excess must keep the total coefficient in (R3) at 1.
