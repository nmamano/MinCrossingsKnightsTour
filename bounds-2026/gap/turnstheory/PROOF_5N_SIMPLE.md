# S2: a shorter hand proof of 5n

2026-10-03. **PROOF REORGANIZATION SUBMITTED FOR AUDIT.** Best option:
keep only candidates with two non-strong ends, count two usable bad
quarters per surviving path, and use one scalar quarter inequality.
This retains `X>=5n-612` with the audited strip black box. It removes
the residue-retention rule, deficient paths, private allocations and
the good-middle argument. No new finite theorem is needed for this hand reorganization.

**S1 addition:** Lower Bounds now proposes option C, a degree-only
cut-state certificate with 3,136 states and 48,510 arcs. Combining
that certificate with this hand proof is the best COMPLETE proposed
presentation. Option C is author-certified and awaits independent
audit. Sections 7–9 below check the connectivity dependence, state the
candidate 2-factor extension, and include its model and identity (K).

If simpler handling of the strip input matters, use its separate
UP/DOWN error bounds instead of their interface and obtain
`X>=5n-614`. The audited input in Sections 1–6 concerns closed tours, even n>=32;
Section 7 states the candidate extension to spanning knight 2-factors.
The audited PROOF_5N.md and both blog posts are unchanged. Beyond-5n
research is stopped; none of its unfinished lemmas is used here.

## 1. Best option: discard strong-end paths first

### 1.1 Objects and the one strip input

Let X count proper unordered crossing pairs, E=X-4n+2. Let S be the
UNION of crossing-pair sets within the four width-two side edge strips
(edges touching depth zero or one), and let s=|S|. Put T=s-4n+2.

Use the existing strong test on each actual oriented side row:
F!=2 modulo three, or the endpoint exception, or VIS. F is the eight-
edge sum in PROOF_5N.md Section 2. VIS is a two-quarter overlap of two
strip edges, not both outer-column edges, in squares of depths 1..3
at that endpoint row. DOWN uses square row r-1 with test row r.
Let b be the strong-row count over the four half-oriented side scans.

Take the following as a black box, with ONE global constant C:

    T >= b-C.                                      (S)

The audited proof permits C=1160. Separate half-side estimates permit
C=1164 without checking the common-state interface. Section 5 below
states the exact contract for Lower Bounds' replacement proof.

### 1.2 The surviving paths

Use all corner candidates of radii 12 through n/2-4:

    (r+1/2,3/2) -> (r+1/2,r+1/2) -> (3/2,r+1/2).

There are N=2n-60, with distinct square centres. KEEP a candidate
exactly when both its oriented strong tests are zero. Let z be the
number discarded and M=N-z the number kept. Each discarded candidate
can choose one strong end; candidate endpoint rows on each physical
side are distinct. Hence

    z <= b.                                       (2)

This rule deliberately keeps fewer paths than the old residue rule.
There is no penalty: (S) pays every discarded path, including a path
that would have been retained and fully payable under the old rule.

Each kept path has both ordinary endpoint tests passing. The corner
flux computation gives outside flux `1+3*(-1)^r=1 mod 3`; the internal
path is charged. This uses only the passing case of the endpoint lemma.
There is no need to define the two h residues or classify their other
possible values.

By the local flux identity, the path has a bad adjacent quarter.
The alternating square identity gives at least two bad quarters in
that square. Distinct kept paths use distinct squares.

**No forbidden overlap on a kept path.** A two-quarter strip pair
can overlap only square depths at most two from its side. At candidate
radius r>=12, a square this close to a side lies at the corresponding
path end and has that end's row. If both pair edges touch the outer
column, it is the endpoint exception. Otherwise it is VIS. Either
would make the endpoint strong, contrary to keeping the path.
The other sides are too far away to cause such a pair. Therefore no
bad quarter of a kept path has multiplicity two whose covering pair
is in S with a two-quarter overlap.

Call bad quarters without that last forbidden type usable. The kept
paths supply at least 2M DISTINCT usable quarters. This is the whole
replacement for retention, deficiency, H1 and the visibility lemma.
The seven-pair visibility and one-exception enumeration is unchanged.
No small-radius omission, locality radius or payment neighbourhood is
required.

### 1.3 One scalar quarter inequality

Each tile has four quarters. Two tiles overlap iff their edges cross,
in one or two quarters. Write m(q) for full-tour quarter multiplicity
and X1 for the number of one-quarter crossing pairs. Set

    D = sum_q (binom(m(q),2)-m(q)+1).

This summand is 1 at m=0, 0 at m=1 or 2, and at least 1 at m>=3.
It equals binom(m-1,2) as a polynomial, including m=0; no special
W3 convention is needed. Incidence counting gives

    D = (2X-X1)-4n^2+4(n-1)^2 = 2E-X1,
    D+X1 = 2E.                                    (3)

In particular E>=0. This retains the tile bound 4n-2.

Let Q be ANY set of usable bad quarters. Those with multiplicity zero
or at least three number at most D. A remaining quarter has m=2:
if its pair is outside S, each such pair covers at most two quarters;
if its pair is in S, usability forces one-quarter overlap, counted
by X1. Consequently

    |Q| <= D+2(X-s)+X1
         = 2E+2(X-s)
         = 4E-2T.                                 (4)

This is a scalar counting proof. It neither introduces capacity atoms
nor has to show their radius or allocate them to individual paths.
The nonnegative summands in D automatically pay the holes and higher
multiplicities. Counting X1 also for some pairs outside S only makes
the upper bound looser; no new resource is being spent in (4).

### 1.4 Finish in two lines

Use the 2M usable quarters, then (S) and (2):

    4E >= 2M+2T
        >= 2(N-z)+2b-2C >= 2N-2C.

Thus E>=n-30-C/2, and

    X >= 5n-(32+C/2).                              (5)

With C=1160 this is 5n-612. With C=1164 this is 5n-614.
No coefficient is lost. The proof works for every even n>=32 with
all candidate radii. Below 32 these numerical bounds follow from X>=0.

**Audit boundary.** This is a hand reorganization of audited geometry
and the SAME strong strip theorem. The new endpoint filtering and
scalar inequality (4) should be audited before changing a public proof.
It is not a claim that the strip theorem now has a hand proof.

## 2. What carries the weight in the current proof

The following map refers to PROOF_5N.md Sections 1–4 and 6. The strip
certificate is treated only through (S).

| Current input | Role | In the shorter proof |
| --- | --- | --- |
| Tile area and one/two-quarter overlap | Essential bridge from crossings to local defects | Keep |
| Exact identity G+X1+W3=2E | Essential accounting, but three named terms are optional | Replace by D+X1=2E and one polynomial summand |
| Mod-three flux and zero circulation | Essential source of a defect on a path | Keep; it is not replaced by a picture of normal rows |
| Eight-edge endpoint identity | Essential link to the strip's row predicate | Keep its F table and passing case |
| h residues, exceptional-pair retention, L and D_loss | Bookkeeping to retain more than the passing paths | Remove; keep only two non-strong ends |
| Candidate count N=2n-60, distinct squares and side rows | Essential no-reuse and linear count | Keep, in one geometry paragraph |
| Outer-column set B | Convenient notation for exclusion | Remove the global set; keep its single local exception fact |
| Mixed nu, its atom types, and four-case private packing | A valid stronger result than the scalar proof needs | Replace by (4) |
| Radius-two support, radius-ten eligibility | Not used in the global lower bound | Remove |
| s_i, d_i, L_def and good middle H1 | Bookkeeping to separate payment cases | Remove |
| Visibility at a deficient path end | Essential geometric fact in indirect form | Use its contrapositive: zero strong ends exclude forbidden quarters |
| E+580=nu+(T+1160)/2 and final cancellation | Bookkeeping | Replace by 4E>=2M+2T and T>=b-C |

Dependency chain:

    tiles -> scalar bound (4)
    flux + passing endpoint identity -> each kept path has a bad square
    alternating square identity -> two bad quarters
    strip depth + exception/VIS geometry -> those quarters are usable
    disjoint paths -> 2M usable quarters
    disjoint endpoint rows + (S) -> M+T >= N-C
    combine -> 5n-(32+C/2).

The square identity, visibility exclusion and exact accounting each
supply real strength. Retaining every possible charged path does not.
There is no W1/fold-stack classification, W3 support SAT lemma, chamber
argument, Hall theorem or untrapping lemma in this chain. The old W3
multiplicity variable and the unrelated W3 SAT lemma must not be confused.

## 3. Concrete choices and their prices

| Choice | Bound / loss | Assessment |
| --- | --- | --- |
| Strong-end filtering + scalar usable-quarter count | 5n-612, epsilon=0 | Recommended; same black box and fewer hand cases |
| Same proof, separate half-side errors | 5n-614, epsilon=0 | Drops the common-potential interface from the certificate contract |
| Keep existing retained set but replace nu by scalar (4) | 5n-612, epsilon=0 | Safe smaller edit, but still carries L_def and the visibility split |
| Use only one bad quarter per kept path | (9/2)n-597 with C=1160; (9/2)n-599 with C=1164 | Deletes the alternating-square step, epsilon=1/2; that step is too short to make this a good trade |
| Prove only strip rate beta, 0<beta<=1 | (4+beta)n-(30beta+2+C/2) | Exact contract below; epsilon=1-beta |

For the one-quarter option, (4) gives `4E>=M+2T>=N+b-2C>=N-2C`,
which proves the stated constants. It does NOT eliminate tile overlap,
flux, visibility or the strong-row strip theorem; the saving is small.

For the rate option, replace (S) by `T>=beta*b-C`. Since b>=z and
0<=z<=N,

    4E >= 2(N-z)+2beta*b-2C
         >= 2N-2(1-beta)z-2C >= 2beta*N-2C.

This is useful if Lower Bounds finds an elementary positive rate
before it finds rate one. Any fixed beta>0 beats 4n by a constant
factor; beta=1/2 gives 4.5n with the stated constant formula. No such
new elementary rate is asserted here.

**Do not remove the corner charge without a replacement.** Good
quarters alone do not force a defect on each candidate. Merely having
many paths or many boundary vertices is not a lower-bound argument.
Similarly, replacing the strong test by ordinary endpoint failure
would leave two-quarter strip overlaps on kept paths, invalidating (4)
for their witness quarters. This needs a new proof or a coefficient
trade such as the older 14/3 argument, not a deletion of a test.

## 4. Pareto comparison of the ladder

Page estimates below refer to HAND argument at roughly 450–550 words
per page, allowing room for equations. They are editorial estimates,
not measured rendered pages. The listed source word counts are measured
with `wc -w` on 2026-10-03 and include code, commands and audit prose.
PROOF_R3.md is a delta and must not be compared as a standalone proof.
All four bounds are audited; PROOF_N1.md's historical conditional
header is superseded by Claim 27 in the Verifier's findings.

| Coefficient and constant | Hand burden, excluding implementation details | Computer inputs beyond shared tile/flux/endpoint geometry |
| --- | --- | --- |
| 52/11, constant 360 (Claim 26) | About 4–5 pages; fractional endpoint-loss table, boundary-surplus credit and elimination. Source 2,654 words including reproduction. | Width-two boundary-credit potentials in both orientations and parities; independent base 82,516 states / 144,674 arcs, augmented 368,012 / 687,262. Endpoint-loss and boundary-credit local checks. |
| 204/43, constant 12,993 (Claim 27) | About 6–7 pages; previous argument plus blocked intervals, ghost-degree history, separate crossing budget. Source 3,515 words. | Combined row graph 3,427,200 nodes / 40,158,400 arcs per orientation; PLUS interval graph 330 states / 700 arcs (580 hard inequalities), history and run-counter checks. |
| 24/5, constant 2,603 (Claim 31) | About 4–5 pages after expanding inherited sections; fractional loss and one joint crossing budget, no interval lemma. Delta only 1,304 words. | Six-column graph; independent UP 83,780,188 states / 171,579,088 arcs, DOWN 162,690,236 / 343,695,792, two integer potentials. Recorded audit about 320 s and 1.76 GiB. |
| 5, constant 612 (Claims 39–42) | Existing presentation about 5–6 pages; 2,858 source words. Recommended main argument about 2–3 pages after expanding the common flux/endpoint lemma and table. | Width-two strong-test graph, independent augmentation 184,006 states / 343,631 arcs; two potentials and their interface. Recorded initial audit about 22 s. No parity product, blocked history or interval lemma. |

The times are previously recorded audit measurements, not new runs.
The 52/11 independent rebuild record is about 15.5 s. No new timing is
claimed for the 204/43 product graph. The small local geometry checks
are common prerequisites, not four different large certificate families.

**Simplest proof above 4n, with the existing finite inputs allowed:**
the recommended scalar 5n proof. It uses a smaller independent state
space than 52/11, no fractional endpoint loss, and no interval or
six-column machinery. There is no reason to pay for the older ladder
just to obtain a smaller coefficient.

For historical comparison, 14n/3-407 uses a binary endpoint test,
an outer-boundary crossing bound and two inequalities in the number
of lost rows. It avoids the higher-multiplicity identity but needs a
separate width-one boundary certificate and the joint strip stability
certificate; it is not an elementary replacement for Section 5.
The tile bound 4n-2 is the simplest fully local count, but does not beat
coefficient four. None of these observations establishes a computer-
free coefficient above four without a replacement for the strip input.

## 5. The exact black box Section 6 needs

**For the CURRENT proof, and unchanged for Section 1 above:**

For every closed tour on an even n by n board, n>=32, let s be the
union count of crossing pairs within the four width-two side strips.
On each physical side scan use the audited UP test in the first half
and DOWN test in the second, with their exact exception and visibility
rows. Count the strong-row OR indicator once per row, obtaining b.
Then

    b <= s-4n+1162, or equivalently T+1160>=b.       (BB)

That is the ONLY numerical statement from Section 5 used in Section 6.
The definition of b is essential: DOWN at vertex row r sees square
row r-1; pairs have both edges in the same strip; s is a UNION, not
the sum of side counts. Candidate endpoint rows form a subset of the
scanned rows. Additional nonnegative strong rows are allowed.

The numerical black box needs no statement about individual resource
payments, matching, critical rate, initial parity, or a sharp constant.
Those are certificate implementation issues or stronger claims. A new
proof of (BB) may use different means, provided it proves the same
count for every actual closed tour with one global constant.

For a replacement proved one physical side at a time, it is enough to
show `b_sigma<=X_sigma-n+A` with one constant A per full side. The
existing corner union estimate is 1104, so then

    b <= s-4n+1104+4A,
    C = 1102+4A,
    X >= 5n-(583+2A).

Claim 42 supplies A=37/4, which is stronger than needed for the rounded
612 theorem; this note makes no public constant change. Independent
half errors give A=29/4+33/4=31/2, yielding 614. To retain the published
612 exactly it is enough that A<=29/2. A hand proof with any absolute
A retains coefficient five and gives its explicit constant by this
formula. An O(1) PER RUN or PER STRONG ROW is not sufficient.

If the full row predicate is awkward, a logically weaker sufficient
input for the recommended proof is `T>=z-C`, where z is the number of
candidates with at least one strong end. That only changes the proof
of (S), not the hand reduction. It is global and may be less convenient
for a one-side proof because a candidate joins two sides.

## 6. Reproduction and handoff

No new large computation is required for this proposal. The common
finite geometry and unchanged black box can be reproduced from the
research root with

    python3 w-turnstheory/check_knight_tiles.py
    python3 w-turnstheory/check_corner_box.py
    python3 w-turnstheory/check_square_defects.py
    .venv/bin/python gap/verifier/claim42_geometry.py
    OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim42_check.py

The new scalar hand steps to audit are: the stronger initial filter,
all usable quarters on kept paths, inequality (4), and the two-line
elimination. Old private-payment and support checks are not new proof
obligations. No saved-tour experiment substitutes for these arguments.

Lower Bounds owns the Section 5 hand replacement in SIMPLE_STRIP.md.
The first draft predated that file. The addition below now includes
its option C and checks identity (K), while keeping the audit status
separate. Section 5 remains the plug-in contract and permits a larger
constant or rate beta<1. The hand simplification with the old audited
black box does not depend on option C passing its new audit.


## 7. Connectivity audit of the hand proof

**HAND CHECK: no step in PROOF_5N.md Sections 1–4 or 6 requires a
single cycle.** Let H be a spanning SIMPLE degree-two subgraph of the
knight graph on the board. It can have several components. X must
count ALL proper edge pairs, including pairs from different cycles.
A sum of only within-component crossing counts is a different statistic
and is not covered by this argument.

The following table supplements every item of the dependency map in
Section 2. “Geometry only” means it holds for arbitrary selected edges
with the indicated tile convention, or for the fixed candidate paths.

| Original step | Actual hypothesis used | One cycle? |
| --- | --- | --- |
| Section 1: n^2 edges and 4n^2 quarter incidences | Spanning degree two: sum degrees=2n^2 | No |
| Tile area, endpoint box, one/two-quarter overlap | Legal distinct knight edges; exact geometry | No |
| Pair-incidence identity and E=(G+X1+W3)/2 | Geometry plus n^2 edges, hence degree two suffices | No |
| Section 2: one-edge flux formula | Linear identity for arbitrary selected edges | No |
| Zero circulation modulo three | At EACH vertex deg_H=2, so deg_H+4=6 | No |
| Nonzero path charge forces a bad quarter | Local flux formula | No |
| Two bad quarters per bad square | Alternating tile identity | No |
| Candidate count/disjointness/row ownership | Board geometry, even n>=32 | No |
| Eight-edge endpoint identity | Arbitrary-edge coefficients plus deg_H(0,r)=2 | No |
| h residues and implication of two passing tests | Endpoint identity, zero circulation and parity | No |
| Outer-column exception and B exclusion | Exact pair geometry and absence of the exception | No |
| Section 3: S union and exact mixed identity | Sets of crossing pairs and tile identity | No |
| Four-case quarter packing or scalar inequality (4) | Multiplicities and at-most-two-quarter pair overlap | No |
| Deficiency and good-middle implication | Strip tile depth and square identity | No |
| Section 4: unpaid quarter gives VIS at an end | Charged path, multiplicities, strip depth and exception rule | No |
| Strong-row injection for lost/deficient candidates | Distinct candidate endpoint rows | No |
| Section 6: combine path and reserve counts | Scalar inequalities and N=2n-60 | No |

The original Section 5 DOES use connectivity to reject strip cycles.
Its strip is a proper subgraph of a single Hamiltonian cycle and hence
a forest. For a 2-factor, a whole small cycle can lie within one strip.
That old certificate cannot be invoked without a new argument.
Option C permits such cycles and removes exactly this obstruction.
The 1104 corner union bound uses geometry, not the forest property.

**Candidate theorem, pending option C and simplified-proof audit:**
For every even n>=32, every spanning knight 2-factor H on the n by n
board has

    X(H) >= 5n-612,

where X counts proper unordered pairs from all edges of H. For
smaller positive even n the numerical inequality follows from X>=0.
This note does not relabel the published tour theorem or claim that
the new certificate has had an independent check.

### Exact re-checks for that extension

1. Rebuild option C with NO component labels, cycle rejection, or
   implicit “extends to a tour” filter. Read source confirms those
   rules are absent; an independent rebuild must confirm the result.
2. Map every actual width-two restriction of a finite 2-factor to a
   walk from the empty bottom cut, through the middle state, to the
   empty top cut. Core degrees are two and halo degrees at most two
   regardless of components. Boundary states must not be excluded.
3. Check crossing ownership for all pairs, including edges in different
   strip components and pairs that straddle the orientation change.
4. Recheck the hard-coded F coefficients, exception and all seven VIS
   pairs against the audited geometry, including DOWN square row r-1.
   The test must be the same one used in the hand filtering proof.
5. Check both row-arc potentials and their COMMON-CUT interface on
   all enumerated states, then the four-side and 1104 union constants.
6. Audit the hand hypothesis table above and the new filtering/scalar
   proof; existing saved TOUR tests alone do not prove a 2-factor claim.
   In particular use degree two, not a tour traversal, in the flux proof.

A checker run of the author's code would reproduce its certificate,
not independently settle items 1–5. No such rerun is claimed here.

## 8. Option C in the simplified proof outline

**ARGUMENT FROM AUTHOR-CERTIFIED INPUT; independent audit pending.**
I read SIMPLE_STRIP.md 1.2–1.4 and the complete source
`gap/lowerbounds/simple_strip/check_cut_certificate.py`.

Replace only the proof of the black box (S), leaving Section 1's
hand argument intact. Scan one WHOLE ROW per arc. A state contains
only selected S-edges crossing a horizontal cut. There are 12 possible
pending edges. A row arc selects edges whose lower endpoint is in that
row, with exact degree two in columns 0,1 and degree at most two in
columns 2,3. No path partition or no-cycle rule is present. The mask
of edges meeting the row is available directly from the incoming
state and the newly selected edges; no separate mask state is needed.

The source generates reachable states from the empty cut. Bellman-Ford
then starts at zero at every generated state, providing arbitrary
actual half-side starts. The reported graph has 3,136 states and
48,510 row arcs. w counts every newly introduced crossing once.
On every row arc and in each orientation the reported potentials obey

    4w-4-4g+h(u)-h(v) >= 0.

The reported ranges are UP [-24,0], DOWN [-28,0], with eight relaxation
passes in each case. The common-state difference h_up-h_down is [0,4].
Writing a,m,z for a side's start, middle and end states gives

    4(X_sigma-n-b_sigma)
      >= h_up(m)-h_up(a)+h_down(z)-h_down(m) >= -28.

Thus four sides give b<=sum X_sigma-4n+28. With the unchanged corner
union correction,

    b <= s-4n+1132 = T+1130 <= T+1160.

This proves the precise black box (BB) if option C passes audit. Keep
constant 612 in the candidate theorem; the numerical slack is not a
reason to change the public statement during a simplification task.

The proposed presentation is therefore:

1. Tile geometry, flux and the passing endpoint lemma.
2. Strong-end filtering and scalar quarter bound (Section 1 here).
3. The cut-state strip certificate in the preceding four paragraphs.
4. The two-line final algebra.

Compared with the current proof this removes both the private payment
bookkeeping and the forest/full-mask graph augmentation. It still uses
a computer for the strong-row price; it is not a full hand proof.

Reproduction from the research root:

    .venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py

Requirements: Python standard library and NumPy only, with no project
imports. The author reports about 4 seconds and 40 MB on 2026-10-03.
This is a different command from f1v_stab.py and has no OR-Tools import.
It writes its two potential arrays under gap/lowerbounds/simple_strip/.
I did not edit or execute it in this task.

**Pareto addendum:** the proposed new 5n row of the ladder table has
about 2–3 hand pages plus a 3,136-state / 48,510-arc certificate and
two potential arrays with their interface. Those sizes and 4-second
runtime are author reports pending audit, not replacements for the
older audited measurements in the table. It also appears to extend
the theorem's scope to 2-factors, as Section 7 specifies.

## 9. Identity (K): checked hand explanation of the base strip rate

**HAND PROOF CHECKED HERE.** This identity is optional in the shortest
proof. It explains why the base term is one crossing per side row;
it does not prove the extra cost of strong rows. It uses no connectivity.
It concerns a FINITE full side on the board, not a periodic infinite
strip, so keep its end constant.

Use m_S(q), the multiplicity from S_sigma's tiles ONLY, and board
squares only. This is different from the full-tour multiplicity m(q)
in Section 1. Let a,b0,c,d count strip edges of column types 01,02,12,13
respectively. (b0 is an edge count, not the strong-row count b.) Degree
two in the first two vertex columns gives

    a+b0=2n,      a+c+d=2n.

Tile incidences in square columns zero and one are respectively
4a+2b0 and 2b0+4c+2d. Let H_i be holes there and
exc_i=sum_(col i)(m_S-1)_+. Since each column has 4(n-1) quarters,

    exc_0=2a+4+H_0,
    exc_1=4n-4a+2c+4+H_1.

Eliminate a between the two equations:

    exc_0+exc_1=2n+6+H_0+c+(H_1+exc_1)/2.

Now H_1+exc_1=sum_(col 1)|m_S-1|. If X1_sigma is the number of
one-quarter crossing pairs within this strip, tile-pair counting gives
`2X_sigma-X1_sigma=sum_q binom(m_S(q),2)`. Splitting the latter sum
into columns 0,1 and the deeper column, and using
`binom(m,2)=(m-1)+binom(m-1,2)` for m>=1, proves

    2X_sigma = 2n+6+H_0+c
             + (1/2) sum_(q in col 1)|m_S(q)-1|
             + sum_(q in cols 0,1; m_S>=1) binom(m_S(q)-1,2)
             + sum_(q in cols >=2) binom(m_S(q),2)
             + X1_sigma.                          (K)

All terms after 2n+6 are nonnegative. Hence X_sigma>=n+3 for every
finite side restriction of a spanning 2-factor. The apparently stronger
constant does not contradict a periodic strip with one crossing per
row: a periodic strip does not have these board-end mass equations.

**How to include K without adding a dependency:** place this hand
calculation after the tile lemma as an optional explanation. Keep
option C's direct crossing-cost certificate for the extra strong-row
count. Summing K alone proves only 4n-O(1), after the corner union
correction; it does not reach 5n. Turning K into a row-by-row kappa
potential introduces an additional telescoping check. That would make
the proof longer unless it enables an actual hand proof of the strong
row price, which Lower Bounds has not claimed.

The author measured K on 112 sides of 28 saved tours. The command is

    .venv/bin/python gap/lowerbounds/simple_strip/check_tours.py

Those measurements support implementation, while the displayed degree
and incidence equations prove K for all spanning 2-factors. The source's
additional kappa/debt experiments are not inputs to this simplified
proof or to the candidate extension.
