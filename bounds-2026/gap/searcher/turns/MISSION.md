# Turns upper side: mission and state (KT Edge Searcher, 2026-10-04)

Mission (CR, from Nil, 2026-10-04): close the constant gap in TURNS: 8n - 28 <= T_min(n) <= 8n - 14 for even n >= 48.
I own the UPPER side. Goal: closed tours with fewer than 8n - 14 turns, and as a floor the best 2-factors
(no connectivity).
Starting point: TT16 recipe (w-integrator/FINDINGS.md section TT16; w-integrator/periodic.py, combos2.py,
corners/TT16_res{00,02,04,06}.json; corners were 6x6 zones solved turn-first with crossings as tie-break, so turns
may have room; side gadgets in w-integrator/gadgets/; Turns Builder heels in w-turnsbuilder/).
Steps:
- U1: for one n per residue mod 8 (56, 58, 60, 62), re-solve the corners with larger free zones (8x8, 10x10,
  12x12, plus free side bands near the corners), turns only, WITH connectivity (AddCircuit over contracted paths)
  and WITHOUT it (2-factor floor).
- U2: vary the side patterns and phases: all 12 slope-8 combos from combos2.py, and other 2-turns-per-column side
  patterns; the corner cost depends on how the side pattern meets the corner.
- U3: any improvement must extend to every even n >= 48 (period-in-n argument, as for TT16).
Facts: a single corner window cannot do better than -7 slack (w-turnstheory/corner_integer_large.py, OPTIMAL at
K = 8, 12, internal cycles forbidden); TT16 averages -3.5 per corner; target per corner between -7 and -3.5.
Lower Bounds (agent-1790897635493-c80g) computes the exact boundary-ring minimum and will send optimal ring
configurations as candidate corners; send it my best constructions too. Integrator (agent-1790897628991-tlfe) knows
the TT16 tooling. Report to CR (agent-1790895858902-etft): best T - 8n per residue, tours and 2-factors, dated.
Rules: write only under gap/searcher/ (this folder: gap/searcher/turns/); one heavy job; <= 8 GB with
gap/searcher/wall/run_wd.sh watchdog; CP-SAT num_workers <= 2; check uptime; no commits; ASD-STE100; hand off near 50%.

## State
- 2026-10-04: mission received; nothing run yet. Previous mission (beyond-5n flux) is stopped; see BEYOND5_FLUX.md.
