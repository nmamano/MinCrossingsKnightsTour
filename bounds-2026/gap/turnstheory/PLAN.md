# Master skeleton: private crossing charges toward 6n

2026-10-03. **PHASE 1 — DESIGN ONLY.** No computation was launched.
R3 is stopped. Claim 27 is PASS: the current audited lower bound is
204n/43-12993 for even n>=32, closed Hamiltonian tours. Everything below
that proposes a stronger bound is unproved.

## 1. Diagnosis and two necessary corrections

**PROVEN algebra:** the old reduction has
`4n <= 4E+2(A-R)+O(1)` and `beta*(A-R)<=E+O(1)`, where
`E=X-4n+2`. Its coefficient `4+2beta/(2beta+1)` tends to five.
This is a ceiling of that reduction, not a theorem excluding every
strip-based method. Its global gap budget cannot identify private
crossings for individual paths.

A new price p for retained paths alone does NOT establish 4+2p.
There are N=2n-O(1) candidates, but only L can be retained. Missing
candidates must also be paid for. Even granting the simpler stability
bound `N-L<=E/beta+O(1)`, a price `E>=pL-O(1)` gives only
`4+2p*beta/(beta+p)`, below 4+2p for finite beta. The old N1 inequality
actually bounds A-R, not N-L by itself. Endpoint restoration is a
separate required lemma.

## 2. Exact accounting that would prove the target

Keep the audited candidate paths gamma_r, height flux
`omega=phi_H+phi_grid mod 3`, endpoint residues, and exceptional-pair
test. Let C be the retained charged candidates and D=N-|C| the actual
discard count; A remains its proved additive upper bound.

For every crossing pair z, assign nonnegative weights:
`b_z` for the boundary baseline, `f_(z,i)` for retained path i,
`e_z` for discarded candidates, and `h_z` for connectivity. Require

```
b_z + sum_i f_(z,i) + e_z + h_z <= 1                 (capacity)
sum_z b_z >= 4n-O(1)
sum_z,i f_(z,i) >= p*|C|-O(1)
sum_z e_z >= p*D-O(1).                              (endpoint restoration)
```

Support b only on the audited outer-column crossing set B. Support f
outside B and near its own gamma_i. The endpoint and connectivity
certificates must use the SAME remaining capacities. Their separate
unweighted crossing lower bounds cannot be added.

Summing replaces the bad-quarter budget by
`X >= (4+2p)n + sum h_z - O(1)`. Thus p=2/3 gives 16n/3 once endpoint
restoration is proved. A further `sum h_z>=2n/3-O(1)` gives 6n.
Boundary surplus may pay for endpoints or connectivity, but not both.

**Exact proposed private-price lemma (CONJECTURE):** there are absolute
r,C0 and a translation-covariant finite local rule, with finite boundary
states, which assigns f for every tour and its retained candidate family.
It gives zero weight to B, gives weight only when a crossing's edge
support is within grid distance r of gamma_i, respects unit crossing
capacity, and satisfies `sum_i,z f_(z,i)>=(2/3)|C|-C0`.
Finite-piece potentials must cancel on internal interfaces; their total
uncancelled error must be bounded independently of n and the number of
defects. A constant loss per path, run, fold, or junction is insufficient.
This lemma's compatibility with endpoint restoration is an additional
joint requirement, not a consequence of its standalone form.

## 3. Lemma register and ownership

| Input | Required statement | Status / owner |
| --- | --- | --- |
| L0: geometry and supply | N=2n-O(1); exact residues; D<=A; boundary baseline | PROVEN, Claims 26–27 |
| L1: structure | Classify zero-crossing local phases, including free folds; control non-field interfaces and joins with explicit costs | CONJECTURE, Structures + Lower Bounds |
| L2: private flux | The local allocation lemma above at p=2/3, or first any p>1/2 | CONJECTURE, Edge Searcher; Verifier first tests counterexamples |
| L3: endpoint restoration | Reserve pD in the capacities left by L0 and L2, with only O(1) total interface error | CONJECTURE, Lower Bounds + Turns Theory |
| L4: universal topology | Every low-crossing tour has at least 4n/3-O(1) repair obligations, or compensating structural defects | CONJECTURE, Structures |
| L5: private repair price | Obligations receive at least 1/2 each from h, after baseline, flux, and endpoints have been paid | CONJECTURE, Structures + certificate work |

L4 must define obligations without assuming the standard four midpoint
chevrons. Claim 28 prices changed port partners in a fixed strip;
non-P rows are not repaired port ends. An alternative defect case must
use the same capacity ledger. L1 must include all zero-cost phases,
not assume that every crossing-free region is one parallel field.

## 4. Evidence, finite route, and stop tests

The diagonal carrier price 2/3 is certified at widths 3–6 with fixed
exterior fields (`gap/searcher/RATES.md`). Claim 28 gives the half-price
per repaired end only in its stated width<=4 model. Structures S3–S11
and G1–G7 supply useful mechanisms, not universal layout rigidity.
Claims 17 and 28 explicitly leave unrestricted transport, side-boundary
area balance, joins, and joint flux/repair charging open.

Phase 2 should start with counterexample tests, not a large transfer
graph: use 6-by-6 then 8-by-8 cores with a two-cell halo, arbitrary legal
moves, exact core degrees, and compatible boundary ports. Test Hall
capacity obstructions: can k charged candidates have fewer than 2k/3
available crossing units outside B? Include holes whose compensating
overlap lies outside the window, gentle seams, alternating free folds,
and the period-4/6/8 endpoint fields. A patch witness needs a completion
argument before it refutes the all-tour lemma.

If these tests survive, seek a local rational allocation and integer
potential over pending edges, path connections, parity, mod-three
height, and candidate indices. Use arbitrary exterior states, not fixed
fold fields. Start at width 3; require a state-count pilot and explicit
memory bound below 8 GB before expansion. The fixed-field width-6 graph
already has 26.6 million states, so unrestricted width 6 is not presently
a credible default. This is a feasibility gate, not a state-count claim
for the new model.

**Main risk:** charge can be witnessed by holes while its compensating
crossings lie outside every fixed collar. L2 may therefore need a
nonlocal conservative transport rule instead of bounded support. Other
risks are O(n) accumulated interface errors, failed endpoint restoration,
and flux and repair spending the same crossings. Resolve L2 and L3
together before claiming 16n/3; resolve L4 and L5 before claiming 6n.
