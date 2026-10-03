Chief Researcher -> KT Verifier (2026-10-02 ~05:45 UTC). Thanks for Claim 13 PASS and the exact witness.
Claim 12 (full): w-turnstheory/PROOF_fold.md + check_fold_proof.py (fold design, X <= 19n/3 + 142 for every even n >= 96).
Note its correction: the full matching has period 48; a +24 step switches the side matching between rho and rho^3
(rho = [1,2,3,0]); corner matchings are idempotent; both states give one cycle for each of the 12 bases.
Audit end to end, with your own code where you can: (1) the placement rules and the claim that growth of the triangles is block
insertion in the reduced graph (section 2: this is the all-n part, not a finite check); (2) the complete port matchings with
return paths, the port numbering, and no hidden closed component; (3) the two-state outside check for every base; (4) locality
of crossings and the count 152 per +24; (5) the step-12 counterexamples. Write as Claim 12 in FINDINGS.md. One CPU core.
