# Improved turn upper bounds for n = 2 and 6 (mod 8)

2026-10-04. For every even `n >= 48`:

- if `n = 2 (mod 8)`, there is a closed tour with exactly `8n - 17` turns, so `T_min(n) <= 8n - 17`;
- if `n = 6 (mod 8)`, there is a closed tour with exactly `8n - 16` turns, so `T_min(n) <= 8n - 16`.

For `n = 0, 4 (mod 8)` the best known tours are still TT16, with `8n - 14` turns ([TURNS_PROOFS.md](TURNS_PROOFS.md)).
The lower bound `8n - 28` of [TURNS_PROOFS.md, part C](TURNS_PROOFS.md#c-the-corner-certificate-and-8n---28) holds for every n.
No optimality is claimed. Audit: Claims 55b and 56 (below).

## Construction

The scheme is the scheme of TT16 ([TURNS_PROOFS.md, part D](TURNS_PROOFS.md#d-the-tours-complete-construction)), with
other side bands and larger corners. Move codes are those of part D.

1. **Interior.** Every cell gets code `26`, on the straight lines `x + 2y = c`.
2. **Bands, depth 4.** Bottom: cell `(x, y)`, `y = 0..3`, uses column `x mod 8` of row `y`.
   Top: cell `(x, n - 1 - y)` uses column `(-x) mod 8` of row `y`, with both moves negated.
   Left: cell `(x, y)`, `x = 0..3`, uses column `x` of row `y mod 4`.
   Right: cell `(n - 1 - x, y)` uses column `x` of row `(-y) mod 4`, with both moves negated.
   Left and right override bottom and top where they meet; the corners override both.
3. **Corners.** Each `8 x 8` corner square gets fixed moves that depend only on `n mod 16`.

Band templates (rows from the highest index to 0):

```
n = 2 mod 8                                   n = 6 mod 8
bottom  y\k  0  1  2  3  4  5  6  7          bottom  y\k  0  1  2  3  4  5  6  7
         3  26 26 26 26 26 26 26 26                   3  26 26 26 26 26 26 26 26
         2  46 36 26 26 46 26 46 26                   2  26 36 26 36 26 36 26 36
         1  25 26 25 25 26 26 25 26                   1  26 25 26 25 26 25 26 25
         0  16 16 67 06 16 06 16 06                   0  67 16 67 16 67 16 67 16
top     y\k                                   top     y\k
         3  26 26 26 26 26 26 26 26                   3  26 26 26 26 26 26 26 26
         2  26 46 26 46 36 26 36 26                   2  36 26 26 46 36 26 26 46
         1  25 26 26 25 26 25 25 26                   1  26 25 25 26 26 25 25 26
         0  06 16 06 16 16 67 16 67                   0  16 67 06 16 16 67 06 16
left    row\x 0  1  2  3                      left    row\x 0  1  2  3
         3  23 27 26 26                                3  23 27 26 26
         2  02 27 26 26                                2  23 24 26 26
         1  23 27 26 26                                1  23 27 26 26
         0  23 24 26 26                                0  02 27 26 26
right   row\x 0  1  2  3                      right   row\x 0  1  2  3
         3  02 24 26 26                                3  02 24 26 26
         2  02 27 26 26                                2  02 27 26 26
         1  02 24 26 26                                1  02 24 26 26
         0  23 24 26 26                                0  23 24 26 26
```

The corner moves are in the residue files `w-integrator/pipeline/ES_res2/res02.json`, `res10.json` and
`w-integrator/pipeline/ES_res6/res06.json`, `res14.json` (key `"<corner>:dx,dy"` = the cell at the corner anchor plus
`(dx, dy)`, anchors BL `(0,0)`, BR `(n,0)`, TL `(0,n)`, TR `(n,n)`; value = the two moves). The checker below rebuilds
every tour from these files and the templates; its function `graph` is the exact definition.
The base tours came from a CP-SAT search over periodic bands with subtour cuts (`gap/searcher/turns/`, tours in
`gap/searcher/turns/tours/res2/` and `res6/`).

## Every n: the same block insertion as TT16

The proof is the block insertion of [TURNS_PROOFS.md, part F](TURNS_PROOFS.md#f-one-closed-tour-for-every-n-block-insertion),
done by a general checker. Here the corner data repeat with period 16 in `n`, so the step is `n -> n + 16`: each of
the three blocks of 8 lines is replaced by three copies, and the checked identity is `M^3 = M`. Each step adds exactly
`128 = 8 * 16` turns: two periods of the bottom and of the top band (16 turns each) and four periods of the left and of
the right band (8 turns each). Every even `n` in
each class from the first size `>= 48` up to the induction base plus 16 is checked directly as a closed tour.

## Checks

The checker uses the Python standard library only:

```sh
python3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res2 --partial
python3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res6 --partial
python3 w-integrator/allsize_regress.py
```

The first two print `PASS: T(n) <= 8n + (-17)` and `PASS: T(n) <= 8n + (-16)` for the stated classes. `--partial`
means that the residue files cover only these classes, and the PASS line names them. The third runs the checker's
regression tests (bad inputs must be rejected).

The residue files can be rebuilt from the base tours (this step needs OR-Tools):

```sh
.venv/bin/python w-integrator/allpipe.py --tag ES_res2 gap/searcher/turns/tours/res2/n66.json \
    gap/searcher/turns/tours/res2/n74.json --extract 4,4,8,4 --A 8 --B 8 --period 16 --residues 2,10 --nmax 126
.venv/bin/python w-integrator/allpipe.py --tag ES_res6 gap/searcher/turns/tours/res6/n62.json \
    gap/searcher/turns/tours/res6/n70.json --extract 4,4,8,4 --A 8 --B 8 --period 16 --residues 6,14 --nmax 126
```

## Audit

- Claim 55b ([report](gap/verifier/claim55b_report.md)): the general checker is sound for families with a single
  straight interior field (not for mixed interior fields).
- Claim 56 ([report](gap/verifier/claim56_report.md)): PASS for both bounds, with independent reconstruction of every
  tour and the period-16 insertion certificates. Audited versions: `allsize_check.py` SHA-256
  `f3925853ab20f57416678ee81aa2b4322c7e5074fe4065ff3ef29730353bc5d6`, `allpipe.py`
  `2dfc8f14657e04ef2315d3cafa609d691ae59d7223675a00466a5c7f644316d8`.
