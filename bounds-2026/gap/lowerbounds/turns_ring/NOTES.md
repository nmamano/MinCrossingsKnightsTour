# L1 notes (KT Lower Bounds, 2026-10-04) - working state, not the report

Task: exact min of sum r over the boundary ring (TURNS, writeup/turns/main.tex), 2-factors first.

1. Free-interior side strip, width 4 (strip.py): 36,064 cut states, 856,330 arcs, every arc cost >= 0. Zero-cost subgraph:
   one recurrent class of 2,657 states with PERIOD 1 plus two fixed points (zero.py). So a free-interior ring has no
   phase constraint. The corner-attach run (corner.py) ran out of memory; CONJECTURE: free-interior ring min = -28.
2. Single straight interior family (depth >= 4 straight, field (2,-1)), fstrip.py (MEASURED):
   steep side (left/right) 1,483 states, zero classes: a 4-cycle (period 4) and a fixed point;
   grazing side (top/bottom) 12,920 states, one zero class of 6 states, period 2. Same sizes for field (2,1)/(1,2).
3. Corner segment with that field forced at ALL depth >= 4 cells (no interior turn), D=8 (cornerseg.py, partial):
   pairs (left 119, bottom 10626/11024) -> -2; (254, 5365/5385) infeasible; (119, 6932) infeasible. Python too slow
   (frontier up to 5M). Next: C++ frontier DP (regiondp.cpp) with Python instance generator.
4. Construction (main.tex): left/right templates period 4, bottom/top period 8, corners 6x6 depend on n mod 8, total -14.

## 2026-10-04 later
5. C++ frontier DP (regiondp.cpp + gen.py) and CP-SAT (gen.corner_window_sat, cwsat.py) corner tables, BL corner,
   single family far interior. K=4 (no interior turn): field (2,-1) best -3; field (2,1) best -6 (left 950).
   K=8 window (interior turns allowed near the corner): field (2,-1) still -3; field (2,1) -5/-6 so far.
   Each family is good (-6) for two opposite corners and bad (-3) for the other two.
6. assemble.py K=4 D=8 (side cuts at distance 8 in zero classes): ring min -18 (n = 0 mod 4), -16 (n = 2 mod 4),
   corners (-3,-6,-3,-6), sides 0 or (1,0,1,0).
7. board_sat.py (full board CP-SAT, depth>=4 forced straight, 2-factor): n=48 field (2,-1): OPTIMAL T-8n = -18,
   witness checked directly (board_n48_W4_K0.json, 14 cycles, not a tour).
   A/D residue mixtures (x+2y mod 4 in R -> (2,-1), else (2,1)): R=0: -17, 01: -16, 012: -17 (OPTIMAL);
   R=02: open (feasible -5, bound -21 after 600 s); rerun 1800 s -> mix02_n48.log.
   Turn-free fields: lines of one residue class mod 4 for the pair (2,-1)/(2,1) must be all one family
   (connected intersection graph), so turn-free fields = single families or residue mixtures (ARGUMENT).

## 2026-10-04 (cont.)
8. Free-interior ring W=4, n=48: CP-SAT OPTIMAL -28 (ring_free_sat.py). L1 as posed gives nothing.
9. mixstrip.py: zero-cost periodic side exists on all 4 sides for AD mod 4 R in {01,03,12,23}, all AC mod 3, AB mod 5
   for 9 of the first 15 subsets (n=48). Note: zero-cycle test is asymptotic; finite n can still do well without one.
10. board_sat.py fixed fields, n=48/50, OPTIMAL (presolve ON; Structures warns CP-SAT 9.15 presolve can report a wrong
   best_bound - rerun key claims with presolve off): AB:5:0 -> -21 (n=48 and 50); other AB subsets -17..-20.
   AB:5:0 with free 8x8 corner windows (interior turns allowed): still -21 at n=48.
   Structures (TMIN.md): D=4 (straight, free direction) n=32 -22; exact whole-board n=16 -20.
11. Remote desktop survey of all 100 two-family mixtures at n=48: ~/nil/knight-remote/lb_turns/survey48.log.
