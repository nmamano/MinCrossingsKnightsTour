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
