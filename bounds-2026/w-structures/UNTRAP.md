# Why the fold family stops at 19n/3: untrapping costs about n (KT Structures, 2026-10-02)

This explains the arch term (+n) of the fold design 4n (edges) + n (arch fix) + 4n/3 (flux) = 19n/3.
It is NOT a lower bound for all tours. It covers only the layout family below.

## Layout family covered
- Board regions, each filled with one straight line family: A (dir (2,-1)), A' (2,1), B (1,-2), B' (1,2).
- All four edges steep (left/right A or A', bottom/top B or B'), with the cheap U-turn pattern P (1 crossing per row).
- Region boundaries: free folds (0 crossings: A|A' horizontal, B|B' vertical, A'|B' slope +1, A|B slope -1, LB F3),
  or the measured non-free seams (gentle A|B on slope +1 and A'|B' on slope -1, 1.0 per unit x; A|A' vertical and
  B|B' horizontal, 1.0 per unit).
- Repairs: edge pattern changes (flips), interior jog bands (odd-width fold pairs), and seam templates.
- Searched layout sets: k x k grids of squares cut by both diagonals, k = 2, 4, 6, 8 (free folds), k = 2 (with seams).

A nest is a bundle of lines between two edge stretches. It is trapped when its lines close into short cycles
(Theta(n) cycles per nest). Untrapping a line needs an ODD index shift between its two ends (LB F10b).

## Steps (status in brackets)
1. [PROOF] A chevron (same-edge nest through one free fold) is always trapped: the fold fixes the edge line, so the
   shift is 0 (LB F10d).
2. [FINITE CHECK] With free folds only, the 8-triangle fold field is the only layout with all edges steep on the
   k x k grids, k = 2, 4, 6, 8. Its 4 midpoint chevrons hold n/4 lines per edge, n in total.
   [CONJECTURE] The field is unique for all free-fold layouts with all edges steep.
3. [ARGUMENT] Edge-only repair costs >= 1 per trapped row. P and its mirror P' are the only 1/row patterns (LB F5,
   proof). The edge phase changes only at defects. Rows with odd phase use a non-P pattern, and the best one costs
   2/row (+1) (FINITE CHECK: OPTIMAL for depth D = 3..5, period 4..8, and LB F12 W = 4). Each chevron line needs
   exactly one odd-phase end, so a midpoint needs >= n/4 odd rows. Total >= n. The arch flips reach n.
4. [PROOF] Interior repair: in a corridor through a uniform (2,1) region, current - base current = line shift
   (mod 2) (S8 lemma). An untrapping corridor (odd shift) carries an odd current, never 0. Its ends hold opposite
   charges, at best +-3, and these must reach other charges.
   [ARGUMENT] Flux-3 moves for free only along slope +1 inside one region. The band ends lie on the edge and on
   the midline (flux-3 rates there 2/row and 7/4/row, LB F12, exact for W <= 4). A band pair catches an odd number
   of lines only on a set of measure 1.5 x (end distance), so straight bands cost >= 1.25h per midpoint, more than
   the flips (h/2).
5. Seam repair: a gentle seam maps A-line c to B-line c' with c + c' = 0 (mod 3) [FINITE CHECK, S1]. So the
   shift s(c) = c (mod 3), and trapping is decided per residue class.
   [PROOF, for seams that keep lanes of 3] the shifts of the 3 classes are D, D+1, D-1, which mixes parities, so 1/3
   or 2/3 of the nest stays trapped [FINITE CHECK on the board: 6 templates x 5 seam positions, n = 96].
   [FINITE CHECK] A seam with one parity for all lines costs 3.0 per unit x, OPTIMAL at (p, w) = (6,3), (6,4),
   (6,5), (12,3), against 1.0 for the trapped seam. Two seams in series give one parity (D + D'), at >= 2n of seam.
6. [FINITE CHECK] k = 2 with seams: min of edges + seams + arch = 5.0n (31 layouts tie). With the seam result of
   step 5, none of them beats the fold field once flux is added (layout G: 4 + 1 + trapped seam nests, or
   4 + 3 + 2/3 with an untrapping seam).

Conclusion: in this family every untrapping mechanism costs >= about n. So 4n + n + 4n/3 = 19n/3 is the
end point unless the flux term drops (Edge Searcher: axis-parallel carriers) or a layout outside this family exists.
Escape routes and their status: spiral (4-fold) same-edge nests do not exist (LB F14a, measured);
7-fold nests untested; non-grid junctions (fans) are not excluded by step 2.

## Checker commands (from w-structures/, python = ../.venv/bin/python)
- Step 2: `python layout2.py 2 20`, `python layout2.py 4 8`, `python layout2.py 6 6`, `python layout2.py 8 4` (each prints 1 layout).
- Step 4: `python jog_flux.py 2 2 3 -3`, `python jog_flux.py 2 3 -3` (shift -3: rel current +-3 at 0, +-1 at 12, 0 INFEASIBLE).
- Step 5: `python seam_shift2.py 6 3` (lane-of-3 classes), `python seam_par.py 6 3 0` and `... 6 3 1` (one parity: 18 per period = 3.0/unit x);
  board check: see the snippet in FINDINGS S10 (layoutG_paste.place_seam + kt.board.fixed_paths, n = 96).
- Step 6: `python layout3.py 2 5.0 20`.
Details and data: FINDINGS.md S7-S11.
