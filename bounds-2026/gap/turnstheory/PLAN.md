# Skeleton v2 update: corner capacity and local fold stacks

2026-10-03. This update qualifies V2.2–V2.4 below. **L3 accounting
remains proved; L2 remains open.** The pair-ledger option with all flux
credit outside S* is no longer the default local contract. The mixed
ledger remains a valid accounting option, not a proved flux price.

## New evidence and its exact scope

**W1, finite certified input from KT Lower Bounds.** In a 9 by 9
core of degree two with a width-two halo of degree at most two, if no
two selected edges touching the core cross, the central 3 by 3 edge map
is one of 156 fold-stack maps. The four level functions are x, y, x+y,
and x-y. The phase library must include arbitrary layer choices,
including zigzags; straight fields and single folds do not suffice.
See `gap/lowerbounds/FINDINGS.md`, W1, for the construction and SAT
encoding. The certificate is 424 variables and 7,144 clauses; its
Glucose proof has 2,942 RUP additions.

This is a LOCAL crossing-free classification. It does not by itself
prove that an entire large region has one common level function:
different families can be separated by a parallel field compatible
with both. It also does not classify zero mu-density regions. The
condition mu=0 allows two-quarter crossings at multiplicity two,
whereas W1 assumes no crossings. An L2 proof using W1 must establish
its crossing-free premise or prove the needed density version.

**W3, checked finite witness.** The saved file
`gap/lowerbounds/windows/w3_corner_K9_R3_6_outS.json` has degree two
on a 9 by 9 core, a degree-at-most-two halo, no cycle, 57 proper
crossings, and zero crossing pairs outside the two side strips. All
four paths at radii 3,4,5,6 have nonzero combined flux (residue two).
I verified these statements directly, without running an optimizer.
Thus charge alone cannot force a positive outside-strip crossing
count in this local model. Gap quarters can carry the charge even
when the counted crossing budget outside S* is zero.

Scope matters: these radii are below the audited retained family's
minimum radius 12; the local model imposes charge, not the full
retention test or extension to a Hamiltonian tour. Four paths in one
fixed box also do not refute an asymptotic inequality with an arbitrary
absolute error. W3 rules out the proposed unrestricted positive local
price, rather than proving the global V5 contract false.

## Revised L2/L3 interface

Keep V2 (endpoint restoration) and V3 (mixed capacity) unchanged.
Use one of the following explicit contracts near path ends.

1. **Mixed atoms:** prove V5 in nu_lambda, including its gap and overlap
   atoms inside S*. A W3 check must measure these full-tour atoms, with
   all tiles entering from the halo included. Zero outside-strip pairs
   is not zero nu_lambda cost when lambda<1. The reserve
   lambda*(T+1160) remains separate; no extra raw S* pair is available.
2. **Joint pair allocation:** if f or h uses S* pairs, replace the
   saturated e of V2.2 by an actual allocation and prove simultaneously
   `b_z+e_z+sum_i f_(z,i)+h_z<=1`,
   `sum e_z>=p*D_loss-C_end`, and
   `sum_(z,i) f_(z,i)>=p*L-C_flux`, with absolute constants.
   V2 alone does not prove that the chosen local endpoint allocation
   leaves the needed residual pairs. A joint certificate must include
   both lost-endpoint and retained-path demands, both orientations,
   and all boundary states permitted by the tour.
3. **Fixed corner excision:** choose a box side B independent of n,
   with a fixed halo, and remove only O(B) small-radius candidates per
   corner. The lost price and the O(B^2) possible local edge/pair cost
   are absolute constants for fixed B. The remaining L2 assertion must
   still prove its endpoint price along the long side strips. Removing
   a fixed corner box does not remove endpoints of large-radius paths.

No allowance per endpoint, path, window, or missing-radius run is
permitted unless a telescoping certificate pays for the total. A box
with B growing with n is not an O(1) correction. Connectivity credit
must use the same residual capacities as flux credit.

The next finite L2 test should use the actual retention test and the
mixed currency V4, or certify the joint pair allocation. The phase
library for any crossing-free portion must admit the W1 fold stacks.
A failed local test must retain its exact boundary assumptions before
it is used to rule out a global route.

## Proof size and finite inputs

This update is a contract correction, not a new lower-bound theorem.
Its new proof content is the short capacity split and scope arguments
above. W1 requires the 156-map encoding and the 2,942-step DRUP proof;
W3 needs only an explicit witness check, not a SAT lower-bound proof.
The inherited L3 beta=1 certificate remains an input. Both checks below
passed on 2026-10-03; the DRUP checker verified all 2,942 RUP additions
and the empty clause. This verifies the supplied CNF proof, not an
independent reconstruction of its geometric encoding. No new large
state graph was built. Reproduction commands from the research root:

```sh
python3 gap/turnstheory/check_w3_witness.py
python3 w-lowerbounds/check_drup.py gap/lowerbounds/windows/w1cert_k9_b3.cnf gap/lowerbounds/windows/w1cert_k9_b3.drup
```

---

# Skeleton v2: exact excess density and proved endpoint restoration

2026-10-03. **Phase 2 report.** The excess identity is correct with the
zero-multiplicity convention below. L3 follows from the audited beta=1
strip certificate under an explicit capacity split. The original pair
ledger requires flux and connectivity outside S*. A second, mixed
ledger permits use of local excess atoms inside the strips without
spending the endpoint reserve twice. L2 remains unproved in either
ledger. See the update above for the corner restriction; the R3 strip
proof is now separately submitted as Claim 31.

## V2.1. Exact nonnegative excess density — PROVEN derivation

Let m_t be the multiplicity of quarter t, over all quarters of the
board square D. Define

```
G  = number of quarters with m_t=0;
X1 = number of crossing pairs whose tiles overlap in one quarter;
W3 = sum_(t:m_t>=1) binomial(m_t-1,2).
```

The summand for m_t=0 is ZERO; do not use the polynomial continuation
binomial(-1,2)=1. Equivalently use binomial(max(m_t-1,0),2).
The audited tile geometry gives

```
sum_t (m_t-1) = 8n-4,
sum_t binomial(m_t,2) = 2X-X1.
```

For m>=1, binomial(m,2)=(m-1)+binomial(m-1,2). At m=0 the missing
correction is one. Therefore

```
2X-X1 = 8n-4+G+W3,
E = X-4n+2 = (G+X1+W3)/2.                            (V1)
```

This is an exact whole-board identity, with no connectivity assumption
beyond the spanning degree-two edge count. It defines a nonnegative
measure mu: mass 1/2 per uncovered quarter, per one-quarter crossing
pair, and per unit of W3. Each atom has a local position and a finite
edge neighbourhood. It is suitable as a capacity ledger for E.

It is NOT a canonical allocation of one unit per crossing pair: holes
are separate atoms, and their compensating crossings can be elsewhere.
One cannot add an independent side-pair or arch bound to mu(D)=E. Nor
does V1 assert a boundary-free identity for a subwindow's crossing
count. A local certificate must count actual full-tour multiplicities
on its credited quarters, including tiles entering from the halo.

Independent exact-integer check on the saved n=166 tour passed:
X=1240, E=578, G=611, X1=466, W3=79. Command and output:

```
python3 gap/turnstheory/check_density_ledger.py gap/lowerbounds/conn/FIELD_n166_92_155.json
gap/turnstheory/density_ledger_check.log
```

The new checker uses the audited integer microtiles, not the searcher's
floating-point quarter-centroid code. The algebra above proves V1 for
all sizes; the example is a consistency check.

## V2.2. Endpoint restoration — PROVEN from audited inputs

Let S* be the UNION of crossing-pair sets of the four width-two side
strips, and write s=|S*|. Membership means both edges have an endpoint
at depth zero or one of the SAME side. Let N=2n-60, L be the number of
retained candidates, and D_loss=N-L. For now retain the audited rule:
discard uncharged candidates and candidates with an inward exception.
Let A be the sum of their audited endpoint penalties. Then D_loss<=A.

The oriented beta=1 certificate has error 29/4 per half walk. Summing
eight halves and using the audited strip overcount gives

```
A <= sum_sigma X_sigma-4n+58 <= s-4n+1162.
T := s-(4n-2)  satisfies  T+1160 >= A >= D_loss.       (V2)
```

All constants are conservative. The first inequality also holds for
the smaller penalty table that discards only uncharged candidates.
Dropping the exception rule would change L2's input family, so that
change must be stated rather than silently assumed.

**Pair-ledger contract.** B is contained in S*, and |B|>=4n-24. Choose
B0 subset B with exactly 4n-24 pairs. Set b_z=1 on B0 and zero elsewhere,
and set e_z=1-b_z on S*, zero elsewhere. Then

```
sum b_z=4n-24,
sum e_z=s-4n+24 >= D_loss-1138 >= p*D_loss-1138
```

for every 0<=p<=1. Thus L3 is proved for the phase-1 pair ledger IF f
and h use only pairs outside S*. Here e spends ALL residual S* capacity;
its spare capacity is exactly zero. To retain spare capacity, choose a
smaller fractional e paying only min(p*D_loss, available capacity),
and prove the repair claim with that actual residual allocation.
Also, s is the union count, not sum_sigma X_sigma: their difference is
bounded by 1104, not identically zero. These correct Part A's two
accounting statements without changing its endpoint conclusion.

## V2.3. Recommended mixed ledger — PROVEN accounting

Put U=X-s, the number of crossing pairs outside S*. Since E=T+U, for
any 0<=lambda<=1 define the atomic capacity

```
nu_lambda = lambda*(unit masses on pairs outside S*) + (1-lambda)*mu.
sum nu_lambda = E-lambda*T,
E+1160*lambda = sum nu_lambda + lambda*(T+1160).       (V3)
```

Both terms on the last right side are nonnegative. The second is the
side reserve and, by V2, supplies at least lambda*D_loss. Thus any
lambda>=p restores every lost candidate at price p, up to the displayed
constant, while leaving ALL nu_lambda available for L2 and connectivity.
The reserve is an aggregate side budget; no unproved local routing of
gap atoms to endpoint rows is assumed.

For the first milestone choose p=lambda=2/3. The explicit L2 currency is

```
2/3 per crossing pair outside S*;
1/6 per uncovered quarter, one-quarter crossing, and W3 unit.          (V4)
```

The second line includes actual atoms inside side strips. This is safe
because V3 already splits the total budget. The pair term still excludes
S*. Claims about raw crossing ownership must not be substituted for
these atom capacities. Searcher's identity II with B is also valid up
to its corner constant, but replacing B by S* is needed for this L3
plug-in. The assertion that lambda=1/2 pays 1/4 per bad quarter applies
only where the excluded pairs' overlaps are absent. It is not a global
pointwise bound, and does not follow after excluding all of S*.

## V2.4. Exact open contract for L2 and the 6n extension

**L2(p,lambda), CONJECTURE.** For every even n>=32 and every closed
Hamiltonian tour, use its ACTUAL retained candidate family C, including
arbitrary missing radii. Assign nonnegative f_(alpha,i) from the atoms
alpha of nu_lambda to i in C. Require

```
sum_i f_(alpha,i) + h_alpha <= nu_lambda(alpha),
sum_(alpha,i) f_(alpha,i) >= p*L-C_flux.              (V5)
```

C_flux must be absolute. A finite-local proof should state its collar
radius and allowed assignments; a transport proof must instead give
explicit conservation and endpoint rules. In either case internal
potentials must cancel globally: no uncharged allowance per retained
path, charged run, window, fold, or junction is available. Use height
flux omega, not raw knight-edge flux. Treat arbitrary exterior states,
or prove the structure lemma that restricts them. A lemma only for a
consecutive run of charged radii is insufficient unless its losses sum
to an absolute constant across the actual family.

For the first milestone set h=0. V2–V5 then give

```
E >= p*L+lambda*D_loss-C_flux-1160*lambda
  >= p*N-C_flux-1160*lambda,
X >= (4+2p)n - O(1).                                (V6)
```

Hence p=lambda=2/3 would prove 16n/3-O(1), with endpoint restoration
already supplied. To reach 6n, prove additionally
`sum h_alpha>=2n/3-O(1)` using the SAME capacities in V5. The fixed-strip
repair price of Claim 28 is not yet a price in this mixed currency; a
joint conversion or new certificate is required. The pair-ledger option
lambda=1 remains an algebraic possibility, but its unrestricted local
flux premise fails on W3. It requires the revised corner contract above.

**Updated status:** L0 and V1–V3 are proved; L3 is proved under the stated
pair or mixed contract. L2 at p=2/3, the needed unrestricted structure
lemma, universal repair obligations, and residual repair pricing remain
open. The main next test is V5 in currency V4, with the side reserve
already removed. The excess identity does not itself prove wall tension
or prevent endpoint-local charge from exhausting all local capacity.

---

# Original phase-1 skeleton (historical)

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
