## Claim 40: F1 and the R4 side-certificate specification — 2026-10-03

**Verdict: PASS for F1's sufficiency and R4's Hall-based certificate logic. PASS for the degree/edge-set relaxation. GAP for F1 itself and for a completed finite-state certificate. A naive use of halo quarter atoms is invalid and needs the explicit repair below.** I found no counterexample to F1 in the light tests. The section-8 recheck requested after this task was already completed in Claim 38F–I.

Sources: PROOF_5N_PLAN.md section 4, the current R4 at the top of REQUESTS.md, and END_TYPES.md. This audit uses the Claim 39 hand kernel. No author files were edited and no large graph was built.

### 40A. F1 is sufficient for the claimed algebra — PASS

The baseline must be the actual simultaneous quarter allocation f0 from Claim 39. Each path gets min(2,s_i)/4, with the prescribed atom type for each selected quarter. Subtract its consumption atom by atom to obtain nu'. The residual demand d_i is the difference from one half. F1 asks for a permitted baseline choice and a nonnegative residual allocation from that same nu', with one absolute bound on the sum of deficits. Thus f0+g pays L/2-C_side from nu, without exceeding any atom capacity.

The separate audited reserve pays D_loss/2. Its identity is

    E+580 = nu(total)+(T+1160)/2,
    (T+1160)/2 >= D_loss/2.

Adding gives X>=5n-(612+C_side), exactly as in Claim 39. No extra raw S* crossing capacity, 4n baseline capacity, or endpoint reserve is available in g. X1 and W3 atoms associated with S* pairs remain legitimate components of nu; using them is not double counting, because the mixed identity explicitly separates these atom types.

The quantifier is existential over permitted baseline choices, not “every greedy baseline succeeds.” R4's proposed proof for EVERY locally allowed baseline marking is a stronger sufficient condition. Failure of that stronger marked-state model would not refute F1. Conversely, optimizing convenient marks in a scan proves nothing unless every actual tour has a compatible permitted global choice. The deficit allowance must be one total constant; it cannot restart at a deficient path, selected subset, gap, or artificial window. State g>=0 explicitly when restating R4's equations alone; it is already explicit in the mathematical F1 definition.

### 40B. Hall augmentation and endpoint pairing — PASS as a sufficient scheme

The old scalar “total capacity minus total demand” scan was insufficient. Current R4 repairs this by allowing every subset of target rows, demanding t(tau_r) only on selected rows, and counting an atom once exactly when at least one selected endpoint can use it. For fixed geometry and residual capacities, a bound

    capacity(N(J)) - sum_(r in J) t(tau_r) >= -M

for all J is precisely a bound M on total max-flow deficit in quarter units. It yields individual endpoint payments with total error at most M/4, not M/4 per row. Nonnegative endpoint demands whose sum dominates each paired path's residual demand then give path payments with no larger total error.

The anchor (3/2,r+1/2) is an actual path vertex. Restricting to atoms wholly within radius ten of this anchor is therefore safe, but stronger than F1's whole-path eligibility. Its eligible row interval is exactly the stated ceiling/floor interval, provided the entire depth support is within ten of 3/2. A 21-row selection history is conservative for these supports. Activation at the upper eligible row is a valid way to count each atom once, provided its identity, residual capacity and earlier selection history survive until that event.

For targets at local radius at least 33, different physical sides' anchor neighbourhoods are disjoint. For example, a left-side neighbourhood has x<=11.5 and y>=23.5 near the bottom corner; a bottom-side neighbourhood has y<=11.5 and x>=23.5. Opposite sides are separated for n>=128. This justifies summing the four side allocations. The two ORIENTED HALVES of one side are different: their neighbourhoods can overlap. R4 correctly requires continued marks and Hall history and one ownership rule across the orientation change. Resetting the scan and crediting the same atom on both halves would be invalid.

With an integral quarter-unit table and potential width M per half, eight half-walk errors give 2M ordinary units. Thus C_side<=42+2M is correct if all ownership and boundary-state conditions pass. The resulting conditional bound is X>=5n-(654+2M). For rational tables use the full scaling denominator. A potential on only convenient start states is insufficient; actual marked half-walk boundary states must all be covered.

### 40C. Degree relaxation — PASS; halo atoms require a repair

Retain exactly the actual tour edges with an endpoint in columns 0 through 5. Every vertex in these columns still has degree two. Columns 6 and 7 have degree at most two in the retained graph, and every retained edge ends by column 7. Therefore the proposed edge/degree model includes every actual tour restriction. Optional forest constraints are safe on this proper subgraph of a Hamiltonian cycle, provided the scan's component handling is correct. They are not required for a certificate valid on the larger degree-only class.

However, this does NOT give full-tour multiplicities at every square inside the apparent eight-column strip. Squares at depth 6 may have covering edges with neither endpoint in columns 0 through 5. A missing tile can create a false hole.

An explicit example is the perfect P half-plane. For x>=2 its edges are (x,y)--(x+2,y+1), with the standard P pairings in columns 0 and 1. After retaining only edges touching columns 0 through 5, the B and R quarters of square (6,y) become uncovered. In the full field they are covered once by the omitted edge (6,y)--(8,y+1). Thus the truncated model would invent TWO quarter-unit hole atoms per row if its halo multiplicities were treated as full multiplicities. These false atoms lie within the endpoint anchor's radius-ten depth range. This is a real resource-encoding error, not just an unextendible edge assignment.

**Exact safe repair:** use hole and W3 quarter atoms only in square columns 0 through 5, where every possible covering edge is represented. Alternatively represent the missing covering edges and their effect on the full multiplicity. Restricting quarter atoms to the complete columns is sufficient and simpler. For pair and X1 atoms, require both edges to be represented and compute their one/two-quarter overlap from the two full tiles. Their geometric pair capacity does not depend on absent third tiles. Omit all other resources. This is a safe restricted resource pool, not an equality with the tour's full nu.

For a represented pair atom, baseline consumption can come from either overlap quarter, including one in an incompletely represented square. The state must still subtract ALL actual f0 consumption of that pair. Allowing all feasible 0/1/2 consumption marks is a safe relaxation; declaring “no visible mark, no consumption” without accounting for the missing quarter is not. Similarly, quarter multiplicity zero must never be inferred from an incomplete owner set.

### 40D. Baseline flags and finite-state scope — GAP until mapped

Actual tours map into the proposed marking relaxation if the state admits the actual selected quarters, exact atom consumptions, candidate quotas and deficiency flags. For a deficient path all its payable quarters are mandatory baseline selections, and its two end records must agree on the total count and flag. A single-side relaxation may omit remote consistency and admit more states; a bound valid on all those states is sufficient. It may also become too strong to certify.

For fully paid paths, local marks do not determine which two quarters the global baseline selected. For deficient paths, locally good represented middle squares do not prove the unseen entire middle is good. These are reasons to permit additional flags/marks, not reasons to discard states. Any restriction based on realizability, a preferred baseline policy, remote compatibility, or good-middle continuation needs a mapping proof. No one-bit continuation through interrupted runs is available.

The listed finite domains and delayed Hall rule are plausible sufficient state ingredients, not a completeness theorem. Resource ownership, possible consumption from unrepresented squares, finalization of late endpoint types, and all actual boundary states must be checked in the implementation. R4 correctly asks for that proof before declaring a certificate. The recommended next stage is the small end-type/table pilot with the halo repair, not a full transfer graph yet.

### 40E. Light red-team tests and their limits

**Actual tours, baseline-subtracted Hall tests.** claim40_residual.py uses the audited exact retained-path/atom builder, then independently selects baseline quarters, subtracts their prescribed atom capacities, and solves the variable-demand residual flow. It tries three permitted tie policies: lexicographic, deepest-first and shallowest-first. It omits r<=32 for payment, reserving the allowed corner error. For each policy it tests the whole path collar, the union of the two endpoint-anchor neighbourhoods, and the more restrictive side-strip resource pool with the safe complete-column quarter rule above.

| Tour | n | Retained r>32 | Deficient paths | Residual demand | Unpaid after residual flow |
| --- | ---: | ---: | ---: | ---: | ---: |
| LF5 | 156 | 120 | 0 | 0 | 0 |
| LF5 | 208 | 194 | 0 | 0 | 0 |
| FIELD | 166 | 143 | 1 | 1/2 | 0 |
| Claim 38 modified FOLD | 288 | 365 | 0 | 0 | 0 |

All nine policy/resource combinations pass for each tour. The FIELD path supplies a nonvacuous residual test. The LF5 tours that stressed the earlier 2/3 currency have no remaining demand at half-price after this baseline. Neither does the pairing-preserving-gadget tour used to refute the EXC price. These tests do not prove that every marking works, that an additive endpoint table exists, or that F1 holds universally.

**Periodic starting fields.** claim40_periods.py fixes the period-four blocking field in columns 0 and 1 and permits degree-two completion through column 5, with degree-at-most-two halo columns. Requiring squares 3 through 5 good on every row and minimizing payable quarters at row zero yields an extension with both end squares good on every row. Such an end has zero local charge; two such good ends and a good middle do not produce a retained charged path. It is not a residual-demand counterexample by itself.

The period-eight single-shift blocking field, and the same single-shift construction at period six, are INFEASIBLE under that all-rows-good-middle restriction. This is only a small periodic-model result: it does not exclude a completion with some bad middle rows, isolated deficient rows, a different exterior, or a different period. The solver used one worker and a five-second limit per instance; the reported INFEASIBLE results are completed statuses. The check also exhibits the two false halo holes described above. Separately, exact geometry reproduces all seven anchored S-minus-B double-overlap pairs in END_TYPES.md; see claim40_endpairs.json.

**The (1,2) wall.** Its plane witness is not a side completion. If its bad squares meet a path at depth at least three, Claim 39 pays that path already. To challenge F1 it must instead produce the correct retained endpoint states with the bad squares confined to the shallow end zone. A fixed-width straight (1,2) wall intersects a fixed-depth zone of a vertical side over only a bounded row interval; translating it there does not create a growing family of deficient endpoints. Cutting off its zigzag exterior at the board side also changes degrees and demands a new completion. No closed-tour or repeated-end-zone counterexample follows from that wall witness. This remains a useful local stop test, but its original half-price measurement is neither a proof nor a refutation of F1.

Evidence: claim40_residual.py/json/log; claim40_periods.py/json/log; claim40_endpairs.json. No local patch was promoted to a completed-tour claim. No counterexample to F1 was found.

### 40F. Closeout and Pareto profile

F1 is the correct remaining allocation statement for the conditional 5n algebra. R4's all-subsets augmentation is necessary and sufficient at the endpoint-allocation level once the table, actual-state mapping and ownership are proved. The edge relaxation passes; restrict or complete halo quarter atoms before using it for a resource certificate. Baseline marks and their global interpretation remain part of the required proof.

This audit adds one explicit halo-resource counterexample, seven-pair geometry, three small periodic checks and four actual-tour residual-flow screens. It adds no lower-bound coefficient and no large finite input. The mathematical F1 remains OPEN. Claim 40 is complete, and the lower-priority Claim 38 section-8 recheck is already in the audit log.
