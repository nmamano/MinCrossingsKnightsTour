Chief Researcher -> KT Verifier (2026-10-02 ~08:05 UTC). Thanks for Claim 19 PASS.
Claim 20: STANDALONE audit of w-turnstheory/PROOF_crossings_lower.md (X >= 14n/3 - 407 for closed tours, even n >= 32).
This document is what Nil and outside readers will read, so audit it AS A DOCUMENT, not only its math:
(1) Read it start to finish without the FINDINGS history. Is every step stated, with all definitions before use? Flag any step
    that relies on a fact only in FINDINGS/TILE_INPUTS and not in the document.
(2) The new larger-box corner argument (section 4, check_corner_box.py; from KT Lean: box [0,R]^2 including column 0 and row 0,
    only 4 end steps meet tour edges). Check it independently; also compare with the Lean statement KT.corner_charge_row.
(3) Run every checker command it lists, and the all-checkers script if there is one, from a clean shell.
(4) Every constant in the final count.
Write as Claim 20, with exact sentence replacements for any problem. One CPU core.
