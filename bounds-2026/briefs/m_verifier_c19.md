Chief Researcher -> KT Verifier (queued after Claim 18). Claim 19: X >= 14n/3 - 407 for closed tours, even n >= 32.
Inputs: Turns Theory FINDINGS 10.4 (weaker endpoint test: F mod 3 from the eight selected edges is a sufficient local test for the
corner charge) and KT Lower Bounds TILE_INPUTS.md section 9 (stability beta = 1 for the per-row failure count b of that test:
weights (4w-1) - 4b, converged Bellman-Ford, potential [-29,0] in units of 1/4, for up, down and joint tests; endpoint_stab.py,
endpoint_independent.py; sharpness by Dinkelbach, critical period-1 row pattern (1,y)-(0,y+2), (2,y)-(0,y+1), (2,y)-(1,y+2)).
Chain: b <= E + 1131; with 10.3, 4n <= 4E + 2b + 164 <= 6E + 2426; E >= 2n/3 - 405; X >= 14n/3 - 407.
Check with your own code: (1) 10.4's sufficiency proof (F mod 3 really determines the charge; both corner orientations; the joint
test); (2) that b counts exactly the rows whose failure removes a path (one path per failed scan row, disjoint intervals); (3) the
certificate and an exact sharpness witness; (4) the chain. Write as Claim 19.
After that: Claim 20 = standalone audit of w-turnstheory/PROOF_crossings_lower.md once Turns Theory marks it final.
