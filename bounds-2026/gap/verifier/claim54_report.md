# Claim 54: Lean proof of the 8n - 28 turn bound

Audit date: 2026-10-04. Reviewer: KT Verifier (Astra).
Commit: `e55bc59cc6b4dcf8381c56bb578fd325ee00a0c0` in `ktlean`.

**Verdict: PASS.** The clean project build passes, both theorem axiom lists are exactly the requested three standard axioms, the definitions match the paper, and `cert28` equals Tables 1 and 2.

## Clean build method

The audit exported the exact commit with `git archive` into the new directory `gap/verifier/claim54_clean`. All 43 tracked files were compared byte for byte with the commit; no differences were found. The copy began with no project build output. The existing external dependency cache was linked at `.lake/packages`; Mathlib and its dependencies were not rebuilt from source. All project modules are built afresh by `lake build`. The process and its children are restricted to two CPU cores, with `LEAN_NUM_THREADS=2`.

The toolchain is Lean `v4.35.0-rc3`; the manifest pins Mathlib to `c55e6e786f49471c72fbddbec5415808896aec1e`.

Evidence: `claim54_build.log`, `claim54_source_check.json`, and the clean exported source tree. `Claim54Axioms.lean` is an added audit harness, not a change to the exported project sources.

## Build and axioms: PASS

`lake build` exited 0 with `Build completed successfully (8985 jobs).` In particular, the clean copy rebuilt `Ktlean.CornerTurns`, `Ktlean.Turns28`, and the aggregate `Ktlean` target.

`lake env lean Claim54Axioms.lean` also exited 0. Its exact outputs for the two theorems are:

```text
@KT.ClosedTour.eight_mul_sub_28_le_numTurns : ∀ {n : ℕ} (T : KT.ClosedTour n), 8 ≤ n → 8 * n - 28 ≤ T.numTurns
@KT.TwoFactor.eight_mul_le_numTurns_add_28 : ∀ {n : ℕ} (F : KT.TwoFactor n), 8 ≤ n → 8 * n ≤ F.numTurns + 28
'KT.ClosedTour.eight_mul_sub_28_le_numTurns' depends on axioms: [propext, Classical.choice, Quot.sound]
'KT.TwoFactor.eight_mul_le_numTurns_add_28' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The certificate validity lemma itself reports only `propext`. The certificate total and `cornerBound_seven` report only the same three standard axioms. The complete tracked Lean source scan finds no `sorry`, `sorryAx`, `native_decide`, or custom `axiom` declaration. Thus there is no proof gap or native-decide trust extension in the audited results.

Evidence: `claim54_axioms.log` and `claim54_source_check.json`.

## Definitions: PASS

Inspected `Ktlean/Basic.lean` and `Ktlean/Tour.lean` in the exported copy.

- `Cell n` is `Fin n × Fin n`; displacement uses integer coordinates.
- `IsKnightVec` requires absolute coordinate differences 1 and 2 in either order.
- `ClosedTour n` is an equivalence from `Fin (n*n)` to all board cells. Its knight-move condition applies to every position and its cyclic successor, including the closing edge. Thus it is a single Hamiltonian knight cycle.
- `ClosedTour.IsTurn` is failure of collinearity of predecessor, current cell, and successor. `Collinear3` uses a zero integer cross product. `ClosedTour.numTurns` counts precisely these positions.
- `TwoFactor n` assigns each cell a finite set of exactly two distinct knight neighbors, with a symmetric relation. Connectivity is not assumed, as in the paper's stronger 2-factor statement.
- `TwoFactor.IsTurn` means its two displacement vectors are not opposite. A knight vector is nonzero; the two neighbors are distinct. Parallel knight vectors are equal or opposite, so this is the same turn definition.
- `toTwoFactor_isTurn_iff` and `numTurns_toTwoFactor` prove that the closed-tour conversion preserves the predicate and count. The new closed-tour theorem uses that equality explicitly.

The closed-tour theorem uses natural subtraction. Since `n ≥ 8`, `8*n ≥ 28`, so subtraction does not truncate and the statement equals the paper's bound. Neither theorem assumes evenness or adds an unproved certificate premise.

## Certificate: PASS

`CornerCert.alphaAt x y` indexes the list at `4*y+x`. `G p q` is `betaAt p q - betaAt q p`, which matches the paper's plus sign at the first endpoint and minus sign at the second. `Lloc` and `Lside` match the four side-contribution formulas printed in the paper.

The independent script `claim54_cert_check.py` parses `cert28` from the clean Lean source and Tables 1 and 2 directly from `writeup/turns/main.tex`. It confirms:

- All 16 alpha entries match, with the same coordinate order and sum -7.
- All nine oriented beta edges and signs match.
- All 209 legal unordered local move-pair cases satisfy the certificate inequality.
- Every corner cell has an equality case.

Lean's `cert28.Valid` checks distinct ordered pairs of the eight knight vectors, with nonnegative endpoints, and requires every listed beta edge to stay inside the corner. This covers the same local cases, with both pair orders. Both `cert28_valid` and `cert28_total` use `decide +kernel`.

The proof then cancels signed internal edge contributions, obtains the bound -7 for each corner, and sums the four side contributions and four corner bounds to obtain 8n - 28. The final theorems instantiate this concrete certificate; they do not assume its validity.

Evidence: `claim54_cert_check.log`, which also records SHA-256 hashes of the compared Lean source and paper.

## Documentation follow-up

`writeup/turns/main.tex:280` still says the constant 28 is not formalized. The formal-verification subsection and the earlier summary at line 90 describe only the old constant 64. Update those statements to describe the now-verified theorem. This is a documentation issue, not a defect in the mathematical definitions or certificate. The audit does not edit the paper.
