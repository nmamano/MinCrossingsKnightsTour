## Claim 34 — Gap Lemma red team and W1 comparison closeout — 2026-10-03

**FAIL: the strong gap-half lemma.** A validated closed 16-by-16 knight tour has an absorbing cut with five gap halves but only **one** bad quarter in their union. Every gap square is at distance at least five from the board sides, so the intended side-collar exclusion does not fix this counterexample.

**GAP / CONJECTURE: the original gap-square Hall lemma.** The counterexample does not refute that version. I found no counterexample to it in the limited searches below; this is not a proof. **PASS: the independent W1 comparison reproduces 200, 164, 156 central maps at R=1,2,3.**

GAP_LEMMA.md was absent at the first read and appeared during the search. I then used its precise definitions, strong version, and intended cost application. A copy of that 1,049-word, 75-line draft is saved as `claim34_GAP_LEMMA_reviewed.md`. Source hashes are in `claim34_sources.json`. No author files were edited.

### 34A. Closed-tour counterexample to the strong version — PROVEN by explicit witness

File: `gap/verifier/claim34_tour_n16.json`, in the repository's standard two-direction-code tour format. It has 256 vertices, 256 undirected knight edges, one connected cycle, and X=318 crossing pairs. The solver-free checker `claim34_validate.py` checks degrees, board containment, knight moves, connectivity, exact quarter coverage, endpoint bits, and the claimed cut. It also calls the prior independent tour checker on the standard encoding. The full edge list and cyclic order are in `claim34_closed_tour.json`.

The backslash-chain cut is

    RT(6,9), LB(7,9), RT(7,8), LB(8,8), RT(8,7), LB(9,7), RT(9,6).

Its two endpoint squares are good. The initial half RT(6,9) is covered by the d-tile of edge (6,10)--(8,9), so its bit is H. The final half RT(9,6) is covered by the c-tile of edge (9,8)--(10,6), so its bit is V. The five intervening squares are all bad. Hence this is an absorbing cut under the draft's definition, with two absorbed ends.

| Gap half | Multiplicities (B,R,T,L) in its square | Bad quarters in that half |
| --- | --- | --- |
| LB(7,9) | (1,0,0,1) | none |
| RT(7,8) | (2,1,1,2) | none |
| LB(8,8) | (1,1,2,2) | L only |
| RT(8,7) | (2,1,1,2) | none |
| LB(9,7) | (1,0,0,1) | none |

Thus the union of the gap halves contains exactly one bad quarter, L(8,8), of multiplicity two. The strong inequality already fails for the singleton set K containing this cut: 1 < 2|K|. Sharing between different cuts is not needed to break it. In contrast, the five gap **squares** contain ten bad quarters.

The tour has five absorbing cuts in total. My independent bipartite matching check finds 10/10 assigned quarters for the square version and only 9/10 for the half version. The author's current scanner agrees when run on this tour with ALLCUTS=1: square matching 10/10, half matching 9/10, and one cut with fewer than two bad quarters in its own halves. See `claim34_cluster_author.log` and `claim34_validation.json`.

**Repair:** remove the strong half statement. Any proof must allow bad-quarter assignments to leave the chain half and enter the rest of a gap square. The original square statement permits precisely that repair. The witness does not show that the square statement is sufficient to finish the global absorption route.

### 34B. Search model and limits of the square-version evidence

`claim34_gap_search.py` independently constructs all knight edges touching a square window's vertex core, with exact degree two on that core and degree at most two on the endpoint halo. Quarter multiplicities use the verifier's exact tile geometry. For every candidate chain interval it can select an absorbing cut only if the endpoint halves are good with different bits and every intervening square is bad. All cuts are generated in one fixed direction, without reversed duplicates.

The model selects an arbitrary subset of candidate cuts. It counts each bad quarter in their allowed union only once, then asks for 2 times the number of selected cuts to exceed that count. This tests a Hall deficit directly; it does not merely count single cuts. Local SAT witnesses are not automatically tours. I therefore completed the half-version witness to a closed tour using a circuit constraint, then validated it without the solver.

Results, one worker per job:

| Window of unit squares / maximum gap length | Version | Result |
| --- | --- | --- |
| 3-by-3 / 4, 28 candidate cuts | square | INFEASIBLE, about 0.10 s |
| 3-by-3 / 4, 28 candidate cuts | half | INFEASIBLE, about 0.14 s |
| 4-by-4 / 6, 88 candidate cuts | half | Counterexample found, about 0.43 s |
| 4-by-4 / 6, 88 candidate cuts | square | UNKNOWN after 20 s |
| 5-by-5 / 8, 200 candidate cuts | square | UNKNOWN after 30 s |

The small INFEASIBLE results are bounded CP-SAT checks, not general proofs or separately checked DRUP certificates. UNKNOWN is no evidence of impossibility. The square conjecture remains open. The saved tour demonstrates why passing four construction-family tours was insufficient for the stronger conjecture.

Definition repair: regard a cut and its reverse as one cut, or require the displayed forward chain orientation. Otherwise a set of sequences could count the same physical gap twice. The scanner uses the forward convention. Also, when applying an interior version, every gap square must satisfy the distance condition, not just the first square to which cluster_scan assigns its two ends.

### 34C. Conditional use of the square lemma in the mixed cost — PASS

For the exact cost identity, define X1(t) as the number of one-quarter-overlap crossing pairs whose overlap quarter is t. Define W3(t)=binom(m_t-1,2) when m_t>=1 and zero at a hole. In particular, do not evaluate the polynomial at m_t=0. With quarter shares of all crossing pairs outside B,

    sum_t c(t) = (G+X1+W3)/4 + (X-|B|)/2
               = E/2 + (X-|B|)/2.

Using E=X-4n+2 and R=|B|-4n gives the exact equality

    E = sum_t c(t) + R/2 + 1.

If the draft's X1 brackets mean only a Boolean indicator, they undercount multiple pairs at a quarter. The stated lower-budget inequality remains valid with that smaller cost, but the exact identity requires the count above.

A hole has cost at least 1/4. At a multiply covered quarter with an overlap pair outside B, that pair contributes at least (1/2)*(1/2)=1/4, because a crossing overlap has at most two quarters. For gap squares at distance >3 from all sides, no B overlap reaches them. Thus, **if the square Hall lemma is proved**, two distinct assigned bad quarters per cut give at least 1/2 per cut, or 1/4 per absorbed end, without spending that quarter twice. This deduction is sound and does not require the false strong version.

The mixed identity is already a residual-budget identity above 4n; it should not be added again to another independent copy of the baseline. Nor does this conditional result establish that 4n-O(1) original side labels become absorbing cuts. Walls, same-bit gaps, side exceptions, and free transfers still require the global accounting identified in Claim 32. The half counterexample and the conditional square price are separate issues.

### 34D. W1 comparison and Claim 30 closeout — PASS

I read `w1_compare.py`. It imposes exact coverage on the (2+2R)-by-(2+2R) square window and degree two at its (1+2R)-by-(1+2R) interior lattice points. It counts the incident-edge maps at the central 3-by-3 vertices. It does not impose degree bounds at other points. These are the local T1–T3 hypotheses, not the same model as W1's crossing-free 9-by-9 core.

The author's full-solution enumeration at R=3 was stopped to keep the check light. Instead, `claim34_w1_check.py` builds the model independently from exact tile quarters and enumerates only **new central maps**. It first excludes all 156 fold-stack maps, then excludes each additional central map as found. The final residual model is INFEASIBLE for every R. Separately, the checker constructs a full-plane extension for each fold-stack map and verifies all finite-window degree and quarter constraints. This proves both inclusion directions in each tested window.

| R | Edge variables | Fold-stack maps | Extra maps | Total central maps |
| --- | ---: | ---: | ---: | ---: |
| 1 | 80 | 156 | 44 | 200 |
| 2 | 168 | 156 | 8 | 164 |
| 3 | 288 | 156 | 0 | 156 |

The projected searches took about 1.47, 0.35, and 0.08 seconds respectively, excluding setup. Outputs: `claim34_w1_check.json/log`. These are exhaustive finite comparison checks. They support the new dictionary in STRUCTURE.md Section 5b, but do not identify the hypotheses of its model with those of W1 or prove a global word per connected domain.

The current STRUCTURE.md explicitly incorporates Claim 30's repairs: one bit per uninterrupted run, T4 restricted to a full spanning 2-factor, and the corrected summary. The prior connected-domain objection is resolved in that revised text. The old counterexample remains a useful test against reintroducing the stronger statement.

**Pareto profile.** The 1,049-word gap draft is still a conjecture in its square form and false in its strong form. This audit adds no lower-bound coefficient. Its decisive finite input is one explicit 16-by-16 tour plus a short exact witness check; no solver trust is needed to verify the counterexample. The W1 comparison uses three small finite models, with at most 288 edge variables, and a direct fold-stack extension check. The next mathematical task is a square-level assignment proof that explicitly permits off-half quarters and handles sharing; the false half lemma must be removed first.

Claim 34 is complete. All computation started for this audit has stopped.
