# Flux route "edge + outer V arm" - assembly spec (KT Structures, 2026-10-02)

Purpose: replace the 4 diagonal flux corridors (4 x (n/2) x 2/3 = 4n/3) by a route that crosses each corner nest
at the board edge (cheapest per line crossed) and then rides along a field line to the centre.
Use it only if KT Edge Searcher finds an along-line corridor with cost c_step < 1/3 per (2,1) step.

## Geometry (BL frame; other quadrants by paste.Rot(p, n, r), r = 0..3, exactly as in fold_board.field)
- Field: any fold field with t = 1 corners, e.g. w-integrator/fold_jog.build_jog(n) (jog bands) or fold3.build
  with arch flips. Nothing in the field changes; the route only frees cells.
- Edge segment (nest escape): cells x < We (We = 4), 0 <= y < h/2 + We. It starts in the corner window and
  ends at the left-edge point (0, h/2), where the outermost nest line starts.
- Arm corridor: the field line from (0, h/2) along (2,1). Traced on E (route_arm.trace_arm): in practice
  n/4 - 1 moves of (2,1) and one (-1,-2) move at the diagonal fold, ending about 5 cells from the centre
  (n=96: 22 x (2,1) + 1 fold move, end (43,44); n=144: 34 + 1, end (67,68)). Free cells: Chebyshev distance
  <= Wa (Wa = 2; use the Edge Searcher's corridor width) around the traced path.
- Centre: the 4 arms end in the centre window (already free), where the 4 imbalances (-1,+1,-1,+1) cancel.
- Diagonal corridors: NOT freed (no flux on the diagonals in this design).

## Entry point
    sys.path.insert(0, 'w-structures'); from route_arm import arm_route
    cells, paths = arm_route(n, E, We=4, Wa=2)   # E from the field builder; cells = free route cells (4 frames)
    free = cluster_windows | cells               # same cluster windows (link 4, rad 4) as fold_assemble.setup
paths[r] is the traced arm in BL-frame coordinates (list of cells) for period ties.

## Periodic middles (for fold_period.py style exact slopes)
- Edge segment middle: tie free-free edges of cells x < We, lo <= y < h/2 - lo to their translate by (0, p_e)
  (p_e = period of the edge carrier; 4 for the measured 2.0/row pattern, which is the cheap pattern with a slip).
- Arm middle: tie the corridor cells around paths[r][lo:-lo] to their translate by k*(2,1) (k = period of the
  along-line carrier in (2,1) steps). Transplant n -> n + 4k*... : the arm gains n/4 steps per +n, the edge
  segment gains n/4 rows per +n, so use step sizes that are multiples of 4*p_e and 4*k.

## Cost (extra crossings above the 4n edges, per board)
- Edge segments: 4 x (n/4 rows) x 1 = n  (edge carrier, flux +-1: +1 per row, EXACT for W=4, LB F12).
- Arms: 4 x (n/4 steps) x c_step = c_step * n  (c_step = along-line cost per (2,1) step).
- Total flux term = (1 + c_step) n + O(1), versus 4n/3 for the diagonal corridors.
- Break-even: c_step = 1/3 per (2,1) step = 0.149 per unit length. If the Edge Searcher's best value is b:
  route flux term = (1 + b) n; with the jog-band field (4n + O(log n)) the total is (5 + b) n + O(log n);
  b = 0 gives 5n, b = 1/3 gives 16n/3 (no gain), b > 1/3: keep the diagonal corridors.
