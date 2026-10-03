# Scalar side-price reduction — 2026-10-03

Claims 39–40 passed the quarter-payment kernel and its conditional
logic. PROOF_5N_PLAN.md Section 9 now reduces GLOBAL 5n to a weaker
scalar side price, using the joint-test reserve to pay all failed-end
paths. R4 in REQUESTS.md gives the current contract. Hall constraints
remain relevant only if private L2 payments are also required. The
universal scalar certificate remains OPEN; no 5n theorem is claimed.

---

# Half-price hand step — 2026-10-03

See PROOF_5N_PLAN.md for the new quarter-payment hand argument and the
remaining side-certificate specification. It proves private half-price
payments for paths with a bad middle square, using distinct payable
quarters. The new argument awaits independent audit. Paths with
residual demand have a good middle and bounded end zones; their joint
residual-capacity price F1 remains open. No 5n theorem is claimed.

## Deferred lead: zigzag colour balance — 2026-10-03

**UNCHECKED here; low priority, behind F1.** Chief Researcher relays
Integrator's claimed obstruction: cutting a (1,-1) zigzag field along
direction (a,b) leaves stubs of one colour, with reported rate
3|a-b|/2 per unit length. The claim suggests restrictions on joining
such a region to a physical board side or to a straight field across
a (1,2) interface. The normalization of “unit length,” the precise cut,
and the allowed boundary repairs must be checked in the proof before
using that formula. This note is not an assertion of the claim.

Possible use: Claim 35's half-price wall uses zigzag exteriors. A
proved cost for closing or transitioning those exteriors might restore
a higher effective flux price in closed tours, potentially the 2/3
route. Colour imbalance alone does not establish that price: identify
how a whole zigzag region balances all its boundary pieces, quantify
necessary repairs, and charge them without using capacity already paid
to flux, endpoint restoration, or connectivity. To affect L2, locate
that cost inside the retained paths' eligible collars. Other exterior
phases or wall mechanisms would also need coverage before claiming a
universal 2/3 price. F1 and the half-price v4 route remain the active work.

---

# Skeleton v4: half-price flux plus separate connectivity credit

2026-10-03. **Current research contract; flux and connectivity lemmas
remain OPEN.** This section supersedes the p=2/3 currency recommendation
below. The audited lower bound remains 5X>=24n-13012 for even n>=32
(Claim 31). No 5n or 6n theorem is claimed by this plan.

## 1. Decision and the wall's precise scope

Use p=lambda=1/2 in the mixed ledger. Searcher's Section 7.1 gives a
(1,2) periodic wall of half a crossing per L-infinity level; the earlier
diagonal wall also attains half-price in the half-mixed currency.
Thus a universal flux-only wall price above 1/2 is not an available
local input. Claim 35 now audits the achieved half-price and an explicit
acyclic plane extension with matching zigzag exteriors. It does not
audit optimality of the large minimum-mean graph.

This does NOT yet refute the exact closed-tour L2-v3(2/3,10) conjecture.
The audited plane extension is acyclic, but supplies neither
Hamiltonian completion nor retained candidate endpoints. An entire
path's collar can receive resources far from its wall intersection.
See WALL_1_2_SCOPE.md for the exact missing hypotheses. The claim that
the 16n/3 route fails must be read as a failure of the proposed universal
wall-price input, not as a proved impossibility for closed tours.

The formal p=2/3 conjecture is left unresolved; it is no longer the main
route. Improvements above 5n in THIS skeleton must use a separate
connectivity allocation rather than increasing the flux price.

## 2. Ledger and endpoint restoration, unchanged proved inputs

Let C be the actual retained family from the audited corner paths,
N=2n-60, L=|C|, D_loss=N-L. Let S* be the union of the four width-two
side crossing sets, s=|S*|, E=X-4n+2, T=s-4n+2, and U=X-s.
Let mu put mass 1/2 on each uncovered quarter, each one-quarter crossing,
and each W3 unit, with W3=0 at multiplicity zero. The exact identity is
mu(total)=E. The audited beta=1 restoration gives T+1160>=D_loss.

Use the atomic capacity

```
nu = (1/2)*(unit pair masses outside S*) + (1/2)*mu;
E+580 = nu(total) + (1/2)*(T+1160).
```

Thus nu has mass 1/2 per non-S* pair and mass 1/4 per hole, one-quarter
crossing, and W3 unit. The separate nonnegative side reserve pays
D_loss/2. It is not available again for flux or connectivity. Keeping
this mixed ledger avoids the unproved pure-currency L2/L3 recombination.

## 3. Exact half-price flux statement

For every even n>=128 and every closed Hamiltonian tour, form C with
radii 12 through n/2-4, both endpoint residues, and both exception
exclusions. For each atom use its four edge endpoints if it is a
crossing atom, and its closed quarter triangle if it is a hole or W3
atom. Eligibility means the whole support lies within L-infinity
radius TEN of ONE dual vertex of the candidate path.

Conjecture: there is an absolute C_flux such that every such tour has
nonnegative payments f_(alpha,i) and deficits delta_i satisfying

```
f_(alpha,i)=0 unless alpha is eligible for i;
sum_alpha f_(alpha,i)+delta_i >= 1/2       for every retained i;
0<=delta_i<=1/2; sum_i delta_i<=C_flux;
sum_i f_(alpha,i) <= nu(alpha)             for every atom alpha.
```

This is individual demand with ONE total error, not aggregate payment
or an allowance per path/run/window. The radius-ten interior support
argument still applies. End-zone paths still need a side-local proof
in the same nu capacity. Fixed corner exceptions can consume a fixed
part of C_flux. A finite local certificate must cancel its internal
boundary terms; neither W3 nor the half-price wall proves this lemma.

With this flux lemma and the proved reserve,

```
E+580 >= L/2-C_flux+D_loss/2 = n-30-C_flux,
X >= 5n-(612+C_flux).
```

The smaller-board range can be covered by increasing a final constant.
A proof of this half-price statement alone is a valuable Pareto result.

## 4. Connectivity: extra demand in the SAME capacity

To improve the coefficient, find nonnegative h_alpha together with f,
not after a flow that has already spent the resource, such that

```
sum_i f_(alpha,i)+h_alpha <= nu(alpha),
sum_alpha h_alpha >= kappa*n-C_conn.
```

The f demands and total-deficit bound remain those above. Then

```
X >= (5+kappa)n-(612+C_flux+C_conn).
```

In particular **6n needs kappa=1: n-O(1) extra connectivity credit**.
The old 2n/3 connectivity target belonged to a p=2/3 flux calculation
and is insufficient here; it would give only 17n/3. Any positive kappa
would improve the leading coefficient above five in this framework.

A connectivity proof must identify forced repair obligations of ONE
closed tour, prove a lower bound on their number or total weight, and
pay them from the unused capacity in this inequality. A crossing price
in a restricted repair strip is not automatically a price in nu.
Claim 30 permits one H/V bit per uninterrupted good ribbon run, not
one bit throughout a connected good domain. Run separation, boundary
ports, and costs at defects must remain in the topological argument.
Local periodic wall/cylinder examples do not supply this global lemma.

## 5. Completed-tour evidence and exact finite tests

All 345 saved records were covered (193 distinct validated tours,
n=32..260; 39 distinct boards with n>=128). At R=10:

| Currency and price | Maximum Delta | Positive-deficit tours |
| --- | ---: | ---: |
| mixed nu_(1/2), p=1/2 | 0 | 0 |
| mixed nu_(2/3), p=2/3 | 25/2 | 7 |
| pure non-B pairs, p=1/2 | 0 | 0 |
| pure non-B pairs, p=2/3 | 0 | 0 |

The mixed p=2/3 LF5 deficits grow over saved sizes from zero at n=104
to 10/3 at 156, 8 at 208, and 25/2 at 260. This is a finite warning,
not an all-size disproof. The worst Hall cut was independently checked.
Both tables contain every tested tour and n; see HALL_V3_RESULTS.md,
HALL_CURRENCY_RESULTS.md, and the full report in FINDINGS.md.

The half-price flux test is exact integer max-flow: scale nu by four,
give each retained path demand two, each non-S* pair capacity two,
and each excess-atom unit capacity one. A min-cut decides the minimum
total deficit for one tour. It does not decide the universal lemma or
supply h. A finite certificate for the universal joint allocation still
requires specified interface states and a proved rule for joining them.
The saved-tour tests show no half-price obstruction to guide one yet.

## 6. Proof size and finite inputs

This v4 is a short conditional reduction, not a new proof. Its proved
inputs are the exact tile ledger, the audited endpoint-restoration
certificate, and local support from the sixteen hole certificates.
Its missing inputs are universal half-price allocation and connectivity
in the residual mixed capacity. The wall witness is a stop test for a
stronger local price, not a premise of the conditional 5n inequality.
No new heavy computation was run for this update. The saved-tour runs
and independent worst-cut check are recorded with commands in FINDINGS.

---

# Currency decision for skeleton v3 — 2026-10-03

**Use pure non-B crossings for the p=2/3 route. Keep the mixed
p=lambda=1/2 route as the simpler 5n target.** The same 193 saved tours
all have zero strict-radius-10 Hall deficit in pure non-B crossings,
at both prices. The mixed p=2/3 test has seven positive deficits and
reaches 25/2 on LF5 n=260. See HALL_CURRENCY_RESULTS.md and FINDINGS.md.
These are exact finite tests, not a universal allocation proof.

## The pure-crossing L2 statement and required L3 repair

Let B be the UNION of outer-column crossing-pair sets. Give every pair
z outside B unit capacity. Keep v3's actual retained paths, strict
radius R=10, individual demands p=2/3, and per-path deficits whose TOTAL
is at most one absolute C_flux. Replace the nu_(2/3) atom capacity by
this unit-pair capacity. This is the recommended new L2 conjecture.
The finite max-flow test is source-to-path capacity two and
pair-to-sink capacity three, in units 1/3. It passes every saved tour.

This changes both the weights AND the exclusion set: B is smaller than
S*. It is not the lambda=1 instance of V3, which excludes S*. In the
old worst 94-path Hall set, pure currency has 109 pairs: 21 outside S*
and 88 in S* minus B. Those 88 pairs explain why endpoint accounting
must be repaired rather than carried over unchanged.

With U_B=X-|B| and T_B=|B|-(4n-2), the exact ledger is E=U_B+T_B.
The audited |B|>=4n-24 implies E>=U_B-22. This pays retained-path
flux from U_B; it does not restore the discarded paths. V2's proved
L3 uses S* capacity, including pairs now eligible for pure L2.

A sufficient joint replacement is: choose B0 subset B of size 4n-24,
and find nonnegative f_(z,i), e_z (and h_z if used) with

```
f_(z,i)=0 unless z is outside B and strictly eligible for i;
e_z=0 outside S* minus B0;
sum_i f_(z,i)+e_z+h_z <= 1-1_(z in B0) for every crossing pair z;
sum_z f_(z,i)+delta_i >= p for every retained i;
sum_i delta_i <= C_flux;
sum_z e_z >= p*D_loss-C_end.
```

All constants are absolute. This single shared allocation would give
`X >= (4+2p)n - (24+60p+C_flux+C_end)` when h=0, hence
`X >= 16n/3 - (64+C_flux+C_end)` at p=2/3. The present pure flows test
ONLY f; they do not establish this joint statement. The next proof
obligation is L2/L3 joint pricing of the side and end zones, alongside
universal sharing control. The old standalone beta=1 L3 certificate
cannot simply be added to the new L2 payment.

For the p=1/2 alternative, retain the existing mixed ledger V3 and its
proved restoration reserve. A universal L2-v3(1/2,10) with total error
C_flux would give `X >= 5n-(612+C_flux)` without this currency change.
All saved tours meet its individual demands with zero deficit. It
still needs a universal allocation proof and end-zone argument.

## Wall input and scope

Searcher Section 7 certifies the stated straight-wall widths: axis
price 2/3 in the tested currencies; at diagonal width four, waste price
zero, half-mixed price 1/2, and pure crossing price 2/3. This supports
the currency choice and the simpler half-price target. The result is
restricted to those widths and boundary conditions, not all slopes,
junctions, variable-width walls, or complete tours. No global ribbon
word is assumed; Claim 30's one-bit-per-run restriction remains.

Proof size and finite inputs: this is a budget correction and a choice
between two open routes. New evidence is 386 pure max-flows on 193
validated tours; the mixed results are the earlier 386 exact flows on
the same hashed boards. The new comparison driver has 55 lines and its
coverage/resource checker has 43 lines, in addition to the shared
geometry, flow, and support implementation. No new universal theorem
or finite-state gluing certificate is supplied.

---

# Screening update — 2026-10-03

The exact R=10 test now covers 193 distinct saved tours. At p=lambda=1/2
all deficits are zero. At p=lambda=2/3, seven are positive; LF5 grows
from zero at n=104 to 25/2 at n=260. The worst cut is independently
checked. See FINDINGS.md and HALL_V3_RESULTS.md. This is finite evidence:
it neither proves a uniform deficit bound nor proves unbounded growth.
The p=1/2 route remains a useful simpler target.

---

# Skeleton v3: individual demands, one global deficit, and test scope

2026-10-03. **L2 CONJECTURE / GAP (Claim 29).** This section supersedes
the L2 quantifiers in V2.4. The exact tile ledger and L3 remain proved.
The audited strip result is now X>=(24n-13012)/5, even n>=32 (Claim 31).
No improvement follows from this skeleton until the allocation below
is proved. The old reduction's coefficient-five ceiling is confirmed.

## 1. Exact proposed L2, with a fixed support rule

Fix p=lambda=2/3 and R=10. For each even n>=128 and each closed
Hamiltonian knight tour H, let C(H) be its ACTUAL retained candidate
family, using radii 12 through n/2-4, both endpoint residues, and both
exception exclusions from the audited proof. Retain arbitrary missing
radii. Do not replace C(H) by all charged curves of an open patch.

Use the mixed capacity nu_(2/3) from V3: mass 2/3 per crossing pair
outside the UNION S*, and mass 1/6 per uncovered quarter, one-quarter
crossing, and W3 unit. W3 contributes zero at multiplicity zero.
These are separate atom types. The two masses of a one-quarter
crossing outside S*, if present, are the two terms of the proved mixed
identity, not a second independent crossing budget.

Define the support of a crossing atom as the four edge endpoints; the
support of a hole or W3 atom as the closure of its quarter triangle.
An atom alpha is eligible for i if its ENTIRE support lies within
L-infinity distance R of some ONE dual vertex of path i. This is a
specific conservative convention; bounding-box intersection alone is
not the eligibility test. The radius-ten localization argument below
supplies at least one eligible non-S* pair for an interior witness.
For one-quarter crossing atoms use the four endpoints as well.

**L2-v3(2/3,10), CONJECTURE:** there exists a finite C_flux>=0,
independent of H and n, such that for every such H there exist
nonnegative payments f_(alpha,i) and deficits delta_i satisfying

```
f_(alpha,i)=0 unless alpha is eligible for i;
sum_i f_(alpha,i) <= nu_(2/3)(alpha)              for every atom alpha;
sum_alpha f_(alpha,i)+delta_i >= 2/3             for every i in C(H);
0 <= delta_i <= 2/3;
sum_i delta_i <= C_flux.                        (ONE total allowance)
```

The quantifier order is `exists C_flux, for all n,H, exists f,delta`.
It does not assert one universal finite local rule, and it does not
assert zero deficit in every free-halo patch. A finite local rule is a
possible sufficient proof, not an unstated requirement of the theorem.
The radius and price are fixed here to make the next test unambiguous;
a failure of this version would not disprove every fixed-radius price.
For connectivity, replace the capacity by nu-h with a jointly proved
nonnegative h. There is currently no such extra allocation.

Fixed corner exclusions must appear as delta_i, with their TOTAL
bounded by a constant. There is no error per path, per side row, per
run, per patch, or per artificial window boundary. Finitely many small
board sizes can be covered by increasing the final theorem constant.

L3 and this individual-demand statement imply the former aggregate
inequality and hence

```
E >= (2/3)*(2n-60)-C_flux-2320/3,
X >= 16n/3 - (2446/3+C_flux).
```

This is a conditional implication only. A smaller price, for example
p=lambda=1/2, would target 5n-O(1) and can be easier to prove. Report
its finite input size as well as its coefficient.

## 2. What Claim 29 stops, and what it leaves open

The audited forest patch has two retained-test-compatible charged
paths at radii 3 and 4, 46 crossings, and only one non-B crossing. A
zero-error unit-pair price above 1/2 fails on this open patch. All-B
side-hole patches also defeat a rule that demands an off-B crossing
at every retained endpoint. Radius-zero demand fails even on the
three checked completed tours. These are mandatory stop tests.

They do not decide L2-v3: its radii start at 12, R is positive, its
currency includes excess atoms inside the strips, and it permits one
absolute total deficit. Free halo ports can acquire further capacity
on completion. The completed-tour tests at radii 1,2,4,8 used non-B
unit pairs and generous bounding-box eligibility; their success is not
a check of the stricter mixed-capacity statement above.

Use W3 to divide the proof effort into interior witness allocation and
end-zone allocation, as detailed below. Both allocations must share
nu. The end-zone alternative using raw S* pairs requires a new joint
L2/L3 certificate. The beta=1 L3 certificate alone cannot price both
lost candidates and retained end zones. An interior crossing can serve
several nested radii; existence is not a price or a private assignment.

Claim 30 permits one H/V bit per uninterrupted good ribbon run.
Connected good domains need not have one global ribbon word. Any local
state model must retain separate run bits and their boundary ports;
it cannot join runs across defects for free. No global ribbon-word
reduction is assumed in L2-v3 or in the tests below.

## 3. The exact finite decision problem

For a GIVEN completed tour, construct its atoms and the strict radius-10
eligibility graph. Multiply all capacities and demands by six. Give
source-to-path arcs capacity 4, eligible path-to-atom arcs capacity
4*|C|+1, and atom-to-sink arcs capacity 4 for each non-S* pair atom and
1 for each excess atom. Compute exact integer maximum flow F. Then

```
Delta(H) = (4*|C(H)|-F)/6
```

is exactly the minimum total deficit in L2-v3 on that tour. Equivalently,

```
Delta(H) = max_(J subset C(H))
  [ (2/3)*|J| - sum_(alpha in N_10(J)) nu_(2/3)(alpha) ]_+.
```

This checks every subset, not only each single radius or each run.
The finite computation decides feasibility with a SPECIFIED C_flux on
that tour. It supplies a cut and its exact deficit on failure. The first
implementation should run on the three Claim 29 completed tours and
replay the saved patch stop tests under their own stated assumptions.
Patch deficits must not be labelled completed-tour obstructions.

For a FIXED board size, a finite exact search over Hamiltonian tours
and path subsets J can maximize this Hall deficit. Require connectivity,
full endpoint retention, full quarter multiplicities, all four strip
unions, and the eligibility rule above. A SAT/MILP witness or exhaustive
certificate then decides the fixed-size question. This is finite but
likely too large for the first experiment; max-flow on saved tours is
the cheap starting test. It needs no new strip transfer graph.

**Scope limit:** no finite set of patch tests, sizes, or saved tours
decides whether sup_(n,H) Delta(H) is finite. W3 proves bounded support,
not a finite-state reduction of this universal allocation problem.
Claim 30 removes the proposed global-word shortcut. A universal proof
still needs a gluing theorem or an explicit bounded-state certificate.

One possible sufficient certificate search is a rational discharging
LP on a FIXED window/halo and a FIXED interface-state scheme. Variables
are local fractional payments and interface potentials. Constraints
must check every admitted edge/quarter pattern and marked path demand,
atoms used by neighbouring windows, and every allowed interface match.
Internal potentials must cancel exactly; only the four physical-side
endpoints and fixed corner exceptions may contribute to C_flux.
Separate ribbon-run bits and arbitrary missing-radius marks belong in
those states. With a fixed finite scheme, feasibility is a finite LP
question and an exact rational solution is checkable. Infeasibility
rejects that scheme only. A state scheme and completeness/gluing proof
have NOT yet been supplied; calling this a finite computation that
already decides the all-tour conjecture would overstate the evidence.

## 4. Status, proof size, and next finite work

This v3 is a corrected conjecture plus a precise finite max-flow test,
not a new proof. Its mathematical reduction uses the audited ledger,
L3, and fractional max-flow/min-cut. Universal finite inputs are still
missing: the shared interior allocation and the joint end-zone price.
The W3 localization uses the sixteen hole certificates named below.
The next concrete computation is mixed-capacity radius-10 max-flow on
the saved completed tours, reporting exact cut sets and Delta(H).
Do not launch a large transfer graph before fixing its interface states.

Claim 31 needs no further strip search. Its audited proof status is
recorded in PROOF_R3.md; no result index or post is changed here.

---

# Skeleton v2 update: bounded support and a separate end-zone lemma

2026-10-03. **Local support ARGUMENT from certified W3 inputs; allocation
and end-zone prices OPEN.** The risk that an interior hole requires a
crossing arbitrarily far away is removed. W3 does not yet give a price
per retained path: several paths can share one local crossing witness.
This section is the current L2 contract and supplements V2.2–V2.4.

## L2-support: explicit conservative radius

KT Lower Bounds' W3 supplies the following finite inputs. A hole in a
square centred within a degree-two 7 by 7 core forces a crossing between
edges touching that core. Near a board side, a hole at square depth
4, 5, or 6 forces a crossing outside that side's width-two strip among
edges touching a 12 by 9 core anchored on the side. Each model includes
a width-two degree-at-most-two halo. At multiplicity at least two, the
audited tile lemma already supplies a crossing of the covering edges.
An overlap of two width-two strip edges lies only at square depths <=3.

For a square with lower-left coordinates (d,c), the interior core has
coordinates [d-3,d+3] by [c-3,c+3]; all relevant edge endpoints lie in
[d-5,d+5] by [c-5,c+5]. If its depth from every side is at least seven,
no such edge can touch a width-two strip. For depths 4–6 from one side,
use the side core: depths 0–11 and rows c-4 through c+4. Its edge
endpoints have depths 0–13 and rows c-6 through c+6. Thus every endpoint
of the crossing witness is within L-infinity distance at most TEN of
the dual vertex at the centre of the witness square. This conservative
radius avoids relying on the informal estimate of about six cells.

Exclude fixed corner boxes when these windows approach a second side.
For example, treat vertices within distance 32 of two adjacent sides
separately, and take n>=128 for this support discussion. Smaller n
form a fixed finite range for any later asymptotic theorem. For the
audited corner paths, at most a fixed number of small radii enter these
boxes. Outside them, the side window cannot acquire a crossing that
belongs to a different side's strip. The witness is therefore outside
the UNION S*, not merely outside the chosen side's strip.

Split each retained path into end zones, consisting of its vertices
whose square has depth <=3 from a side, and the remaining middle.
A nonzero-flux step is adjacent to a bad quarter in one of its incident
squares. If a middle square is bad, the preceding lemmas supply a
non-S* crossing within radius ten of a path vertex. Otherwise all
nonzero-flux steps are incident to end-zone squares. Each end zone has
bounded length on one path, but there are linearly many path ends.
They require a side lemma, not an O(1) global deletion.

This proves existence of a bounded-support witness, conditional on the
geometric encodings of the cited finite lemmas. It does not assign
capacity or imply that every witness crossing is private to one path.

## L2-price: allocation contract with sharing

Partition the actual retained family into I (paths assigned an interior
witness) and Z (paths assigned to the end-zone case), after the fixed
corner exceptions. Use deterministic choices or include all admissible
choices in the certificate. In the mixed ledger V3, the available pair
mass is lambda per non-S* crossing; the remaining mass is (1-lambda)*mu.
A witness crossing can have zero mu mass, so existence alone does not
pay p in this currency. The side reserve is already committed to L3.

The interior task is to allocate from radius-ten support neighbourhoods
N(i), with one capacity constraint per atom, so that

```
sum_alpha f_(alpha,i) >= p                  for each i in I,
sum_i f_(alpha,i)+g_alpha+h_alpha <= nu_lambda(alpha).
```

Here g is the allocation reserved for the end-zone lemma and h is the
connectivity allocation. Any allowed deficit must sum to an absolute
constant over the whole board. For a fractional allocation with fixed
g and h, the relevant condition is the capacitated Hall inequality

```
p*|J| <= sum_(alpha in union_(i in J) N(i))
             (nu_lambda(alpha)-g_alpha-h_alpha)
```

for EVERY subset J of I, with a single global allowance if needed.
Checking only individual paths or consecutive radii does not establish
this condition. Radius ten bounds the number of neighbouring nested
radii; it does not certify the proposed price 2/3. The next finite
input must control sharing and preserve its boundary terms when local
windows are joined.

## L2-end: separate side lemma, still open

Prove `sum g_alpha >= p*|Z|-C_side` in the SAME residual mixed capacity,
with C_side absolute over four sides. The certificate must observe the
actual height-flux test, retention exceptions, both orientations, and
arbitrary missing radii. A path with two charged end zones must be
assigned or split once, not counted twice. Artificial window cuts need
potentials whose terms cancel; an error per end or per run is invalid.

Alternatively use raw S* pairs, but then replace the existing L3
allocation by a joint side certificate that simultaneously pays
p*D_loss and p*|Z| after the boundary baseline and all interior/repair
allocations. The separate beta=1 restoration inequality pays lost
candidates only; it supplies no free capacity for retained end zones.
This is the exact interface needed between L2-end and L3.

Together L2-price and L2-end would give V5. With L3, p=lambda=2/3 would
then give 16n/3-O(1). Neither that price nor a new lower bound is proved
by localization. A smaller price with a short, small-check proof is
also a useful result under the Pareto criterion.

## Finite inputs and proof size

This update adds a short geometric support argument and two open
allocation contracts; it adds no theorem coefficient. It uses four
interior CNF/DRUP pairs and twelve side CNF/DRUP pairs (four quarter
orientations at each of depths 4,5,6), plus the audited tile/flux lemma.
The fold-stack tiling result explains the interior mechanism but is
not an extra premise of this direct hole-certificate route. A test of
random fold stacks alone would not prove that result for all stacks.

I read the generators and producer check logs for the interior and
depth-4/5 lemmas. I also checked the four depth-6 proofs directly:
784, 680, 621, and 633 RUP additions passed for b,l,r,t respectively.
All measurements are from 2026-10-03. No SAT search was rerun. To check
the exact finite proofs, use these read-only commands from the root:

```sh
for q in b l r t; do
  python3 w-lowerbounds/check_drup.py gap/lowerbounds/windows/hole_k7_${q}.cnf gap/lowerbounds/windows/hole_k7_${q}.drup
done
for d in 4 5 6; do
  for q in b l r t; do
    python3 w-lowerbounds/check_drup.py gap/lowerbounds/windows/sidehole_W12_H9_d${d}_S_${q}.cnf gap/lowerbounds/windows/sidehole_W12_H9_d${d}_S_${q}.drup
  done
done
```

These commands check the supplied CNF proofs. The geometric encodings
and the support/gluing argument still need independent theorem audit.

---

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
