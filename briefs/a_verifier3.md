Chief Researcher -> KT Verifier: thank you; claims 2 and 3 are clear. The Integrator has now answered your residue gap:
w-integrator/FINDINGS.md (sections "period-24 argument" and "T18"), w-integrator/period24.py, base corners in
w-integrator/corners/ (one per even residue mod 24 for H16a and for T18), certificates in w-integrator/tours/certificates/.
Claimed: X = 9n + b (H16a, b listed per n mod 24) and T = 8.5n + b (T18, b = -17,-19,-19,-20 for n mod 8 = 0,2,4,6), for all
even n >= 48, by: strand permutation BL order 3, MID identity, TR order 3, so the outside path matching repeats with period
24, and each base corner completion is reused unchanged at n0 + 24k. Please audit that argument (is "outside matching
period 24" enough, together with locality, to make the corner reuse valid for every k?), and spot-check a few reused-corner
tours for large n (e.g. rebuild n0 + 24*8 yourself from the corner files if feasible, or check the stored ones).
Write the verdict as Claim 4 in w-verifier/FINDINGS.md; end with a short summary.
