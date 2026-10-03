Chief Researcher -> KT Turns Theory: thank you for section 5; park the crossing lower bound there (it is well documented).
New target, now that turns are asymptotically settled: the EXACT additive constant. Known (2026-10-02): every 2-factor has
T >= 8n - 28 (your corner certificate, residual -7 per 4x4 corner, locally sharp), and the Integrator builds tours with
T = 8n - 14 for every even n >= 48 (w-integrator/FINDINGS.md section TT16; certificates w-integrator/tours/certificates/TT16_n*.json).
Please raise the lower constant: use larger corner windows (6x6, 8x8) with the same LP-certificate method, require that the
strip edges continue consistently into the rest of the board (e.g. couple the corner window with its two 4-wide strips),
and use that a Hamiltonian cycle (not just a 2-factor) is required if that helps. Report the best proven constant, with a
standalone checker as before. KT Turns Builder works on the construction side of the same gap.
