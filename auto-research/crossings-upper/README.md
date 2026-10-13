# Track: crossings upper bound

Goal: closed tours with X <= cn + O(1) for some c < 19/3, for all large even n, with an all-size proof.

## Where the current bound comes from

The fold construction ([../../bounds-2026/CROSSINGS_PROOFS.md](../../bounds-2026/CROSSINGS_PROOFS.md) part A;
the crossings blog post explains it) pays:

- 4n for the U-turns at the four sides, 1 per row;
- n for the trapped loops near the side midpoints (flipped U-turns on a quarter of each side);
- 4n/3 for the corner imbalance, carried along the diagonal folds at 2/3 per column.

The sides already meet the lower bound, so a gain has to come from the other two terms or from a different layout.

## Known dead ends (2026 session; see the status labels in each file)

- The fold family: [../../bounds-2026/w-structures/FINDINGS.md](../../bounds-2026/w-structures/FINDINGS.md) S9 is
  a table of where it could still gain. In the space "line fields + free folds + measured seams + edge patterns",
  19n/3 is the minimum found ([../../bounds-2026/gap/structures/FINDINGS.md](../../bounds-2026/gap/structures/FINDINGS.md) G5).
- Jog bands do not give 16n/3 (w-structures/FINDINGS.md S8).
- Layout G is closed (gap/structures/FINDINGS.md G4, G6).
- Layout B'/B with shallow side edges is dead; midfold carriers cannot lower the flux term in the fold layout;
  the diagonal carrier rate 2/3 is certified optimal at widths 3 to 6 in its corridor model
  ([../../bounds-2026/gap/searcher/FINDINGS.md](../../bounds-2026/gap/searcher/FINDINGS.md), sections 0, 1 and 4).
- (1,2) walls: no gain below 19n/3 found (gap/searcher/FINDINGS.md section 8).

Structures that are not line fields were not explored. No candidate is known.

## What to submit

A tour family, its tour files for several sizes, an all-size argument, and an independent checker. Tours at a
few sizes with a low count are useful data, but they are not a new bound.
