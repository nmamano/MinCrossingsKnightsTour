# T_min(n) - 8n on whole boards (KT Structures, TURNS data track, started 2026-10-04)

Solver: `tmin.py` (CP-SAT 9.15, 2 workers, presolve OFF: with presolve this version reports a wrong best_bound, below a
constraint of the model). One bool per (cell, pair of on-board moves), edge consistency, objective T. Valid cuts: each 4x4
corner square has residual sum >= -7 (certificate of w-turnstheory/check_corner_certificate.py), T >= 8n - 28.
Tours: AddCircuit (`tour`) or lazy subtour cuts (`tourlazy`). Residual map: `resid.py <file>`.
"D=0" = EXACT (whole board free). "D=4" = RESTRICTED: every cell at depth >= 4 from all sides is straight; a D=4 value
is an upper bound for T_min only (a feasible solution), its OPTIMAL status is optimality inside the restriction.
A tour is a 2-factor, so the exact 2-factor minimum is a lower bound for tours.
Odd n: no 2-factor exists (the knight graph is bipartite with colour classes of different size), so no data.

## Table (T - 8n; logs in logs/queue*.log)

| n | 2-factor | status | tour | status | how |
|---|---|---|---|---|---|
| 8 | -20 | OPTIMAL, exact | -19 | OPTIMAL, exact | 0.4 s / 0.8 s |
| 10 | -18 | OPTIMAL, exact | -18 | OPTIMAL (tour = 2f bound) | 23 s / 120 s |
| 12 | -20 | OPTIMAL, exact | -16 | FEASIBLE, bound -20 | 33 s / 120 s |
| 14 | -20 | OPTIMAL, exact | -20 | OPTIMAL (D=4 tour = exact 2f bound) | 176 s / 397 s |
| 16 | -20 | OPTIMAL, exact | -20 | OPTIMAL (D=4 tour = exact 2f bound) | 312 s / 108 s |
| 18 | <= -21 | D=4 OPTIMAL | <= -21 | D=4 OPTIMAL | 27 s / 427 s |
| 20 | <= -21 | D=4 OPTIMAL | <= -19 | D=4 FEASIBLE (AddCircuit) | 19 s / 600 s |
| 24 | <= -21 | D=4 OPTIMAL | <= -17 | D=4 FEASIBLE (AddCircuit) | 44 s / 600 s |
| 28 | <= -21 | D=4 OPTIMAL | <= -16 | D=4 FEASIBLE (AddCircuit) | 80 s / 600 s |
| 32 | <= -22 | D=4 OPTIMAL | <= -17 | D=4 FEASIBLE (AddCircuit) | 127 s / 600 s |

All runs 2026-10-04. Every tour file passes kt.core.validate.

## Structure (CHECK)
In every optimal solution examined, residual r(v) is 0 outside the four corner squares except for at most one cell
(r = 1), so T - 8n is the sum of the four corner residuals. Corner sums seen: -4 to -6, never -7.
n=16 tour: -4, -6, -6, -4. n=18 tour: -4, -6, -6, -5. n=32 2-factor: -6, -5, -5, -6.
The interior of the D=4 tours is a mixed field of two parallel line directions (move pairs 15 and 37), period 5.
