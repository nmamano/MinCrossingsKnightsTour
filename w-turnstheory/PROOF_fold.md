# An upper bound of 19n/3+O(1) crossings

2026-10-02. **Theorem.** Every even n>=96 has a closed knight's tour
with X<=19n/3+O(1). The certificate also gives X<=19n/3+142. Crossings
mean unordered pairs of edges whose relative interiors intersect properly;
a shared endpoint does not count.

The certificate is `check_fold_proof.py`. It uses only the Python standard
library, the twelve `w-integrator/corners/FOLD24_base_n*.json` files, and
the 36 saved `w-integrator/tours/FOLD24_n*.json` tours. It imports neither
`kt/board.py` nor any solver. Complete port lists and matchings, including
the outside matching, are in `fold_proof_checks.json`.

The all-size proof replaces long paths by their endpoint matchings. A +24
step switches between two matchings; +48 restores the matching. Both
states give one cycle. This finite two-state argument covers every size.

## 1. Exact placement rules

Choose the unique even n0 in {96,98,...,118} with n=n0+24k, k>=0. Use its
saved base file. Coordinates are integer pairs (x,y) in [0,n-1] squared,
with y increasing upwards. Write h=n/2 and R(x,y)=(n-1-y,x).

**Definition.** In each quadrant, rotate coordinates back to the bottom-left
frame. At p=(x,y) in that frame, choose out-direction (2,1) when y>x+1,
and (-1,-2) otherwise. Rotate this direction back to the board. Add the
undirected edge from each cell to its chosen neighbour when that neighbour
is on the board.

Next, in the four rotated left-edge frames, scan y=0,...,n-1. If (0,y) has
degree one and its neighbour is (2,y+s), s in {-1,1}, try to add the edge
from (0,y) to (1,y+2s). Reverse s before this operation when

    h-floor(n/4) <= y < h.

Add the edge only when the second cell is on the board, also has degree
one, and the edge is absent. These are the cheap and reversed U-turns.
The order is rotations 0,1,2,3, then increasing y, as in the checker.

Overwrite the two neighbours at each cell R^r(x,x+j), where

    r=0,1,2,3;  j=0,1,2;  11 <= x < h-11,

with the saved template entry `(r,(x-8) mod 6,j)`, rotating its two move
vectors by r. These four diagonal corridors have period six.

Finally, overwrite the cells of the thirteen saved finite components.
A component contains a base offset o and a map from relative cells q to
two move vectors. Put q at o+q+k*A, with A in the following table. Keep
its move vectors unchanged. The rows are in the JSON component order.

| Components | Translation A per +24 |
| --- | --- |
| Four ends of reversed U-turn intervals | (0,6), (6,24), (18,0), (24,18) |
| Four physical corners | (0,0), (0,24), (24,0), (24,24) |
| Four side midpoints | (0,12), (12,0), (12,24), (24,12) |
| Centre | (12,12) |

This is a definition for every k, with no solve and no component-selection
heuristic. **Finite check:** at k=0,1,2 it reproduces all 36 saved tours
exactly. The checker verifies reciprocal legal knight edges and degree
two at every cell.

**Figure 1.** Draw the n=96 board with the four diagonal and four axis
folds. In the bottom-left frame label the two directions (2,1) and
(-1,-2), and shade cells (x,x+j), j=0,1,2, of one diagonal corridor.
Mark the thirteen finite components and their translations from the table.

## 2. Growth becomes insertion in a graph of paths

**Proof.** Retain the boundary cells of depths zero and one, the diagonal
corridors, and all thirteen finite components. Suppress paths through the
remaining field cells. In one triangle such a path is straight. It can
bend at an axis fold before it returns to retained cells. It cannot cross
a diagonal fold without meeting the retained corridor. Thus each suppressed
piece crosses at most one axis fold. A complete path in the reduced graph
can still cross many triangles; the matchings below keep all its connections.

In a bottom-left triangle the constant line label is 2y-x for direction
(2,1), and 2x-y for direction (-1,-2). The parity of x, respectively y,
also stays fixed. In a left-side chevron the common label is

    c = 2y-x                 below the horizontal midline,
    c = 2(n-y)-x             above it.                       (1)

For example, an edge from (x,h-1) to (x+2,h) has label 2h-2-x on both
sides. The directions on its two arms are (2,1) and (-2,1). The other
three chevrons are rotations of this one. These formulas cover all four
diagonal folds and all four axis folds.

Use these two block types, with integer half-open label intervals:

| Type | Region and label | Base interval |
| --- | --- | --- |
| Corner | bottom-left quadrant, c=max(2x-y,2y-x) | 24 <= c < 30 |
| Side | left half-board, c=2 min(y,n-y)-x | h+16 <= c < h+22 |

Rotate each block four ways. The eight blocks are disjoint. For size
n=n0+24k, replace their width 6 by width 6+12k. Keep the corner lower cut
at 24 and the side lower cut at h+16. Each knight edge changes either
label by at most five, so no edge jumps across a whole six-label block.

Here is the explicit map of the reduced graph outside these growing blocks.
Along each edge frame, the five retained pieces, in order from one physical
corner to the other, shift by

    0, 6k, 12k, 18k, 24k

in their edge coordinate; their depths do not change. These pieces are
separated by the two corner blocks and the two arms of the side block.
On each diagonal corridor, the piece before the corner block stays fixed;
the piece after it translates by (12k,12k) in its quadrant frame. All
finite components have exactly the translations in Section 1.

The map preserves every retained move and corridor phase: 12k is a multiple
of six. It also preserves each suppressed field connection. To see this
directly, solve 2y-x=c or 2x-y=c at the two ends of a straight arm, retaining
the parity just stated. A corner arm has the same increment 12k in its line
label at both ends. For an outer side arm, (1) increases by 12k at both
ends: the lower end shifts 6k and the upper end shifts 18k while n shifts
24k. For the inner side arms, both ends of (1) increase by 24k. These
increments preserve parity. At the fold the two formulas in (1) agree.
The lengths of the arms can change, but their ends cannot change.

The same calculation at the fixed-component ports uses their translations
from Section 1. Component shapes and the relative cut margins are fixed;
checking the margins at n0 therefore checks them for every k. A field
piece cannot hide a cycle: its straight arms are monotone, and a chevron
has monotone y through its single axis fold. Every such piece ends at
retained cells. This also accounts for the new cells in the growing
triangle interiors, whose number is quadratic in n.

Consequently the reduced graph for n0+24k is exactly the base outside
graph with each of the eight blocks replaced by 1+2k primitive blocks.
This is a geometric insertion identity, not an inference from several
successful board sizes. **Finite checks** verify the complete outside
matching at k=0,1,2, the cut margins through the explicit block extraction,
and the block phase after translation by six labels.

**Figure 2.** In the bottom-left quadrant shade 24<=max(2x-y,2y-x)<30.
At the left side shade h+16<=2 min(y,n-y)-x<h+22. Trace one straight
arm and one chevron through the axis fold. Beside them draw their
suppressed paths and show a six-label block becoming three blocks at +24.

## 3. Complete block matchings and the two states

A port is an edge cut by a block boundary. Trace every path inside the
block and pair its two ports. Also check that every block cell occurs in
one of those paths. Write Li and Ri for port i at the lower and upper cuts.

To number ports, orient a crossing edge from lower to higher label. Sort
by its region tag, the two depths, and the two label offsets from the cut.
For a corner, tags are B (bottom), D (diagonal), L (left); a diagonal depth
is y-x. For a side, tags are hi and lo for its two arms, and depth is x.
The exact sorted lists for every phase are included in the JSON report.

**Finite check.** There are just three matching types:

| Block type | Full matching, including returns |
| --- | --- |
| Corner, four ports per cut | L0-R0, L1-R1, L2-R2, L3-R3 |
| Corner, six ports per cut | L0-R5, L1-R1, L2-L5, L3-R3, L4-R4, R0-R2 |
| Side, four ports per cut | L0-R1, L1-R2, L2-R3, L3-R0 |

For the six-port corner, both possible phase lists have the same matching.
They differ only in the offsets of diagonal port 4. The checker records
that difference; it does not identify ports only by a path count.

**Proof from the table.** Every corner matching M is idempotent, with no
closed component on composition. In the six-port case, the first copy's
R0-R2 return joins the second copy's L2-L5 return into the continuing
L0-R5 path; the three other through paths and the two outer returns persist.
Thus M^j=M for every j>=1. The side matching is the permutation
rho=[1,2,3,0], of order four. It has no return path and composition cannot
create a hidden closed component. Hence after 1+2k primitive blocks, the
side matching is rho for even k and rho cubed for odd k.

The outside graph is fixed by Section 2. **Finite check:** for each of the
twelve base files, its union with either of these two block states has
one cycle. The checker verifies this both on the finite matching graphs and on the
full tours at n0 and n0+24, and records the complete outside matching. It traces every outside cell,
so an extra component with no port cannot be missed. The composition
checks also account for every intermediate port. Therefore both states
give a single cycle for all k, proving the one-cycle claim for all n.

A +24 step adds two primitive side blocks and switches rho with rho
cubed. A +48 step adds four and restores the matching. Step 12 cannot
replace step 24: it gives the other powers, and the n0=100 completion at
n=112 has three cycles. The checker verifies this failure as well.

**Figure 3.** Draw the three matching rows in the table, with every port
label shown. For the six-port corner, draw two copies joined at R_i=L_i;
highlight how R0-R2 and L2-L5 become part of L0-R5, with no closed loop.
For the side, draw rho and rho cubed beside the fixed outside matching.

## 4. Crossings are local

**Proof.** Pure straight fields and their free folds have no proper
crossings. At a free fold the two directions change the defining normal
coordinate by the same unit step. Each family remains on its own side of
the fold, with common boundary contacts only at shared endpoints. Therefore
only the boundary bands, diagonal corridors, and fixed neighbourhoods of
the finite components can contribute crossings.

A crossing depends on two knight edges within bounded distance. Away from
the fixed components, the local boundary pattern repeats when its label
increases by six; the corridor pattern repeats under (x,y)->(x+6,y+6).
The inserted blocks preserve these phases at both joins. All remaining
crossing neighbourhoods are translated copies of base neighbourhoods.

**Finite local count:** assign a crossing to the least label among its
four endpoints. In one six-label interval the counts are:

| Primitive block | Boundary crossings | Corridor crossings | Total |
| --- | ---: | ---: | ---: |
| Each corner block | 6 | 4 | 10 |
| Each side block | 9 | 0 | 9 |

The checker counts proper intersections by exact integer orientation tests,
including pairs whose edges extend across a cut. It checks each phase and
the enlarged intervals. The intervals have fixed joins, so these local
counts prove the exact increment for every k:

    X(n+24)-X(n) = 4*2*10 + 4*2*9 = 152
                 = 120 boundary + 32 corridor.

For n=n0+24k this proves

    X(n)=X(n0)+152k=(19/3)n + [X(n0)-(19/3)n0].

There are only twelve base sizes, so the bracket is O(1). The checker
also verifies that its maximum is 142. This proves the theorem.

**Figure 4.** Draw one primitive corner block and one side block. Mark
crossing pairs by the least endpoint label, including pairs crossing a
cut. Label their counts 6+4 and 9. Show eight blocks receiving two copies
each, giving 4*2*10+4*2*9=152 crossings per 24 added rows and columns.

## 5. Reproduction and scope of the finite certificate

Run from the project root:

```sh
python3 w-turnstheory/check_fold_proof.py
```

The check passed on 2026-10-02. It rebuilt and compared all 36 saved tours;
checked legal reciprocal degree-two edges and one cycle; extracted all
block paths and all outside paths; checked both corner return matchings,
the side permutation, and their compositions; counted the local crossings
and all full-board crossings; and checked the step-12 failures. It writes
`fold_proof_checks.json`; the run output is `fold_proof_checks.txt`.
The coordinate and line-label argument in Section 2 is the all-n part of
the proof. Finite testing alone would not establish that part.

**Figure 5.** A proof diagram: explicit placement -> eight block matchings
plus the fixed outside matching -> two connected states -> one tour for
every n; the local count supplies the coefficient 152/24=19/3.
