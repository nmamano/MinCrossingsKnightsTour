# Turns and crossings: findings

Date: 2026-10-02. Author: KT Turns Theory (Astra).

## 1. Turns: one-page proof

**PROVEN.** Every closed knight's tour on an n by n board, n >= 8, has at least **8n-28 turns**. The elementary argument below gives 8n-64. The exact corner certificate in Section 2 improves the constant to 28. Both bounds also hold for spanning degree-two subgraphs with several cycles. Thus the asymptotic lower coefficient 8 is proved; the exact bound 8n is not proved.

**Four-column lemma.** The first four columns contain at least 2n turns.

Index these columns by 0,1,2,3, and let T_i count their turns. Let B count chosen edges between column 3 and columns 1 or 2. Every cell in column 0 is a turn, so T_0=n.

For each cell v in columns 1 or 2, let p(v) count its chosen edges to columns 0 or 3. Its turn indicator is at least p(v)-1. For p<=1 this follows from nonnegativity. For p=2, the two moves cannot be opposite: the permitted horizontal displacements are {-1,+2} in column 1 and {-2,+1} in column 2.

Column 0 has 2n incident edges, all to columns 1 or 2. Hence sum p(v)=2n+B. Summing over the 2n cells gives T_1+T_2>=B.

For each cell v in column 3, let q(v) count its edges to columns 1 or 2. Its turn indicator is at least 1-q(v). If q=0, both moves go right, so v is a turn; if q>=1 the bound is nonpositive. Since sum q(v)=B, we have T_3>=n-B. Thus

    T_0+T_1+T_2+T_3 >= n+B+(n-B) = 2n.

**Global count.** Apply the lemma at all four sides. The sum of strip turn counts is at least 8n. Opposite strips are disjoint for n>=8. Only the four 4 by 4 corner squares are counted twice, so at most 64 turns are counted twice. Therefore T>=8n-64.

**Exact improvement.** The local inequalities in the lemma have unavoidable slack near each corner. Section 2 proves that the corner overlap minus this slack is at most 7 per corner. Therefore **T>=8n-28**. For a w by h rectangle with w,h>=8, the same proof gives T>=4(w+h)-28.

The strip coefficient 2 is sharp: in a half-plane, choose edges (0,y)--(1,y+2), (0,y)--(2,y+1), and (x,y)--(x+2,y+1) for x>=1. Columns 0 and 1 turn; all later columns are straight. Every cell has degree two, and there is no cycle.

## 2. Exact corner certificate for the constant 28

**PROVEN, finite certificate.** This section gives all certificate data. No solver result is needed to check the bound.

For a cell at distance i=0,1,2,3 from one side, define its local lower bound L_i as follows, using the two chosen moves:

    L_0 = 1;
    L_1 = (number of neighbours in columns 0 or 3) - 1;
    L_2 = (number of neighbours in columns 0 or 3) - 1;
    L_3 = 1 - (number of neighbours in columns 1 or 2).

Set L_i=0 for i>=4. The four-column proof shows t(v)>=L_i(v). It also shows that the sum of L_i over one whole side strip is exactly 2n. Let L(v) be the sum of the four side contributions at v. Then sum L(v)=8n. Outside the four corner squares, t(v)-L(v)>=0.

In one corner use coordinates 0<=x,y<=3, measured inward from its two sides. Put r(v)=t(v)-L_x(v)-L_y(v). Define alpha(v) by the following table; rows are y=0,1,2,3 and columns are x=0,1,2,3:

    -1   0   0  -1
     0   1   0  -1
     0   0   0  -1
    -1  -1  -1  -1

Thus sum alpha=-7. Assign beta to nine edges, with endpoints in lexicographic order:

| Edge | beta |
|---|---:|
| (0,1)--(1,3) | -1 |
| (0,2)--(2,3) | -1 |
| (0,3)--(1,1) | +1 |
| (1,0)--(3,1) | -1 |
| (1,1)--(3,0) | -1 |
| (1,2)--(3,3) | -1 |
| (2,0)--(3,2) | -1 |
| (2,1)--(3,3) | -1 |
| (2,2)--(3,0) | -1 |

All other beta values are zero. For each of the two chosen edges at v, add +beta if v is its first endpoint and -beta if v is its second endpoint. Call the resulting sum D(v). The certificate is the local inequality

    r(v) >= alpha(v) + D(v).

**Exact check.** For each of the 16 cells, enumerate each unordered pair of distinct knight moves whose endpoints have nonnegative coordinates. There are 209 pairs in total. Calculate t as 0 for opposite moves and 1 otherwise, then calculate r, alpha, and D from the formulas above. Every resulting difference r-alpha-D is a nonnegative integer. This is an exhaustive finite check of the stated inequality. The minimum difference is zero at each of the 16 cells. The standalone checker `check_corner_certificate.py` carries out precisely these steps using integer arithmetic, with no solver imports.

Sum the certificate over the corner. Each beta edge has both ends inside the corner. A chosen edge occurs at both ends, so its two contributions cancel. Therefore sum r>=sum alpha=-7. Sum over four corners and use nonnegative residuals elsewhere:

    T - 8n = sum_v (t(v)-L(v)) >= -28.

This proves the improved constant. Edges leaving the corner are free in this check. Finite-board restrictions only remove allowed pairs, so the proof holds also at n=8.

**Limit of this corner method.** A 4 by 4 corner with unrestricted outgoing edges can attain residual -7, with consistent internal edges and no internal cycle. The explicit pattern is recorded in `corner_witness.txt` and independently checked by `check_corner_certificate.py`. Thus this specific corner inequality cannot be improved. This does not prove that 28 is the best global additive constant.

**Checks, 2026-10-02.** The certificate checker passed all 209 cases. A separate checker, `check_proof.py`, passed all 77 one-side cases. Both were checked against valid generated tours at n=16,24,40,80. `corner_lp.py` found the certificate; `corner_integer.py` found the sharp local witness. These discovery solvers are not needed to verify either claim.

Run from the project root:

    .venv/bin/python w-turnstheory/check_proof.py
    .venv/bin/python w-turnstheory/check_corner_certificate.py

The original longer account is retained in `TURNS_DETAILS.md`.

## 3. Crossings: scope of the available obstruction

**SOURCE CHECK AND CORRECTION, 2026-10-02.** F3 in `w-lowerbounds/FINDINGS.md` describes a near-2-factor, not a completed 2-factor with 4n-24 crossings. Its stated count of 28 defective cells omits 16 isolated cells. A full scan of the board gives **44 defective cells** at both n=48 and n=96: 16 have degree zero, 24 have degree one, and 4 have degree four. `base_stats.py` builds a graph from edges and counts only graph nodes, which excludes the isolated cells. The independently checked crossing counts are still 168 and 360, exactly 4n-24. Thus F3 does not prove that every improvement above 4n must use connectivity. A global degree or colour argument could still force extra crossings.

`check_base_defects.py` reproduces the degree counts. `check_fold_obstructions.py` checks all board cells, the crossing counts, the explicit cycles of Section 3.3, and the defect colour charges. The four corner charges are +2,-2,-2,+2; the other defect clusters have charge zero.

The one-side strip obstruction in F1 is distinct and valid: its explicit pattern already has degree two throughout the strip, with no cycle. Hence a sum of independent one-side strip bounds cannot improve the leading coefficient 4.

No new unrestricted crossing lower coefficient is claimed below.

### 3.1. What connectivity and colour cuts prove

**PROVEN.** Let H be a closed knight's tour. Give black cells sign +1 and white cells sign -1. For any proper nonempty cell set R, let b_B and b_W count cut edges whose endpoint in R is black or white. Summing degree two over R gives

    b_B - b_W = 2 (number of black cells in R - number of white cells in R).

Connectivity also gives b_B+b_W>=2. More generally, if H[R] has c path components, then b_B+b_W=2c. These are useful exact constraints, but they count edges across a chosen cut, not crossings between edges. Parallel knight segments can cross a long cut with no pairwise crossing. Therefore no positive crossing cost follows from cut size alone.

### 3.2. A precise colour-flow cost at a fixed diagonal fold

**PROVEN, restricted model.** This result explains the modulus-three obstruction in F3. It does not apply to arbitrary modifications of the direction field.

Use the two knight directions A=(2,1) and B=(-1,-2). Both increase f(x,y)=x-y by one. Keep all A edges below the layer f=0, and all B edges above f=1. Only change the outgoing choice at cells

    p_i=(i,i),   i in Z.

Put q_i=(i+2,i+1). The two permitted choices at p_i are

    A_i: p_i--q_i,
    B_i: p_i--q_(i-3).

Each p_i has one fixed incoming edge. Each q_i has one fixed outgoing edge. Write a_i=1 for choice A_i and a_i=0 for choice B_i. The degree at q_i is

    deg(q_i)=2+a_i-a_(i+3).

Thus degree two throughout the interface forces a_i=a_(i+3): there are exactly eight possible period-three states.

Two A edges are parallel, as are two B edges. An A_i edge and a B_j edge cross properly exactly when j-i is 1 or 2. To see this, solve for their intersection parameters: both parameters equal (j-i)/3, which lies strictly between 0 and 1 exactly in these two cases. Edges outside this interface lie in disjoint open f-layers, so they contribute no further crossings with its edges.

Let r=a_0+a_1+a_2. Per three diagonal steps, the number of crossings is exactly

    r(3-r).

Each A residue crosses each distinct B residue once. Therefore the all-B and all-A states have zero crossings, whereas every mixed state has exactly two crossings per three steps. On a finite interval of L consecutive sources, with degree two at all q_i whose two candidate incoming edges lie in the interval, a mixed state gives (2/3)L-O(1) crossings.

**Colour-flow meaning.** Compare with the all-B state. Replacing B_i by A_i gives the directed difference path q_(i-3) -> p_i -> q_i, where added edges run black to white and removed edges run white to black. Each selected residue gives one such path along the interface. Hence r counts the units of signed difference flow through a transverse cut. The zero-crossing choices carry flow 0 or 3; flow 1 or 2 forces two crossings per period.

This proves a positive linear crossing cost for the proposed repair **if the repair stays in this fixed one-layer interface**. It does not prove that a tour must use that interface, or that a wider corridor or another field has the same cost. Those are the missing steps for a global improvement above 4n.

`check_fold_interface.py` independently checks the intersection rule and all eight states with the shared geometric crossing predicate. It uses no solver.

### 3.3. Connectivity forces many changes to the fold example

**PROVEN.** If a near-2-factor F contains K closed components, each smaller than the whole board, every Hamiltonian cycle H must omit at least one edge from each component. Thus |F minus H|>=K. Retaining a whole proper degree-two component would leave it disconnected from the rest of H.

Here is an explicit linear family of such components in the lower-left quadrant of the unshifted F3 field. For each s>=1, form an inner path from (0,s) to (s,0):

    (2k,s+k),                       k=0,...,s;
    (2s-j,2s-2j),                   j=1,...,s.

An outer path has successive cells

    (1+2k,s+2+k),                   k=0,...,s+1;
    (2s+3-j,2s+3-2j),               j=1,...,s+1.

Join the start of the outer path to (0,s), and its end to (s,0). These joins are knight moves. The two paths form a cycle of length 4s+4, with maximum coordinate 2s+3. Their edges are exactly the direction-field and boundary-pairing edges of F3.

The cycles for different s are disjoint. In the upper half of the quadrant their straight lines have x-2y=-2s or -2s-3; these values are distinct, with different parity for the two types. The lower half has the corresponding distinct lines 2x-y=2s or 2s+3. Upper and lower halves meet only on the diagonal, at the distinct values 2s and 2s+3.

For n divisible by four, take 1<=s<=n/4-3 and rotate these cycles to the four corners. They stay at least two cells short of the quadrant midlines, so the midpoint defects do not affect them. This gives n-12 pairwise disjoint closed components. Any full tour must therefore remove at least n-12 edges from this particular base construction.

This is a lower bound on changed edges, not on crossings. It cannot be added to the boundary crossing count without a separate cost inequality.

### 3.4. Small cycle-joining switches

**MEASURED, 2026-10-02.** `cross_switches.py` enumerates all valid two-edge switches between distinct closed components of the unshifted F3 base. The script removes edges ab,cd and adds ac,bd, with all four endpoints distinct and both added edges valid knight moves. It calculates the exact change in the crossing count against all retained nearby edges.

| n | Closed components in the base | Switch counts by added crossings |
|---|---:|---|
| 24 | 20 | +3: 8; +4: 16; +5: 8; +6: 8; +8: 68 |
| 48 | 68 | +3: 8; +4: 456; +5: 8; +6: 920; +8: 956 |

No such switch has cost zero or less in these two checked instances. This is not a bound for larger changes. Even a sequence of switches cannot be assigned the initial cost at every step, because earlier switches change the later crossing counts.

### 3.5. Status and next exact question

No unrestricted crossing lower bound above 4n-O(1) is proved here. The new proved result is the fixed-fold colour-flow lemma in Section 3.2. The next useful test is whether a finite-width repair corridor can carry one unit of difference flow with zero additional crossings when the surrounding fold field stays fixed. A positive bound for every fixed width would still need a global argument to cover tours that change the whole field.

The turns proof and certificate are complete and ready for the Verifier. The crossing question remains open.

## 4. Continued crossing work: all-move corridor obstruction

Date: 2026-10-02. **Main new result: PROVEN, with a finite local certificate.** A periodic corridor of any finite width, between the two fixed fields of Section 3.2, cannot have both zero crossings and colour flow not divisible by three. This result permits every knight direction inside the corridor. A finite-state argument then gives a positive crossing cost per unit length for each fixed width. The constant depends on the width; this is not yet a new lower bound for arbitrary tours.

I read the updated F5-F7 in `w-lowerbounds/FINDINGS.md` before this work. Their boundary stability statement is F5, not F4. I did not repeat their transfer-graph computation. The results below address the corridor obstruction, not their construction search or their boundary stability computation.

### 4.1. Model and definition of colour flow

Use coordinates u=x-y and v=y. A row below means a fixed value of u. The corridor consists of rows 0<=u<D and is periodic under translation (x,y)->(x+P,y+P), for an integer P>=1. Thus v has period P. All cells have degree two. Edges outside the corridor are fixed: A=(2,1) below row 0, and B=(-1,-2) above row D-1. The edges entering row 0 are the fixed A edges, and the edges leaving row D-1 are the fixed B edges. Other edges across those two boundaries are forbidden. Every knight edge with both ends inside the corridor is allowed.

Use as reference the field with B at every outgoing cell in rows u>=0, and A below row 0. Orient an added edge from black to white and a removed reference edge from white to black. Since both configurations have degree two, this signed difference has divergence zero. The difference has no edge across the two fixed normal boundaries. Its integer flow F through any cut v=t+1/2 is therefore independent of t. Crossings are counted per period in the infinite periodic drawing.

In these coordinates, a knight move changes u by 1 or 3 in absolute value. A and B are the two moves with positive u-change one.

### 4.2. A two-row local lemma

**PROVEN by an independently checked finite argument.** Suppose every cell of row u=0 has one fixed incoming A edge from row -1, and no other edge can enter rows 0 or 1 from negative u. Require degree two at cells (u,v) with u=0 or 1 and -2<=v<=2. All other cells have degree at most two. Assume no proper crossing. Then the cell (u,v)=(0,0) cannot use a knight edge to row u=3.

Here, all possible exits from rows 0 and 1 are allowed. In particular, the lemma does not assume the later rows use A or B. The same statement holds with incoming B edges, by the reflection (x,y)->(-y,-x), which fixes u and exchanges A and B.

**Complete finite specification.** The candidate edges have a source (u,v), u in {0,1}, -6<=v<=6, and any knight move with positive change in u. There are 104 candidates. Give row-0 vertices remaining capacity one, since the fixed incoming edge already uses one degree; give all other vertices capacity two. Enforce the remaining degree exactly at the ten cells u in {0,1}, -2<=v<=2. At all other endpoints enforce only the capacity bound. Forbid each properly crossing pair of candidates. Force one of the two long-normal edges from (0,0). Fixed incoming edges lie in -1<=u<=0 and cannot cross a candidate properly.

This finite system is unsatisfiable. It is a valid relaxation of any putative counterexample: all edges incident to the ten exact-degree cells appear in the candidate set. Other incident edges can be discarded because the remaining endpoints have only upper degree bounds.

**Independent checks.** `check_local_geometry.py` implements these geometric and degree constraints directly with standard Python. Its exhaustive search proves unsatisfiability in 25 search nodes. It uses no SAT package or solver result. Separately, `half_window_sat.py` encodes the system as CNF and produces `local_long_edge.cnf` and `local_long_edge.drup`. The certificate has eight added clauses. `check_rup.py`, also standard Python only, verifies each addition by reverse unit propagation and checks the final empty clause. These checks passed on 2026-10-02.

### 4.3. Zero-crossing classification at every width

**PROVEN.** Every zero-crossing corridor in Section 4.1 uses only A and B. Moreover, for each normal row u, all its outgoing edges have the same direction, either A or B. Consequently, its difference flow F is a multiple of three.

Proof: Start with row 0. Every vertex already has its fixed incoming A edge. Apply the local lemma at each v, using the periodic lift to the plane. It rules out both outgoing directions with u-change three. Each vertex must therefore choose exactly one outgoing A or B edge.

Write A_i and B_i for these choices at v=i. A_i crosses B_(i+1) properly: the two segments intersect at parameter 1/3, as calculated in Section 3.2. Thus, if row 0 has an A choice, its next choice must also be A. Periodicity implies that the entire row is A. If it has no A choice, the entire row is B.

The next row now has exactly one incoming edge at every cell, all from the same family. The previous row is saturated, so no additional edge can enter from behind it. Apply the local lemma, reflected if needed, and repeat. This proves the claim for every row. The outside rows supply the degree-two condition when the local lemma reaches the final row of the corridor.

Changing one whole internal interface from B to A replaces the map v->v-2 by v->v+1. Its contribution to difference flow is 3(-1)^u, where u is the lower row and (-1)^u is its cell colour. Sum over the interfaces. Hence F is divisible by three. This argument also covers P=1 and P=2 through their infinite periodic lifts.

The result rules out a zero-crossing repair of nonzero colour residue in any fixed-width periodic corridor, even when the repair changes all knight directions within that corridor.

### 4.4. Positive cost per length at each fixed width

**PROVEN.** Fix D. There is a constant c_D>0 such that a corridor with colour flow F not divisible by three has at least c_D P crossings per period. A deliberately loose explicit choice is

    c_D = 28^(-8D).

For a finite stretch of length L with the same fixed side data and conserved nonzero flow residue, the corresponding bound is c_D L-O_D(1).

Proof: Encode each v-column by the unordered pair of chosen moves at its D cells. There are at most 28^D column symbols. A state consisting of the last eight symbols suffices to check all local conditions and charge all new crossings: each knight move changes v by at most two, and crossing edges can involve endpoint columns only a bounded distance apart, less than eight. Reciprocity, degree two, and the fixed side data are local conditions as well. Thus there is a finite directed transfer graph with at most M=28^(8D) states and nonnegative integer crossing weights. Charge each crossing once, when its last endpoint column is read.

The flow F through a v-cut is determined by the edges that cross that cut, so it is determined by a state. Along valid transitions it is constant. In the states with F not divisible by three, the zero-weight edges contain no directed cycle: such a cycle would give a zero-crossing periodic corridor, contrary to Section 4.3.

A zero-weight walk in this class has length at most M-1. In a closed walk of P transitions and total crossing weight X, there are at most X positive-weight transitions. Partition the walk at those transitions. Each part has length at most M. Hence P<=MX, which gives X>=P/M. The finite-stretch version loses only the start and end state contributions.

This proof gives a positive constant for every fixed width, with no restriction to two move directions. It does **not** give a constant independent of D. A corridor whose width grows with n is therefore not controlled strongly enough to prove 4n+cn.

### 4.5. Stronger bound under forward motion

**PROVEN, restricted model.** If every corridor edge joins adjacent normal rows, and each cell has one edge from the preceding row and one to the next row, then for P divisible by three and F not divisible by three,

    X >= 2P/3,

independent of the corridor width. Equality is attainable.

At each interface, degree one on both sides forces its A/B choice sequence to have period three, as in Section 3.2. Let r_u in {0,1,2,3} count its A residues. That interface contributes (P/3) r_u(3-r_u) crossings and  (-1)^u r_u units of difference flow. Edges in distinct interfaces cannot cross properly, since their open normal-coordinate intervals are disjoint. If every r_u were 0 or 3, F would be divisible by three. Thus at least one interface is mixed, giving 2P/3 crossings. One mixed interface and otherwise pure interfaces attains the bound for F=1 or F=2.

This proof permits arbitrarily many layers. The restriction that paths move forward is essential to the proof; it has not been established for general corridors with crossings.

### 4.6. Finite all-move tests

**EXACT FINITE RESULTS, independently checked, 2026-10-02.** `fold_corridor.py` uses one CP-SAT worker. `check_corridor_sat.py` independently builds a SAT model in Cartesian coordinates, with a separate exact crossing predicate and cardinality constraints. Both permit all knight moves inside the corridor.

| D | P | F | Result |
|---:|---:|---:|---|
| 3 | 6 | 1 | zero crossings infeasible |
| 4 | 6 | 1 | minimum 4 crossings |
| 6 | 6 | 1 | minimum 4 crossings |
| 10 | 6 | 1 | zero crossings infeasible |
| 4 | 12 | 1 | minimum 8 crossings |

The lower bounds in the minimum rows were independently checked by asking the SAT model for at most 3, 3, and 7 crossings, respectively; all three instances were unsatisfiable. The matching upper patterns use one mixed interface from Section 4.5, so their validity and cost follow directly from that proof. A five-second optimization run at D=10, P=6 found a non-optimal solution; it is not used as a lower-bound result.

At D=10, P=6, zero crossings plus the requirement of at least one edge with normal jump three was also unsatisfiable, even with no specified flow. Section 4.3 now proves the corresponding statement for all D and P.

### 4.7. What is still missing for the requested global bound

Neither target is complete. Boundary stability gives cheap P/P' on most boundary cells, but it does not yet force a corridor of bounded width, nor a nonzero flow residue in a corridor with the exact fixed side fields of Section 4.1. The boundary stretch alone has no prescribed interior pairing. The corner-flow obstruction in F3 refers to that particular fold field; it is not yet an invariant of every tour with a cheap boundary.

The new all-move corridor theorem closes the zero-cost loophole for fixed-width repairs of that field. To obtain 4n+cn, one must still prove either a width-independent version of Section 4.4, together with a forced nonzero-residue transport length of order n, or a global decomposition into a linear total length of corridors of bounded width. I do not claim either statement.

**CONJECTURE for a precise next step:** the stronger bound X>=2P/3 of Section 4.5 holds in the full all-move corridor model whenever F is not divisible by three. The checked finite optima support it, but the forward-motion proof does not establish it.

## 5. Next pass: the 2P/3 conjecture and the global invariant

Date: 2026-10-02. No general crossing lower bound above 4n-O(1) is claimed.

### 5.1. Further search for a corridor counterexample

**EXACT FINITE RESULT.** At D=8, P=6, F=1, the all-move corridor minimum is **4 crossings**. `check_corridor_sat.py` independently proved that at most three crossings is infeasible, in about three seconds on one core. The one-mixed-interface pattern in Section 4.5 supplies four crossings. The result is stored in `sat-D8-P6-cap3.json`.

**INCONCLUSIVE SEARCHES.** Four-second, one-worker CP-SAT feasibility searches tested the following possible counterexamples. Every run returned UNKNOWN, not INFEASIBLE:

| D | P | F | Requested crossing cap |
|---:|---:|---:|---:|
| 8 | 6 | 1 | 3 |
| 12 | 6 | 1 | 3 |
| 8 | 9 | 1 | 5 |
| 6 | 5 | 1 | 3 |
| 6 | 7 | 1 | 4 |

The first row was then resolved by the independent SAT check above. A separate SAT search at D=8, P=9, F=1, cap 5 reached a 15-second time limit; it gives no lower bound. The CP-SAT outputs are in `counterexample_search.json`. No witness below 2P/3 was found. These searches do not prove the conjecture.

**Status of the proof attempt.** Section 4.5 still proves 2P/3 only under forward motion. Section 4.3 rules out zero cost with all directions. Neither argument currently gives a quantitative, width-independent cost for long-normal edges or for vertices with both edges on the same side. The full conjecture remains open.

### 5.2. The exact invariant: signed difference flow

**PROVEN, for every tour and every reference graph.** Fix a reference edge set G on the board. It need not have degree two. Let H be any spanning degree-two knight graph; connectivity is not needed. Give a black cell sign chi=+1 and a white cell sign chi=-1. On each knight edge oriented from black to white put the signed value

    J(e) = 1 if e is in H but not G,
           -1 if e is in G but not H,
            0 otherwise.

The divergence at a cell v is

    div J(v) = q_G(v) = chi(v) (2-deg_G(v)).

Therefore, for every set R of cells,

    signed outward difference flow across R = sum_(v in R) q_G(v).       (5.1)

Proof: At a black cell the divergence is deg_H-deg_G=2-deg_G. At a white cell its sign is reversed. Sum over R; internal edges cancel. This proves (5.1).

The right side is independent of H. Thus **the fold reference's corner charge is an invariant of the difference between that reference and every tour**, not just tours whose boundary is cheap. It is not an invariant of the boundary pattern by itself.

In particular, suppose a reference has a corner defect cluster of total charge +2, and no further defects in an annular region around it. Every enclosing cut in that annulus carries signed difference flow +2, hence nonzero residue modulo three, for every H. If the annulus has radial width proportional to n, there is an order-n family of cuts carrying that residue. This conclusion needs no assumption that H stays near the reference field.

The unshifted fold reference has the four corner charges +2,-2,-2,+2 in the checked instances. `check_corner_transport.py` checks (5.1) on a valid n=48 tour against this reference. For every lower-left square window with side r=4,...,20, the difference flow is exactly 2. The script directly checks both edge sets and the degree-charge sum. The earlier full-board check at n=96 gives the same corner cluster charges. These finite checks illustrate the general identity; they are not a new all-n proof of the reference's defect pattern.

**Equivalent transport bound.** For any real potential phi on cells,

    sum_v q_G(v) phi(v)
      = sum_(black b, white w) J(bw) [phi(b)-phi(w)].                  (5.2)

If phi changes by at most K on a knight edge, then

    |H symmetric-difference G| >= |sum_v q_G(v) phi(v)| / K.

For example, phi(x,y)=|x+y-(n-1)| changes by at most three on a knight edge. Four separated corner charges +2,-2,-2,+2, with zero net charges in the other bounded defect clusters, give a numerator 4n-O(1). This proves that order-n changed edges are necessary for any reference with that defect pattern. It still does not count proper crossings. On the checked n=48 example, the exact charge moment is 208 and equals the directly calculated edge moment.

### 5.3. Why raw corner flux is not the claimed invariant

**PROVEN.** The actual black-to-white edge flow of a tour across R equals

    2 (number of black cells in R - number of white cells in R).

This depends only on the cells in R, not on pattern P. For a corner square of even side length, it is zero. For a corner square of odd side length anchored at a black corner, it is two. Thus arbitrarily large even and odd corner windows have different flux residues while the tour and its cheap boundary remain unchanged.

Consequently, a statement that every cheap corner carries a fixed nonzero residue must specify a reference field and the cut convention. The reference subtraction in (5.1) supplies such a convention. It cannot be replaced by an unspecified "corner flux of pattern P."

A single cheap side stretch also has no intrinsic defect charge: the explicit half-plane pattern P in Section 1 has degree two everywhere. Charges arise from a chosen extension, its corner or junction defects, and the comparison with H.

### 5.4. The missing global fact, stated as a sufficient theorem

The charge identity already gives long relative transport when a suitable reference is fixed. The missing result is that a linear amount of this transport must incur **additional** crossings in controlled corridors. It must rule out flow through arbitrary rearranged interior fields, and it must avoid charging boundary crossings a second time.

Here is a precise sufficient statement. Let B be the set of crossings used in the known boundary lower bound, with |B|>=4n-C_0. Put e=X-4n+C_0, so e>=0. Seek constants alpha>0, beta>=0, kappa>=0, and m>=1, independent of n, such that every tour with a cheap boundary admits corridor regions R_j with these properties:

1. Each corridor has the prescribed two line-family side fields, a well-defined nonzero difference-flow residue modulo three, and longitudinal length L_j. It is a finite version of the Section 4.1 model, up to board symmetries.
2. Their total length satisfies sum L_j >= alpha n - beta(e+1). Thus a small number of boundary defects cannot remove all long transport.
3. The crossings charged to these corridors lie outside B, and each such crossing is charged at most m times.
4. Their finite-corridor cost, including the total endpoint loss, satisfies sum X_j >= c sum L_j - kappa(e+1), for some c>0 independent of n. Fixed bounded widths plus Section 4.4 could supply c. Arbitrary widths would need a stronger cost theorem.

If these four properties hold, then

    m e >= c alpha n - (c beta+kappa)(e+1),

so

    X >= [4 + c alpha/(m+c beta+kappa)] n - O(1).

This would prove the requested improvement with an explicit positive coefficient. **The corridor existence, length, and overlap statement is unproved.** Boundary stability F5 by itself specifies only a narrow boundary strip. It does not force the line-family side data in the interior, even if most boundary cells agree with the fold reference.

There is a further endpoint issue: a proof of the periodic inequality X>=2P/3 alone does not automatically give a finite-corridor inequality with an additive constant independent of width. Closing a wide corridor, or applying a finite-state bound to it, can lose a width-dependent amount. Property 4 must control that loss as well.

### 5.5. Alternative global target using the number of components

A second precise sufficient statement would be constants a,b>0 and C such that every spanning degree-two knight graph with K components satisfies

    K + a [X-4n+C] >= b n.

For a tour, K=1, so this would imply X>=(4+b/a)n-O(1). The fold-type examples motivate such a statement, but their many components do not prove it for arbitrary crossing-free interior fields. The current corridor theorem does not yet imply it.

**Current conclusion.** The stronger corridor bound still has no counterexample in the checked small cases, but it remains a conjecture. The corner charge relative to a fixed reference is already an exact invariant for every tour. The main global gap is localization and cost of that invariant transport, not the conservation identity.

## 6. A tile proof of mod-3 flux, and an excess-crossing budget

Date: 2026-10-02. **PROVEN:** every crossing-free, doubly periodic knight
2-factor with even horizontal and vertical periods has colour flux zero
modulo three through both period cuts. This proves the torus conjecture for
all even periods, not only the enumerated tori. There is also an explicit
local mod-3 height and a quantitative bound on its defects. The bound gives
an additional L/4 crossings, up to a constant, if L suitable disjoint charged
curves are forced. **The required corner/edge input for arbitrary tours is
still conditional. No unconditional bound (4+c)n is claimed here.**

I read F13-F14 before this work and the new F15 after it appeared. F15 reports
a finite local M3 proof. The results below do not use its solver output.
They replace the need to classify all crossing-free regions by a geometric
account of both tile overlaps and tile gaps.

### 6.1. Replace a knight edge by a unit-area tile

For a knight edge e=ab, let K(e) be the parallelogram with long diagonal ab
and short diagonal the unit horizontal or vertical lattice edge with the
same midpoint. For example, for a=(0,0), b=(2,1), its other vertices are
(1,0) and (1,1). Its area is one. Its sides consist of two unit grid edges
and two unit diagonals. All four vertices are in the coordinate box of a,b.

Divide each unit lattice square by both diagonals into four open triangles
of area 1/4. Call them *quarter triangles*. Each K(e) is the union, up to
its boundary, of exactly four quarter triangles.

**Geometric lemma (PROVEN, finite exact certificate).** For distinct knight
edges e,f, the interiors of K(e),K(f) overlap if and only if e,f cross
properly. In that case their common area is 1/4 or 1/2. Edges with a common
endpoint have tiles with disjoint interiors.

The certificate is `check_knight_tiles.py`, using only integer arithmetic
and the Python standard library. Translate one edge's left endpoint to
(0,0). Its direction is one of (2,1),(1,2),(1,-2),(2,-1). A tile that can
meet it must have its left endpoint in [-4,4] squared. These bounds follow
from the coordinate spans, which are at most two. The checker tests all
1,292 distinct pairs. It compares strict segment intersection with shared
quarter triangles and independently with the separating-axis test for the
two parallelograms. There are 24 cases with one common quarter triangle,
12 with two, and no other positive intersection sizes. Thus this finite
check covers every relative position; it is not a search over tours.

### 6.2. An exact local flux identity

**PROVEN.** Let q=ab be a unit grid edge. Orient its crossing unit dual
segment s so that its chosen normal points from a to b. Write chi(a)=+1
for black and -1 for white. Let m_+,m_- be the tile multiplicities on the
two quarter triangles immediately adjacent to q, one on each side. Let g_q
be the number of selected knight tiles whose short diagonal is q. For any
set of knight edges, without degree or crossing assumptions, its signed
black-to-white flux satisfies

    phi_H(s) = chi(a) [m_+ + m_- - 3 g_q].                       (6.1)

Here the dual segment joins the centres of the two adjacent unit squares.
Knight edges never pass through such a square centre, so the flux is
unambiguous.

Proof: Give a tile long-diagonal endpoints b,w of colours black,white,
and short-diagonal endpoints b',w' of colours black,white. The two unit
axis sides are bw' and b'w. The oriented chain

    [b,w] + [b',w'] - [b,w'] - [b',w]

is the boundary of two signed triangles inside the tile. Their third
vertices include the common diagonal midpoint. Their supports avoid all
unit-square centres. Hence this chain has zero net flux across s. Sum this
identity over tiles. If a_+,a_- count tile axis sides on q from its two
sides, this gives phi_H(s)=chi(a)(a_+ + a_- - g_q). A tile adjoining either
quarter triangle has q either as an axis side or as its short diagonal.
Thus m_+=a_+ + g_q and m_-=a_- + g_q, which proves (6.1).

The checker also verifies (6.1) one knight edge at a time, for both grid-edge
orientations. Linearity then proves it for every edge set. This requires
648 additional exact finite cases. Translation by an odd-colour vector
changes both sides' signs; reversing the normal also changes both signs.

Let Q be all unit horizontal and vertical grid edges, oriented from black
to white. Its flux through s is chi(a). Therefore

    omega_H(s) := phi_H(s) + phi_Q(s)
                = chi(a) [m_+ + m_- + 1]                 (mod 3). (6.2)

In particular, omega_H(s)=0 whenever both adjacent quarter triangles have
multiplicity one.
With the directed-dual convention of F15, b is the cell on the right,
so phi_Q(s)=-chi(b). Thus omega_H is precisely its phi_H-chi(b).

If H has degree two at every cell inside a dual loop, the signed flux of
H+Q around that loop is

    (2+4) sum chi(v) = 0                                  (mod 3).

Thus omega_H is the difference of a single-valued Z_3 height h_H on every
simply connected dual-grid region of degree-two cells. **A height change
across a unit dual edge requires an adjacent quarter triangle with
multiplicity different from one.** This is a local formula, with no
reference-field choice and no restriction on the knight directions.

### 6.3. The all-period torus theorem

**PROVEN.** Lift the torus graph to the plane. With no crossings, the
geometric lemma makes its tiles a packing. A period cell contains N lattice
vertices and N selected edges, since every vertex has degree two. The tiles
have total area N per period, exactly the area of the period cell. Therefore
they cover it: every quarter triangle has multiplicity one. A gap would
have positive area and would contradict this equality.

Equation (6.2) now gives omega_H=0 on every unit dual segment. Along a full
horizontal or vertical period cut, the flux of Q is zero: the signs of its
unit edges alternate, and the corresponding period length is even. Hence
the flux of H is zero modulo three through both cuts. This proves the
conjecture for all such periodic graphs, including all their components.

This proof uses only the tiles and area. It does not assume straight paths,
free folds, two move types, or a fixed corridor width.

**Scope for open regions.** A crossing-free patch gives a tile packing;
area equality on an entire period is not available for an open patch.
Therefore this proof does not itself show that a crossing-free finite
window has no gap near its centre. F15 addresses that stronger local
statement by a finite computation. The next lemma controls gaps directly,
so the counting route below does not need to assume that statement.

### 6.4. Gaps cost crossings above the boundary term

**PROVEN for every 2-factor on the n by n board.** Let X be the number of
proper crossing pairs. Let G be the number of uncovered quarter triangles
inside [0,n-1] squared. Then

    G <= 2X - 8n + 4.                                         (6.3)

Equivalently, if A_gap=G/4 is their total area,

    X >= 4n - 2 + 2 A_gap.

Proof: All tiles stay within the board's coordinate rectangle. There are
n squared selected edges, each covering four quarter triangles. The board
rectangle has 4(n-1) squared quarter triangles. If m_t is the multiplicity
at quarter triangle t, then

    sum_t (m_t-1)_+ = 4n^2 - [4(n-1)^2-G] = 8n-4+G.

For every integer m>=0, (m-1)_+ <= binomial(m,2). The sum of these binomial
terms counts common quarter triangles of tile pairs. The geometric lemma
bounds this sum by 2X. This proves (6.3).

A second useful bound is local. Fix any set U of quarter triangles inside
the board rectangle [0,n-1] squared, and a set B of crossing pairs such that
no pair in B overlaps on a triangle of U.
Then the number of multiply covered triangles in U is at most

    2 [X-|B|].

Indeed, each such triangle belongs to at least one crossing tile pair,
and every pair has at most two common quarter triangles. Together with
(6.3), the number of bad triangles in U (multiplicity zero or at least two)
is at most

    2X-8n+4 + 2[X-|B|].

This separates interior defects from crossings already used for the
boundary lower bound. A hole in a crossing-free region is not a free
exception: its area consumes this same excess-crossing budget.

### 6.5. Charged curves give an explicit linear improvement

**PROVEN implication.** Suppose there are L edge-disjoint paths in the internal
dual graph, within the degree-two height domain of Section 6.2, with
nonzero change of h_H modulo three. Let U consist of quarter triangles
inside the board rectangle and contain the two quarter triangles adjacent
to every step of these paths. Suppose also that B is a set of
crossing pairs whose tile overlaps avoid U. Then

    L <= 4X - 8n + 4 - 2|B|.

In particular, if |B| >= 4n-C, then

    X >= 4n + L/4 - 1 - C/2.                                 (6.4)

Proof: Each path has a step with nonzero omega_H, so (6.2) gives a bad
adjacent quarter triangle. A quarter triangle has exactly one unit grid
side, and hence is adjacent to exactly one unit dual edge. Thus a single
bad triangle cannot serve two edge-disjoint paths. Apply Section 6.4.
No bounded-width corridor or long-path classification is needed.

For example, L=alpha*n-O(1) would give the coefficient 4+alpha/4. Four
corner families of n/2-O(1) paths would give 9n/2-O(1), **if** their charges
and the required exclusion of boundary crossings were established.

The same implication tolerates edge defects. Put E=X-4n+2, which is
nonnegative by (6.3). Suppose d counts exceptional boundary rows and there
are constants independent of n such that

    d <= K(E+1),
    |B| >= 4n-C0-C1*d,
    L >= alpha*n-C2*d-C3,

with K, C1, C2 >= 0, alpha > 0, and B still avoiding U. Thus
D=4+K(2C1+C2) >= 4 > 0. Then (6.4)'s first form gives

    X >= [4 + alpha/(4+K(2C1+C2))] n - O(1).                  (6.5)

This is the exact place to use the edge stability theorem F5. The constants
can be very poor; positivity is sufficient. The statement is conditional
on the three displayed estimates and the geometric exclusion, not on an
unproved assertion that every defect has a bounded-size crossing nearby.

### 6.6. What remains for the corner computation

The reference-charge identity in Section 5.2 supplies a precise bridge.
Let R surround one reference defect cluster of charge q not divisible by
three. Let its cut consist of an interior dual path gamma and short tails
where H and the reference G agree. Then

    integral_gamma (phi_H-phi_G) = q.

If G's tiles cover the two triangles beside every step of gamma exactly
once, (6.2) gives omega_G=0 there. Therefore

    integral_gamma omega_H = q                            (mod 3),

so gamma is one of the charged paths required in Section 6.5.

For the cheap half-plane pattern, the usual U-turn tiles lie in the first
unit-wide boundary strip. Beyond that strip, the outgoing straight-family
tiles are the same as in the full-plane tiling. Thus the tile-overlap
exclusion has a concrete geometric meaning: use interior paths beyond the
U-turn overlaps, with endpoint tails controlled by the cheap edge pattern.
This observation must be applied with the exact phase and endpoint rules
used by the corner calculation.

**Still to prove for a general near-optimal board:** choose the reference
and endpoint tails from its actual P/P' stretches; show that a positive
linear number of disjoint paths have nonzero charge; and bound the paths
lost to exceptional rows. A charge measured only for one fold reference
cannot be used for all boundary choices without this step. Likewise, the
boundary crossings in B must be shown to have tile overlaps outside U.
These are the corner/edge inputs assigned to KT Lower Bounds. Equations
(6.4)-(6.5) complete the counting once those inputs are available.

**Reproduction.** Run `python3 w-turnstheory/check_knight_tiles.py`.
On 2026-10-02 it passed the 1,292 tile-pair checks and 648 single-edge flux
checks. The all-period theorem and the inequalities then follow by the
arguments above; no solver is involved. An exploratory open-window tile
coverage search found feasible relaxations at widths 2 through 5; width 6
reached its 20,000-node cap. Those searches give no counterexample to F15
and are not used in any proof here.

## 7. Unconditional crossing lower bound for closed tours

Date: 2026-10-02. **PROVEN, with exact finite certificates:** for every even
n >= 32, every closed knight's tour on the n by n board satisfies

    X >= (4 + 1/338) n - 1240.

Thus the asymptotic coefficient 4 is not tight. The additive constant is
only a convenient bound. This proof uses the strip stability facts of
KT Lower Bounds, the tile identity in Section 6, and a sharper version of
its corner-charge check. It does not use M3 or NE-M3 window certificates.

**Scope:** the theorem here is for Hamiltonian cycles. The strip transfer
graph forbids cycles within a strip. A proper subset of a Hamiltonian cycle
has no cycle, so this restriction is valid. It is not automatically valid
for an arbitrary 2-factor. I do not claim that extension here.

### 7.1. The finite strip facts, and one-row stability

Fix a side of the board and use coordinates with that side at x=0. Keep
all tour edges incident to columns 0 or 1; their other endpoints are in
columns 0 through 3. This edge set is a forest of paths. Scan its cells in
order (row,column), with four transitions per row. This gives a walk in
the width-2 strip graph of `w-lowerbounds/strip_dp.py`.

I independently ran `w-lowerbounds/strip2_independent.py`. It returned
82,516 states, 144,674 arcs, an exact potential d in [-1/4,135/4], minimum
positive reduced cost one, two tight cycles of length four, and T*=37.
Here a transition with crossing weight w has reduced cost

    red(u,v) = w - 1/4 + d(u) - d(v) >= 0.

The tight graph after deletion of its two cycle edge sets is acyclic, with
longest path 37. The two cycles give the patterns P and P':

    neighbours of (0,y): (2,y+s), (1,y+2s),
    neighbours of (1,y): (3,y+s), (0,y-2s),       s=+1 or -1.

Let E_sigma be the total reduced cost for this side, and X_sigma its strip
crossing count. Telescoping the potential gives

    X_sigma >= n - 34 + E_sigma.                              (7.1)

Call a row *good* if all four of its transitions are edges of one tight
cycle. Such a row has exactly P or P' at its two strip cells. A critical
state already specifies the pending edges from earlier rows, so no extra
two-row margin is needed in this definition. Consecutive good rows use
the same cycle.

These assertions are checked by `check_strip_row_certificate.py`, adapted
from the independent strip implementation. For each critical cycle it
checks the four column phases, recovers all neighbours at (0,0),(1,0)
from the pending states, and compares them with the displayed patterns.
It also checks the pending crossing used in Section 7.2.

Here is the full stability count. A zero-reduced-cost walk can visit each
of the two cyclic tight components at most once after leaving it. Its
non-cycle edges therefore form at most three paths in the acyclic graph,
with total length at most 3*37=111. Split a general walk at its m positive
transitions. The number of non-cycle transitions is at most

    m + 111(m+1) = 112m+111 <= 112E_sigma+111.

Each bad row contains a non-cycle transition. The rows use disjoint sets
of transitions. If d_sigma is its number of bad rows, then

    d_sigma <= 112E_sigma+111.                                (7.2)

This improves the three-row definition's factor 336 to 112.

Let S=sum E_sigma and d=sum d_sigma over the four sides. Crossing pairs
counted in two different strips lie within a 4 by 4 corner square. Such
a square has 24 possible knight edges, hence at most 276 edge pairs.
Opposite strips cannot share a pair. Consequently

    sum X_sigma <= X+1104,
    S <= X-4n+1240,
    d <= 112S+444.                                            (7.3)

Set E=X-4n+2. Section 6.4 proves E>=0. Equations (7.3) imply

    d <= 112E+139100.                                         (7.4)

### 7.2. One distinct boundary crossing per good row

A good row y supplies a selected crossing pair already present in the
pending state at the start of that row. For P, after translating y to zero,
the pair is

    (0,-2)-(1,0),   (0,-1)-(2,0).

For P' it is

    (0,1)-(1,-1),   (0,0)-(2,-1).

The strip checker verifies both statements directly. Within one pattern,
different rows give different pairs. Between the patterns, the unique
(absolute displacement 1,2) edge has opposite slopes, so the pairs cannot
coincide. Thus each good row gives a distinct crossing.

Use only rows 6 through n-7. Their pairs cannot be shared with another
side's selected pairs. Let B be their union. There are at least

    |B| >= 4n-48-d.                                          (7.5)

Every pair in B has one edge whose endpoints both lie in the first
unit-wide boundary strip. Its tile lies in that strip, so the two tiles'
overlap also lies there. All these overlaps avoid quarter triangles in
the interior rectangle (1,n-2) squared, including triangles with sides on
its boundary. This supplies the geometric exclusion required by Section
6.5; it does not merely exclude the crossing points.

### 7.3. A corner is charged from four endpoint rows

Use the bottom-left corner and an integer R>=12. Let L_R be the positively
oriented dual square with corners (1/2,1/2), (R+1/2,1/2),
(R+1/2,R+1/2), (1/2,R+1/2). Let Q_R be the following connected part of it:

    (3/2,R+1/2) -> (1/2,R+1/2) -> (1/2,1/2)
      -> (R+1/2,1/2) -> (R+1/2,3/2).

All segments are split into unit dual steps. The remaining path, called
gamma_R, joins (R+1/2,3/2) to (3/2,R+1/2) along the right and top sides.

**Corner lemma (PROVEN by exact enumeration plus a degree identity).**
If the strip cells in rows R-1 through R+2 of the left side have one pattern
P or P', and those in columns R-1 through R+2 of the bottom side have one
transposed pattern P or P', then

    sum_(s in Q_R) omega_H(s) = 1                       (mod 3). (7.6)

No condition is imposed on the rest of either boundary arc or on the
corner completion.

This sharpens the endpoint interval in `w-lowerbounds/PROOF_crossings.md`.
The independent standard-library checker is
`check_corner_endpoint_charge.py`. Here is why its finite check applies
at every R. An edge meeting the long part at x=1/2 has an endpoint in
column 0; the analogous statement holds at y=1/2. For each boundary cell
(0,y), 4<=y<=R-2, every possible edge contributes -chi(0,y) to the flux of
Q_R, except contributions already accounted for by another endpoint.
Subtract its degree term -2chi(0,y); do the same along the bottom side.
The checker explicitly verifies the resulting linear identity: every
remaining nonzero edge coefficient is incident either to an endpoint
strip cell in the stated four-row interval or to one of the seven cells

    (0,0),(0,1),(0,2),(0,3),(1,0),(2,0),(3,0).

The endpoint terms are fixed by P/P'. All degree-consistent choices at
these seven cells are then enumerated: 2,916 choices. For all four pattern
combinations and both parities of R, (7.6) holds. Increasing R by two adds
two opposite-colour middle cells per side and translates the endpoint
terms by a colour-preserving vector. The identity is therefore unchanged.
The checker tests R=12,13 and also R=14,15.

The height in Section 6.2 is single-valued on this dual square, so its total
change around L_R is zero. Equation (7.6) makes gamma_R a charged path with
sum omega_H=-1 modulo three. Reflections and rotations give nonzero charge
at each of the other corners as well. This uses the actual P/P' stretches
and arbitrary actual corner moves. No special fold reference is assumed.

### 7.4. Count the charged paths and their defects

At each corner take all integer radii

    12 <= R <= n/2-4.

There are 2n-60 candidate paths in total. They are edge-disjoint. The four
corner boxes have a positive gap between them, and nested paths at one
corner do not intersect.

Discard a radius if one of its four endpoint rows on either side is bad.
Each bad row can discard at most four radii at a corner. Moreover, the
endpoint intervals used by the two corners on one side are disjoint:
they lie in [11,n/2-2] and [n/2+1,n-12]. Thus a bad row can affect at most
four candidate paths in total, rather than eight. The remaining number L
satisfies

    L >= 2n-60-4d.                                           (7.7)

Four consecutive good rows have one common pattern, so Section 7.3 proves
that every retained path is charged.

Every quarter triangle adjacent to a step of these paths lies outside the
unit-wide boundary strips. Therefore the overlaps of all pairs in B avoid
these triangles. Apply Section 6.5 and then (7.5):

    L <= 4X-8n+4-2|B|
      <= 4E+92+2d.

Combine this with (7.7) and (7.4):

    2n <= 4E+6d+152
       <= 676E+834752.

Since X=4n-2+E, this gives

    X >= (4+1/338)n - 1237,

and in particular the stated bound with additive constant 1240.
All uses of connectivity, corner data, boundary crossings, and overlap
multiplicity are explicit above. There is no remaining corridor or
near-edge hypothesis in this theorem.

### 7.5. Certificates and scope of the finite work

The checks use one CPU core and no solver:

```sh
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_corner_endpoint_charge.py
python3 w-turnstheory/check_strip_row_certificate.py
```

The first verifies the tile geometry and exact flux identity. The second
verifies the four-row corner lemma and its linear degree reduction. The
third rebuilds the strip graph, verifies its exact potential and tight
components, and checks the pattern and crossing recovered from a critical
row. Its output is saved in `strip_row_certificate.txt`. All checks passed
on 2026-10-02. The original independent strip check also passed; its output
is in `strip_audit.txt`.

Only the Hamiltonian-tour theorem is claimed. Extending the strip stability
argument to arbitrary 2-factors would require handling cycles wholly
contained in the strip graph; the tile and corner lemmas themselves already
apply to 2-factors.

### 7.6. Sharp strip stability gives coefficient 4+1/17

Date: 2026-10-02. **PROVEN for closed tours:** for every even n >= 32,

    X >= (4+1/17)n - 1006.

Thus the requested bound with additive constant 1009 also holds. This
section replaces the stability estimate in 7.1; all geometric inputs in
7.2--7.4 stay the same.

Here is an exact check of statement (S) in `w-lowerbounds/TILE_INPUTS.md`.
For each strip arc u -> v with crossing weight w, let I=1 for a non-cycle
arc and I=0 for one of the eight P/P' cycle arcs. The checked integer
potential p has values in [-149,0] and satisfies

    20w-5-4I + p(u)-p(v) >= 0.

Sum over any walk. The potential terms cancel except at its endpoints.
Since p(end)-p(start) >= -149, this gives

    sum(w-1/4) >= N_nc/5 - 149/20.                 (S)

The board strip has 4n transitions. Its total weight is X_sigma, and each
bad row contains a non-cycle transition. Hence

    d_sigma <= N_nc <= 5(X_sigma-n+149/20).

A tour gives a valid strip walk because its restriction to a proper
boundary strip has no cycle. This is the sole connectivity restriction;
the theorem is not asserted for all 2-factors.

Sum over four sides and use sum X_sigma <= X+1104 from 7.1. With
E=X-4n+2, the exact arithmetic is

    d <= 5(X+1104-4n+149/5)
      = 5(E-2+1104+149/5)
      = 5E+5659.

The value 5679 in TILE_INPUTS.md is a valid weaker upper bound, but is not
the value of its displayed expression. Substitute into 7.4:

    2n <= 4E+6d+152 <= 34E+34106.

Therefore

    X >= (4+1/17)n - 17087/17
      >= (4+1/17)n - 1006.

**Checks performed.** Both the original exact-integer implementation and
the separate pure-Python implementation passed at alpha=1/5 on 2026-10-02.
Both found eight cycle arcs and potential range [-149,0] in units of 1/20.
Their outputs are `alpha_certificate.txt` and `alpha_independent.txt`.
The following commands run the required positive certificate without the
much longer negative-cycle test at 201/1000:

```sh
cd w-lowerbounds
../.venv/bin/python -c "exec(open('alpha_star.py').read().split('lo, hi = Fraction(0), Fraction(2)')[0]); good, dist = ok(Fraction(1,5)); assert good; print(int(dist.min()), int(dist.max()))"
python3 -c 'import strip2_independent as s; assert s.alpha_check(1,5)'
```

The first command runs the same 1/5 test as `alpha_cert.py`. The second
rebuilds the graph with an independent implementation. Neither uses a
solver. The three geometric and row-pattern checker commands in 7.5
complete the finite inputs. Sharpness of 1/5 is not needed for this theorem;
I did not repeat the 201/1000 negative-cycle test.

### 7.7. Per-row stability gives coefficient 4+1/8

Date: 2026-10-02. **PROVEN for closed tours:** for every even n >= 32,

    X >= (4+1/8)n - 856.

Use the bad-row definition of 7.1. Augment each strip state by a flag that
records whether the current row has used a non-cycle arc. Set the flag
when such an arc occurs. At the fourth transition, charge b=1 if the flag
is set, and then reset it. Thus sum b is exactly d_sigma on a complete
board strip; four consecutive cycle arcs lie on one of the two P/P' cycles.

The exact certificate of KT Lower Bounds, `beta_cert.py`, gives an integer
potential p in [-46,0] on the augmented graph, with

    8w-2-4b + p(u)-p(v) >= 0.

Sum over the 4n transitions and divide by eight. The endpoint potential
difference is at least -46/8. Hence

    X_sigma-n >= d_sigma/2 - 46/8
              >= d_sigma/2 - 6.

This is the per-row statement (S') in `w-lowerbounds/TILE_INPUTS.md`.
Sum over four sides, use sum X_sigma <= X+1104, and put E=X-4n+2:

    d <= 2(X+1104-4n+24) = 2E+2252.

The geometric count in 7.4 is unchanged. It gives

    2n <= 4E+6d+152 <= 16E+13664,
    E >= n/8-854,
    X >= (4+1/8)n-856.

The scope is closed Hamiltonian tours. As in 7.6, the strip graph excludes
cycles contained in a boundary strip, so this argument is not asserted
for arbitrary 2-factors.

**Reproduction.** From `w-lowerbounds`, run:

```sh
../.venv/bin/python beta_cert.py
python3 -c 'import strip2_independent as s; assert s.row_check(1,2)'
```

The original and independent checks passed on 2026-10-02, each with eight
cycle arcs and potential range [-46,0] in units of 1/8. Their outputs are
`w-turnstheory/row_stability_certificate.txt` and
`w-turnstheory/row_stability_independent.txt`. The geometric and row-pattern
checks remain those in 7.5. No estimate of the optimal stability constant
is needed here; the converged potential at 1/2 is the certificate.

## 8. The 4.5 ceiling: boundary data and unused tile counts

Date: 2026-10-02. This section separates two proved counting facts from an
unproved route to a stronger bound. It does not change the bad-row loss 6d.

### 8.1. Corner charges alone cannot force more than 2n paths

**PROVEN limitation of the boundary-height data.** On an m by m square
dual grid with m >= 3, prescribe height 0 on the left and right sides, and height 1
on the top and bottom sides. Omit the four corner vertices from the
prescribed terminal sets. There are at most 2m edge-disjoint paths with
prescribed endpoints of unequal height.

Proof: Extend this boundary assignment to an auxiliary height f. Set f=1
on the top and bottom rows except their corner vertices, and f=0 elsewhere.
The edges on which f changes are the 2(m-2) inward edges from these rows
and four edges to the corner vertices: exactly 2m edges. Every path from a
prescribed 0 terminal to a prescribed 1 terminal uses one of these edges.
Edge-disjoint paths use different edges. This proves the bound.

This assignment is consistent with all four ideal corner charges used in
7.3, for every radius at once. In counterclockwise order the charges are
+1,-1,+1,-1: rotation by 90 degrees on an even board exchanges black and
white, while rotation by 180 degrees preserves them. Thus the assignment
left=right=0, bottom=top=1 meets all these constraints. Removing a fixed
corner margin changes the count only by O(1), and m=n-O(1).

Consequently, the corner constraints alone admit a height field with only
2n+O(1) nonzero steps. A proof based only on those boundary constraints
cannot force more than 2n+O(1) disjoint charged paths. This is an abstract
height assignment, not a claimed knight tour or tile configuration.
The knight-edge constraints may rule it out. Extra forced interior height
data, or a stronger cost for each defect, is needed to pass this ceiling.
Merely adding more radii or changing the routes does not supply that data.

### 8.2. An exact stronger defect budget

There is a separate loss in the coefficient 4 multiplying E. We can state
it exactly without changing any row estimates.

For a proper crossing pair c, let a_c be its number of common quarter
triangles. Section 6 proves a_c is 1 or 2. Define

    J = sum_c (2-a_c),
    Q = sum_t [binomial(m_t,2) - (m_t-1)_+].

The sum defining Q is over triangles inside the board. Both J and Q are
nonnegative integers. J counts crossings with overlap area 1/4. Q measures
the extra pair count at triangles with multiplicity at least three.
The exact area and pair counts give

    2X-J = 8n-4+G+Q,
    G = 2E-J-Q.                                      (8.1)

For the boundary crossing set B of 7.2, split J=J_B+J_I, where J_I is the
sum over all crossing pairs outside B. Since overlaps from B avoid U,

    number of multiply covered triangles in U
        <= sum_{c outside B} a_c = 2(X-|B|)-J_I.

Add the gap bound (8.1). The injective path charge of 6.5 now gives

    L <= 4E+92+2d - S,
    S := J_B+2J_I+Q >= 0.

Use the same L >= 2n-60-4d as before:

    2n <= 4E+6d+152-S.                              (8.2)

All statements up to (8.2) are **PROVEN**. They identify exactly where
crossings with smaller tile overlap, or triple coverage, improve this
part of the count. This improvement is separate from the loss 6d.

### 8.3. A precise open target beyond 4.5

**UNPROVEN sufficient target:** find beta>0 such that every closed tour
in the relevant low-crossing regime satisfies

    J_B+2J_I+Q >= 6d+beta*n-O(1).

Then (8.2) would give X >= (4.5+beta/4)n-O(1), without additional boundary
paths. For perfectly cheap sides, d=O(1), so it would suffice to force a
linear number of quarter-area crossings or excess multiplicities. No such
forcing theorem is proved here. In particular, the abstract height example
in 8.1 does not establish it. An alternative is to force additional interior
terminal charges from the knight-edge constraints, but the present corner
certificate gives no such interior data. Thus the unconditional theorem
proved in this report is now the one in 7.7.

## 9. Past 4.5: square defects, and a limit of the J,Q route

Date: 2026-10-02. **Status:** no unconditional bound past 4.5n is proved
here. There is a new local counting theorem. It raises the bound for
O(1) bad boundary rows from 4.5n-O(1) to **5n-O(1)**, without a new
stability estimate. There is also an explicit counterexample to forcing
positive J or Q from nonzero transported charge alone. The definition
and treatment of bad rows remain those of Sections 7.1--7.4.

### 9.1. Every defective square has at least two bad quarters

**PROVEN.** Number the quarter triangles of a unit square by 0,1,2,3,
starting at its bottom side and proceeding counterclockwise. For any
selected set of knight edges, its tile multiplicities satisfy

    m_0 - m_1 + m_2 - m_3 = 0.                         (9.1)

Indeed, one knight tile meets exactly two unit squares. In each square
it occupies two adjacent quarter triangles. Its contribution to the
alternating sum is zero. Sum this identity over the selected edges.
This argument needs neither degree two nor a tour.

Subtract the all-one vector. If one multiplicity differs from one, at
least one other must differ from one, by (9.1). Thus every defective
square has at least two bad quarters. This includes both gaps and
multiply covered quarters. It does not require J=0 or Q=0.

**Finite geometry check:** `check_square_defects.py` checks the adjacent
quarter property for all four unoriented knight directions and all four
translation parities. The proof above then applies to every square and
every edge set. No solver is used.

### 9.2. Vertex-disjoint paths improve the defect budget by two

**PROVEN.** Let L charged paths in the internal degree-two height domain
be vertex-disjoint. Let U contain all four quarters of every unit square
whose centre is a vertex of one of these paths. Suppose every square is
inside the board, and the boundary crossing set B has no tile overlap
in U. Then

    2L <= 4X-8n+4-2|B|.                                (9.2)

Proof: A charged path has a step with nonzero height change. By (6.2), one
of the two adjacent quarter triangles is bad. The centre of its unit
square is an endpoint of that step, so it belongs to the path. By (9.1),
that square contains at least two bad quarters. Distinct paths use
different square centres, hence give disjoint sets of at least two bad
quarters. Apply the bad-quarter budget of 6.4 to U.

The enlargement of U is important: it contains the whole square, not
only the two quarters beside a selected step. For the paths gamma_R of
7.3--7.4, this is permitted. Those paths are vertex-disjoint, since nested
right-and-top square arcs do not intersect, and the four corner boxes
are separated. Their unit squares lie in [1,n-2] squared. The boundary
pairs in B overlap only inside the outer unit-wide strips, so their
quarter triangles avoid U, including at the path endpoints.

The stronger budget of 8.2 also applies to this U. With
S=J_B+2J_I+Q >= 0, E=X-4n+2, and d the unchanged bad-row count, it gives

    2L <= 4E+92+2d-S.

Use the existing L >= 2n-60-4d, with no change to the loss per bad row:

    4n <= 4E+10d+212-S,
    X >= 5n-55-(5/2)d+S/4.                             (9.3)

This is the main new inequality. The former 4.5 ceiling was a loss from
counting one bad quarter per path. It is not a ceiling imposed by the
knight tiles. No new lower bound on J or Q is needed to remove it.

In particular, for d <= eta*n+C, (9.3) implies

    X >= (5-(5/2)eta)n - 55-(5/2)C.

This is past 4.5 whenever eta<1/5, and gives 5n-O(1) when d=O(1).
Conversely, a tour with X <= (4.5+delta)n must satisfy

    d >= (1/5-(2/5)delta)n - 22 + S/10.                 (9.4)

Thus any family at or below 4.5n must have a linear number of bad rows.
This is a necessary condition, not a proof that such a family exists.
The current stability estimate does not exclude it. As a direct
by-product only, substituting the already proved d<=2E+2252 gives
X >= (4+1/6)n-950 for closed tours. This uses no new strip computation;
it still falls short of the requested unconditional 4.5 target.

### 9.3. A nonzero-charge seam with J=Q=0

**PROVEN counterexample to a local forcing assertion.** A nonzero mod-3
height jump does not by itself force quarter-area crossings or triple
coverage, even in an infinite degree-two knight graph with no finite
cycle.

Here is an explicit graph on the integer plane. Give p=(x,y) the out-edge

    p -> p+(1,-2)   when y-x >= 0,
    p -> p+(2,-1)   when y-x < 0.

Both directions decrease y-x by three. For a target at level h, both
possible predecessors are at level h+3, where the same rule selects
exactly one of them. Thus every vertex has one incoming and one outgoing
edge. Every out-edge increases x, so the components are infinite paths,
not finite cycles. The graph has period (1,1).

Its square multiplicities are exactly

    (m_0,m_1,m_2,m_3) = (0,2,2,0)  if y=x-2,
                        (1,1,1,1)  otherwise.

To verify this formula, examine the eight possible knight tiles that can
meet a given unit square. Translation by (1,1) leaves the rule unchanged;
away from the interface, the square is in a single straight tiling.
The checker performs the remaining finite cases exactly.

At the square with lower-left corner (0,-2), the two overlapping tiles
come from the crossing edges

    (0,-1)--(2,-2),     (0,0)--(1,-2).

They share quarters 1 and 2. Every crossing is a (1,1) translate of this
pair. Thus there is one crossing per period, every overlap has area 1/2,
and no multiplicity exceeds two: **J=Q=0 everywhere**.

Nevertheless, a vertical dual path at x=1/2 crossing the interface has
nonzero height change. Write its step across the grid edge at height y as

    omega_y = (-1)^y [m_(0,y-1,2)+m_(0,y,0)-2]  (mod 3).

The only nonzero terms are omega_-2=omega_-1=-1. Their sum is -2=1 mod 3.
This carrier therefore transports a nonzero height difference for an
arbitrarily long distance while J and Q stay zero.

This example does not refute a global J+Q lower bound for closed tours:
a finite board must still attach the carrier to its boundary and close
all paths. It does refute a proposed proof that charges positive J or Q
to every fixed-length part of every nonzero-charge carrier. The carrier's
ordinary half-area crossings must be included in any universal transport
cost. A positive per-length cost is not automatically an *additional*
cost beyond the existing tile budget; counting it twice would be invalid.

### 9.4. What is forced by the corner data

**PROVEN scope clarification.** The corner charge is already independent
of a chosen fold reference in 7.3. Four consecutive actual good rows at
each endpoint force the charge on gamma_R, with arbitrary tour edges
elsewhere. Hence the retained radii force charge transport in every tour
that has those endpoint patterns. The new square argument counts its
cost more strongly.

There is no claim here that an arbitrary tour has a charged path at every
radius. Bad endpoint rows are the explicit exception. Nor does the corner
identity force all transport to use a diagonal, a bounded-width corridor,
or a fixed set of line families. The seam in 9.3 shows why a catalogue of
measured carrier costs cannot replace that missing global argument.

For a route that avoids a new estimate on d, (9.3) gives a precise revised
sufficient target: for some epsilon>0, prove in the low-crossing regime

    S >= 10d-(2-4epsilon)n-O(1).

This would imply X >= (4.5+epsilon)n-O(1). **UNPROVEN.** In particular,
forcing S>=c*n alone would not settle the case of a large d. A global
attachment or connectivity constraint is needed; nonzero local flux
alone cannot force S, by 9.3.

### 9.5. Resolved finite test: the proposed lemma is false

**COUNTEREXAMPLES VERIFIED, 2026-10-02.** KT Lower Bounds found feasible
witnesses for the proposed finite lemma at radii 4 and 5. A two-bad-quarter
square can occur deep inside a degree-two region with J=Q=0 locally.
I independently ran the solver-free witness checker on both edge sets.
Thus the local lower bound of two bad quarters in 9.1 is attained even
under these extra restrictions. The proposed stronger lemma is false;
none of the proved bounds above or in 9.6 uses it.

A concrete finite model is:

1. Let V=[-4,4]^2 be integer cells. Variables are all knight edges with
   at least one endpoint in V; their other endpoints are in [-6,6]^2.
2. Require degree two on V and degree at most two at the other endpoints.
   Permit cycles: this proposed lemma concerns local degree constraints.
3. Forbid choosing both members of any edge pair whose tiles share
   exactly one quarter triangle. Require every quarter multiplicity
   induced by selected edges to be at most two.
4. At the unit square [0,1]^2, require exactly two of its four
   multiplicities to differ from one.

The radius-5 witness has central multiplicities (1,1,2,2). Its local
crossings come from the four-edge chain

    (-1,-1)--(0,1),  (-1,0)--(1,1),
    (0,0)--(1,2),    (0,1)--(2,2).

Three consecutive pairs cross with overlap area 1/2. Six double quarters
are balanced by six gap quarters in a 2 by 2 square block. The central
square has two doubles and no gaps; the gaps lie in nearby squares.
Thus surplus and gap quarters need not occupy the same square.

The independent checks returned 161 edges and central (1,1,2,2) for
radius 5, and 112 edges and central (0,0,1,1) for radius 4. Reproduce the
radius-5 check from the project root:

```sh
python3 w-lowerbounds/sq2_check_witness.py w-lowerbounds/sq2_min_R5W4.edges 5
```

For radius 4, `sq2_R4_checked.edges` in this directory contains only the
edge tuples from the original witness, converted to the checker's four-
integer format. It passes the same checker with radius argument 4.
I have not verified the separate solver claim that twelve bad quarters
is the minimum; that claim is not needed for this counterexample.

No gap-free variant is requested. Our charged paths do not supply a
gap-free-neighbourhood hypothesis, and imposing one would remove defects
that the global budget must count. A variant needs a concrete charging
argument before it justifies another computation.

**Checks run on 2026-10-02:**

```sh
python3 w-turnstheory/check_square_defects.py
```

All checks passed. The output is `square_defect_certificate.txt`. They
cover the local alternating identity, the geometry of the vertex-disjoint
path charge, and the explicit J=Q=0 seam. The all-size implications and
the conditional 5n bound are the proofs in 9.1--9.2, not extrapolations
from tested board sizes.

### 9.6. Combine full-square charges with run stability

Date: 2026-10-02. **PROVEN for closed tours, with exact finite inputs:**
for every even n >= 32,

    X >= (4+4/11)n - 736.                              (9.5)

The coefficient proposed by the Chief is correct. Two geometric details
need care: the column-0 overlaps do not avoid all inner squares, and the
claimed one-pair overlap between adjacent side crossing sets is false.
The first issue needs no change to the retained paths. The second changes
only the additive constant in the argument below.

**Full-square exclusion (proof and exhaustive local check).** Consider
knight edges with an endpoint on x=0 and their other endpoint in x>=0.
An overlap of two such tiles can enter a square [1,2] x [j,j+1] only for

    e = (0,j)--(2,j+1),   f = (0,j+1)--(2,j).

Their overlap there is its left quarter. All other overlaps lie in squares
with left coordinate zero; no overlap reaches a square with left coordinate
at least two. `check_col0_squares.py` checks all 20 crossing configurations
with the first boundary endpoint translated to row zero. An intersecting
pair's boundary rows differ by at most four, so the enumeration is complete.

A retained corner path gamma_R meets a unit square at x in [1,2] only at
its endpoint (3/2,R+1/2), in the square with j=R. Rows R and R+1 are among
its four required good rows. Consecutive good rows use the same P or P'
pattern. Their column-0 neighbours in column 2 therefore have the same
vertical sign. They cannot contain both e and f above, whose signs are
opposite. Thus the possible inward overlap is absent at every retained
endpoint square. Rotation and reflection give the same fact at the other
sides. The entire squares at all other path vertices are farther inside.
Hence the union U of whole squares used in 9.2 avoids every overlap in B,
where B is the union of all four outermost-column crossing sets.

**Boundary count (corrected finite bound).** The width-one strip certificate
gives at least n-1 crossings on each side. For completeness, the new checker
rebuilds its 330-state graph. Integer weights 3w-1 have a potential p with
p(start)=0, min p=-3, and 3w-1+p(u)-p(v)>=0. Telescoping over 3n transitions
gives X_side>=n-1. A closed tour induces a forest in this proper boundary
strip, as required by that graph.

At a bottom-left corner, the edges incident to both adjacent sides are
exactly

    a=(0,0)--(1,2),  b=(0,0)--(2,1),
    c=(0,1)--(2,0),  d=(0,2)--(1,0).

There are five proper crossing pairs among them: a-c, a-d, b-c, b-d, c-d.
In particular a-c and b-c can both occur. The saved FOLD24 tour at n=96
has two duplicated crossing pairs at each corner. Thus the claim in
TILE_INPUTS.md Section 7 that at most one pair can be shared is not valid.
This does not disprove its numerical bound on |B| by some other argument;
it means that its stated overlap argument does not prove that bound.

Opposite sides cannot share an edge for n>=32. Subtracting at most five
pairs at each corner gives the safe bound

    |B| >= 4(n-1)-20 = 4n-24.

No new claim about sharpness of this additive constant is needed.
With E=X-4n+2, the full-square count in 9.2 now gives

    2L <= 4X-8n+4-2|B| <= 4E+44.                       (9.6)

The right-hand side can also be reduced by S_B=J_B+2J_notB+Q>=0, with J_B
and J_notB defined using this new B. We do not need that improvement.

**Run count and stability.** Let

    R = sum over all sides and all maximal bad-row runs of (k+3),

where k is the run length. A run hitting only one corner's endpoint range
removes at most k+3 candidate radii. If a run meets both endpoint ranges
on a side, split it into two parts; the loss is at most k+6. At most one
run per side can do this. Therefore, allowing a safe extra three per side,

    L >= 2n-60-R-12.

This uses KT Lower Bounds' run estimate without changing the definition
of a bad row or making a new stability claim.

Their certified 2/7 stability has integer potential in [-167,0] for arc
weights 7(4w-1)-8*loss. Here a bad row costs one, and the first bad row of
a run costs three more. With initial flags zero, the total loss on a side
is exactly its sum of k+3. Telescoping in units 1/28 gives

    X_sigma-n >= (2/7)R_sigma - 167/28.

Use the existing sum X_sigma <= X+1104 for the four width-two strips:

    R <= (7/2)(X+1104-4n+167/7)
      = (7/2)E + 7881/2.

Combine this with (9.6), keeping the twelve extra lost radii explicit:

    4n <= 4E+188+2R <= 11E+8069,
    X >= (4+4/11)n - 8091/11
      >= (4+4/11)n - 736.

This proves (9.5). Its scope remains closed Hamiltonian tours, because the
strip certificates exclude closed components inside a strip.

**Checks, all passed on 2026-10-02.** From the project root:

```sh
python3 w-turnstheory/check_square_defects.py
python3 w-turnstheory/check_col0_squares.py
```

For the run potential, from `w-lowerbounds`:

```sh
../.venv/bin/python -c "exec(open('kappa2_star.py').read().split('lo, hi = Fraction(1, 5), Fraction(2)')[0]); good, dist=ok3(Fraction(2,7),100000); assert good; print(int(dist.min()),int(dist.max()))"
python3 -c 'import strip2_independent as s; assert s.run_check(2,7,1,3)'
```

The first run command checks the positive 2/7 certificate without the
unneeded negative-cycle search. Both implementations converged to range
[-167,0]. Outputs are `col0_square_certificate.txt`,
`run_square_certificate.txt`, and `run_square_independent.txt` in this
directory. The original corner-charge and good-row pattern certificates
are unchanged.

## 10. Reduce the loss at the endpoints

### 10.0. Chosen route

Date: 2026-10-02. The most promising route is to reduce the endpoint data
needed by the corner-charge identity. The current test asks for four
complete good rows at each end, although its residual coefficients use
only selected boundary incidences. A shorter sufficient condition would
reduce how many radii one bad run removes. The square count and the
full-square exclusion can then stay unchanged. I will first check which
endpoint incidences actually determine the charge, and request a new
finite stability calculation only if that check gives a proved smaller
condition.

### 10.1. One critical scan row fixes the required endpoint data

**PROVEN, with a finite strip check.** A good row in the existing definition
(all four scan transitions on one P/P' cycle) fixes every selected and
absent strip edge whose endpoint rows straddle that row. This is stronger
than knowing only the two neighbours of the cells in columns zero and one.

Before row R is processed, its state contains every selected pending edge
with lower endpoint row below R and upper endpoint row at least R. During
the four transitions it introduces every selected edge with lower endpoint
row R. The state after the row contains all those edges still pending.
No knight edge in this strip has zero vertical displacement. Consequently
these states together determine every strip edge e with

    min_y(e) <= R <= max_y(e).

For a critical row, all five states (before, between, and after its four
transitions) are specified by one of the two four-state cycles. Their edge
union is exactly the set of P or P' edges straddling row R. Absence is
specified as well as presence. `check_one_row_strip.py` rebuilds the strip
graph, identifies its two critical cycles, and checks this equality for
both cycles. The last state's coordinates are shifted back by one row
before taking the union.

### 10.2. The corner needs only that one row

**PROVEN.** In the degree cancellation of 7.3, include boundary cells
(0,y) and (y,0) for 4<=y<=R-1, rather than stopping at R-2. This is a
valid use of their degree-two equations. After cancellation, the nonzero
coefficients outside the seven-cell corner set K all lie on strip edges
straddling row R on the left, or column R on the bottom.

For clarity, the complete left-end list is below. Coordinates are relative
to row R. Multiply the coefficient column by chi(0,R). The bottom-end
list is its transpose.

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

Each listed edge is fixed by a critical scan row, by 10.1. Its total
normalised contribution is -1 for P and also -1 for P'. The residual
corner enumeration therefore gives exactly the same identity as before:

    integral_(Q_R) omega_H = 1 mod 3.

Thus gamma_R is charged if the single scan row R on each of its two sides
is good. `check_corner_one_row.py` verifies the complete residual support,
all four pattern choices, all 2,916 corner choices, and R=12,13,14,15.
The R -> R+2 proof is unchanged: two opposite-colour boundary cells are
added on each side, while the endpoint terms translate by two.

This does not claim that the ordinary neighbour pattern on just one row
is sufficient. The full critical scan state supplies pending edges that
skip that row, such as (0,R-1)--(1,R+1). That distinction is essential.

The full-square exclusion in 9.6 also survives. Its only possible inward
overlap uses the pair

    (0,R)--(2,R+1),  (0,R+1)--(2,R).

Both edges straddle row R, so 10.1 fixes their status. P and P' never
contain both. Under a reflection, the endpoint square is below the fixed
row rather than above it; the reflected exceptional pair still straddles
that row, and the same argument applies.

### 10.3. Combined theorem: coefficient 9/2

Date: 2026-10-02. **PROVEN for closed tours:** for every even n>=32,

    X >= 9n/2 - 585.                                  (10.1)

Keep the same 2n-60 nested corner paths. On each side, the scan-row indices
used by its two corners are disjoint: they lie in [12,n/2-4] and
[n/2+3,n-13]. A bad scan row therefore removes at most one candidate path
in total. No run penalty is needed. Hence

    L >= 2n-60-d.

All retained paths are vertex-disjoint and charged, and their whole
squares avoid B by 10.2. The corrected boundary bound |B|>=4n-24 from 9.6
therefore gives

    2L <= 4E+44,
    4n <= 4E+2d+164,

where E=X-4n+2. Use the already certified per-row stability from 7.7,
without rounding 46/8 up to six. Summed over the four width-two strips,

    d <= 2(sum X_sigma-4n+23)
      <= 2(X+1104-4n+23)
       = 2E+2250.

Consequently

    4n <= 8E+4664,
    E >= n/2-583,
    X >= 9n/2-585.

Only the endpoint lemma has changed. The square count, the corrected
boundary crossing count, and the per-row stability certificate are the
ones already proved. The restriction to closed tours still comes from
the forest condition in the strip graph.

**Checks passed on 2026-10-02:**

```sh
python3 w-turnstheory/check_one_row_strip.py
python3 w-turnstheory/check_corner_one_row.py
python3 w-turnstheory/check_col0_squares.py
python3 w-turnstheory/check_square_defects.py
```

New outputs are `one_row_strip_certificate.txt` and
`one_row_corner_certificate.txt`. The strip check uses only the standard
library and verifies 82,516 states and 144,674 arcs. The potential from
7.7 remains [-46,0] in units of 1/8; its two independent successful checks
are saved as `row_stability_certificate.txt` and
`row_stability_independent.txt`.

An intermediate two-row proof also passed (`check_corner_two_rows.py`),
as did a stability check for loss k+1 at coefficient 2/5, with potential
[-117,0] in units of 1/20. Neither intermediate result is needed in (10.1).

### 10.4. A weaker endpoint test for the next finite calculation

**PROVEN sufficient local test; the stability task is resolved in 10.5.** Let F be the sum of
the eight selected-edge coefficients in the table in 10.2, without the
factor chi(0,R). The corner computation uses only F modulo three.
An endpoint is therefore sufficient when

    F = -1 mod 3,

and the two edges of the inward-overlap exception are not both present.
This permits many scan rows that are not critical P/P' rows. Reflect the
coefficient list and the exceptional pair for the opposite orientation
of the side. The reflected test has the same sufficient property.

Let b count failures of the appropriate test in the row range used by
each corner. If a strip certificate proves, for some beta>1/2,

    X_sigma-n >= beta*b_sigma - C,

then the same proof yields

    X >= [4 + 2beta/(2beta+1)]n - O(1),

which is strictly above 4.5. Separate potentials for the two reflected
tests are enough: split the strip walk between the two corner row ranges;
this changes only the endpoint constant. A joint test requiring both
orientations at every row is also sufficient, but is more restrictive.

The new finite question is therefore specific: find a positive potential
certificate with beta>1/2 for this residue-and-overlap test, or give a
cycle showing that no such coefficient is possible in the strip model.
`QUESTIONS.md` specifies the exact data to accumulate in the scan. I have
not run that larger augmented-state computation and make no claim that
beta>1/2 exists.

### 10.5. Joint endpoint stability gives 14n/3-407 (2026-10-02)

**PROVEN, with an exact finite certificate.** The weaker test in 10.4 now
has coefficient beta=1. Use the joint test: a row fails if either its
up test or its reflected down test fails. KT Lower Bounds supplies the
certificate in `TILE_INPUTS.md` section 9. I re-ran the independent
implementation through `check_lower_stability.py`. Its augmented strip
graph admits integer potentials in [-29,0] with

    4w-1-4f+p(u)-p(v) >= 0,

where f=1 at the end of a failed row, and zero otherwise. The independent
checker reaches a fixed point after integer relaxation over every arc;
the wrapper requires convergence and the stated potential range. Thus
on each side sigma,

    X_sigma-n >= b_sigma-29/4.

Here b_sigma counts failed joint tests. The joint condition handles both
corners of the side without splitting the walk. Sum over the four sides
and use the existing strip overlap error 1104, with E=X-4n+2:

    b <= sum_sigma X_sigma-4n+29 <= E+1131.

A passing endpoint gives both the nonzero corner charge and absence of
the inward tile overlap. Each failed row removes at most one of the
2n-60 candidate paths. The same whole-square budget therefore gives

    L >= 2n-60-b,              2L <= 4E+44,
    4n <= 4E+2b+164 <= 6E+2426.

Consequently E>=2n/3-1213/3 and X>=14n/3-1219/3. In particular:

**Theorem.** Every closed knight's tour on an even n by n board, n>=32,
has X>=14n/3-407 proper crossing pairs.

The proof needs beta=1, not its optimality. KT Lower Bounds also reports
a cycle proving sharpness of beta=1 in this strip model; that extra claim
is not an input to this theorem. The independent certificate command is

```sh
python3 w-lowerbounds/endpoint_independent.py both 1 1
python3 w-turnstheory/check_crossings_lower.py
```

**Final document for standalone audit:** `PROOF_crossings_lower.md` now
states the stronger theorem, defines both endpoint tests, gives the
larger-box corner argument, and includes every finite input and checker
command. The former open slot is filled. The unified checker writes
`crossings_lower_checks.json`; its text output is saved in
`crossings_lower_checks.txt`. Section 10.6 records the box simplification
used in that document; its reference to the older bound describes the
change before this stronger stability certificate was applied.

### 10.6. Simpler one-row corner proof (2026-10-02)

**PROVEN; finite end-flux check.** The larger cell box [0,R]^2 removes
both the seven-cell corner enumeration and the middle boundary degree
cancellation. Keep gamma_R unchanged. The rest of its dual boundary lies
outside the board, apart from two top and two right end steps. Every
knight edge through the top steps straddles scan row R and has an endpoint
in columns 0 or 1. Thus one good scan row fixes all eight possible edges.
Each pattern sign gives top flux chi(0,R); transposition gives right flux
chi(R,0). The outside unit-grid flux is 1+(-1)^R in total, and the four
end steps have zero unit-grid flux. The complementary path therefore has
flux 1+3(-1)^R, which is 1 modulo three.

The full box has zero flux modulo three: replace each knight edge by its
three unit lattice steps and telescope the boundary flux. The result is
sum over box cells of chi(v)(deg_H(v)+4)=6 sum chi(v). Only gamma_R is
used in the area count; its vertices and whole squares remain inside the
board. Thus the theorem X>=9n/2-585 and its constants do not change.

The normalised new top-end flux equals the old F from 10.4 plus the degree
of (0,R), hence equals F+2. The checker verifies this coefficient identity.
Therefore the weaker endpoint test in 10.4 is unchanged.

`PROOF_crossings_lower.md` now gives this proof from start to finish.
The standard-library checker is `python3 w-turnstheory/check_corner_box.py`.
The unified command `python3 w-turnstheory/check_crossings_lower.py` uses
this check instead of the old 2,916-case corner check. The old check and
its evidence remain available as a separate proof.

## 11. Recover paths from failed endpoint rows (2026-10-02)

### 11.0. Route choice

The best next step is to keep the existing paths and retain more of them.
The current proof discards a path when either endpoint fails a local test.
But failure does not always make the path uncharged. The exact corner
formula gives three endpoint residues. It permits penalties 0, 1/2, and 1
in place of the binary failure flag. The known sharp strip cycle has
average penalty 3/4, so its obstruction moves from beta=1 to beta=4/3.
This asks for a small change to the existing finite strip calculation,
not a wider strip graph. The new geometric count below is proved. A
stronger weighted stability coefficient is still an open finite task.

### 11.1. The exact endpoint residue

**PROVEN.** Use one corner's local coordinates, with its two sides at
x=0 and y=0. At radius R put c=(-1)^R. Let F be the up-oriented eight-edge
sum in Section 10.4, and let g=F+2 modulo three. Section 10.6 proves that
the tour flux through the two end steps, divided by c, equals g modulo
three. Define the endpoint residue

    h = (1+c)/2 + c*g    in Z/3Z.                      (11.1)

The term (1+c)/2 is the unit-grid flux on that endpoint's outside side
of the larger corner box. For the two ends of gamma_R, the complementary
path Q_R therefore has

    integral_(Q_R) omega = h_left+h_bottom mod 3.       (11.2)

This formula holds for arbitrary selected endpoint edges of a tour.
It does not require a critical row or a passing test. Let e=1 when the
inward-overlap exception at that endpoint is present, and e=0 otherwise.
If both endpoints have e=0, their whole path squares avoid all overlaps
in B. Such a path is charged precisely when h_left+h_bottom is nonzero.
The down-oriented definition is the reflection of this entire local
calculation, including the exceptional pair.

For either cheap pattern P/P', g=1 and h=2 for both parities. For the
known sharp failing pattern, F=1 mod 3, g=0, and h alternates between 1
at even radii and 0 at odd radii. Thus two ends in that failing pattern
still give a charged path at every even radius. With one cheap end and
one failing-pattern end, every odd radius gives a charged path. The
previous binary test discards all these paths.

### 11.2. Half-unit endpoint penalties

**PROVEN.** Give an endpoint penalty a as follows:

| Inward exception e | Residue h | Penalty a |
| --- | --- | ---: |
| 1 | any | 1 |
| 0 | 0 | 1/2 |
| 0 | 1 | 1 |
| 0 | 2 | 0 |

Discard a candidate path only if an endpoint has its inward exception,
or the sum of the two residues is zero. Its discard indicator ell obeys

    ell <= a_left+a_bottom.                            (11.3)

If an exception is present, one penalty is already one. Otherwise, the
only zero-sum pairs are (0,0), (1,2), and (2,1). Their penalty sums are
respectively 1, 1, and 1. This proves (11.3) in all cases.

Let A sum these penalties over the endpoint rows of all 2n-60 candidate
paths. Each endpoint row occurs at most once on its side, as before.
The retained paths are charged, have disjoint vertices, and their whole
squares avoid the same set B. Consequently

    L >= 2n-60-A,          2L <= 4E+44,
    4n <= 4E+2A+164.                                  (11.4)

This is the old geometric inequality with a smaller, fractional loss.
In particular a<=b for the old *oriented* binary test, so this change
cannot weaken the existing theorem. No tour connectivity assumption is
lost: the same forest strip model supplies the remaining stability step.

The finite local check verifies all 36 residue/exception combinations,
the cheap patterns, and the sharp failing pattern:

```sh
python3 w-turnstheory/check_endpoint_loss.py
```

### 11.3. A precise finite task and its consequence

**OPEN FINITE TASK.** In the width-two forest strip, replace the binary
failure charge by a from 11.2. Add the scan-row parity to the finite state.
For each orientation separately, seek an exact potential proving

    sum (w-1/4) >= beta * sum_rows a - C,  beta>1.       (11.5)

Here w is still the transition crossing count. The row accumulator and
exception bits are exactly those of `endpoint_independent.py`; only the
row charge changes. With t=2a in {0,1,2} and beta=p/q, the integer arc
weights are

    q(4w-1)-2p*t,

where t is charged at row end. At other transitions its value is zero.
Toggle parity at row end. A potential range of width M gives C=M/(4q).
Both possible initial parities must be covered. Separate up and down
certificates are sufficient; take C to be the larger endpoint error.

Use the up certificate on the first half of each physical side and the
down certificate on the second half. Their row parities are measured
from their respective corners. The arbitrary initial parity permits
this reversal without a further assumption. Both half walks include
all their rows, so they also pay for the smaller subset used as path
endpoints. There are eight half walks. The existing corner overlap count
then gives

    beta*A <= sum_sigma X_sigma-4n+8C <= E+1102+8C.

Together with (11.4), this would prove

    X >= [4+2beta/(2beta+1)]n
         -2-[1102+8C+82beta]/(2beta+1).                (11.6)

For example beta=4/3 would give 52n/11-O(1), above 14n/3-O(1).
This coefficient is a target, not a claimed certificate. Any beta>1
would improve the current result. The exact computation is specified in
`QUESTIONS.md` for assignment to KT Lower Bounds.

Do not replace the two oriented charges by their maximum at each physical
row. The two corners use opposite row parities on an even board. On the
known failing pattern, that maximum is one at every row and restores the
old obstruction. Splitting each side costs only a bounded potential error.

### 11.4. What the known sharp cycle does and does not rule out

**PROVEN local calculation.** The period-one field

    (1,y)--(0,y+2), (2,y)--(0,y+1), (2,y)--(1,y+2)

has two crossings per row, no inward exception, and penalty 1,1/2 on
successive parities in either oriented test. Its excess crossing rate is
one per row. Thus no certificate (11.5) can have beta>4/3 in this strip
model. It does not rule out beta in (1,4/3]. The local checker assigns
crossing pairs to max(min_y(e),min_y(f)) and finds exactly two pairs per
period. It also checks the residues in both orientations.

The field gives another possible route, but I have not used it in the
count above. It saturates every cell of columns 0,1,2 with degree two.
On a long exact run, a cell in column 3 sufficiently far from the run
ends therefore cannot connect back into columns 1 or 2. Its two tour
edges must go to columns 4 or 5. This creates an additional boundary-like
strip inside the board. A quantified crossing charge for that strip
could help if (11.5) has another obstruction. Such a charge, including
its run-end error and avoidance of double counting, is not proved here.

### Section 11 status: stopped (2026-10-02)

The fractional endpoint-loss inequality is proved and its local check passes.
The stronger weighted strip certificate is unproved; no new lower bound is claimed.
Work on this direction is stopped. The final results remain 14n/3 and 19n/3.

## 12. Final proof documents (2026-10-02)

`PROOF_crossings_lower.md` and `PROOF_fold.md` now present the two final
results, 14n/3-O(1) and 19n/3+O(1), with explicit bounds retained in short
certificate notes. Every section has a figure specification with cells,
edges, cuts, or matching ports to draw.

The lower proof applies the Claim 20 document corrections: explicit
colours and crossing convention, unit dual steps and integer flux,
fixed side scans, normalised reachable strip states, bounded corner
radii, the endpoint normalisation and transposition signs, positive-area
overlap, and the reflected far-end scan row. The critical-cycle
classification and its reduced-cost terminology are removed because the
weaker endpoint certificate does not use them. The old proof-slot history
is removed. Its runner now has five checks; the boundary check no longer
reads a saved tour used only as a historical counterexample.

The fold proof retains the exact placement, all-size geometric insertion,
complete matchings and return paths, the rho/rho-cubed states, and the
local increment 152=120+32. It removes the residue constant table and the
unproved jog-band sketch from the final presentation. The detailed data
remain in the certificate report. No theorem or certificate inequality
has changed.

Validation completed on 2026-10-02, sequentially with one CPU process:

```sh
python3 w-turnstheory/check_crossings_lower.py
python3 w-turnstheory/check_fold_proof.py
```

Both pass. The fold check covers all 36 saved tours and all complete
block/outside matchings; the lower check confirms 14n/3-407. Reports and
text logs are `crossings_lower_checks.json/.txt` and
`fold_proof_checks.json/.txt`. The documents are ready for final reading
and for figures to be drawn from their specifications.

### Final release corrections (2026-10-02)

Applied all four Claim 21 section B replacements verbatim to
`PROOF_crossings_lower.md`. The endpoint columns, exact-degree scan rule,
edge endpoint notation, and geometric corner-overcount arguments are now
explicit. Re-ran `python3 w-turnstheory/check_crossings_lower.py`; all five
checks passed. The document is marked final. `PROOF_fold.md` is unchanged,
as requested by its passing audit.
