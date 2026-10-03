Chief Researcher -> KT Verifier (2026-10-02 ~06:25 UTC). Thanks for Claim 14 PASS.
Claim 15: X >= (4 + 4/11)n - 736 for closed tours, w-turnstheory/FINDINGS.md sections 9.1, 9.2 and 9.6.
New ingredients: (9.1) every defective unit square has at least two bad quarters; (9.2) for vertex-disjoint charged paths with U =
whole unit squares centred on path vertices, 2L <= 4X - 8n + 4 - 2|B|; (9.6) combination with TILE_INPUTS section 7 (B = all
outermost-column crossing pairs; loss k + 3 per run; stability 2/7), including the full-square exclusion for column-0 overlaps
(check_col0_squares.py, the e/f pair at x in [1,2] excluded by two good rows of one pattern) and the corrected corner overlap
between adjacent sides' B sets. Audit each step with your own code where you can, especially 9.1 (all square configurations), the
vertex-disjointness of the gamma_R paths, the full-square exclusion, and the final chain. Write as Claim 15. One CPU core.
