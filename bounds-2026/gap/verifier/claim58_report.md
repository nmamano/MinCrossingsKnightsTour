# Claim 58: single-size tour certificates

Date: 2026-10-04. Verdict: **PASS for all 14 entries.**

I checked the supplied files with `claim58_check.py`, a new independent Python standard-library checker. It imports no project code and does not use `kt.core` or a solver.

For each entry, the checker verifies the SHA-256 against the manifest, exact integer board size, exactly n² coordinate pairs, integer coordinates inside the board, and coverage of every board cell exactly once. It checks all n² knight moves, including the closing edge. Thus the listed order is one closed Hamiltonian cycle, rather than a union of cycles.

At cyclic index i, write d_i = v_(i+1) - v_i. The checker counts a turn exactly when d_(i-1) differs from d_i, including both ends of the list. This is the requested definition and the Claim 56 definition. A second recount uses the nonzero determinant of successive moves; the two counts agree in every file. The checker compares T and T - 8n against both the manifest and the tour JSON.

| n | Cells and cyclic edges | Recounted T | T - 8n | Hash | Verdict |
|---:|---:|---:|---:|:---:|:---:|
| 24 | 576 | 173 | -19 | PASS | PASS |
| 28 | 784 | 206 | -18 | PASS | PASS |
| 34 | 1156 | 254 | -18 | PASS | PASS |
| 38 | 1444 | 286 | -18 | PASS | PASS |
| 44 | 1936 | 335 | -17 | PASS | PASS |
| 48 | 2304 | 366 | -18 | PASS | PASS |
| 54 | 2916 | 414 | -18 | PASS | PASS |
| 58 | 3364 | 447 | -17 | PASS | PASS |
| 64 | 4096 | 497 | -15 | PASS | PASS |
| 68 | 4624 | 528 | -16 | PASS | PASS |
| 74 | 5476 | 574 | -18 | PASS | PASS |
| 78 | 6084 | 607 | -17 | PASS | PASS |
| 88 | 7744 | 689 | -15 | PASS | PASS |
| 98 | 9604 | 768 | -16 | PASS | PASS |

## Reproduction and evidence

Run from the repository root:

```sh
python3 gap/verifier/claim58_check.py
```

Full file paths, checked SHA-256 values, and results are in [claim58_results.json](claim58_results.json). The checker is [claim58_check.py](claim58_check.py).

Manifest: `gap/structures/tmin/single_tours.json`.
Manifest SHA-256: `1d51c280e73dc4819b11ebcd261cc5de0fb56f4624502033865fa2ea220233ed`.

These certificates prove T_min(n) is at most the recounted T at each listed size. They do not establish optimality or an extension to other sizes.
