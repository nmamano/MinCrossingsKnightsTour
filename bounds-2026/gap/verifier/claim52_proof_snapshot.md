# A short proof of 5n-597 crossings

2026-10-03. Assembled from the audited hand argument (Claim 51) and
cut-state certificate (Claim 50); this consolidated text is submitted
for review. This replaces the private-payment and forest machinery
of PROOF_5N.md by a scalar count and a degree-only strip certificate.

**Theorem.** Every closed knight tour on an n by n board, for even
n>=32, has at least `5n-597` proper unordered crossing pairs.

**2-factor theorem — pending Claim 52.** The same bound holds for
every spanning simple knight 2-factor, counting crossing pairs from
different cycles as well as from the same cycle.

## 1. Tiles and one scalar count

The board vertices are `{0,...,n-1}^2`. A knight edge has coordinate
spans one and two. The graph has degree two and therefore n^2 edges.
Let X count proper crossings; shared endpoints do not count. Put
`E=X-4n+2`.

The tile of an edge is the parallelogram with that edge as its long
diagonal and the unit grid edge of the same midpoint as its short
diagonal. For `(0,0)--(2,1)` its vertices are
`(0,0),(1,0),(2,1),(1,1)`. It lies in the endpoint box and consists of
four quarter triangles obtained by cutting unit squares along both
diagonals. Two tiles overlap exactly when their edges cross properly,
in one or two quarters. This finite geometry is checked by the tile
command in Section 7; the second edge need only range over [-4,4]^2
relative to the first because tile spans are at most two.

All quarter sums below are over the 4(n-1)^2 quarters of board squares.
Let m(q) be full-graph tile multiplicity and X1 count pairs with
one-quarter overlap. Define

```
D = sum_q [binom(m(q),2)-m(q)+1].
```

The summand is 1 at m=0, zero at m=1,2, and at least 1 at m>=3.
Tile and pair incidences give

```
D = (2X-X1)-4n^2+4(n-1)^2 = 2E-X1,
D+X1=2E.                                           (1)
```

In particular E>=0, proving the tile bound X>=4n-2.

For each physical side sigma let S_sigma be the graph edges touching
vertex depth zero or one. Let S be the UNION of crossing-pair sets
within these four strips, s=|S|, and T=s-4n+2. A quarter is bad if
m!=1. Call it usable unless m=2 and its unique covering pair belongs
to S with a two-quarter overlap.

For any set Q of usable bad quarters, those with m=0 or m>=3 number
at most D. At m=2, a pair outside S accounts for at most two quarters;
a pair in S must have one-quarter overlap. Thus

```
|Q| <= D+2(X-s)+X1 = 4E-2T.                        (2)
```

## 2. Charge and bad squares

Set `chi(x,y)=(-1)^(x+y)`. Orient both graph edges and unit grid edges
from chi=1 to chi=-1. On a directed step between unit-square centres,
let omega be their signed flux from its left to its right. If a is
the endpoint of the crossed grid edge on the left, m_+,m_- the adjacent
quarter multiplicities and k the number of tiles having that edge
as short diagonal, the graph contribution is
`chi(a)*(m_++m_--3k)`. Adding the grid contribution gives

```
omega = chi(a)*(m_++m_-+1) modulo three.             (3)
```

The tile checker verifies the linear one-edge identity. Around a
finite vertex set A, the total flux is
`sum_(v in A) chi(v)*(deg(v)+4)=6 sum_(v in A) chi(v)`, hence zero
modulo three. To see the boundary formula, replace each knight edge
by its three unit lattice steps in crossing order and telescope the
endpoint indicators of A.

A path with nonzero flux modulo three is charged. Equation (3) forces
a bad quarter in a square centred on that path. Each tile occupies
two adjacent quarters in every square it meets, so the square's four
multiplicities obey `m_B-m_R+m_T-m_L=0`. A bad square therefore has
at least two bad quarters.

## 3. The endpoint test and strong rows

Use side coordinates (inward depth x, scan row y). Translate the tested
vertex row to zero. Let F be the sum of these coefficients on selected
edges:

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

The UP test passes if F=2 modulo three and the pair
`(0,0)--(2,1), (0,1)--(2,0)` is absent. VIS holds if two strip edges,
not both touching depth zero, have a two-quarter overlap meeting a
square (x,0) with x in {1,2,3}. A row is strong if the test fails OR
VIS holds. Reflect this whole definition by y -> -y for DOWN. Thus
DOWN at vertex row r uses square row r-1. Let b be the total strong-row
count using UP in the first half of each physical side and DOWN in
the second half.

The endpoint identity is that the graph flux through the two omitted
end steps of a corner box, divided by c=(-1)^r, equals F+deg(0,r)=F+2.
It follows by subtracting the displayed eight coefficients from the
edge flux coefficients; the remainder is exactly the degree at (0,r).
The unit-grid contributions on these two steps cancel. Along each
outer side the grid contribution is `(1+c)/2`, and no graph edge
crosses the boundary outside the board. Hence when both endpoint
F values equal two modulo three, the complementary boundary flux is

```
1+c*(F_left+F_bottom+5) = 1 modulo three.           (4)
```

The internal corner path is therefore charged. The endpoint checker
in Section 7 verifies the coefficient identity in both directions.

## 4. Keep only paths with two non-strong ends

At each corner take all radii 12<=r<=n/2-4 and the paths

```
(r+1/2,3/2) -> (r+1/2,r+1/2) -> (3/2,r+1/2).
```

Their square coordinates are (r,j) and (j,r), 1<=j<=r. Different radii
have different maximum coordinates; the four corner boxes are disjoint.
There are N=2n-60 paths. Keep those with neither end strong. Write
M=N-z, where z is the discarded count. Each discarded path chooses
one strong end. On each side the near and far vertex-row intervals
are [12,n/2-4] and [n/2+3,n-13], and each row belongs to at most one
candidate. Therefore z<=b.

Each kept path is charged by (4) and supplies two bad quarters in one
square. These quarters are usable. Indeed a strip tile reaches vertex
depth at most three, so an overlap lies at square depth at most two.
A candidate with r>=12 can be this close only to its own endpoint
side, at the endpoint row; opposite-side square depths are at least
n-2-r>=n/2+2. A two-quarter strip pair meeting the path is either VIS
or, if both edges touch depth zero, the endpoint exception. The latter
is the only outer-column pair whose overlap reaches square depth one,
and it does not reach depth two. Either case would make the end strong.
The exact exception/VIS enumeration is part of the independent strip
check in Section 7.

Different kept paths have distinct squares. Applying (2) to their
2M usable quarters gives

```
4E >= 2M+2T.                                      (5)
```

## 5. The cut-state strip certificate

For a side, S_sigma has degree two in columns 0,1 and at most two in
columns 2,3. It need not be a forest. Scan whole rows. A cut state is
the selected edges with lower endpoint below the current row and
upper endpoint in or above it. There are twelve possible pending
edges. A row arc selects all edges starting in that row, subject to
those degree constraints and future endpoint loads at most two.
Remove edges ending at the row and translate coordinates by one.

The actual board begins and ends with the empty cut. Induction through
its rows maps the strip to the graph reachable from the empty state,
including its actual middle state. The incoming set union new edges
contains all edges meeting that row, so both strong flags are row-arc
functions. No separate parity or component state is required.

An arc weight w counts new/pending crossings and unordered new/new
crossings. An older edge that crosses a new one is still pending;
otherwise it ends below the new edge. Thus each crossing is counted
once, and the n arc weights sum to X_sigma. The same pending state
and crossing ownership are preserved at the orientation change.

**Finite certificate (Claim 50).** The reachable graph has 3,136
states and 48,510 arcs. Integer potentials h_up in [-24,0] and h_down
in [-28,0] satisfy, on every row arc in the respective orientation,

```
4w-4-4g+h(u)-h(v) >= 0,
0 <= h_up-h_down <= 4 on every state.              (6)
```

Here g is the strong-row indicator. Exact relaxation from zero at all
generated states stabilizes in eight passes per orientation; a final
pass checks every inequality. An independent implementation derives
both VIS lists from tile geometry and reproduces the graph, potentials
and interface. Both orientations have seven VIS pairs.

Split at row n/2. For start, middle and end states a,m,z, telescoping
(6) gives

```
4(X_sigma-n-b_sigma)
 >= h_up(m)-h_up(a)+h_down(z)-h_down(m) >= -28.
```

Therefore b<=sum_sigma X_sigma-4n+28. A pair counted in two adjacent
strips has both edges in their 4 by 4 corner square. That square has
24 possible knight edges. Opposite strips share no edges for n>=32;
hence their total overcount is at most `4*binom(24,2)=1104`. It follows
that

```
b <= s-4n+1132 = T+1130,
T >= b-C,                    C=1130.               (S)
```

## 6. Conclusion

Combine (5), (S), M=N-z and z<=b:

```
4E >= 2(N-z)+2T >= 2N-2C.
X = E+4n-2 >= 5n-(32+C/2) = 5n-597.
```

This uses C=28+1104-2=1130 without rounding up the audited constants.
For smaller positive even n, the same numerical bound follows from
X>=0. Every hand step uses only degree two; the separate 2-factor
statement above remains marked pending Claim 52 as requested.

## 7. Reproduction

Run from the research root (`bounds-2026` in the public repository):

```sh
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_corner_box.py
python3 w-turnstheory/check_square_defects.py
.venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py
python3 gap/verifier/claim50_check.py
```

The author cut-state checker needs NumPy and writes its two potential
arrays under `gap/lowerbounds/simple_strip/`. The independent Claim 50
checker needs only the Python standard library; it checks the strip
certificate and exact exception/VIS geometry without author imports.
The small checks cover tile overlap, local flux, endpoint coefficients
and the square identity. Claims 50 and 51 contain the audit arguments.
