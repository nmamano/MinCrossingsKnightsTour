# Turn lower bound 8n - 24

2026-10-04. **For every n >= 20, every spanning knight 2-factor of the n x n board has at least 8n - 24 turns.**
Every closed tour is a 2-factor, so every closed tour has `T >= 8n - 24`. With the tours of
[TURNS_IMPROVED.md](TURNS_IMPROVED.md) and [TURNS_PROOFS.md](TURNS_PROOFS.md), for every even `n >= 48`:

| n mod 8 | Lower bound | Upper bound |
| --- | --- | --- |
| 2 | 8n - 24 | 8n - 17 |
| 6 | 8n - 24 | 8n - 16 |
| 0, 4 | 8n - 24 | 8n - 14 |

The older bound `T >= 8n - 28` ([TURNS_PROOFS.md, part C](TURNS_PROOFS.md#c-the-corner-certificate-and-8n---28))
stays: it holds for every `n >= 8` and has an unconditional Lean proof. The new bound has no Lean proof.
Audit: Claim 57 ([report](gap/verifier/claim57_report.md)), PASS. The proof is from KT Lower Bounds
([L1.md, section 1b](gap/lowerbounds/turns_ring/L1.md)); the audit replaced its large computations with smaller
exact checks (below).

## The inequality chain

For a cell v, `t(v)` is 1 if the 2-factor turns at v, else 0. `L(v)` is the sum of the four side contributions of the
paper. For one side, with inward distance `i` of v and the distances of its two neighbors to that side:

```text
L0 = 1
L1 = L2 = (number of neighbors at distance 0 or 3) - 1
L3 = 1 - (number of neighbors at distance 1 or 2)
Li = 0 for i >= 4
```

For a 2-factor, one side gives exactly `2n` (the terms between depths 1, 2 and depth 3 cancel; the rest counts the
edges into depth 0). So `sum L = 8n`, and with the residual `r = t - L`:

```text
T - 8n = sum of r over all cells
       >= R6(n)              (cells at depth >= 6 have r = t >= 0; drop the interior)
       >= 4 * (corner value)  (side potential and telescoping, below)
       >= -24.
```

`R6(n)` is the minimum residual sum over the width-6 ring relaxation: every cell at depth < 6 chooses two legal moves,
choices are reciprocal between ring cells, and a move into the interior is free at its other end. This only removes
constraints, so it can not raise the minimum. No connectivity is used.

## The side potential

Cut the side strip (depths 0..5) between two rows. The 28 slots are the knight edges with both ends in the strip that
cross the cut ([slot list](gap/lowerbounds/turns_ring/z6/z6_slots.txt)). Orient a slot edge from its lower end to its
upper end. Its weight is +1 if both ends are at depth 3..5 and the upper end is shallower, -1 if both ends are at depth
3..5 and the upper end is deeper, else 0. `H(c)` is the sum of the weights of the chosen edges that cross cut `c`.
In slot order, `w = +1` on slots 8, 9, 25, 26, 27 and `w = -1` on slots 5, 7, 19, 20, 23.

**Row inequality.** For every row and for both scales `S = 3` and `S = 6`:

```text
S * (row cost) + H(incoming cut) - H(outgoing cut) >= 0.
```

Proof: `H(in) - H(out)` is a sum over the cells of the row of a local term `D_x` (an edge that passes the row without
an end there is in both cuts and cancels). For each depth `x`, the minimum of `S * r_x + D_x` over all 133 legal move
pairs is `0, 0, 0, 1, 0, -1` for `x = 0..5`. These sum to 0. The proof does not use consistency between cells, so it
holds for every strip transition.

## The corner certificate

The corner region with arm length `A` is `{(x, y): 0 <= x, y < A, min(x, y) < 6}`. Its reduced cost is
`S * (residual sum) - H(s) + H(sigma(t))`, where `s` and `t` are the states of its two arm cuts and `sigma` is the row
mirror `(x0, y0, x1, y1) -> (x1, -1 - y1, x0, -1 - y0)`.

| A | S | Certificate lower bound | Equality case | Proved corner value | Witness |
| --- | --- | --- | --- | --- | --- |
| 10 | 6 | -38 | impossible (complete search, 15 nodes) | -37/6 | -37/6 |
| 14 | 3 | -19 | impossible (33 nodes) | -6 | -6 |
| 20 | 3 | -19 | impossible (33 nodes) | -6 | -6 |

Each lower bound is a sum of integer local inequalities (1,693, 2,757 and 4,353 of them), checked in exact arithmetic.
The equality case is excluded by a complete search, and integrality then gives the value one higher. A checked witness
attains each value, so these are the exact corner minima.

**Telescoping.** For `n >= 2A`, the four rotated corners and the four side rectangles partition the ring. On each side
the row inequalities sum to `side cost >= (H(sigma(t_next)) - H(s)) / S`; the far end of a side is `sigma` of the next
corner's state for every n (a coordinate identity). The boundary terms move into the four corner objectives, so
`R6(n) >= 4 * (corner value)`. With `A = 10, S = 6`: `R6(n) >= -74/3` for every `n >= 20`, and `R6(n)` is an
integer, so `R6(n) >= -24`. (`A = 14` gives `-24` directly for `n >= 28`.)

## Checks

Exact checks, Python standard library only, from the bounds-2026 folder (each takes seconds):

```sh
python3 gap/verifier/claim57_local.py
python3 gap/verifier/claim57_frames.py
python3 gap/verifier/claim57_corner_exact.py 10 6
python3 gap/verifier/claim57_corner_exact.py 14 3
python3 gap/verifier/claim57_corner_exact.py 20 3
python3 gap/verifier/claim57_witness_check.py
```

They check, in order: the row inequality for both scales; the slots, the mirror, the row identity, the ring partition
and the joins; the three corner certificates with the equality-case search; the three witnesses. The inputs are in
[gap/verifier/claim57_run/](gap/verifier/claim57_run/) (snapshots of the potential and slot files, with SHA-256 hashes
in `source_manifest.json`, and the integer certificates `corner_A*_S*_dual.json`).

The original computations of L1.md section 1b are not needed for the proof. They use OR-Tools (and NumPy), from
`gap/lowerbounds/turns_ring/`:

```sh
python3 certcheck.py 6 14 z6/cert_A14_w.txt 600     # corner value -6 at A = 14 (CP-SAT, 4 settings)
python3 certcheck.py 6 10 z6/cert_A10_w.txt 600     # corner value -37/6 at A = 10
python3 verify_frames.py 28 6 14                    # frames on a real ring solution
```

The strip-graph validity check of L1.md (`stripz.cpp`, 38.8 million states, about 5.4e9 arcs) is replaced by the
133-pair row inequality above.

## Not proved

- `R6(n) >= -24` is the limit of this method with a linear potential: the LP over all slot weights reaches exactly
  -6 per corner (L1.md). A better bound needs a wider ring or a non-linear potential.
- No bound below `n = 20` beyond `8n - 28`, and no claim that `-24` is tight for tours.
