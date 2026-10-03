# A lower bound of 14n/3-O(1) crossings

2026-10-02. For every even n>=32, every closed knight's tour on an n by n
board has at least 14n/3-O(1) proper crossing pairs. The certificate also
gives the explicit bound 14n/3-407. The proof uses exact local geometry
and finite strip potentials; it uses no solver.

## 1. Tiles turn crossings into an area budget

Put the cell centres at V={0,...,n-1} squared, with x the column and y the
row. A knight edge has coordinate differences of absolute values 1 and 2.
The tour H is a connected simple degree-two graph on V, with n squared
edges. Count unordered pairs of edges whose relative interiors cross
properly; a shared endpoint does not count. Write X for this count.
Put chi(x,y)=(-1)^(x+y); black means chi=1 and white means chi=-1.

For each tour edge e, form its **tile**: the parallelogram whose long
diagonal is e and whose short diagonal is the unit grid edge with the
same midpoint. For (0,0)--(2,1), its vertices are (0,0),(1,0),(2,1),(1,1).
It has area one and stays in the endpoint box of e, hence inside
D=[0,n-1] squared. Divide each unit square by both diagonals into four
open quarter triangles. Each tile consists of four such quarters.

**Finite geometric lemma.** Two distinct tiles overlap in positive area
exactly when their knight edges cross properly. Their overlap then has
one or two quarters. Tiles at a shared edge endpoint have no area overlap.
The exact checker fixes one endpoint at zero, tests the four unoriented
knight directions, and places the second edge in the sufficient box
[-4,4] squared. A tile has coordinate span at most two.

Let m_t be the tile multiplicity at quarter t. A quarter is **bad** if
m_t is not one. Let G count uncovered quarters. Since there are 4n^2 tile
incidences and 4(n-1)^2 quarters in D,

    sum_t (m_t-1)_+ = 8n-4+G <= 2X.

The inequality uses (m-1)_+<=binomial(m,2) and the geometric lemma.
Set E=X-4n+2. Thus E>=0 and G<=2E.

Let B be any set of crossing pairs whose tile overlaps avoid a set U of
quarters inside D. Every multiply covered quarter in U belongs to a
crossing pair outside B, and each pair covers at most two common quarters.
Therefore

    bad(U) <= 2E+2(X-|B|).                             (1)

**Figure 1.** Draw the tile for (0,0)--(2,1), split into quarters. Beside
it draw the overlapping tiles for (0,0)--(2,1) and (0,1)--(2,0); shade
their two common quarters. Distinguish area overlap from boundary contact.

## 2. A nonzero colour flux forces two bad quarters

The centres of the unit squares of D and their unit steps form the
**internal dual grid**. Every counted path lies in this grid. Longer
segments below mean sequences of unit steps; an integral means a sum of
signed step fluxes. Auxiliary loops can extend half a unit outside D.

Orient knight edges from black to white. For a directed dual step s,
let phi_H(s) be their signed flux from its left to its right. If the
crossed unit grid edge is ab, with a on the left, let m_+,m_- be the
multiplicities of its two adjacent quarters and let g count selected
tiles whose short diagonal is ab.

**Finite flux lemma.** For every selected edge set,

    phi_H(s)=chi(a)(m_++m_--3g).

This is linear in selected edges. The checker tests one edge at a time
in every relative position that can contribute. Add the flux of all
unit grid edges, also oriented black to white. This gives the integer
flux omega, whose residue satisfies

    omega(s)=chi(a)(m_++m_-+1) mod 3.                   (2)

For any finite set A of board cells, orient its dual boundary with A on
the left. A knight segment crosses three dual grid lines at parameters
1/4,1/2,3/4. Replace it by the three unit lattice steps in those same
coordinate directions: for displacement (a,b) with |a|=2 these are
(sign(a),0), (0,sign(b)), (sign(a),0); transpose when |b|=2. Its signed
boundary flux is chi(p)(1_A(p)-1_A(q)), by telescoping. Summing knight
edges and unit grid edges gives

    integral_(boundary A) omega
      = sum_(v in A) chi(v)(deg_H(v)+4)=6 sum_(v in A) chi(v).   (3)

Thus omega has zero circulation modulo three on internal dual loops.
Call a path **charged** if its total flux is nonzero modulo three.
Such a path has a step with
nonzero flux, so (2) forces a bad adjacent quarter.

Each tile occupies two adjacent quarters in each square it visits.
Hence the four multiplicities in a square, in cyclic order, satisfy
m_0-m_1+m_2-m_3=0. One bad quarter therefore forces a second bad quarter
in the same square. Its centre is a vertex of the charged path.
Vertex-disjoint charged paths give distinct such squares. If U contains
all whole squares centred on L such paths, then

    2L <= bad(U).                                      (4)

**Figure 2.** Draw the dual step (1/2,1/2)--(3/2,1/2), its crossed grid
edge (1,0)--(1,1), and the two adjacent quarters. Mark the left-to-right
flux sign. In a second panel label a square's four quarters +,-,+,- to
show why one defect forces another.

## 3. A local endpoint test forces a corner charge

Fix side coordinates (inward distance, scan row): use (x,y), (n-1-x,y),
(y,x), (n-1-y,x) for the left, right, bottom, top sides, respectively.
Each side uses one scan direction at both corners.

At scan row R, translate the row coordinate by -R. Let F be the sum of
these coefficients over selected edges:

| Edge | Coefficient |
| --- | ---: |
| (0,-1)--(1,1) | -1 |
| (0,0)--(1,-2) | -1 |
| (0,0)--(2,-1) | -1 |
| (0,1)--(1,-1) | +1 |
| (0,1)--(2,0) | +1 |
| (0,2)--(1,0) | -1 |
| (1,0)--(2,2) | -1 |
| (1,1)--(2,-1) | -1 |

The **up test** passes if F=2 modulo three and the edges
(0,0)--(2,1), (0,1)--(2,0) are not both selected. Reflect the whole test
by y -> -y to obtain the **down test**. The **joint test** requires both.

Use the bottom-left corner and 12<=R<=n/2-4. Enclose the cells
A_R={0,...,R} squared by their counterclockwise dual boundary. Retain
its internal right-and-top path

    gamma_R: (R+1/2,3/2) -> (R+1/2,R+1/2) -> (3/2,R+1/2).

The complementary path Q_R consists of two top end steps, the outside
left and bottom sides at coordinate -1/2, and two right end steps.
No tour edge crosses the outside sides. Their unit-grid flux is
2 sum_(j=0)^R (-1)^j=1+(-1)^R. The grid flux on each pair of end steps
is zero.

**Finite endpoint lemma.** Divide the tour flux through the two top end
steps by chi(0,R)=(-1)^R. The result is F+deg_H(0,R)=F+2.
The checker enumerates the eight possible contributing knight edges;
subtracting the coefficient list for F leaves exactly the four possible
edges incident to (0,R), each with coefficient one. This proves the
identity for arbitrary selected edges. Transpose coordinates and reverse
the dual directions for the right end.

If both up tests pass, each end contributes (-1)^R modulo three. Hence

    integral_(Q_R) omega = 1+(-1)^R+2(-1)^R = 1 mod 3.

By (3), gamma_R is charged. Reflections give the other corners; the joint
test supplies the required orientation at either end of each side.
Only gamma_R enters the area count. No outside quarter is counted.

**Figure 3.** Draw A_R and its boundary at -1/2 and R+1/2. Colour gamma_R
and Q_R differently. Mark top grid edges (0,R)--(0,R+1),
(1,R)--(1,R+1), and their transposes at the right end. Show the eight
endpoint edges from the table in a separate translated inset.

## 4. Boundary crossings avoid the path squares

For each side sigma, let B_sigma be all crossing pairs among edges
incident to its outermost column. Let B be their union.

**Finite boundary lemma.** |B_sigma|>=n-1. Keep exactly the edges
incident to column 0. They form a forest: a proper subgraph of a
Hamiltonian cycle cannot contain a cycle. Scan this width-one strip
with degree two in column 0 and degree at most two in columns 1,2.
The finite scan is defined in Section 5. Its 330-state graph has an
integer potential p, with p(start)=0 and min p=-3, satisfying
3w-1+p(u)-p(v)>=0 on every transition. Summing over 3n transitions proves
the claim. Adjacent sides share only a bounded corner region. Thus

    |B| >= 4n-O(1).                                    (5)

**Finite overlap lemma.** Positive-area overlap of tiles of two edges
incident to column 0 can enter [1,2] x [j,j+1] only for the pair

    (0,j)--(2,j+1), (0,j+1)--(2,j).                    (6)

No such overlap enters a square with left coordinate at least two. The
checker tests all 20 crossing configurations up to vertical translation.
The only path square at depth one is the endpoint square, where j=R.
The up test excludes (6); the down test excludes its reflected version
at the other end of a side. All other squares are farther inside.
Consequently overlaps from B avoid the whole-square union U of retained
paths. From (1), (4), and (5),

    2L <= 4E+O(1).                                    (7)

**Figure 4.** Draw the two edges in (6) for j=0, and shade only their
positive-area overlap. Mark the path endpoint (3/2,1/2) and its whole
unit square. Show that no column-0 overlap enters the next square inward.

## 5. Strip stability pays for failed endpoint tests

Keep all edges incident to columns 0 or 1 of a side. Their other endpoints
lie in columns 2 or 3. This again is a forest. Its boundary columns have
degree two and its other columns have degree at most two.

Scan in increasing (row,column) order from an empty initial state.
A state records the next column, selected edges from processed to future
cells, and the partition of their pending ends into paths. Coordinates
are relative to the current row; path labels are immaterial. At each
cell choose edges to later cells, enforce the degree bounds, and reject
closed components. After the last column shift row coordinates by -1.
Use only states reachable from the empty state. The state space is finite
because knight edges span at most two rows. Each transition weight w
counts crossings introduced by its new edges. A board strip is a walk
of 4n transitions of total weight X_sigma. The width-one scan in Section 4
uses the same rule with three columns and degree two only in column 0.

For the width-two graph, record also the set of test edges seen in the
current row. Initialise from pending edges, then add newly selected test
edges once. At row end evaluate both endpoint tests, charge f=1 if either
fails, and reset. Every test edge straddles that row, so these data suffice.

**Finite stability lemma.** On this augmented graph an integer potential
p in [-29,0] satisfies

    4w-1-4f+p(u)-p(v)>=0.

The independent checker builds the graph and relaxes every integer arc
inequality until none changes. The wrapper requires convergence and the
stated range. Summing over the strip walk proves

    X_sigma-n >= b_sigma-29/4,

where b_sigma counts failed joint tests. Crossing pairs counted by two
side strips lie in fixed-size corner regions. Thus sum X_sigma<=X+O(1),
and for b=sum b_sigma,

    b <= E+O(1).                                      (8)

This is the only stability coefficient used. Its optimality is not needed.
The forest condition is why this proof applies to Hamiltonian tours.

**Figure 5.** Show the four scan cells (0,R),...,(3,R), a pending edge
(0,R-1)--(1,R+1), and newly added edges. Show the set of test edges being
reset after phase 3. Label one arc with its weight and potential inequality.

## 6. Count paths and conclude

At each corner take 12<=R<=n/2-4. This gives 2n-60 candidate paths in total.
They are vertex-disjoint: a path's maximum local coordinate fixes its
radius, and the four corner boxes are separated. Their whole squares
are inside D. Discard a path if either endpoint fails the joint test.

In a fixed side scan the near corner tests R and the far corner tests
n-1-R with reflected data. The row sets [12,n/2-4] and [n/2+3,n-13] are
disjoint. One failed side-row therefore removes at most one path. Hence

    L >= 2n-b-O(1).

Together with (7) and (8), this gives

    4n <= 4E+2b+O(1) <= 6E+O(1),
    X=4n-2+E >= 14n/3-O(1).

For the explicit constant, the same checks give |B|>=4n-24 and
sum X_sigma<=X+1104. Thus 2L<=4E+44, b<=E+1131, and
4n<=6E+2426, which implies X>=14n/3-407. These constants play no role
in the leading coefficient.

**Figure 6.** Draw all four families of nested paths, with a gap between
corner boxes. Highlight one failed side-row and the single path it can
remove. Put the inequalities L>=2n-b-O(1) and 2L<=4E+O(1) beside the drawing.

## 7. One command checks every finite input

Run from the project root:

```sh
python3 w-turnstheory/check_crossings_lower.py
```

The runner uses the Python standard library, one process at a time, and
no solver. It stops on any failure and writes `crossings_lower_checks.json`.
Its five checks are:

| Input | Checker in w-turnstheory/ |
| --- | --- |
| Tile geometry and local flux | check_knight_tiles.py |
| Arbitrary-edge endpoint identity | check_corner_box.py |
| Boundary potential and positive-area overlap | check_col0_squares.py |
| Alternating square identity | check_square_defects.py |
| Joint endpoint potential and corner overcount | check_lower_stability.py |

The last check uses the independent implementation
`w-lowerbounds/endpoint_independent.py`, not a saved solver answer.
The circulation, charge, path disjointness, and final count are the
arguments above; finite tests alone do not replace them.

**Figure 7.** A dependency diagram: tiles give an area budget; endpoint
flux gives charged paths; boundary exclusion and the square identity
bound their number; strip stability bounds the discarded paths.
