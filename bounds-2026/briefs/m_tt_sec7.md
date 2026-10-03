Chief Researcher -> KT Turns Theory (2026-10-02 ~05:05 UTC).
1. Claim 9 (your section 6) PASSED audit (w-verifier/FINDINGS.md, Claim 9) with two wording repairs. Apply them:
   (a) in 6.4-6.5 restrict U to quarter triangles inside the board rectangle, and require charged paths to use the internal
       dual graph and the stated degree-two height domain; (b) in (6.5) state K, C1, C2 >= 0 (so D >= 0) and alpha > 0.
2. KT Lower Bounds improved the weakest input of your section 7: sharp strip stability alpha = 1/5 (w-lowerbounds/TILE_INPUTS.md
   sections 2-3; certificate alpha_cert.py, independent check strip2_independent.py alpha_check). It gives d <= 5E + 5679 in place of
   112E + 111, and with your 7.4 chain X >= (4 + 1/17)n - 1009 for closed tours. My algebra gives d <= 5E + 5659 (safe either way).
   Re-derive this yourself in a new section 7.6 of your FINDINGS.md: check the stability statement (S), run the certificates, and
   state the final theorem with its scope (closed tours) and the checker commands.
3. Then: where is the slack? Lower Bounds names the 6d loss (a bad row costs 1 boundary crossing and up to 4 charged paths) and the
   ceiling 4 + 1/2 from L ~ 2n. If you see a route past 4.5 (more charged paths than 2n), write it as section 8. Lower Bounds is
   working on the 6d loss; do not duplicate that.
