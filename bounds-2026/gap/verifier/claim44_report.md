## Claim 44: connectivity surplus in BEYOND5 — 2026-10-03

**Verdict: GAP for B5 and C5. FAIL for the claimed implication from B5-strip to the N_free/2 term in B5: the mixed ledger introduces a factor of two. PASS for deep-first quarter selection, with the capacity and shallow-user qualifications below.** No closed-tour counterexample to C5 was established. The gentle-seam replay confirms that flux can change at zero extra crossing cost, but does not establish vanishing residual BQx.

Sources: gap/structures/BEYOND5.md, beyond5_ledger.py/log, and w-structures/FINDINGS.md S3/S10 with seam_flux.py. Hashes: claim44_sources.json. This is a light audit; no new strip graph was built.

### 44A. What route (i) owns — PASS with precise units and scope

Claim 42 uses the exact identity E=nu+T/2. A retained candidate selects min(2,s_i) PAYABLE QUARTERS and receives one quarter-unit per selection from the prescribed atoms. Deep-first is a valid tie rule. It changes neither the deficient-path condition s_i<2 nor Claim V, which uses all payable quarters on the path.

A selected quarter is not necessarily a whole atom. A two-quarter overlap outside S* has one half-unit pair atom; one selected quarter consumes only one quarter-unit of it. The other quarter may be selected elsewhere using the remainder. Thus the phrase “two quarter atoms” should be replaced by “two quarter requests with their actual atom consumption.” The Claim 39 packing lemma makes this simultaneous fractional use valid.

Each lost or deficient retained candidate owns one distinct strong side-row. That numerical row unit is paid from (T+C)/2, at one half-unit per row. T itself is an excess count, not a separate list of crossing atoms assigned by physical row. The strip potential gives an aggregate inequality. Spatial exclusion from strong rows is therefore a proposed NEW joint certificate condition, not an existing disjointness theorem.

Route (i) can overpay a deficient retained path: when d_i=1/4 it uses its baseline 1/4 plus a full strong-row payment 1/2. This is harmless but must be retained when defining the actual residual budget. Its total is N/2 plus the baseline payments on deficient paths, not always exactly N/2.

**Do not switch to deep-only deficiency.** A path with fewer than two deep quarters can still have two payable shallow quarters and no strong end. Claim V does not classify it as deficient. The source correctly acknowledges these shallow users. The displayed LF4 and TT16 rows have a linear number of them, so an O(1) exception is not a repair.

### 44B. Deep capacity — PASS; shallow ownership remains GAP

At a square of depth at least five from every side, every covering edge endpoint has depth at least four. A width-three strip edge has an endpoint at depth at most two. Thus a pair covering such a deep quarter cannot belong to the width-three crossing union S3. Hole and W3 atoms there also have deep support.

All deep bad quarters are payable. Their simultaneous quarter-unit payments, including selected baseline quarters and the unselected BQx quarters, obey the same packing lemma. Distinct quarters need not use distinct pair atoms; their total usage stays within the pair's half-unit capacity. Accordingly deep baseline plus BQx/4 is sound with actual fractional consumption.

Shallow baseline quarters can use pairs in S3 minus S*. These were legitimate half-unit atoms in nu, but disappear from the analogous outside-S3 currency. A widened strip lemma must subtract their actual usage or jointly include their demands. Merely requiring changed ports to be far from g rows does not remove this conflict. Shallow users need not themselves own a g row. The source identifies this issue as open; it is a real missing input.

### 44C. Factor-of-two defect in the strip-to-E step — FAIL as a deduction

This problem exists even when every retained baseline payment is deep, so it is independent of the shallow-user issue.

Let s3=|S3|, T3=s3-4n+2, Y=s3-s, and define

    nu3 = (X-s3)/2 + E/2 = nu-Y/2.

Then, exactly,

    E = nu3+T3/2.

Deep quarters remain payable from nu3. After summing sides and absorbing corner overcounts into one constant, the requested B5-strip says

    T3 >= g + N_free/2 - O(1).

Put o=D_loss+L_def, so G_free=g-o. The resulting budget is only

    E >= f0 + BQx/4 + g/2 + N_free/4 - O(1)
      >= N/2 + G_free/2 + N_free/4 + BQx/4 - O(1).

It does NOT supply N_free/2 as written in B5. In general a strip coefficient a on N_free becomes a/2 in this mixed ledger. The extra pairs in Y cannot simply be credited again: Y/2 was exactly what was removed from nu to form nu3.

Two possible repairs are concrete. Ask the strip certificate for coefficient one on N_free, with shallow consumption handled, to obtain B5 as stated. Or retain the requested coefficient one half and weaken B5 to N_free/4. If the original C5 were later proved and the three counts were nonnegative, that weaker B5 would still give a coefficient at least 5+c/8, since

    2G_free+N_free+BQx >= (2G_free+2N_free+BQx)/2.

This is a conditional salvage, not a proof of C5. A stronger joint currency argument could also repair the factor, but none is specified in the design.

### 44D. What the existing table actually tests — FAIL as evidence for C5

beyond5_ledger.py returns C5_ratio=(2*N_re+BQx)/n. It does not compute g rows, G_free, N_free, d0, or the exclusion neighbourhoods. I checked the 11 JSON rows currently in beyond5_ledger.log against that formula. The Markdown table includes additional rows, but has the same proxy column.

There is no supplied inequality converting this proxy to 2(G_free+N_free)+BQx. In particular, many changed ports may lie near already-owned g rows; those ports and rows then contribute to neither free count. Thus the sentence that all tours satisfy C5 with the quoted ratio is not established by this table. Also, the column E-route(i)-N_re/2 omits both BQx/4 and G_free/2; its positivity alone is not a check of full B5.

Repair: implement the requested R-b census using the fixed up/down half-side convention from Claim 42, count every owned row once, and evaluate the exact C5 expression separately for each d0. Use the same deep-first baseline and exact collar partner rule. Do not infer the new counts from T_left or all changed ports. Rows 8..n-9 exclude only O(1) boundary data, but the orientation change and neighbourhood convention still need one fixed definition.

### 44E. Gentle seams and the C5 sharing risk — verified local obstruction, global GAP

I reran the small gentle-seam model with period vector (3,3), width three on each side, one solver worker and a five-second limit per solve. The unconstrained optimum is three crossings per period. Both current -1 and current 0 also have OPTIMAL cost three; current +1 has OPTIMAL cost nine in this phase convention. Saved assignments are in claim44_seam.json. This confirms the precise useful fact: switching between two current classes need not add any crossings to a seam already present for the field transition.

The saved low-cost seams were also unrolled and checked, with independent exact tile-quarter counting. Both have twelve bad quarters per period: six holes and six multiplicity-two quarters. This is four bad quarters per unit seam displacement. This is a local periodic seam test, not a closed tour or a verification of the proposed residual K lemma. No model here includes the actual retained-candidate selections or subtracts their two quarters. Therefore it cannot prove either K in BQx or a counterexample to C5.

The general accounting obstruction is direct: a lower bound on raw bad quarters of a carrier does not survive subtraction of flux-owned quarters without a joint statement. If a carrier supports k freed returns and q retained candidates, a raw bound BQ>=4k yields at best BQx>=4k-2q before any other losses. No relation between q and k, or positive residual density, is proved in the design. The same seam can be relevant to both tasks; separate proofs about it cannot be added.

Nor does a collar odd-current price automatically leave a free row. If its strong rows are the rows already assigned to deficient candidates, K-collar's cost is entirely owned. A constant distance d0 removes some nearby changed ports from consideration; it does not create a new payment for their returns. C5 must show that a one-cycle tour has sufficiently many resources left AFTER these two removals.

The old layout-G computations are not a counterexample: S10 reports that the tested minimal seam templates leave fixed trapped cycles, and the completed n=32 example uses a free seam band with additional cost. Treating those incomplete templates as closed tours would discard exactly the connectivity requirement under examination. Conversely, the finite failures do not prove that all wider or more general sharing layouts are trapped.

### 44F. Labels, repairs and Pareto profile

PROVEN / PASS: the exact mixed identities; deep-first selection among all payable quarters; simultaneous deep-quarter packing; geometric separation of deep quarters from S3; distinct strong-row ownership inherited from Claim 42.

FAIL as stated deductions: B5-strip with coefficient one half implies the requested B5 coefficient one half on N_free; the table's proxy ratio establishes C5. The corrected deductions and required census are above.

CERTIFIED in the small replayed model: two different gentle-seam currents attain the same minimum crossing cost. ARGUMENT / GAP: a uniform residual carrier price after flux subtraction, the ownership version of K-collar, B5 with shallow consumption removed, and C5 for closed tours. No closed-tour refutation was found.

The most useful next action is the exact R-b census, followed by a JOINT small seam window with actual candidate-quarter marks and residual bad-quarter objective. Before building the width-three graph, choose whether the target is coefficient one for the stated B5 or coefficient one half for the weaker conclusion. This audit launches no such graph.

Proof size and finite input: short ledger algebra, a code/data check of the current table, and four small single-worker CP-SAT seam solves plus saved-witness checks. No new crossing coefficient follows. The above-5n connectivity route remains open.
