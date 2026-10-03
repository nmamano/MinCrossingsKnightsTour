# Claim 12 (preparation): FOLD24 tours and the all-size proof requirements — 2026-10-02

**Verdict: finite evidence PASS. The all-size theorem is pending its proof.** All 36 FOLD24 files are single closed knight tours and have the stored crossing and turn counts. For every even residue modulo 24, both checked extensions add exactly 152 crossings and 304 turns. The largest exact crossing offset is 142. These checks establish the numerical claim for every even n from 96 through 166; they do not establish induction for arbitrary k.

## Independent checks

`claim12_prep.py` imports only my existing independent checker. It decodes the board.js moves, checks every move is on the board, checks two distinct reciprocal knight edges at every cell, and follows the cycle from one cell. The cycle must return to that cell after exactly n² distinct visits. It then counts turns and all proper intersections of open edge segments with exact integer predicates. Spatial bins only select candidate pairs; each candidate receives the exact intersection test.

All stored n, crossing counts, and turn counts agree. The four FOLD24 certificate copies at n=96,98,100,102 also pass and have exactly the same grids as their main tour files. File hashes and individual results are in `claim12_prep_results.json`; the run log is `claim12_prep.log`. No construction code or solver was imported or run.

The three entries in each count column below are for n0, n0+24, n0+48. The offset b is X-19n/3, calculated as an exact fraction.

| Base n0 | n mod 24 | Crossings | Turns | b |
|---:|---:|---|---|---:|
| 96 | 0 | 720, 872, 1024 | 1251, 1555, 1859 | 112 |
| 98 | 2 | 752, 904, 1056 | 1265, 1569, 1873 | 394/3 |
| 100 | 4 | 775, 927, 1079 | 1319, 1623, 1927 | 425/3 |
| 102 | 6 | 754, 906, 1058 | 1310, 1614, 1918 | 108 |
| 104 | 8 | 776, 928, 1080 | 1352, 1656, 1960 | 352/3 |
| 106 | 10 | 786, 938, 1090 | 1383, 1687, 1991 | 344/3 |
| 108 | 12 | 788, 940, 1092 | 1386, 1690, 1994 | 104 |
| 110 | 14 | 803, 955, 1107 | 1402, 1706, 2010 | 319/3 |
| 112 | 16 | 839, 991, 1143 | 1459, 1763, 2067 | 389/3 |
| 114 | 18 | 864, 1016, 1168 | 1500, 1804, 2108 | 142 |
| 116 | 20 | 850, 1002, 1154 | 1507, 1811, 2115 | 346/3 |
| 118 | 22 | 875, 1027, 1179 | 1529, 1833, 2137 | 383/3 |

Thus every tested tour satisfies X <= 19n/3+142. The maximum offset occurs at residue 18. The repeated turn increment is additional finite evidence; I make no all-size turn claim here.

I also checked the saved base data independently in `claim12_base_data.py`. All twelve bases use p=6, lo=8, band=1, rad=4. Each stores 72 corridor template entries: four corridors, six longitudinal phases, and three transverse offsets. Every stored template move agrees with the corresponding base-tour move at every middle cell, not just in the extracted sample period. Every copied-component move also agrees with its base tour, and the saved component cells are disjoint from each other and from the middle cells.

All twelve bases have the same multiset of normalized component shapes: four components of size 60, four of size 63, four of size 78, and one of size 204. This is 13 components and 1008 cells. There are nine distinct shapes, with multiplicities 1,1,1,1,1,2,2,2,2. Thus shape equality alone does not identify every component. The number of middle cells in these bases is 6n-264, so the total represented free-cell set has size 6n+744. These are checked properties of the saved bases; uniformity at larger sizes still needs proof. Results are in `claim12_base_data.json`.

## What the construction does

I read `w-integrator/fold_period.py`, `fold_assemble.py`, `w-lowerbounds/fold_board.py`, and `w-structures/fold3.py`, plus the `paste.py` and `repair.py` routines that define the field and free regions. I also read the FOLD findings and `w-integrator/runs/fold24.txt`.

The field splits the square into four quadrants and splits each quadrant along a diagonal. In the local bottom-left frame, with offset t=1, a cell chooses direction (2,1) above y=x+1 and direction (-1,-2) otherwise. The other quadrants rotate this rule. The undirected union of the on-board chosen edges is the initial field; it is not yet assumed to be degree two or connected.

`fold3.build` adds boundary U-turns at degree-one cells. The arch interval h-floor(n/4) <= y < h, where h=n/2, reverses the usual U-turn direction. The insertion has degree guards and a fixed scan order, so its exact output, including exceptions near interval ends, matters to a proof.

For FOLD24 the call uses an empty `tgs` dictionary. Thus the separate diagonal templates loaded by `paste_field` are not inserted. The solver's free set consists of radius-four boxes around linked degree-defect clusters, together with four diagonal corridors. Defect clustering uses Chebyshev distance at most four. In a corridor's local frame its cells satisfy 0 <= x < h and y-x in {0,1,2}.

The saved periodic middle is 11 <= x < h-11 in those same three diagonal rows. The code inserts a six-period table there. On increasing n by 24, each middle gains twelve longitudinal cells, or two periods. The remainder of the free set is split into components using eight-neighbour cell adjacency. These are geometric components of the free-cell set, not components of the knight graph.

Each such component stores moves relative to its minimum-coordinate offset. On a larger board the code matches equal shapes greedily, choosing the unused base component with the closest normalized offset, and copies its moves by translation. Fixed-cell moves come from the rebuilt field. This procedure produces no new solver completion for the larger sizes. The final validation detects a failure at a particular tested n; it does not prove that no failure can occur later.

## Facts the all-size proof must establish

1. **Exact domain and size changes.** Fix the twelve base data files and all parameters. For n=n0+24k, give formulas for the field regions, U-turn intervals, defect clusters, corridor cells, and copied-component offsets. The size change moves h by 12 and floor(n/4) by 6. A coordinate-shift table must cover all these motions, including the rotations and the centre. It must apply from n0 onward, not only after some larger threshold.

2. **The fixed field and all free components are accounted for.** Prove that all degree defects are within the stated free set, that the relevant defect clusters remain separated, and that free-set components retain their shapes for every k. Prove the number and size of copied regions stay bounded. The 13-component, 1008-cell inventory above is the finite base evidence. A component must not grow with n or split, merge, disappear, or acquire a new interface. The reported raw-field crossing count 5n also needs an exact all-size count if it is used in the slope proof.

3. **Component identities and phases are preserved.** Four pairs of saved components have the same shape. Prove that the normalized-distance rule assigns each to the intended base component for all k, including ties and iteration order, or replace that rule in the mathematical construction with explicit geometric labels and offsets. Equal shape does not by itself prove equal surrounding field phase or equal port connections. A ranking observed at k=0,1,2 is not a proof that the normalized-distance ranking never changes.

4. **Every local edge is consistent.** Prove on-board knight moves, degree two, and reciprocity at every cell after all replacements. This includes corridor-to-field, corridor-to-endpoint, copied-region-to-field, and any edges between distinct free components. Eight-neighbour separation of cell components does not by itself exclude knight edges between them. The solver ties constrain free-free corridor edges; the proof must also cover all other incident edges of the saved periodic moves. Any overlap of region definitions needs a consistent assignment.

5. **The complete graph is one cycle for every k.** Give an exact path or port description for the field, each periodic corridor, and each copied piece. Include paths that return to the same cut and rule out closed components wholly inside a piece. Prove that insertion of two six-period blocks per corridor preserves the relevant exterior connections, or give an equivalent inductive graph isomorphism. All vertices of the new board must occur in the described paths. Matching visible endpoints alone does not rule out extra internal cycles. A local period of six does not, by itself, imply that the global matching has period 24 in n.

6. **Crossing changes are local and exhaustively counted.** Show that the inserted material and the coordinate shifts preserve all old crossing pairs except the explicitly counted local changes. Count the new proper intersections, including those across every seam and those involving field edges outside a corridor. Specify a unique counting rule so a pair is neither lost nor counted twice. The claimed decomposition is 120 extra field crossings plus 32 from four corridors, for a total of 152 per +24. This needs a proof of the *net* corridor change after old edges are replaced; simply adding corridor crossings to the original field count is not enough. Bounded copied regions give a constant contribution only after their local surroundings and separation from other regions are proved stable.

7. **Close the induction and the uniform bound.** Use one valid base in each even residue class and the proven extension to cover every even n>=96. The finite offsets in the table then give X(n)=19n/3+b[n mod 24] and max b=142. State that the base search is used only to provide the fixed finite certificates; the extension must not require a new successful optimization, a larger repair window, or a changed gadget at some later n.

These are proof requirements, not counterexamples to the design. The finite data are consistent with the claimed theorem. The preparation verdict remains finite PASS until the extension and connectivity argument is supplied in `w-integrator/PROOF_fold.md`.
