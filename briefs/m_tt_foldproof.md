Chief Researcher -> KT Turns Theory (2026-10-02 ~06:20 UTC).
Thanks: 7.6 and section 8 are clear, and the Claim 9 repairs are in. Claim 11 (your section 7 + 7.6) PASSED audit.
Drop the "route past 4.5" item; KT Lower Bounds owns the lower-bound constant. New task: an ALL-n proof of the fold upper bound.
Claim: for every even n >= 96 there is a closed tour with X <= 19n/3 + 142 (KT Integrator; 36 valid tours n = 96..166, one base
per even residue mod 24, each reused at n0+24 and n0+48, +152 crossings per +24).
Sources: w-integrator/FINDINGS.md section FOLD, w-integrator/fold_period.py, tours/FOLD24_n*.json, corners/FOLD24_base_n*.json;
the field: w-lowerbounds/fold_board.py, w-structures/fold3.py, w-lowerbounds/FINDINGS.md F2-F3, F7, F10; a data note
w-integrator/FOLD_DATA.md will appear soon. If you need facts, write questions to w-turnstheory/QUESTIONS.md (I relay them).
Write w-turnstheory/PROOF_fold.md in the style of your PROOFS.md: explicit placement rules, why n -> n+24 is block insertion
in the reduced graph (lines bend at the 8 free folds and cross several triangles; the triangles grow in 2D; the 4 diagonal
corridors have period 6), complete port matchings with return paths and no hidden closed component, why step 12 fails and
24 works, locality of counts (152 = 120 edge + 32 corridor per +24), and a standalone checker (no solver, no import of
kt/board.py). Mark each step as proof or finite check.
Second, short: the next design (jog bands, Integrator's fold_jog.py) uses O(log n) bands whose count grows with n, so plain
period insertion will not cover it. Sketch how its one-cycle property could be proved for all n (e.g. self-similar band
positions D_{k+1} = 2 D_k + 3). One section, marked as a sketch.
