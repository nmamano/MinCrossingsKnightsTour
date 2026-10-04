# Claim 57: T ≥ 8n - 24

Audit date: 2026-10-04. Reviewer: KT Verifier (Astra).

## Verdict: PASS

**Every knight 2-factor on an n by n board, for every n ≥ 20, has at least 8n - 24 turns.** This includes every closed knight's tour. The claimed corner values and the potential argument pass independent exact checks.

The audit supplies a smaller proof of strip validity, so it does not depend on the reported 38.8-million-state enumeration or the unfinished BFS recheck. It also supplies exact corner lower-bound certificates checked with standard-library Python, independent of CP-SAT optimality.

A simplification: **the arm-10 certificate at scale 6 is sufficient for every n ≥ 20**, not just n<28. Its four-corner sum is -74/3; the integer ring cost is therefore at least -24. The arm-14 and arm-20 results are also independently verified but are not needed for this rounded global bound.

## Sources and audit artifacts

The starting claim is `gap/lowerbounds/turns_ring/L1.md`, section 1b. The audit inspected `stripz.cpp`, `corner_pot.py`, `certcheck.py`, `verify_frames.py`, both integer potential files, the slot list, and the residual definition in `TURNS_PROOFS.md` / `writeup/turns/main.tex`.

Relevant worker sources and potential data are snapshotted under `gap/verifier/claim57_run/source_*`; their original paths and SHA-256 hashes are recorded in `source_manifest.json`. The audit's exact checkers use the snapshotted slot and weight files, not mutable worker data.

New audit code:

- `claim57_local.py`: exact local side-potential inequalities.
- `claim57_frames.py`: independent slot enumeration, row divergence, mirror map, ring partition and coefficient cancellation.
- `claim57_corner_exact.py`: exact corner lower bounds, using integer/rational local certificates and a complete finite consistency search.
- `claim57_witness_check.py`: independent exact checks of primal corner witnesses.

`claim57_corner_lp.py` and `claim57_witness.py` only generate candidate certificates and witnesses. Their numerical optimizers are not trusted for the proof. The four checkers above need neither SciPy nor OR-Tools. No remote access was used; work stayed within two cores.

## 1. Restriction to the width-6 ring

For each cell v, let t(v) be its turn indicator and let L(v) be the sum of the four side contributions from the paper. For one side, with inward distance i and two neighbor distances, the contribution is:

```text
L0 = 1
L1 = L2 = number of neighbors at distance 0 or 3, minus 1
L3 = 1 minus number of neighbors at distance 1 or 2
Li = 0 for i >= 4
```

For a 2-factor, the sum from one side is exactly 2n. To see this, the depth-1/2 to depth-3 incidence terms cancel their reverse depth-3 terms by reciprocity. The remaining edge count is the number of incidences into depth 0, exactly 2n. Summing four sides gives `sum L = 8n`. Thus, with `r=t-L`,

```text
T - 8n = sum over all cells of r.
```

A cell at depth at least 6 has all four side contributions zero. Its residual is t≥0. Restricting a 2-factor to the depth<6 ring therefore gives

```text
T - 8n >= sum of its ring residuals >= R6(n).
```

The restriction chooses exactly two legal moves per ring cell and keeps reciprocal choices for edges between ring cells. A move into the deeper interior is left free at its other endpoint. This removes constraints and enlarges the feasible set; it cannot raise the relaxation minimum. Such a move still contributes to the turn and L-values of its ring endpoint. It is not deleted from that endpoint's local choice. No connectivity assumption is used.

## 2. Strip validity without enumerating billions of arcs

Use strip coordinates `(x,y)`, with depth x in `{0,...,5}` and increasing row y. The 28 slots are exactly the knight edges crossing a row cut with both endpoints in this strip. Independent enumeration agrees with the supplied slot list.

For a crossing edge oriented from its lower endpoint to its upper endpoint, give it weight +1 if both endpoint depths are in `{3,4,5}` and the upper endpoint is shallower, weight -1 if it is deeper, and zero otherwise. This exactly matches both supplied weight vectors. Write H(c) for the sum of those integer weights on the selected edges crossing cut c.

For a cell at depth x whose chosen horizontal displacements are a and b, define

```text
D_x(a,b) = sum of sign(d) over d in {a,b}
           for which both x and x+d lie in {3,4,5}.
```

Then for one row,

```text
H(incoming cut) - H(outgoing cut) = sum over that row of D_x.
```

Reason: a selected edge ending in the row leaves the cut sum; an edge starting in the row enters it with a minus sign. Both give `sign(d)` at the row's endpoint. An edge spanning two rows and passing through the current row without an endpoint appears in both cuts with the same weight and cancels. The independent coefficient check verifies this identity edge by edge, including those carried edges.

For each depth x, enumerate every pair of distinct knight moves with nonnegative neighbor depth. This is only **133 pairs across the six depths**. Let `r_x=t-L_x`. Exact enumeration gives the following minimum of `S*r_x + D_x`:

| Depth x | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| S=3 | 0 | 0 | 0 | 1 | 0 | -1 |
| S=6 | 0 | 0 | 0 | 1 | 0 | -1 |

The minima sum to zero. Therefore every row satisfies

```text
S * row_cost + H(incoming) - H(outgoing) >= 0
```

for both S=3 and S=6. This proof even allows the six local choices to be inconsistent with one another outside the row; imposing the strip's consistency conditions only restricts them. It therefore proves the inequality for every valid strip transition, including its minimum-cost realization, without requiring any reachable-state enumeration.

Evidence: `side_local.json`, `side_local.log`, and the row-divergence check in `frames.json`.

The two certificates use the same integer H but **different normalized potentials**, H/3 and H/6. The scale-6 potential is not numerically the same function as H/3.

## 3. Corner bounds by exact certificates

For arm length A, the corner cells are

```text
C_A = {(x,y): 0 <= x,y < A and min(x,y) < 6}.
```

Each cell chooses two distinct knight moves that stay in the nonnegative quadrant. Choices must be reciprocal whenever both endpoints are in C_A; moves leaving C_A are otherwise free. This is the required corner relaxation. Let s and t be its vertical and horizontal cut states in their local strip frames. The scaled objective is

```text
F_A = S * sum_C_A r - H(s) + H(sigma(t)).
```

The independent checker computes the boundary coefficients directly from the supplied slots and weights, rather than trusting the corner solver's objective construction.

### Exact lower-bound method

For every cell p and every legal pair of moves, the audit checks an inequality

```text
local scaled cost >= alpha_p + sum of signed beta_e on its chosen internal edges.
```

The coefficients are in the saved `corner_A*_S*_dual.json` files. All coefficients in these certificates are integers. There are 1,693 local inequalities for A=10; 2,757 for A=14; and 4,353 for A=20. The checker evaluates every one using exact `Fraction` arithmetic. On summation, the internal edge terms cancel by reciprocity.

The sums of alpha give the preliminary lower bounds -38 at `(A,S)=(10,6)` and -19 at `(14,3)` and `(20,3)`.

For each certificate, an objective equal to that preliminary bound would require **every** selected local inequality to be tight, since all slacks are nonnegative. The checker retains only the zero-slack move pairs, groups pairs with the same chosen internal edges, and tests whether reciprocal choices can exist. It uses complete branching over a cell's remaining choices, with propagation of forced edge membership. Each branch is covered; there is no heuristic cutoff or numerical test.

All three equality cases are impossible:

| A | S | Preliminary scaled bound | Complete search nodes | Contradiction leaves | Proved scaled bound |
|---:|---:|---:|---:|---:|---:|
| 10 | 6 | -38 | 15 | 8 | -37 |
| 14 | 3 | -19 | 33 | 17 | -18 |
| 20 | 3 | -19 | 33 | 17 | -18 |

The final step uses integrality of F_A. Thus the normalized corner lower bounds are exactly the claimed `-37/6`, `-6`, and `-6`.

### Witnesses attaining the bounds

Separate primal witnesses were generated and checked in exact arithmetic: correct region, two distinct legal moves per cell, nonnegative endpoints, reciprocal internal edges, and a direct recomputation of both boundary states and objective. They attain scaled costs -37, -18 and -18, respectively. Thus these are the exact corner minima, not just certified lower bounds.

The optimizer's reported optimal status is not used in this conclusion. Lower bounds come from the exact local certificates plus the exhaustive equality-case rejection; upper bounds come from the independently checked witnesses.

Evidence: `exact10.log`, `exact14.log`, `exact20.log`, `corner_A*_exact.json`, `corner_A*_witness.json`, and `witness_checks.json`.

## 4. Frames, mirror, joins, and telescoping

For a slot `(x0,y0,x1,y1)`, the row mirror is

```text
sigma(x0,y0,x1,y1) = (x1,-1-y1,x0,-1-y0).
```

The slot set is closed under sigma; sigma is an involution; and its weight is negated. The `-1` is necessary because the cut is between consecutive integer rows.

Use rotations `rho(x,y)=(y,n-1-x)` and label corners by powers of rho. In the frame of side k, the horizontal-cut edge of corner k+1 has endpoints

```text
(x0, n-1-A-y0), (x1, n-1-A-y1).
```

At the far side cut c=n-A, those are precisely the endpoints of the mirrored slot, in reverse order. Thus the far side state is `sigma(t_next)` for every n, not merely for sampled ring solutions. This identity is algebraic and does not depend on a particular assignment of moves.

For n≥2A, the four rotated corner regions C_A and four side rectangles

```text
0 <= x < 6,  A <= y < n-A
```

partition the ring exactly. Corners have residual `t-L_x-L_y`; side cells have residual `t-L_x`, since all other side distances are at least A≥10. At n=2A the side rectangles are empty, and the same cut identities still hold.

Summing the row inequality on a side gives

```text
side cost >= [H(sigma(t_next)) - H(s_source)] / S.
```

After adding the four corner costs, the boundary terms group into the four reduced corner objectives. Equivalently, all remaining side/corner potential coefficients cancel edge by edge. Therefore

```text
R6(n) >= 4 * minimum normalized corner objective, for n >= 2A.
```

The independent frame checker verifies the slot enumeration, involution, row-divergence identity, and coefficient cancellation. It also checks exact ring partition and all joins for 42 `(A,n)` cases, including n=2A and larger separations. These finite tests check the implementation; the coordinate identity and partition argument above establish the statement for all n≥2A.

Evidence: `claim57_frames.py` and `frames.json`. No CP-SAT ring solution is required for these checks.

## 5. Board-size range and integer rounding

The original split is valid:

- For n≥28, A=14 and S=3 give `R6(n) >= 4*(-6) = -24`.
- For 20≤n<28, A=10 and S=6 give `R6(n) >= 4*(-37/6) = -74/3`; since ring costs are integers, `R6(n) >= -24`.

In fact, A=10 is admissible for **all** n≥20, and the S=6 row inequality is valid on every side length. Thus the second argument alone proves the rounded bound over the entire claimed range. Odd n require no separate parity assumption in the proof; the assertion applies to any 2-factor if one exists.

Combining this with the ring restriction gives

```text
T - 8n >= R6(n) >= -24,
```

as claimed. The audit does not claim this bound below n=20, or that -24 is globally tight for rings or tours.

## Exact reproduction

From the project root, these commands use only standard-library Python and saved finite certificates:

```sh
python3 gap/verifier/claim57_local.py
python3 gap/verifier/claim57_frames.py
python3 gap/verifier/claim57_corner_exact.py 10 6
python3 gap/verifier/claim57_corner_exact.py 14 3
python3 gap/verifier/claim57_corner_exact.py 20 3
python3 gap/verifier/claim57_witness_check.py
```

The reduced proof needs no desktop resources, no 5.4-billion-arc enumeration, no CP-SAT lower bound, and no floating-point assertion. Numerical optimization was used only to find candidate finite certificates and primal witnesses, which the commands above verify exactly.

No audit blocker remains. The next useful step is to incorporate this short side proof and the exact corner certificates into the lower-bound package, so future readers can verify 8n - 24 without the large strip-state computation. Updating the public theorem statements remains the Chief Researcher's integration task.
