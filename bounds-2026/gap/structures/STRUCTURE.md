# Crossing-free parts of a knight tour are ribbon fields cut by straight axis walls

KT Structures, 2026-10-03. Status: PROOF (elementary), with two machine checks. Audited as Verifier Claim 30:
T1-T3 PASS, T4 PASS with the scope below; the first version's connected-domain claim was FALSE and is repaired here
(one H/V bit per uninterrupted good ribbon RUN, not per domain). Title read with "good" = exact quarter coverage.
Sources used: only the tile/quarter facts of w-turnstheory/PROOF_crossings_lower.md, Section 1 (audited).

## 0. Setting and the facts we use

Cells are the lattice points V = {0,...,n-1}^2, x = column (right), y = row (up). H is any set of knight edges
for T1-T3 (a tour, a 2-factor, or a part of one); T4 needs H to be a full spanning 2-factor (a closed tour is
enough). deg(v) is the degree of v in H. Move classes:
a = (2,1), b = (1,2) (class '/'); c = (1,-2), d = (2,-1) (class '\').

The TILE of an edge e is the parallelogram whose long diagonal is e and whose short diagonal is the unit grid edge
with the same midpoint (the "carried" unit edge of e). Each unit square of D = [0,n-1]^2 is divided by its two
diagonals into four open QUARTERS, named B, R, T, L after the side of the square that they touch.
m_t = number of tiles that contain quarter t. Audited facts (Section 1): every tile is the union of 4 quarters
(plus boundaries); two distinct tiles overlap in positive area exactly when their edges cross properly.

Definition. A unit square is GOOD if each of its four quarters has m_t = 1. A lattice point v with all four of its
unit squares inside D is GOOD if these four squares are good. A HALF of a square is the union of two quarters on
one side of a diagonal: the '/' halves BR and TL, and the '\' halves RT and LB.

**Lemma 0 (tile shape; direct computation).** Let e = (x,y)-(x+2,y+1) (an a-edge). Its tile has the vertices
(x,y), (x+1,y), (x+2,y+1), (x+1,y+1), and it meets exactly two squares: in [x,x+1]x[y,y+1] it is the half BR and in
[x+1,x+2]x[y,y+1] the half TL. For a b-edge (x,y)-(x+1,y+2) the tile meets [x,x+1]x[y,y+1] in TL and
[x,x+1]x[y+1,y+2] in BR. The c and d tiles are the mirror images (x -> -x): they meet two squares in '\' halves;
a d-tile across a vertical side covers RT of the left square and LB of the right square, a c-tile across a
horizontal side covers LB of the upper square and RT of the lower square.
So: (i) a tile meets exactly two squares, which share its carried unit edge; (ii) in each, it is one half, and the
half has the carried edge as one of its two sides ("legs"); (iii) the halves are '/' halves for a, b and '\' halves
for c, d. Also: tiles across a VERTICAL unit edge are a or d moves (|dx| = 2); across a HORIZONTAL one, b or c.

## 1. T1: a good square has a split

**T1.** In a good square S, the quarters are covered by exactly two tiles, both of one class; S is cut along the
diagonal of that class ("split '/'" or "split '\'"), and each tile covers one half.
Proof. By Lemma 0 each tile that meets S covers one half of S. The four quarters are covered exactly once, so S is
the disjoint union of halves of the covering tiles. Two halves of different diagonals share a quarter
(BR and RT share R, and so on), so the halves are BR + TL or RT + LB. []

Consequence. A tile joins two squares of the same split, so a unit edge between good squares of DIFFERENT splits
carries no tile. We call such a unit edge a WALL edge.

## 2. T2: each uninterrupted good ribbon run has one matching phase

Take split '/'. Write BR(i,j), TL(i,j) for the halves of the square with lower-left corner (i,j). By Lemma 0,
BR(i,j) can only be covered by an a-tile with partner TL(i+1,j) (carried edge = right side) or by a b-tile with
partner TL(i,j-1) (carried edge = bottom side). TL(i,j) can only pair with BR(i-1,j) (a) or BR(i,j+1) (b).
So the possible partners form a graph in which every half has degree 2; its components are the RIBBONS

    ... BR(i,j) - TL(i+1,j) - BR(i+1,j+1) - TL(i+2,j+1) - ...      (ribbon k = j - i),

staircases of half-squares along the slope +1 direction (ribbon k uses the BR halves on the diagonal j - i = k and
the TL halves on j - i = k - 1). Links of the form BR(i,j)-TL(i+1,j) are a-tiles ("H"); links TL(i+1,j)-BR(i+1,j+1)
are b-tiles ("V").

A half is GOOD if it lies in a good square of its split. A RUN is a maximal sequence of consecutive good halves on
one ribbon (consecutive in the chain above).

**T2.** (a) Along a run, the tiles are all a-tiles or all b-tiles (one bit per run).
(b) Conversely, for every word w: Z -> {H, V}, the edge set
    a-edges (x,y)-(x+2,y+1) where w(y-x) = H,   b-edges (x,y)-(x+1,y+2) where w(y-x+1) = V
has degree 2 at every point and no crossing (the RIBBON FIELD of w).
(c) In the full-plane ribbon field of one word, every edge changes y - x by exactly 1, and the two edges at v (on diagonal d = y - x) go to
diagonals d - 1 and d + 1. So every strand is monotone in y - x and meets each ribbon once; the strand step across
ribbon k is (2,1) if w(k) = H and (-1,-2) if w(k) = V (in the direction of decreasing y - x). All strands are
translates of each other by multiples of (1,1).
Proof. (a) In a run every half is covered exactly once by a '/' tile (T1), and that tile is a link of the chain. If
one link is used, its neighbouring links are not, and the next links are used: the choice propagates along the run.
It does not propagate through a half that is not good. (b) Degree at v = (x,y), d = y - x: a-edge out iff w(d) = H; a-edge in (from (x-2,y-1), on
diagonal d+1) iff w(d+1) = H; b-edge out iff w(d+1) = V; b-edge in (from (x-1,y-2), on diagonal d-1) iff w(d) = V.
The sum is 2. The a-edge from (x,y) covers BR(x,y) (ribbon d), and the b-edge from (x,y) covers BR(x,y+1)
(ribbon d+1): each ribbon is perfectly matched, so every quarter is covered once, no two tiles overlap, and by the
audited geometric lemma no two edges cross. (c) Read off the four edge types in (b). []
The split '\' is the mirror image (ribbons along slope -1; H = d moves, V = c moves).

Warning (Claim 30B, exact counterexample in the validated n = 96 tour w-integrator/tours/FOLD24_n96.json): a
connected good '/' region can contain two runs of the SAME ribbon with different bits, joined around bad squares
that interrupt the ribbon. So there is no single word per connected domain; T2(b)-(c) describe only defect-free
single-split fields.

Remarks. All-H is the pure (2,1) field; mixed words are the staircases of LB F8; an H|V word boundary is the
diagonal free fold, and its '\' analogue the sharp fold (w-structures S1). In a '/' domain only a and b moves occur.

## 3. T3: walls are straight axis lines

**Angle identity.** Let v be a good lattice point. Lattice points are tile vertices only (tile sides have lattice
length 1 or sqrt 2, the long diagonal is a knight move, the short diagonal is a unit edge between two vertices).
The eight quarters at v are covered exactly once, so the tile corners at v fill the full angle exactly once. A tile
has angle 45 deg at the ends of its edge and 135 deg at the ends of its carried unit edge. With b(v) = number of
unit edges at v that carry a tile:

    45 deg(v) + 135 b(v) = 360.          For a tour (deg = 2): b(v) = 2.

**T3.** Let v be a good lattice point with deg(v) = 2. Then either the four squares at v have one split, or exactly
two unit edges at v are wall edges and they are collinear (a straight wall through v). Moreover, a horizontal wall
forces H on every ribbon that meets it from either side, and a vertical wall forces V.
Proof. Going around v, the split changes an even number of times: 0, 2 or 4.
4 changes: no unit edge at v carries a tile (Consequence of T1), so b(v) = 0, a contradiction.
2 changes, not collinear: one square (the odd one) differs from the other three. The dihedral symmetries of the
lattice act on the 8 cases with two orbits; take the odd square NE = [0,1]^2 at v = (0,0). Its left side (N edge
at v) and bottom side (E edge) are walls.
- NE '\', others '/': the half LB of NE has both legs on walls, so no tile can cover it (Lemma 0 (ii)). Contradiction.
- NE '/', others '\': b(v) = 2 and the N, E edges are walls, so the S edge (between SW and SE) and the W edge (between
  NW and SW) both carry tiles. By Lemma 0 the S-edge tile (a d-tile) covers RT of SW, and the W-edge tile (a c-tile)
  also covers RT of SW. That quarter pair is covered twice. Contradiction.
Forcing: let the wall be horizontal with a '/' square S below it. The half TL of S has legs T (the wall) and L, so
its tile crosses L: an a-tile, i.e. the ribbon of TL(S) is H. With '\' below, the half RT has legs R and T (wall),
so its tile is a d-tile: H again. Above the wall the same argument applies with BR / LB. The vertical case is the
transpose (b or c tiles: V). By T2(a) the bit holds along that good run of the ribbon (not across a bad interruption). []

Consequences. (1) A wall cannot turn, branch, end or cross at a good point (1 or 3 changes are odd). So the walls
are straight horizontal or vertical segments whose ends are bad points or the board boundary. (2) Next to a
horizontal wall only a and d moves occur (the A|A' fold); next to a vertical wall only b and c (the B|B' fold).
Together with the remark after T2 this gives all four free folds of LB F3 / w-structures S1, and the rule of
LB F8 / F9 (at most two move types near a point, and they are angular neighbours).

## 4. T4: the defect budget

Hypothesis: H is a full spanning 2-factor (a closed tour suffices), U is a union of whole unit squares inside D, and
every tile overlap of a pair in B avoids U. A square is BAD if it is not good. By the audited relation m_0 - m_1 + m_2 - m_3 = 0 (cyclic order) a bad square
has at least two bad quarters. With E = X - 4n + 2, and B, U as in the audited inequality (1):

    number of bad squares inside U <= E + X - |B|,      number of bad squares <= X + E.

(The second: uncovered quarters G <= 2E, and each crossing pair overlaps in at most two quarters.)

**Summary theorem (repaired wording, as accepted in Claim 30).** In a closed tour, at most X + E unit squares fail
exact quarter coverage. Each remaining square has one diagonal split. On each uninterrupted run of good halves in a
fixed-split ribbon, the covering tiles have one H/V matching phase; different runs of one ribbon may differ. At a
degree-two lattice point incident to four good squares, split walls are absent or form one straight horizontal or
vertical line. Horizontal wall contacts force H, and vertical contacts force V, on their incident good ribbon runs.
Wall segments end only at bad points or the board boundary. A complete defect-free single-split field is the full
ribbon field of one word, whose strands are monotone translates.

## 5. Checks (both run 2026-10-03, ../../.venv/bin/python, from gap/structures/)

- `python tiling_check.py 6 6` (about 30 s): all crossing-free knight 2-factors of the 6x6 torus by CP-SAT
  enumeration (252). For each one it checks by geometry (quarter centroids) that every quarter is covered once and
  that each square splits with both tiles of its class (T1); it builds all 2 x 2^6 ribbon fields and checks degree 2
  and zero crossings (T2 (b)); the single-split solutions are exactly these 128 fields (T2 (a)); the other 124 have
  only straight full-length horizontal or vertical walls (T3).
- `python wall_check.py` (seconds): plane, v = (0,0), all 24 knight edges whose tile meets a square at v;
  constraints: the 16 quarters covered once and deg(v) = 2 only (weaker than a tour). CP-SAT enumeration: 48
  solutions = 32 single split + 8 horizontal + 8 vertical straight walls; no turn, no 4-wall; b(v) = 2 in all 48;
  carried tiles at a horizontal wall are (2,1) and (2,-1), at a vertical wall (1,2) and (1,-2).

## 5b. Dictionary with KT Lower Bounds W1 (fold stacks; SAT + checked DRUP, Claim 30 addendum)

W1: a fold stack (f, dA, dB), f in {x, y, x+y, x-y} (up to sign), chooses c[t] in {dA, dB} per level t; cell P has
the edges P - c[f(P)-1] and P + c[f(P)].
| W1 | here |
|---|---|
| f = x - y, moves (2,1), (-1,-2) | '/' ribbon field: level t = ribbon k = -t; c[t] = (2,1) iff bit H, c[t] = (-1,-2) iff bit V |
| f = x + y, moves (2,-1), (-1,2) | '\' ribbon field (mirror) |
| f = y, moves (2,1), (-2,1) | rows of good squares, '/' where c = (2,1) and '\' where c = (-2,1); a switch of c = a horizontal wall; all ribbon runs H (T3 forcing) |
| f = x, moves (1,2), (1,-2) | the transpose: vertical walls, all runs V |
| constant c / one switch / alternating | parallel field / one free fold / zigzag (dense folds) |
| "fold lines of different families never meet" | walls are straight and cannot meet or end at good points (T3); a diagonal H|V switch cannot touch a wall at a good point, because the wall forces H (or V) on every run that meets it |
Hypotheses differ: W1 assumes no crossing and exact degree 2 in a 9 x 9 core with 3 rings of context and concludes
for the central 3 x 3 block; T1-T3 assume exact coverage (good squares) and conclude at once, with no context. W1's
conclusion implies exact coverage in its centre (a fold stack is an exact tiling), so W1 also shows: crossing-free +
degree 2 with 3 rings of context forces no holes. They agree exactly, ring by ring (check `python w1_compare.py R`, 2026-10-03,
CP-SAT enumeration): with the (2+2R) x (2+2R) unit squares around a 3 x 3 block of points all good and degree 2 at
every interior point, the distinct central maps number 200 (R = 1), 164 (R = 2), 156 (R = 3); the 156 fold-stack
maps of W1 (generated directly from its definition) are a subset each time and equal at R = 3. W1 reports 164 at
2 rings (156 stacks + 8 junctions) and 156 at 3 rings. The extra maps at small R are runs that would meet a wall
just outside the window, where T3 forcing removes them. Neither proves
anything about bad squares, and neither gives one word per connected domain (W1's gluing corollary is ARGUMENT).

## 6. What this does not claim

It says nothing about bad squares: their shapes, and the price of a defect line between two ribbon fields, are
the open part of the structure lemma (gap/structures/PLAN.md, C3). The count X + E is linear in n for the tours of
interest, so the bad set is not negligible; it is where all excess crossings live.
