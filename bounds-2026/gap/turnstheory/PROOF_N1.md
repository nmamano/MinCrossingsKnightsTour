# Claim 27: interval credit and the N1 crossing bound

2026-10-03. **CONDITIONAL PROOF SUBMITTED FOR AUDIT.** The interval
certificate has passed two strip implementations. KT Lower Bounds and
KT Edge Searcher independently certified the combined coefficient
beta=16/11 in Python and C++, in both orientations and both parities.
The all-size reduction and interval application await Claim 27 review.

**Proposed theorem.** For every even n>=32, every closed Hamiltonian
knight tour on an n by n board has

```
X >= 204n/43 - 12993.
```

The exact conservative constant below is 558664/43. This is not yet an
audited improvement. No Lean result and no result for arbitrary
2-factors is claimed. The large constant comes from a coarse corner
union bound; the leading coefficient is the objective.

This document consolidates the full argument. Sections 1–3 repeat the
audited tile, endpoint, and boundary-credit argument of Claim 26.
Section 4 proves the interval input. Section 5 states the precise new
finite input and proves N1. Section 6 combines the inequalities. The
sharper short-run research is separate and is not an input to this claim.
Equations in the interval subsection have local numbering.

## 1. Tiles and charged paths

The board vertices are `V={0,...,n-1}^2`, with colour
`chi(x,y)=(-1)^(x+y)`. A tour is a connected simple graph of degree two
on `V`. Its edges are legal knight moves. `X` counts unordered pairs of
edges whose relative interiors cross properly. Shared endpoints do not
count. Put `E=X-4n+2`.

For each tour edge, form the parallelogram whose long diagonal is that
edge and whose short diagonal is the unit grid edge with the same
midpoint. For example, the edge `(0,0)--(2,1)` has tile vertices
`(0,0),(1,0),(2,1),(1,1)`. Each tile has area one and lies inside
`D=[0,n-1]^2`. Divide every unit square into four open quarter triangles
by both its diagonals. A tile contains four quarters.

Two distinct tiles overlap in positive area exactly when their edges
cross properly. Their overlap then consists of one or two quarters.
Tiles at a common edge endpoint have no positive-area overlap. These
finite geometric facts are checked by `check_knight_tiles.py`.

Let `m_t` be the tile multiplicity of quarter `t`, and let `G` count
uncovered quarters. The difference between tile area and board area gives

```
sum_t (m_t-1)_+ = 8n-4+G <= 2X,
G <= 2E.                                               (1)
```

Call a quarter bad if its multiplicity is not one. Let `B` be a set of
crossing pairs whose tile overlaps avoid a region `U` made from whole
unit squares. At most `G` quarters in `U` are uncovered. Every multiply
covered quarter in `U` belongs to a crossing pair outside `B`, and one
pair covers at most two such quarters. Thus

```
bad(U) <= 2E+2(X-|B|).                                 (2)
```

The internal dual grid has vertices at the unit-square centres. Orient
each tour edge and each unit lattice edge from black to white. On a
directed dual step, let `omega` be their combined signed flux from the
left to the right of that step. If the crossed unit edge has endpoint
`a` on the left, the exact local flux calculation gives

```
omega = chi(a)*(m_+ + m_- + 1) mod 3,                  (3)
```

where `m_+,m_-` are the multiplicities of its two adjacent quarters.
Indeed the tour-edge flux is `chi(a)*(m_++m_--3g)`, where `g` counts
selected tiles with that unit edge as short diagonal. Adding the unit
edge flux gives (3).

For a cell set `A`, the combined flux across its dual boundary is
`6 sum_(v in A) chi(v)`. To verify this, replace each knight segment by
the three unit lattice steps in the order in which that segment crosses
dual lines. The steps telescope to the endpoint difference. The tour
degree contributes two and the unit grid degree contributes four.
Consequently every internal dual loop has zero total flux modulo three.

A dual path is charged if its flux is nonzero modulo three. Some step
of such a path has nonzero flux, so (3) gives a bad adjacent quarter.
Every tile occupies two adjacent quarters in each square it visits.
The four multiplicities of a square therefore have alternating sum
zero. A square with one bad quarter has at least two bad quarters.
For vertex-disjoint charged paths, these witness squares are distinct.
If `U` contains all squares centred on `L` such paths, then

```
2L <= bad(U).                                         (4)
```

## 2. Corner residues and fractional loss

At the bottom-left corner take integer radii `12<=r<=n/2-4`. The dual
path is

```
gamma_r: (r+1/2,3/2) -> (r+1/2,r+1/2) -> (3/2,r+1/2).
```

Reflect or rotate this construction at the other three corners. A
path's maximum local coordinate fixes its radius; corner boxes are
separated. All paths are vertex-disjoint and internal. There are exactly
`N=2n-60` candidate paths.

For each side, use coordinates `(inward depth, scan row)`, with one fixed
scan direction. Translate a tested row to row zero. The up endpoint
quantity `F` is the sum of these coefficients over selected edges:

| Edge | Coefficient |
| --- | ---: |
| `(0,-1)--(1,1)` | -1 |
| `(0,0)--(1,-2)` | -1 |
| `(0,0)--(2,-1)` | -1 |
| `(0,1)--(1,-1)` | +1 |
| `(0,1)--(2,0)` | +1 |
| `(0,2)--(1,0)` | -1 |
| `(1,0)--(2,2)` | -1 |
| `(1,1)--(2,-1)` | -1 |

Let `e=1` when both `(0,0)--(2,1)` and `(0,1)--(2,0)` are selected;
otherwise set `e=0`. Reflect this entire definition by `y -> -y` for the
down endpoint data. The local radius from the relevant corner, rather
than the fixed physical scan index, determines its parity.

For `c=(-1)^r`, define the endpoint residue

```
h = (1+c)/2 + c*(F+2) mod 3.                           (5)
```

To prove (5), enclose the cells `[0,r]^2` by their dual boundary. Apart
from `gamma_r`, this boundary contains two end steps at each side and
the outside left and bottom portions. The tour flux through two end
steps, divided by `c`, is `F+deg_H(0,r)=F+2`. The arbitrary-edge
coefficient identity is checked by `check_corner_box.py`. The unit-grid
flux on those two steps cancels, and the outside portion of that side
has grid flux `sum_(j=0)^r (-1)^j=(1+c)/2`. The outside tour flux is zero.
The other endpoint follows by transposition with the boundary direction
reversed. Thus the complementary path has flux equal to the sum of its
two endpoint residues. Since the full boundary has zero flux modulo
three, `gamma_r` is charged exactly when that sum is nonzero. Reflections
give the same conclusion at the other corners.

Keep a candidate path exactly when neither endpoint has `e=1` and its
two residues do not sum to zero. Assign the endpoint penalty

```
a=1 if e=1;
a=1/2 if e=0,h=0;  a=1 if e=0,h=1;  a=0 if e=0,h=2.
```

The discard indicator is at most the sum of endpoint penalties. An
exception pays one itself. In its absence, the zero-sum pairs are
`(0,0),(1,2),(2,1)`, whose penalty sums are all one. Let `A` be the total
penalty of all candidate endpoints. Then

```
L >= 2n-60-A.                                         (6)
```

For each physical side, its near-corner rows lie in `[12,n/2-4]` and its
far-corner rows in `[n/2+3,n-13]`. The intervals are disjoint. Thus every
used side-row supplies at most one endpoint penalty.

## 3. Keep the boundary surplus

For side `sigma`, let `B_sigma` be the set of crossing pairs both of
whose edges have an endpoint at depth zero. Put `b_sigma=|B_sigma|`,
`B=union B_sigma`, and

```
R = sum_sigma b_sigma - 4n.                            (7)
```

Every tile overlap of a pair in `B_sigma` lies in the outermost square
column except for one possible pair in a square at depth one:

```
(0,j)--(2,j+1), (0,j+1)--(2,j).
```

No such overlap enters a square at depth at least two. This is an exact
finite geometric check in `check_col0_squares.py`. A candidate path has
only its endpoint square at depth one relative to a side. Retention
excludes precisely this exceptional pair, in the appropriate orientation.
Therefore all overlaps from `B` avoid the whole-square union `U` of the
retained paths.

For adjacent sides, an edge touching both outermost columns must be
one of four corner edges:

```
(0,0)--(1,2), (0,0)--(2,1),
(0,1)--(2,0), (0,2)--(1,0).
```

These four edges have five crossing pairs. Opposite sides share none
for `n>=32`. The union overcount is therefore at most twenty:

```
|B| >= sum_sigma b_sigma-20 = 4n+R-20.                 (8)
```

Use (2), (4), and `X=4n-2+E` without replacing `R` by zero:

```
2L <= 2E+2(X-|B|) <= 4E-2R+36.
4n <= 4E+2(A-R)+156.                                  (9)
```

This retained surplus is the new geometric step. It uses the same
overlap exclusion as before. It needs no new boundary lower bound.

## 4. Interval credit and its separate budget

### Interval statement

Let `J` be a finite forest of legal knight edges with endpoints in
`{0,1,2} x Z`. Every edge has an endpoint in column zero, and every
vertex has degree at most two. Scan cells in increasing row order, then
column order. An edge is added when its lower endpoint is processed.
Assign a crossing pair to the transition that adds its later edge.

Let `I` be an interval of `l` consecutive rows such that every vertex
`(0,y)`, `y in I`, has degree two in `J`. Let `W(I)` be the number of
crossings assigned to transitions in those rows. Then

```
W(I) >= l-4.                                          (1)
```

For any collection of disjoint such row intervals with lengths `l_i`,
the total number `X_J` of crossing pairs in `J` therefore satisfies

```
X_J >= sum_i max(0,l_i-4).                             (2)
```

`W(I)` can include an edge whose lower endpoint is outside `I`. The
statement concerns the row to which the crossing is assigned, not the
subgraph induced by the interval. This distinction avoids cut errors.

### Interval certificate and proof

A scan state records the next column and the pending edges, with row
coordinates relative to the current row. It also records the partition
of pending edges into connected path components. Canonical labels remove
irrelevant component names. There are only finitely many states because
a knight edge spans at most two rows and every degree is at most two.

Start before all edges, with an empty state. At every cell allow degree
zero, one, or two. Reject excess degrees at future endpoints and any
cycle closure. This degree rule applies to column zero as well as the
ghost columns. Thus an arbitrary prefix of the forest, including rows
with incomplete column-zero degree, is a valid scan. Components that
have no pending edge need not stay in the state: no future edge can
reach them.

A transition adds a set of edges from the current cell to future cells.
Its nonnegative integer weight `w` is the number of new crossing pairs.
It suffices to compare new edges with pending edges and one another.
A completed past edge ends at or below the current row and cannot
properly cross a new edge. Incoming edges at the current cell share
its endpoint with the new edges, so they cannot give proper crossings.
Thus every crossing is counted exactly once.

Call a transition hard if it processes column one or two, or if it
processes column zero with final degree two. Complete enumeration gives
330 reachable states, 700 transitions, and 580 hard transitions. The
saved integer potential `p` obeys, on every hard transition,

```
3w-1+p(u)-p(v) >= 0.                                 (3)
```

At all row boundaries its values lie between -12 and zero. The
certificate generator verifies (3) on every hard arc after exact integer
relaxation has reached a fixed point. A separate strip implementation
reconstructs the states and verifies all 580 inequalities against the
saved potential. It imports no code from the generator.

The `3l` transitions of `I` are all hard. Summing (3) gives

```
3W(I)-3l >= p(end)-p(start) >= -12,
```

which proves (1). Every interval endpoint is a state of the full soft
scan. No empty-state assumption is made at either end of the interval.
Disjoint intervals have disjoint transition sets, and all weights are
nonnegative. Apply (1) only to intervals longer than four and sum to
obtain (2).

### How a tour forces these intervals

Take a closed tour on an n by n board with n>=32. Use coordinates
`(inward depth, row)` for one physical side. Let `S` contain the selected
edges with an endpoint in column zero or one. Let `d_x(y)` be the degree
of `(x,y)` in `S`, not its full tour degree. For `2<=y<=n-3`, call row y
blocked when

```
d_3(y)=0,    d_2(y-2)=2,    d_2(y+2)=2.                (4)
```

The four possible left neighbours of `(3,y)` are `(1,y-1)`, `(1,y+1)`,
`(2,y-2)`, and `(2,y+2)`. Edges to column one belong to `S`, so `d_3(y)=0`
excludes both. Each listed column-two vertex already has degree two in
`S`, so it cannot take another tour edge. Consequently both tour edges
at `(3,y)` go to column four or five.

Let `J` consist of all selected edges joining column three to column
four or five, for all rows. After translation by three columns, it has
the form required by the lemma. It has maximum degree two. It is a
forest because it is a proper subgraph of the Hamiltonian cycle.
Each blocked row has degree two at its boundary vertex. For the maximal
blocked runs define

```
K_sigma = sum_runs max(0,run_length-4).
```

Equation (2) gives `X_(J_sigma)>=K_sigma`. This statement uses only the
width-two strip data to identify the runs. It needs no assumptions about
the tour in columns four and five beyond their tour degrees.

### Separate crossing budget for four sides

On a fixed side, `S_sigma` and `J_sigma` have disjoint edge sets, hence
disjoint crossing-pair sets. Every edge in either set has both endpoints
at depth at most five. Opposite-side sets are disjoint for n>=32. If a
pair is counted by sets from adjacent sides, both of its edges lie in
the six-by-six corner square. That square has 80 possible knight edges,
so each pair of sets shares at most `binomial(80,2)=3160` crossing pairs.
There are four adjacent side pairs and four choices of S or J for each
pair. The sum of these pairwise intersection bounds controls every
multiple count, since `m-1 <= binomial(m,2)`. Therefore

```
sum_sigma (X_(S_sigma)+X_(J_sigma)) <= X+50560.
```

For `D0=sum_sigma X_(S_sigma)-4n`, `K=sum_sigma K_sigma`, and
`E=X-4n+2`, this gives the explicit, conservative consequence

```
D0+K <= E+50558.                                     (5)
```

The constant is not optimised. The planned combined-credit proof needs
only that it is independent of n.

## 5. The combined finite certificate and N1

For each side let S_sigma be the tour edges with an endpoint in column
zero or one. Let X_sigma count its crossings, let b_sigma count the
crossings whose two edges both touch column zero, and put

```
D0 = sum X_sigma - 4n,   R = sum b_sigma - 4n,
K = sum K_sigma,        E = X-4n+2.
```

A is the sum of the fractional penalties on candidate endpoints only,
as defined in Section 2. In particular A is not a sum over every row.
Section 4 gives the independent crossing budget

```
D0+K <= E+50558.                                      (N0)
```

### Scan and row data

Scan the four-column side strip in increasing row and column order.
The two outer columns have degree exactly two; the two ghost columns
have degree at most two. Choose only legal knight edges to later cells
with an endpoint in column zero or one. Reject excess degrees and cycle
closure. Retain pending edges and their path-component partition, with
relative row coordinates and canonical labels. The actual tour gives a
walk from the empty state because S_sigma is a proper subgraph of a
Hamiltonian cycle.

Let w count new crossing pairs on a cell transition. Let w0 count those
new pairs whose two edges both have an endpoint in column zero. Both
counts are assigned when the later edge is added. The implementation
recomputes w from edge geometry and checks it against the base weight.
A row arc is four consecutive cell transitions. Its weights are

```
W = sum_row(4w-1),    W0 = sum_row(4w0-1).
```

For each orientation separately, retain the endpoint-test data from
Section 2. Every test edge has minimum row at most the tested row and
maximum row at least that row. It is pending at row start or added during
that row. Initialise from pending edges, accumulate newly selected test
edges, and charge t=2a once at row end. Include both parity phases.

Let d2(r) and d3(r) be the final degrees in S_sigma of ghost cells
(2,r) and (3,r). These are the incoming plus newly selected edges at
those cells. Define g_r=[d2(r)=2] and z_r=[d3(r)=0]. For the first rows
put missing negative-index g values equal to zero. Define

```
cand_r = z_r * g_(r-2).
```

After row r, retain the four history bits
(cand_(r-1),cand_r,g_(r-1),g_r). Processing row r+1 emits

```
blocked(r-1) = cand_(r-1) * g_(r+1),
cand_(r+1) = z_(r+1) * g_(r-1).
```

This is exactly d3(y)=0 and d2(y-2)=d2(y+2)=2 with y=r-1. A run counter
s in {0,1,2,3,4} counts preceding emitted blocked flags, capped at four.
For a new flag b, charge k=[b=1 and s=4], and set
s_next=min(4,s+1) if b=1, or zero otherwise.

At the physical side's start use empty history and counter zero.
The first four scanned rows emit no blocked flags. Completing rows
4,...,n-1 emits exactly centre rows 2,...,n-3. No artificial final rows
are added. Thus sum k equals K_sigma exactly. The four-bit compression
is equivalent to the six raw history bits in REQUESTS.md R2: cand
stores the conjunction whose two factors are already known.

### Finite input at beta=16/11

KT Lower Bounds L4 supplies integer potentials satisfying

```
11*W + 16*W0 + 44*k - 32*t + p(u)-p(v) >= 0           (Ncert)
```

on every augmented row arc, in both orientations. Both potential ranges
are [-596,0]. The graph includes both parities and every history and
counter at row-boundary base states. Thus every actual start state of
an oriented half walk is included. Dividing the summed inequality by
44 gives, for a half of m rows,

```
sum w-m + (16/11)*(sum w0-m) + sum k
    >= (16/11)*sum a - 149/11.                        (Nhalf)
```

The Python row-level implementation reports the range above. The
independent C++ cell-level implementation confirms beta=16/11, with
all-history full-state ranges [-667,0] for up and [-687,0] for down in
units of 1/44. These broader ranges are not substituted into the exact
constant below, which uses the Python row-level range [-596,0]. The
theorem still awaits Claim 27's audit. The all-size implication uses
only (Ncert) and its range, not optimality of beta.

### Eight halves and the reduction

Split each physical side at n/2. The near half uses the up endpoint
formula; the far half uses the down formula. Both scans run in increasing
physical row order. Near parity is y modulo two and far parity is
n-1-y modulo two. Both toggle at every row. At the split retain the
actual base state, history bits, and run counter. Initialise the new
orientation's test data from pending edges at the row boundary.

The half walks partition the full strip transitions. Their crossing
weights sum exactly to sum X_sigma and sum b_sigma. Their delayed k
weights sum exactly to K, even when a flag emitted just after the split
concerns a centre row just before it. No term in Nhalf requires the row
of k to equal the row of a. The penalty totals over all half rows dominate
A, since they include every candidate endpoint and all penalties are
nonnegative. The eight errors sum to 8*(149/11)=1192/11. Therefore

```
(16/11)*A <= D0+K+(16/11)*R+1192/11,                  (N1)
(16/11)*(A-R) <= E+50558+1192/11,
A-R <= (11/16)*E+557330/16.                           (N2)
```

No crossing counted in K has been added to the square budget. Its only
use is the separate inequality N0. The boundary surplus R is the same
quantity in N1 and in Section 3, so it cancels exactly.

## 6. Conclusion, constants, and checks

The audited square budget in Section 3 is

```
4n <= 4E+2(A-R)+156.
```

Substituting N2 and multiplying by eight gives

```
32n <= 43E+558578,
43X = 172n-86+43E >= 204n-558664,
X >= 204n/43-558664/43 >= 204n/43-12993.
```

The size condition is even n>=32 throughout. It ensures the candidate
path ranges and all separation arguments used above. The numerator is
not optimised. The coefficient exceeds 52/11 by 8/473.

The following commands check all geometric and local inputs, from the
research root:

```
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_corner_box.py
python3 w-turnstheory/check_col0_squares.py
python3 w-turnstheory/check_square_defects.py
python3 w-turnstheory/check_endpoint_loss.py
python3 gap/turnstheory/check_inner_boundary.py
python3 gap/turnstheory/verify_inner_boundary.py
python3 gap/turnstheory/check_r2_history.py
python3 gap/lowerbounds/check_combo_history.py
python3 gap/lowerbounds/check_combo_obstruction.py
```

The independent history check uses the raw six-bit rule. Lower Bounds'
history check compares its compressed rule against the raw blocked
condition. Its random tests supplement the algebraic update identity;
they do not replace that identity.

The producing combined-certificate commands are below. Run from
`gap/turnstheory/`, so any generated data stay in this worker directory.
They use one orientation at a time and need the project virtual
environment. The run constant defaults to four; explicitly fixing it
prevents an inherited experimental setting from changing the task.

```
CAP=4 ../../.venv/bin/python ../lowerbounds/combo_stab.py up 16 11
CAP=4 ../../.venv/bin/python ../lowerbounds/combo_stab.py down 16 11
```

These reproduce the Python implementation. The separate C++ check can
be built and run from the research root with

```
g++ -O2 -std=c++17 gap/searcher/lower/r2.cpp -o gap/turnstheory/r2_independent
gap/turnstheory/r2_independent up cert 16 11 allhist
gap/turnstheory/r2_independent down cert 16 11 allhist
```

I read its source and the successful `crit_up_allhist.log` and
`crit_down_allhist.log` in `gap/searcher/lower/`. Each reports exact
beta=16/11 and zero violated arcs. Their full-state ranges are -667..0
and -687..0, respectively; they do not independently reproduce the
smaller Python row-level range. Claim 27 should check that range if it
retains the sharper explicit constant in this document. The interval
certificate and its separate implementation are included above.
