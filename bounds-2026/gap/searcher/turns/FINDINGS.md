# Turns upper side: findings (KT Edge Searcher)

Notation: residual of a cell = t - (side charge), with the side charge `lower()` of
w-turnstheory/check_corner_certificate.py. For every 2-factor of the n x n board the side charges sum to 8n
(checked by assertion on every output), so T - 8n = sum of residuals. The T16 / '23 27' / '02 24' side
gadgets have residual 0, so T - 8n = sum of the four corner-region residuals.

## 2026-10-04: method - the residual objective makes corner solves fast and OPTIMAL
Tools: csolve.py (pair formulation, one option per cell; modes 2f = degree 2 only, tour = AddCircuit over
contracted fixed paths), sweep.py (per-corner sweep), combine.py, mixed.py (side transitions), band.py
(free side band / free ring).
With the plain turn count as objective, CP-SAT does not close a 10x10 corner in 300 s (LP bound 23 vs 37).
With the residual as objective (same optimum), the same corner is OPTIMAL in 0.7 s.

## 2026-10-04: TT16 corner residuals (n = 56, phases (0,1,0,0), left '23 27', right '02 24')
BL -4, BR -6, TL -3, TR -1 (sum -14). Same values at Z = 6, 8 (OPTIMAL 2-factor) and Z = 10 (BL, BR, TL
OPTIMAL; TR best -1, not closed). So with the TT16 sides, larger corner zones give nothing, even without
connectivity.

## 2026-10-04: per-corner 2-factor floors, T16 top/bottom, Z = 8 (sweep_Z8_n*.jsonl)
Left/right gadgets with 2 turns per row: A = '23 27', B = '02 24', C = lanes4o0 (period 4).
Odd bottom phases / even top phases have no 2-factor (bipartite b-matching flow check).
Best per corner (all n = 56..62): BL: A -4, B -1, C -3 | BR: A -3, B -6, C -6 | TL: A -3, B -6, C -6 |
TR: A -4, B -1, C -3. The bottom/top phase does not change the value; the C phase does.
Best one-gadget-per-side 2-factor floor: -18 (n = 0, 4 mod 8), -16 (n = 2, 6 mod 8), with C on both sides.
Region rules (strands, periodic.Combo.regions_ok): only (A, B) and (B, A) pass; every pair with C fails,
and (A, A), (B, B) fail. So C sides give no tour without more free cells.
Side transition A -> B (or B -> A) inside a free side window costs +6 (OPTIMAL for 6x8, 8x12, 6x20 windows).
Free left band (width 6, whole side) + free 8x8 corners, n = 56, 2f: T - 8n = -16 OPTIMAL, i.e. the left side
with its two corners gives -9 (same as C), against -7 for TT16's A.

## 2026-10-04: free periodic sides (pring.py) - 2-factor floor -18, tour bound -14 at n = 56
pring.py frees the four Z x Z corners and the four side bands (depth D), with periodicity ties (bottom/top
period P, left/right period Q); interior lines stay fixed. 2-factor floor, n = 56, Z = 8, all OPTIMAL:
P8/Q4/D4 -18 (3.6 s), P8/Q8/D4 -18, P8/Q4/D5 -18. Example best left period: '23 24 / 02 24 / 02 27 / 02 24'.
Ring with free NON-periodic bands (width 6) is too large for CP-SAT (bound -50 after 1800 s).
Tour mode with AddCircuit is weak here (best +4, bound -53 in 600 s).
Cut loop (2f + subtour cuts "a closed cycle on S needs 2 free edges leaving S", every bound is a valid
lower bound for all tours of the family): n = 56, Z = 8, P8/Q4/D4: bound -18, -17, -17, -16, -16, -15, -14
(OPTIMAL at iteration 6, 69 s). TT16 is in this family, so the family optimum is exactly -14.
Note: CP-SAT with num_workers = 2 does not close these 2f models (bound -52); num_workers = 1 closes them.
