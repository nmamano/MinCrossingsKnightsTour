# Boundary crossing credit gives 52n/11-O(1)

2026-10-03. **AUDITED — Claim 26, PASS.** KT Verifier checked the full
proof and independently rebuilt the finite certificate. The two Section
4 wording repairs requested by the audit are applied below. This is a
Python-certified mathematical proof for closed Hamiltonian tours; no
Lean theorem or extension to disconnected two-factors is claimed.

**Theorem.** For every even `n>=32`, a closed knight tour on an `n` by `n`
board has at least

```
X >= 52n/11 - 360
```

proper crossing pairs. In particular the leading coefficient
is `52/11`, which exceeds `14/3` by `2/33`.

The change is to retain the actual number of outer-boundary crossings
in the area budget. These crossings pay for some endpoint losses as well
as for the basic boundary term. The argument uses the same corner paths
and local tile geometry as the audited 14/3 proof.

## Exact changes to the audited proof

The reference document is `w-turnstheory/PROOF_crossings_lower.md`.
The complete argument below includes the unchanged inputs, so the
reader can follow the proof without combining different drafts.

| Reference section | Change in this proof |
| --- | --- |
| 1. Tiles turn crossings into an area budget | No change. Its inequality (1), with the actual set B, is used here as (2). |
| 2. A nonzero colour flux forces two bad quarters | No change. The flux and two-quarter argument appear in Section 1 below. |
| 3. A local endpoint test forces a corner charge | Keep the eight-edge flux identity and the same paths. Replace the binary joint test by exact endpoint residues and fractional penalties, defined and proved in Section 2 below. |
| 4. Boundary crossings avoid the path squares | Keep B and the overlap exclusion. Retention still excludes the exceptional pair. Keep the actual boundary count and its surplus R instead of substituting 4n-O(1). Section 3 gives the new inequality and exact union error 20. The old width-one potential is no longer needed for the leading-bound argument. |
| 5. Strip stability pays for failed endpoint tests | Replace the binary joint-test certificate by the two oriented boundary-credit certificates (10), each with both parities. Use eight half walks and the common error 53/4. Section 4 includes the state and parity details. |
| 6. Count paths and conclude | Keep the count 2n-60 and the strip overcount 1104. Replace binary loss by A, retain R, and apply (12)–(13). Section 5 obtains c=360 for every even n>=32. |
| 7. One command checks every finite input | Replace the old runner with `gap/turnstheory/check_52_11.py`. The command list below names every component. |

The size range, the definition of proper crossings, and the restriction
to Hamiltonian tours are unchanged. No assertion about disconnected
two-factors is added.

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

## 4. Finite strip certificate with boundary credit

Let `S_sigma` contain all selected edges with an endpoint at depth zero
or one of side sigma. Its endpoints have depths zero through three.
It is a forest, since it is a proper subgraph of a Hamiltonian cycle.
Columns zero and one have degree exactly two; columns two and three
have degree at most two. Let `X_sigma` count its crossing pairs.

Scan rows increasingly, and columns zero through three within each row.
A state records the next column, the selected pending edges from
processed to future cells, and the partition of their pending ends into
paths. The transition chooses only legal knight edges to later cells that have an endpoint in column zero or one. It meets the stated degree rule and rejects cycle closure and excess future degrees. Canonical
component labels and relative row coordinates make the state set finite.
Start at the empty state. There are 82,516 reachable base states and
144,674 arcs in the separate checker.

For each transition let `w` count all introduced crossings. Let `w0`
count the introduced crossings whose two edges both touch column zero.
All crossings are counted exactly once, at the addition of the later
edge. A past edge that is already complete cannot properly cross a new
edge. The checker recomputes `w` from the geometry and confirms its
agreement with the base transition weight before it computes `w0`.

Augment the state by the selected endpoint-test edges seen so far in
the row and a parity bit. At row start, initialise the test set from
pending edges; add newly introduced test edges during the row. Every test edge has minimum row at most the tested row and maximum row at least the tested row. It is therefore pending at row start or is selected during that row. At row end
charge `t=2a`, reset the test set, and toggle parity. Both possible
initial parities are included at every base state at a row boundary.
Separate graphs use up and down test data.

The new finite certificate has an integer potential `p` such that

```
3*(4w-1)+4*(4w0-1)-8*t+p(u)-p(v) >= 0.               (10)
```

Here `t=0` except at row end. The up potential lies in `[-155,0]`; the
down potential lies in `[-159,0]`. These ranges and every arc inequality
are established by exact integer relaxation to a fixed point. A
separate implementation confirms both results. The weaker common range
`[-159,0]` suffices below.

On any oriented half walk with `m` complete rows, divide the sum of
(10) by twelve. This gives

```
sum w - m + (4/3)*(sum w0-m)
    >= (4/3)*sum a - 53/4.                            (11)
```

Split each side at its middle row. Use the up graph for the near half
and the down graph for the far half, in the SAME increasing physical
scan direction. On the far half set parity to `n-1-y` modulo two,
where `y` is the physical scan row; it still toggles at each row. This
is the local radius parity required by (5). Arbitrary initial parity and
arbitrary base row-boundary states are included by the checker, so the
half-walk start is valid. The first and last edges of a half walk retain
their states and assigned crossing weights; no graph is cut and rebuilt.

The eight halves partition every transition of the four whole-side
walks. Thus their `w` totals sum to `sum X_sigma`, and their `w0` totals
sum to `sum b_sigma`. Their row totals sum to `4n`. Their penalty sum
includes all candidate endpoint penalties and perhaps additional
nonnegative penalties. Put `D0=sum X_sigma-4n`. Summing (11) yields

```
(4/3)*(A-R) <= D0+106.                                (12)
```

If a pair is counted in two adjacent width-two strips, both edges lie
in their four-by-four corner square. That square has 24 possible knight
edges, so the total strip overcount is at most
`4*binomial(24,2)=1104`. Opposite strips share no edge. Consequently

```
D0 <= X+1104-4n = E+1102.
A-R <= (3/4)*(E+1208) = 3E/4+906.                     (13)
```

The forest rule is where Hamiltonian connectivity enters this argument.
No claim for arbitrary disconnected two-factors is made.

## 5. Conclusion and reproduction

Insert (13) into (9):

```
4n <= 4E+2(A-R)+156 <= (11/2)*E+1968.
E >= 8n/11-3936/11.
X >= 52n/11-3958/11 >= 52n/11-360.
```

The coefficient gain is `52/11-14/3=2/33`. The constant was chosen for
a simple uniform certificate error; it is not optimised.

Run all local checks and both independent strip certificates with

```
python3 gap/turnstheory/check_52_11.py
```

The runner uses one process at a time, asserts convergence and the exact
potential ranges, and writes its report and logs only under
`gap/turnstheory/`. The local geometry commands come from the audited
proof. The penalty-pair check comes from old Section 11. The new strip
command is `gap/lowerbounds/r1_independent.py`, which imports neither
`r1_stab.py` nor its transfer-graph implementation.

These are every component command, from the research root:

```
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_corner_box.py
python3 w-turnstheory/check_col0_squares.py
python3 w-turnstheory/check_square_defects.py
python3 w-turnstheory/check_endpoint_loss.py
python3 gap/turnstheory/check_boundary_credit.py
python3 gap/lowerbounds/r1_independent.py up 4 3
python3 gap/lowerbounds/r1_independent.py down 4 3
```

The runner also checks the 24-edge corner enumeration and all constants
with exact rational arithmetic. `check_col0_squares.py` checks the old
width-one potential as well as the needed overlap facts; that potential
is extra verification, not a new assumption of this proof.

The separate producer implementation can be checked with the following
commands. Its numerical graph uses the project virtual environment.

```
.venv/bin/python gap/lowerbounds/r1_stab.py up 4 3
.venv/bin/python gap/lowerbounds/r1_stab.py down 4 3
```

The producer checks are not required in addition to the independent
runner. KT Lower Bounds ran that implementation, and its logs are listed
in `gap/lowerbounds/FINDINGS.md`, L3. All required component checks passed
on 2026-10-03. The report is `gap/turnstheory/check_52_11_report.json`.

Claim 26 checked the actual-set budget (8)–(9), the far-half parity and
state treatment in (11), and the cancellation of `R` in (12)–(13), as
well as every finite input. Its consolidated-document verdict confirms
the exact numerator 3958 used here and the rounded constant 360. The
audit also derives the optional sharper numerator 3954 by using the
separate orientation errors. This document retains its checked common
error and constants. The audit record is in `w-verifier/FINDINGS.md`,
under Claim 26 and its consolidated-document verdict.
