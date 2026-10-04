# Single-size closed knight tours with few turns (KT Structures, 2026-10-04)

Each file in `tours/` is one closed tour on the n x n board, found by CP-SAT (tmin.py) with band copies and greedy
cycle merges (TMIN.md). These are single sizes, not a family for all n. General bounds: 8n - 28 <= T_min(n) <= 8n - 14
(even n >= 48).

Format: JSON with keys n, T, T_minus_8n, source, format, order. `order` is a list of n*n pairs [row, col], 0-based,
row 0 = top row. Consecutive pairs, and the last pair to the first, are knight moves. Every cell appears once.

Turn definition: a cell is straight if the move into it equals the move out of it (its two tour moves are opposite
vectors); otherwise it is a turn. T = number of turn cells.

Self-check (standard library, 2026-10-04): hash, board, permutation, knight moves, closure and T: PASS for all 14.
Independent audit: requested from the Verifier as Claim 58 (gap/verifier/claim58_report.md).

| n | n mod 8 | T | T - 8n | file | sha256 | source |
|---|---|---|---|---|---|---|
| 24 | 0 | 173 | -19 | `tours/tour_n24.json` | `7b89e8d78f34e5cee611520d0356ad7b55c40a861ef7d3dec2b3651df0ea1549` | `mrg/r24_2f_D4.json` |
| 28 | 4 | 206 | -18 | `tours/tour_n28.json` | `c9ac27c281436b529807a1df2f9fd443d1e6253f7d17596a30488c1cf1429dd5` | `desk/c28_P6_10_F15_37_c2.json` |
| 34 | 2 | 254 | -18 | `tours/tour_n34.json` | `7f4eae2b0c962e0e35d4d53485a1f36869d492aa55a530767ae9220b85a21a17` | `fam/q34_2f_P810_t0.json` |
| 38 | 6 | 286 | -18 | `tours/tour_n38.json` | `9483266460a1d43ede805ee363646b6310494b97e9ed3c74230107d8bd3cc4de` | `fam/c28_P6_10_F15_37_c2_t1.json` |
| 44 | 4 | 335 | -17 | `tours/tour_n44.json` | `0665ba8142c9b53ee5980e3f5b28a1141355aa7d7576ca63ad4411f5b4a013a5` | `fam/t24_P6_10_s1_t2.json` |
| 48 | 0 | 366 | -18 | `tours/tour_n48.json` | `30eede9b7b69da406be6b058cc182526cc956c74a93c0ae190289d157e4bea49` | `fam/c28_P6_10_F15_37_c2_t2.json` |
| 54 | 6 | 414 | -18 | `tours/tour_n54.json` | `20d848a115caabc5b66c4e433bed0ba7648650e6fe354a7ff391d5419d0bc696` | `fam/t24_P6_10_s1_t3.json` |
| 58 | 2 | 447 | -17 | `tours/tour_n58.json` | `d257fb99eb67d1c77a8684a049ef2d45b737d923c4c258299632220eafe170ca` | `fam/c28_P6_10_F15_37_c3_t3.json` |
| 64 | 0 | 497 | -15 | `tours/tour_n64.json` | `c5d28f21d71caa0beffab7ba269cb2584cdf536e17e2c0bc30c1edb8e8a3caae` | `fam/t24_P6_10_s1_t4.json` |
| 68 | 4 | 528 | -16 | `tours/tour_n68.json` | `881928bc166fd2ad4f7ddc8ef95f17f9dc9e72ab2141a9177e4e6a33916ebac7` | `fam/c28_P6_10_F15_37_c2_t4.json` |
| 74 | 2 | 574 | -18 | `tours/tour_n74.json` | `992c286416c1dd015212e4deac24c133013e2018d86c038d5e1ffd0e715056db` | `fam/c24_P6_10_F15_37_c2_t5.json` |
| 78 | 6 | 607 | -17 | `tours/tour_n78.json` | `53f6271e2d6325d4790e0daeaf53cfe1eaa1e5bd6aaf0859daef08ee909b1aba` | `fam/c28_P6_10_F15_37_c2_t5.json` |
| 88 | 0 | 689 | -15 | `tours/tour_n88.json` | `f4bdca92decc63dd455fe586c89dc76db709d7a9e4827d625695a9d2bf6866ca` | `fam/c28_P6_10_F15_37_c3_t6.json` |
| 98 | 2 | 768 | -16 | `tours/tour_n98.json` | `f1555538d34fb64662a10067537813ecdf5313def4ec057e43c6706454e7ae9a` | `fam/c28_P6_10_F15_37_c3_t7.json` |

Note: n = 24 is -19 here (merged from the D=4 2-factor optimum); the lane (a) report listed -18 for n = 24.
