Chief Researcher -> KT Turns Builder: T16 is a great find (2 turns/col, proved optimal at P=8, D=4). With side edges at
2 turns/row it would give 8n + O(1) turns, matching the proven lower bound 8n - 28. The Integrator is now checking global
closure. Next task for you: a MENU of min-turn LEFT gadgets (kind 'left', lanes=False, Q in {4,8}, D in {2,3,4}), one entry per
pairing class you can force: pairs {c, c+d} with lower element of fixed parity for d in {1,3,5,7,9}, plus the unconstrained
optimum. For each entry: turns per row (is 2.0 reachable?), crossings per row as tie-break, the template, and the line
offsets. Write it to w-turnsbuilder/LEFT_MENU.md (format like w-searcher/MENU.md). One CP-SAT worker. End with a summary.
