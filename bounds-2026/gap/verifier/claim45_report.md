## Claim 45: C5-4 is false — 2026-10-03

**Verdict: FAIL for C5-4 as defined by BEYOND5 section 8 and r_b.py.** A fixed 6-by-16 collar replacement preserves every exterior connection and hence preserves a closed tour. It creates four strong rows, removes 38 ports from N_free, and changes no deep quarter. Copies at spacing 24 in the audited FOLD family give

    2(G_free+N_free)+BQx = (5/2)n + O(1).

Thus no absolute C can make this expression at least 4n-C. This attacks target (i), the near-g-row exclusion. It does not refute a crossing lower bound of 5.5n, the weaker unspecified-c C5, or the audited 5n proof.

The local certificate, saved complete tours, and the independent count are described below. No author files were changed. Only a small one-worker CP-SAT patch search was used; no strip graph was rebuilt.

### 45A. Exact convention and the replacement

The orientation is the R-b convention: UP for side rows r<n/2 and DOWN for r>=n/2. It is not the OR of both orientations. Owned rows use the stated vertical-end-first rule. N_free uses distance strictly greater than two from every strong row of its side. BQx uses every candidate radius 12..n/2-4 and the stated deep-first selection count. A different orientation convention would define a different conjecture.

The base patch is the pure flipped U collar in a left-side frame:

    neighbours(0,y) = {(2,y+1),(1,y-2)},
    neighbours(1,y) = {(3,y+1),(0,y+2)},
    neighbours(x,y) = {(x+2,y+1),(x-2,y-1)} for x>=2.

Replace only edges whose two endpoints lie in 0<=x<6, 0<=y<16. Keep all edges leaving that box unchanged. The exact removed and added edge lists are in claim45_U_gadget.json. The model fixes the original pairing of every boundary stub and excludes internal cycles. The search found an OPTIMAL patch for its local masking objective in the allotted 15 seconds, with one worker. Optimality is not needed: the saved edge lists are the counterexample certificate.

The separate solver-free validator checks all degrees, every knight move, all 22 boundary-stub pairs, and absence of internal cycles. The old and new pairings agree exactly. Therefore replacing this subgraph inside any one-cycle tour leaves one cycle and visits the same vertices. This is stronger than merely retaining the degree-two condition.

Every changed tile is supported in square columns at most four. Hence no quarter at depth at least five changes. The patch does create shallow defects and costs 71 additional crossing pairs. Those extra crossings are allowed: C5-4 is a claim about its specified count on EVERY tour, not about tours that minimize crossings.

### 45B. Independent local count — PROVEN / CERTIFIED

claim45_local_count.py does not use R-b's g or port routines. It reads the saved edge lists, computes the endpoint residues from the audited coefficient table, tests the seven exact Claim 42 VIS pairs, traces collar partners to completion, and applies the fixed P/P' partner rule. Its results are:

| Quantity | Change per copy |
| --- | ---: |
| Strong rows | +4, at local rows 0,5,9,14 |
| N_free, distance >2 | -38 |
| Deep bad quarters | 0 |
| 2g+2N_free | -68 |

The original U collar has no strong rows and two changed ports per row. The four new strong rows have distance-two neighbourhoods covering every row from -2 through 16. There are no surviving far changed ports in this affected interval. Changed ports outside it retain their original contribution. Copies separated by 24 rows have disjoint affected neighbourhoods and their local changes add.

A preliminary width-four pairing-preserving search was infeasible. The width-six witness is valid; no conclusion about all width-four replacements is needed or used here.

### 45C. Complete-tour checks

I inserted copies only where a larger neighbourhood matched the pure U field, allowing all four side rotations/reflections. Each resulting board passed the full closed-tour checker. The R-b census used its exact stated definitions; BQx was recomputed separately from full-tour quarter multiplicities and the audited retained-path set.

| n | Copies | G_free | N_free | BQx | C5 count | C5 count - 4n |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 96 | 0 | 12 | 102 | 292 | 520 | 136 |
| 144 | 0 | 12 | 198 | 356 | 776 | 200 |
| 192 | 4 | 19 | 142 | 438 | 760 | -8 |
| 240 | 4 | 19 | 238 | 502 | 1016 | 56 |
| 288 | 8 | 26 | 182 | 584 | 1000 | -152 |

The n=288 example has X=2504 and is saved as claim45_U_patched_n288.json. The smaller examples have the same filename pattern. Every candidate needing a strong end has one; no Claim V failure occurs. For example, at n=288 there are 25 lost candidates and no deficient retained candidates. These finite deficits alone would not refute an unspecified additive constant; the family argument below does.

As a control, I also checked the earlier Claim 38 replacement family at n=96,144,192,240,288. Its C5 surplus grows rather than shrinks. That family is not the counterexample. Its separate output is claim45_scan.json; the new U-family output is claim45_U_scan.json.

### 45D. Unbounded family and the cancellation of ownership changes — PROVEN

Use the already audited closed FOLD family with n=96+48k. Its explicit assembler in w-verifier/claim12_full.py has four pure U collar intervals, each of length n/4-O(1). The finite exceptional corner/midpoint patches have bounded size; the diagonal templates are away from a fixed-width collar except at bounded endpoint regions. Thus one can insert

    m = n/24 + O(1)

copies in these four intervals, at spacing 24, leaving bounded buffers at every exceptional region. The port-pair certificate proves that the result is a closed tour for every such n. The pure-field check used in the finite insertion code is a conservative way to select these locations.

The deep interior consists of four diagonal corridors, each of length n/2-O(1). The independently audited periodic tile count is 16 bad quarters per (6,6) period of EACH corridor. Hence

    BQ_deep = (16/3)n + O(1).

This is an exact periodic-template argument, not a fitted slope from the five examples. The same templates give at least two bad quarters near the turn of every candidate hook except O(1) hooks meeting the finite gadgets/end zones. I explicitly checked all six radius classes for all four frames: the counts are permutations of [2,2,2,2,4,4]. Those quarters are deep for all but the bounded end radii. They remain untouched by the collar replacement. See claim45_hook_periods.json and the prior exact claim38_corridor_bq.py/json.

Consequently, for every retained candidate except O(1), deep-first selects exactly two deep quarters. Deficient candidates number O(1). If L is the new retained count and D=N-L, then

    BQx = BQ_deep - 2L + O(1),
    G_free = g-D + O(1).

The loss count D may increase linearly after the replacement; it is NOT assumed bounded. It cancels:

    2(G_free+N_free)+BQx
      = 2g + 2N_free + BQ_deep - 2N + O(1).

On the base family g=O(1), N_free=2n+O(1), and N=2n-60. Each copy changes g by +4 and N_free by -38, with BQ_deep and N unchanged. Therefore the new expression is

    (16/3)n - 68m + O(1)
      = (16/3 - 68/24)n + O(1)
      = (5/2)n + O(1).

The deficit from 4n grows as (3/2)n-O(1). This proves that the stated constants C,n0 cannot exist. It also explains the exact -68 per-copy change in the complete-tour table despite changes in retention and owned-row counts.

### 45E. What fails in the ownership plan

The patch is a direct obstruction to P1. Four g rows remove 38 changed ports from N_free, while their own gross contribution is only eight units. Owned-row changes cannot repair this loss: their effect cancels against the lost deep-first selections as shown above. The uncounted payment is in the new shallow defects and excess crossings, not in BQx.

The patch leaves the deep corridors and their flux quarters unchanged. It therefore does NOT require a tour that uses the same deep quarter for both flux and untrapping. Target (ii), the residual deep-quarter disjointness claim, remains unproved, but C5-4 is already false before resolving it. Claim 39's packing and Claim 42's 5n ledger continue to hold on these tours.

A possible repaired statistic must retain enough information about changed ports near strong rows, or count residual shallow-quarter/collar-excess capacity. Simply deleting the entire distance-two neighbourhood of each g row and assigning two units to that row loses a linear amount of the required count. Increasing the excluded distance only worsens this mechanism. A larger weight for g alone would need a new joint certificate, especially when the row is owned. No corrected universal inequality is asserted here.

### 45F. S1 and S2 — separate their local count from the global price

**S1: PASS for the elementary run-end identity; GAP for the complete asserted global chamber reduction.** Partitioning boundary runs into bad starts, through runs, wall ends and bad-square ends gives the stated count. A chosen disjoint family of proper chambers can also partition its own side intervals from the remaining rows. However, the cited SHEET 9.6 explicitly leaves failed zigzags, perpendicular-side endings and an O(1) error PER CHAMBER open. Section 13.3 still has O(number of chambers+1), not one absolute O(1). Calling the entire global step PROOF must not erase these qualifications. A global construction must justify its maximal-region/disjointness convention, handle all failed boundaries, and pay or cancel the accumulated endpoint errors. The change from rows 3..n-5 to 8..n-9 costs only a fixed number of rows and is not the issue.

**S2: PASS as the conditional count for a proper chamber; GAP as a disjoint payment theorem.** Let p be its port count and m12 its collar edges of type (1,y)--(2,y+-2). Degree counting gives

    p = 2L-2m12+O(1),
    p = 2R_in+2R_out+X.

For a closed good barrier with crossing capacity at most L+O(1), every outside return crosses it at least twice and every through chord at least once. Thus X+2R_out<=L+O(1), and

    L <= 2R_in+2m12+O(1).

Column-two tile coverage gives p+c>=2L-G2/2-O(1), where c counts non-steep ports. Hence 2m12<=c+G2/2+O(1), and, writing R_in=C_in+U_in,

    L <= 2C_in+2U_in+c+G2/2+O(1).

This proves the displayed local inequality under the stated proper-barrier hypotheses. The local degree/coverage calculation does not prove that c, C_in and G2 can be charged to distinct free resources. A shallow port can be its return's only changed end and also contribute to c: this is precisely the source's unresolved L4'. Nor does this count prove 2U_in<=BQx; subtracting the flux-owned quarters is a separate requirement. Summing local counts also requires control of the per-chamber errors above. These are real gaps even apart from the counterexample to C5-4.

### 45G. Evidence, reproduction and Pareto profile

Discovery: claim45_U_gadget.py/json/log. Solver-free patch proof and full-tour insertion: claim45_U_validate.py, claim45_U_validation.json/log. Independent local g/port count: claim45_local_count.py/json/log. Complete-tour census: claim45_U_scan.py/json/log. Deep periodic hook counts: claim45_hook_periods.json. Source hashes: claim45_sources.json.

Useful reproduction commands from the research root:

    .venv/bin/python gap/verifier/claim45_local_count.py
    .venv/bin/python gap/verifier/claim45_U_validate.py gap/verifier/claim36_FOLD_n288.json
    .venv/bin/python gap/verifier/claim45_U_scan.py gap/verifier/claim45_U_patched_n288.json

The patch validator checks the saved witness without a solver. The census uses the author's R-b g/port implementation and the audited retention builder; the separate local counter independently checks the decisive -68 change. Full-tour degree and connectivity checks are independent of R-b. No wide strip transfer computation was used.

Proof size: one finite 6-by-16 pairing-preserving gadget, its local count, and a short insertion/counting argument on the previously audited FOLD family. The large-n contradiction uses exact periodic structure, not extrapolation from measured deficits. This closes the requested red team with a counterexample to C5-4. Any above-5n connectivity route must replace that statistic or its exclusion rule.


### Claim 45 addendum: revised C5-K and section 9.1 — 2026-10-03

**FAIL for C5-K too. PASS for the displayed ledger, conditional on the new joint strip certificate and its atom ownership.** Read current BEYOND5 sections 9 and 9.1 after the queued update. The same saved U-collar family refutes this revised connectivity count; no new solver run is needed.

Let f_deep be the simultaneous deep-first payment using min(2, number of deep payable quarters) per retained candidate. If K counts lost candidates and retained candidates with fewer than two such quarters, then f_deep >= (N-K)/2. Deep baseline plus BQx/4 uses only deep resources of nu3. The unsubtracted Q3 resources are shallow and separate; the joint strip input would give E >= f_deep+BQx/4+g+N_free/2-O(1). Consequently the proposed E >= N/2+g+N_free/2+BQx/4-K/2-O(1) is a valid scalar deduction. It does not itself prove that each of the K candidates receives a private side allocation, and no such allocation is needed for the scalar deduction. Complete halo multiplicities, one global corner error, and the new joint strip certificate remain requirements.

On every saved counterexample, all retained candidates have two deep selected quarters, so K=D_loss exactly. The revised counts are:

| n | g | K | C5-K | C5-K minus 4n |
| ---: | ---: | ---: | ---: | ---: |
| 96 | 19 | 7 | 558 | 174 |
| 144 | 19 | 7 | 814 | 238 |
| 192 | 35 | 16 | 830 | 62 |
| 240 | 35 | 16 | 1086 | 126 |
| 288 | 51 | 25 | 1102 | -50 |

These numbers are in claim45_K_check.json. For the unbounded family, K=D_loss+O(1) and BQx=BQ_deep-2L+O(1), so

    4g+2N_free+BQx-2K
      = 4g+2N_free+BQ_deep-2N+O(1).

Each gadget adds four g rows, removes 38 far changed ports, and leaves the deep quarters unchanged. Its change to this revised expression is therefore 16-76=-60. The same spacing-24 packing gives m=n/24+O(1), hence

    C5-K = (16/3)n - 60m + O(1) = (17/6)n + O(1).

The deficit from 4n is (7/6)n-O(1), so no additive constant repairs C5-K. Giving g twice its old weight does not recover the many ports removed by the distance-two exclusion. This refutes the revised connectivity input, not the conditional ledger or a 6n crossing bound itself.
