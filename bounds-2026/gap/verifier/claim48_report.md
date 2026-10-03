# Claim 48: independent crossing recount — 2026-10-03

**PASS.** A fresh standard-library checker, with no imports from earlier checkers or worker code, counts 1936 proper crossing pairs in `claim36_FOLD_n288.json` and 2380 in `claim47_patched_n288.json`. It checks degree, reciprocal edges and single-cycle connectivity in both tours, reconstructs the patched edge set from the Claim 47 witness and all four placements, and verifies exact equality with the saved patched tour.

Each copy removes 29 crossing pairs and introduces 140, hence adds exactly 111. These are four separate local recounts, not just (2380-1936)/4. Pairs are unordered, proper intersections use strict integer determinant signs, and shared endpoints do not count. The complete-tour recount uses unit-square bounding-box bins; the local recount examines every pair involving a changed edge.

The d0=0 joint slack is also correct: 598+1584/2-2*55-388=892, versus 116 for the base. The minimum patched per-side slack is 220. This is a recomputation from our saved Claim 47 full-tour census, not a fresh quarter census.

Thus Claim 47 refutes C5-W, not an above-5n lower bound. At n=288 the patched tour has X-5n=940. In the period-28 family, X=X_FOLD+111m+O(1), m=n/28+O(1), giving coefficient 19/3+111/28=865/84, approximately 10.30, well above 5.

Evidence: `claim48_check.py`, `claim48_check.json`, `claim48_check.log`. The JSON records all input hashes and per-copy counts. Reproduce with `python3 gap/verifier/claim48_check.py` from the research root; one process, no solver.
