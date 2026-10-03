## Claim 38: SHEET v2, T5 and clean returns — 2026-10-03

**Verdict: FAIL for T5 as written. D_T with the exact exception-window count is false, including its O(1) allowance. B_T and the numerical clean-return inequality remain GAP. The proposed clean-return proof has two missing implications. The repaired label count and the local barrier convention pass with their stated qualifications.** Audit object: gap/structures/SHEET.md section 7. No author files were edited.

### 38A. A repeatable counterexample to D_T — FAIL

D_T asserts E >= BQ/4 + EXC - O(1), where E=X-4n+2 and EXC counts the non-P/P' windows with d=3. I found a finite replacement in the pure left P collar, in columns 0 through 5 and rows 0 through 15. The replacement changes 12 edges to 12 edges, preserves every vertex degree, has no internal cycle, and preserves **every exterior port pairing**. It can therefore be inserted into a closed Hamiltonian tour without changing the tour's connectivity. In the reference P field its exact changes are

    delta X = 20,   delta BQ = 34,   delta EXC = 18,
    delta(E - BQ/4 - EXC) = 20 - 34/4 - 18 = -13/2.

The complete removed/added edge list is in claim38_gadget.json. The box has 22 exterior-port pairs, including trivial components with both external edges incident to one vertex; the replacement preserves the entire pairing. A solver-free validator checks the edge list, knight moves, degrees, absence of cycles, the actual *external edge* pairings, exact proper crossings, quarter multiplicities, and both P/P' window tests. No SAT lower bound is needed: this is a finite explicit witness.

The gadget does not simply exchange two paths and hope that the tour remains connected. It preserves their exterior connections. Any number of spatially separated copies therefore preserves one Hamiltonian cycle. Copies at a fixed sufficiently large row spacing, for example 40, have disjoint crossing, quarter and window supports. Reflection and transposition give the other side orientations.

Use the audited all-size FOLD family n=96+48k from Claim 12. Its unchanged bulk has pure collars on intervals of length proportional to n; the finitely many construction patches and phase transitions remove only O(1) rows at any fixed collar depth. Thus a positive linear number of these fixed-size replacements fits. For the unmodified family,

    E = 7n/3 + O(1),   BQ = 16n/3 + O(1),   EXC = n + O(1).

The first coefficient is the audited X=19n/3+O(1) construction. For the second, claim38_corridor_bq.py counts 16 bad quarters per (6,6) period in each of the four diagonal corridors. Each has n/12+O(1) periods; the pure/fold bulk has no bad quarters, and the remaining patches and endpoints contribute O(1). The collar arch flips are outside the interior BQ region. The third coefficient is the quarter-side arch-flip count, with fixed-window and patch effects O(1), already used in Claim 36. Consequently the unmodified D_T surplus is O(1), whereas m disjoint gadgets change it by -13m/2. Taking m proportional to n disproves D_T with any uniform additive constant. This conclusion is not an extrapolation from the finite table.

Five complete modified tours were also checked from their stored grid encodings by the independent tour and geometry checks:

| n | Gadget copies | X | E | BQ | EXC | E-BQ/4-EXC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 96 | 2 | 760 | 378 | 690 | 191 | 14.5 |
| 144 | 6 | 1144 | 570 | 1082 | 311 | -11.5 |
| 192 | 12 | 1568 | 802 | 1542 | 467 | -50.5 |
| 240 | 19 | 2012 | 1054 | 2036 | 641 | -96 |
| 288 | 26 | 2456 | 1306 | 2530 | 815 | -141.5 |

These are one-cycle Hamiltonian tours, not only degree-two witnesses. B_T is satisfied on these examples; the counterexample attacks D_T.

Evidence: claim38_gadget.json; claim38_validate_gadget.py; claim38_gadget_validation.json/log; claim38_patched_n96.json through claim38_patched_n288.json; claim38_corridor_bq.py/json. CP-SAT with one worker was used only to discover the local replacement. claim38_gadget.py --replay fixes the saved edge choices and checks the model; its OPTIMAL status concerns this fixed-witness replay, not a claim that the gadget is globally best. The exact validator is the decisive check.

An earlier exploratory search also produced a validated n=96 tour with D_T surplus -88.75 by successive cycle-preserving two-edge switches. That single-size result alone would not defeat O(1), so the proof above uses the pairing-preserving gadget instead. The exploratory files are claim38_switch.py/log and claim38_switched_n96.json.

### 38B. N_re is a different quantity — repair requires a new statement

The gadget preserves all exterior partners. Thus N_re, if defined from these actual collar-port partners relative to P, does not change, while EXC increases by 18 per copy. This gives a direct unbounded separation between exception windows and pairing repairs. Replacing EXC by N_re/2 avoids this specific counterexample; it does not establish the resulting D_T.

If only D_T is changed, B_T still contains EXC and the advertised conclusion E>=n-O(1) no longer follows. One must either prove a geometric inequality involving the same pairing variable, such as an appropriate BQ+2N_re bound, or prove a different common-budget relation. In particular, N_re/2>=EXC-O(1) is false for these insertions.

The witness uses a width-six replacement. Claim 28's price is for a fixed-field strip of width at most four and a specified current class, with finite-interval qualifications. Nothing here contradicts that certificate. A new arbitrary-collar pairing price, or a reduction to its certified strip class, is still needed. Measuring a constant surplus on the unmodified FOLD family cannot establish a universal joint ledger.

### 38C. Clean-return argument — FAIL for the stated implication; GAP for C'

C' is SSR_clean<=EXC+O(1). I did not find a counterexample to this numerical inequality. Its proposed proof is incomplete even after removing returns through bad squares.

First, “the return's interior lies in good squares” must specify what happens at lattice vertices. There is a degree-two local edge configuration containing

    (0,0) -> (2,1) -> (3,3)

in which all four squares traversed by the two open knight segments are good:

    (0,0), (1,0), (2,1), (2,2).

At the turning vertex (2,1), the other two incident squares are bad. Their quarter multiplicities, in B,R,T,L order, in the saved witness are

    square (1,1): (0,0,1,1);   square (2,0): (1,1,2,2).

Thus the path goes through good squares yet makes a gentle (2,1)->(1,2) turn, which is not an allowed transition of G1's free-fold eight-cycle. The point (2,1) itself belongs to the closure of good squares, so requiring containment in that closed union does not remove the issue.

claim38_clean.py constructs the local witness with exact degree two on the point box [-4,7] x [-5,7], degree at most two outside, the two forced moves, and exact goodness of the four traversed squares. A direct recount of its 172 selected edges confirms these assertions. The full edge list is in claim38_clean.json. This is a local counterexample to the claimed implication, not a completed closed-tour counterexample to C'. A repair could require a full good neighbourhood at every interior turning vertex, then prove that this implies the free-fold hypothesis. Such a stronger definition changes SSR_clean and requires a new geometric count in (B).

Second, even when the free-fold hypothesis is separately ensured, G1 proves a *net cycle step* of +1. It explicitly allows cancelling fold pairs and a composite reflection or glide, and explicitly says it does not prove a general arch price. This is not a proof of the fixed P-compatible matching relation required by Claim 28C. That claim assumes fixed chevron interior matchings and changes only to edge pairings. A single clean arc does not establish that its partner arc survives, that its nest has that matching, or that all nests share a disjoint supply of exception slots. A charging proof of SSR_clean<=EXC+O(1) must address these points.

The saved FOLD, FJOG and FIELD diagnostics were also tested for clean SSRs using goodness of every square traversed by their interior edges. Results are in claim38_clean.json/log. These tests do not supply the missing universal implication or matching theorem.

### 38D. Label count and barrier convention

**PASS, conditional on exhaustive stopping:** W+D+I+X_E=4(n-2d)-EXC is the correct starting-label count under the stated slot convention. No labels are initially assigned to exception slots. The revision correctly retains the qualification that all label paths stop in one of the listed classes. This count alone supplies no price for a slot.

**PASS for the local barrier repair; GAP for a global chamber argument.** A slash strip midline y-x=k-1/2 avoids lattice vertices. Within a good square of its split, an intersecting tour edge is the corresponding present chain link. Likewise a transversal passage through a wall edge's midpoint avoids the uncounted wall-vertex passages from Claim 36E. A knight edge crossing that unit edge in its interior would be its carried tile link, which the good wall does not permit. Thus the revised convention removes that particular defect.

The withdrawal of the old half-chamber and attached-wall claims is necessary. A full-triangle count can only be invoked after the two complete boundary paths, their good-strip hypotheses, and the partner's arrival at the side are established. It cannot be applied to the pleat deflector by the midpoint convention alone. In particular, the convention proves neither B_T nor the clean-return version of (B).

### 38E. Scope and Pareto profile

T5 with window EXC is false because D_T is false. B_T remains GAP; C' remains GAP, with the clean-to-free-fold and free-fold-to-P-matching steps unproved. The proposed replacement of EXC by N_re/2 is a new conjecture, not an audited repair. The counterexample does not refute X>=5n-O(1); all modified tours have many more crossings than that.

The decisive finite input is one 6-by-16 pairing-preserving collar replacement, independently checked without a solver. Its unbounded use relies only on the previously audited FOLD construction and a 16-bad-quarter period count. Five full tours are regression evidence. The clean-turn objection uses one small local degree-two witness. There is no large transfer graph and no new lower-bound coefficient. All computations are finished; Claim 38 is complete.


### Claim 38 follow-up: latest SHEET section 8 — 2026-10-03

**Verdict: GAP for (B'), (C*) as an input sufficient for the lower bound, and (D*). No counterexample to these numerical targets was found. PASS for the good-point/free-fold local step and the conditional trap-parity calculation. FAIL for the unrestricted statement that every clean return is a steep-port horizontal chevron.** The section-7 EXC counterexample remains valid for that withdrawn price; it is not a counterexample to section 8's pairing price.

The current file is more specific than the queued summary. Its actual geometric target is

    (B') BQ + 2 RET_clean + 2 N_re' >= 4n-O(1),

where N_re' counts changed ports that are NOT ends of clean returns. This distinction is required for the final addition. I audited this version.

#### 38F. Good-point repair and the missing port hypothesis

Requiring all four squares at each interior chord vertex to be good fixes the gentle-turn objection from the previous audit. The local classification used in 8.1 is correct. At a one-split point, the four possibilities given by T2 are two straight pairs and two free-fold pairs. The wall classification gives the remaining axis-fold pairs. Thus the turns of such a clean chord are free folds. Goodness also rules out proper edge crossings along the interior arc. The previous witness with two bad squares at its turning vertex is excluded by the new definition.

However, RET_clean explicitly allows ANY port type. G1 requires steep ports. The cut x=5/2 can also be crossed by a shallow (1,2) or (1,-2) edge. Good points do not exclude them. A concrete whole-plane perfect field provides the counterexample to the asserted classification:

    w(k)=V for k<=-1, and w(k)=H for k>=0,

in T2's slash ribbon-word construction. Its strand contains

    (2,-2), (3,0), (4,2), (5,4), (3,3), (1,2).

The portion in x>5/2 returns to the same boundary. Every point and square is good. Its entrance is shallow (1,2); its exit is steep (-2,-1). Both ports have slash sign. The turn from (1,2) to (-2,-1) is a valid diagonal free fold. The composite reflection is diagonal, not the asserted horizontal reflection. The two intersections with x=5/2 are (5/2,-1) and (5/2,11/4).

This is a whole-plane perfect-field counterexample to “clean return implies G1's steep-port hypotheses,” not a completed closed-tour counterexample to (C*). claim38_v3_local.py checks the word-field edges, degrees and all quarter multiplicities on a surrounding box. The infinite extension is exactly T2's word formula.

**Repair:** first separate shallow and steep ports. Under the census convention a shallow port is automatically changed, so any return with a shallow end already satisfies the required changed-end alternative. Apply G1 only to the remaining two-steep-port returns, and obtain only its actual net-step and reflection/glide conclusion. The definition of N_re should explicitly classify shallow ports as changed, since P/P' has no reference port of that type. This is a definition choice currently implemented by the script, not supplied by the phrase “its P/P' partner.”

A short odd-shift free-fold candidate was also tested with every interior vertex required good; the local degree-two SAT model was UNSAT. That single failed candidate is not a parity proof and supplies no new claim about 8.5.

#### 38G. Trap parity is conditional; the exceptions are not controlled

The algebra in 8.2 passes. Write P(c)=c-3 for even c and c+3 for odd c. Then

    P(c+s)=P(c)+s                  if s is even,
    P(c+s)=P(c)+s +/- 6            if s is odd.

If two distinct returns have the stated partner endpoints, equal even shift, and unchanged collar partners at both ends, these two chords and their two collar paths form a closed component. A larger single tour cannot contain it as a proper component. This is the fixed-matching trapping result, not a proof that the partner return exists or that the shifts agree.

Section 8.3 explicitly assumes P/P' WINDOWS at the ports and a defect-free region between the two returns, and still depends on the unwritten Lemma F. “Unchanged partner” alone does not imply a P/P' window. Those hypotheses must be established when applying the development argument to an arbitrary return. The good-point condition on the return itself does not establish goodness of the partner or of the enclosed region.

More importantly, the proposed exceptions (i) dirty/nonreturn partner, (ii) a bad square between the returns, and (iii) odd shift are not bounded in number. They are not merely the O(1) geometric board-corner exceptions. Even if the alternatives in 8.3 are made exhaustive, listing them gives no estimate sufficient for the target. A bad cluster can be enclosed by many nested regions, and the same dirty partner or bad-quarter capacity must not be charged repeatedly without a matching/allocation proof.

Here is the exact missing term. Let U_0 be the number of clean returns with zero changed ends, and N_c the number of changed ports incident to clean returns. Distinct interior chords have distinct ports, so

    N_re = N_c + N_re',     N_c >= RET_clean-U_0.

Consequently (B') and (D*) would give only

    E >= n - U_0/2 - O(1).

To conclude E>=n-O(1), prove U_0=O(1), or prove a stronger joint inequality that pays this loss. Merely permitting the cases (i)-(iii) in (C*) does not do so. The BQ/4 term is already fully present in (D*); it cannot be used a second time to pay these cases. Similarly, the Parity Lemma remains a conjecture, as the source itself states. G1's net-step result does not prove even shift or absence of defects inside the return's disk.

**Status:** the conditional trap calculation is PROVEN. The universal changed-end count, or a version with quantitatively paid exceptions, is GAP. No closed-tour counterexample to the strengthened, exception-free count is claimed here.

#### 38H. Independent census of the actual section-8 quantities

claim38_v3_census.py traces each interior chord and each collar path directly, tests goodness of all four squares at every interior vertex, and uses the fixed parity rule for P. It does not infer the rule from whichever cheap windows happen to occur in the test tour. It marks shallow, cross-side, cross-sign and ambiguous corner ports changed, as the author census intends. It traces collar paths to completion rather than imposing a 4n-step cap; the collar contains about 12n vertices, so that cap is not justified for arbitrary tours.

The author's learned `exp` table has another scope issue: if a side/sign/parity class has no sampled cheap ports, a genuinely P-paired port in that class is automatically counted as changed. Hard-code the proved reference matching and handle nonreference port types explicitly. The reference rule can be derived directly from the short P paths; its use should not depend on the test tour's training samples. The independent counts below agree with the published FOLD and FJOG rows.

| Tour | n | BQ | RET_clean | N_re | N_re' | B' left side minus 4n | E-BQ/4-N_re/2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FOLD | 96 | 622 | 138 | 194 | 53 | 620 | 85.5 |
| FOLD | 288 | 1646 | 522 | 578 | 53 | 1644 | 85.5 |
| FOLD with 26 audit gadgets | 288 | 2530 | 288 | 786 | 485 | 2924 | 280.5 |
| FJOG | 130 | 2544 | 0 | 148 | 148 | 2320 | 335 |
| H16a | 96 | 0 | 0 | 362 | 362 | 340 | 306 |

Every tested clean return had one or two changed ends. These are finite tests with substantial geometric slack, not certificates for (B') or (C*) on arbitrary tours or 2-factors.

**Important cut-depth distinction:** Claim 38's collar replacement preserves all port pairings at the boundary of its six-column box. It does NOT preserve all ports or pairings at the depth-three cut now used in section 8. In the displayed 26-gadget tour, N_re at that cut increases by 208, while RET_clean decreases by 234. Thus the earlier EXC counterexample does not refute (D*) at this cut. Do not transfer the “unchanged pairing” statement between these two different port sets. The claim that RET_clean is flip-invariant also needs a specified class of flips: general collar modifications crossing the chosen cut can create bad interior points and destroy clean returns, as this example does.

(B') still needs a global geometric proof. The local midline convention from section 7 repairs the wall-vertex issue, but it does not provide partner paths or bound shared defect regions. (D*) still needs one joint allocation of quarter and pairing charges. Claim 28's certificate has its fixed-field, width-at-most-four, current-class and finite-interval hypotheses; it is not by itself a theorem for every depth-three collar with arbitrary exterior ports.

#### 38I. Closeout for section 8

The clean-point correction is valid. Restrict the chevron classification to the steep-port case, state how nonreference ports enter N_re, replace the learned matching rule and fixed collar-path cutoff, and quantify the U_0 exception term in the shared budget. These repairs are necessary before the revised route can prove 5n. The new numerical targets remain GAP, not refuted by this audit.

**Pareto profile:** one explicit perfect word field disproves the unrestricted local classification; five direct tour scans check the revised quantities. One small rejected odd-shift SAT candidate provides only a diagnostic. No large computation and no new asymptotic crossing coefficient are involved. Evidence: claim38_v3_local.py/json/log and claim38_v3_census.py/json/log. This follow-up completes the latest Claim 38 request.
