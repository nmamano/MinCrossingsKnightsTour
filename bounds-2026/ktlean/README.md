# ktlean: machine-checked lower bounds on the turns and crossings of closed knight's tours

Lean 4 + Mathlib (toolchain `leanprover/lean4:v4.35.0-rc3`, Mathlib `v4.35.0-rc3`).

## Main theorem (proved, no `sorry`, no new axioms)

```lean
theorem KT.ClosedTour.eight_mul_sub_28_le_numTurns (T : ClosedTour n) (hn : 8 ≤ n) :
    8 * n - 28 ≤ T.numTurns
theorem KT.TwoFactor.eight_mul_le_numTurns_add_28 (F : TwoFactor n) (hn : 8 ≤ n) :
    8 * n ≤ F.numTurns + 28
```

Every closed knight's tour (and every 2-factor of the knight's graph) of the n × n board, n ≥ 8,
has at least 8n - 28 turns. This proves the paper's conjecture (a leading factor of 8) with the
constant of `writeup/turns/main.tex`, Theorem 1(a). The best known upper bound is 8n - 14 (TT16,
every even n >= 48). The earlier, weaker bound `KT.ClosedTour.eight_mul_sub_64_le_numTurns`
(8n - 64, no corner certificate) is still in the project.

`#print axioms` gives only the standard axioms: `propext`, `Classical.choice`, `Quot.sound`.

## Second theorem: crossings (proved, no `sorry`, no new axioms)

```lean
theorem KT.ClosedTour.four_mul_sub_two_le_numCrossings (T : ClosedTour n) :
    4 * n - 2 ≤ T.numCrossings
theorem KT.TwoFactor.four_mul_sub_two_le_numCrossings (F : TwoFactor n) :
    4 * n - 2 ≤ F.numCrossings
```

Every closed knight's tour (and every 2-factor of the knight's graph) of the n × n board has at
least 4n - 2 crossings, for every n. `#print axioms` gives only `propext`, `Classical.choice`,
`Quot.sound`.

## Definitions (file `Ktlean/Basic.lean`; this is all a reader must check)

- `Cell n := Fin n × Fin n`, a cell is `(x, y)`.
- `disp u v : ℤ × ℤ` is the vector `v - u`.
- `IsKnightMove u v`: `(|dx| = 1 ∧ |dy| = 2) ∨ (|dx| = 2 ∧ |dy| = 1)` for `(dx, dy) = disp u v`.
- `ClosedTour n`: a bijection `cell : Fin (n * n) ≃ Cell n` (the i-th visited cell; every cell
  exactly once) such that `cell i` and `cell (finRotate _ i)` are a knight's move apart for
  every `i`. `finRotate` is the cyclic successor (`i ↦ i + 1`, last ↦ `0`), so the tour is closed.
- `Collinear3 a b c`: the cross product of `b - a` and `c - a` is `0`.
- `ClosedTour.IsTurn T i`: `cell (i - 1)`, `cell i`, `cell (i + 1)` (cyclic) are not collinear.
  This is Definition 1 of Besa–Johnson–Mamano–Osegueda–Williams.
- `ClosedTour.numTurns T`: the number of positions `i` with `IsTurn T i`.
- `OpenSegmentsMeet a b c d`: the open segments `(a, b)` and `(c, d)` of the real plane
  intersect (Mathlib's `openSegment ℝ`).
- `ClosedTour.numCrossings T`: the number of pairs of positions `i < j` such that the moves
  `cell i → cell (i+1)` and `cell j → cell (j+1)` have intersecting open segments
  (Definition 2 of the paper).
- `TwoFactor.numCrossings F`: the number of sets `{e, f}` of two distinct edges of `F.graph`
  (a Mathlib `SimpleGraph`) whose open segments intersect.

## Also proved

- `KT.TwoFactor.eight_mul_le_numTurns_add`: the same bound `8 * n ≤ F.numTurns + 64` for every
  2-factor of the knight's graph (every cell has two chosen knight neighbours, symmetric; any
  number of cycles). A turn of a 2-factor is a cell whose two moves are not opposite.
- `KT.Example.tour8`: an explicit closed tour of the 8 × 8 board, and
  `KT.Example.tour8_numTurns : tour8.numTurns = 61` (checked by `decide +kernel`; Python gives
  61 too). This shows that `ClosedTour` is not empty, so the main theorem is not vacuous.

## Proof structure

1. `Ktlean/Strip.lean`, `KT.strip_lemma`: the four-column lemma in abstract form. A 2-regular
   symmetric graph with a column function `c ≥ 0` (each edge changes `c` by 1 or 2, a non-turn
   `v` has neighbours `u, w` with `c u + c w = 2 c v`) and `m` vertices in each column 0..3 has
   at least `2m` turns in columns 0..3. Proof: T0 = m; T1 + T2 ≥ B; T3 ≥ m - B, from the local
   inequalities t ≥ p - 1 and t ≥ 1 - q and double counting of edges.
2. `Ktlean/TwoFactor.lean`: apply the lemma with `c` = distance to each of the four sides (no
   symmetry argument is necessary). Opposite strips are disjoint for n ≥ 8; two crossing strips
   share at most 64 cells (the four 4 × 4 corners). So 8n ≤ turns + 64.
3. `Ktlean/Tour.lean`: a closed tour gives a 2-factor (predecessor and successor) with the same
   turns. For knight moves, "not collinear" is the same as "the two moves are not opposite",
   because two parallel knight vectors are equal or opposite.

Crossings (tile argument of KT Turns Theory, FINDINGS.md sections 6.1 and 6.4):

4. `Ktlean/Tiles.lean`: each unit square is cut by its diagonals into 4 quarter triangles. The
   tile of a knight edge is an explicit set of 4 quarter triangles in the edge's bounding box.
   Finite certificate (`decide +kernel`, all relative positions in `[-3, 3]²` and all 64 pairs
   of directions): the tiles of two distinct edges share at most 2 quarter triangles, and share
   one only if the edges cross properly (strict integer orientation tests). Edges further apart
   have disjoint tiles (proved from the bounding boxes).
5. `Ktlean/CrossCore.lean`: counting. With `m_t` the multiplicity of quarter triangle `t`:
   `Σ m_t = 4n²`, `Σ m_t² = 4n² + Σ_{e≠f} |tile e ∩ tile f| ≤ 4n² + 2Y` (`Y` = ordered properly
   crossing pairs), and `3m ≤ 2 + m²`. The board has `4(n-1)²` quarter triangles, so `Y ≥ 8n - 4`.
   Also: a proper crossing makes the two real open segments intersect.
6. `Ktlean/Crossings.lean`: apply this to the `n²` moves of a tour (distinct as unordered
   pairs) and to the `n²` edges of a 2-factor (handshake lemma); each crossing pair is counted
   twice in `Y`.

Constant 28 (corner certificate, Lemma 3 of `writeup/turns/main.tex`; added 2026-10-04):

7. `Ktlean/CornerTurns.lean`: the local bounds `Lside` (L_0 = 1, L_1 = L_2 = (neighbours at
   distance 0 or 3) - 1, L_3 = 1 - (neighbours at distance 1 or 2)), with `Lside_le_turn`
   (t ≥ L) and `sum_Lside` (the sum over the board is exactly 2m). `CornerBound c` is the corner
   lemma as a parameter: in an abstract corner (2-regular symmetric graph, corner coordinates
   X, Y ≥ 0, knight moves), the sum of t - L_x - L_y over the 16 corner cells is at least -c.
   A `CornerCert` (numbers α on the 16 cells, β on oriented edges inside the corner) with
   `Valid` (a decidable check of r(v) ≥ α(v) + D(v) for every cell and every pair of distinct
   legal moves) gives `CornerBound (-Σ α)` (`CornerCert.cornerBound`; the β terms cancel by
   antisymmetry). `cert28` is Tables 1 and 2 of `main.tex`; `cert28_valid` and
   `cert28_total : cert28.total = -7` are `decide +kernel` checks (seconds).
   `cornerBound_seven : CornerBound 7`.
8. `Ktlean/Turns28.lean`: `TwoFactor.eight_mul_le_numTurns_add_of_cornerBound`:
   `CornerBound c → 8n ≤ T + 4c` for every 2-factor, n ≥ 8. A cell outside the four corners
   has at most one nonzero side term; at a corner cell only the two sides of that corner
   contribute. A better certificate of the same shape (4 × 4 corner, same `Lside`) only needs a
   new `CornerCert` value and its two `decide` checks.

## How to build

```sh
export PATH=$HOME/.elan/bin:$PATH
lake exe cache get   # once, downloads the Mathlib build
lake build           # builds Ktlean (about 5 minutes when Mathlib is cached; the tile
                     # certificate in Tiles.lean takes about 2 minutes)
lake env lean Axioms.lean   # prints the main statement and its axioms
```

Status (2026-10-04): everything builds with no errors, no warnings and no `sorry`.

## Toward crossings above 4n (in progress, 2026-10-02)

Target: `X ≥ (4 + c) n - O(1)` for closed tours (KT Turns Theory FINDINGS.md sections 6-7,
KT Lower Bounds TILE_INPUTS.md sections 2-3: `c = 1/17`).

Proved (no `sorry`, standard axioms only):

- `KT.flux_eq` (`Flux.lean`): the exact flux identity (6.1) for any family of knight edges,
  `flux(q) = χ(q) (m(t₋) + m(t₊) - 3 g(q))`. The single-edge case is a kernel check over relative
  positions (about 30 s). `KT.three_dvd_flux_add_chi`: `ω = flux + χ ≡ 0 (mod 3)` when both
  beside-triangles have multiplicity one (6.2).
- `KT.bad_budget` (`TileBudget.lean`): for `U` inside the board and a set `B` of crossing pairs
  whose tile overlaps avoid `U`: `#{t ∈ U : m(t) ≠ 1} ≤ 4X - 8n + 4 - 2|B|` (stated with ordered
  pairs: `bad + 8n + 2|B| ≤ 2Y + 4`, `Y = 2X`).
- `KT.charged_paths_budget`: `L` disjoint dual paths, each with a step where `3 ∤ ω`, with their
  beside-triangles in `U`: `L ≤ 4X - 8n + 4 - 2|B|` (6.5).
- `KT.counting_chain`: the arithmetic of 7.4/7.6, `69 n ≤ 17 X + 17087` from the four inputs.

- `KT.three_dvd_sum_bdry` (`Loop.lean`): the closed-loop identity. For any finite lattice set
  `B` whose points have degree 2, the outward sum of `ω` over the boundary steps of `B` is
  `0 (mod 3)`. Each knight edge crosses the dual grid along a 3-step lattice path
  (`KT.flux1_eq_path`), so its flux out of `B` telescopes.
- `KT.corner_charge` (`Corner.lean`): for `R ≥ 12`, P/P' patterns on the four endpoint rows of
  the left and bottom sides give a step of `γ_R` with `ω ≢ 0 (mod 3)`. With the box `[0, R]²`
  the outer sides carry no board flux; only four end steps meet tour edges.

## Conditional theorem: X ≥ 14n/3 - 421 (proved 2026-10-02; strip stability is a hypothesis)

```lean
theorem KT.ClosedTour.combined_count {h : ℕ} (T : ClosedTour (2 * h)) (hh : 16 ≤ h) :
    10 * (2 * h) ≤ 2 * T.numCrossings + T.badRows.card + 130
theorem KT.ClosedTour.fourteen_mul_le_of_stability {h : ℕ} (T : ClosedTour (2 * h))
    (hh : 16 ≤ h) (C : ℤ)
    (hstab : (T.badRows.card : ℤ) ≤ (T.numCrossings : ℤ) - 4 * (2 * h) + 2 + C) :
    14 * (2 * h : ℤ) ≤ 3 * T.numCrossings + C + 132
```

**Proved in Lean (no `sorry`, standard axioms only):** `combined_count`, i.e.
`X ≥ 5n - 65 - b/2` for every closed tour of the `n × n` board, `n = 2h ≥ 32`, where `X` is the
number of crossings and `b = T.badRows.card` is the number of rows, in the scan ranges
`[12, h-4]` and `[h+2, n-14]` of the four sides, that fail the endpoint test of KT Turns Theory
FINDINGS 10.4 (`KT.GoodRow`): in the board rotated `k` times, the sum `F` of the coefficients
`KT.Fcoef` of the eight listed edges at row `y` is `2` mod 3, and the exceptional pair
`(0,y)--(2,y+1)`, `(0,y+1)--(2,y)` is not present. A row that passes the joint test of KT Lower
Bounds TILE_INPUTS section 9 passes this test.

**Explicit hypothesis (not formalized):** the per-row strip stability `b ≤ E + C`, `E = X - 4n + 2`.
TILE_INPUTS section 9 certifies it with `C = 1131` (beta = 1, potential range [-29, 0]; checked by
three independent programs, not in Lean). With it, `3X ≥ 14n - 1263`, so `X ≥ 14n/3 - 421`.

Ingredients (FINDINGS 9-10):
- `corner_charge_mod` / `corner_charge_mod_rot`: `γ_R` is charged when both end values are 1 mod 3
  (all four corners by rotation). `sum_gL_eq`: end value `= F + deg(0, R)`, so the test gives it.
  `gB_rot`: the bottom end of corner `k` is the top end of side `k + 3` at row `n - 2 - R`.
- `mult_alt`, `two_bad`, `charged_squares_budget`: whole-square charges (9.1-9.2).
- `side_pairs`: at least `n + 1` crossing pairs among the moves at one side, for every
  degree-two family (no forest condition).
- `col0_overlap`, `canon_exc`: the boundary pairs avoid the squares of the retained paths (the only
  overlap at `x = 1` is the exceptional pair, which the test excludes).
- `combined_count` (any `n²` distinct knight edges with degree two at every cell) and the closed
  tour version in `TourMain.lean`.

The additive constants (130, 132) are loose at the corners; only the coefficient 14/3 matters here.
`corner_charge_row` (the earlier hypothesis: the straddling edges at a row are exactly `P` or `P'`)
is still proved and implies the test hypothesis.

### Feasibility of the finite certificates (measured 2026-10-02 on this box, under load)

1. **Strip graph + potential certificate** (82,516 states, 144,674 arcs, potential in
   `[-149, 0]`). I ported the transition function of `strip2_independent.py` to Lean. Run by
   `#eval` (compiled interpreter), it gives the same graph: 82,516 states and 144,674 arcs, in
   35 s. Kernel evaluation (`decide +kernel`) is much slower: the successors of a 400-state
   sample took about 2 minutes (about 0.3 s per state), and parsing the state table from a string
   another 5 minutes. Projection for the full check (successors of every state, closure of the
   state table, and the potential inequality on every arc): about 7 hours with the direct port.
   A Nat-only encoding and a balanced lookup tree could perhaps make this 1-2 hours (unchecked
   estimate). With `native_decide` the same check takes under a minute, but it adds the
   `Lean.ofReduceBool` axiom (not approved).
   The larger cost is not the certificate but the **soundness proof of the strip model**: that
   the tour edges at one side give a walk in this graph from the start state, with total weight
   equal to the strip crossings, and that a row whose four transitions are cycle arcs has
   pattern P or P'. This needs a Lean model of pending-edge states, component labels and the
   acyclicity argument. I estimate 1,500-3,000 lines of Lean. This is the most expensive input.
2. **Corner endpoint charge** (2,916 corner choices × 4 pattern pairs × 2 parities of R): the
   finite part is small (a kernel check of minutes). The work is the uniform-in-R reduction: the
   loop identity, the degree identity for the middle boundary cells, and the translation of the
   endpoint data. The loop identity has a clean proof: each knight edge crosses the dual grid
   along a 3-step lattice path, so its flux through the boundary of any lattice point set
   telescopes. Estimate: a few hundred lines.
3. **Strip row certificate** (cycle arcs give P/P', and the pending crossing pair): small as a
   finite check, but it is stated about the strip model of item 1, so it comes with item 1. If
   good rows are defined directly by the P/P' pattern, the crossing pair of 7.2 and its overlap
   in the boundary strip are a short direct proof.

Order I plan: loop identity, then good-row crossings (7.2), then the corner lemma (7.6), then
strip stability (7.1/7.6).
