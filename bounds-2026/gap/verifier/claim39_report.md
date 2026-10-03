## Claim 39: half-price quarter-payment hand kernel — 2026-10-03

**Verdict: PASS for Sections 2–3 of gap/turnstheory/PROOF_5N_PLAN.md and the conditional reduction to F1, with the flux wording clarified below. F1 remains GAP/OPEN. No 5n theorem is established.** The proof is a valid private allocation in the stated mixed currency, rather than an aggregate support count. I also checked the ledger and final constant needed for its intended use.

### 39A. Currency and quarter-payment rule — PASS

Use the audited full-tour quarter multiplicities and crossing pairs. Write X1 for the number of pairs with a one-quarter overlap, and define W3(q)=binomial(m(q)-1,2) for m(q)>=1, zero for m(q)=0. The exact identity is

    G+X1+W3 = 2(X-4n+2) = 2E.

For S* the UNION of the four width-two strip pair sets, T=|S*|-4n+2, the stated capacity therefore satisfies

    nu(total) = (X-|S*|)/2 + E/2 = E-T/2.

A pair outside S* has a half-unit pair atom. Hole atoms, X1 atoms and each W3 unit have quarter-unit capacity. These are distinct summands even when associated with the same physical crossing or neighbourhood.

The four-case allocation is correct:

* A hole uses its own quarter-unit atom.
* A quarter with multiplicity at least three uses one of its W3 units; at least one exists. W3 units at different quarters are distinct.
* At multiplicity two, a pair outside S* pays a quarter unit. The two tiles overlap in at most two quarters, so the same half-unit pair atom receives at most two requests, even if the requests come from different paths.
* At multiplicity two, a pair in S* with one-quarter overlap pays from its X1 atom. This atom can receive a request at only that quarter.

The only excluded bad-quarter type is multiplicity two with its pair in S* and a two-quarter overlap. Calling this type “unpaid” means that the specified direct rule does not pay it; it does not rule out payment from other nearby residual atoms in F1.

This proves the allocation for ANY set of distinct payable quarters, including all payable quarters at once. It does not require a hole-to-crossing injection, an assumption about phases, or a no-sharing conjecture. In particular, using one W3 unit at a multiplicity-four quarter is safe even though that quarter has several incident crossing pairs.

### 39B. Locality and distinct path squares — PASS

If a knight tile covers a quarter of a square, its endpoint box contains the full coordinate intervals of that square. The integer endpoint extrema have coordinate span at most two, so each endpoint is within L-infinity distance 3/2 of the square centre. Both edges of a pair covering the quarter obey this bound. A closed quarter triangle is within distance 1/2 of its centre. Thus the whole support of the chosen atom is within radius two of ONE dual vertex of the path, as required; radius ten is more than sufficient. This uses the precise support definition, not a bounding-box intersection with the union of a path neighbourhood.

A dual vertex is the centre of one unique unit square. The audited candidate paths are vertex-disjoint: in a corner frame their maximum square coordinate identifies their radius, and the four corner boxes do not meet. Therefore the chosen quarters for different paths are distinct. Picking any two payable quarters per eligible path and applying the global quarter rule gives a simultaneous half-unit allocation. This proves all subset/Hall inequalities for those paths, including when one crossing pair supplies quarters to two different paths.

The author support check passes: four unoriented move types, 16 covered quarters, maximum endpoint distance 3/2. The independent check uses the previously audited exact polygon-quarter geometry and reproduces these values without importing the author script or its microtile implementation.

### 39C. Reduction to end zones — PASS

The square identity m_B-m_R+m_T-m_L=0 implies that exactly one bad quarter is impossible. Every bad square has at least two bad quarters.

Membership in a side's width-two pair set means BOTH edges have an endpoint at depth zero or one from that same side. Each edge endpoint box reaches depth at most three. Hence its tile, and therefore the pair's overlap, cannot have positive area in a square starting at depth at least three. The source uses the weaker safe cutoff four; that is valid. Every quarter in its defined middle is payable if it is bad.

A bad middle square therefore supplies two payable quarters and pays its path in full. After choosing min(2,s_i) quarters for every path, the explicit atom allocation leaves a nonnegative residual capacity nu'. Any path with positive residual demand has no bad middle square. This reasoning concerns actual full-tour multiplicities, not a local patch with missing exterior edges.

For even n>=128 and r>32, the corner path has exactly six squares at square-depth below four: depths 1,2,3 at each of its two ends. The opposite board sides are far away. The remaining squares are in the middle. At each corner there are 21 possible radii 12 through 32; discarding these only for payment loses at most 84 paths, hence 42 units. Keeping them in L and D_loss, while assigning their unmet demand to the one total error, is consistent. C_side must include this allowance, as the source states.

Retention excludes B overlaps from every path square by the audited endpoint exception rule. Thus an unpaid quarter on a retained path has its covering pair in S* minus B. This exclusion is inherited from the audited retained family; it is not true merely because a candidate path has the right radius.

**Wording repair:** “the flux across the good middle is zero” should say “zero modulo three.” For a step with two good adjacent quarters, the flux formula gives omega=3 chi(a)(1-g), which need not be the integer zero. Its residue is zero, which is exactly what the charge reduction uses. Include the transition steps between the end zones and the good middle when assigning the remaining charge to the ends.

**Optional tightening:** with square depth defined as min(x,y,n-2-x,n-2-y), the endpoint-box argument actually makes every bad square of depth at least three fully payable. A deficient path can therefore have bad squares only at depths one and two, four end squares in total. The stated six-square reduction is conservative and requires no change for correctness.

### 39D. Independent checks — PASS

New check: claim39_check.py, standard Python, one process, no author imports. Evidence is in claim39_check.json/log and claim39_sources.json. It checks:

* the exact endpoint support bound on all 16 template quarters;
* all 81 choices of half multiplicities in {0,1,2}, confirming the square identity and exclusion of one bad quarter;
* 232 overlapping pairs from a sufficient local set of width-two side edges, all with overlap-square depth at most two;
* candidate-square disjointness, exact candidate count 2n-60, the 84 small-radius candidates, and the six end squares at n=128,130,144,288;
* the complete atomic allocation on two independently validated tours, choosing EVERY payable quarter at once, and checking that no atom exceeds its capacity;
* the exact mixed identity and the residual-good-middle implication on those candidate paths.

For FOLD n=96 the check obtains X=720, |S*|=541, E=338 and 4 nu=1034. It simultaneously assigns 901 quarter units to all payable quarters without overuse. At n=144 it obtains X=1024, |S*|=781, E=450, 4 nu=1386 and 1253 assigned quarter units. These finite runs support the elementary allocation proof; they do not establish F1. The n=96 run is a local-allocation test, not an assertion of the proposed theorem's n>=128 scope.

Commands:

    python3 gap/turnstheory/check_quarter_payment_support.py
    python3 gap/verifier/claim39_check.py

### 39E. Conditional 5n conclusion and exact remaining obligation

The audited beta=1 certificate has error 29/4 per oriented half walk. Eight halves give 58. The strip sum exceeds the S* UNION count by at most 1104, so

    D_loss <= A <= |S*|-4n+1162 = T+1160.

Combining this with nu(total)=E-T/2 gives the exact stated reserve identity and restoration inequality:

    E+580 = nu(total)+(T+1160)/2,
    (T+1160)/2 >= D_loss/2.

If F1 supplies the residual payments in the SAME nu' after the baseline quarter choices, with total error at most C_side, then nu(total)>=L/2-C_side. Since L+D_loss=2n-60,

    E+580 >= n-30-C_side,
    X >= 5n-(612+C_side),       for even n>=128.

The constant and sign pass. The 42-unit small-radius allowance is already included in C_side and is not to be added again. To extend to smaller even boards by the trivial X>=0 bound, one may enlarge the final constant to at least 630.

F1 is the single remaining NEW price lemma in this conditional chain. Its existence is not proved by the hand kernel. In particular, fully paid paths may already have spent pair capacity near a deficient path's end windows. The side proof must use the actual residual atom capacities and one total error, not independently reset each window's budget. The good-middle reduction localizes possible path defects and the residue calculation; it does not automatically prove that end-local resources suffice. As written, F1 allows radius-ten eligible resources along the path. A certificate restricted to end windows would be a sufficient, potentially stronger implementation and needs its own domination and joining proof.

The proposed finite-state description in Section 4 is explicitly a specification, not an audited completed reduction. No claim is made here that it has finitely many sufficient marks with proved compatibility, that an LP/transfer certificate exists, or that W1/W3 substitute for it. Their support results and the full allocation are different statements.

**Pareto profile:** the new proof consists of four local allocation cases, the square identity, disjoint square centres and a bounded end-zone argument. It needs no new SAT or large graph certificate. Its inherited finite inputs are the audited tile/flux facts and beta=1 endpoint-restoration certificate. If F1 admits a short side proof, this is a valid simple route to 5n. At present the hand kernel passes and F1 remains open. Claim 39 is complete; no author files were edited.
