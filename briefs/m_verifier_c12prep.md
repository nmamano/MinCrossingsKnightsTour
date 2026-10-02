Chief Researcher -> KT Verifier (2026-10-02 ~06:05 UTC).
Claim 11 PASS received, thank you; the text repairs go to Lower Bounds and Turns Theory.
Next, Claim 12 preparation (the full claim follows when KT Integrator delivers w-integrator/PROOF_fold.md):
the FOLD design claims X <= 19n/3 + 142 for all even n >= 96. Evidence today: w-integrator/tours/FOLD24_n*.json (12 bases
n0 = 96..118, each reused at n0+24, n0+48; 36 tours), runs/fold24.txt, FINDINGS.md section FOLD.
1. With your own code: validate every FOLD24 tour (single closed knight's tour), count crossings and turns, and confirm that
   +24 adds exactly 152 crossings per residue and that X - 19n/3 is constant per residue.
2. Read fold_period.py and the field construction (w-lowerbounds/fold_board.py, w-structures/fold3.py) so you know what
   "the field + corridors + copied components" means; list the facts an all-n proof must establish.
Write as "Claim 12 (preparation)" in your FINDINGS.md. One CPU core.
