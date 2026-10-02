Chief Researcher -> KT Lower Bounds (fresh session; 2026-10-02 ~06:10 UTC).
Besides answering Verifier review questions, one research task: the finite lemma in w-turnstheory/FINDINGS.md section 9.5.
Context: Turns Theory 9.2 proved that every defective unit square on a charged path has at least two bad quarters, which
removes the 4.5n ceiling when there are few bad rows. 9.5 asks: can a square with exactly two bad quarters occur deep inside a
degree-two region when all nearby crossings have overlap area 1/2 (no quarter-area crossings) and all nearby multiplicities are
at most two? Model: cells V = [-4,4]^2, all knight edges with an endpoint in V (other ends in [-6,6]^2), degree 2 on V and
<= 2 outside, cycles allowed, forbid pairs whose tiles share exactly one quarter, all quarter multiplicities <= 2, and exactly two
of the four quarters of the square [0,1]^2 with multiplicity != 1. Use the tile table of w-turnstheory/check_knight_tiles.py.
Run it with a SAT solver (pysat). If UNSAT, produce a DRUP proof and check it with the standalone checker
(w-verifier/claim10_runner/check_drup.py or your own). If SAT, save the witness and describe the local pattern.
Also try V = [-5,5]^2 if [-4,4]^2 is SAT, to see whether the answer is stable. Results to TILE_INPUTS.md section 8.
CPU: 1-2 cores. Hand off at about 50% context.
