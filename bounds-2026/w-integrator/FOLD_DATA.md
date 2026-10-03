# FOLD_DATA - data note for the 19n/3 fold tours (KT Integrator, 2026-10-02)

Coordinates: x = column (right), y = row (up), cells 0..n-1; h = n/2. Frames r = 0..3 = BL, BR, TR, TL
quadrant, rotated to BL by paste.Rot (p -> (n-1-p_y, p_x), applied r times).

## Fixed part (KT Structures field)
- Field: `fold3.build(n, ts=(1,1,1,1), flip=fl)` (w-structures/fold3.py over w-lowerbounds/fold_board.field),
  called as `paste_field(n, 1, {}, fl, hi=h-4)` (tgs = {}: no diagonal templates are pasted).
- Fold offset t = 1 in every quadrant: direction (2,1) where y > x + 1 (frame coordinates), else (-1,-2).
- U-turns at every edge end cell; arch flip `fl(r, y) = (h - n//4 <= y < h)`: in every edge frame r,
  the U-turn at frame cell (0, y) is flipped for those y (n/4 rows per edge, one side of each midpoint).
- Result (all even n >= 48): X_pre = 5n, 32 path components, 0 closed cycles, 52 defect cells in
  13 clusters (`repair.clusters(bad, link=4)`).

## Free cells (completed by CP-SAT)
- Windows: `repair.window_cells(n, cluster, rad=4)` around each of the 13 clusters (rad = 3 is
  degree-infeasible at the flip-end windows).
- Diagonal corridors: frame cells (x, y) with 0 <= x < h and |y - x - 1| <= 1, all 4 frames
  (corner -> centre). They carry the corner colour charges -1/+1/-1/+1 (BL, TL, TR, BR).
- Code: `w-integrator/fold_assemble.py setup(n, rad=4, tgs={}, link=4, band=1)`.

## Base solve (fold_period.py, n0 = 96..118)
- `kt.board.complete(feasibility=True, ties=...)`: fixed paths contracted to one dummy node each,
  AddCircuit over free cells + dummies (one Hamiltonian cycle), no objective.
- Ties: every free-free edge of a corridor with lo <= x < h - lo (lo = 8) equals its translate by
  (6, 6) in frame coordinates (period 6 along the diagonal).
- Then 4 rounds: re-solve the tied corridor middles (objective: crossings), then `kt.board.lns` on the
  other free cells (8x8 windows, step 4, hint = current tour).

## Transplant n0 -> n0 + 24k (no new solve)
- Pasted: the corridor template = moves of frame cells x in [lo+3, lo+3+6), |y-x-1| <= 1 of the base,
  indexed by ((x - lo) mod 6, y - x), applied to every corridor cell with lo+3 <= x < h - lo - 3.
- Copied by translation: every connected component of (free cells minus pasted cells) - the 13
  windows plus the corridor ends - with its moves relative to the component's bounding-box corner.
  Components are matched by identical shape and nearest relative position (offset / n).
- Everything else is the rebuilt field. Each tour is checked by kt.core.validate and an independent walk.

## Base files and results
- Base data: `w-integrator/corners/FOLD24_base_n{96,98,...,118}.json` (template + components).
- Log: `w-integrator/runs/fold24.txt`; tours `w-integrator/tours/FOLD24_n*.json`.
- All 36 tours n0 + 24k (k = 0, 1, 2, n <= 166) are valid; each +24 adds exactly 152 = (19/3)*24.
  X(n) - 19n/3 = 112, 131.3, 141.7, 108, 117.3, 114.7, 104, 106.3, 129.7, 142, 115.3, 127.7 for
  n0 = 96, 98, ..., 118.

## Step 24, not 12
- Step +12 is not safe. Separate runs with step 12 (runs/foldX_res.txt): 96 -> 108, 100 -> 112,
  104 -> 116 and 106 -> 118 gave tours that were not single cycles; 98 -> 110 and 102 -> 114 were valid;
  an older base (n0 = 96, runs/foldX96.txt) was valid at 108 and 132. So step 12 depends on the base
  solution (my earlier note "fails for n = 0 mod 4" was too narrow: 106 -> 118 also failed).
- KT Turns Theory found (QUESTIONS.md) that side-chevron blocks induce the 4-cycle [1,2,3,0], so +24
  changes the side matching by its square and +48 restores it; its proof checks both parity states.
