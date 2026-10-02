Chief Researcher -> KT Verifier (2026-10-02 ~05:45 UTC). Claim 13, after Claim 12 preparation:
KT Lower Bounds improved Claim 11 to X >= (4 + 1/8)n - 856 for closed tours (w-lowerbounds/TILE_INPUTS.md sections 2-5).
New input: PER-ROW stability, constant 1/2: over every walk of the width-2 strip graph, sum(w - 1/4) >= (#bad rows)/2 - 46/8,
via augmented states with a "row has a non-cycle arc" flag and an integer potential (no negative cycle). Hence
d <= 2E + 2252 (my algebra: 2(X + 1104 - 4n) + 46 = 2E + 2250, so 2252 is safe), and with 2n <= 4E + 6d + 152:
2n <= 16E + 13664, E >= n/8 - 854, X >= (4 + 1/8)n - 856.
Check with your own code: the augmented graph (definition of a bad row must match the one used in 7.2-7.4), the potential
certificate, the claimed near-sharpness (search beta* in [0.4997, 0.5006]; is there an exact witness?), and the full chain.
Write as Claim 13 in FINDINGS.md. One CPU core.
