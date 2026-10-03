## Claim 42: strong visible-overlap test and the 5n bound — 2026-10-03

**Verdict: PASS, with a repaired orientation-join argument. For every even n>=32, every closed knight tour has X >= 5n-612 proper crossing pairs. The same inequality holds for smaller positive even n by X>=0. No 42-unit small-radius allowance is required.**

There is one material correction to the submitted certificate description: UP has potential range [-29,0], but DOWN has range [-33,0] in both the independent reconstruction and the author's current program. Adding eight separate half-side errors would give T+1164, not T+1160. The independently checked common-state interface below repairs this and proves the requested T+1160 bound with room to spare. The theorem does not require the private F1 allocation or a Hall certificate.

Sources: Lower Bounds FINDINGS.md section F; f1v_stab.py and its frac_stab.py/strip_dp.py dependencies; PROOF_5N_PLAN.md; PROOF_52_11.md; audited PROOF_crossings_lower.md. Source hashes are in claim42_sources.json. No author files were changed.

### 42A. Claim V — PASS, with a shorter proof

Use all N=2n-60 candidate paths, including radii 12 through 32 when present. Retain exactly the candidates with neither endpoint exception and nonzero total residue. A lost candidate has a failed oriented test at an end: if both tests pass, each endpoint residue is 2 for either parity, the exceptions are absent, and the sum is nonzero modulo three. Thus a lost candidate owns a strong row.

For a retained deficient path, the Claim 39 baseline selects at most one payable quarter. The path is charged, so the audited flux identity gives a bad quarter in a square centred on a path vertex. The square identity gives at least two bad quarters in that square. At least one is therefore UNPAYABLE. Its multiplicity is exactly two, and its covering pair belongs to S* and has a two-quarter overlap.

Every tile of an edge incident to depth zero or one has its inward coordinate at most three. Its open quarters have square depth at most two. Hence this unpayable quarter is near one physical side. On a candidate path with r>=12, such a square can only be in one of its two end zones; the other physical sides are too far away to supply its covering pair. In that side's up coordinates it is in square (1,r) or (2,r), hence in the stated larger list (1..3,r).

The pair cannot be in the outer-column set B_sigma. The only B_sigma pair with a common quarter at square depth at least one in row r is

    (0,r)--(2,r+1), (0,r+1)--(2,r),

which is precisely the excluded up exception. It has no overlap at square depth two or greater. Reflect this statement for the down end. Thus the unpayable quarter witnesses VIS at that endpoint. This proves V for deficient retained paths even without assuming that both end tests pass.

This also validates the longer submitted charge-localization proof: a deficient path has no bad middle square, and its end-zone nonzero flux leads to the same unpayable quarter. The shorter argument avoids the need to sum separate end-zone fluxes.

Independent exact polygon geometry in claim42_geometry.py finds exactly one outer-column exception pair and seven eligible VIS pairs at an up row. It verifies that every VIS pair crosses properly, has two common quarters, and both edges are pending after that row. The source's square depth three is a harmless extra column; two-quarter strip overlaps reach square depth at most two.

### 42B. The small-radius issue and row ownership — PASS without an extra error

The earlier cutoff r>32 was used for separated local payment neighbourhoods and the proposed side allocation. It is unnecessary for this scalar proof. The quarter-payment rule is valid simultaneously for ANY distinct selected payable quarters. The audited candidate paths have distinct square centres for every radius in [12,n/2-4]. Thus their baseline payments remain private even when neighbourhoods overlap.

For n>=32, each candidate has precisely six squares of depth below four: depths 1,2,3 at each of its two ends. All remaining squares are at depth at least four from every side. Indeed the corner radius is at least 12 and at most n/2-4, while the opposite-side square depths are at least n/2+2. The same inequalities apply after a rotation. The independent code checks every even n from 32 through 258, including every candidate, in addition to this general argument.

Each side-row belongs to at most one candidate endpoint. The near and far intervals [12,n/2-4] and [n/2+3,n-13] are disjoint. Assign one strong end to each lost candidate and each deficient retained candidate. These are disjoint classes of candidates and their chosen rows are distinct. Therefore the strong-row count G satisfies

    G >= D_loss + L_def.

A candidate with two strong ends is assigned only one. Rows from different physical sides are counted separately, as in the strip sum. The corner overcount correction concerns crossing resources, not row ownership.

### 42C. Independent strip reconstruction — PASS

claim42_check.py imports only prior verifier code: the independent forest transitions from Claim 26 and the exact polygon tile geometry from Claim 37. It imports none of the author's graph, endpoint accumulator, VIS, or potential code.

The reconstructed base graph has 82,516 states and 144,674 arcs. Its states retain pending edge geometry and the connectivity partition. Core columns 0 and 1 have degree two; columns 2 and 3 have degree at most two; cycles are rejected. Every restriction of a closed tour to a width-two side is such a forest, since it is a proper subgraph of the one-cycle tour. Crossings are counted once when the later of their two lower endpoints is processed.

Instead of the author's F/exception accumulators, the independent augmentation retains the full selected-edge mask for a row. There are 20 possible strip edges meeting that row. The mask retains edges removed during processing and includes every newly introduced edge. At row end it evaluates the audited endpoint test and the exact geometric VIS predicate from that full set. It then resets the mask. Every base phase-zero state is admitted as a start, so the certificate covers arbitrary actual half-side boundary states.

The independent augmented graph has 184,006 states and 343,631 arcs. Both orientations use this SAME graph. No parity bit is needed: g depends on F modulo three, exceptions and visibility, all independent of row parity. This covers both initial parities; the retention implication F=2 implies h=2 was checked separately for both parities in the audited endpoint proof.

For each orientation the arc cost is exactly

    c = 4w-1-4g,

with g charged only at row end. Four cell transitions per row give 4(X_half-rows-G_half) on a row-aligned subwalk. Integer Bellman-Ford starts from zero at every node and runs to an exact fixed point. A separate final pass checks c+h(u)-h(v)>=0 on EVERY arc. The resulting ranges are UP [-29,0] and DOWN [-33,0]. Both runs stabilize after 41 passes. Full potential arrays and SHA-256 digests are saved with the report.

The independent checker also extracts a zero-slack directed cycle with positive strong-row count, confirming critical rate one for its relaxation. The extracted cycle has 16 arcs, four strong rows, and sum(4w-1)=16. The independent rebuild and certificate checks took about 22 seconds on this box on 2026-10-03. Criticality is not needed for the lower bound; the verified rate-one arc inequalities are the finite proof input.

### 42D. Down orientation and the repaired join — PASS

Reflection y -> -y sends up row r=0 to down row zero, but square row zero to square row minus one. Therefore the down test must inspect VIS in (1..3,r-1), not (1..3,r). The independent code reflects the exact endpoint terms and exception, computes all overlap quarters afresh, and verifies that its seven down VIS pairs are exactly the reflected seven up pairs.

The author's current down code carries the previous row's visibility bit. This is correct: at the end of row r-1, all edges covering its square row are pending; that bit is then used with the down test at r. In the independent full-mask model, those edges are present at the start of row r and are retained in the accumulated mask, so no separate previous-row bit is needed. This provides a different implementation of the same attribution.

Reflection alone does not justify copying the UP potential range: the scan direction and crossing-attribution boundary terms also change. In fact the down range is 33. To retain the claimed constant, use the two independent potentials on their common row-mask state space. The checker verifies at EVERY row boundary

    -4 <= h_up - h_down <= 4.

Split each physical side at row n/2, using up tests on the first half and down tests on the second. Let a,m,z be its start, middle and end states. Summing the two arc inequalities gives

    4(X_sigma-n-G_sigma)
      >= h_up(m)-h_up(a)+h_down(z)-h_down(m)
      >= -4-33 = -37.

Here h_up(a)<=0 and h_down(z)>=-33. This bound permits arbitrary boundary states; it does not need an empty-state shortcut or any assumed agreement of separately optimized baseline marks.

Summing four physical sides gives

    G <= sum_sigma X_sigma - 4n + 37.

The audited union overcount is at most 1104: a pair in two adjacent strips uses edges in a four-by-four corner square, with 24 possible knight edges. Opposite strips do not overlap. With s=|S*| and T=s-4n+2,

    G <= s-4n+1141 = T+1139 <= T+1160.

This is the required repair. Using only the two separate potential widths would instead give T+1164 and would not prove the requested constant by that calculation. The interface inequality above is part of the independently checked finite certificate, not an unverified symmetry claim.

### 42E. Exact ledger and final theorem — PASS

Keep the audited nonnegative mixed currency nu. The tile identity gives

    E=X-4n+2,  nu(total)=E-T/2,
    E+580 = nu(total)+(T+1160)/2.

For each retained path choose min(2,s_i) payable quarters, where s_i is its total payable-quarter count. The simultaneous Claim 39 allocation gives f0_i=1/2-d_i, with 0<=d_i<=1/2. All retained paths with d_i>0 are counted in L_def. The geometric and strip steps above prove

    (T+1160)/2 >= (D_loss+L_def)/2.

Thus

    E+580 >= sum_retained(1/2-d_i)+(D_loss+L_def)/2
           >= (L+D_loss)/2
            = (2n-60)/2 = n-30.

Rearranging gives X>=5n-612. There is no second use of the reserve for D_loss, no residual-capacity claim, and no additional use of the 4n baseline: the exact mixed identity separates these contributions. The baseline uses only its permitted atoms; the single reserve sum pays both disjoint classes once. No per-path or per-stretch error remains.

The proof applies directly for every even n>=32. For positive even n<32 the right side is negative, so X>=0 proves the same stated inequality. Consequently it holds for every positive even board size that admits a closed tour. This audit does not extend the forest certificate to arbitrary disconnected 2-factors or open tours.

### 42F. Evidence and Pareto profile

Run from the research root:

    OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim42_check.py
    .venv/bin/python gap/verifier/claim42_geometry.py

Evidence: claim42_check.json/log; claim42_potential_up.npy; claim42_potential_down.npy; claim42_geometry.json; claim42_sources.json. The author's current down certificate was also rerun, with output in claim42_author_down.log.

The new hand proof is the short deficient-square argument, distinct-row counting, potential joining and final ledger. Its new finite input is the width-two strong-test certificate: an 82,516-state base graph, independently checked through a 184,006-state full-mask augmentation and two integer potential arrays, including their interface difference. It uses no new SAT window lemma, square Gap Lemma, wide-strip graph, private flux allocation, or Hall augmentation. This is a computer-assisted proof with a full independent reconstruction, not a formally verified or DRUP-certified theorem. The required source repair is to state the down range correctly and include the orientation-join inequality. No further price lemma remains for this 5n bound.


### Claim 42 update: revised Lower Bounds section F — 2026-10-03

Checked the current source after the queued update. PASS for the revised separate-half calculation: 4*(29/4)+4*(33/4)=62, hence G<=T+1164, E+582=nu+(T+1164)/2, and X>=5n-614. Its displayed consequence still uses T+1160 and E+580; those lines need the 1164/582 replacement if using only separate-half ranges. No 42 allowance is needed, by 42A–B.

The stronger audited conclusion X>=5n-612 stands: the independent common-mask potentials give h_up-h_down>=-4 at every row boundary, so 42D proves G<=T+1139<=T+1160. This is an additional checked interface input, not a claim that the down width is 29. The source can either use its simpler separate-half proof with constant 614 or cite the checked join for constant 612. No rerun is needed: both orientations and this join were already rebuilt and checked in Claim 42.
