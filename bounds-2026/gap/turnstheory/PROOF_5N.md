# Five crossings per side length from quarter payments and strip stability

2026-10-03. **AUDITED — Claims 39, 40 and its scalar addendum, 42.**
Every closed knight tour on an n by n board, for even n>=32, satisfies

    X >= 5n-612.

The proof is computer-assisted, with an independent reconstruction
of its finite certificate. Claim 42 checks both orientations and the
common-state interface used below. No price lemma remains open for
this bound. The proof is not a formal proof-assistant verification
and does not assert the same certificate for disconnected 2-factors.

## 1. Tiles and the exact excess identity

The vertices are V={0,...,n-1} squared. H is a connected simple graph
of degree two whose edges have coordinate differences of absolute
values one and two. It has n^2 edges. X counts unordered edge pairs
whose relative interiors cross properly; shared endpoints do not count.

The tile of a knight edge is the parallelogram with that edge as long
diagonal and the unit grid edge of the same midpoint as short diagonal.
For (0,0)--(2,1), its vertices are (0,0),(1,0),(2,1),(1,1). Its area
is one and it stays within its endpoint box. Divide each unit square
in D=[0,n-1]^2 by both diagonals into four open quarter triangles.
Each tile consists of four quarters.

The audited geometric lemma states that two tiles overlap in positive
area exactly when their edges cross properly. The overlap then has
one or two quarters. The check enumerates four unoriented moves for
one edge and the other edge's translated endpoint in [-4,4]^2; the
tile coordinate span of at most two makes this sufficient.

Let m(q) be the tile multiplicity at quarter q. A quarter is bad if
m(q)!=1. Let G count holes (m=0), and let X1 count crossing pairs with
one-quarter overlap. Define

    W3 = sum_q W3(q),
    W3(q) = binom(m(q)-1,2) if m(q)>=1, and 0 if m(q)=0.

There are 4n^2 tile incidences and 4(n-1)^2 board quarters, so

    sum_q (m(q)-1)_+ = 8n-4+G.

At each covered quarter,
`binom(m,2)=(m-1)+binom(m-1,2)`. Counting pair incidences therefore gives

    2X-X1 = sum_q binom(m(q),2) = 8n-4+G+W3.

Thus, with E=X-4n+2,

    E = (G+X1+W3)/2.                               (1)

This is an exact identity, with no omitted boundary term.

## 2. Flux, candidate paths and endpoint tests

Set chi(x,y)=(-1)^(x+y). Orient tour edges and unit grid edges from
chi=1 to chi=-1. On a directed step of the grid of square centres,
let omega be their total signed crossing flux. If a is the endpoint
of the crossed unit grid edge on the left of the step and m_+,m_-
are the adjacent quarter multiplicities, the audited local identity is

    omega = chi(a)*(m_++m_-+1) modulo three.         (2)

For completeness the exact tour contribution is
`chi(a)*(m_++m_--3g)`, where g counts tiles with the crossed grid edge
as short diagonal. Adding the unit grid contribution gives (2).
The identity is linear in selected knight edges and is checked one
edge at a time. Around any finite vertex set A, the total flux is
`sum_(v in A) chi(v)*(deg_H(v)+4)=6 sum_(v in A) chi(v)`, hence zero
modulo three. One can verify the boundary identity by replacing each
knight edge by its three unit lattice steps and telescoping.

A path is charged if its flux is nonzero modulo three. A charged path
has a bad adjacent quarter by (2). Moreover, each tile occupies two
adjacent quarters in any square it meets, so the four multiplicities
satisfy m_B-m_R+m_T-m_L=0. A bad square has at least two bad quarters.

At each corner, use coordinates increasing into the board and take
integer radii 12<=r<=n/2-4. The candidate is the dual path

    (r+1/2,3/2) -> (r+1/2,r+1/2) -> (3/2,r+1/2).

Its square coordinates are (r,j) and (j,r), 1<=j<=r. Candidates are
vertex-disjoint: their maximum corner coordinate fixes r, and the
four corner boxes are separated. Their total number is N=2n-60.

In a side frame (inward depth x, row y), translate the tested row to
zero. The UP endpoint quantity F is the sum of these coefficients
on selected edges:

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

Let e=1 if both (0,0)--(2,1) and (0,1)--(2,0) are present. The UP
test passes when e=0 and F=2 modulo three. Reflect the entire geometry
by y -> -y for the DOWN test, including the square containing the
endpoint: square row r reflects to -r-1. Always use the orientation
and row of the actual candidate end, not an unshifted reflected row.

For c=(-1)^r the endpoint residue in its corner frame is

    h=(1+c)/2+c*(F+2) modulo three.

The endpoint lemma follows by summing the eight listed edge
coefficients: the tour contribution through the two omitted end
steps is c*(F+deg_H(0,r))=c*(F+2). Their grid contributions cancel;
the outer side contributes sum_(j=0)^r (-1)^j=(1+c)/2. Applying the
zero-circulation identity to the corner square proves that a candidate
is charged when h_left+h_bottom is nonzero.

Retain a candidate if both endpoint exceptions are absent and the
sum of its two residues is nonzero. Let L be the retained count and
D_loss=N-L. Two passing endpoint tests give h=2 at both ends and
therefore imply retention. Every lost candidate has a failed end test.

Let B be the union of crossing-pair sets whose two edges both touch
depth zero of the same board side. The audited overlap check shows
that such a pair can reach the depth-one square only as the exception
pair above, or its reflected copy, and cannot reach deeper squares.
It follows that B overlaps avoid every retained candidate's squares.

## 3. Quarter payments and deficient paths

For each side sigma, let S_sigma contain all tour edges with an
endpoint at depth zero or one from that side. Let S* be the UNION of
crossing-pair sets within these four edge sets, and put

    s=|S*|,     T=s-4n+2.

Define a capacity nu with separate atoms as follows: one half unit
for each crossing pair outside S*, one quarter unit for each hole,
one quarter unit for each X1 pair, and one quarter unit for each W3
unit at its quarter. These atom types are separate even if they refer
to the same physical crossing. By (1),

    nu(total)=(X-s)/2+E/2=E-T/2,
    E+580=nu(total)+(T+1160)/2.                     (3)

Call a bad quarter payable unless its multiplicity is exactly two
and its unique covering pair is in S* with a TWO-quarter overlap.
The following rule pays any set of distinct payable quarters at
one quarter unit each:

* A hole uses its own atom.
* A quarter with m>=3 uses one W3 unit at that quarter.
* A quarter with m=2 and pair outside S* uses one quarter of that
  pair's half-unit capacity. A pair covers at most two quarters.
* A quarter with m=2 and pair in S* uses its X1 atom. This pair covers
  exactly one quarter in this case.

No atom is overused. This is the Claim 39 packing kernel. On different
candidate paths the selected quarters are distinct, so the payments
are simultaneous. Locality, though not needed for this scalar proof,
also holds: every covering edge endpoint is within distance 3/2 of
the square centre, and every quarter within distance 1/2.

Let s_i count payable quarters on retained path i. Call it deficient
when s_i<=1, and write L_def for this count. Every other retained path
has two payable quarters, hence

    nu(total) >= (L-L_def)/2.                       (4)

No payments on deficient paths are needed. For comparison with the
previous H1 formulation, d_i=(2-min(2,s_i))/4, so deficiency is exactly
d_i>0. Since strip tiles reach at most depth three, a bad square at
depth at least three from every side is fully payable. Such a square
would give two payable quarters. Every deficient path thus has a good
middle, including the earlier conservative depth-at-least-four middle.

## 4. Visibility pays deficient paths

In an UP side frame, VIS(r) holds if a crossing pair in S_sigma, not
both edges touching depth zero, has a two-quarter overlap with a
quarter in a square (x,r), x in {1,2,3}. Reflect this whole definition
for the DOWN endpoint geometry. Put g=1 if the actual oriented test
fails OR VIS holds, and g=0 otherwise.

**Visibility lemma.** Every deficient retained candidate has an end
with VIS. Proof: it is charged, hence has a bad square. That square
has two bad quarters, but the entire path has at most one payable
quarter. It therefore contains an unpaid quarter. Its covering pair
is in S* with two-quarter overlap, and is outside B by retention.

A side-strip tile reaches depth at most three, so the overlap lies
at square depth at most two from that side. A candidate square has
coordinates (r,j) or (j,r). Since r>=12, the only possible side is
the side at that arm's endpoint, and j is one or two. The opposite
board sides are at depth at least n-2-r>=n/2+2. The pair therefore
belongs to the correct S_sigma and satisfies VIS at the endpoint
row. This proves the lemma for ALL candidate radii, including r<=32.
There is no small-radius allowance in this proof.

Every lost candidate has a failed end test. Choose one such end for
each lost candidate, and one visible end for each deficient retained
candidate. A side row can belong to at most one candidate: in a fixed
side scan the near and far index intervals are [12,n/2-4] and
[n/2+3,n-13], with the endpoint square convention reflected as above.
Thus all chosen side rows are distinct. If G_strong is the total g
count over the four sides with their proper half orientations, then

    G_strong >= D_loss+L_def.                       (5)

## 5. The finite strong strip certificate

Each S_sigma is a proper subgraph of the connected tour, so it is a
forest. Its vertices in columns zero and one have degree two; those
in columns two and three have degree at most two.

Scan cells in increasing (row,column) order. Record pending selected
edges and the partition of their ends into paths. Select forward
edges to satisfy the degree requirements, reject degree overflow and
closed cycles, and shift row coordinates after column three. Reachable
states from the empty board boundary form a finite graph since edges
span at most two rows. A transition weight w counts newly introduced
proper crossings once. A full side walk has 4n transitions and total
weight X_sigma, the crossings within S_sigma.

Use the independent Claim 42 augmentation: retain the full selected-
edge mask for the current row. There are 20 possible strip edges
meeting that row. The mask keeps edges removed during row processing
and includes newly introduced edges. Evaluate the endpoint test and
VIS at row end, then reset the mask. Both orientations use this SAME
state graph. Admit every base row-boundary state as a start; this
covers arbitrary actual half-side boundary states. No parity bit is
needed, since the strong test does not depend on row parity.

The base graph has 82,516 states and 144,674 arcs. The full-mask graph
has 184,006 states and 343,631 arcs. A crossing is counted when the
later of its two lower endpoints is processed. The full mask preserves
the geometry needed for both tests: UP at row r uses square row r,
whereas DOWN uses square row r-1. The independent geometry check
verifies that the seven DOWN visibility pairs are exactly the
reflections of the seven UP pairs.

**Finite strong-test certificate (Claim 42, independently checked).**
There are integer potentials h_up and h_down on this common graph,
with ranges [-29,0] and [-33,0], respectively. In either orientation,
every arc satisfies

    4w-1-4g+h(u)-h(v) >= 0.                        (6)

Here g is charged only at row end. The checker verifies every arc
inequality after exact integer relaxation to a fixed point, reached
after 41 passes in each orientation. It ALSO verifies at every row
boundary the interface inequality

    -4 <= h_up-h_down <= 4.                        (7)

This is an additional finite input. Reflection alone would not
justify equal potential ranges or this interface bound.

Split each physical side at row n/2, using UP for the first half and
DOWN for the second. Keep pending edges, crossing ownership and the
common state at the cut. Let a,m,z be the start, middle and end states.
The two sums of (6) telescope to

    4(X_sigma-n-G_sigma)
      >= h_up(m)-h_up(a)+h_down(z)-h_down(m)
      >= -4-33 = -37.

The last step uses (7), h_up(a)<=0 and h_down(z)>=-33. It permits
arbitrary boundary states. Summing the four physical sides yields

    G_strong <= sum_sigma X_sigma-4n+37.

Adding separate half-side widths would instead give error 62. That
weaker calculation does not give the constant stated here; the
checked common-state interface is essential to this presentation.

A pair counted in two adjacent strips has both edges in their 4 by 4
corner square. There are 24 possible knight edges in that square.
Opposite strips share no edges for the stated size range. Thus

    sum_sigma X_sigma-s <= 4*binom(24,2)=1104.

Consequently, since T=s-4n+2,

    G_strong <= s-4n+1141 = T+1139 <= T+1160.       (8)

We keep the looser final number to match the stated theorem. The
forest condition is where Hamiltonian connectivity enters the proof.

## 6. Conclusion

Insert (4), (5) and (8) into (3):

    E+580 >= (L-L_def)/2+(D_loss+L_def)/2
          = (L+D_loss)/2 = (2n-60)/2 = n-30.

Since X=E+4n-2, this proves the stated bound

    X >= 5n-612, for even n>=32.

For smaller positive even n, the same bound follows from X>=0,
since 5n-612 is negative. The direct geometric proof above applies
for n>=32.

The reserve and quarter capacities are distinct terms of the exact
identity (3). No crossing is charged twice outside that identity.
No residual matching, Hall condition, clean-run error, height mismatch,
or general ribbon classification is required.

## 7. Reproduction and Pareto profile

Run from the research root. The decisive independent reconstruction
and geometry checks are

```
OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim42_check.py
.venv/bin/python gap/verifier/claim42_geometry.py
```

The first imports prior VERIFIER forest and exact polygon routines,
not the author's graph, endpoint accumulator, VIS or potential code.
It checks both full potential arrays and their common-state interface.
The second checks the boundary exception, visibility geometry,
pending-edge attribution and candidate geometry. Evidence is in
`gap/verifier/claim42_check.json`, `claim42_check.log`,
`claim42_potential_up.npy`, `claim42_potential_down.npy`,
`claim42_geometry.json` and `claim42_sources.json` (all under the same
folder). Potential digests and source hashes are included in the
saved audit record. Audit reasoning is in w-verifier/FINDINGS.md,
Claims 39, 40 and its scalar addendum, and 42.

The inherited local checks and quarter kernel are reproduced by

```
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_corner_box.py
python3 w-turnstheory/check_col0_squares.py
python3 gap/turnstheory/check_quarter_payment_support.py
python3 gap/verifier/claim39_check.py
```

The boundary-square checker also checks an older boundary-count
lemma, which this proof does not use. The exact identity (1) follows
from its displayed hand calculation; saved-tour checks are checks
of implementation, not its proof.

For comparison, the author implementation can be run separately:

```
(cd gap/lowerbounds && ../../.venv/bin/python f1v_stab.py cert 1 1 up)
(cd gap/lowerbounds && ../../.venv/bin/python f1v_stab.py cert 1 1 down)
```

To regenerate its rate search and saved potentials, replace
`cert 1 1` by `crit 2` in each command. Its UP and DOWN graphs use
2,095,620 and 4,191,240 arcs. DOWN carries previous-row VIS as a bit.
Those separate potential ranges alone prove the weaker constant 614;
use the independent common-state check for the interface in (7).
Optimality of rate one and periodic SAT checks are not proof inputs.

**Pareto profile (2026-10-03).** Approximately six short hand-proof
pages, depending on layout, plus one narrow-strip graph certificate.
The new hand work is one bad-square argument, distinct-row counting,
the potential join and the exact ledger. Finite input sizes are:

| Input | Size | Measured time / scope |
| --- | --- | --- |
| Tile and flux geometry | 1,292 edge-pair tests; 648 single-edge flux tests | Together with the next two small checks, about 1 second in the writing-time run |
| Endpoint coefficient identity | Eight contributing edges | Same combined run |
| Quarter support | Four moves, 16 quarters | Same combined run |
| Claim 42 geometry | One boundary exception, seven VIS pairs per orientation; every candidate for even n=32..258 | Separate runtime not recorded here |
| Strong strip certificate | 82,516 base states / 144,674 arcs; 184,006 mask states / 343,631 arcs; two integer potential arrays and their interface | About 22 seconds, one process, independent audit on 2026-10-03 |

The 22-second figure is the Verifier's recorded rebuild and certificate
check time, not a new rerun during this document update. The small
writing-time checks passed on 2026-10-03. Runtime is machine-dependent.
The geometric enumeration is backed by the stated bounded-support
arguments, and the candidate size check is backed by the general
coordinate proof. No new SAT/DRUP lemma, wide-strip model, Gap Lemma,
private flux allocation or Hall augmentation is needed. This is a
complete audited computer-assisted proof of the stated bound.
