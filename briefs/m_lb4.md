Chief Researcher -> KT Lower Bounds: thank you, F7-F9 are clear and useful. I choose (b), but as a separable sub-problem so you
and KT Structures do not edit the same construction:
YOUR TASK: the colour-flux transport cost. Structures has the fold field at 5n + const with 32 path components (no closed cycles),
and the remaining obstacle is the corner colour imbalance (you measured total 4; Structures sees +-1 per corner window).
Find the cheapest way to carry one unit (and two units) of colour flux over a long distance L inside the fold field, per unit
length, along every candidate route: a board edge (inside the cheap U-turn pattern), a diagonal fold line, a midline fold,
and through the interior lines. Use a periodic corridor model (translation along the route, a band of constant width free,
the field fixed outside, degree 2 everywhere in the band, flux = signed black/white edge balance across a transverse cut).
Report the min crossings per unit length for each route and flux value, with the corridor template. If some route costs o(1)
per unit (e.g. a zero-cost corridor), the fold design gives about 5n; if every route costs >= c, you also get a statement in
the direction of (ii) for your notes. Send corridor templates to Structures (agent-1790897635740-iq1g) directly and copy me.
2 CP-SAT workers max.
