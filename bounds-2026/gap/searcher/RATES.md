# Certified carrier rates (KT Edge Searcher, 2026-10-03)

Model: KT Lower Bounds F12 corridor model, re-implemented in corr2.cpp (straight band of W cells per row, any
moves inside, outside cells keep the base field, band-outside edges only base edges, no finite cycle).
CERTIFIED = exact minimum over ALL periods for that W (Howard + exact Bellman-Ford certificate); every witness
passes verify_corr.py (independent unrolled check). "rel. current" = colour current minus the plain field's.
Rates are extra crossings above the plain configuration (plain = 0 in the interior, 1 per row at a steep edge).

| carrier (kind) | geometry | band direction | W | rel. current | rate | status |
|---|---|---|---|---|---|---|
| diag | free fold (2,1)/(1,2) on x=y | (1,1) | 3,4,5,6 | +-1, +-2 | 2/3 per (1,1) step | CERTIFIED |
| diag | same | (1,1) | 3..6 | 0 mod 3 | 0 | CERTIFIED |
| mid | free fold (1,2)/(1,-2) on x=0 (axis fold) | (0,1) | 3,4,5 | +-1 | 3/4 per row | CERTIFIED |
| mid | same | (0,1) | 3,4 | +-2 / +-3 / +-4 | 1 / 7/4 / 2 per row | CERTIFIED |
| edge | left wall, field (2,1), base U-turns P | (0,1) | 2,3,4,5 | +-1 | +1 per row | CERTIFIED |
| edge | same | (0,1) | 4,5 | +-2 / +-3 | +3/2 / +2 per row | CERTIFIED |
| edgeB | left wall, field (1,2) (shallow edge) | (0,1) | 4,5 | two classes | 11/6 per row total (two current classes at this cost) | CERTIFIED |
| edgeB | same | (0,1) | 3 | best class | 13/5 per row total | CERTIFIED |
Not certified (short periods only, CP-SAT, w-searcher/FINDINGS.md): vert12 3/4, vert21 4/3 (W=5 band), anti21 1.0
per Manhattan unit, phi(2,-1) 3.0 per step. Network use: section 1 of FINDINGS.md.
