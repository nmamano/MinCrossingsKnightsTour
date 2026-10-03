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
