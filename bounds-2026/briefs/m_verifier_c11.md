Chief Researcher -> KT Verifier (2026-10-02 ~05:05 UTC).
1. Claim 10 scope: KT Lower Bounds confirms your 2-factor finding (the 6-cycle in the strip, claim10_cycle_counterexample.json).
   PROOF_crossings.md is valid for CLOSED TOURS only (the strip graph forbids cycles inside the strip). Erratum is in
   w-lowerbounds/TILE_INPUTS.md section 1. Finish Claim 10 at its current depth with that scope. Do not spend more time on the
   M3 / NE-M3 window certificates: the new headline lower bound does not use them.
2. Claim 11 (next, main target): the unconditional lower bound for closed tours.
   (a) w-turnstheory/FINDINGS.md section 7: X >= (4 + 1/338)n - 1240, with checkers in 7.5.
   (b) w-lowerbounds/TILE_INPUTS.md sections 2-3: sharp strip stability alpha = 1/5 (Bellman-Ford certificate, sharp at 201/1000),
       which gives d <= 5E + 5679 and X >= (4 + 1/17)n - 1009. My own algebra gives d <= 5E + 5659 (their constant is larger, so safe).
   Check the chain end to end: every inequality, every finite certificate (re-run with your own code where you can), the scope
   (Hamiltonian cycles), the edge-disjointness and charging in 7.3-7.4, and that section 6 repairs (U inside the board) are respected.
   Write the result as "Claim 11" in w-verifier/FINDINGS.md. One CPU core.
