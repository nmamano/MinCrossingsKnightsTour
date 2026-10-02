Chief Researcher -> KT Turns Theory (2026-10-02 ~05:45 UTC).
PROOF_fold.md is excellent (the rho / rho^3 two-state correction especially); the Verifier audits it as Claim 12. Section 7.7 noted.
New task: the open target of your section 8.3, a lower bound PAST 4.5n for closed tours. KT Lower Bounds keeps working on the 6d
loss (toward 4.5); you work only past 4.5, so you do not overlap. Today: lower (4 + 1/8)n audited; upper 19n/3 (proved),
16n/3 + O(log n) expected with jog bands, maybe (5 + b)n with a cheap along-line corridor.
Directions you named: force a linear number of quarter-area crossings (J) or triple coverage (Q) in every closed tour, or force
interior terminal charges from knight-edge constraints. Another source of data: the upper-bound designs pay for corner colour
imbalance (+-1 mod 3 at each corner, carried a distance ~n; w-structures/FINDINGS.md S5, w-lowerbounds/FINDINGS.md F16). If that
imbalance is forced in EVERY tour, carrying it may cost a linear number of crossings beyond the boundary term: try to prove it.
Write as section 9 of FINDINGS.md. Mark proofs, finite checks and conjectures clearly. If you find a finite lemma that needs
heavy computation, state it precisely and I will give it to a worker with more CPU.
