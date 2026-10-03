# Crossing-free parts of a knight tour are ribbon fields cut by straight axis walls

KT Structures, 2026-10-03. Status: PROOF (elementary), with two machine checks. For the Verifier (Claim 30).
Sources used: only the tile/quarter facts of w-turnstheory/PROOF_crossings_lower.md, Section 1 (audited).

## 0. Setting and the facts we use

Cells are the lattice points V = {0,...,n-1}^2, x = column (right), y = row (up). H is any set of knight edges
(a tour, a 2-factor, or a part of one); deg(v) is the degree of v in H. Move classes:
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

## 2. T2: a connected domain of one split is a ribbon field

Take split '/'. Write BR(i,j), TL(i,j) for the halves of the square with lower-left corner (i,j). By Lemma 0,
BR(i,j) can only be covered by an a-tile with partner TL(i+1,j) (carried edge = right side) or by a b-tile with
partner TL(i,j-1) (carried edge = bottom side). TL(i,j) can only pair with BR(i-1,j) (a) or BR(i,j+1) (b).
So the possible partners form a graph in which every half has degree 2; its components are the RIBBONS

    ... BR(i,j) - TL(i+1,j) - BR(i+1,j+1) - TL(i+2,j+1) - ...      (ribbon k = j - i),

staircases of half-squares along the slope +1 direction (ribbon k uses the BR halves on the diagonal j - i = k and
the TL halves on j - i = k - 1). Links of the form BR(i,j)-TL(i+1,j) are a-tiles ("H"); links TL(i+1,j)-BR(i+1,j+1)
are b-tiles ("V").

**T2.** (a) Along a run of consecutive good '/' squares of a ribbon, the tiles are all a-tiles or all b-tiles.
(b) Conversely, for every word w: Z -> {H, V}, the edge set
    a-edges (x,y)-(x+2,y+1) where w(y-x) = H,   b-edges (x,y)-(x+1,y+2) where w(y-x+1) = V
has degree 2 at every point and no crossing (the RIBBON FIELD of w).
(c) In a ribbon field, every edge changes y - x by exactly 1, and the two edges at v (on diagonal d = y - x) go to
diagonals d - 1 and d + 1. So every strand is monotone in y - x and meets each ribbon once; the strand step across
ribbon k is (2,1) if w(k) = H and (-1,-2) if w(k) = V (in the direction of decreasing y - x). All strands are
translates of each other by multiples of (1,1).
Proof. (a) In a run all halves are covered exactly once (T1), so the tiles are a perfect matching of a path
segment. If one link is used, its neighbouring links are not, and the next links are used: the choice propagates
along the whole run. (b) Degree at v = (x,y), d = y - x: a-edge out iff w(d) = H; a-edge in (from (x-2,y-1), on
diagonal d+1) iff w(d+1) = H; b-edge out iff w(d+1) = V; b-edge in (from (x-1,y-2), on diagonal d-1) iff w(d) = V.
The sum is 2. The a-edge from (x,y) covers BR(x,y) (ribbon d), and the b-edge from (x,y) covers BR(x,y+1)
(ribbon d+1): each ribbon is perfectly matched, so every quarter is covered once, no two tiles overlap, and by the
audited geometric lemma no two edges cross. (c) Read off the four edge types in (b). []
The split '\' is the mirror image (ribbons along slope -1; H = d moves, V = c moves).

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
transpose (b or c tiles: V). By T2(a) the bit holds along the whole good run of the ribbon. []

Consequences. (1) A wall cannot turn, branch, end or cross at a good point (1 or 3 changes are odd). So the walls
are straight horizontal or vertical segments whose ends are bad points or the board boundary. (2) Next to a
horizontal wall only a and d moves occur (the A|A' fold); next to a vertical wall only b and c (the B|B' fold).
Together with the remark after T2 this gives all four free folds of LB F3 / w-structures S1, and the rule of
LB F8 / F9 (at most two move types near a point, and they are angular neighbours).

## 4. T4: the defect budget

A square is BAD if it is not good. By the audited relation m_0 - m_1 + m_2 - m_3 = 0 (cyclic order) a bad square
has at least two bad quarters. With E = X - 4n + 2, and B, U as in the audited inequality (1):

    number of bad squares inside U <= E + X - |B|,      number of bad squares <= X + E.

(The second: uncovered quarters G <= 2E, and each crossing pair overlaps in at most two quarters.)

**Summary theorem.** Every closed tour with X crossings is, outside at most X + E bad squares, a union of ribbon
fields (one H/V bit per ribbon, all strands monotone translates) whose split changes only along straight
horizontal or vertical walls; walls force H (horizontal) or V (vertical) on the ribbons that meet them; and walls
end only at bad points or at the boundary of D.

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

## 6. What this does not claim

It says nothing about bad squares: their shapes, and the price of a defect line between two ribbon fields, are
the open part of the structure lemma (gap/structures/PLAN.md, C3). The count X + E is linear in n for the tours of
interest, so the bad set is not negligible; it is where all excess crossings live.
