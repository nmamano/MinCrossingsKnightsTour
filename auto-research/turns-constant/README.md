# Track: the additive constant for turns

Goal: narrow 8n - 24 <= T_min(n) <= 8n - 14 for even n >= 48. The upper bound is 8n - 17 for n = 2 mod 8 and
8n - 16 for n = 6 mod 8. The exact value may depend on n mod 8. This track has lower priority than the
crossings tracks: the leading term 8n is already exact.

## Starting points

- Lower bound: [../../bounds-2026/TURNS_LOWER24.md](../../bounds-2026/TURNS_LOWER24.md). Its section
  "Not proved" says that -24 is the limit of its method with a linear potential; a better bound needs a wider
  ring or a non-linear potential.
- [../../bounds-2026/gap/turnstheory/TURNS_GAP.md](../../bounds-2026/gap/turnstheory/TURNS_GAP.md): its
  section 1 states the exact slack, relative to 8n - 28, that a stronger bound must force. It also finds that a width-four ring with a
  free interior attains the old corner value, so a stronger model must keep inner endpoint loads and forced
  inner turns.
- Upper bound: the single-size tours in
  [../../bounds-2026/TURNS_SINGLE_SIZES.md](../../bounds-2026/TURNS_SINGLE_SIZES.md) beat the families at 12 sizes
  (for example 8n - 18 at n = 48). No all-size family below 8n - 14 is known for n = 0, 4 mod 8.
- Small boards: [../../bounds-2026/gap/structures/tmin/TMIN.md](../../bounds-2026/gap/structures/tmin/TMIN.md)
  has CP-SAT values of T_min(n) - 8n for small n (for example -20 at n = 14 and 16, -21 at n = 18). These are
  solver results. They are not in RESULTS.md.

The 2026 session already spent a significant effort on this gap without closing it. Explain what is new in
your approach.
