# Claim 31: exact joint-strip crossings

2026-10-03. **AUDITED PASS (Claim 31).** The Verifier independently
rebuilt both integer certificates and checked this reduction. The
coefficient, constant, and size range below pass. See Claim 31 in
`w-verifier/FINDINGS.md` for the independent checks.

For every even n>=32, the audited theorem for closed Hamiltonian knight
tours on the n by n board is

```
X >= (24n-13012)/5 >= 24n/5-2603.
```

X counts unordered proper crossing pairs. This is a computer-assisted
audited proof, not a Lean theorem or a claim for arbitrary 2-factors.

## Delta and inherited input

Retain Sections 1–3 of `gap/turnstheory/PROOF_N1.md`, including all
endpoint definitions and the candidate radii 12 through n/2-4. Those
sections were audited in Claims 26 and 27; the old conditional header
in PROOF_N1.md predates the Claim 27 PASS recorded in
`w-verifier/FINDINGS.md`. Replace its Sections 4–6 by the sections below.
Neither its interval lemma nor its blocked-row credit is used here.

The inherited quantities are E=X-4n+2; A, the sum of fractional endpoint
penalties on the 2n-60 candidate paths; and R=sum_sigma b_sigma-4n,
where b_sigma counts pairs whose two edges touch side sigma's outermost
column. The inherited square and path argument gives

```
4n <= 4E+2(A-R)+156.                                  (R1)
```

It uses connectedness of the tour, the same boundary overlap exclusion,
and the same candidate endpoints as the audited proof.

## 4. Joint edge sets and their budget

For a physical side sigma, give vertices coordinates (depth, scan row).
Use columns 0 through 5 and the seven legal unordered column pairs

```
01, 02, 12, 13, 23, 34, 35.
```

Let S_sigma be the selected edges with an endpoint in column 0 or 1;
F_sigma the selected edges between columns 2 and 3; and J_sigma the
selected edges between column 3 and column 4 or 5. Their disjoint union
T_sigma is exactly the tour edges with an endpoint in columns {0,1,3}.
It contains every tour edge at those columns. Thus the restriction has
degree exactly two at columns 0,1,3 and at most two at columns 2,4,5.
It is a proper subgraph of the Hamiltonian cycle, hence a forest.

Let Y_sigma count all crossing pairs within T_sigma. All endpoints of
its edges have depth at most five. Opposite-side sets have no common
edge for n>=32. A pair counted at two adjacent sides has both its edges
in the six-by-six corner square. That square has
2*4*5+2*5*4=80 possible knight edges. Its number of crossing pairs is
therefore at most binomial(80,2)=3160. For a pair counted m times, its
excess multiplicity m-1 is at most binomial(m,2). Sum over the four
adjacent-side intersections to obtain

```
sum_sigma Y_sigma <= X+12640.
D_T := sum_sigma Y_sigma-4n <= E+12638.               (R2)
```

No tile overlap localization is needed for this count. Mixed crossings
between S_sigma, F_sigma, and J_sigma are included.

## 5. Six-column certificate and half-side application

Scan in increasing (row,column) order. Introduce an edge at its lower
row endpoint. Assign each crossing to the transition that introduces
its later edge. At a cell transition let

* w count pairs with both edges in S;
* w0 count pairs with both edges incident to column zero;
* wx count all remaining pairs in T, each exactly once.

Thus w+wx counts all T crossings, and w0 is a subset of w. Use the
inherited up or down endpoint test, with t=2a in {0,1,2}. All its watched
edges belong to S. Evaluate t once, at the end of the row.

For beta=p/q, `gap/searcher/lower/jr.cpp` assigns the integer weight

```
4q*w+4p*w0+4q*wx
```

to each cell transition, and adds `-4q-4p-2p*t` at column 5 only.
If W,W0,WX denote row sums, the row weight is exactly

```
q*(4W-4)+p*(4W0-4)+4q*WX-2p*t.                       (R3)
```

There are six cells per row. In particular the baseline is subtracted
once per row, not six times at the old four-column rate.

The certificate uses degree string EELELL and labels only S components
(`slab` mode). It rejects S cycles, but need not reject a cycle that
uses F or J. This is a relaxation: every actual T_sigma forest is
admitted. The theorem needs only the certificate on this larger set.

The augmented state stores pending edges, S component labels, endpoint
test bits that would disappear during a row, and parity. At row starts,
the disappearing test bits are initialized from the actual pending
edges. Both initial parity states are seeded. Every reachable base
row-start state occurs with either parity: parity has no effect on
base transitions, and switching the initial parity switches every
subsequent parity. The row-start test accumulator has no older history.

The producer logs `gap/searcher/lower/joint_up.log` and
`gap/searcher/lower/joint_down.log` report these exact results at p=2,q=1:

| Test | Augmented states | Arcs | Potential range | Violated arcs |
| --- | ---: | ---: | --- | ---: |
| up | 83,780,188 | 171,579,088 | [-104,0] | 0 |
| down | 162,690,236 | 343,695,792 | [-104,0] | 0 |

The potential satisfies d(v)<=d(u)+weight(u,v) on every arc. Telescope
over any admitted half walk of m complete rows and divide by 4q=4.
The potential loss is at most 104/4=26. Therefore

```
Y_H-m+2*(b_H-m) >= 2*sum_H a-26.                    (R4)
```

Y_H and b_H are assigned crossing counts, not counts in the subgraph
induced by half-board rows. This convention preserves crossings across
the middle cut.

Use the up test on rows 0 through n/2-1 and the down test on rows n/2
through n-1. Keep the actual pending edges and S labels at the cut;
initialize the new orientation's test bits from them. That base state
is reachable from the empty state along the actual tour prefix. Both
parities are available. For the near half use physical row parity;
for the far half use local radius parity (n-1-y) mod 2. This is opposite
to physical row parity for even n. The certificate covers both choices.

The candidate endpoint rows are [12,n/2-4] and [n/2+3,n-13], respectively.
Thus every candidate penalty is covered once. Other row penalties are
nonnegative. The eight half walks partition all four full-side scans;
their row counts sum to 4n. Sum (R4), then apply (R2):

```
2*(A-R) <= D_T+8*26 <= E+12846.                     (R5)
```

## 6. Conclusion and scope of the limit

Combine (R1) and (R5):

```
4n <= 4E+2*(A-R)+156 <= 5E+13002.
X = 4n-2+E >= (24n-13012)/5 >= 24n/5-2603.
```

The size range remains every even n>=32. No new asymptotic threshold
or extra assumption on the retained paths is used.

The producer also gives zero-weight critical cycles at beta=2: period
six for up and period four for down. They establish the coefficient
limit of this certified relaxation. The down cycle has wx=0. No claim
about a stronger model that labels every T edge is needed here.

## 7. Check commands and audit boundary

All commands below run from the research root. The inherited geometry
has already passed Claims 26 and 27. Its checks are:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 w-turnstheory/check_knight_tiles.py
PYTHONDONTWRITEBYTECODE=1 python3 w-turnstheory/check_corner_box.py
PYTHONDONTWRITEBYTECODE=1 python3 w-turnstheory/check_col0_squares.py
PYTHONDONTWRITEBYTECODE=1 python3 w-turnstheory/check_square_defects.py
PYTHONDONTWRITEBYTECODE=1 python3 w-turnstheory/check_endpoint_loss.py
```

The new small budget and arithmetic check is:

```sh
python3 gap/turnstheory/check_r3_reduction.py
```

To reproduce the two finite certificates, run these jobs sequentially
(each uses several GB of RAM; the producer measured about 3.6 GB up
and 5.3 GB down on 2026-10-03):

```sh
g++ -O2 -std=c++17 gap/searcher/lower/jr.cpp -o gap/turnstheory/jr_check
gap/turnstheory/jr_check EELELL 01,02,12,13,23,34,35 slab up cert 2 1
gap/turnstheory/jr_check EELELL 01,02,12,13,23,34,35 slab down cert 2 1
```

Require CERTIFIED, potential range [-104,0], and zero violated arcs in
both outputs. Exit status alone is not a sufficient success check.
To reproduce the optional critical-cycle search behind the producer
logs, replace `cert 2 1` by `crit 8 3` in each command. That search is
not an extra premise of the lower bound.

For this submission I read the source and both producer logs and ran
the small reduction check. I did not rerun the large graph jobs. The
Verifier subsequently audited graph completeness, crossing counts,
endpoint state coverage, and exact potentials using an independent
implementation, and passed this reduction as Claim 31.
