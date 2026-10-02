Chief Researcher -> KT Turns Builder (steer): CHANGE OF TASK. Nil does not care about the additive constants (14, 28), so drop
the corner-constant work. Turns are done asymptotically (8n). Please move to CROSSINGS.
Current crossing record: 173n/24 ~ 7.21n (lane-free: bottom free 11/6, top 19/8, left d=5/even 2, right d=3/odd 1 per unit).
One of two remaining levers is yours: a LEFT-type gadget that is a MID partner of right d=3/odd (pairs {o,o+3}, o odd) and costs
below 2.0 crossings per row. Known MID partners: d=1/even (2.0/row at best so far), d=5/even (2.0/row), d=7/odd. Search with
kt/strip.py + kt/search.py (kind 'left', lanes=False, crossings objective), Q in {4,8,12}, D in {2..5}, and accept a gadget only if
w-integrator/strands.py region_check reports no finite cycle and even cut parity in MID against d=3/odd (ask nothing; read
the code: pairing(tpl,'left'), region_check). Mixed pairings (not a single d) are allowed and are where gains may be. The Edge
Searcher works on the top-type lever, so stay on left-type gadgets. One CP-SAT worker. Write results to w-turnsbuilder/FINDINGS.md
(new section) with templates; end your turn with a short summary.
