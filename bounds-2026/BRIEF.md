# Knight's tour turns/crossings research — shared brief (Chief Researcher, 2026-10-02)

Goal (from Nil): improve either bound on the minimum number of CROSSINGS (and, secondarily, TURNS) of a
closed knight's tour on an n x n board. Published: crossings 12n+O(1) upper (paper), 11.5n (Shisheng Li's
4x40 block, 2026-05), lower 4n-O(1). Turns: 9.25n upper, (6-eps)n lower (paper conjectures >= 8n).
Nil's idea: inside a heel (or group of heels) let the 4 formation knights end in ANY permutation; fix the
global cycle at the corners with O(1) extra work. Branching out to other ideas is welcome.

Sources in this dir: paper.pdf / paper.txt (arXiv 1904.02824v2), board-original.js, board-patched.js
(Shisheng's fork), RESTART.md (older notes). Python venv: .venv (ortools 9.15, python-sat, numpy, scipy, networkx).
Run with  .venv/bin/python .

## Geometry / conventions (all verified 2026-10-02)
- board.js grid: tour[i][j] = 'ab' two move codes, i = row DOWN, j = column. Move codes 0..7 =
  (di,dj): (-2,1) (-1,2) (1,2) (2,1) (2,-1) (1,-2) (-1,-2) (-2,-1).  Interior cells are '26'.
- Our board coords: x = column (right), y = row UP. Interior = parallel knight lines  x + 2y = c  (direction (2,-1)).
  Line ends: 1 per column on top/bottom edges, 2 per row on left/right edges. 3n lines total.
- Lanes = 4 consecutive lines (the 2x2 formation). The formation visits lanes in order; bottom & right
  edges pair lanes (2j,2j+1), left & top edges pair (2j+1,2j+2). Corners: O(1) gadgets incl. junctions.
- Crossing = open segments properly intersect (board.js numCrossings). Turn = cell whose 2 moves are not opposite.

## Code (kt/)
- kt/core.py: validate (single closed tour), num_crossings, num_turns on board.js grids.
- kt/gentour.py: exact port of Algorithm 1 (+ Shisheng block). VERIFIED slopes (n=120->200, 160->240):
  default heel 13.0n X / 9.5n T; paper heel 12.0n X; P40 both bands 11.5n X / 9.75n T. All tours valid.
- kt/strip.py: periodic edge-gadget model (kind 'bottom' period P cols x depth D rows; kind 'left'
  period Q rows x depth D cols; lane offset off). Strip.evaluate(chosen) gives (crossings, turns) per
  period. Reproduces: paper heel 28/22, default heel 32/22, P40 130/115, paper VerticalEdge 10/8.
- kt/search.py: CP-SAT model: degrees, no cycles (flow), lane-pair labels + orientation flow
  (each strand joins lane 2j to lane 2j+1 of the same pair = Nil's permutation relaxation).
- kt/verify_strip.py: independent unrolled check of a bottom gadget (paths, lane pairing, crossings).
- kt/board.py: DRAFT, UNTESTED full-board assembler: tiles a bottom gadget on bottom/top and a left
  gadget on left/right with lane alignment, then CP-SAT completes four ZxZ corner zones with lazy
  subtour cuts. Owned by the Integrator.

## Results so far (2026-10-02)
- Bottom, P=8, D=4: optimum 16 crossings per 8 columns (OPTIMAL, CP-SAT) = 2.0/column vs 3.5 (paper)
  and 3.25 (Shisheng). Unrolled check confirms pairing + 16/period. Two optimal heels seen:
    H16a (T=25): ['26 26 36 36 36 36 56 26','23 36 36 36 13 23 23 23','26 26 26 27 27 27 27 26','67 67 67 67 67 67 67 67']
    H16b (T=27): ['46 46 56 56 56 26 46 46','14 14 14 45 45 45 45 46','05 15 15 15 15 05 05 05','01 01 01 01 01 01 01 01']
  NOT YET CONFIRMED IN A FULL TOUR. If it holds with the paper's left edge (2.5/row): 2(2.5+2)=9n.
- Left, Q=4, D=2..4: optimum 10 per 4 rows (= paper's VerticalEdge), off=1 class worse (14).

## Rules for workers
- CPU: the box has 8 cores shared by everyone. Use at most the CP-SAT num_workers your brief gives
  you, never run more than one heavy job at once, check `uptime` before launching big runs.
- Work in your own subdirectory (w-<name>/); import kt/ but do not edit kt/ files you do not own
  (copy and extend instead). Write findings to w-<name>/FINDINGS.md with dates, proof status
  (OPTIMAL vs FEASIBLE + bound) and the exact template strings.
- A claim counts only after an independent check (unrolled check or full-tour validation).
- Report to the Chief Researcher (agent id agent-1790895858902-etft) via the isomux messages API when
  you finish a milestone or find something big. No need to steer; plain messages are fine.
- Do not contact Nil directly, do not commit/push, do not touch other projects.
- Use ASD-STE100 Simplified Technical English in written reports.

## Context rule (Nil, 2026-10-02)
Claude workers hand off at about 50% context: at the next natural break, write all state to your files, then POST your own
/handoff with a short forward-looking brief. Do not start a big new step above 50%.
