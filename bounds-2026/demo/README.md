# Interactive demo of the knight's tour constructions (KT Integrator, 2026-10-02)

Static page, no build step: `index.html`, `demo.css`, `tourlib.js` (decode + checks), `app.js` (UI),
`data/` (one JSON per tour, loaded lazily, 10-45 KB each; `data/summary.json` has all counts).
Served as the isomux app `knight-demo` (`serve.py`: listens on `$PORT`, binds `$ISOMUX_APP_HOST`).

## Progression shown (Measure: crossings | turns; a step slider and list)
Crossings: orig 13n -> paper (Parker Williams heel) 12n -> P40 (Shisheng Li) 11.5n -> H16a 9n -> LF4 343n/48 -> FOLD 19n/3.
Turns: orig 9.5n -> heel21 (Parker Williams turn heel) 9.25n -> T18 8.5n -> TT16 8n - 14.
Chart lower bounds: crossings 4n (paper), 24n/5 (ours, Claim 31, 2026-10-03; was 14n/3, then 204n/43); turns 6n (paper), 8n - 28 (ours).

| key | n (even) | crossings | turns | audit |
| --- | --- | --- | --- | --- |
| orig | 48..200 | 13n + c | 19n/2 + c | reproduces published numbers |
| paper | 48..200 | 12n + c | 19n/2 + c | reproduces 12n; heel figure in Verifier Claim 21 |
| heel21 | 48..200 | 51n/4 + c | 37n/4 + c | reproduces 9.25n; heel rebuilt (see below) |
| P40 | 48..200 | 23n/2 + c | 39n/4 + c | reproduces 11.5n |
| H16a | 48..200 | 9n + c | 41n/4 + c | Verifier Claims 1, 4, 7 |
| LF4 | 96..200 | 343n/48 + c | 43n/4 + c | Verifier Claim 8 |
| FOLD | 96..200 | 19n/3 + c | 38n/3 + c | Verifier Claim 12 |
| T18 | 48..200 | 51n/4 + c | 17n/2 + c | Verifier Claims 3, 4 |
| TT16 | 48..200 | 19n/2 + c | 8n - 14 | Verifier Claims 6, 7 |
Slopes are exact over the data (one value for every n -> n + period; build logs 2026-10-02).

## The paper's 21-turn heel (heel21)
No file had its move codes (paper Figure 11 shows it only as a picture). `w-integrator/heel21.py` rebuilds it:
CP-SAT on the periodic bottom strip (P = 8, D = 4), the exact line pairing of the paper heels, the moves across
the 8-column boundary equal to Sequence1Opt, objective turns then crossings. Result OPTIMAL: 21 turns, 31
crossings per 8 columns, as in the paper. Template in `w-integrator/gadgets/heel21.json`. Without the boundary
rule the same search finds 20 turns / 24 crossings per period, but that heel is not a drop-in for Algorithm 1.

## Data and checks
- `../.venv/bin/python demo/build_data.py [--keys ...] [--nmin --nmax] [--jobs 2] [--brute 96,98,120]`
  rebuilds every tour from the verified recipes (no new CP-SAT solve): H16a = period24.apply_zone with
  corners/H16a_VE_res*.json; TT16 = periodic.Combo with corners/TT16_res*.json (n = 48..54 from
  w-integrator/tours/TT16_n*.json); FOLD = the fold_period.py transplant from corners/FOLD24_base_n{96..118}.json;
  orig/paper/heel21/P40 = kt.gentour.gen_tour with that heel or block; LF4 = periodic.Combo with
  w-turnstheory/lf-corners/LF4_res*.json; T18 = period24.apply_zone with corners/T18_res*.json. Each tour: kt.core.validate + assemble.walk_check, counts by kt.core,
  and assemble.brute_crossings (all pairs) at n = 96, 98, 120. About 9 minutes with 2 processes.
- `node demo/check.js`: an independent JS check (tourlib.js) of every data file: one closed tour, and
  the JS crossing and turn counts equal the Python counts. The page runs the same check on every tour it shows.
- Result 2026-10-02: 645 tours (FOLD and LF4 53 each, others 77 each), all valid, 0 count mismatches, brute force agrees.
  FOLD is now checked for every even n up to 200 (before: n <= 166).

## Note on the Algorithm 1 tours
Our port of Algorithm 1 with an optimised heel (Sequence1Opt, heel21) runs off the board for
n = 2 mod 4 (top-left corner case 1) and n = 6 mod 8 (bottom-right corner case 1). In those two corner
pieces the demo uses the board.js default heel (Sequence1Default), an O(1) change. All n are then valid.

## URL state
`#m=X&k=H16a&n=96&view=edge&show=cross,turns,color,layout,solver` (m = X or T) opens a given view (view: fit, edge, corner, centre).

## Credits shown (decided by Nil, 2026-10-02)
Original step: Besa, Johnson, Mamano, Osegueda (2019). Parker Williams steps: January 2022. Shisheng Li: May 2026.
Our steps: Agent Team, October 1, 2026 (Pacific).

## Audit
KT Verifier Claim 22 (w-verifier/FINDINGS.md, 2026-10-02): tour data PASS; its display and caption replacements are applied.
