<details id="proof-crossings-lower">
<summary>B. Full proof: every tour has at least <code>5n - 612</code> crossings, including the <code>4n - 2</code> tile bound</summary>

For every even `n >= 32`, every closed knight's tour on an `n x n` board has at least `5n - 612` proper crossing pairs. The proof uses exact tile geometry and a finite strip certificate. An independent program rebuilds the strip graph and checks every integer potential inequality, including the join between its two orientations.

The tile bound `4n - 2` is also proved in Lean as `KT.ClosedTour.four_mul_sub_two_le_numCrossings`. The `5n - 612` bound here is computer-assisted, not a Lean theorem. With the project's Lean toolchain and dependencies installed, its existing theorem statements and axioms can be checked with:

```sh
(cd ktlean && lake env lean Axioms.lean)
```

Run the commands below from the repository's `bounds-2026` folder. Commands using `.venv/bin/python` use the research virtual environment. The independent strip checker needs NumPy. The author checker `f1v_stab.py` needs NumPy and OR-Tools: it imports `ortools.sat.python.cp_model` through its geometry helpers, although this certificate does not run a SAT solver. Other imports are Python standard-library or repository modules.

### B.1. Tiles and the exact excess identity

Put the cell centres at `V={0,...,n-1}^2`. The tour `H` is a connected simple degree-two graph on `V`. Each edge has coordinate differences of absolute values 1 and 2, and there are `n^2` edges. Let `X` count unordered pairs whose relative interiors cross properly. Shared endpoints do not count.

The tile of an edge is the parallelogram whose long diagonal is that edge and whose short diagonal is the unit grid edge with the same midpoint. For `(0,0)--(2,1)`, its vertices are `(0,0),(1,0),(2,1),(1,1)`. Its area is one. It stays in the endpoint box, hence inside `D=[0,n-1]^2`.

Divide each unit square into four open quarter triangles along its diagonals. Every tile consists of four quarters. Two tiles overlap in positive area exactly when their edges cross properly; their overlap then has one or two quarters. Tiles sharing an edge endpoint have no area overlap.

This finite geometric fact is checked for four unoriented moves and the second edge's endpoint in `[-4,4]^2`. Each tile has coordinate span at most two, so the box includes every possible overlap:

```sh
python3 w-turnstheory/check_knight_tiles.py
```

Let `m(q)` be the multiplicity of quarter `q`. A quarter is bad if `m(q) != 1`. Let `G` count holes, `X1` count crossing pairs with one-quarter overlap, and define:

```text
W3 = sum_q W3(q)
W3(q) = binom(m(q)-1,2) if m(q)>=1, and 0 if m(q)=0.
```

There are `4n^2` tile incidences and `4(n-1)^2` quarters in the board. Therefore:

```text
sum_q (m(q)-1)_+ = 8n-4+G.
```

At each covered quarter, `binom(m,2)=(m-1)+binom(m-1,2)`. Counting pair incidences in two ways gives:

```text
2X-X1 = sum_q binom(m(q),2) = 8n-4+G+W3.
E := X-4n+2 = (G+X1+W3)/2.                         (1)
```

All terms on the right are nonnegative, so `X >= 4n - 2`. This area argument also holds for a spanning 2-factor; it does not use connectivity. Identity (1) has no omitted boundary term.

### B.2. Colour flux forces a bad square

Put `chi(x,y)=(-1)^(x+y)`. Orient tour edges and unit grid edges from `chi=1` to `chi=-1`. The internal dual grid has the unit-square centres as vertices. For a directed dual step, let `omega` be the total signed flux of these oriented edges from the step's left to its right.

Let `a` be the endpoint of the crossed unit grid edge on the left of the step. Let `m_+,m_-` be the two adjacent quarter multiplicities, and let `g` count tiles whose short diagonal is that grid edge. The tour contribution is `chi(a)*(m_++m_--3g)`. Adding the unit grid contribution gives:

```text
omega = chi(a)*(m_++m_-+1) modulo three.             (2)
```

The formula is linear in selected knight edges. The tile checker above verifies it one edge at a time, in both dual directions.

For a finite set of board vertices `A`, orient its dual boundary with `A` on the left. Replace each knight edge by its three unit lattice steps in the same crossing order. For displacement `(2,1)`, these steps are horizontal, vertical, horizontal; signs and transposition handle the other moves. Their signed boundary crossings telescope to the difference of the endpoint indicators of `A`. Summing tour and grid edges gives:

```text
integral_(boundary A) omega
  = sum_(v in A) chi(v)*(deg_H(v)+4)
  = 6 sum_(v in A) chi(v).
```

Thus internal dual loops have zero flux modulo three. A path is charged if its flux is nonzero modulo three. By (2), a charged path has a bad adjacent quarter in a square centred on one of its vertices.

Every tile occupies two adjacent quarters in each square it meets. Consequently the four multiplicities satisfy `m_B-m_R+m_T-m_L=0`. A bad square has at least two bad quarters. The finite square check is:

```sh
python3 w-turnstheory/check_square_defects.py
```

### B.3. Corner candidates and endpoint tests

At each corner use coordinates increasing into the board. For every integer radius `12<=r<=n/2-4`, take the dual path:

```text
gamma_r: (r+1/2,3/2) -> (r+1/2,r+1/2) -> (3/2,r+1/2).
```

Its square coordinates are `(r,j)` and `(j,r)` for `1<=j<=r`. Different radii have different maximum coordinates, and the four corner boxes are separated. Thus all candidates are vertex-disjoint. Their total number is `N=2n-60`.

For a side, use coordinates `(inward depth, scan row)`. Translate a tested row to zero. The up endpoint quantity `F` is the sum of these coefficients on selected edges:

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

The exception is the simultaneous presence of `(0,0)--(2,1)` and `(0,1)--(2,0)`. The up test passes if the exception is absent and `F=2 mod 3`. Reflect the entire definition by `y -> -y` for the down test. This sends square row zero to square row minus one. The test and the square row must both be reflected.

With `c=(-1)^r`, the endpoint residue in the corner frame is:

```text
h = (1+c)/2+c*(F+2) modulo three.                   (3)
```

To obtain (3), enclose the corner cells `[0,r]^2` by their dual boundary. The tour flux through the two omitted steps at an end is `c*(F+deg_H(0,r))=c*(F+2)`. Their grid contributions cancel. The outer side contributes `sum_(j=0)^r (-1)^j=(1+c)/2`. Transposition gives the other end. The full boundary has zero flux modulo three, so a nonzero sum of the two endpoint residues forces the internal path to be charged.

Retain a candidate if both exceptions are absent and its two residues have nonzero sum. Write `L` for the retained count and `D_loss=N-L`. A passing endpoint test gives `h=2` for either parity. Hence two passing tests imply retention, and every lost candidate has a failed test at an end.

The endpoint coefficient identity is checked by:

```sh
python3 w-turnstheory/check_corner_box.py
```

Let `B` be the union, over the four sides, of crossing pairs whose two edges both touch depth zero of that side. There is just one such pair whose overlap reaches positive square depth at up row `r`:

```text
(0,r)--(2,r+1), (0,r+1)--(2,r).
```

It is the excluded exception pair. Its overlap reaches square depth one, but not two. Reflect for the down end. Thus overlaps from `B` avoid all retained path squares. The exact enumeration checks this fact:

```sh
.venv/bin/python gap/verifier/claim42_geometry.py
```

The same check verifies the side-depth argument and candidate geometry for every even `n` from 32 through 258. The coordinate argument above proves disjointness and the count for every even `n>=32`; the finite size checks are additional checks of the implementation.

### B.4. Quarter payments

For each side `sigma`, let `S_sigma` contain all tour edges with an endpoint at depth zero or one. Let `S*` be the union of the crossing-pair sets within these four edge sets. Put `s=|S*|` and `T=s-4n+2`.

Define a nonnegative capacity `nu` with separate items:

- `1/2` for each crossing pair outside `S*`;
- `1/4` for each hole;
- `1/4` for each one-quarter crossing pair;
- `1/4` for each unit of `W3(q)` at its quarter.

These are distinct terms even when they refer to the same physical crossing. By (1):

```text
nu(total) = (X-s)/2+E/2 = E-T/2,
E+580 = nu(total)+(T+1160)/2.                       (4)
```

A bad quarter is _payable_ except when it has multiplicity exactly two and its unique covering pair is in `S*` with a two-quarter overlap. Any set of distinct payable quarters can receive `1/4` each:

- A hole uses its own quarter unit.
- A quarter with multiplicity at least three uses one of its `W3` units.
- At multiplicity two with the pair outside `S*`, use `1/4` of the pair's half unit. The pair covers at most two quarters, so it receives at most two requests.
- At multiplicity two with the pair in `S*`, the payable case has one-quarter overlap. Use that pair's one-quarter unit, which receives only this request.

No capacity is exceeded. The rule holds simultaneously for any distinct quarters, including quarters on different candidate paths. If locality is needed, every covering edge endpoint is within distance `3/2` of the square centre. The support check and independent payment check are:

```sh
python3 gap/turnstheory/check_quarter_payment_support.py
python3 gap/verifier/claim39_check.py
```

Let `s_i` count payable quarters on retained path `i`. Call it _deficient_ when `s_i<=1`, and write `L_def` for the deficient count. Every other retained path has two payable quarters. Since candidate squares are distinct, the payment rule gives:

```text
nu(total) >= (L-L_def)/2.                           (5)
```

A strip edge's tile reaches depth at most three, so its open quarters have square depth at most two. A bad square at depth at least three from every side is therefore fully payable and pays its path in full. Deficient paths have a good middle; their bad squares lie near their ends.

### B.5. A visible side overlap pays a deficient path

In an up side frame, `VIS(r)` holds if two edges of `S_sigma`, not both touching depth zero, form a crossing pair with two-quarter overlap and a common quarter in a square `(x,r)` with `x` in `{1,2,3}`. For the down test at row `r`, use square row `r-1`. Let `g=1` when the oriented endpoint test fails or `VIS` holds, and `g=0` otherwise.

Every deficient retained path has a visible end. The path is charged, so it has a bad square. That square has two bad quarters, but the entire path has at most one payable quarter. At least one quarter is therefore unpayable. Its multiplicity is two, and its covering pair belongs to `S*` with a two-quarter overlap. The pair is outside `B`, by retention.

That overlap has square depth at most two from its side. A candidate square is `(r,j)` or `(j,r)`, with `r>=12`. The side must therefore be the one at that arm's endpoint, with `j` equal to one or two. Opposite-side depths are at least `n-2-r>=n/2+2`. The pair belongs to that side's `S_sigma` and witnesses `VIS` in the endpoint row.

This works for every candidate radius, including 12 through 32. There is no small-radius error. The exact geometry check in B.3 finds seven possible visible pairs per orientation, verifies their reflection and checks that their edges are pending at the required row boundary.

Choose one failed end for each lost candidate and one visible end for each deficient retained candidate. The two classes are disjoint. In a fixed side scan, near and far endpoint rows lie in the disjoint intervals `[12,n/2-4]` and `[n/2+3,n-13]`. Each row belongs to at most one candidate. If `G_strong` counts strong rows over the four sides with their proper half orientations, then:

```text
G_strong >= D_loss+L_def.                          (6)
```

### B.6. The strong strip certificate and the orientation join

Each `S_sigma` is a proper subgraph of the connected tour, so it is a forest. Columns zero and one have degree two; columns two and three have degree at most two.

Scan cells in increasing `(row,column)` order. A state records pending selected edges and the partition of their ends into paths. At each cell choose forward edges to meet the degree requirements. Reject degree overflow and any closed cycle. Shift the row coordinates after column three. Knight edges span at most two rows, so the state space is finite.

Each transition weight `w` counts crossings introduced when the later of the two edges' lower endpoints is processed. Each crossing is counted once. A full side walk has `4n` transitions and total weight `X_sigma`.

The independent checker augments the state with the full selected-edge mask for the current row. There are 20 possible strip edges meeting that row. The mask keeps edges removed during processing and includes new edges. At row end it evaluates the endpoint test and `VIS`, then resets the mask. Both orientations use the same graph. All base row-boundary states are admitted as starts, so actual half-side states are covered. No parity bit is needed: the strong test is independent of row parity.

The base graph has 82,516 states and 144,674 arcs. The augmented graph has 184,006 states and 343,631 arcs. Exact integer relaxation produces potentials `h_up` in `[-29,0]` and `h_down` in `[-33,0]`. Each stabilizes after 41 passes. A final pass checks every arc inequality:

```text
4w-1-4g+h(u)-h(v) >= 0.                            (7)
```

The penalty `g` is charged only at row end. The checker also verifies, at every row boundary:

```text
-4 <= h_up-h_down <= 4.                            (8)
```

The down test at row `r` uses square row `r-1`, because reflection sends square row zero to minus one. The full row mask keeps the required edges. Reflection alone would not justify copying the up potential range; the down range is 33. The interface check (8) is a separate part of the certificate.

Split a physical side at row `n/2`. Use up tests on the first half and down tests on the second. Keep the same state and crossing ownership at the cut. Let `a,m,z` be the start, middle and end states. Summing (7) across both halves gives:

```text
4(X_sigma-n-G_sigma)
  >= h_up(m)-h_up(a)+h_down(z)-h_down(m)
  >= -4-33 = -37.
```

Here (8) bounds the middle difference, `h_up(a)<=0`, and `h_down(z)>=-33`. This permits arbitrary boundary states. Summing over four sides gives:

```text
G_strong <= sum_sigma X_sigma-4n+37.                (9)
```

A crossing pair counted in two adjacent strips has both edges in their `4 x 4` corner square. That square has 24 possible knight edges. Opposite strips share no edges in the stated size range. Hence:

```text
sum_sigma X_sigma-s <= 4*binom(24,2)=1104,
G_strong <= s-4n+1141 = T+1139 <= T+1160.           (10)
```

The final inequality keeps a looser constant to match the stated bound. Connectivity is used in the forest condition. This certificate does not assert the same result for disconnected 2-factors.

The independent reconstruction, both potential checks and their interface check run with:

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim42_check.py
```

This took about 22 seconds on the research machine on 2026-10-03, in one process. The program imports prior verifier transition and exact polygon routines, not the author's graph or potential code. The potential arrays, hashes and report are saved under `gap/verifier/` as `claim42_potential_up.npy`, `claim42_potential_down.npy`, `claim42_check.json`, `claim42_check.log` and `claim42_sources.json`.

The separate author implementation uses endpoint accumulators and carries previous-row visibility as a bit for down scans. Its commands are:

```sh
(cd gap/lowerbounds && ../../.venv/bin/python f1v_stab.py cert 1 1 up)
(cd gap/lowerbounds && ../../.venv/bin/python f1v_stab.py cert 1 1 down)
```

The measured author run times were 31 seconds up and 42 seconds down on 2026-10-03. These programs require both NumPy and OR-Tools, as noted above. Their separate half-side ranges alone give the weaker constant 614. Use the independent common-state interface check for the constant 612 proved here. No periodic SAT result or critical-rate optimality claim is needed.

### B.7. Add the payments

Combine (4), (5), (6) and (10):

```text
E+580 = nu(total)+(T+1160)/2
      >= (L-L_def)/2+(D_loss+L_def)/2
       = (L+D_loss)/2
       = (2n-60)/2 = n-30.
```

Since `X=E+4n-2`, this gives:

```text
X >= 5n-612, for every even n>=32.
```

The quarter payments and the strip reserve are distinct terms of the exact identity (4). The reserve pays lost and deficient retained paths once, as disjoint classes. No further payment or error is needed for individual paths or stretches of a side. For smaller positive even `n`, the same numerical inequality follows from `X>=0`.

The proof needs the local tile, flux and endpoint checks, the quarter-payment rule, and one narrow-strip certificate with two potentials and their interface. It uses no wider strip model, local matching certificate or classification of all interior patterns. The full proof and audit records are in `gap/turnstheory/PROOF_5N.md` and Claims 39, 40 and 42 of `w-verifier/FINDINGS.md`.

</details>
