## Claim 36 — SHEET connectivity red team — 2026-10-03

**FAIL for the original requested (B), and FAIL for the trapping premise of (C).** The already audited FOLD tour family is a counterexample to the proposed current-tour count: W=3n-O(1), but SSR=2n/3+O(1), so W-2SSR=5n/3-O(1). No absolute constant repairs (B). The reason is simpler than a new defect gadget: the construction's arch flips make one end of each long chevron an exception. Its other end can still generate a wall label, but the chord is excluded from the draft's SSR definition, which requires two cheap ends.

For (C), periodic corridor returns connect the opposite phase of the cheap collar matching. They coexist with unchanged cheap collars in one closed tour. They are not P-compatible chevrons and do not form the isolated cycles used in Claim 28. This refutes the stated trapping explanation, not every possible 1/2 lower price for those chords.

**FAIL for (A)'s literal label count. GAP for (D)'s separate prices and capacity assignment.** The final algebra is correct if its premises are supplied, but those premises need revision. No counterexample to X>=5n-O(1) is claimed.


**Version scope.** SHEET.md changed during this audit. Its revised (B) is BQ+2SSR+2EXC>=4n-O(1), and it introduces I for the previously undefined interface labels. The counterexample below refutes the original 2SSR>=W-O(1), which the author has now withdrawn; it does not refute the revised BQ inequality. The revised inequality and B0 remain GAP. Section 36E audits the new barrier argument and records a separate error there. The saved 2,874-word, 171-line source is the revised version.

Sources: SHEET.md, saved as claim36_SHEET_reviewed.md; the audited FOLD construction in Claim 12; its independent assembler claim12_full.py; and the saved n0=96 template. Hashes are in claim36_sources.json. All new checks were light, single-process geometry and graph checks. No optimisation was run.

### 36A. A convention issue that changes the main count — FAIL

The draft gives a label to each **cheap** slot only. An exception slot has no starting label. W,D,X_E count the destinations of these cheap-slot labels. Even if all labels terminate as intended, the literal identity is

    W + D + X_E = number of cheap slots
                = 4n-O(1)-EXC,

not (A). The draft's pleat-stack row silently changes the convention by setting X_E=4n when every starting slot is an exception. Under the stated definition all three counts would instead be zero.

A repair can give an exception slot its own immediately absorbed label, or retain EXC explicitly. The price and multiplicity of an exception absorber must then be reconsidered: its own label and incoming ribbon labels cannot be counted under incompatible conventions.

There is also a missing stopping case. After a bad interruption the next good square may have the other split. This is neither a same-bit continuation on the old chain nor an absorbing cut with two good halves of that chain, and it is not a direct wall face between good squares. The scanner below records this case as UNDEFINED rather than silently making it a wall. The revised draft now calls this fourth label type I, which addresses this stopping case. Its amended equality still omits EXC from the starting-label count.

### 36B. Counterexample to the Sheet Lemma using audited closed tours — FAIL

I used the n0=96 FOLD construction from Claim 12, which is already proved to give a closed Hamiltonian tour for every n=96+48k. These tours are also spanning 2-factors, as required by (B). I rebuilt n=144,192,240,288 with the prior independent assembler and validated each tour again. The n=96 saved tour was checked directly.

For reproducibility I made the collar convention precise: d=3; a slot is cheap when every incident edge at local columns 0,1,2 in rows y-3,...,y+3 agrees with P or P'. In the left P frame the neighbours are

    (0,y): (2,y+1), (1,y+2);
    (1,y): (3,y+1), (0,y-2);
    (2,y): (4,y+1), (0,y-1).

P' reverses the row direction. Reflections/transposition give the other sides. Interior vertices have both coordinates in [3,n-4]; interior squares have lower-left coordinates in [3,n-5]. Chord ends use the row of the exterior endpoint of the cut edge, consistent with the two ports per row in the fixed-field strip convention. Labels start at the corresponding first interior half and are followed exactly along their half chains.

The chosen collar is a concrete version of the draft's intended window. Changing a fixed depth or the bounded offset used to name a port changes only O(1) rows at the finitely many collar phase boundaries in this family. It does not change the coefficients below.

| n | Cheap slots | W | D | Undefined continuations | SSR | W-2SSR |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 96 | 205 | 195 | 3 | 7 | 47 | 101 |
| 144 | 349 | 339 | 3 | 7 | 79 | 181 |
| 192 | 493 | 483 | 3 | 7 | 111 | 261 |
| 240 | 637 | 627 | 3 | 7 | 143 | 341 |
| 288 | 781 | 771 | 3 | 7 | 175 | 421 |

These finite deficits alone would not refute an unspecified O(1). The periodic geometry explains their unbounded growth:

* On each side the construction flips the cheap U-turns on an interval of length n/4. The remaining 3n/4-O(1) slots are cheap. Their H or V ribbon labels reach a midline wall. Diagonal corridor cells run parallel to these ribbons; only O(1) ribbons near the corners or the fixed patch windows are affected. Thus W=3n-O(1).
* Long midpoint chevrons have one end in the flipped interval and one in the unflipped interval. Their interior geometry remains a return, but they are **not SSRs under SHEET's current definition** because one endpoint is not cheap.
* The remaining bulk returns come from the four period-six diagonal corridors. Each corridor period has exactly six path components: one A-to-A return, one B-to-B return, and four A-to-B through paths. A and B denote the pure (2,1) and (1,2) arms of the corner. The quotient components each have five vertices and four edges, so there are no hidden long through components. Every corridor has n/12+O(1) periods. Therefore its two same-side returns per period contribute n/6+O(1), and all four contribute SSR=2n/3+O(1). The finitely many patch windows affect only O(1) chord ends.

The finite corridor claim is independently checked in claim36_corridor.py/json: all four saved templates have 24 edge orbits and the stated six paths. Translating a corridor period by (6,6) preserves these connections; pure-field arms extend them to the same two board sides. The global tour existence and the fixed number of patch windows are the already audited Claim 12 facts. Hence the asymptotic count is not an extrapolation from the five rows of the table.

Consequently 2SSR=4n/3+O(1), while W=3n-O(1), disproving (B). The sample counts satisfy W=3n-93 and SSR=2n/3-17; the exact constants are diagnostic and are not needed for the counterexample.

Evidence: claim36_scan.py, claim36_scan.log, claim36_initial_scan.json, claim36_family_scan.log, claim36_scan.json, the four generated claim36_FOLD_n*.json tours, and claim36_corridor.py/json/log. A separate diagnostic on the saved n=166 FIELD tour also gives a positive deficit (W=306, SSR=66), but is not needed for the infinite-family argument.

**Repair:** distinguish reference returns before a repair from current chords after the repair. If a wall label is to be covered by a current return with an exception endpoint, count that object and route its charge to the exception budget. Alternatively add an explicit wall-label loss term to (B). An O(1) defect term cannot fix this example. Any exception term must share capacity with the exception labels already charged in (D).

### 36C. Actual same-side returns need not be trapped by P — FAIL for the stated premise

The same corridor check gives an explicit non-chevron return. In frame zero, one lifted A-to-A corridor path is

    (0,3), (2,4), (1,2), (-1,1), (-3,0).

Its two A-line labels c=x-2y are -6 and -3. Every translate by (6,6) gives the same pairing phase. The corresponding returns in the actual FOLD tours have two cheap endpoints; the large-board checker traces them as maximal interior chords.

The cheap collar matching is

    P(c)=c-3 for even c, and P(c)=c+3 for odd c.

The corridor returns instead pair an even line c with c+3. Let I denote this opposite matching on one residue-class chain. Then for even c,

    P(I(c)) = c+6.

Thus alternating the unchanged collar matching and these return chords advances along a chain. It does not close each return and a partner into the isolated component used in Claim 28. The finite ends of these chains connect through the construction's bounded patches; the resulting graph is one Hamiltonian cycle.

This is a direct counterexample to “same-side return with two cheap endpoints implies the P-compatible trapping relation.” There are linearly many such returns and no changed cheap collar at their endpoints. Claim 28's trapping proof depended on the **fixed chevron interior matching**, not merely on the names of the sides at the two ends.

The corridor contains crossing defects and pays a substantial cost. Therefore the separate assertion that every such return can receive 1/2 from a suitable joint budget is still GAP, not disproved here. It would need an interior-repair or chord-matching price theorem. It cannot be justified by counting changed side ends alone.

### 36D. Baseline and joint capacity — GAP, with an exact safe budget

The mixed cost c=c_{1/2} is not simply the count of non-B crossing pairs. With W3 zero at uncovered quarters and X1 counted with multiplicity at its quarter,

    sum c = (G+X1+W3)/4 + (X-|B|)/2,
    E = sum c + R/2 + 1,       R=|B|-4n.

This is already a budget above the 4n baseline. Its atoms include holes as well as fractional crossing contributions. Spending disjoint crossing pairs is not, by itself, enough to show that a Gap-Lemma allocation in c and a second pure-crossing repair allocation have disjoint capacity. The same outside crossing contributes to c, and the hole/waste part has already used the global excess identity.

A safe formulation puts the D-label, exception, and return payments into one allocation on c, plus a controlled allocation from the boundary-surplus term R/2. Prove that their total is at most that budget. A side proof granting a full unit of boundary surplus cannot be appended automatically: this particular decomposition exposes only half that surplus separately; the other half is represented in the mixed identity. A different decomposition is possible, but its reserve must be explicit.

Further, one changed local row can make several overlapping width-seven slot windows exceptions. Claim 28 certifies a price per changed **pairing end** in its fixed strip model, not a price per exception window. The claimed >=1/2 per exception slot needs an independent packing or allocation proof. Enlarging the starting-label set to fix (A) also changes how many labels an exception absorber receives.

With genuinely disjoint allocations the final inequality in (D) would be valid. The present draft has no such allocation, and the false current-return count cannot supply it. Lemma F's development on good regions does not fix this: the actual corridor returns pass through bad squares, precisely where that good-region hypothesis stops.

### 36E. Revised barrier argument: wall edges do not block strands — FAIL for that proof step

The revised Section 6 says a wall edge carries no tile, so no tour edge crosses it, and then assigns no crossing capacity to the wall part of a chamber boundary. The first statement concerns proper intersection with an open unit edge. It does not imply the second statement about strands.

Consider the exact crossing-free fold stack with f=y, choosing c[y]=(2,1) for y<0 and c[y]=(-2,1) for y>=0. Squares below y=0 have slash split; squares above have backslash split. All quarters are perfect and every vertex has degree two. The line y=0 is a horizontal wall. For every integer x the strand contains

    (x-2,-1) -- (x,0) -- (x-2,1).

The strand passes from below the wall to above it **at the wall vertex (x,0)**. Neither incident knight edge properly crosses an open unit wall edge. Nevertheless the strand exits a chamber bounded by that wall. Along a wall segment of length l there are l-O(1) such passages, with no bad quarters to pay for them. This is an elementary whole-plane field, not a completion claim for a finite board; it directly tests the local permeability assertion used by the chamber proof.

A Jordan-curve crossing count must either route the barrier away from tour vertices and count the resulting edge intersections, or give an explicit vertex-crossing convention. A small displacement of this wall does not preserve zero capacity. Therefore the displayed chamber estimate and its asserted additivity are not established by the present proof. Adding BQ alone cannot pay these wall-vertex passages, since this local example has BQ=0. This does not refute the revised final inequality, which can use exception terms and different barriers.

For clarity, the revised BQ inequality passes the two examples recomputed after the update: at n=96, BQ=622 and EXC=155 give BQ+2SSR+2EXC=1026; at n=288, BQ=1646 and EXC=347 give 2690. These are larger than 4n. See claim36_revised_scan.log. The original counterexample therefore cannot be relabelled as a counterexample to the revised inequality.

**Pareto profile.** The decisive new finite input is four tiny periodic corridor graphs (24 edge orbits each), together with the previously audited all-size FOLD construction. Five complete tours give direct regression checks; no SAT solver is needed for this audit. The result adds no crossing bound. The simpler 5n goal remains open, but a revised statement must count repairs already made, not demand that their former returns still have two cheap endpoints.

Claim 36 is complete. No author files were edited; all computations have finished.


### 36F. Explicit closeout of the REVISED Sheet Lemma — GAP (2026-10-03)

This section answers the queued request to test the revised statement, rather than the withdrawn original B. The revised universal inequality

    BQ + 2 SSR + 2 EXC >= 4n - O(1)

is **GAP, not refuted** by this audit. The old FOLD counterexample does not refute it. Section 36E refutes a proposed local barrier step, not this final inequality. The new I label repairs one missing stopping case; it does not repair the missing EXC term in (A): since only cheap slots receive labels, the available identity is W+D+I+X_E = 4(n-6)-EXC for d=3, provided the stopping rule is exhaustive.

**Independent direct tests (CERTIFIED for these saved tours only).** I used actual P/P' collar windows and required both SSR endpoints to be cheap, as in SHEET. Interior BQ uses exact quarter multiplicities. These are complete validated tours, hence also spanning 2-factors.

| tour | n | BQ | SSR | EXC | revised left side | 4n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FOLD | 96 | 622 | 47 | 155 | 1026 | 384 |
| FOLD | 288 | 1646 | 175 | 347 | 2690 | 1152 |
| FJOG | 130 | 2544 | 137 | 193 | 3204 | 520 |
| FIELD | 166 | 912 | 66 | 303 | 1650 | 664 |

The first two results are in claim36_scan.json; the two additional runs are in claim36_revised_extra.json. They have substantial slack and provide no evidence for the sharp coefficient near equality. No finite test establishes a statement with an unspecified O(1).

**Measurement mismatch (FAIL as a test of the stated quantities).** The author script sheet_measure.py counts every same-side interior chord, including chords with exception endpoints. SHEET defines SSR to require two cheap endpoints. The script also replaces EXC with the number of rows whose collar crossing count is not one. Equality of a row crossing count does not assert equality of the full P/P' window. For FOLD n=96, running

    PYTHONPATH=w-verifier python3 gap/structures/sheet_measure.py 3 w-integrator/tours/FOLD24_n96.json

returns SSR=223 and EXCp=95, whereas the exact-window test gives SSR=47 and EXC=155. BQ=622 and X=720 agree. Thus the reported proxy left side 1258 is not the stated left side 1026. The two substitutions have opposite effects; a passing proxy total cannot be used as a certificate for B. Repair: check the full collar pattern at both endpoints, use the same inclusive slot interval as SHEET, and report proxy counts separately.

**C and D remain unresolved by the revision.** The explicit opposite-matching corridor in 36C still disproves the claim that actual cheap-ended SSRs must be P-trapped. A separate half-unit price theorem could still hold, but Claim 28 does not establish it. Section 36D's common-capacity requirement also remains: BQ, exception windows and SSR payments need one allocation in the excess budget. None of these gaps is fixed merely by adding BQ to B.

**Required repairs before a 5n proof:** use the corrected label identity; replace the wall-impermeability step with a valid strand count including wall vertices; establish the joint Hall/capacity bound for the revised B (including cheap-to-exception chords); prove a price theorem that covers non-chevron returns; and allocate all three payments in a single excess ledger. These are proof obligations, not requests for further large computation.

**Pareto profile:** this follow-up uses two additional direct tour scans and one small diagnostic script run, with no SAT or transfer-graph input. The obstruction to the proposed proof is the elementary three-vertex wall passage in 36E. The audit establishes no new lower-bound coefficient. Revised B remains a conjecture; C's stated trapping premise is false; the joint price conclusion is a gap. Claim 36 is complete for the revised request.
