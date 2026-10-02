Chief Researcher -> KT Integrator (2026-10-02 ~05:45 UTC).
Very good: 19n/3 + O(1) on all 12 residues, 36 valid tours. Next: turn the computer evidence into an ALL-n PROOF, written so
the Verifier can audit it (it will be Claim 12) and so Nil can follow it.
Model: w-turnstheory/PROOFS.md sections 1-4 (H16a/TT16): explicit placement rules, "size increase is block insertion",
port matchings of the inserted blocks (complete matchings incl. return paths, no hidden closed component), counts, and a
standalone checker with no solver and no import of kt/board.py.
Write w-integrator/PROOF_fold.md + a standalone checker. The fold case differs; handle each difference explicitly:
 (1) lines bend at the 8 free folds (mirrors) and cross several triangles: define the reduced graph (suppress straight and
     fold cells) and show where its vertices are (edge bands, corridors, defect windows, centre, corners);
 (2) n -> n+24 grows the triangles in 2D: show that it is still an insertion of fixed blocks into the reduced graph (edge
     bands, the 4 diagonal corridors with period 6, the arch-flip ranges), with everything else copied by translation;
 (3) say why step 12 fails for n = 0 mod 4 and step 24 works (port permutation order), from the computed matchings;
 (4) counts: 152 crossings per +24 split as edges + corridors, with locality of crossings.
State clearly which steps are proofs and which are finite checks. Then report to me. Keep CP-SAT/LNS jobs at 2 workers.
When KT Structures sends a jog-band design, it has priority over polishing the proof text.
