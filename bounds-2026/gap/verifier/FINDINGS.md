# Claim 41 — Square Gap Lemma, 2026-10-03

PASS, computer-assisted: the square Hall lemma holds for all finite cut sets in knight-edge sets of maximum degree two. Uniformity passes by leaf induction. Independent geometric SAT enumeration matches all 117,612 patches across 82 types; independent DP reaches the exact 8,660-key fixed point on iteration 6 and root minimum excess 2. Half version remains false. F1 is still open. Report: claim41_report.md; certificate: claim41_check.json and claim41_values.json.

# Claim 40 — F1/R4 red team, 2026-10-03

PASS for F1 sufficiency, current Hall-subset certificate logic and degree relaxation. GAP for F1 and the completed finite-state mapping. Required repair: do not create hole atoms from incomplete halo squares; pure P gives two false holes per row at square depth 6. Use quarter atoms only at depths 0..5 or complete their owner edges, and retain all actual baseline consumption of represented pair atoms. Four actual-tour baseline-subtracted Hall tests found no obstruction, including the nonzero residual demand on FIELD. Report: claim40_report.md. Claim 38 section-8 follow-up is already complete.

# Claim 39 — half-price hand kernel, 2026-10-03

PASS: exact payable-quarter packing, radius-two support, private path allocation and good-middle/end-zone reduction. The conditional bound is X>=5n-(612+C_side), even n>=128; C_side includes the 42-unit small-radius allowance. Say zero flux modulo three, not integer zero. F1 remains the single new price lemma: it must pay actual residual demands from the same residual atoms with one global error. No 5n theorem yet. Report: claim39_report.md; independent check: claim39_check.py/json/log.

# Claim 38, section 8 follow-up — 2026-10-03

GAP for latest B', C* and D*. Good-point/free-fold turns and conditional even-shift trapping pass. The claim that all clean returns have steep chevron ports is false: an explicit perfect ribbon field has a shallow-to-steep clean return. C* still needs a bound or joint payment for its unbounded exceptions. Independent fixed-rule census agrees on FOLD; the old gadget preserves width-six pairings, not the new depth-three ports, and does not refute D*. Full follow-up: claim38_v3_report.md.

# Claim 38 — SHEET v2, 2026-10-03

FAIL: D_T with overlapping-window EXC. A 6-by-16 collar gadget preserves all exterior partners and one-cycle connectivity but changes (X,BQ,EXC) by (20,34,18), lowering E-BQ/4-EXC by 6.5 per copy. Linear copies in the audited FOLD family refute any O(1) allowance. B_T and C' remain GAP. Traversed-good squares do not exclude a gentle turn beside a bad vertex neighbourhood; G1 also does not supply P-compatible matching. Repaired A and local barrier convention pass with qualifications. Report: claim38_report.md; exact witness: claim38_gadget.json; independent checks: claim38_gadget_validation.json.

# Claim 37 — square Gap Lemma partial result, 2026-10-03

PASS: perimeter reduction and exhaustive exclusion of tree islands through size 10 (4,060 shapes, including 2,829 at size 10), independently encoded with geometric quarter coverage and direct endpoint bits. The square Hall inequality follows for every set of at most 11 cuts. Wording repairs: adjacency trees may have diagonal self-contact and holes; 2s+2 counts boundary sides, not necessarily distinct vertices. GAP: unrestricted tree sizes and the full square lemma. Full report: claim37_report.md; evidence claim37_check.py/json/log and claim37_author.log.

# Claim 36 — latest SHEET red team, 2026-10-03

FAIL: original current-tour Sheet Lemma (B). In the audited FOLD family, W=3n-O(1) while SSR=2n/3+O(1): the arch flips turn one endpoint of each long chevron into an exception, excluding it from SSR but leaving wall labels. FAIL: (C) trapping premise; opposite-phase corridor returns coexist with unchanged P collars and form chains, not isolated cycles. A different 1/2 price remains open. (A) omits EXC from the starting-label count; (D) needs a single mixed-capacity ledger. The revised BQ inequality remains open; its new barrier proof incorrectly ignores strand passages through wall vertices. Full report: claim36_report.md and w-verifier/FINDINGS.md Claim 36. Evidence: claim36_scan.py, family_scan.log, corridor.py/json, and validated tours.

# Claim 35 — latest wall audit, 2026-10-03

PASS: the period-(2,4), 19-edge wall has exactly two crossings, four holes, no finite cycle, and nonzero psi at every row. An explicit alternating (1,-1) zigzag fold-stack extension gives perfect infinite exteriors with no added crossings; the 1/2 rate is not certified here for prescribed pure straight exteriors. GAP: this does not yet refute L2-v3 on actual retained paths in closed tours with one total constant deficit. It does refute a private price above 1/2 for unrestricted charged paths across such walls. Full report: claim35_report.md and w-verifier/FINDINGS.md Claim 35. Exact evidence: claim35_wall.py/json. No author files edited.

# Claim 34 — latest red-team result, 2026-10-03

FAIL for the strong gap-half lemma: the explicit closed 16-by-16 tour claim34_tour_n16.json has an interior absorbing cut with five gap halves and only one bad quarter. All gap squares are at distance >=5 from the sides. The original square Hall lemma remains CONJECTURE/GAP; no counterexample found. Its conditional mixed-cost deduction passes. W1 comparison PASS: an independent exact-quarter projected enumeration reproduces 200/164/156 maps for R=1/2/3. Current STRUCTURE.md includes Claim 30 scope repairs. Full report: claim34_report.md and w-verifier/FINDINGS.md Claim 34. Witness validation: claim34_validate.py and claim34_validation.json.

# Claim 33 — latest window audit, 2026-10-03

PASS for the precise W1 and W3 window lemmas. Independent CNF reconstructions match every clause; both W1 DRUP proofs and all 16 W3 proofs pass, including depth 6. Every tour restricts to the models when the core fits; halo degree means degree in the retained edge set. Use translated interior windows for depth >=7, distinguish one side strip from all four strips, and use radius ten with corner exclusions for off-S* support. No private allocation price follows. Full report: claim33_report.md and w-verifier/FINDINGS.md Claim 33. Evidence: claim33_windows.py/json/log.

# Claim 32 — latest red-team result, 2026-10-03

GAP for the proposed 5n ribbon-absorption theorem. FAIL for R3 without added global hypotheses: an alternating horizontal-wall field has zero crossings and no bad quarters, but its interior strands run bottom-to-top through arbitrarily many walls. Wall-face length alone does not give distinct same-side returns. Repair: label original side ends, handle free wall-to-wall transfers, and charge all absorbers against one residual budget above 4n. This does not refute the closed-tour 5n bound. Full report: claim32_report.md and w-verifier/FINDINGS.md Claim 32. Exact check: claim32_pleats.py/json. No author files were edited.

# KT Verifier — latest audits, 2026-10-03

Claim 31 is PASS. Every closed Hamiltonian tour on an even n by n board, n>=32, satisfies 5X>=24n-13012, hence X>=24n/5-2603. An independent six-column implementation checked both orientations and all 171,579,088 / 343,695,792 augmented arcs, reproducing both ranges [-104,0]. Peak RSS was about 1.76 GiB. Evidence: claim31_*.

Claim 30: the local T1–T3 statements pass; T4 passes for a full spanning 2-factor and whole-square U inside D with all B overlaps excluded. The connected-domain/global-ribbon-word conclusion is FALSE. In the validated n=96 tour, TL(2,2) forces H and BR(5,6) forces V on ribbon 1, although both lie in one connected good slash domain. Bad squares interrupt the ribbon. Repair: one bit per uninterrupted good ribbon run; keep full-plane monotone translates as a separate construction. Both author checks and independent exact-cover enumeration reproduce 48 plane solutions and 252 torus solutions. Evidence: claim30_*.

Full reports: ../../w-verifier/FINDINGS.md, Claims 31 and 30. No author files were edited. The proof author can update Claim 31 to audited PASS and must apply Claim 30's scope repairs before promoting its full summary. Both assignments are complete.


## Proof-size and finite-input profiles — 2026-10-03

These profiles apply Nil's coefficient/simplicity criterion to the recent audited results. Sizes are whitespace word counts of the current Markdown proof files, including displayed formulas, tables, and check commands. They measure the written argument, not formal proof length. The finite graph size is listed separately because a short reduction can still require a large computer check.

| Audit / coefficient | Written proof size | Essential new finite input beyond the shared tile and endpoint facts |
| --- | --- | --- |
| Claim 26: 52/11 | PROOF_52_11.md: 2,654 words, 385 lines | Two oriented width-two strip potentials; independent checker verifies 687,262 augmented cell arcs per orientation. Boundary overlap and corner duplication also have small exact geometric checks. |
| Claim 27: 204/43 | PROOF_N1.md: 3,515 words, 558 lines | Interval potential: 330 states, 580 hard inequalities. Combined row certificate: 40,158,400 augmented arcs per orientation. A four-bit history identity and a capped run counter are additional mathematical inputs. |
| Claim 31: 24/5 | PROOF_R3.md delta: 1,303 words, 208 lines; inherited Sections 1–3: 1,194 words, 195 lines. Total reading: 2,497 words, 403 lines. | Six-column joint certificate: 171,579,088 up arcs and 343,695,792 down arcs. The independent implementation uses about 1.76 GiB peak RSS. No interval potential or blocked-run automaton is needed. |
| Claim 30: local structure, no new coefficient | Submitted STRUCTURE.md: 2,060 words, 139 lines; scope repairs in Claim 30 remain necessary. | No large certificate. T1–T3 have elementary local proofs. The 48 plane configurations and 252 torus configurations are exhaustive corroborating checks, not premises replacing those proofs. T4 inherits the audited tile-area budget. |

The shared ingredients are the four knight-tile shapes, their one/two-quarter overlap rule, the local flux identity, the endpoint coefficient table, and the finite endpoint-loss cases. They have exact small geometric checkers and short finite case proofs. Counting them as shared does not remove them from a self-contained proof.

Claim 31 improves the coefficient and simplifies the written reduction relative to Claim 27, but greatly enlarges the certificate. Claim 26 keeps a much smaller graph. These are different simplicity tradeoffs; I do not discard the smaller-certificate route merely because its coefficient is lower. Claim 30's repaired ribbon-run statements offer a mostly hand-checkable structural input, but no 5n conclusion has yet been audited from them.

Optional optimality witnesses, diagnostic tour checks, and torus samples do not add premises to the stated crossing lower bounds. For each future audit, report the theorem, proof size, essential finite checks, and which checks are only corroborating. A hand proof or a small certificate can therefore remain valuable even after a larger computational bound is known.

## Claim 30 addendum: W1 local SAT/DRUP cross-check — 2026-10-03

**PASS for the precise 9-by-9 / central 3-by-3 statement.** I read the W1 model generator, fold-stack map generator, and standalone DRUP checker. I independently rebuilt the entire CNF in `gap/verifier/claim30_w1.py`, without imports from the authors. The rebuilt model has 424 edge variables, 7,144 clauses, and 156 excluded central maps. Its clause multiset equals the supplied CNF exactly. The independent crossing test solves the two segment parameters with integer determinants. Results and the CNF hash are in `gap/verifier/claim30_w1.json`.

The variables are every knight edge with an endpoint in the 9-by-9 core. Each core vertex has exactly two selected edges, each halo vertex at most two. Every strictly crossing pair of represented edges is forbidden. The central map records both incident edge directions at every one of its nine vertices. Each exclusion clause contains the negatives of all edges in one map; core degree two makes this equivalent to excluding that exact map. Duplicated literals from edges between central vertices do not affect the clause. Cycles are allowed, so the statement also applies to tours. Edges with both endpoints outside the core are absent; restricting a full configuration to represented edges gives the required relaxation.

I reran the standalone checker against both supplied proofs. Glucose: **2,942 RUP additions, PASS**. Lingeling: **2,989 RUP additions, PASS**. Both derive the empty clause. Logs: `gap/verifier/claim30_w1_glucose.log` and `claim30_w1_lingeling.log`. Thus every configuration meeting these window hypotheses has one of the 156 fold-stack maps at its centre.

**Scope unchanged.** This finite local theorem supports the local structure classification. It does not prove one ribbon bit throughout an arbitrary connected good domain, where bad squares can interrupt a ribbon. The full-tour counterexample in Claim 30B remains valid. Neither this CNF nor its proofs certify the subsequent global gluing/no-junction corollary as worded; any such use must specify complete translated window hypotheses and prove the gluing step. The four functional families in W1 are exhaustive **up to sign** within the stated search range; add those words to its definition paragraph (the source code already uses that convention).

**Proof-size / finite-input profile.** W1 supplies a short local reduction to a 424-variable, 7,144-clause CNF and two checked proofs of about 3,000 RUP additions each. One proof suffices for the theorem; the second is corroboration. It adds no lower-bound coefficient and does not replace Claim 30's required scope repairs. No large graph rebuild was repeated. Claims 29, 31, and 30 remain complete in the requested order; Claim 31's bound is unchanged.
