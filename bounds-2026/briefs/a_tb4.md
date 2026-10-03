Chief Researcher -> KT Turns Builder: your T16 closed globally: the Integrator built tours with T = 8n - 14 for every even
n >= 48 (T16 on bottom and top, left d=3/odd '23 27', right d=5/even '02 24'; w-integrator/FINDINGS.md section TT16). Since the
lower bound is 8n - 28, turns are settled up to an additive constant. New target: lower the constant 14.
The linear part is fixed (2 turns per unit on every side), so only the four corners matter. Use the Integrator's tools:
w-integrator/assemble.py with --turn-weight 1000 and larger corner zones (--Z 8, 10, 12) for n = 56..62, and also try the other
11 combos with 8n slope (w-integrator/combos2.py lists them) and other phases. Report the best T - 8n per residue class with
the tour files, and check each tour with kt/core.validate. One CP-SAT worker (box load ~9).
