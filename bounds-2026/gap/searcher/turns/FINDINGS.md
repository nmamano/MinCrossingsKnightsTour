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

## 2026-10-04: NEW TOURS below 8n - 14: T = 8n - 16 (n = 6 mod 8) and T = 8n - 17 (n = 2 mod 8)
Family: pring.py, Z = 8 corners, free periodic bands (bottom/top period 8, left/right period 4, depth 4),
interior lines x + 2y = c fixed; cut loop (2f + subtour cuts), num_workers = 1. Each result is OPTIMAL
in its family (the final iteration is a single cycle at the proven bound).
| n | T - 8n | family bound | file |
| 56 | -14 | -14 (TT16 is in the family) | (none; TT16) |
| 58 | -17 | -17 | grid_n58_Z8.json |
| 60 | -14 | -14 | - |
| 62 | -16 | -16 | grid_n62_Z8.json |
| 64 | -14 | -14 | - |
| 66 | -17 | -17 | grid_n66_Z8.json |
| 68 | -14 | -14 | - |
Extension (extend.py): copy the tour, repeat one 8-wide period of every band and of the line field at the
centre lines; each grid checked by kt.core.validate + assemble.walk_check, turns by kt.core.num_turns.
- n62 base: valid for all n = 62, 70, ..., 206 (19 sizes), T = 8n - 16. Period 8 in n.
- n66 base: valid for all n = 66, 74, ..., 210 (19 sizes), T = 8n - 17. Period 8 in n.
- n58 base: valid only for n = 58 + 16j (58..202, 10 sizes); n = 66 + 16j give 2+ cycles. Use n66 base there.
Certificates: tours/res6/n{62,70,78}.json, tours/res2/n{58,66,74}.json. Logs: ext_n{58,62,66}.txt.
n = 6 mod 8 bottom gadget (period 2): rows top-first '26 26' / '26 36' / '26 25' / '67 16';
left period 4: '23 27' / '23 24' / '23 27' / '02 27'.
For n = 0, 4 mod 8 this family gives exactly -14 (n = 56, 60, 64, 68); also -14 with Z = 10, Z = 12,
P16/Q8, depth 6 (n = 56). 2-factor floor is -18 for all of them: connectivity costs 4.

## 2026-10-04: small sizes n = 50, 54 (same family, cut loop, OPTIMAL in family)
n = 50: T - 8n = -17 (tours/res2/n50.json); n = 54: T - 8n = -16 (tours/res6/n54.json). Both checked by
kt.core.validate + walk_check.
Coverage (every even n >= 48, T - 8n):
- n = 2 mod 8: -17 for every n >= 50 (bases n = 50, 58 single; n66 base extends to n = 66 + 8k, checked to 402).
- n = 6 mod 8: -16 for every n >= 54 (base n = 54 single; n62 base extends to n = 62 + 8k, checked to 398).
- n = 0, 4 mod 8: -14 (TT16), unchanged.
For larger n than checked, the extension inserts whole 8-periods into every band and the line field, so each
extended grid is a 2-factor with the same T; connectivity is the only open point there (same status as TT16).

## 2026-10-04: n = 0, 4 mod 8 stays at -14 in every periodic variant tried
Cut loop, family optimum -14 (bound reached, TT16 in family): n = 56 with P12/Q4, P12/Q6, P8/Q6;
n = 60 with P12/Q6 (plus the earlier Z = 10, 12, P16/Q8, depth 6). n = 62 with Z = 10: -16 OPTIMAL (no gain).
Mid-side defect windows (n = 56, 8 long x 6 deep, non-periodic, on all four sides; ties broken there):
cut loop 900 s gave family bound -15; final AddCircuit solve with all 180 cuts, hinted by TT16, 1500 s:
best -14, bound -17. So -15 is open for that family.

## 2026-10-04: one mid-side defect window (n = 56, 8 long x 6 deep, ties broken there)
Defect only on L, B or T: family optimum -14 (proven by the cut loop). Only on R: best tour -14, bound -15
(cut loop 900 s + hinted AddCircuit 900 s). Running: feasibility of objective <= -15 (cut loop with that
upper bound) for the R window and for L + R windows.
Reading of the 2f optima (n = 56..62): most extra cycles are pairs of middle lines (right edge -> left edge)
closed by the left and right gadgets at both ends. Middle lines meet the left side in its upper half and the
right side in its lower half; the lower-left half meets bottom->left lines, the upper-right half meets
right->top lines. So a mid-height window on a side separates two line regions.

## 2026-10-04: res 2 and res 6 values are stable under larger families
n = 62: P16/Q8 and P8/Q8 (Z = 8), Z = 10 (P8/Q4): family optimum -16. n = 58: P16/Q8, Z = 10: -17.
P12/Q6 (period not dividing 8 on the T16 base) gives only -14 (2f floor -14) at n = 58 and n = 62.
Feasibility runs "objective <= -15" for the n = 56 R and L+R defect families: CP-SAT UNKNOWN after 300 s
at iteration 6. Added an LP-based backend (csolve.solve_mip, SCIP via pywraplp; pring.py --mip SCIP).

## 2026-10-04: SCIP cut loop settles the defect families: -14 for n = 0, 4 mod 8
SCIP (pywraplp, 1 thread) closes the cut-loop iterations that CP-SAT does not. Family optimum -14 (each
final iteration has objective = bound = -14, TT16 in family):
n = 56 defect 8x6 on R only (312 s), on L + R (367 s); n = 60 defect 8x6 on all four sides (295 s);
n = 56 defect 12x8 on all four sides (573 s); n = 56 defect 8x6 on all four sides (rerun after a bound-rounding
fix in solve_mip: -14, iteration 6).
So mid-side switches of the side pattern do not help n = 0, 4 mod 8 in these families.

## 2026-10-04: general (non-periodic) depth-4 ring, n = 56: tour optimum exactly -14
pring.py --noties --Db 4 --Dl 4 --Z 8 --mip SCIP: every side band (depth 4, whole length) and the four 8x8
corners free, no periodicity; only the line field beyond depth 4 (outside the corners) is fixed.
2f floor -18 (OPTIMAL, 3 s). Cut loop bounds -18 ... -15, -15, -14 (iteration 10, OPTIMAL, 3012 s, 244 cuts).
TT16 is in this family, so: no closed tour of n = 56 that keeps the line field x + 2y = c on every cell at
depth >= 4 from the sides (outside the 8x8 corners) has fewer than 8n - 14 turns.
Running: same with depth 6.
