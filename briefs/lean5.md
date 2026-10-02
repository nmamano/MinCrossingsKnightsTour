Chief Researcher -> KT Lean (2026-10-02 ~08:45 UTC). Excellent milestone. Skip the constant improvement (Nil only cares about
the asymptotic coefficient). The chain is now STABLE: Claim 19 PASSED X >= 14n/3 - 407 for closed tours, and beta = 1 is exactly
sharp, so it will not move again soon. Goal: a fully kernel-checked X >= 14n/3 - O(1) for every closed tour, n even, large.
1. Corner hypothesis -> the weaker endpoint test of w-turnstheory/FINDINGS.md 10.4 (F mod 3 from the eight selected edges at the
   endpoint row; joint test over both orientations), as used in w-turnstheory/PROOF_crossings_lower.md section 4. Restate
   combined_count with b = number of failed tests in the scan ranges, and the conditional theorem: b <= E + C  =>  X >= 14n/3 - C'.
2. Then the strip-stability certificate, now with small numbers: joint endpoint test, weights (4w - 1) - 4b, beta = 1, potential
   range [-29, 0] in units of 1/4 (w-lowerbounds/TILE_INPUTS.md section 9; endpoint_stab.py, endpoint_independent.py). Kernel-only,
   Nat-only encoding; a 1-2 h one-time build is acceptable. Plus the strip-model soundness (tour edges at one side give a walk whose
   weight is the strip crossings, and b counts failed tests). Plan it in STATE.md first, with the soundness statement you will
   prove, and report the plan in 5 lines before the long build.
Kernel-only, no native_decide. Hand off at about 50% context.
