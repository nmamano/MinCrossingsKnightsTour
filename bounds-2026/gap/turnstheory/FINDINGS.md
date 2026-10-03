# Simplified proof assembled: 5n-597 — 2026-10-03

PROOF_5N_V2.md is written (1,655 whitespace-delimited words). It
combines Claim 51's strong-end filtering and scalar quarter count
with Claim 50's cut-state certificate as Section 5. The exact audited
constants give C=28+1104-2=1130 in T>=b-C, hence
X>=5n-(32+C/2)=5n-597 for even n>=32.

The closed-tour theorem is stated first. The separate spanning simple
2-factor theorem is explicitly marked pending Claim 52. Identity K
is omitted because the proof does not use it. The reproduction section
names the author cut checker, independent Claim 50 checker and small
geometry checks. No new certificate run was needed; the constant was
recomputed exactly. PROOF_5N.md and both blog posts are untouched.

---

# S2 addition: connectivity audit, option C and identity K — 2026-10-03

PROOF_5N_SIMPLE.md now includes Sections 7–9. Every hand step in
PROOF_5N.md Sections 1–4 and 6 is mapped to its actual hypothesis:
geometry, degree two, or counting. NONE needs a single tour cycle.
Only the old Section 5 forest certificate needed connectivity.

Read Lower Bounds SIMPLE_STRIP.md 1.2–1.4 and the complete option C
source. Its row-cut model has no cycle rejection or component labels.
The reported 3,136 states / 48,510 arcs and potentials give per-side
error 7, global T+1130>=b, hence the same T+1160 black box. These are
author-certified inputs pending independent audit, not relabelled as
audited here. No new certificate run was made.

Candidate scope: X>=5n-612 for every spanning simple knight 2-factor
on an even n>=32 board, counting crossings BETWEEN different cycles
as well as within cycles. Six exact re-check obligations cover the
cycle-free enumeration restriction removal, finite-board walk mapping,
crossing ownership, predicate geometry, potential interface, and hand
proof hypotheses. The candidate theorem remains pending those checks.

Identity (K) is checked algebraically in Section 9: strip degree and
tile mass equations give X_sigma>=n+3 without connectivity. I include
it as an optional hand explanation of the base rate. It does not pay
strong rows, and its row-local kappa experiments are not proof inputs.
The best proposed outline is the new scalar hand proof plus option C;
PROOF_5N.md and both blog posts remain untouched.

---

# S2: simpler hand proof of 5n, same strip black box — 2026-10-03

Delivered PROOF_5N_SIMPLE.md, best option first. PROOF REORGANIZATION
submitted for audit; no change to PROOF_5N.md or either blog post.
Beyond-5n research remains stopped.

The simplification: discard every candidate with a strong end before
counting quarters. Each survivor is charged and has no two-quarter
strip overlap anywhere on its squares. Two bad quarters are therefore
usable. Count them with one scalar bound |Q|<=4E-2T, proved from
D=sum_q[binom(m(q),2)-m(q)+1]=2E-X1. This removes the h-residue
retention rule, deficient paths, nu atoms, individual allocations,
locality and the good-middle detour. With z discarded paths, z<=b
and T>=b-C give 4E>=2(N-z)+2T>=2N-2C.

Result: the SAME 5n-612 from the audited C=1160 black box. Taking
C=1164 gives 5n-614 and avoids the potential-interface requirement.
The note includes the dependency map, a ladder Pareto table with
measured graph sizes and estimated hand pages, and the exact scalar
contract for Lower Bounds' hand replacement. For strip rate beta in
(0,1], the same argument gives (4+beta)n-(30beta+2+C/2), explicitly
quantifying the coefficient trade. No new finite input or computation.

The new parts for the Verifier are the stronger initial filtering,
its exclusion of all forbidden overlaps, and the scalar inequality.
SIMPLE_STRIP.md was not present at preparation time; no result from
that parallel task is assumed. No POST attempted, per the request.

---

# C5-J L3/L4 proof task: exact pairing and conditional chamber count — 2026-10-03

POST delivery to the Chief Researcher was attempted as requested,
but localhost:4000 failed to connect (curl error 7). This file is the
durable report; c5j_report_message.json contains the unsent message.

Delivered C5J_L3L4.md, with PROOF / ARGUMENT / OPEN labels at each
step. The small standard-Python check check_c5j_width6.py passes;
output is c5j_width6_check.json. No heavy computation or blog edit.

L3: the exact P matching at depth 5.5 is still c->c-3 for even c,
c->c+3 for odd c. Two actual partner returns of equal even shift
close the four-piece cycle. Require it to be a proper component.
For cross chords use f(P_lower(c))=P_upper(f(c)); when f=epsilon*c+s
and the two reference rules agree, this means epsilon=+1/s even OR
epsilon=-1/s odd. P-class ends alone do not prove the partner exists
or that shifts agree. Lemma F needs the full intervening good region.

Key correction to BEYOND5 13.4: width-six P and U have the same PORT
EDGES and straddle count, but DIFFERENT labelled pairings. P joins
(4,r) to (5,r+2), U joins (5,r) to (4,r+2). I derive both with six-cell
paths, matching Lower Bounds B5f. A pairing class must retain this.

L4: for a proper chamber with barrier capacity L+e_beta, coverage of
square column five gives L<=2R_in+c+G5/2+128+e_beta. Here c counts
shallow p56 ports and G5 raw holes; the 128 is a conservative explicit
PER-INTERVAL endpoint allowance. This count avoids an unsupported
translation of the old m12 degree identity. It remains conditional
on constructing the proper chamber and barrier.

The payment gaps are explicit: L4' still double-uses a shallow port
as a return's escape and in c; G5 can overlap flux-selected quarters
and is not automatically free BQx; non-P does not imply Phi>0 without
a zero-set result; a segment cost must cover all returns it serves;
L5 prices untrapping; per-chamber/junction errors need global control.
There is no unconditional L4 proof or beyond-5 claim in this report.

---

# Public crossings demo embedded — 2026-10-03

Replaced the Integrator-demo TODO in writeup/crossings/post.mdx with
DemoEmbed and one plain sentence linking to the same demo. Both embed
attributes and the text link use the exact requested URL:
https://nmamano.github.io/MinCrossingsKnightsTour/bounds-2026/demo/?metric=crossings
The title is "Interactive demo: knight tours with few crossings".
`node writeup/crossings/check_mdx.mjs` PASSED after the change.

---

# Crossings blog updated to audited 5n bound — 2026-10-03

Updated writeup/crossings/post.mdx under the Chief Researcher's relayed
Nil approval. Ready for the Verifier's completeness/faithfulness audit.
No publication, site-source edit, commit or service restart was made.

Sections changed:

* Excerpt, introductory bound, result Callout and leading-coefficient
  ratio: 5n-612, range even n>=32, ratio 19/15 (about 1.27). The existing
  title-option comment's numerical ratio was updated too.
* Part 2: replaced the old balance of two lower bounds with quarter
  payments plus the strip reserve. It includes both lost paths and
  deficient charged paths with visible end overlaps. Existing useful
  tile/corner images remain; the old abnormal-row-only conclusion and
  its strip image were removed from this section.
* The gap, lower-proof Details link and Open questions now use 5n
  against 19n/3. No intermediate results were added.
* Appendix B: full self-contained 5n-612 proof, including 4n-2, the
  exact tile identity, flux, endpoint table/residues, quarter kernel,
  visibility, full-mask certificate and Claim 42 common-state join.
  Finite facts name their check commands from bounds-2026. It states
  the NumPy/OR-Tools requirements, author timings 31/42 seconds and
  independent audit timing 22 seconds. The old Lean stability theorem
  is replaced by the correct scope: the tile bound is in Lean, while
  5n is computer-assisted Python. Appendix A is BYTE-IDENTICAL.

Word counts (whitespace-delimited MDX source tokens, including markup
and code; same rule before and after):

| Scope | Before | After |
| --- | ---: | ---: |
| Body, from opening paragraph to before Appendix heading | 2770 | 2385 |
| Entire appendix, including introduction and A+B | 4664 | 5043 |
| Appendix B only | 2340 | 2719 |
| Part 2 only | 1384 | 1006 |

Exact counts and content hashes: blog_5n_change_counts.json. Original
source snapshot: post_before_5n.mdx. Replacement drafts are
blog_part2_5n.md and blog_appendix_b_5n.md. These files are audit aids,
not additional publication targets.

Checks: `node writeup/crossings/check_mdx.mjs` PASSED with the site's
compiler/options; both details blocks are complete and collapsed.
Search of post.mdx found no 14n/3, 14/3, 4.67n, 19/14 or 1.36 remnants.
Referenced Python command paths exist. No new em dash was added.

PREVIEW CHECK NOT COMPLETED: curl to
http://127.0.0.1:21019/blog/knights-tour-crossings returned curl error 7,
HTTP 000, on two attempts (connection failed immediately). This
sandbox also refuses the netlink socket used by ss, so I cannot tell
whether the service is down or inaccessible here. No HTTP 200 claim
is made. Verifier/Integrator must check the live preview from a
network-enabled session. The progression chart remains the Integrator's
assigned update; this edit changes no image asset.

---

# Reply to Edge Searcher: beyond-5 pure currency definitions — 2026-10-03

Read gap/searcher/BEYOND5_FLUX.md. Answers (a)–(d), plus a new cheap
stop test, follow. The proposed algebra is correct, but the cited
193-tour evidence uses a DIFFERENT pair exclusion.

**(a) Restoration: YES.** With s=|S*|, T=s-4n+2 and retained candidates
as in PROOF_5N.md, T+1160>=D_loss is audited. T is the pure strip
surplus, not a mixed currency. Indeed Claim 42 proves the stronger
T+1139>=D_loss+L_def. E=T+X_out holds exactly for X_out=X-s.
For 0<=p<=1, F-beyond(p) would imply explicitly

    X >= (4+2p)n-(60p+C+1162),

because E>=D_loss+pL-C-1160>=pN-C-1160. The 1-p coefficient of
D_loss must be nonnegative; retain the p<=1 restriction.

**(b) Hall data: B, not S*.** The pure experiment used unit crossing
pairs outside B, the UNION of outermost-column pair sets. Source:
HALL_CURRENCY_RESULTS.md and compare_hall_currencies.py, which calls
geometry(..., pair_exclusion='B'). B is a subset of S*. Thus

    X-|B| = X_out + |S* minus B|.

Keep S* in F-beyond if you want the displayed restoration algebra.
The 193 zero deficits outside B do NOT test that statement. Please
correct that evidence sentence and its source link (the comparison
report, not the original mixed HALL_V3_RESULTS.md). Replacing S* by B
requires a new restoration/budget proof; the extra S* minus B pairs
are already part of T and cannot be counted twice.

**(c) Aggregate is enough.** A universal scalar X_out>=pL-C with ONE
absolute C suffices for the coefficient. Radius ten and individual
payments are optional stronger tools, not obligations of this global
reduction. A local model still needs a global no-double-counting
argument and one error, not one error per carrier, run or patch.

**(d) No audited asymptotic counterexample identified here, but the
saved closed tours give a serious stop test.** Claims 29 and 35 concern
open patches/plane walls; neither establishes an unbounded deficit
on retained candidates in closed tours. However, a new read-only
scan of the 193 saved validated-tour counts gives:

| Family | n | L | X_out (outside S*) | L/2-X_out | 2L/3-X_out |
| --- | ---: | ---: | ---: | ---: | ---: |
| LF5 | 156 | 181 | 56 | 34.5 | 194/3 |
| LF5 | 208 | 256 | 73 | 55 | 293/3 |
| LF5 | 260 | 332 | 91 | 75 | 391/3 |
| TT16 | 96 | 65 | 3 | 29.5 | 121/3 |

These are aggregate deficits, with no radius restriction. The LF5
values increase on the saved sequence even at p=1/2. Finite data
cannot disprove the existence of an absolute C; do not label this
an asymptotic refutation. Before carrier computation, derive the
LF5 or TT16 family counts for unbounded n, or generate larger members
and then prove their count formula. The statement may be stronger
than the beyond-5 result needs because it discards strip surplus.

A less restrictive sufficient alternative keeps that surplus:
let R=T+1160-D_loss>=0 and seek

    X_out+R >= pL-C.

This yields exactly the same bound in (a). It is a scalar joint
strip/interior target; it permits high-strip-cost tours to use that
cost instead of forcing all retained paths into X_out. Use the same
R once, with no second claim on those strip pairs. This is a proposed
contract, not a proved beyond-5 inequality.

Reproduction (light, saved counts only):

    python3 gap/turnstheory/check_pure_aggregate.py

Output: pure_aggregate_check.json. This does not rerun tour validation
or geometry; it uses the stored validated snapshot hall_v3_results.json.
No new flow or heavy computation was run. Proof profile: the reduction
is two identities and one inequality; the missing global price is the
substantive theorem. The local wall certificates alone do not prove it.

---

# Reproduction dependencies and author timings added — 2026-10-03

PROOF_5N.md now states the exact third-party imports for f1v_stab.py:
NumPy and OR-Tools. OR-Tools is a transitive geometry-helper import,
even though the certificate does not run a SAT solver. Commands use
the research venv. The document records the Integrator-reported
31-second UP and 42-second DOWN times separately from the Verifier's
22-second independent check. No theorem or certificate changed.

---

# Headline proof aligned with audited Claim 42 — 2026-10-03

PROOF_5N.md is now AUDITED (Claims 39, 40 plus scalar addendum, 42):
X>=5n-612 for every even n>=32, without a small-radius allowance.
Section 5 uses the independent common-mask state graph and the
checked interface -4<=h_up-h_down<=4. Each full side has error 37/4;
four sides and the corner correction give G<=T+1139<=T+1160.
The exact ledger therefore uses E+580 and yields constant 612.
The DOWN range remains correctly stated as [-33,0].

The document includes both independent audit commands, author
comparison commands, certificate sizes and the Verifier's measured
22-second rebuild/check time. Its Pareto profile is approximately six
short hand pages plus one narrow-strip certificate. No certificate
rerun was needed for this alignment. Earlier 614 statements below
refer only to the weaker separate-half calculation and are superseded
for the headline proof. No price lemma remains open for this bound.

---

# Direct DOWN certificate changes the constant to 614 — 2026-10-03

Lower Bounds now reports UP potential [-29,0] and direct DOWN
potential [-33,0]. DOWN carries previous-row VIS as one bit, because
the test at row r uses square row r-1. I checked the updated source
and report; independent certification remains with Claim 42.

PROOF_5N.md now uses total half error 62, T+1164>=G_strong and the
exact ledger E+582=nu+(T+1164)/2. The resulting conditional theorem
is X>=5n-614 for even n>=128. No 42-unit corner allowance is needed.
Both orientation commands and potential filenames are updated.
Earlier 612 statements below are superseded for the VIS route;
the older scalar F1 reduction with constant 612+C remains valid.

---

# Consolidated five-n proof ready for Claim 42 — 2026-10-03

PROOF_5N.md now gives the full conditional proof of X>=5n-612 for
even n>=128: exact tile identity, flux and endpoint definitions,
Claim 39 quarter packing, visibility lemma, strong strip certificate,
1104 corner correction and final algebra. It lists reproduction
commands and a Pareto profile. The new finite potential and its down
orientation/half-scan mapping remain PENDING independent audit.

The H1/deficiency match is already recorded in REQUESTS.md and is
restated in the proof: s_i<=1 on the whole path, good middle at depth
>=4 (indeed >=3). The visibility argument works for every candidate
radius r>=12, so no 42-unit corner allowance is needed. No new heavy
computation was run to prepare this consolidated proof.

---

# VIS hand reduction checked; conditional 5n-612 — 2026-10-03

**To Lower Bounds and Chief Researcher:** H1 and the deficient
condition match Claim V exactly. The hand implication passes. There
is a shorter proof, now in PROOF_5N_PLAN.md Section 10: a charged path
has a bad square; two bad quarters and at most one payable quarter
force an unpaid pair. Its overlap is in S* minus B, and strip depth
forces it into an endpoint row. Thus every deficient retained path
has VIS, without any passing-test assumption or height argument.

The same geometry works for ALL candidate radii r>=12: the fixed
coordinate r keeps other sides away. No r<=32 omission is required.
Distinct side rows pay lost and deficient retained candidates, so
T+1160>=D_loss+L_def gives X>=5n-612 for even n>=128, CONDITIONAL on
the new finite certificate. Fully paid paths use the quarter rule;
the reserve pays all deficient paths in full. No residual atom model,
marks or Hall bits remain in this global proof.

**Audit still needed:** Lower Bounds reports the up certificate at
rate one and potential width 29. I read its source, not independently
rebuilt it. Check VIS pending-edge geometry, arc inequalities, down
reflection and half-boundary accounting. Square row r reflects to
-r-1, so reflecting only the test table is insufficient. Section 10
states the exact contract and reproduction command. No theorem is
marked audited yet. Proof size is one short geometric implication,
one row injection and the ledger, plus one strengthened width-two
finite potential.

---

# F1 scalar simplification accepted; side price still open — 2026-10-03

**HAND REDUCTION, pending audit:** Lower Bounds' proposal is correct
for the global 5n target. PROOF_5N_PLAN.md Section 9 gives the exact
row injection and algebra. The audited JOINT-test potential bounds
all failed rows: T+1131>=b, hence T+1160>=b. Distinct failed rows pay
lost candidates AND retained failed-end paths. The remaining scalar
obligation is nu'(total)+(T+1160-b)/2 >= sum_both-pass d_i-C.
It implies X>=5n-(612+C). No Hall bits are needed for this weaker
global target; the private L2/F1 statement remains open.

R4 is updated at the top of REQUESTS.md. First try pure strip price
F1-T with one extra count per marked passing charged end row. This
avoids all baseline marks. If it fails, use residual currency; omit
baseline marks on failed-end paths, which the reserve already pays.
A1 does not propagate mismatch through a dirty interior boundary.
Lower Bounds' proposed deep-defect check tests the actual remaining
risk; periodic clean-strip evidence does not settle it.

**Audit status read and applied:** Claims 39–40 pass the hand kernel,
seven-pair end list and the conditional certificate logic. The flux
wording now says zero modulo three. R4 records Claim 40's false-halo-
hole repair and subtraction of invisible overlap-quarter consumption.
No new lower-bound coefficient is claimed. No new computation was
needed: this reduction uses the existing joint potential and one
short ledger calculation. The next required result is a universal
F1-T or F1-scalar certificate with one total error.

---

# R4 posted; unpaid end zone reduced to four squares — 2026-10-03

**R4 is ACTIVE at the top of REQUESTS.md for KT Lower Bounds.** It
specifies the actual residual F1 demands and nu capacities, baseline
marks, endpoint pairing, a safe eight-column model, complete-square
requirements, state domains, scale, and potential constants. Start
with local end-type enumeration and table feasibility; no large scan
was launched here. Claim 39's audit can amend the hand-kernel premises.

**New hand classification (awaiting audit):** END_TYPES.md lists all
seven anchored S-minus-B two-quarter crossing pairs, four geometric
shapes up to translation/reflection. There are no unpaid quarters at
depth >=3. Residual paths therefore have only TWO potentially bad
squares per end, not three. At depth two the only unpaid quarter is L.
A deficient path can have a bad depth-two square at only one end, and
then has one payable quarter and only 1/4 residual demand. Zero-payable
active ends have only three multiplicity vectors. Exact edge witnesses
and the local flux formula are written in END_TYPES.md.

The small enumeration `python3 gap/turnstheory/classify_unpaid_ends.py`
found seven records; output is `unpaid_end_types.json`. It uses exact
tiles and no solver. The bounded support argument proves the search
box covers every possible pair. These geometric types are not yet
claims of degree-two or closed-tour completion.

**Certificate correction:** a total-demand side potential would only
prove aggregate capacity. R4 instead requires the potential to cover
all Hall subsets of marked target rows. An atom contributes once when
its eligible row interval meets the subset. This enforces individual
payments with ONE bounded total deficit, as Claim 29 requires. The
recent-selection history is finite, but may be costly; first shrink
local types. Pending edges, baseline marks, and subset history must
continue across cuts. Complete-square tests prevent ghost holes from
being credited. Exact half-walk widths give explicit global constants.

Pareto profile: the new hand step is a seven-pair geometric table and
its short multiplicity/flux consequences. R4 is a detailed sufficient
certificate specification, not a finished finite-state proof. The
universal side price, baseline-choice reduction, and state completeness
remain open. Both routes' shared quarter ledger is unchanged.

---

# Shared D*: bulk allocation matches, side identification does not yet — 2026-10-03

Section 7 is now in the existing `PROOF_5N_PLAN.md`.
**HAND IMPLICATION:** Structures' interior BQ quarters are all payable
by the quarter-packing lemma, so nu>=BQ/4 and
`E=nu+T/2>=BQ/4+T/2`. Thus `T>=N_re-O(1)` would imply D*.
However, that is not the proved L3 statement, which concerns D_loss.

A light exact count on the five audited FOLD tours gives T=159,207,
255,303,351 for n=96,144,192,240,288. Against Structures' reported
N_re=194,290,386,482,578, the deficits T-N_re are -35,-83,-131,-179,
-227. The observed formulas are T=n+63 and N_re=2n+2. This strongly
warns against a side-only identification; an infinite-family count
is still needed to turn the observed growth into an O(1) disproof.

The correct shared identity keeps residual bulk capacity:
`M_bulk=nu-BQ/4>=0` and `E=BQ/4+(T+2*M_bulk)/2`.
D* needs `T+2*M_bulk>=N_re-O(1)`, not necessarily T>=N_re-O(1).
The five samples have M_bulk=103,127,151,175,199 and
`T+2*M_bulk-N_re=171`, which exactly reproduces the 85.5 margin.
Thus both routes can share the quarter allocation and its residual;
D* still needs a changed-port price in that combined capacity.

No double use: D_loss restoration and N_re repair cannot both spend
T independently, and BQ payments and flux-path payments use the same
quarter allocation. The new evidence is five O(n)-strip crossing
counts after reading each saved grid; it does not re-audit Structures'
port census. Command: `python3 gap/turnstheory/check_shared_dstar.py`.
Full counts and paths are in `shared_dstar_check.json`. No heavy job ran.

---

# Five-n plan: interior half-price has a direct hand proof — 2026-10-03

**NEW HAND ARGUMENT, submitted for independent review; no 5n theorem.**
`PROOF_5N_PLAN.md` gives the lemma chain, finite-state requirements,
and the first hand step. The main simplification is an exact
quarter-payment rule in nu_(1/2), which removes interior sharing from
the open part of the proof.

Every bad quarter can receive 1/4 privately except one precise type:
multiplicity exactly two, whose unique covering pair is in S* and has
a two-quarter overlap. Holes use their G atoms; multiplicity >=3 uses
one W3 unit; a non-S* pair pays at most two quarters from its half-unit
capacity; a one-quarter S* crossing pays its only quarter from X1.
Thus ANY set of distinct payable quarters can be funded simultaneously.
The paying supports lie within distance 3/2 of the square centre, so
they obey the strict radius-ten rule (in fact radius two suffices).

A bad middle square has at least two bad quarters by the alternating
multiplicity identity, and both are payable because S* overlaps cannot
reach that depth. Vertex-disjoint candidate paths use distinct squares.
This proves the private half-price and all subset Hall inequalities
for paths with a bad middle square, without an injection from holes to
crossings and without a global fold-stack description.

After paying min(2,s_i) payable quarters per path, the exact remaining
demand is (2-min(2,s_i))/4. Any path with positive demand has a completely
good middle. Apart from at most 84 fixed small-radius candidates,
its bad squares lie in its two three-square end zones. Retention also
excludes B overlaps, so the unpaid overlaps are in S* minus B.

**Single remaining new price lemma F1:** pay those residual end demands
from the SAME residual nu capacity, with one total constant error.
The plan specifies eight side columns, degree/halo rules, endpoint
types, baseline-consumption marks, finite state domains, the two-end
domination table, and a bounded-range potential target. Baseline-mark
realizability and state gluing are still open; no completed finite
reduction is asserted. Start with hand analysis / local end-type
enumeration before any large transfer graph. A failing relaxation
would reject that certificate class, not the closed-tour theorem.

If F1 has total error C_side, the already proved endpoint reserve gives
`X>=5n-(612+C_side)`. This route needs no SHEET connectivity count.
W1/W3 and Claims 33/35 are used with their audited scope as support,
pruning, and stop-test inputs; the direct quarter-payment proof itself
needs only the audited tile and square identities.

Checks: `python3 gap/turnstheory/check_quarter_payment_support.py` passes
all four move types and 16 covered quarters, with exact maximum endpoint
distance 3/2. No SAT search or large state graph was run. The earlier
193-tour zero-deficit screen at mixed p=1/2 remains evidence for full
L2, not yet for the more restrictive baseline-plus-F1 certificate.

Pareto profile: the hand kernel (Sections 2–3) has 100 lines and
832 words. The full plan has 270 lines and 2,159 words, including
certificate specifications and scope limits. Only the side price
remains new finite work.
The detailed plan distinguishes inherited finite inputs, optional
W1/W3 pruning, and the missing side certificate. Next: audit the hand
packing lemma and classify the residual end types for F1.

---

# Claim 35 read; closed-wall Hall test queued — 2026-10-03

**AUDITED wall rate, L2-v3 still OPEN.** The Verifier proves the achieved
half-price wall with an explicit acyclic full-plane zigzag extension.
This is stronger than the finite-cylinder source evidence I previously
reviewed. The audit also checks charged gamma_R shapes at radii 12..80;
the missing steps are actual board-side retention and the cost of
Hamiltonian completion inside the full eligible collars. The wall's
edges preserve x+y modulo three, so completion needs extra structure.
PLAN.md and WALL_1_2_SCOPE.md now reflect the completed audit.

The next incoming Integrator wall tour will receive the existing exact
R=10 pure non-B Hall test, primarily at p=2/3, with p=1/2 as comparison.
Report actual retained paths, Delta, and the min-cut. A single positive
deficit is decisive for that tour and proposed constant, but does not
refute an unknown uniform C_flux; that requires unbounded deficits in
a completed-tour family. No new tour path was included in this message.
No new search or background polling was started.

Finite-input profile: the achieved wall rate now needs 19 edge orbits,
four row checks, a three-path quotient, and the explicit exterior word,
not the large minimum-mean graph. The pending tour test uses only the
existing validation, support, and exact max-flow checks.

---

# Skeleton v4: half-price flux; wall scope checked — 2026-10-03

**Decision:** use mixed p=lambda=1/2 for the flux route to 5n. Seek
connectivity credit for any coefficient above five in this skeleton.
The new top section of PLAN.md supersedes the p=2/3 recommendation.
No new lower-bound theorem is claimed; Claim 31 remains the audited
24n/5 result.

**The (1,2) wall does not yet refute closed-tour L2-v3.** I read the
witness and extension code and reproduced two crossings per four rows,
modeled degree two, and no cycle in the finite unroll. The extension
is a skew cylinder with soft outer degrees and permits cycles. It
provides neither a square Hamiltonian tour nor the actual retained
corner endpoints. One wall intersection does not determine total path
flux, retention, or all resources in the path's full radius-ten collar.
See WALL_1_2_SCOPE.md. Claim 35 is pending in the supplied material.

To turn this wall into a formal fixed-radius counterexample, construct
closed tours with retained subsets J of unbounded size and prove that
their ENTIRE eligible capacity is at most |J|/2+O(1). Then the p=2/3
Hall deficit is at least |J|/6-O(1). The current wall files do not supply
that completion and capacity argument. They do block the proposed
universal open-wall price above 1/2, so that is no longer an input to
the main route. This is not a ceiling on all closed-tour methods.

V4 keeps the proved endpoint reserve:
`E+580 = nu_(1/2)(total) + (T+1160)/2`.
Individual half-price flux with total deficit C_flux would give
`X>=5n-(612+C_flux)`. A JOINT unused-capacity allocation of
`kappa*n-C_conn` for connectivity would give
`X>=(5+kappa)n-(612+C_flux+C_conn)`.
**Reaching 6n now requires n-O(1) connectivity credit, not 2n/3.**
Flux and connectivity must obey one capacity constraint. The global
ribbon-word shortcut remains excluded by Claim 30.

The exact Delta(H) results are included in v4: all 193 distinct saved
tours pass mixed p=1/2; seven fail zero-error mixed p=2/3, up to 25/2
on LF5 n=260; every tour passes pure non-B at both prices. These finite
results do not prove uniform bounded deficit or unbounded growth.
The per-tour tables and the independently checked worst cut remain in
the earlier report and data files.

Size and checks: v4 has 153 lines / 1,078 words; the wall scope note has
90 lines / 703 words. The update uses the inherited ledger/restoration
inputs, the sixteen local hole certificates, and the existing Hall
screens; universal flux and connectivity inputs remain missing. The
only new run was the light witness check:

```sh
python3 gap/searcher/wall/verify_witness.py
```

Its output is saved as `wall_1_2_check.log`. I did not rerun the large
wall graph or the cylinder solver. The next proof task is a universal
half-price allocation including the side/end zones; above 5n, it must
be accompanied by connectivity obligations priced in the same ledger.

---

# Currency comparison: use pure non-B for 2/3; retain mixed 1/2 — 2026-10-03

**MEASURED exact result:** all 193 distinct completed tours (345 saved
records, n=32..260) have Delta=0 in PURE NON-B CROSSINGS at p=2/3 and
p=1/2, with the same strict radius ten and actual retained family.
The mixed nu_(2/3) test has the seven deficits previously reported;
its maximum is 25/2. The mixed nu_(1/2) test has zero deficit throughout.
The per-tour, per-n comparison is `HALL_CURRENCY_RESULTS.md`, with all
source aliases in `hall_currency_results.tsv` and exact data in
`hall_currency_results.json`.

| Family / n | Mixed 2/3 | Pure non-B 2/3 | Mixed 1/2 | Pure non-B 1/2 |
| --- | ---: | ---: | ---: | ---: |
| FOLD24, all 36 sizes 96..166 | 0 | 0 | 0 | 0 |
| H16a, all 44 distinct boards | 0 | 0 | 0 | 0 |
| TT16, all 13 boards | 0 | 0 | 0 | 0 |
| Forced FIELD, 166 | 0 | 0 | 0 | 0 |
| LF1/LF2/LF3, 120 (each) | 1/3 | 0 | 0 | 0 |
| LF4, 144 | 7/3 | 0 | 0 | 0 |
| LF5, 104 | 0 | 0 | 0 | 0 |
| LF5, 156 | 10/3 | 0 | 0 | 0 |
| LF5, 208 | 8 | 0 | 0 | 0 |
| LF5, 260 | 25/2 | 0 | 0 | 0 |

All remaining boards, including the eight smaller LF4 boards, pass all
four columns. Thus no deficit growth is seen in pure non-B currency
on this data. The saved worst pure representative is LF5 n=260, tied
with every other tour at zero; both pure Hall cuts J are empty.

## The old worst cut explains the budget issue

The old mixed Hall set on LF5 n=260 is unchanged:
`J={(1,0,r):15<=r<=126, r mod 6 !=2}`, with 94 retained paths.
Its pure radius-ten neighbourhood contains 109 crossing pairs outside
B: 21 outside S* and 88 in S* minus B. Pure capacity 109 exceeds demand
188/3 by 139/3. Its mixed capacity was only 301/6, with deficit 25/2.
The exact neighbouring pairs are saved in `hall_currency_old_cut.json`.

Therefore the success is not just a change of weight on the same
resources. It also admits 88 side-strip pairs previously excluded by
S*. The existing endpoint-restoration reserve can need those pairs.
A pure L2 proof and the old L3 proof cannot spend them independently.

## Recommendation and precise remaining gap

**Use pure non-B crossings for p=2/3. Keep mixed p=lambda=1/2 as the
simpler Pareto route to 5n.** PLAN.md now states the pure L2 contract
and a sufficient JOINT L2/L3 allocation after reserving a baseline
B0 subset B of size 4n-24. Its single capacity inequality covers kept
paths and lost endpoints. This joint allocation is OPEN; the present
flows test kept paths only. The exact identity E=(X-|B|)+(|B|-4n+2)
and |B|>=4n-24 give E>=X-|B|-22, but do not pay lost endpoints for free.

Searcher Section 7 gives supporting local evidence: at the stated
width-four diagonal wall, pure crossings cost 2/3 per level while the
half-mixed currency costs exactly 1/2. Those are certified fixed-width
wall results, not a proof for arbitrary walls or tours. The global
allocation and side/end-zone obligations remain. No new lower-bound
coefficient is claimed from these tests.

## Checks, size, and reproduction

The 55-line comparison driver uses the checked integer flow and strict
support routines. It recomputes and validates every tour's geometry,
checks its board hash against the original test, and uses unit crossing
capacity outside the UNION B of all four outer-column pair sets. It
runs exact flows at both prices. The original mixed values are reused
from the saved exact run on these identical boards; their equality is
checked rather than silently replacing the old data.

The 43-line comparison checker verifies complete inventory coverage,
all pure demands met, and the unchanged mixed results. It independently
classifies the old worst set's 109 eligible pairs into the 21+88 split.
The B union counts match all three Claim 29 records (519, 534, 944).
The shared flow and support self-tests passed again. New finite work:
193 validations and 386 pure flows, about 182 seconds, one process,
no solver threads. This is screening evidence rather than proof size
for a universal theorem.

Commands from the research root:

```sh
python3 gap/turnstheory/compare_hall_currencies.py > gap/turnstheory/hall_currency_run.log 2>&1
python3 gap/turnstheory/check_currency_comparison.py
```

`hall_currency_check.log` records the checks. The original mixed run
and separate worst-cut geometry audit remain in their earlier files.
The next mathematical action is the joint side budget for pure p=2/3,
or a universal mixed p=1/2 allocation for the simpler 5n route. No
further computation was launched.

---

# Exact Hall screening: p=1/2 passes; p=2/3 deficits grow in LF5 — 2026-10-03

**MEASURED, exact finite tests; no universal theorem.** I tested all 345
saved JSON tour records found in the research tree: 193 distinct closed
Hamiltonian tours, n=32 through 260. Every tour passed degree,
reciprocity, connectivity, and proper-crossing validation. At R=10 and
lambda=p, **p=1/2 has Delta(H)=0 on all 193 tours.** At p=2/3, 186 tours
have zero deficit and seven have positive deficit. The full per-tour
and per-n table is `HALL_V3_RESULTS.md`; every saved filename, including
duplicate copies, is in `hall_v3_results.tsv`.

## Positive deficits and observed growth

| Tour | n | Retained paths | Delta at p=2/3 | Delta at p=1/2 |
| --- | ---: | ---: | ---: | ---: |
| LF1 | 120 | 165 | 1/3 | 0 |
| LF2 | 120 | 119 | 1/3 | 0 |
| LF3 | 120 | 132 | 1/3 | 0 |
| LF4 | 144 | 180 | 7/3 | 0 |
| LF5 | 156 | 181 | 10/3 | 0 |
| LF5 | 208 | 256 | 8 | 0 |
| LF5 | 260 | 332 | 25/2 | 0 |

LF5 at n=104 has Delta=0. Thus its measured sequence is
`(104,0), (156,10/3), (208,8), (260,25/2)`: the deficit grows with n on
these saved tours. This is a warning for the fixed-radius p=2/3
conjecture, not yet a proof of unbounded deficit. A proof needs a growing
family and its resource count. The current v3 constant must be at least
25/2. The three n=120 examples lie below v3's n>=128 range; the larger
LF4/LF5 examples do not. No growth occurs for p=1/2 in this data.

Required-family coverage: all 36 primary FOLD24 tours n=96,98,...,166,
all 44 distinct H16a tours n=48..142, all 13 TT16 tours n=48..96, and the
forced period-four FIELD tour at n=166 have zero deficit at both prices.
All nine LF4 tours were tested: n=96,98,...,110 pass both prices;
n=144 is in the table above. The three Claim 29 tours are included, and
their X,E,G,X1,W3 and retained-path counts agree exactly with the
Verifier's saved records. There are 39 tested distinct tours with
n>=128. Additional families and old audit copies were also included.

## Worst Hall cut, independently checked

For `w-integrator/tours/LF5_n260.json`, the p=2/3 maximum flow has
scaled value 1253 against total demand 1328 (units 1/6). Its source-side
Hall set is entirely at the bottom-right corner:

```
J = {(fx,fy,r)=(1,0,r): 15<=r<=126 and r mod 6 != 2}.
|J| = 94.
```

Use x rightwards and y upwards, as in the audited endpoint convention.
The STRICT radius-ten neighbourhood of J contains 21 outside-S* pair
atoms and 217 hole atoms, and no X1 or W3 atoms. Its capacity is
`21*(2/3)+217*(1/6)=301/6`. Demand is `94*(2/3)=376/6`. Hence

```
Delta(H) = (376-301)/6 = 25/2.
```

The flow attains the complementary upper bound, so this is the exact
maximum Hall deficit, not just the deficit of one selected subset.
`hall_v3_worst_2_3.json` contains J and every neighbouring atom with its
geometry and capacity. A separate checker rebuilt tiles by rational
polygon clipping and tested support using explicit dual-vertex sets;
it reproduced the cut, all endpoint retention tests, the 21 pairs,
and the 217 holes. It does not import the main flow or support code.
Its output is `hall_v3_cut_check.log`.

At p=1/2 all tours tie for worst deficit zero. The saved representative
is also LF5 n=260; its full scaled flow is 664/664 (units 1/4). The
residual source-side Hall set is empty, so there is no obstructing J.
See `hall_v3_worst_1_2.json`.

## Exact test, finite inputs, and reproduction

The test uses the whole-tour S* union, actual retained paths, full-tour
quarter multiplicities, and the v3 rule: every point of an atom's
support must lie within distance ten of ONE dual vertex. Pair support
is its four endpoints; hole/W3 support is its closed quarter triangle.
This is not the Verifier's generous bounding-box-intersection test.
W3 units with identical support are aggregated with their exact total
capacity. The mixed identities are checked before every flow.

At p=2/3, capacities are multiplied by six: demand four, pair capacity
four, excess-atom capacity one. At p=1/2, capacities are multiplied by
four: demand two, pair capacity two, excess-atom capacity one. Thus
lambda=p in BOTH experiments; the p=1/2 experiment uses its own mixed
ledger. All arithmetic is integer or exact rational arithmetic.

Finite evidence: 193 geometry validations and 386 integer max-flows.
The 228-line main checker also passes 300 small random graphs checked
against exhaustive Hall-subset enumeration and 2,000 strict-support
checks against direct path-vertex enumeration. Every computed flow
checks capacity, conservation, and equality with its residual Hall cut.
The second worst-cut checker and the inventory summary are separate
small scripts; no SAT or large strip graph is an input. The main run
took about 210 seconds in one process. No solver threads were used.

Commands from the research root:

```sh
python3 gap/turnstheory/check_hall_v3.py > gap/turnstheory/hall_v3_run.log 2>&1
python3 gap/turnstheory/summarize_hall_v3.py
python3 gap/turnstheory/verify_hall_v3_cut.py
```

`hall_inventory.json` fixes the 345 input paths. `hall_v3_results.json`
records board hashes, source aliases, exact deficits, and cut data.
The summary checks complete inventory coverage and the three Claim 29
records. The test includes the 36 assembled FOLD24 tours; corner
`template` files are construction data, not additional completed tours.

**Next mathematical action:** count the displayed LF5 Hall set along
an arbitrary-size LF5 family before treating the growing deficit as a
disproof. In parallel, retain p=1/2 as the simpler 5n target: every saved
tour meets its individual demands, but a universal allocation and the
end-zone lemma remain unproved. No further computation was launched.

---

# Skeleton v3: Claim 29 quantifiers fixed; Claim 31 audited — 2026-10-03

**L2 remains CONJECTURE / GAP.** The new top section of PLAN.md gives
L2-v3(2/3,10): individual retained-path demands, strict radius-ten atom
support, mixed capacity, and ONE absolute total deficit. The statement
quantifies the constant before all board sizes and tours. It permits
no allowance per path, run, or open patch. Claim 29's forest, near-side,
and radius-zero stop tests are stated with their exact limits.

The exact next finite test is max-flow on each completed tour, with
capacities scaled by six: demand four per retained path, capacity four
per outside-S* pair atom, capacity one per excess atom. Its min-cut
returns the exact Hall deficit over ALL path subsets. This differs
from the earlier aggregate-payment formula and generous non-B tests.

Important limit: this finite flow decides one tour, not the all-size
conjecture. A universal finite certificate still requires a specified
interface-state scheme and a proof that its local payments and boundary
potentials join correctly. W3 supplies support but not that proof.
Claim 30's one-bit-per-run correction is included; no global ribbon
word is assumed. Interior sharing and end-zone/L3 joint pricing remain
open. The proposed next computation is the strict mixed-capacity test
on the three saved completed tours; no large computation was launched.

Proof size: the v3 statement, reductions, and test specification have
169 lines and 1,325 words. They add no new finite proof input. W3's
sixteen local hole certificates and the audited ledger/L3 remain inputs;
the universal allocation certificate is still missing.

**Claim 31 PASS:** I read the independent audit and marked PROOF_R3.md
AUDITED. The final strip theorem is 5X>=24n-13012 for even n>=32.
No result index or post was changed.

---

# W3 support incorporated; end-zone price separated — 2026-10-03

**ARGUMENT, no new coefficient.** PLAN.md now gives a conservative
L-infinity support radius TEN for a non-S* crossing near an interior
bad square, from the 7 by 7 and side-anchored 12 by 9 hole certificates.
I read their generators and check logs and independently ran all four
depth-6 DRUP checks; all passed. Fixed corner boxes handle interference
from a second side. The current support discussion uses n>=128 and
fixed size 32 corner boxes; no new theorem size range is claimed.

The remaining L2 tasks are explicit: a capacity allocation controlling
shared crossing witnesses, and a separate side lemma for paths whose
charge lies in depth-at-most-three end zones. L3 pays lost candidates;
it does not also pay these retained end zones without a joint budget.
The mixed-ledger contract is preserved. PLAN.md states a Hall-type
condition for arbitrary subsets of retained radii, not only runs.

Proof size: the new PLAN.md section has 139 lines and 1,100 words,
including the geometric derivation, open contracts, and check commands. Finite inputs are four interior and twelve
side CNF/DRUP proofs, plus the inherited tile/flux input. No large
computation or new SAT search was run. The 2/3 price remains open.

---

# L2/L3 corner contract corrected — 2026-10-03

**No new bound.** The top of PLAN.md now incorporates W1 and W3.
I checked the W3 witness directly: 57 crossings, zero outside S*,
forest, core degree two, and four flux residues [2,2,2,2]. L3 accounting
survives, but a local L2 price cannot rely on charge alone to obtain
outside-strip pairs. The revised choices are mixed atoms inside the
strips, a joint endpoint/flux allocation, or fixed-size corner excision
with a separate proof for the remaining side endpoints.

Two scope limits matter. W3 uses radii 3–6 and does not impose the full
audited retention test; it is not a global asymptotic counterexample.
W1 classifies crossing-free 3 by 3 centres, not all zero-excess-density
regions, and does not force one fold family throughout a large region.
The phase library must include fold stacks and zigzags. The standalone
DRUP check also passed: 2,942 RUP additions and the empty clause.
PLAN.md names the exact finite inputs and the small reproduction checks.

---

# Pareto assessment of R3 — 2026-10-03

**ARGUMENT submitted for audit; coefficient 24/5 = 4.8.** The proof
is shorter in structure than N1 because it removes the interval lemma
and blocked-run accounting. Its finite input is large, so this is not
a small-check proof of 4.8n.

Proof size measured today: `PROOF_R3.md` has 208 lines and 1,303 words.
It also requires Sections 1–3 of `PROOF_N1.md`: 195 lines and 1,194
words for the inherited tile, mod-three flux, endpoint, and square-budget
argument. Together these total 403 lines and 2,497 words, excluding
check code. The 208-line delta alone is not the full proof size. The new graph engine
`gap/searcher/lower/jr.cpp` has 314 lines.

Finite inputs: five inherited local geometry/endpoint checks named in
the proof; the new 21-line budget/arithmetic check; and two exact
potential checks on graphs with 83,780,188 and 162,690,236 augmented
states (171,579,088 and 343,695,792 arcs). The producer measured about
3.6 and 5.3 GB of RAM. Critical-cycle searches are optional and are
not premises of the lower bound. The proof depends on the graph
builder's completeness as well as on all arc inequalities passing.

A route to the same coefficient with hand-verifiable local inequalities
or much smaller finite checks would improve the simplicity axis. R3's
short final algebra does not remove its large finite dependency. Future
result reports will state both proof size and required finite inputs.

---

# R3 proof ready for Claim 31 — 2026-10-03

**SUBMITTED FOR AUDIT:** `PROOF_R3.md` replaces Sections 4–6 of
`PROOF_N1.md` and gives the explicit proposed bound

```
X >= (24n-13012)/5 >= 24n/5-2603
```

for every even n>=32 and every closed Hamiltonian knight tour.
I checked the source and both producer logs: beta=2, potential range
[-104,0] in units 1/4, hence C=26 per oriented half. The budget is
sum Y_sigma<=X+12640. Together these give
2(A-R)<=E+12846 and 4n<=5E+13002.

The proof states the six-column normalization, the crossing partition,
the S-only forest relaxation, both parities, and the actual-state
middle cut. It names all reproduction commands. The exact small check
`python3 gap/turnstheory/check_r3_reduction.py` passed. I did not rerun
the large graph jobs; independent Claim 31 review remains necessary.
The period-four and period-six cycles limit the certified relaxation;
they are not used to assert a limit for a stronger full-forest model.
This completes the requested strip proof write-up. No result index or
post was changed.

---

# R3 budget confirmed; six-cell weights corrected — 2026-10-03

**R3 is written at the top of REQUESTS.md.** The joint edge set is
exactly the selected edges incident to columns {0,1,3}; its seven allowed
column pairs are 01,02,12,13,23,34,35. The tour restriction has degree
two in columns 0,1,3 and at most two in columns 2,4,5, and is a forest.
Its complete crossing count includes mixed S/F23/J crossing pairs.
The four-side count is at most X+12640, since only adjacent-side pairs
overlap and their edges lie in six-by-six corner squares.

**Required correction:** a six-cell scan must use
`q(6w-1)+p(6w0-1)+6q*wx-3p*t`, or the equivalent row-level weight in
R3. Using the old four-cell baseline on all six phases subtracts 3/2
per row. Also, w must count only S/S pairs; wx counts every remaining
pair exactly once. These conditions make the proposed budget valid.

If that certificate has beta=p/q and half-walk error C, the precise
conclusion is

```
X >= [4+2beta/(2beta+1)]n
     -2-(12638+8C+78beta)/(2beta+1),
```

for every even n>=32 and closed Hamiltonian tours. No interval lemma is
needed for R3. No new beta is certified yet.

I checked the period-six obstruction directly. It has X_S=10, B=6,
no blocked rows, and penalty 5/2 per period in the costly phase in both
orientations. Thus credits based only on blocked flags cannot pass
beta=8/5. R3 requests its completion in the joint model as a diagnostic:
the added edges' mixed crossings may supply the missing cost, but no
positive completion cost is asserted without a certificate.

**N1 finite input update:** I read KT Edge Searcher's independent C++
source and both all-history logs. They confirm beta=16/11 and zero
violated arcs. PROOF_N1.md now names that implementation and its commands.
Its full-state ranges are -667..0 and -687..0 in units of 1/44; the
Python row-level range is -596..0. The proof's constant 12993 uses the
Python range. The second implementation confirms the coefficient but
does not reproduce that smaller numerical range. Claim 27 should check
the latter if it retains the exact constant. Only the interval/N1 proof
audit is pending; the coefficient now has two finite implementations.

Checks on 2026-10-03 confirmed the seven column pairs, the 80-edge corner
enumeration, the R3 coefficient/constant algebra, and the explicit
period-six field. The field output is `cap0_field_check.log`.

---

# N1 consolidated; sharper short-run results — 2026-10-03

**For Claim 27:** `PROOF_N1.md` now contains the tile/charge proof, the
interval lemma, all four-side budget constants, the exact N1 half-walk
reduction, and the producing beta=16/11 input. Its explicit CONDITIONAL
theorem is `X>=204n/43-12993` for every even n>=32, closed Hamiltonian
tours. The interval/reduction audit and the second combined-certificate
implementation remain pending. The large constant is deliberately
conservative; no stronger audited result is asserted.

**New local findings, two implementation checks, pending audit:**
`PROOF_SHORT_RUNS.md` records three results.

1. Loss four is sharp for crossings assigned inside one full-degree
   interval: four such rows can have zero assigned crossings.
2. The TOTAL inner-strip crossings do pay `sum max(0,l-3)` exactly, with
   no O(1) loss for a finite forest. A 520-state, 4,800-arc potential in
   [-4,0] passes both graph builders. Generic run constants 0, 1, and 2
   fail on repeatable zero-crossing cycles. Cap three still gives zero
   for the new period-eight obstruction's runs of lengths two and three.
3. Two repeats of the period-eight blocked word in a sixteen-row window
   force at least one assigned inner crossing, in every phase. Exact
   minima are 2,2,2,3,3,2,1,1. Thus a charge for short runs TOGETHER is
   possible even though a charge for each short run is not.

The last result gives a precise possible next task: replace K4 by
`K4/2+M/32`, where M counts matching sixteen-row windows. This raises
the known period-eight obstruction's ratio to 3/2 while the saturated
field permits beta up to 2. A finite pattern matcher can supply the
extra row charge. No new combined certificate is claimed. REQUESTS.md
contains the exact integer weight and the boundary conditions.

Checks passed on 2026-10-03:

```
python3 gap/turnstheory/check_run_credit.py
python3 gap/turnstheory/check_short_windows.py
```

Their reports are `run_credit_certificate.json` and
`short_window_checks.json`. The first code is new; the two underlying
strip builders are separate implementations. The second checker repeats
the window calculation on each graph. All edits remain in this worker's
directory. The currently audited theorem remains 52n/11-360 (Claim 26).

---

# Claim 26 repairs applied — 2026-10-03

**AUDITED (Claim 26):** `PROOF_52_11.md` now states the PASS status and
contains both Section 4 wording repairs exactly as quoted by KT
Verifier. Its theorem is `X>=52n/11-360` for every even n>=32 and closed
Hamiltonian tours. The common-error numerator 3958 is retained, so the
proof and reproduction arithmetic stay aligned. This is Python-certified,
not a Lean theorem and not a theorem for disconnected two-factors.

I read the full-draft follow-up and consolidated-document audit verdict
before applying the repairs. RESULTS.md and the posts were not changed.
R2 remains assigned to KT Lower Bounds; `PROOF_INTERVAL.md` and the R2
history specification are ready for Claim 27. No coefficient beyond
52/11 is claimed.

---

# Claim 27 ready and R2 specified — 2026-10-03

**Claim 27 submission:** `PROOF_INTERVAL.md` gives the standalone
interval lemma `W(I)>=length(I)-4`, its exact 330-state certificate,
the blocked-row test, and the application to four sides. The last step
has the explicit conservative bound `D0+K<=E+50558` for n>=32. The
certificate has a separate implementation check; the proof awaits
KT Verifier's review.

**R2 is active, as assigned by Chief Researcher.** `REQUESTS.md` now
specifies six ghost-degree history bits, a capped run counter, the exact
two-row delay, and the full-side initial and terminal conditions. It
retains the actual history across the middle split, so the halves sum
to exactly K. The far-half scan still runs in increasing physical row
order. No additional endpoint loss is hidden in the delay.

The check commands are

```
python3 gap/turnstheory/check_inner_boundary.py
python3 gap/turnstheory/verify_inner_boundary.py
python3 gap/turnstheory/check_r2_history.py
```

The earlier instruction to wait for Claim 26 is superseded by Chief
Researcher's parallel assignment. No combined-credit certificate, and
no coefficient beyond 52/11, is claimed here.

Checks on 2026-10-03 passed: the separate interval checker verified all
580 hard arcs and the 80-edge corner count; the new history checker
verified all 4096 twelve-flag sequences with every split, all 4096
six-row degree-bit pairs, and long blocked runs. The certificate
generator and its full saved potential are unchanged.

---

# Claim 26 audit request — 2026-10-03: proposed 52n/11 bound

**Full proof ready for KT Verifier: `PROOF_52_11.md`.** KT Lower Bounds
certified request R1 at beta=4/3 in both orientations and both initial
parities, with two implementations. I read its code and logs and reran
the independent certificate in each orientation. The ranges are -155..0
and -159..0 in units of 1/12. The complete reproduction runner is
`check_52_11.py`.

**PROOF SUBMITTED FOR REVIEW, not an audited result:** every closed tour
on an even board n>=32 satisfies

```
X >= 52n/11 - 360.
```

This improves the leading coefficient by 2/33. With the retained
boundary surplus R, the exact inequalities are

```
4n <= 4E + 2(A-R) + 156,
(4/3)*(A-R) <= E+1208,
4n <= (11/2)*E+1968,
X >= 52n/11-3958/11 >= 52n/11-360.
```

The pending external review should focus on the actual boundary union
budget, the eight half-walk sum with far-corner parity, and cancellation
of R. The full proof defines every quantity and gives the exact corner
overcount constants. The audited 14/3 theorem and published files remain
unchanged. Chief Researcher has assigned Claim 26 to KT Verifier. The
proof now includes an exact section-by-section delta against the audited
document and every component check command.

**Checks passed on 2026-10-03:** all six local checks, both freshly rerun
independent strip certificates, and the rational constant calculation.
`check_52_11_report.json` records the results. The aggregate run used
`--reuse-stability-logs` to read the two successful runs from this same
session; its default command reruns them. No check was omitted.

## Request status

R1 is complete at beta=4/3. R2 is now assigned in parallel with the audit.
The saturated period-one field proves
that 4/3 is the exact limit of R1. Combining the inner-boundary lemma
with R1 is a possible later task, but is not an input to this proof.

## Route past 52/11: combine the two credits

2026-10-03. **ARGUMENT for a new finite task; no larger beta is claimed.**
The two known obstructions now have separate costs. R1 pays for the
period-4 reversal field with its boundary surplus. The blocked-interval
lemma below pays for the saturated field with interior crossings.
Together they suggest a stronger certificate than either alone.

Let `K` be the sum, over all sides, of `max(0,l-4)` over blocked runs of
length l. The interval certificate below gives additional crossings
outside each side's width-two strip, and only a constant corner
overcount across sides. Thus `D0+K <= E+O(1)`. Seek a finite certificate

```
beta*A <= D0 + K + beta*R + O(1).                     (N1)
```

The same square budget then gives
`X >= [4+2beta/(2beta+1)]n-O(1)`. Hence any beta>4/3 would pass 52/11.
With `k` the zero-or-one blocked-run charge per row and `t=2a`, the new
integer arc weight for beta=p/q would be

```
q*(4w-1) + p*(4w0-1) + 4q*k - 2p*t.                 (N2)
```

The ghost-degree history and run counter needed for k are specified in
R2 of REQUESTS.md. This augmentation is larger than R1. Chief Researcher
assigned its computation in parallel with Claim 26.

On the saturated field, `D0/length=1`, `K/length -> 1`, `R/length=0`,
and `A/length=3/4`; it imposes only beta<=8/3 on (N1). On the period-4
field in its costly parity phase, the respective rates are 1, 0, 1, 1,
so it imposes no beta limit. Cheap fields still have all four rates zero.
Thus neither known obstruction rules out beta>4/3 for the combined task.

**Unresolved:** another periodic field, or short saturated runs separated
by low-cost transitions, can still block (N2). The interval lemma loses
four crossings per run. No certificate beyond 4/3 follows without the
new finite check. The existing exact interval certificate itself still
needs the Verifier's separate review before use in a new global theorem.

---

# Earlier update — 2026-10-03: keep actual boundary crossings

**New priority: request R1 in `REQUESTS.md`. No global improvement is
claimed.** I read KT Lower Bounds' L1 and checked the new period-4 field.
It has no blocked rows, so it defeats the blocked-run-only proposal
below. The interval lemma remains valid, but that proposal alone cannot
pass beta=1. Its requested computation is superseded by R1.

The new field also gives a better lead: all eight crossings per four
rows belong to the outer-column boundary set. The current proof replaces
that set's size by its lower bound, and loses this surplus. Keeping the
actual size gives a stronger square budget and a new finite task with
the SAME strip state space.

## U1. Exact boundary surplus in the square budget

**PROVEN algebraic reduction, pending external review.** Let `b_sigma`
be the actual number of crossing pairs whose two edges both touch the
outermost column of side sigma. This is the size of that side's original
set `B_sigma` in the audited proof, not its width-two crossing count
`X_sigma`. Define

```
R = sum_sigma b_sigma - 4n,
D = sum_sigma X_sigma - 4n,
E = X - 4n + 2.
```

All candidate paths and endpoint tests stay as in old Section 11. The
union `B` satisfies `|B| >= sum_sigma b_sigma - O(1)`, since duplicate
pairs occur only in fixed corner regions. Each retained path still
avoids every overlap from `B`, regardless of how large `B` is. The
original bad-quarter budget therefore gives

```
2L <= 2E + 2(X-|B|) <= 4E - 2R + O(1).
L >= 2n - A - O(1).
4n <= 4E + 2(A-R) + O(1).                             (U1)
```

Suppose a finite certificate, summed over the eight oriented half-side
walks, gives

```
beta*A <= D + beta*R + O(1).                          (U2)
```

The actual strip crossings still give `D<=E+O(1)`. Thus
`A-R<=E/beta+O(1)`, and (U1) yields

```
X >= [4 + 2beta/(2beta+1)] n - O(1).                  (U3)
```

The new potential task for beta=`p/q` is

```
q*(4w-1) + p*(4w0-1) - 2p*t >= potential change,
```

where `w0` counts introduced crossing pairs with BOTH edges incident to
column zero and `t=2a` is charged at row end. The subtracted constants
apply to every cell transition. `w0` uses the same new and pending edges
as the old crossing weight `w`; it needs no larger state space. Splitting
a strip walk preserves these assigned crossing totals. Half-strip end
errors are bounded just as in 11.3.

**OPEN:** a certificate for any beta>1. R1 requests beta=4/3 first, then
any beta>1 or a blocking cycle. The saturated field still limits this
specific certificate to beta<=4/3. The period-4 field from L1 imposes no
such limit on the new inequality: it has `D=4`, `R=4`, `A=4` per period
in its bad parity phase, so (U2) has slack four for every beta.

## U2. Checks on the new obstruction

**PROVEN finite local calculations, checked on 2026-10-03.** Run

```
python3 gap/turnstheory/check_boundary_credit.py
```

The script directly checks proper crossings and column-zero incidence,
without the transfer graph. Per four rows it finds:

| Field | Width-two crossings | Outer-column crossings | Blocked rows |
| --- | ---: | ---: | ---: |
| New period-4 obstruction | 8 | 8 | 0 |
| Old saturated obstruction | 8 | 4 | 4 |
| Cheap field | 4 | 4 | 0 |

The new period-4 field also has four crossing pairs with a one-quarter
overlap per period, two triple-covered quarters, and two empty quarters
in square column zero. These are further possible budget credits if R1
fails. They are not used in (U1)–(U3). Unlike the saturated field, this
field does have local area slack. The two obstructions must be treated
separately.

---

# Earlier report to Chief Researcher — 2026-10-03

**Milestone: a new local lemma and a precise next finite task. No new
global crossing bound is claimed.** The saturated obstruction from old
Section 11.4 forces a second boundary at column 3. A run of `l` blocked
rows forces at least `l-4` additional crossings. These crossings are
separate from all crossings counted in the width-two strip on that side.
The proof has an exact 330-state certificate, checked with a separate
implementation. KT Verifier has not reviewed it.

This gives a new strip cost, `X_strip - length + K`, where
`K = sum_runs max(0, run_length-4)`. The old sharp field has this cost
equal to 2 per row, rather than 1. Its endpoint penalty remains 3/4 per
row. It therefore permits beta up to 8/3 in the new model, rather than
4/3 in the old model. This is only the limit imposed by that particular
field. Other cycles can impose a lower limit. No new beta is certified.

**Next action:** after its assigned 11.3 check, KT Lower Bounds can test
the augmented cost in Section 4 below. It needs a short history of ghost
degrees and a run counter capped at four. It does not need to enumerate
a full width-six strip. A certificate with beta above 4/3 would pass the
old method's ceiling. A certificate with beta above 1 would improve the
currently audited 14/3 bound.

All code and outputs for this report are in `gap/turnstheory/`. No audited
file was changed. No commit or push was made.

## 1. A column can become a boundary inside the board

**PROVEN local implication.** Fix the left-side coordinates. Let `S` be
the selected tour edges with an endpoint in column 0 or 1. For a ghost
cell `(x,y)`, let `d_x(y)` be its degree in `S`. Call row `y` blocked if

```
d_3(y) = 0,       d_2(y-2) = d_2(y+2) = 2.                 (1)
```

Rows outside the board are not used in this definition. We can omit the
first and last two rows, at a constant cost.

The possible neighbours of `(3,y)` to its left are `(1,y-1)`,
`(1,y+1)`, `(2,y-2)`, and `(2,y+2)`. An edge to column 1 belongs to `S`,
so the first condition excludes it. Each listed cell in column 2 already
has both tour edges in `S`, so neither can have an edge to `(3,y)`.
Thus a blocked cell has both its tour edges to columns 4 and 5.

Let `J` contain all selected edges between column 3 and columns 4 or 5.
It is a path forest: it is a proper subgraph of a Hamiltonian cycle.
Every cell has degree at most two in `J`. Blocked cells of column 3 have
degree exactly two in `J`. After translation by three columns, `J` is a
width-one boundary strip with some incomplete boundary rows.

## 2. Interval boundary lemma

**PROVEN with an exact finite certificate; separate implementation check
passed on 2026-10-03.** Suppose `I` is an interval of `l` consecutive
blocked rows. Scan `J` in increasing `(row,column)` order, using three
columns. Assign each crossing to the transition that adds the later of
its two edges. Let `W(I)` count these assigned crossings in rows of `I`.
Then

```
W(I) >= l - 4.                                         (2)
```

The state records pending edges and their path-component labels. The
scan permits degree 0, 1, or 2 in every column. It rejects degree excess
and cycle closure. All states are generated from the empty state. This
soft degree rule is important: a blocked interval can follow any finite
prefix, including rows with edges back toward the physical boundary.
Such rows give incomplete degrees in `J`.

A transition is called hard if it processes a ghost column, or if it
processes a boundary cell with final degree two. There are 330 states,
700 total transitions, and 580 hard transitions. The saved integer
potential `p` satisfies

```
3w - 1 + p(u) - p(v) >= 0                              (3)
```

on every hard transition. At row boundaries `-12 <= p <= 0`.
All `3l` transitions of a blocked interval are hard. Summing (3) gives
`3W(I)-3l >= p(end)-p(start) >= -12`, which proves (2).

In the actual finite board, the scan starts empty before row zero and
ends empty after the last row. Its partial degrees and component labels
are among the generated states. Restricting a tour to `J` cannot add a
cycle. Thus no assumption about the interval's end states is needed.

Let `K` sum `max(0,l-4)` over the maximal blocked intervals. These
intervals have disjoint scan transitions, and all crossing weights are
nonnegative. Consequently, if `X_J` counts all crossing pairs in `J`,

```
X_J >= K.                                              (4)
```

The interval cost is exactly computable by a run counter: cap the count
of previous consecutive blocked rows at four, and charge one at a
blocked row if that count is already four. Reset to zero at any other
row. This charges `max(0,l-4)` for a run of length `l`.

Checks, run from the research root:

```
python3 gap/turnstheory/check_inner_boundary.py
python3 gap/turnstheory/verify_inner_boundary.py
python3 gap/turnstheory/check_patterns.py
```

The first command creates `inner_boundary_certificate.json`, containing
all states and potentials. The second command uses the old, separate
`w-lowerbounds/strip_dp.py` implementation. It relaxes only its boundary
degree rule in memory; it does not modify that file. It reconstructs the
states and checks each of the 580 hard arc inequalities against the
saved potential. Both commands use exact integers and no solver.

## 3. The extra crossings fit the global budget

**PROVEN counting reduction, pending external review.** For each of the
four sides, define `S_sigma`, `J_sigma`, and `K_sigma` as above in that
side's coordinates. Write `X_sigma` for the crossings within `S_sigma`
and `Y_sigma` for the crossings within `J_sigma`.

On one side, the edge sets `S_sigma` and `J_sigma` are disjoint. The first
set has an endpoint at depth 0 or 1. The second set has endpoints at
depths 3 and 4 or 5. Thus their crossing-pair sets are disjoint too.
Across adjacent sides, a duplicate pair lies in a fixed corner region:
the side sets extend at most five columns inward, and an edge spans at
most two cells in either coordinate. Across opposite sides these sets
are disjoint for sufficiently large boards. The finitely many smaller
sizes can be covered by the constant. Therefore

```
sum_sigma (X_sigma + Y_sigma) <= X + O(1).
```

Set `E=X-4n+2` and `D=sum_sigma X_sigma-4n`. From (4),

```
D + sum_sigma K_sigma <= E + O(1).                     (5)
```

Use the same endpoint residues, penalties, and corner paths as old
Sections 11.1–11.3. Let `A` be their total penalty. That argument gives

```
4n <= 4E + 2A + O(1).                                 (6)
```

Suppose a new strip certificate proves

```
beta*A <= D + sum_sigma K_sigma + O(1).                (7)
```

Equations (5)–(7) give

```
X >= [4 + 2beta/(2beta+1)] n - O(1).                  (8)
```

This implication is proved. Inequality (7) for any new beta is open.
For reference, beta=4/3 would give 52/11, beta=2 would give 24/5, and
beta=8/3 would give 92/19. These are conditional coefficients, not bounds
established by this report.

## 4. Precise finite task for KT Lower Bounds

**CONJECTURE / finite task.** Seek beta above 4/3, or at least above 1,
with the following cost. Keep the existing width-two forest graph and
the separate oriented endpoint penalty `a` from 11.3. Retain both
possible initial row parities. Add enough row history to determine (1).

At the processing of a ghost cell, its final degree in the strip is its
number of incoming edges plus its number of newly selected outgoing
edges. Record `d_2` and `d_3`. After row `y+2` is complete, all three
values in (1) are known. The blocked flag for row `y` can then be emitted.
Carry the capped run counter from Section 2. Let `k` be its emitted
zero-or-one cost at each completed row. A shift of two rows in when this
cost is emitted changes only the endpoint constant on finite walks.

For beta=`p/q` and `t=2a`, seek an integer potential for arc weights

```
q*(4w-1) + 4q*k - 2p*t.                               (9)
```

The endpoint penalty and `k` are each charged only once per row; each
can be charged at its own completion time. The accumulated inequality
is `X_strip-length+K >= beta*sum a-C`, up to the bounded initial and
terminal history error. All history initializations used for actual
subwalks must be covered by the potential, or the omitted boundary rows
must be included in that error.

As in 11.3, use an up certificate on the near half of each side and a
down certificate on the far half. Resetting the run counter at the split
can only reduce `K`: for nonnegative integers `u,v`,

```
max(0,u-4)+max(0,v-4) <= max(0,u+v-4).
```

Thus the sum of the two half costs is at most the full-side `K`, as
needed in (5). A direct reflected scan is also valid. Degree condition
(1) is unchanged by reflection in the row coordinate.

No large computation was launched for this task. The office load was
above the brief's threshold when checked on 2026-10-03. The new local
certificate and its check each took less than one second.

## 5. Exact field checks and limits of the result

**PROVEN local calculations.** The known saturated field contains, for
every integer `y`,

```
(1,y)--(0,y+2), (2,y)--(0,y+1), (2,y)--(1,y+2).
```

Every cell of columns 0, 1, and 2 has degree two, and column 3 has no
incident edge in the strip. Every row is blocked. The strip has two
crossings per row. Its endpoint penalties alternate 1 and 1/2 in both
orientations. On a long interval, `X_strip-length+K = 2*length-O(1)`
and `sum a = 3*length/4+O(1)`. The ratio tends to 8/3. The former 4/3
obstruction therefore does not survive unchanged under (9).

The cheap field has edges

```
(0,y)--(2,y+1), (0,y)--(1,y+2), (1,y)--(3,y+1).
```

It has one crossing per row, penalty zero, and no blocked rows. The new
cost is zero, so the proposed certificate preserves the required cheap
equality case.

The checker also tests a possible competing route. In both fields every
crossing overlaps in exactly two quarters, every quarter in the first
two square columns has multiplicity one or two, and none is empty.
Hence the saturated obstruction has neither a one-quarter overlap loss,
a triple-cover loss, nor a hole in those square columns. These local
area-slack charges alone cannot remove that obstruction. The missing
crossing cost comes from the next boundary, not from such a local slack.

**Limit:** frequent breaks in blocked runs can make `K` small. The
constant four per run is not known to be optimal. Other periodic strip
patterns can still block (9) at beta=1 or beta=4/3. The next finite check
must settle this; the positive local lemma does not settle it.
