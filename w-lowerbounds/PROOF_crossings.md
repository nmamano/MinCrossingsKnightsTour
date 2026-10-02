# Crossings lower bound (4 + 1/7392) n - O(1) for every knight 2-factor

Author: KT Lower Bounds. Date: 2026-10-02. Status: DRAFT. Every finite step has two independent certificates (Section 7, all PASS on
2026-10-02). Needs an independent human/agent review before it is reported as a theorem.

**Theorem.** There are constants n0 and C such that for n >= n0 every spanning 2-regular subgraph F
of the n x n knight graph (in particular every closed knight's tour) has at least
(4 + 1/7392) n - C pairs of properly crossing edges.

The constant 1/7392 is not optimised; the point is that 4 is not the right coefficient.

## 1. Notation

Cells are integer points (x, y), 0 <= x, y <= n-1. chi(x, y) = +1 if x + y is even, -1 otherwise.
A knight edge always joins cells of opposite colour, it contains no lattice point in its interior,
it never passes through a point (a+1/2, b+1/2), and two knight edges meet properly or in a common
end point or not at all (no overlaps).

Dual points: (a+1/2, b+1/2), 0 <= a, b <= n-2. A dual segment s is a directed unit segment between
two adjacent dual points. For an edge e that properly crosses s, its *left end* is the end point on
the left of the directed line of s. Define
  phi(s) = sum over edges e of F that cross s of chi(left end of e),
  c(s)   = the cell next to the midpoint of s on the right of s,
  w(s)   = phi(s) - chi(c(s)).
Both terms change sign when s is reversed (the other end of an edge, and the other side cell, have
the opposite colour), so w(-s) = -w(s).

## 2. Lemma 1 (a Z_3 potential; elementary)

For every closed dual path L of the board, sum_{s in L} w(s) = 0 (mod 3).

Proof. It suffices to take the counter-clockwise unit loop around an interior cell c0 (the dual
grid is simply connected, the loop sums add up, inner segments cancel by antisymmetry). The two
edges of F at c0 each leave the unit square once; their left end is c0: contribution 2 chi(c0).
Every other edge meets the square boundary 0 or 2 times (convexity; no end point inside, no passage
through a corner); at the two crossings the left ends are the two different end points, whose
colours cancel. The four right cells are the four orthogonal neighbours of c0, each of colour
-chi(c0). Total: 2 chi(c0) + 4 chi(c0) = 6 chi(c0) = 0 (mod 3).

## 3. Lemma 2 (M3, finite check)

Let s be a dual segment and Win(s) its 8 x 7 block of cells (for a horizontal s from
(a-1/2, b-1/2) to (a+1/2, b-1/2), and for a vertical s from (a-1/2, b-1/2) to (a-1/2, b+1/2):
Win(s) = [a-4, a+3] x [b-3, b+3]). If all cells of Win(s) are on the board and no two edges of F
that touch Win(s) cross, then w(s) = 0 (mod 3).

Check: the statement holds for the 7 x 7 sub-block used in the certified instances (two colour
classes for each orientation; all other segments are colour-preserving translates), and a larger
crossing-free block implies the smaller one. Certificates: Section 7, items C1, C2.

## 4. Lemma 3 (NE-M3, finite check)

Left board edge x = 0. Pattern P: (0,y)-(2,y+1), (0,y)-(1,y+2), (1,y)-(3,y+1) for all y.
Pattern P' is its mirror image (y -> -y). Suppose the cells of columns 0 and 1 in rows r-8..r+9
have exactly the edges of P (or exactly those of P'), and no two edges that touch the block
[0, j+4] x [r-6, r+7] cross, except two edges of the pattern. Then for 2 <= j <= 8 the segment
s_j from (j-1/2, r+1/2) to (j+1/2, r+1/2) has w(s_j) = 0 (mod 3). (In fact phi(s_j) = chi(j, r)
exactly, CP-SAT.) By transposition (x,y) -> (y,x), which preserves colours and reverses
orientation (w(Ts) = -w(s)), the same holds at the bottom edge for the transposed patterns.
Certificates: C3, C4 (P and P', both parities of r, j = 2..8).

## 5. Lemma 4 (corner charge, finite enumeration)

For R >= 12 let L_R be the counter-clockwise boundary of the dual square with corners (1/2,1/2),
(R+1/2,1/2), (R+1/2,R+1/2), (1/2,R+1/2). Let Q be the sum of w over: the left side, the bottom side,
the first segment (R+1/2,1/2)->(R+1/2,3/2) of the right side, and the last segment
(3/2,R+1/2)->(1/2,R+1/2) of the top side. Suppose columns 0,1 of rows R-3..R+9 carry P or P', and
rows 0,1 of columns R-3..R+9 carry the transposed P or P'. Then Q = 1 (mod 3), whatever F does
elsewhere.

Proof. Only edges with an end point in column 0 cross the line x = 1/2, and only edges with an end
point in row 0 cross y = 1/2. An edge of a column-0 cell in a row 4 <= y <= R-3 crosses the left
side exactly once, with left end (east side) of colour -chi(0, y), whatever its direction; so each
such cell contributes -2 chi(0, y), independently of F. The same holds on the bottom. The
remaining contributions come from (i) the seven corner cells (0,0..3), (1..3,0), whose edges are
arbitrary (all degree-consistent choices are enumerated; edges between two of them cross the path
twice and cancel), and (ii) the patterns near row R and column R, which are fixed by the hypothesis.
For R >= 12, Q(R+2) = Q(R) (two more middle cells of opposite colours per side, and the end region
is a colour-preserving translate), so R = 12 and 13 suffice. Enumeration: for all 4 pattern
combinations, both parities, and all 2916 corner options, Q = 1 (mod 3). Certificates: C5, C6.

## 6. The counting argument

**Strips.** For a board side sigma, let S_sigma be its two outermost lines of cells, B_sigma the set
of crossing pairs among edges that touch S_sigma, B the union, and I the set of all other crossing
pairs. Then X(F) >= |B| + |I| and |B| >= sum |B_sigma| - C1 (overlaps only near corners).

**Stability (from the width-2 transfer graph of F1/F5).** The column-by-column scan of S_sigma is a
walk of 4n steps from the start state in the finite transfer graph G2 (82,516 states; it encodes
all edges at columns 0,1 with their other ends in columns 0..3, degree 2, no cycle, and the crossing
weight). Let d be the exact shortest-distance potential with step weight w - 1/4 (Bellman-Ford; no
negative cycle). Reduced costs red = w - 1/4 + d(u) - d(v) are >= 0 and are integers/4. Exact
values (C7): every positive reduced cost is >= 1 (rho = 1); d ranges in [-1/4, 135/4]; the tight
graph contains exactly two cycles (patterns P and P', period one row = 4 steps); the tight graph
without these cycle edges is acyclic with longest path T* = 37 steps. Hence
  |B_sigma| >= n - 34 + E_sigma,   E_sigma = sum of reduced costs >= N_nt (non-tight steps),
and a counting of maximal non-cycle runs gives N_nc <= (3T*+1) N_nt + 3T* = 112 N_nt + 111.
Call a row *good* if the 12 steps of it and the two rows below lie on one tight cycle; then columns
0,1 of every interval of good rows carry exactly P (or exactly P'). Each non-cycle step makes at
most 3 rows bad, so bad rows <= 336 E_sigma + 333.

**One defect per square.** Fix the bottom-left corner and R in [12, n/2 - 9]. If (a) rows
R-10..R+11 of the left side and columns R-10..R+11 of the bottom side are good, and (b) every segment
of the top and right sides of L_R other than the two used in Q satisfies the hypothesis of Lemma 2
or Lemma 3 (j >= 2, NE window; M3 window when x >= 8.5 or y >= 8.5), then
  sum_{L_R} w = Q + 0 = 1 (mod 3),
contradicting Lemma 1. So (a) or (b) fails. If (a) holds and (b) fails, the failing window contains
a crossing pair that is not a pattern pair; since all strip edges touching the window belong to good
rows (exactly P/P'), the pair is in I. Same for the other three corners (by symmetry).

**Charging.** A bad row of a side is used by at most 22 values of R for each of the two corners at
that side: <= 44. A crossing pair in I has its 4 end points in a 5 x 5 box; it touches the windows
of at most 2 x (14 + 4) = 36 squares of one corner, and squares of different corners are disjoint
(R <= n/2 - 9). With R ranging over n/2 - 20 values for each of 4 corners:
  2n - 80 <= 36 |I| + 44 sum_sigma (336 E_sigma + 333).
Therefore |I| + sum E_sigma >= (2n - C2) / (44 * 336) = (2n - C2)/14784, and
  X(F) >= sum_sigma (n - 34 + E_sigma) - C1 + |I| >= 4n + 2n/14784 - C = (4 + 1/7392) n - C.

## 7. Finite checks and certificates

| id | statement | primary | independent |
|---|---|---|---|
| C1 | M3, 4 instances (h/v, 2 colour classes), 7x7 window, frame 2 | local_m3.py (CP-SAT: other values in -6..6 INFEASIBLE) | sat_cert.py m3: own CNF + Glucose4 UNSAT + DRUP proof, checked by check_drup.py (4/4 PASS) |
| C2 | the CNF is not trivially UNSAT | wrong residues are SAT (sat_cert sanity) | check_drup rejects an empty proof |
| C3 | NE-M3, 28 instances (P, P'; r = 8, 9; j = 2..8) | ne_m3.py (CP-SAT, all values -6..6) | sat_cert.py nem3: 28/28 UNSAT, DRUP checked (certs/) |
| C4 | NE CNF not trivially UNSAT | wrong residues SAT for two instances | - |
| C5 | Lemma 4 enumeration: Q = 1 mod 3 for all 2916 corner options, 4 pattern pairs, R = 12, 13 | corner_charge.py (also R = 14, 15) | corner_charge2.py (separate code, exact fractions): same result |
| C6 | Q(R+2) = Q(R) for R >= 12 | proof in Section 5 | corner_charge.py checks R = 12..15 |
| C7 | width-2 strip graph: 82,516 states, 144,674 arcs; potential range [-1/4, 135/4]; rho = 1; exactly two tight cycles (P, P'), each of 4 steps; T* = 37 | strip_constants.py (uses strip_dp.py) | strip2_independent.py (separate code, own geometry and SCC/DAG code): identical numbers |

## 8. Gaps to review

- The window multiplicities (22, 36, 44) and the strip overlap constants should be re-derived by a
  reviewer; they only affect the value of c, not its positivity.
- Good rows (self-check done 2026-10-02): if the 4 steps of row y are cycle edges, the state at the
  start of row y is a cycle state, so the pending (downward) edges of the row-y cells are pattern
  edges and the chosen upward edges are pattern edges; consecutive good rows lie on the same cycle
  (the two cycles are disjoint and the walk is continuous). The 3-row definition is conservative.
- Walk sum (self-check): sum of weights = sum red + n + d(end) - d(start) >= n - 1/4 + E_sigma, so the
  additive constant 34 can be replaced by 1/4.
- N_nc bound (self-check): every tight closed walk lies in a tight SCC, and the only tight SCCs with
  a cycle are the two 4-cycles, whose only tight arcs are the cycle arcs (C7). So fully tight
  non-cycle runs between cycle segments go from one cycle to the other, only in one direction.
