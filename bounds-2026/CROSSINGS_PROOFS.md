# Appendix: full proofs

[Code and certificate data](https://github.com/nmamano/MinCrossingsKnightsTour/tree/master/bounds-2026) are available in the public source repository.

The two proofs below include their finite certificates and the commands to check them. Run every command from the bounds-2026 folder of the repository. The geometric arguments explain why the finite checks cover every board size; testing a list of tours alone would not suffice.

## A. Full proof: tours with at most `19n/3 + 142` crossings

**Theorem.** Every even `n>=96` has a closed knight's tour with `X<=19n/3+O(1)`. The certificate also gives `X<=19n/3+142`. Crossings mean unordered pairs of edges whose relative interiors intersect properly; a shared endpoint does not count.

The certificate is `check_fold_proof.py`. It uses only the Python standard library, the twelve `w-integrator/corners/FOLD24_base_n*.json` files, and the `36` saved `w-integrator/tours/FOLD24_n*.json` tours. It imports neither `kt/board.py` nor any solver. Complete port lists and matchings, including the outside matching, are in `w-turnstheory/fold_proof_checks.json`, which the command generates.

The all-size proof replaces long paths by their endpoint matchings. A `+24` step switches between two matchings; `+48` restores the matching. Both states give one cycle. This finite two-state argument covers every size.

### A.1. Exact placement rules

Choose the unique even `n0` in `{96,98,...,118}` with `n=n0+24k`, `k>=0`. Use its saved base file. Coordinates are integer pairs `(x,y)` in `[0,n-1]` squared, with `y` increasing upwards. Write `h=n/2` and `R(x,y)=(n-1-y,x)`.

Use rotation index `r=0,1,2,3` on the bottom-left, bottom-right, top-right, and top-left quadrants, respectively. The left and bottom halves have coordinates less than `h`; the other halves have coordinates at least `h`. Rotating back means applying `R^(-r)`.

**Definition.** In each quadrant, rotate coordinates back to the bottom-left frame. At `p=(x,y)` in that frame, choose out-direction `(2,1)` when `y>x+1`, and `(-1,-2)` otherwise. Rotate this direction back to the board. Add the undirected edge from each cell to its chosen neighbour when that neighbour is on the board.

Next, in the four rotated left-edge frames, scan `y=0,...,n-1`. If `(0,y)` has degree one and its neighbour is `(2,y+s)`, `s` in `{-1,1}`, try to add the edge from `(0,y)` to `(1,y+2s)`. Reverse `s` before this operation when

`h-floor(n/4) <= y < h.`

Add the edge only when the second cell is on the board, also has degree one, and the edge is absent. These are the cheap and reversed U-turns. The order is rotations `0,1,2,3`, then increasing `y`, as in the checker.

Overwrite the two neighbours at each cell `R^r(x,x+j)`, where

`r=0,1,2,3;  j=0,1,2;  11 <= x < h-11,`

with the saved template entry `(r,(x-8) mod 6,j)`, rotating its two move vectors by `r`. These four diagonal corridors have period six.

Finally, overwrite the cells of the thirteen saved finite components. A component contains a base offset `o` and a map from relative cells `q` to two move vectors. Put `q` at `o+q+k*A`, with `A` in the following table. Keep its move vectors unchanged. The rows are in the JSON component order.

| Components | Translation `A` per `+24` |
| --- | --- |
| Four ends of reversed U-turn intervals | `(0,6)`, `(6,24)`, `(18,0)`, `(24,18)` |
| Four physical corners | `(0,0)`, `(0,24)`, `(24,0)`, `(24,24)` |
| Four side midpoints | `(0,12)`, `(12,0)`, `(12,24)`, `(24,12)` |
| Centre | `(12,12)` |

This is a definition for every `k`, with no solve and no component-selection heuristic. **Finite check:** at `k=0,1,2` it reproduces all `36` saved tours exactly. The checker verifies reciprocal legal knight edges and degree two at every cell.

**Finite checks for this section:**

```sh
python3 w-turnstheory/check_fold_proof.py
```

### A.2. Growth becomes insertion in a graph of paths

**Proof.** Retain the boundary cells of depths zero and one, the diagonal corridors, and all thirteen finite components. Suppress paths through the remaining field cells. In one triangle such a path is straight. It can bend at an axis fold before it returns to retained cells. It cannot cross a diagonal fold without meeting the retained corridor: the corridor contains the three integer transverse positions `y-x=0,1,2`, while a knight step changes `y-x` by at most three. The finite components cover the corridor ends and the central junction. Thus each suppressed piece crosses at most one axis fold. A complete path in the reduced graph can still cross many triangles; the matchings below keep all its connections.

In a bottom-left triangle the constant line label is `2y-x` for direction `(2,1)`, and `2x-y` for direction `(-1,-2)`. The parity of `x`, respectively `y`, also stays fixed. In a left-side chevron the common label is

`c = 2y-x` below the horizontal midline,

`c = 2(n-y)-x` above it. (1)

For example, an edge from `(x,h-1)` to `(x+2,h)` has label `2h-2-x` on both sides. The directions on its two arms are `(2,1)` and `(-2,1)`. The other three chevrons are rotations of this one. These formulas cover all four diagonal folds and all four axis folds.

Use these two block types, with integer half-open label intervals:

| Type | Region and label | Base interval |
| --- | --- | --- |
| Corner | bottom-left quadrant, `c=max(2x-y,2y-x)` | `24 <= c < 30` |
| Side | left half-board, `c=2 min(y,n-y)-x` | `h+16 <= c < h+22` |

Rotate each block four ways. The eight blocks are disjoint. For size `n=n0+24k`, replace their width `6` by width `6+12k`. Keep the corner lower cut at `24` and the side lower cut at `h+16`. Each knight edge changes either label by at most five, so no edge jumps across a whole six-label block.

Here is the explicit map of the reduced graph outside these growing blocks. Along each edge frame, the five retained pieces, in order from one physical corner to the other, shift by

`0, 6k, 12k, 18k, 24k`

in their edge coordinate; their depths do not change. These pieces are separated by the two corner blocks and the two arms of the side block. On each diagonal corridor, the piece before the corner block stays fixed; the piece after it translates by `(12k,12k)` in its quadrant frame. All finite components have exactly the translations in Section `A.1`.

The map preserves every retained move and corridor phase: `12k` is a multiple of six. It also preserves each suppressed field connection. To see this directly, solve `2y-x=c` or `2x-y=c` at the two ends of a straight arm, retaining the parity just stated. A corner arm has the same increment `12k` in its line label at both ends. For an outer side arm, `(1)` increases by `12k` at both ends: the lower end shifts `6k` and the upper end shifts `18k` while `n` shifts `24k`. For the inner side arms, both ends of `(1)` increase by `24k`. These increments preserve parity. At the fold the two formulas in `(1)` agree. The lengths of the arms can change, but their ends cannot change.

The same calculation at the fixed-component ports uses their translations from Section `A.1`. Put `h0=n0/2`. The corner upper cut is `30+12k = h-(h0-30) <= h-18`. The side upper cut is `h+22+12k = n-(h0-22) <= n-26`. In a corner block, `max(2x-y,2y-x) >= max(x,y)`, so the block stays away from the quadrant axes. In a left-side block, the lower cut `h+16` implies `x <= h-16`, so this block stays away from the diagonal corridor. The rotated bounds are the same. For each copied component cell, the board coordinates and cut labels are affine functions of `k`. Each required separation from a forbidden block is nonnegative at `k=0` and has nonnegative coefficient of `k`. Thus each separation stays nonnegative for every `k >= 0`. The component shapes stay fixed, but some separations increase. A field piece cannot hide a cycle: its straight arms are monotone, and a chevron has monotone `y` through its single axis fold. Every such piece ends at retained cells. This also accounts for the new cells in the growing triangle interiors, whose number is quadratic in `n`.

Consequently the reduced graph for `n0+24k` is exactly the base outside graph with each of the eight blocks replaced by `1+2k` primitive blocks. This is a geometric insertion identity, not an inference from several successful board sizes. **Finite checks** verify the complete outside matching at `k=0,1,2`, the cut margins through the explicit block extraction, and the block phase after translation by six labels.

**Finite checks for this section:**

```sh
python3 w-turnstheory/check_fold_margins.py
python3 w-turnstheory/check_fold_proof.py
```

### A.3. Complete block matchings and the two states

A port is an edge cut by a block boundary. Trace every path inside the block and pair its two ports. Also check that every block cell occurs in one of those paths. Write `Li` and `Ri` for port `i` at the lower and upper cuts.

To number ports, rotate the block to its bottom-left or left reference frame. Write a cut edge as `(u,v)` with the label of `u` less than the label of `v`. Its name is `(tag, depth(u), depth(v), label(u)-cut, label(v)-cut)`. Sort names lexicographically and number them from zero, separately at each cut. For a corner, use tag `L` if both endpoint x coordinates are at most two, otherwise `B` if both endpoint y coordinates are at most two, and otherwise `D`. The corresponding depths are x, y, and `y-x`. For a side, use tag `lo` if the lower-label endpoint has `y<h`, and `hi` otherwise; its depth is x. The complete sorted lists are in `w-turnstheory/fold_proof_checks.json`.

**Finite check.** There are just three matching types:

| Block type | Full matching, including returns |
| --- | --- |
| Corner, four ports per cut | `L0-R0`, `L1-R1`, `L2-R2`, `L3-R3` |
| Corner, six ports per cut | `L0-R5`, `L1-R1`, `L2-L5`, `L3-R3`, `L4-R4`, `R0-R2` |
| Side, four ports per cut | `L0-R1`, `L1-R2`, `L2-R3`, `L3-R0` |

For the six-port corner, both possible phase lists have the same matching. They differ only in the offsets of diagonal port `4`. The checker records that difference; it does not identify ports only by a path count.

**Proof from the table.** Every corner matching `M` is idempotent, with no closed component on composition. In the six-port case, the first copy's `R0-R2` return joins the second copy's `L2-L5` return into the continuing `L0-R5` path; the three other through paths and the two outer returns persist. Thus `M^j=M` for every `j>=1`. The side matching is the permutation `rho=[1,2,3,0]`, of order four. It has no return path and composition cannot create a hidden closed component. Hence after `1+2k` primitive blocks, the side matching is `rho` for even `k` and `rho` cubed for odd `k`.

The outside graph is fixed by Section `A.2`. **Finite check:** for each of the twelve base files, its union with either of these two block states has one cycle. The checker verifies this both on the finite matching graphs and on the full tours at `n0` and `n0+24`, and records the complete outside matching. It traces every outside cell, so an extra component with no port cannot be missed. The composition checks also account for every intermediate port. Therefore both states give a single cycle for all `k`, proving the one-cycle claim for all `n`.

A `+24` step adds two primitive side blocks and switches `rho` with `rho` cubed. A `+48` step adds four and restores the matching. Step `12` cannot replace step `24`: it gives the other powers, and the `n0=100` completion at `n=112` has three cycles. The checker verifies this failure as well.

**Finite checks for this section:**

```sh
python3 w-turnstheory/check_fold_proof.py
```

### A.4. Crossings are local

**Proof.** Pure straight fields and their free folds have no proper crossings. At an axis fold, use the integer coordinate normal to that axis. At a diagonal fold, use `y-x` in its local frame. Each relevant field edge changes that coordinate by one unit in the same direction on both sides of the fold. Within each open unit slab all field edges are parallel. Edges in different slabs have disjoint interiors in that coordinate and can meet on a slab boundary only at endpoints. Thus the free fold has no proper crossing. Therefore only the boundary bands, diagonal corridors, and fixed neighbourhoods of the finite components can contribute crossings.

A crossing depends on two knight edges within bounded distance. Away from the fixed components, the local boundary pattern repeats when its label increases by six; the corridor pattern repeats under `(x,y)->(x+6,y+6)`. The inserted blocks preserve these phases at both joins. All remaining crossing neighbourhoods are translated copies of base neighbourhoods.

**Finite local count:** assign a crossing to the least label among its four endpoints. In one six-label interval the counts are:

| Primitive block | Boundary crossings | Corridor crossings | Total |
| --- | ---: | ---: | ---: |
| Each corner block | `6` | `4` | `10` |
| Each side block | `9` | `0` | `9` |

The checker counts proper intersections by exact integer orientation tests, including pairs whose edges extend across a cut. It checks each phase and the enlarged intervals. The intervals have fixed joins, so these local counts prove the exact increment for every `k`:

`X(n+24)-X(n) = 4*2*10 + 4*2*9 = 152`

`= 120 boundary + 32 corridor.`

For `n=n0+24k` this proves

`X(n)=X(n0)+152k=(19/3)n + [X(n0)-(19/3)n0].`

There are only twelve base sizes, so the bracket is `O(1)`. The checker also verifies that its maximum is `142`. This proves the theorem.

**Finite checks for this section:**

```sh
python3 w-turnstheory/check_fold_proof.py
```

### A.5. Reproduction and scope of the finite certificate

Run from the bounds-2026 folder of the repository:

```sh
python3 w-turnstheory/check_fold_proof.py
```

The check passed on `2026-10-02`. It rebuilt and compared all `36` saved tours; checked legal reciprocal degree-two edges and one cycle; extracted all block paths and all outside paths; checked both corner return matchings, the side permutation, and their compositions; counted the local crossings and all full-board crossings; and checked the `step-12` failures. It writes `w-turnstheory/fold_proof_checks.json` and prints its checks to standard output. It also checks the affine component margins and writes `w-turnstheory/fold_margin_checks.json`. The coordinate and line-label argument in Section `A.2` is the all-n part of the proof. Finite testing alone would not establish that part.

## B. Full proof: every tour has at least `5n - 597` crossings, including the `4n - 2` tile bound

For every even `n >= 32`, every closed knight's tour on an `n x n` board has at least `5n - 597` proper crossing pairs.

The same bound holds for every spanning simple knight 2-factor: a set of disjoint cycles that together visit every cell. Count all crossing pairs, including pairs whose moves belong to different cycles.

The proof uses exact tile geometry and a finite strip certificate. The [cut-state checker](gap/lowerbounds/simple_strip/check_cut_certificate.py) has 3,136 states and 48,510 arcs. An [independent checker](gap/verifier/claim50_check.py) rebuilds the graph and checks every potential inequality. The tile bound `4n - 2` is also proved in Lean; the stronger bound here is computer-assisted, not a Lean theorem.

### B.1. Tiles and one scalar count

Put the cells at `V={0,...,n-1}^2`. The graph `H` has degree two at every cell, so it has `n^2` edges. Let `X` count proper unordered crossing pairs; shared endpoints do not count. Put `E=X-4n+2`.

The tile of an edge is the parallelogram with that edge as its long diagonal and the unit grid edge of the same midpoint as its short diagonal. For `(0,0)--(2,1)`, its vertices are `(0,0),(1,0),(2,1),(1,1)`. It lies in the endpoint box and consists of four quarter triangles obtained by cutting unit squares along both diagonals.

Two tiles overlap exactly when their edges cross properly, in one or two quarters. The tile checker in B.7 checks four unoriented moves and the second edge's endpoint in `[-4,4]^2` relative to the first. Tile spans are at most two, so that box includes every possible overlap.

All quarter sums are over the `4(n-1)^2` quarters of board squares. Let `m(q)` be the full graph's tile multiplicity and `X1` count pairs with one-quarter overlap. Define:

```text
D = sum_q [binom(m(q),2)-m(q)+1].
```

The summand is 1 at `m=0`, zero at `m=1,2`, and at least 1 at `m>=3`. Counting tile and pair incidences gives:

```text
D = (2X-X1)-4n^2+4(n-1)^2 = 2E-X1,
D+X1=2E.                                           (1)
```

In particular, `E>=0`, which proves `X>=4n-2`.

For each side `sigma`, let `S_sigma` be the graph edges touching vertex depth zero or one. Let `S` be the union of crossing-pair sets within the four strips, `s=|S|`, and `T=s-4n+2`. A quarter is bad if `m!=1`. Call it _usable_ unless `m=2` and its unique covering pair belongs to `S` with a two-quarter overlap.

For any set `Q` of usable bad quarters, those with `m=0` or `m>=3` number at most `D`. At `m=2`, a pair outside `S` accounts for at most two quarters; a pair in `S` must have one-quarter overlap. Thus:

```text
|Q| <= D+2(X-s)+X1 = 4E-2T.                        (2)
```

### B.2. Charge and bad squares

Set `chi(x,y)=(-1)^(x+y)`. Orient the graph edges and all unit edges of the infinite square lattice from `chi=1` to `chi=-1`. On a directed step between square centres, let `omega` be their signed flux from its left to its right.

Let `a` be the endpoint of the crossed grid edge on the left, `m_+,m_-` the adjacent quarter multiplicities, and `k` the number of tiles having that edge as short diagonal. The graph contribution is `chi(a)*(m_++m_--3k)`. Adding the grid contribution gives:

```text
omega = chi(a)*(m_++m_-+1) modulo three.             (3)
```

The tile checker verifies this linear identity one edge at a time. For a finite vertex set `A` contained in the board, the total boundary flux is `sum_(v in A) chi(v)*(deg_H(v)+4)=6 sum_(v in A) chi(v)`, hence zero modulo three. Replace each knight edge by its three unit lattice steps in crossing order and telescope the endpoint indicators of `A` to obtain the boundary formula. All corner vertex sets below are contained in the board.

A path with nonzero flux modulo three is charged. Equation (3) forces a bad quarter in a square centred on that path. Each tile occupies two adjacent quarters in every square it meets, so the four multiplicities obey `m_B-m_R+m_T-m_L=0`. A bad square therefore has at least two bad quarters.

### B.3. The endpoint test and strong rows

Use side coordinates `(inward depth x, scan row y)`. Translate the tested vertex row to zero. Let `F` be the sum of these coefficients on selected edges:

| Edge | Coefficient |
| --- | ---: |
| `(0,-1)--(1,1)` | `-1` |
| `(0,0)--(1,-2)` | `-1` |
| `(0,0)--(2,-1)` | `-1` |
| `(0,1)--(1,-1)` | `+1` |
| `(0,1)--(2,0)` | `+1` |
| `(0,2)--(1,0)` | `-1` |
| `(1,0)--(2,2)` | `-1` |
| `(1,1)--(2,-1)` | `-1` |

The up test passes if `F=2 mod 3` and the edges `(0,0)--(2,1)` and `(0,1)--(2,0)` are not both present. This pair is the endpoint exception.

`VIS` holds if two strip edges, not both touching depth zero, have a two-quarter overlap meeting a square `(x,0)` with `x` in `{1,2,3}`. A row is _strong_ if the test fails or `VIS` holds. Reflect the whole definition by `y -> -y` for the down test. Thus down at vertex row `r` uses square row `r-1`. Let `b` count strong rows using up in the first half of each physical side and down in the second half.

The graph flux through the two omitted end steps of a corner box, divided by `c=(-1)^r`, equals `F+deg_H(0,r)=F+2`. Subtracting the eight displayed coefficients from the edge flux coefficients leaves exactly the degree at `(0,r)`. The endpoint checker in B.7 verifies this identity in both directions.

The unit-grid contributions on those two steps cancel. Along each outer side the grid contribution is `(1+c)/2`, and no graph edge crosses the boundary outside the board. When both endpoint values equal two modulo three, the complementary boundary flux is:

```text
1+c*(F_left+F_bottom+5) = 1 modulo three.            (4)
```

The internal corner path is therefore charged.

### B.4. Keep only paths with two non-strong ends

At each corner, take all radii `12<=r<=n/2-4` and the paths:

```text
(r+1/2,3/2) -> (r+1/2,r+1/2) -> (3/2,r+1/2).
```

Their square coordinates are `(r,j)` and `(j,r)`, with `1<=j<=r`. Different radii have different maximum coordinates, and the four corner boxes are disjoint. There are `N=2n-60` candidates.

Keep those with neither end strong. Write `M=N-z`, where `z` is the discarded count. Each discarded path chooses one strong end. On each side the near and far vertex-row intervals are `[12,n/2-4]` and `[n/2+3,n-13]`. Each row belongs to at most one candidate, so `z<=b`.

Each kept path is charged by (4) and supplies two bad quarters in one square. These quarters are usable. A strip tile reaches vertex depth at most three, so its open quarters have square depth at most two. A candidate with `r>=12` can be this close only to its own endpoint side, at the endpoint row. Opposite-side depths are at least `n-2-r>=n/2+2`.

A two-quarter strip pair meeting the path is either `VIS` or, if both edges touch depth zero, the endpoint exception. The exception is the only outer-column pair whose overlap reaches square depth one, and it does not reach depth two. Either case would make the end strong. The exception check in B.7 verifies this enumeration; the independent strip checker derives both `VIS` lists from tile geometry.

Different kept paths have distinct squares. Apply (2) to their `2M` usable quarters:

```text
4E >= 2M+2T.                                      (5)
```

### B.5. The cut-state strip certificate

For a side, `S_sigma` has degree two in columns 0 and 1 and degree at most two in columns 2 and 3. Cycles are allowed. Scan whole rows. A cut state is the selected edges with lower endpoint below the current row and upper endpoint in or above it. There are twelve possible pending edges.

A row arc selects all edges starting in that row, subject to those degree constraints and future endpoint loads at most two. Remove edges ending at the row and translate coordinates by one. The actual board begins and ends with the empty cut. Following its rows maps the strip to the graph reachable from the empty state, including its middle state.

The incoming set together with new edges contains all edges meeting the row, so both strong flags are functions of a row arc. No parity or component labels are needed. An arc weight `w` counts new/pending crossings and unordered new/new crossings. An older edge that crosses a new one is still pending; otherwise it ends below the new edge. Each crossing is counted once, and the `n` weights sum to `X_sigma`. The same state and crossing ownership are kept at the orientation change.

The reachable graph has 3,136 states and 48,510 arcs. Integer potentials `h_up` in `[-24,0]` and `h_down` in `[-28,0]` satisfy:

```text
4w-4-4g+h(u)-h(v) >= 0 on every row arc,
0 <= h_up-h_down <= 4 on every state.              (6)
```

Here `g` is the strong-row indicator in the chosen orientation. Exact relaxation from zero at all states stabilizes in eight passes per orientation. A final pass checks every inequality. The independent checker derives the seven `VIS` pairs per orientation and reproduces the graph, both potentials and their interface.

Split at row `n/2`. For start, middle and end states `a,m,z`, sum (6):

```text
4(X_sigma-n-b_sigma)
 >= h_up(m)-h_up(a)+h_down(z)-h_down(m) >= -28.
```

Thus `b<=sum_sigma X_sigma-4n+28`. A pair counted in two adjacent strips has both edges in their `4 x 4` corner square, which has 24 possible knight edges. Opposite strips share no edges for `n>=32`. The total overcount is therefore at most `4*binom(24,2)=1104`, giving:

```text
b <= s-4n+1132 = T+1130,
T >= b-C,                    C=1130.               (7)
```

### B.6. Add the counts

Combine (5), (7), `M=N-z` and `z<=b`:

```text
4E >= 2(N-z)+2T >= 2N-2C.
X = E+4n-2 >= 5n-(32+C/2) = 5n-597.
```

The constant is `C=28+1104-2=1130`. For smaller positive even `n`, the same numerical bound follows from `X>=0`.

Every hand step uses degree two, and the strip certificate allows cycles. The proof therefore applies to spanning simple knight 2-factors as well. The tile and flux sums must include all edges, and `X` must include crossings between different cycles.

### B.7. Reproduction

Run from the repository's `bounds-2026` folder:

```sh
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_corner_box.py
python3 w-turnstheory/check_square_defects.py
.venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py
python3 gap/verifier/claim50_check.py
python3 gap/verifier/claim52_check.py
```

The small checks cover tile overlap, local flux, endpoint coefficients and the square identity. The author cut-state checker needs NumPy and writes its two potential arrays under `gap/lowerbounds/simple_strip/`. It uses no solver or component labels.

The independent Claim 50 checker uses only the Python standard library and repository fixtures. It checks the graph and derives both `VIS` lists without importing the author's code. The Claim 52 checker rechecks the outer-column exception and the 2-factor case. On 2026-10-03, the author certificate took 5.38 seconds and the independent certificate took 8.51 seconds in the audit run.

The [standalone proof](gap/turnstheory/PROOF_5N_V2.md) and [audit report](gap/verifier/claim52_report.md) give the same argument and its checks.
