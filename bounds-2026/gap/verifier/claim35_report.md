## Claim 35 — rational-shear wall witness and L2 scope — 2026-10-03

**PASS: the 19-edge periodic witness achieves 1/2 crossing per row, has nonzero transverse psi jump, and admits perfect exteriors.** I give an explicit extension to the whole plane, stronger than the supplied finite-cylinder feasibility result. The extended graph has degree two everywhere and no finite cycles.

**GAP: the advertised disproof of L2-v3 at p=2/3.** The example refutes a universal price above 1/2 for unrestricted charged paths across a straight wall. It does not provide the closed tours, actual retained candidates, or unbounded total deficit required to refute L2-v3. The sentence “the 16n/3 route via flux alone fails as stated” is not established for the current skeleton's quantifiers.

Evidence: `claim35_wall.py/json/log`, `claim35_extension_author.log`, `claim35_witness_author.log`, and `claim35_sources.json`, all in gap/verifier. The independent checker imports the verifier's exact tile geometry, not the author's model or witness checker. I read the rational-shear geometry and row-weight code and reran both small author checks. I did not rebuild the 10.6-million-state minimum-mean graph. Thus this audit proves an achievable rate of 1/2; it does not independently certify that no cheaper witness exists in that finite model.

### 35A. Exact periodic graph, degrees, cycles, crossings — PASS

Use the 19 listed edges and translate them by T=(2,4). Write

    u(x,y)=x-floor((y+1)/2).

Modeled vertices have 0<=u<4. Each represented edge has a modeled endpoint, every modeled vertex has degree two, and every other endpoint has degree at most two. There are exactly 19 distinct edge orbits; no duplicate edge is hidden by the period.

To check cycles for all periods, I form the finite quotient graph and retain the integer translation of each edge. It has three components, all paths, on 8, 6, and 8 vertices. Their edge counts are 7, 5, and 7. Hence every lifted component of the represented band is a finite path; no finite cycle can be concealed beyond an unrolling cutoff. This is stronger than merely finding no cycle in a long finite sample.

There are exactly two crossing-pair orbits. Representatives, assigned by the later lower endpoint row, are

    (1,0)--(3,1) with (2,0)--(3,2),
    (2,0)--(3,2) with (2,1)--(4,2).

Both overlaps contain two quarters. There are no one-quarter crossings. Therefore X=2 per four-row period, or 1/2 per row. Since T advances four L-infinity levels along a ray in the region y>x, the rate is also 1/2 per such level. This is a count of unordered crossing pairs, even though the two pairs share one edge.

### 35B. Quarter multiplicities and psi — PASS

I independently enumerate every tile that could cover each tested square. A square is complete exactly when every such tile has a modeled endpoint. The complete-column intervals alternate in width because the witness starts at shear phase one.

Quarter order below is B,R,T,L. Unlisted complete squares have multiplicities (1,1,1,1).

| Square row y | Complete x columns | Non-perfect square and multiplicities | Left-to-right omega sum | psi mod 3 |
| --- | --- | --- | ---: | ---: |
| 0 | 0,1,2,3 | x=2: (1,1,2,2) | 2 | 2 |
| 1 | 1,2,3 | x=2: (2,2,1,1) | -1 | 2 |
| 2 | 1,2,3,4 | x=3: (1,1,0,0) | -4 | 2 |
| 3 | 2,3,4 | x=3: (0,0,1,1) | -1 | 2 |

The first and last complete square in every row are perfect margins. The period has four uncovered quarters and four doubly covered quarters, with no multiplicity above two. These statements initially concern complete squares only; the bare 19-edge band leaves incomplete exterior squares uncovered.

For a horizontal dual step from square (x-1,y) to square (x,y), the lattice endpoint on its left is (x,y+1). The audited residue formula gives

    omega = (-1)^(x+y+1) * (m_R(x-1,y)+m_L(x,y)+1) mod 3.

Summing across the complete interval gives the table. The C++ row check omits a common checkerboard sign depending on the row/frame; that does not change the zero-versus-nonzero test. The supplied verify_witness.py does not itself print or test psi, despite its descriptive header. The independent computation above fills that omission.

### 35C. Perfect exterior: finite check and explicit infinite construction — PASS

I reran `extend_witness.py 2 8`. It reports 160 cylinder vertices, 416 free edge variables, 38 fixed witness edges, 336 quarter constraints, and OPTIMAL feasibility. Its period is (4,8). It imposes degree two away from its soft outer boundary and exact coverage on the specified inner exterior squares. It allows cycles. By itself, this finite-window result would not prove an infinite perfect extension or acyclicity.

There is, however, a direct extension. Let f(x,y)=x-y and define the full-plane fold stack by

    c[t]=(-1,-2) for even t, and c[t]=(2,1) for odd t;
    neighbours of v are v+c[f(v)] and v-c[f(v)-1].

Keep every translated witness edge. Add every edge of this fold stack whose two endpoints are outside the modeled band. The same stack is used on both sides. **Exterior-phase scope:** this is an alternating zigzag field with strand direction (1,-1). At every exterior vertex, one incident edge has move class (2,1) and the other has move class (1,2). It is not a pure straight (2,1) or pure straight (1,2) field. The achieved 1/2 rate is verified for these two matching zigzag exteriors; this audit does not certify the same rate with prescribed pure straight exteriors. The reported straight-field extension infeasibility tests are outside this audit. No knight edge can jump from u<0 to u>=4 without a modeled endpoint, since its u displacement is at most three.

For each of the four row phases I checked every external vertex that could have an edge into the band (u=-3,-2,-1 and u=4,5,6). Its fold-stack neighbours inside the band are exactly its fixed witness neighbours. Thus the union has degree two everywhere. Away from this finite transverse interface it is precisely the full-plane fold stack.

The exact check covers a 24-column transverse range through all four row phases: 96 vertex degrees and 384 quarter multiplicities. Every quarter outside the complete band squares is covered once; complete-square multiplicities remain those in 35B. This range contains the entire interface and every tile that can meet it. Beyond it, perfect coverage follows from the fold-stack formula. There are no additional crossing pairs. This proves two perfect infinite exterior regions, not just a fixed number of perfect collar columns.

For acyclicity, orient the fold-stack strands by increasing f. The even step (-1,-2) leaves u unchanged; the odd step (2,1) increases u by one or two. Therefore u is nondecreasing and increases over every pair of steps. An exterior strand cannot leave the band and return to it while staying in that exterior half-plane. Each finite witness-band path attaches to two infinite exterior tails. Together with the quotient-path check in 35A, this excludes finite cycles in the full-plane extension.

### 35D. What the price obstruction proves

In the extended plane, all crossings and waste are confined to this wall. Each four-row period has

    crossings = 2,   holes = 4,   X1 = 0,   W3 = 0.

Consequently, the mixed local currency lambda*X+(1-lambda)*(G+X1+W3)/2 is exactly two units per period for every lambda. At lambda=2/3, this is 4/3 from the two crossing pairs plus 2/3 from the four holes. Pure crossing capacity is also two units per period. No claim about a finite board's global E is needed for this local calculation.

Take M consecutive charged transverse paths, one per row, in this plane field. For a fixed support radius, their entire eligible atom union contains at most M/2+O(1) capacity, because there are only two capacity units per four wall rows and the radius adds only a bounded number of rows. A requested price p>1/2 therefore has an unbounded Hall deficit (p-1/2)M-O(1). This refutes the broad straight-wall rule even with one total constant allowance.

The paths need not be very small. The standard corner-path shapes

    gamma_R: (R+1/2,3/2) -> (R+1/2,R+1/2) -> (3/2,R+1/2)

cross this wall on their top arm for large R; the other arm lies in a perfect region. The checker explicitly verifies residue 1 for R=12,...,80 in the extended plane. Periodicity and the perfect-region residue zero explain the continuation. Thus restricting the geometric radii to start at 12 does not by itself remove this open-plane obstruction.

### 35E. Why this does not yet refute L2-v3 — GAP

L2-v3 quantifies over closed Hamiltonian tours on even boards n>=128. Its demanded family is the **actual retained** family after the endpoint-residue tests and both exception exclusions. It permits a single unknown finite total deficit C_flux, independent of n and the tour. Its eligibility rule requires the entire atom support to be within radius ten of one path vertex. The revised pure-crossing proposal at the top of PLAN.md keeps these family and error requirements.

The witness and its infinite extension establish neither of the following necessary facts:

1. A family of closed tours can contain arbitrarily long copies of this wall, while linearly many corresponding corner paths pass the actual retention tests.
2. Completing the sides, corners, and one-cycle connections adds only O(1) eligible capacity to the selected Hall family, rather than enough linear capacity to pay its deficit.

Both are material. The perfect infinite exteriors have no board-side degree conditions. Cutting them at x=0 and y=0 does not produce a tour. Nor may an arbitrary charged path be substituted for a retained candidate. All edges in the explicit plane construction have move class (2,1) or (1,2), so they preserve x+y modulo three; a Hamiltonian completion necessarily uses additional structure. No cost or support estimate for that structure is supplied here.

A finite completed example with a positive deficit would still not refute the quantified theorem: C_flux could cover that fixed deficit. A valid disproof needs an unbounded family of completed-tour deficits, or a theorem that embeds these wall patches while controlling both retention and all extra eligible atoms. I have not proved or assumed such an embedding.

**Required wording repair:** “A straight (1,2) wall between perfect infinite regions achieves rate 1/2 and refutes an unrestricted charged-path private price p>1/2. It is a candidate obstruction to L2-v3; closed-tour completion, actual retained-path density, and the total eligible-capacity bound remain open.” Do not mark L2-v3 or the current 16n/3 reduction false on this evidence alone.

**Pareto profile.** Source Section 7.1 is 523 words and 39 lines as read. The verified construction needs only 19 edge orbits, four exact row checks, a three-component quotient graph, and a two-letter exterior formula. The cylinder solver is now corroboration rather than an essential input. The large minimum-mean certificate is not needed to prove the achieved upper rate and was not audited here. No new finite-board lower or upper coefficient follows without the missing global completion argument.

Claim 35 is complete. No author files were edited, and all checks have finished.
