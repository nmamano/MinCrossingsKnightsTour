# Inputs for the tile framework (KT Lower Bounds, 2026-10-02)

Companion to w-turnstheory/FINDINGS.md sections 6-7 (tile identity, charged paths, and the
unconditional tour bound X >= (4 + 1/338) n - 1240). This file improves one input: the strip
stability constant. Result: **X >= (4 + 1/17) n - O(1) for closed tours** (n even, large).

## 1. ERRATUM for PROOF_crossings.md (frozen draft)

PROOF_crossings.md claims the bound for every 2-factor. That scope is WRONG as written: the strip
transfer graph forbids cycles inside the strip (columns 0..3), which is valid for a Hamiltonian
cycle but not for a general 2-factor (small cycles can live in the strip). The argument as written
proves the bound for closed tours (and for 2-factors with no cycle inside any 4-column boundary
strip). KT Turns Theory pointed this out in its section 7. The rest of the draft is unaffected.

## 2. Sharp linear stability: alpha = 1/5 (PROVEN, exact)

In the width-2 strip graph (strip_dp.py; 82,516 states, 144,674 arcs), call an arc a *cycle arc*
if it lies on one of the two tight cycles (P, P'; 8 arcs). Then for every walk from the start state

    sum over steps of (w - 1/4)  >=  (1/5) * N_nc  -  149/20,                  (S)

where N_nc is the number of non-cycle arcs used. Proof: with integer weights 20w - 5 - 4[non-cycle],
Bellman-Ford from a virtual source converges (no negative cycle); the potential lies in [-149, 0].
The constant 1/5 is sharp: with 201/1000 instead of 1/5 a negative cycle exists, and the Verifier
found an explicit witness (w-verifier/claim11_runner/check_sharp_witness.py: a reachable 12-step closed
walk with weight 5 and 10 non-critical steps, ratio exactly 1/5). Verified as Claim 11 (PASS).
Checks: alpha_star.py (binary search), alpha_cert.py (exact 1/5 and 201/1000, numpy integer
Bellman-Ford); KT Edge Searcher's C++ code confirms the potential [-149,0] and the 201/1000 negative
cycle. (My pure-Python alpha_check was stopped at the 30-minute limit before printing; not used.)

Consequence per side sigma: X_sigma >= n + N_nc(sigma)/5 - 7.45, and the number of bad rows
(rows containing a non-cycle arc) satisfies d_sigma <= N_nc(sigma) <= 5 (X_sigma - n + 7.45).
This replaces the run-counting bound d_sigma <= 112 E_sigma + 111 (factor 112 -> 5).

## 3. Plugging into Turns Theory section 7.4

With (7.3) there: sum X_sigma <= X + 1104, so with E = X - 4n + 2,

    d <= 5 (X + 1104 - 4n + 4 * 7.45) <= 5E + 5659 <= 5E + 5679.

Section 7.4 gives 2n <= 4E + 6d + 152 (from L >= 2n - 60 - 4d, |B| >= 4n - 48 - d and
L <= 4X - 8n + 4 - 2|B|). Hence

    2n <= 34 E + 34226,   E >= n/17 - 1007,   X >= (4 + 1/17) n - 1009.

## 4. Where the remaining slack is

- The loss 6d per bad row: each bad row removes one boundary crossing (|B| term, factor 2 in the
  tile budget) and up to 4 charged paths (factor 1/4 ... appears as 4d). A sharper corner lemma
  needing fewer than 4 good endpoint rows, or a stability count per row (not per non-cycle arc)
  would help.
- The charged-path count L ~ 2n gives at most 4 + 1/2 even with no defects; reaching that needs
  d = o(E).

## 5. Per-row stability beta = 1/2 (PROVEN, exact) => X >= (4 + 1/8) n - 856 for closed tours

Bad row = a row whose 4 transitions are not all tight-cycle arcs (the definition of Turns Theory
7.1). Augment the strip graph with a flag "this row already used a non-cycle arc" (states (s,f)),
and charge beta when a row ends with the flag set. Then for every walk

    sum (w - 1/4) >= (1/2) * (#bad rows) - 46/8.                            (S')

Proof: integer weights 2(4w - 1) - 4[row ends with flag] = 8(w - 1/4 - [..]/2) have no negative
cycle (Bellman-Ford from a virtual source converges; potential in [-46, 0]). beta = 1/2 is sharp
up to the search resolution (beta* in [0.49966, 0.50059], beta_star.py with an iteration cap; the
certified value 1/2 is from beta_cert.py with no cap). Independent check: strip2_independent.py
row_check(1,2) (separate pure-Python code; result in row_check.log).
Per side: X_sigma >= n + d_sigma/2 - 6. With sum X_sigma <= X + 1104 and E = X - 4n + 2:
    d <= 2 (X + 1104 - 4n + 24) <= 2E + 2252.
Turns Theory 7.4: 2n <= 4E + 6d + 152 <= 16 E + 13664, so E >= n/8 - 854 and

    X >= (4 + 1/8) n - 856      (closed tours, n even, n >= 32 as in Turns Theory 7).

Remaining loss: the 6d term (4 charged paths and 1 boundary crossing per bad row) against
beta = 1/2. With no bad rows the framework gives 4 + 1/2.

## 6. Run-aware stability kappa = 2/15 (PROVEN, exact, sharp) => X >= (4 + 4/23) n - 750 for tours

In Turns Theory 7.4 a run of k consecutive bad rows on one side costs at most k + 3 charged paths
(radius R is lost iff a bad row lies in [R-1, R+2]; the two corners of a side use disjoint row
ranges) and k boundary crossings of B (which enter the tile budget with factor 2). So the total
loss in "2n <= 4E + loss + 152" is  Loss = sum over runs (3k + 3)  (instead of 6d).
Exact stability for this loss: for every walk of the width-2 strip graph

    sum (w - 1/4) >= (2/15) * sum_runs (3k + 3) - 351/60.                  (S'')

Proof: states (s, flag of the current row, previous row bad); integer weights 15(4w - 1) - 8 loss
have no negative cycle (Bellman-Ford converges; potential in [-351, 0], unit 1/60).
Sharp: 67/500 instead of 2/15 gives a negative cycle. Checks: kappa_star.py (search),
kappa_cert.py (exact 2/15 and 67/500), strip2_independent.py run_check(2,15) (separate pure-Python
code: converged after 12 passes, same range -351..0).
Per side: Loss_sigma <= 7.5 (X_sigma - n + 5.85). Summing with sum X_sigma <= X + 1104:
    Loss <= 7.5 (E + 1125.4),   2n <= 4E + Loss + 152 <= 11.5 E + 8593,
    E >= (4/23) n - 748,   X >= (4 + 4/23) n - 750      (closed tours, n even, n >= 32).
4/23 = 0.1739. (Section 5's per-row bound gives 1/8 = 0.125; Turns Theory 7 gives 1/338.)

## 7. No boundary-crossing loss + run stability 2/7 => X >= (4 + 4/15) n - 540 for closed tours

Two changes to the chain of Turns Theory 7.4.

(a) Take B = all crossing pairs among edges incident to the outermost line of a side (column 0 for
the left side), for all four sides. The paper's strip bound (my exact certificate F1: L_1 = 1, the
walk weight is >= rows - 1) gives n - 1 such pairs per side, unconditionally, also in bad rows.
A pair can belong to two sides only if both its edges meet column 0 and row 0 (at most one pair per
corner), so |B| >= 4n - 8. Their tile overlaps avoid the charged paths: the tile of an edge at
column 0 lies in x <= 2 and never contains the right quarter of a square [1,2] x [j,j+1], so the
overlap of two such tiles avoids every quarter triangle next to a dual step at x >= 3/2
(check_col0_overlaps.py, exact, all 115 crossing pairs in a period: 0 violations; bottom edge by
transposition). Turns Theory 6.5 then gives L <= 4X - 8n + 4 - 2|B| <= 4E + 12 with E = X - 4n + 2:
a bad row no longer costs a boundary crossing.

(b) A run of k consecutive bad rows (or columns) removes at most k + 3 radii (Turns Theory 7.4;
a run that crosses the middle of a side can touch both corners: +3, a constant per side). Exact
stability for this loss (sharp):

    sum (w - 1/4) >= (2/7) * sum_runs (k + 3) - 167/28      for every strip walk.   (S''')

Proof as in section 6 (states (s, row flag, previous row bad); integer weights 7(4w-1) - 8 loss;
Bellman-Ford converges, potential in [-167, 0]); 1431/5000 gives a negative cycle. Checks:
kappa2_star.py (search), kappa2_cert.py (exact), strip2_independent.py run_check(2,7,1,3)
(separate pure-Python code: converged after 12 passes, same range).

Chain: Loss = sum over sides and runs (k + 3) <= 3.5 (sum X_sigma - 4n + 24) + 12
<= 3.5 (X + 1104 - 4n + 24) + 12 <= 3.5 E + 3962, and
    2n - 60 - Loss <= L <= 4E + 12   =>   2n <= 7.5 E + 4034   =>   E >= (4/15) n - 538,
    X >= (4 + 4/15) n - 540      (closed tours, n even, n >= 32).
4/15 = 0.267. With no bad rows at all the same chain gives 4 + 1/2.

## 8. State for a fresh session (2026-10-02, written at handoff)

Role now: answer KT Verifier review questions on Claims 10 (PROOF_crossings.md, PASS, repaired by
the Verifier for all 2-factors via claim10_allow_cycles.py), 11 (4 + 1/17, PASS), 13 (4 + 1/8,
section 5), 14 (4 + 4/23, section 6); section 7 (4 + 4/15) is newer and not yet routed as a claim.
No new research unless the Chief Researcher asks.

Results ladder (closed tours, n even, n >= 32): 4 + 1/338 (Turns Theory 7) -> 1/17 (sec 2-3) ->
1/8 (sec 5) -> 4/23 (sec 6) -> 4/15 (sec 7). Method limit with 4-row corner windows ~ 4 + 1/3.

Reproduce (from w-lowerbounds/, ../.venv/bin/python unless noted):
- strip graph + tight cycles + T*: strip_constants.py; independent: python3 strip2_independent.py
- alpha = 1/5 (per non-cycle arc): alpha_cert.py (exact), alpha_star.py (search)
- beta = 1/2 (per bad row): beta_cert.py; independent: python3 -c "import strip2_independent as S; S.row_check(1,2)"
- kappa = 2/15 (loss 3k+3 per run): kappa_cert.py; independent: S.run_check(2,15)
- kappa' = 2/7 (loss k+3 per run): kappa2_cert.py; independent: S.run_check(2,7,1,3)
- column-0 tile overlaps avoid the charged paths: python3 check_col0_overlaps.py
- older finite lemmas (Claim 10): sat_cert.py m3|nem3 + python3 check_drup.py certs/X.cnf certs/X.drup;
  corner_charge.py, corner_charge2.py; Edge Searcher's C++ certificates in w-searcher/cert/.
Logs: row_check.log, run_check.log, run_check2.log, kappa*_star.log, beta_star.log, certs_nem3.log.

Open ideas (tell the Chief Researcher before starting):
- Corner lemma with fewer endpoint rows: Q depends only on column-0 cells of rows R-1..R+2 and
  column-1 cells of rows R-1..R+1 (not on the ghost columns 2,3). Defining "good" by these cells only
  (augmented strip DP that flags only column-0/1 deviations) may give a larger kappa.
- Rectangular loops [1,b] x [1,a] (independent left/bottom endpoints) do not help in the worst case.
- Past 4 + 1/3 the tile budget term 4E must improve (Turns Theory works on past-4.5 ideas).

### 8.1 Turns Theory 9.5 finite lemma: SAT (2026-10-02)

Model exactly as Turns Theory FINDINGS 9.5 (V = [-R,R]^2, edges with an endpoint in V, degree 2 on V,
<= 2 outside, cycles allowed, no tile pair sharing exactly one quarter, every quarter multiplicity <= 2,
exactly two quarters of [0,1]^2 with multiplicity != 1; tile table = w-turnstheory/check_knight_tiles.py).
Result: **SAT for R = 4 and R = 5** (no solver search needed: CaDiCaL finds it with <= 1 conflict).
So the lemma is false: a two-bad-quarter square occurs deep in a degree-two region with J = Q = 0 locally.

Minimal local pattern (R = 5; RC2 MaxSAT minimum of bad quarters over squares with lower-left in
[-4,3]^2 = 12; solver optimum, no certificate). All other inner squares are 1111. Squares (x,y): m0..m3
(q0 bottom, q1 right, q2 top, q3 left):

    (-1,1) 0011   (0,1) 2200
    (-1,0) 2200   (0,0) 1122   <- central square, exactly two bad quarters (both double)

Cause: a chain of four alternating edges, (-1,-1)-(0,1), (-1,0)-(1,1), (0,0)-(1,2), (0,1)-(2,2)
(directions (1,2) and (2,1), consecutive pairs translated by (1,1)). Consecutive edges cross with
area 1/2: three half-area crossings, 6 double quarters, compensated by 6 gap quarters in the same
2x2 block. It is a short finite piece of a (1,1)-periodic seam like the one in Turns Theory 9.3
(mirror directions). In the infinite seam each seam square has 4 bad quarters; the middle square of
this short piece has its two doubles and no gaps.
Files: sq2_lemma.py (model + SAT), sq2_min.py (minimum-defect witness), sq2_check_witness.py
(standalone witness check, no solver: PASS for sq2_R4.witness.txt, central 0011, and
sq2_min_R5W4.edges, central 1122). Witness picture: sq2_min_R5W4.txt.
Reproduce: ../.venv/bin/python sq2_lemma.py 5; ../.venv/bin/python sq2_min.py 5 4 edges;
python3 sq2_check_witness.py sq2_min_R5W4.edges 5.

## 9. Weaker endpoint test (Turns Theory 10.4 / QUESTIONS.md): beta = 1, EXACT and SHARP (2026-10-02)

Task: width-two strip graph (crossings). At scan row R, F = sum of the coefficients of the selected
edges in the list of Turns Theory 10.2 (coordinates relative to R, no chi factor). Row passes iff
F == 2 (mod 3) and the exceptional pair (0,0)--(2,1), (0,1)--(2,0) is not both selected; b = 1 for a
failed row, charged when the row ends. Opposite orientation: list and pair reflected y -> -y.

Result, for each orientation separately and for the joint test (b = 1 if EITHER test fails):

    sum over a strip walk of (w - 1/4)  >=  1 * b  -  29/4.                        (S9)

- Certificate: integer weights (4w - 1) - 4b (beta = 1/1) have no negative cycle. Bellman-Ford from a
  virtual source CONVERGES (no cap involved); potential range [-29, 0] in units of 1/4, for up, down
  and joint. Code: endpoint_stab.py (augmented nodes (state, F mod 3, number of exceptional edges);
  pending edges added at column 0, edges introduced at each cell added once, test at the row end).
- Independent check: endpoint_independent.py (built on strip2_independent.py, no import of strip_dp.py;
  augmented state = (state, set of listed edges seen in the row), test evaluated from the set):
  converged at beta = 1, same range [-29, 0], all three variants. Log: endpoint_independent.log.
- Sharpness (critical cycle, exact): Dinkelbach iteration with explicit negative cycles from parent
  pointers (endpoint_stab.py crit ORIENT 8; log endpoint_crit.log) ends at beta* = 1 exactly. The
  critical cycle is the period-1 pattern, per row y:
      (1,y)--(0,y+2),  (2,y)--(0,y+1),  (2,y)--(1,y+2)
  i.e. column 0 uses (1,-2) and (2,-1); column 1 uses (-1,2) and (1,-2); ghost column 2 has degree 2.
  It has 2 crossings per row (base rate 1), and every row fails the test (F == 1 mod 3), in both
  orientations. So no beta > 1 is possible in this strip model. Unrolled check (degrees, crossings,
  F per row): endpoint_cycle_show.py ORIENT; log endpoint_cycle_both.log.
- Sanity: the tight P/P' cycles have weight 0, so they must pass the test (else beta* = 0); they do,
  which agrees with Turns Theory 10.2 (F = -1 for P and P').

Consequence (my derivation, TO BE CONFIRMED by Turns Theory / Verifier): with beta = 1 the formula of
Turns Theory 10.4 gives X >= [4 + 2beta/(2beta+1)] n - O(1) = (4 + 2/3) n - O(1). Constant, following
10.3 with d -> b and the joint test (so no split of the walk is needed): per side X_sigma - n >= b_sigma
- 29/4, so b <= sum X_sigma - 4n + 29 <= X + 1104 - 4n + 29 = E + 1131. Then 4n <= 4E + 2b + 164 <=
6E + 2426, E >= 2n/3 - 404.4, and X >= 14n/3 - 407 (closed tours, n even, n >= 32).

Reproduce (from w-lowerbounds/):
    ../.venv/bin/python endpoint_stab.py crit both 8      # also: up, down
    python3 endpoint_independent.py both 1 1              # also: up, down
    ../.venv/bin/python endpoint_cycle_show.py both
