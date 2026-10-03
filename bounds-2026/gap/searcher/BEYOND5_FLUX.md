# Beyond 5n, flux half: a carrier pays more than 1/2 per path when its zone is counted (DESIGN, 2026-10-03)

Author: KT Edge Searcher. Status: DESIGN. Labels: PROVEN / CERTIFIED (finite, stated model) / ARGUMENT / CONJECTURE.
Sources: gap/turnstheory/PROOF_5N_PLAN.md (identity (1), S*, retained paths C), gap/turnstheory/PLAN.md (L2-v3),
w-integrator/FINDINGS.md (colour-balance lemma), gap/searcher/FINDINGS.md sections 7 and 8, WALL12.md.

## 1. Target statement (pure crossing currency)

Notation as in PROOF_5N_PLAN.md section 1: N = 2n - 60 audited corner paths gamma_R, retained set C, L = |C|,
D_loss = N - L, S* = union of the width-two side crossing-pair sets, s = |S*|, E = X - 4n + 2, T = s - 4n + 2.
Let X_out = number of crossing pairs NOT in S*.

**F-beyond(p), CONJECTURE.** There are p > 1/2 and C such that every closed knight tour (n even, n >= n0) has

    X_out >= p * L - C.

**Reduction (PROVEN, hand algebra).** E = T + X_out exactly. The audited beta = 1 restoration gives
T + 1160 >= D_loss. So E >= p L + D_loss - C - 1160 >= p N - C' (p <= 1), and

    X >= 4n + p(2n - 60) - C'.     p = 2/3 gives 16n/3 - O(1); any p > 1/2 gives more than 5n.

This uses NO mixed currency: holes, W3 and X1 are not needed.

**Correction (Turns Theory reply, gap/turnstheory/FINDINGS.md top, 2026-10-03).** (i) The 193-tour pure Hall data
excludes B (outermost-column pairs), not S*, so it does NOT test F-beyond. (ii) On saved tours, X_out alone is far
below L/2 (LF5 n = 260: L = 332, X_out = 91, T = 724; check_pure_aggregate.py): those tours carry the flux in the
side strips. So F-beyond(p) as stated is the wrong target. Use the deficient paths of Claim 42 instead:

**F-beyond'(p), CONJECTURE.** With L_def = retained paths that are deficient in the sense of PROOF_5N.md (no two
payable quarters off the strips; paid by strong rows), every closed tour has

    X_out >= p (L - L_def) - C.

**Reduction (from audited inputs).** F1-V (Claim 42): T + 1160 >= D_loss + L_def (one strong row per lost or
deficient candidate, at price 1 in pure T). Hence E = T + X_out >= D_loss + L_def + p(L - L_def) - C - 1160
>= p N - C' for p <= 1, and X >= 4n + p(2n - 60) - C'. Deficient paths are paid at 1 > p by the strips, so the
carrier analysis below is needed only for the non-deficient paths, whose defects are in their middles (interior
carriers). Turns Theory's alternative X_out + R >= pL - C (R = T + 1160 - D_loss) is weaker and also suffices.
Check to request: X_out versus p(L - L_def) on the saved tours (Turns Theory has the tools).

## 2. Why the pure currency, and where 1/2 comes from

In pure crossings (lambda = 1, wall.cpp) the straight psi carriers cost per level crossed (W = 4, CERTIFIED in the
band model, FINDINGS 7): (1,1) 2/3, (0,1) 2/3, (1,2) **1/2**, (1,3) 5/9, (2,3) 7/12. In the mixed nu currency
the (1,1) wall also costs 1/2 (lambda = 1/2 column), so the mixed currency cannot pass 1/2 without the zone
argument for TWO carrier families. The pure currency has only the slopes strictly between (1,1) and (0,1) below 2/3.
The 1/2 is real in the plane: the (1,2) wall with a perfect plane extension (Claim 35). So any proof of p > 1/2
must use what the plane extension hides: the closed tour must END the fields that the cheap wall needs.

## 3. The facts it rests on

| id | statement | status | finite input |
| --- | --- | --- | --- |
| P1 | Straight carrier between STRAIGHT-word ribbon fields (all ribbons of one side have one bit) costs >= 2/3 per level, every direction | CERTIFIED for (1,2) (none below 1, WALL12 s.2); (1,3), (2,3) TO RUN (fields of the witnesses are mixed words HVVVHV / VVHHVHVV, ribbon_ends.out); other slopes >= 2/3 already | wall_if.cpp, about 20 runs |
| P2 | The (1,2) wall at 1/2 needs zigzag z0 \| z0 (same orientation) on both sides | CERTIFIED W = 4 (FINDINGS 8, orient run) | done |
| P3 | Colour current: for any cell set S of a 2-regular graph, (black-ended minus white-ended edges leaving S) = 2(B_S - W_S). Relative to straight fields, a zigzag ribbon carries current 3/2 along its ribbon direction; straight fields carry 0; a straight boundary line can supply at most 1 per unit length (a, b odd), 0 (a + b odd) | PROVEN (first identity, one line); field currents: Integrator's lemma, PROVEN for periodic bands | none |
| P4 | Consequence: a zigzag region is bounded along its ribbon direction only, never touches an axis side, and its current returns only through turns ('/' zigzag \| '\' zigzag, axis-parallel line) or through defect regions | ARGUMENT for finite regions (current must cross a transverse cut of bounded width); PROVEN for periodic bands | none |
| P5 | Price of a zigzag ribbon end: >= 1/3 per end at every boundary slope (relaxed model, lower bound); 1/2 per end at a colour-balanced turn | CERTIFIED W = 4 (FINDINGS 8.1, 8.2) | done |
| P6 | Mixed-word fields (any word not straight) carry current proportional to their bit alternations; the (1,3), (2,3) witnesses need it too | CONJECTURE (to check with P3 on the saved witnesses) | ribbon_ends.py |

## 4. Counting argument (ARGUMENT)

Fix one corner and its carrier: the defects that the nested paths gamma_R (R in [12, n/2 - 4]) cross. Cut the
carrier into straight pieces. Only pieces in zigzag zones are below 2/3 per level (P1, P2). In the region y > x
(levels = rows) a '/' zone has ribbons x - y. Piece types inside one zone (W = 4 prices, pure crossings):

| piece | levels gained per ribbon crossed | crossings per ribbon crossed | ribbon direction |
| --- | --- | --- | --- |
| forward (1,2) wall | 2 | 1 | forward |
| back (2,1) wall | 1 | 1 | back |
| back (1,0) | 0 | >= 2/3 | back |

Every zone ribbon segment has two ends, at >= c each (P5: c >= 1/3 relaxed, 1/2 balanced). Let F, B be the ribbons
crossed forward and back, and mu the number of corners that use the same segments. Net segments >= (F - B)/mu.
Per level crossed:

    price >= [F + B + 2c (F - B)/mu] / (2F + B)  >=  min( 2/3 , 1/2 + c/mu ).

(Linear-fractional in B/F on [0,1]: B = F gives the thin-stripe staircase at exactly 2/3 = the diagonal carrier;
B = 0 gives one straight wall plus its zone.) A '/' stripe along (1,1) passes near two corners only (BL and TR;
the TR carrier can use a (2,1) wall on the same ribbons), so mu <= 2. With c = 1/3 the bound is exactly 2/3: no
slack, and p = 2/3 would give 16n/3. With any c > 0 it is 1/2 + c/2 > 1/2: **beyond 5n needs only c > 0**.

Bridging to F-beyond(p): each retained path is crossed by its corner's carrier; sum over levels and corners. The
zone ends must be charged to paths: ends lie in the corner squares (inside N_r of SOME retained paths, possibly of
another corner), so the aggregate statement is the right form; a per-path local rule is not needed for X.

## 5. What is still ARGUMENT, and the main risks

1. Non-straight carriers (curved, mixed pieces, branching) are priced as sums of straight pieces: corner/bend
   costs >= 0 assumed. Risk: a curved defect could be cheaper than its straight pieces.
2. W = 4 only for every price (W = 5 does not fit in 8 GB). Risk: a wider zone end costs less than 1/3. Only c > 0
   is needed for > 5n, so a qualitative proof of P5 suffices for the coefficient > 5; 2/3 needs c = 1/3 exactly.
3. P4 for finite, irregular regions: the current argument must be made local (a cut of width w carries current
   <= 4w), and zone ends inside defect regions must still be priced (a defect region that absorbs current is itself
   a zone end; P5 prices only straight ones).
4. P1/P6: other mixed-word fields (not zigzag) might give cheap walls with LESS current per level. Then c must be
   taken per unit current, and the LP gets one row per word family.
5. Retention: paths lost at the endpoint tests are paid by restoration at 1 (pure T); no new input needed.
6. (from the corrected target) A non-deficient path may own its two payable quarters only through S* pairs with a
   one-quarter overlap (X1 atoms of S* pairs, depth <= 2). Such a path has no interior defect, and its crossings are
   in T, which F1-V already spends on strong rows. These "strip-paid, non-deficient" paths need either a joint strip
   price above 1 per strong row plus p per such path (KT Lower Bounds B5 found c* = 0 for changed ports: a warning),
   or a proof that they are deficient-like. This is the strip half of the problem, not the flux half.

## 6. Proposed finite program (after CR approval; each item small, one job at a time, <= 8 GB, watchdog)

- A. P1 completion: (1,3), (2,3), (3,4) walls at lambda = 1 with straight-word margins (CELL 00/22 x 00/22,
  '\' too): expect >= 2/3. About 20 runs, 2 h.
- B. P6: colour current of every cheap witness (extend ribbon_ends.py with P3's count). Minutes.
- C. P5 in the TRUE model: zone ends with the zigzag ENFORCED on ZW = 2 columns and the ghost cells beyond the
  margin forced into the field (no colour leak), to replace "relaxed >= 1/3" by exact prices. Pilot first.
- D. A non-straight test of the whole claim: a carrier band that must cross k levels with a zigzag zone inside a
  bounded window (both zone ends inside), exact min cost by transfer matrix along (1,1). This tests risk 1 and 3
  together. Design to be agreed with Turns Theory (window size, eligibility radius).
Proof size if all go through: hand algebra (section 1) + P3 (one-line identity + Integrator's lemma) + a counting
argument (section 4) + finite certificates A, C (band transfer matrices, about 30 runs). Risk 1 is the hard part.

## 7. Status after the first finite program (2026-10-03; details FINDINGS.md 9.1-9.6)

- B: walls below 2/3 carry colour current, but NET current cancels (z0/z1 stripes): price zones by switched
  ribbon ends, not by current (risk 4 resolved this way).
- A (CERTIFIED, W = 4): walls between straight-word fields >= 2/3 at every tested slope.
- Slope table: every slope strictly between (0,1) and (1,1) is below 2/3 without its zone (min 1/2 at (1,2)).
- Wall + zone (CERTIFIED per slope for ANY words, given e and mu): crossings + e|1-s|/4 * mixed margin squares.
  At e = 1/2, mu = 2: minimum over 13 slopes = 31/50 at (3,5). With the staircase cap: flux price per level
  p* >= 31/50 > 1/2, i.e. X >= 4n + (31/25) n - O(1) = 5.24n - O(1), conditional on the ARGUMENT steps.
- C (CERTIFIED per boundary slope, W = 4): e >= 1/2 per switched ribbon end for ANY word at slopes 0, +-1/2,
  +-2/3 (more slopes running). e <= 2/3 is forced by the zigzag | V line at s = -1/2.
Still ARGUMENT: straight-piece decomposition (bends, curved zone ends), mu <= 2, the staircase LP for general
back pieces, W = 4 only, and the strip-paid non-deficient paths (risk 6, strip side).
