# Piece 1 plan: a finite certificate for the private flux price (KT Edge Searcher, 2026-10-03)

Status labels: PROVEN / CERTIFIED / ARGUMENT / CONJECTURE. Notation as in w-turnstheory/PROOF_crossings_lower.md.

## 1. The accounting identity (PROVEN, short; please check, Turns Theory)

Let G = uncovered quarters, X1 = crossing pairs whose tiles overlap in ONE quarter, W3 = sum over quarters of
binom(m-1, 2) (waste of triple and higher cover). Then, EXACTLY,

    E = X - 4n + 2 = (G + X1 + W3) / 2.                                        (I)

Proof: sum_t (m_t - 1) = 4n^2 - 4(n-1)^2 = 8n - 4 (every tile lies in D). Tiles overlap iff their edges cross, in
1 or 2 quarters, so 2X = sum_t binom(m_t, 2) + X1. For m >= 1, binom(m,2) = (m-1) + binom(m-1,2); for m = 0,
binom(m,2) = (m-1) + 1. Sum: 2X = 8n - 4 + G + W3 + X1. The 4n term is absorbed exactly: a perfect field costs 0.
Numeric check (2026-10-03): `python3 gap/searcher/check_identity.py gap/lowerbounds/conn/FIELD_n166_92_155.json`
gives X = 1240, E = 578, G = 611, X1 = 466, W3 = 79: exact.
With the boundary set B (Section 4 of the proof; |B| - 4n = R >= -O(1)): E >= X_int + R - O(1), X_int = pairs not
in B. So for every lambda in [0,1], with an additive, local, nonnegative density

    c_lambda = lambda * (1 per crossing pair not in B)  +  (1 - lambda)/2 * (1 per unit of G, X1, W3),
    E >= sum c_lambda + lambda * R - O(1).                                       (II)

Each unit of cost sits at one place, so any rule that hands it to at most one charged path is a "weight <= 1" rule.
Check: lambda = 1/2 gives at least 1/4 per bad quarter, 2 bad quarters per charged path: exactly today's 1/2.

## 2. Statement of piece 1

**P1(p) (CONJECTURE for p = 2/3).** For the nested corner paths gamma_R (R0 <= R <= R1) of one corner, if every
gamma_R is charged, then the c_lambda cost in the corner region (minus the side strips, which keep their own
credits) is at least p (R1 - R0) - C, for one fixed lambda. With (II), 2n charged paths give E >= p * 2n - O(1)
and X >= (4 + 2p) n - O(1); p = 2/3 gives 16n/3. (How lost paths and the side terms merge is Turns Theory's skeleton.)

Reformulation that the certificate uses: by (3) of the proof, omega is a gradient mod 3. So there is a potential
psi (dual vertices -> Z/3) with omega = d psi, and psi is constant on every perfect region (all m = 1 there gives
omega = 0 by (2)). gamma_R is charged iff psi differs at its two ends. So the defect set must contain a "wall"
that crosses every gamma_R. P1 is a lower bound on wall cost per nested level crossed.

## 3. Evidence

- CERTIFIED (gap/searcher/RATES.md, corr2.cpp): between fold fields, any configuration in a band of width
  W = 3..6 along (1,1) costs 2/3 per (1,1) step for current +-1, +-2; an axis fold costs 3/4 per row; a steep edge
  carrier costs +1 per row. Per nested level: diagonal 2/3, axis and edge >= 3/4. Nothing below 2/3 is known.
- Between two perfect fields on a period quotient, area balance gives c_lambda = X for every lambda, so these rates
  are already in the currency of (II). The 1/2 of today's proof needs every crossing's 2 doubles and its 2 matched
  gaps to serve two different paths; no known wall does that.

## 4. Finite computations

**Step A - wall tension table (CERTIFIED numbers; first, cheap, about 1 day).** Generalize corr2.cpp:
a periodic band along direction v = (a,b), W cells per row, ANY degree-2 configuration inside, no finite cycle;
outside, one of the 4 perfect line fields on each side (16 pairs, not only the fold pair); constraint: psi jump
across the band != 0 mod 3, computed from the transversal flux (2) at one row (the jump is the same at every row).
Cost = crossings with a band end (equal to c_lambda here). Output tau_W(v) = min cost per nested level crossed
(a straight wall of direction v crosses |v|_inf levels per period). Directions: (1,0), (1,1), (2,1), (1,2), (3,1),
(1,3), (3,2), (1,-1). State space: corr2 reached W = 6 on (1,1) with 26.6 M states (under 4 GB); other directions
are similar. Value: min_v tau_W(v) is an upper limit for p from straight walls; a value below 2/3 is either a
counterexample to P1 or a better carrier for the UPPER bound. Both outcomes are useful.

**Step B - proof-grade certificate (after A).** Two candidates; choose by the numbers from A.
- B1 (transfer matrix over levels). Sweep up a vertical band of W consecutive levels x = R + 1/2 below the
  diagonal (vertical arms of gamma_R), from the bottom side to the diagonal. State = band cut with 2 soft margin
  columns on each side + one mod-3 flux accumulator per level (3^W) + the open quarter multiplicities. Cost =
  c_lambda counted only in x >= y. Certificate: sum c_lambda >= p * #(charged arms) - C_W by exact Bellman-Ford,
  as in jr.cpp. Feasible for W <= 4 (base cut about 10^6-10^7 states, times 81). Horizontal arms by symmetry; a
  charged path has at least one charged arm.
- B2 (discharging lemma by window enumeration, with KT Lower Bounds' SAT tools). Rule: each cost unit goes to
  the charged steps (omega != 0) of distinct levels within distance d. Prove by UNSAT of a (2d+1)-window model
  that each charged arm gets >= p. No additive error term.

## 5. Main risks

1. Error terms (B1): one constant C_W per band, and n/(2W) bands per arm, so the loss is about C_W/W per path.
   It kills the gain unless C_W is small or W is large. B2 has no such term, but needs a correct rule.
2. Soft margins (B1, B2): doubles inside a window can be balanced by gaps outside it. This is why the cost must
   be c_lambda, not X. The best lambda can give p < 2/3 even if straight walls cost 2/3 (Step A cannot see this).
3. Non-field neighbours: Step A assumes perfect fields on both sides of the wall. Piece 2 (structure lemma)
   must justify this, or B1/B2 must avoid it (they do: their margins are arbitrary).
4. Region near the sides and the corner: the wall can run along a side (edge carrier). Its crossings lie in B
   and are paid by R in (II) (Turns Theory U1), not by c_lambda; the merge needs care at the corner.
5. Curved walls: P1 needs all wall shapes. B1 and B2 handle any shape; Step A only straight periodic walls.

## 6. Proposed order

A (1 day, one heavy job, <= 8 GB) -> report tau table -> B1 at W = 3, 4 with lambda scan, to measure C_W and p_W
-> decide B1 vs B2 with the CR and KT Lower Bounds. The engines exist: corr2.cpp (bands), jr.cpp (augmented strip
certificates with exact Bellman-Ford and Dinkelbach).
