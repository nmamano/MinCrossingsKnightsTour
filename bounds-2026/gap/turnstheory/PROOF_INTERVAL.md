# Claim 27 submission: crossings in a blocked interval

2026-10-03. **Local lemma with an exact certificate; submitted for
independent audit.** The certificate passed a separate implementation
check. The combined-credit strip inequality is not proved here.

## Statement

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

## Certificate and proof

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

## How a tour forces these intervals

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

## Separate crossing budget for four sides

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

## Reproduction

From the research root:

```
python3 gap/turnstheory/check_inner_boundary.py
python3 gap/turnstheory/verify_inner_boundary.py
```

The generator writes `gap/turnstheory/inner_boundary_certificate.json`.
The checker loads that file and builds the state graph with the separate
`w-lowerbounds/strip_dp.py` implementation, relaxing only its boundary
degree rule in memory. It does not change the source file. Both commands
use exact integers and no solver.

The certificate proves only (1)–(2). Condition (4), the application to
tours, and the disjoint-set count giving (5) are the mathematical
arguments above. A future finite certificate for the combined-credit
inequality must be checked separately.
