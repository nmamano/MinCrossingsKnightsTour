## Claim 43: red team of BEYOND5_FLUX — 2026-10-03

**Verdict: GAP for F-beyond(p) and for a proof above 5n. PASS for the exact ledger identity and the conditional algebra. FAIL for P6's proposed proportionality to bit alternations, and FAIL for the geometric justification of mu<=2.** These are explicit counterexamples to intermediate claims, not closed-tour counterexamples to F-beyond(p). I found no such tour counterexample in this light audit. The large wall graphs were not rerun.

Sources: gap/searcher/BEYOND5_FLUX.md, WALL12.md, FINDINGS.md sections 7–8, wall/ribbon_ends.out, and the colour-balance lemma in w-integrator/FINDINGS.md. Source hashes: claim43_sources.json. Independent checks: claim43_check.py/json/log.

### 43A. Exact identity and reduction — PROVEN / PASS

With the SAME union S* in both definitions, X_out=X-s and T=s-4n+2. Thus

    E=X-4n+2 = T+X_out

is exact. It agrees with Claim 42's mixed identity: nu(total)=E-T/2=X_out+T/2. The mixed currency does not supply an independent lower bound for X_out; a large T can pay much of the mixed budget.

If X_out>=pL-C, T>=D_loss-1160, and 0<p<=1, then

    E >= p(2n-60)+(1-p)D_loss-C-1160,
    X >= (4+2p)n-(60p+C+1162).

So the stated reduction to a coefficient above five is correct. This does not require local eligibility or a Hall allocation. It still requires a count of distinct crossing-pair capacity in X_out.

**Currency gap in the evidence and zone-end argument.** The cited tests in the design concern crossings outside B, not outside S*. Since B is a subset of S*, they test a larger resource pool. An explicit pair away from the board corners is

    (0,20)--(2,21), (1,20)--(2,22).

Its two overlapping quarters are L and T of square (1,20). Both edges belong to the width-two left strip; only the first edge touches column zero. Thus the pair is in S* minus B: it contributes to the non-B count and contributes NOTHING to X_out. This exact pair is among the independently enumerated Claim 42 VIS types. Its role here is to distinguish the currencies, not to assert a complete tour containing a prescribed repeated patch.

Likewise an end lying in a corner square need not lie outside S*. The end price must either count only pairs outside S*, or be combined with an explicitly revised joint ledger that accounts for its use of T. Merely locating an end near some retained path does not solve this issue. Aggregate accounting also needs wall and end charges whose combined use of each pair is at most one.

### 43B. Mixed-word current counterexample — PROVEN / FAIL for P6

Use the audited perfect '/' word field. Put t=x-y, c_t=(2,1) for H and c_t=(-1,-2) for V, and give vertex v the neighbours

    v+c_t and v-c_(t-1).

Every word gives a degree-two perfect field, with no bad quarters. For a word of period k, let P=k if k is even and P=2k otherwise. Directly count signed edge stubs across x=1/2, with the sign at the left endpoint, over one P-row period. The mean is

    J_x = -(3/P) * sum_(t=0)^(P-1) (-1)^t [w_t=V].

The same parity imbalance determines the other component. It is NOT the number of bit alternations. One derivation is to orient each t-to-t+1 edge with sign (-1)^t: c_t=(2,1)-3[V_t](1,1), and the constant term cancels over an even period. Equivalently count the finitely many edges crossing the cut, as the independent checker does.

Examples, with this fixed phase convention:

| Word | Cyclic bit alternations | Mean vertical-cut current |
| --- | ---: | ---: |
| HV | 2 | 3/2 |
| HHVV | 2 | 0 |
| HHV | 2 | 0 |
| HVVH | 2 | 0 |
| HVVVHV | 4 | 1 |
| VVHHVHVV | 4 | -3/8 |

Thus a nonstraight perfect field can have exactly zero current. Every odd-period word has zero mean over its doubled period. The checker tests all 510 binary words of lengths one through eight; 252 mixed words have zero current. It separately checks degrees, reciprocal neighbours, and exact perfect-quarter coverage for the displayed fields.

There is also no uniform positive current density for words with many alternations. For

    w_m = (HV)^(m+1) (VH)^m,

length is 4m+2, the number of cyclic alternations is 4m, and |J_x|=3/(4m+2), tending to zero. For m=2,4,8,16 the exact currents are 3/10, 1/6, 3/34, 1/22. These are perfectly tiled mixed fields, not noisy patches. Opposite zigzag phases can cancel their signed current.

**Repair:** replace P6 by the exact signed parity statistic and prove a quantitative relation between a wall's discount below 2/3 and a noncancelling current demand. The conservation identity alone cannot give that relation. A price per unit of signed net current cannot control all mixed-word regions or provide a uniform positive addition per level without it. These examples do not show that a cheap psi wall can actually use the zero-current words; that is the missing test/theorem.

**Saved-witness caution.** Interpreting the printed (2,3) margin strings literally as repeating full-plane words gives current magnitudes 3/8 for VVHHVHVV and 3/4 for VHHVVHVH. Cyclic shifts or phase reversals cannot remove this magnitude mismatch. Hence these strings cannot, in that interpretation, be the two fixed exteriors of a colour-balanced bounded-width periodic interface along (2,3). The author already notes that the one-column margins have free ghost cells and are not full exterior fields. This calculation makes that limitation concrete. One must construct and check the actual exteriors before using the strings as current evidence. The corresponding (1,3) strings HVVVHV and HVHHHV both give magnitude one; this consistency check does not prove their extension.

### 43C. One straight ribbon can meet three corners — PROVEN / FAIL for the stated mu<=2 rationale

Take n=200 and the single '/' ribbon indexed by square centres with x-y=40. Use the audited corner paths and their square coordinates. The same uninterrupted line meets candidates from:

- BL: radii 41 through 96, for example square (96,56);
- BR: radii 79 through 96, for example square (119,79);
- TR: radii 41 through 96, for example square (142,102).

It does not meet TL candidates. These are actual candidate-square intersections, verified by the independent path generator. The BR intersections are between the BL and TR parts along the very same line. Therefore the sentence that a '/' stripe passes near only BL and TR is false. It can pass through a third corner box. This is a geometric counterexample, not an assertion that all the intersected paths are retained in a particular closed tour.

An extra restriction on carrier orientations or which intersections are assigned could still prove a useful bound on sharing, but it must be stated and proved. For straight lines the geometry permits three corner families. If mu counts only distinct corners, mu<=4 is automatic and does not itself need field geometry. Neither observation controls repeated use within one corner when carriers branch, have several components, or revisit the same ribbon.

The displayed linear-fractional calculation IS correct under its premises F>=B>=0 and a valid sharing bound. At c=1/3 and mu=3 it gives 11/18, not 2/3; at mu=4 it gives 7/12. Thus this geometric correction alone does not rule out a coefficient above five. The unresolved issue is proving that those premises cover the actual carrier system and that end prices are private in X_out.

### 43D. Bent carriers, finite regions and shared capacity — ARGUMENT / GAP

**Carrier existence is not automatic.** A retained path is charged modulo three. This implies a bad adjacent quarter; it does not by itself specify one connected curve of defects crossing all its corner's levels. Nor does it imply that every such witness is a crossing outside S*. Before cutting a carrier into straight pieces, define its components, how it is selected from the tour, and how it covers the retained paths. Holes and higher multiplicities remain present in the geometry even if the final currency counts only crossings.

**Periodic prices do not add for arbitrary short pieces.** A minimum-mean certificate for a straight band gives a price times length minus a boundary-potential term for a finite segment. Cutting at k bends can introduce k such terms. Nonnegative crossing counts at the bends do not imply that these boundary terms are nonnegative. Rapid switching can make this a linear loss, not one absolute constant. A valid repair is a common state space and a telescoping potential with checked transition costs at bends and branches, or a direct certificate for the whole nonstraight carrier. Claim 42's explicitly checked orientation join is an example of the additional input needed; reflection alone was not enough even there. No bent knight-wall counterexample was built in this audit.

**Conservation gives a signed constraint, not a price.** The finite-set identity in P3 is correct: internal bipartite edges cancel and the boundary signed count is 2(B_S-W_S). The stated periodic-band consequences need their fixed exteriors and periodic colour balance. For a finite irregular region, current can leave through transverse ends, neighbouring opposite-current zones, or a defect region. An O(width) transverse bound does not exclude a region of width proportional to its length. There is no bound here charging that transport or cancellation to a positive density of crossings outside S*. The HHVV and w_m examples show why the word and sign information cannot be suppressed.

**Uniform end price is still missing.** The width-four straight-interface results are author-certified finite-model results. They do not prove a lower bound for wider interfaces: allowing more width enlarges the configuration set and can reduce the optimum. The finite list of rational slopes does not prove an all-slope theorem. Free ghost cells make the finite model a relaxation of its specified fixed-width transitions, not a relaxation containing every arbitrary-width curved end. A positive price at every fixed width also does not imply one uniform c>0 as width increases.

**Shared ends need joint capacity accounting.** Even if a ribbon segment has two ends, several segments can terminate in one defect region. A turn price already counts ends on both sides of that turn. A wall crossing can also be in the endpoint region. The proposed addition of carrier costs and 2c times segment count requires a simultaneous assignment or one combined inequality preventing reuse of those pairs. The global rather than local target removes the radius constraint; it does not remove this capacity constraint.

### 43E. Labels and next useful test

PROVEN: E=T+X_out and the conditional coefficient calculation; the signed colour identity; the mixed-word zero/small-current examples; the three-corner ribbon geometry; the linear-fractional formula under its assumptions.

FAIL: current proportional to bit alternations (P6); the stated geometric reason for mu<=2; using non-B test success as if it certified X_out.

CERTIFIED only in the author's stated finite models, not independently rebuilt here: the width-four straight-wall and end-price tables. Their arbitrary-width, all-slope and curved-interface extensions remain ARGUMENT. The global F-beyond(p) statement remains CONJECTURE, with no counterexample established here.

Before more straight-slope runs, the most discriminating small test is a charged wall with complete fixed exteriors HHVV (zero current), and then w_m with increasing period and small nonzero current. Measure crossings outside the side strips and the current separately. Independently, a whole-window carrier-and-two-ends model should price all crossings once and allow bent interfaces; separate segment minima cannot answer that question. These are proposed tests, not jobs launched by this audit.

**Pareto profile:** this audit uses a short exact current formula, finite quarter checks, 510 word checks, and one candidate-geometry example. It launches no transfer graph or solver. It adds no crossing coefficient. The above-5n route still needs a uniform carrier/end theorem with the correct currency and sharing rules; completing a finite slope table alone will not supply it.
