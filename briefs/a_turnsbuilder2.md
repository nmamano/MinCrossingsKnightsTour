Chief Researcher -> KT Turns Builder: good result. Your POST did not reach me (sandbox); that is expected, keep using files.
I am building full tours with T18 now (runs/t18/), so you do not need the Integrator for that.
Continue: (1) P=8 D=5: check whether the unroll window truncates long paths (use more periods, start tracing from the middle)
before you accept or reject; (2) P=16 and P=24 at D=4, D=5 with the lane rule, seeded with tiled T18 (AddHint) so you
always have 2.25; is 2.0 turns/col reachable? (3) lane-free gadgets (lanes=False in kt/search.build_model), recording each
gadget's line pairing as offsets; (4) the lexicographic version of the best: fixed min turns, then min crossings.
Write to w-turnsbuilder/FINDINGS.md and end your turn with a short summary. One CP-SAT worker only.
