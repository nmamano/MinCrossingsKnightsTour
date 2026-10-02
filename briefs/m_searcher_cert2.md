Chief Researcher -> KT Edge Searcher (2026-10-02 ~05:05 UTC). PRIORITY CHANGE.
The headline lower bound is now X >= (4 + 1/17)n - O(1) for closed tours (w-turnstheory/FINDINGS.md section 7 +
w-lowerbounds/TILE_INPUTS.md sections 2-3). It does NOT use the M3 / NE-M3 window lemmas. If your current certify2 run is
within ~10 minutes of a result, finish it and record it; otherwise park it with a note in your FINDINGS.md.
New task: an independent C++ certification (3rd method, your own code, no reuse of their Python) of the finite inputs that
section 7 does use:
 (1) the width-2 strip graph (w-lowerbounds/strip_dp.py: 82,516 states, 144,674 arcs): build it from the definition yourself and
     check the state and arc counts, the two tight cycles, and the stability statement (S): with integer weights
     20w - 5 - 4[non-cycle arc] there is no negative cycle (potential in [-149, 0]), and with 201/1000 in place of 1/5 there is one;
 (2) the corner endpoint charge lemma (w-turnstheory/check_corner_endpoint_charge.py, FINDINGS section 7.3);
 (3) the strip row certificate (w-turnstheory/check_strip_row_certificate.py, section 7.1).
Read the definitions in their files, not their code paths. Report mismatches at once to me. Results to w-searcher/FINDINGS.md.
One heavy job at a time, 1-2 cores.
