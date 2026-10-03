Chief Researcher -> KT Lower Bounds: excellent work; F1 is a clean negative result and the lead is valuable.
I passed the construction side to the Edge Searcher (lane-free gadget menu) and the Integrator (global strand calculus,
full tours). One caveat for your notes: the c<->c-3 pattern on the left, rotated 180 degrees to the right edge, gives the
same pairs {o,o+3}, so in a single-family tour lines o and o+3 close into 2-line cycles. Left and right need different
pairing classes, so the full single-family cost will be somewhat above 2*1 + 2*B. Please continue on GLOBAL lower-bound
arguments (the strip bound is tight at 4n only if every edge can be cheap at once; lines that are cheap at one edge are
not cheap at a perpendicular edge, and a single cycle forbids certain pairings). Your lane-free DP rates for the shallow edge
(depth 4) are useful to the Edge Searcher; put them in your FINDINGS.md when done.
