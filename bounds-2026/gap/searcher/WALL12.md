# The (1,2) wall (KT Edge Searcher, 2026-10-03, 10:00 box time)

Status: witness CERTIFIED in the band model (wall.cpp, relaxed: no path labels; WM = 4 cells per row, 1 margin
square column per side, exterior free). Plane extension PASS (Verifier Claim 35). NOT a closed tour.

## 1. The wall

A defect band of direction (1,2) between two perfect regions with psi jump != 0 mod 3. Cost: 1/2 crossing per row
(= per L-infinity level crossed). Period vector (2,4); one period (board coordinates; modeled cells
0 <= x - floor((1+y)/2) < 4):

    (-1,0)-(1,1)  (1,0)-(3,1)  (1,0)-(2,2)  (2,0)-(3,2)  (3,0)-(5,1)  (3,0)-(4,2)
    (0,1)-(2,2)   (2,1)-(4,2)  (2,1)-(3,3)  (4,1)-(6,2)  (4,1)-(5,3)
    (1,2)-(3,3)   (1,2)-(2,4)  (3,2)-(5,3)
    (0,3)-(2,4)   (2,3)-(4,4)  (2,3)-(3,5)  (4,3)-(6,4)  (4,3)-(5,5)

Per period: 2 crossings, 4 doubly covered and 4 uncovered quarters, no cycle, modeled degrees 2.
The fields on both sides: split '/', ZIGZAG word (ribbon bits alternate V, H; strands step (2,1) and (-1,-2) in
turn, so they run in direction (1,-1) and cross the band). Both sides have the same split and the same bit on every
ribbon: the wall absorbs 0 ribbon ends (FINDINGS 7.3).

## 2. Which exterior fields allow a cheap (1,2) wall (NEW, CERTIFIED in the same model, W = 4, lambda = 1)

The margin squares are restricted to one field type per side (env FIELDL / FIELDR in wall.cpp: allowed moves of the
tiles that cover the margin squares). Crossings per row, minimum over all periodic configurations:

| left field | right field | crossings per row |
| --- | --- | --- |
| '/' any word (a and b moves) | '/' any word | **1/2** (the witness: zigzag VH both sides) |
| '/' straight, any of H (2,1)-lines, V (1,2)-lines | '/' straight, any | none below 4 (no wall at W = 4) |
| '\' any word (c and d moves) | '\' any word | 1 |
| '\' H (2,-1)-lines | '\' H | none below 4 |
| '\' V (1,-2)-lines | '\' V | 3/2 |
| '\' H | '\' V (either order) | 1 |
| '/' H | '\' V (either order) | 1 |
| '/' H | '\' H; '/' V | '\' H or V (either order) | none below 4 |

Reading: the 1/2 rate needs mixed-word '/' fields (the optimum is zigzag) on both sides; straight '/' fields give no wall. Next to straight knight-line fields (the fold layout's
fields) the cheapest (1,2) wall at W = 4 costs 1 per level, more than the certified diagonal carrier (2/3). This
agrees with the Integrator's finding (ext2.py: straight exteriors do not extend the witness).
Caveat: W = 4 only (W = 5 does not fit in 8 GB: the relaxed warm-up layer alone exceeds 90 M states); a wider band
can only lower these numbers.

## 3. What a 6n layout would need (ARGUMENT, unchecked)

Zigzag fields on both sides of every (1,2) wall. Zigzag '/' fields next to a board side: KT Structures C2
(gap/structures/FINDINGS.md G10) found the word HV INFEASIBLE next to a side in their periodic model (integer colour
charge injection), so the layout also needs a cheap transition zigzag -> straight field (or a side that takes zigzag
fields). Price of that transition per unit length is open; it decides whether 6n is reachable.

## 4. Commands (gap/searcher/wall/)

    g++ -O2 -march=native -std=c++17 -DNOLABK -o wallc wall.cpp
    NOLAB=1 LAMS=1/1 ./run_wd.sh LOG 7 ./wallc 1/2 4 1 nz 8 1 90000000           # 1/2 per row, 50 s, 0.7 GB
    ./fields_s12.sh > fields_s12.out                                          # section 2 table, 18 runs, 15 min
    python3 verify_witness.py; ../../../.venv/bin/python extend_witness.py 2 8   # witness checks
    python3 ribbon_ends.py nl_s12_W4.log                                       # fields, ribbon ends, current

A printed value "8/1" in fields_s12.out is the start ratio: no cycle below 8 weight units (4 crossings) per row.
