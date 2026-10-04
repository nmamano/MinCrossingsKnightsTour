# Closed tours with few turns at single sizes

2026-10-04. Each file below is one closed knight's tour on the n x n board, found by KT Structures. Each tour proves
`T_min(n) <= T` at its own size only. These are upper bounds at single sizes: they are not claimed optimal, and they are
not families (no all-size construction comes with them).

They show that `8n - 14` is not the true minimum for `n = 0, 4 (mod 8)`: for example, at `n = 48` there is a tour with
`8n - 18` turns.

| n | n mod 8 | T | T - 8n | File | Best general bound at this n (RESULTS.md) | Better? |
| ---: | ---: | ---: | ---: | --- | --- | --- |
| 24 | 0 | 173 | -19 | [tour_n24.json](gap/structures/tmin/tours/tour_n24.json) | no general bound below 48 | - |
| 28 | 4 | 206 | -18 | [tour_n28.json](gap/structures/tmin/tours/tour_n28.json) | no general bound below 48 | - |
| 34 | 2 | 254 | -18 | [tour_n34.json](gap/structures/tmin/tours/tour_n34.json) | no general bound below 48 | - |
| 38 | 6 | 286 | -18 | [tour_n38.json](gap/structures/tmin/tours/tour_n38.json) | no general bound below 48 | - |
| 44 | 4 | 335 | -17 | [tour_n44.json](gap/structures/tmin/tours/tour_n44.json) | no general bound below 48 | - |
| 48 | 0 | 366 | -18 | [tour_n48.json](gap/structures/tmin/tours/tour_n48.json) | 8n - 14 | yes |
| 54 | 6 | 414 | -18 | [tour_n54.json](gap/structures/tmin/tours/tour_n54.json) | 8n - 16 | yes |
| 58 | 2 | 447 | -17 | [tour_n58.json](gap/structures/tmin/tours/tour_n58.json) | 8n - 17 | no, equal |
| 64 | 0 | 497 | -15 | [tour_n64.json](gap/structures/tmin/tours/tour_n64.json) | 8n - 14 | yes |
| 68 | 4 | 528 | -16 | [tour_n68.json](gap/structures/tmin/tours/tour_n68.json) | 8n - 14 | yes |
| 74 | 2 | 574 | -18 | [tour_n74.json](gap/structures/tmin/tours/tour_n74.json) | 8n - 17 | yes |
| 78 | 6 | 607 | -17 | [tour_n78.json](gap/structures/tmin/tours/tour_n78.json) | 8n - 16 | yes |
| 88 | 0 | 689 | -15 | [tour_n88.json](gap/structures/tmin/tours/tour_n88.json) | 8n - 14 | yes |
| 98 | 2 | 768 | -16 | [tour_n98.json](gap/structures/tmin/tours/tour_n98.json) | 8n - 17 | no, 8n - 17 is lower |

The general bounds are the all-size constructions for even `n >= 48`: `8n - 14` (TT16, [TURNS_PROOFS.md](TURNS_PROOFS.md))
and `8n - 17` (`n = 2 mod 8`), `8n - 16` (`n = 6 mod 8`) ([TURNS_IMPROVED.md](TURNS_IMPROVED.md)). The lower bound at
every listed size is `8n - 24` ([TURNS_LOWER24.md](TURNS_LOWER24.md), every `n >= 20`).

## Format and check

Manifest: [gap/structures/tmin/single_tours.json](gap/structures/tmin/single_tours.json) (n, T, T - 8n, file, SHA-256).
Each tour file is JSON with `n`, `T`, `T_minus_8n` and `order`, the list of the `n^2` cells `[row, col]` (0-based) in
cyclic order. A cell is a turn unless its two tour moves are opposite vectors.

Audit: Claim 58 ([report](gap/verifier/claim58_report.md)), PASS for all 14 tours. The checker uses the Python standard
library only and imports no project code. For each tour it checks the hash, that every cell is visited exactly once,
that all `n^2` moves (with the closing move) are knight moves, and it counts the turns twice (equal consecutive moves;
nonzero determinant). From the bounds-2026 folder:

```sh
python3 gap/verifier/claim58_check.py
```

Results: [claim58_results.json](gap/verifier/claim58_results.json).
