# Claim 13: per-row stability and the 4+1/8 crossing bound — 2026-10-02

**Verdict: PASS for closed knight tours on every even n >= 32.** The augmented graph proves the required per-row estimate, and the complete chain gives

```text
X >= (4+1/8)n-856.
```

I also found an exact sharpness witness. The optimal per-row coefficient for this strip-graph inequality is exactly 1/2, not just close to 1/2 at the search resolution. There is no new gap in the boundary or charged-path inputs from Claim 11.

## Independent augmented graph

`claim13_rows.py` rebuilds the forest strip graph using my own `claim11_forest.py` transition routine. It imports no worker code. The ordinary graph again has 82,516 states, 144,674 arcs, and the same eight critical arcs of the two P/P' cycles.

Let c(s) be the column to be processed next, and let f record whether an earlier transition in the current row was noncritical. For an ordinary arc s -> t, define

```text
a = 1 if the arc is not one of the eight critical arcs, else 0,
g = max(f,a).
```

If c(s) is 0, 1, or 2, the augmented transition keeps g as the new flag and charges zero bad rows. If c(s)=3, the transition charges g and resets the next flag to zero. The next state is then at column zero.

This tests membership in the two critical cycles, not merely zero reduced cost. A zero-cost arc outside those cycles makes its row bad, as required. The current arc enters the logical OR before the end-of-row charge, so a noncritical fourth arc is not lost. A row with several noncritical arcs is charged only once.

Starting with the empty strip state and flag zero, this rule charges exactly one for each row whose four arcs are not all critical. All four critical arcs of a good row must be on one cycle, because the critical cycles are disjoint and the walk is continuous. This is exactly the good/bad row definition used for the selected boundary crossings in Section 7.2 and the four endpoint rows in Sections 7.3–7.4. No three-row margin or change to the meaning of d is introduced.

The full doubled graph has 165,032 states and 289,348 arcs. Exactly 82,521 augmented states are reachable from the empty state with flag zero. The full graph includes flag assignments that are not reachable; proving a potential on that larger graph is safe. The exact sharpness witness below uses reachable states.

## Potential certificate and row bound

For an augmented arc with crossing weight w and bad-row charge b, use integer cost

```text
C = 8w-2-4b.
```

My exact Bellman-Ford computation from a virtual source gives an integer potential h in [-46,0]. The checker verifies C+h(s)-h(t) >= 0 on every augmented arc, not only convergence of the relaxation loop. Thus, for any augmented walk,

```text
sum C >= h(end)-h(start) >= -46.
```

A complete strip scan has 4n transitions, crossing weight X_sigma, and exactly d_sigma bad-row charges. Therefore

```text
8X_sigma-8n-4d_sigma >= -46,
X_sigma >= n+d_sigma/2-46/8.
```

There is no unfinished row in the tour application. For clarity, a general prefix should count completed rows under the charge rule. I also checked that h(s)-4f has minimum -46 on the reachable augmented states. This supplies the same constant if a prefix from the empty state counts its unfinished row as bad whenever its flag is set.

Both supplied implementations agree with the independent computation. `beta_cert.py` converges with range [-46,0], and `strip2_independent.py`'s `row_check(1,2)` converges after eleven in-place passes with the same range. All arithmetic in the verification is integral.

## Exact sharpness witness

The independent checker finds a closed walk in the zero-reduced-cost graph of the new certificate with:

```text
16 transitions = 4 complete rows,
6 crossings,
4 bad rows.
```

It rotates this walk to start at column zero with flag zero, and checks every row directly against the eight ordinary critical arcs. All four rows are bad. Hence

```text
[sum w - transitions/4] / bad rows
    = (6-16/4)/4
    = 1/2.
```

The walk is reachable from the ordinary empty start through the augmented graph. Repeating it makes any coefficient beta>1/2 fail for every fixed additive constant. Together with the potential certificate, this proves that beta*=1/2 exactly for the transfer-graph stability problem.

For example, at beta=501/1000 this cycle has total cost -16 in units of 1/4000. `claim13_runner/check_witness.py` maps its states back to the original `strip_dp.py` graph and verifies all sixteen original arcs, crossing weights, critical-arc flags, row-end charges, and flag resets. That separate check passes.

The capped binary search alone does not certify an upper endpoint: failure to converge before its cap need not mean a negative cycle. The exact witness removes that limitation and makes the approximate interval unnecessary. This sharpness statement is about the strip relaxation; it does not claim that the final coefficient 4+1/8 is optimal for tours.

## Constants and the complete bound

The Claim 11 overlap count gives sum X_sigma <= X+1104. With the exact loss 46/8 on each of the four sides, summing the row estimate gives

```text
d <= 2(sum X_sigma-4n)+46
  <= 2(X+1104-4n)+46
   = 2E+2250,                    E=X-4n+2.
```

Thus the Chief Researcher's tighter arithmetic is correct. The source's 2252 is also correct: it first rounds 46/8=5.75 up to 6 per side. That gives

```text
d <= 2(X+1104-4n+24)
   = 2E+2252.
```

Unlike the earlier alpha calculation, this displayed equality does not need an erratum; the two-unit difference is an explicit rounding loss.

All geometric inputs from Claim 11 still apply to this same d:

```text
|B| >= 4n-48-d,
L >= 2n-60-4d,
L <= 4X-8n+4-2|B| <= 4E+92+2d.
```

Here B contains one distinct crossing pair for each retained good boundary row. Its tile intersections lie in the unit boundary strips. The paths are edge-disjoint, each bad row can remove at most four paths, and all their adjacent quarter triangles U lie inside the board and beyond those strips. Thus the repaired U-domain condition is respected. The use of a per-row flag changes none of those facts.

Combining the last two inequalities and the safe row bound yields

```text
2n <= 4E+6d+152
   <= 16E+13664,
E >= n/8-854,
X = 4n-2+E >= (4+1/8)n-856.
```

With the exact 2250 one instead gets additive loss 3421/4 = 855.25. The requested integer loss 856 remains valid. The only connectivity assumption is the established forest restriction for a proper boundary strip of a Hamiltonian cycle. This audit does not extend the theorem to arbitrary 2-factors.

## Reproduction and status

The original sources were copied to `w-verifier/claim13_runner/`. `run_all.py` runs the two supplied positive certificates and my independent augmented-graph check sequentially, with one CPU core. The exact negative-cycle witness replaces the capped search; no solver or long search was run.

- `claim13_rows.py`, `claim13_rows.json`, and `claim13_rows.log`: independent graph, potential, reachable-state count, and complete exact witness.
- `claim13_runner/beta_primary.log`: supplied beta certificate, PASS.
- `claim13_runner/beta_separate.log`: separate supplied pure-Python row certificate, PASS.
- `claim13_runner/check_witness.py` and `witness.log`: the exact witness checked against the original graph, PASS.

All checks have finished. **Next action:** cite the saved sixteen-step witness and replace the search-resolution statement with the exact value beta*=1/2. The closed-tour bound X >= (4+1/8)n-856 is verified as stated.
