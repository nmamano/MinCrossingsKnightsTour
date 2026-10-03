Chief Researcher -> KT Turns Theory (steer): CHANGE OF TASK. Nil says the additive constants (14, 28) do not matter to him; he
cares about the asymptotic terms and about being CONVINCED the results are correct. So drop the constant work.
New task: write the human-readable all-n correctness proofs of the two upper-bound constructions, in w-turnstheory/PROOFS.md:
 (A) TT16: for every even n >= 48 there is a closed tour with 8n + O(1) turns (data: w-integrator/FINDINGS.md section TT16,
     kt/board.py, w-integrator/corners/TT16_res*.json, w-integrator/tours/certificates/TT16_n*.json);
 (B) H16a: 9n + O(1) crossings (sections "period-24 argument" and H16a).
The gap the Verifier flagged: the corner reuse works for all n only if the outside path structure for n + p is the one for n
with one period inserted in each band, and the strand permutation per inserted period composes to the identity (p = 8 for
TT16, 24 for H16a). Prove this by an insertion argument (cut each band at a fixed place away from the corners, insert one
period, show the endpoint matching seen from the corners changes by the permutation rho of one period, and rho^k = id), then
show the turn/crossing count grows by exactly the per-period amount (locality). State which finite checks the proof relies on
and give a standalone checker (no solver) that performs them. Keep it short and convincing: Nil is a co-author of the paper.
End your turn with a short summary.
