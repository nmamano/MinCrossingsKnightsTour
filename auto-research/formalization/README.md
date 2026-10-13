# Track: formalization

Goal: Lean 4 proofs of bounds that are not formalized yet.

## What exists

The Lean project is [../../bounds-2026/ktlean/](../../bounds-2026/ktlean/) (Lean 4 and Mathlib; toolchain in
`ktlean/lean-toolchain`). Its README states the theorems and their axioms. Proved without `sorry`:

- T >= 8n - 64 and T >= 8n - 28 for closed tours and 2-factors, n >= 8.
- X >= 4n - 2 for closed tours and 2-factors.
- X >= 14n/3 - 421, conditional on strip stability as an explicit hypothesis.

Build, from `bounds-2026/ktlean`:

```sh
lake exe cache get
lake build
lake env lean Axioms.lean
```

## Not formalized

- T >= 8n - 24 ([../../bounds-2026/TURNS_LOWER24.md](../../bounds-2026/TURNS_LOWER24.md)).
- X >= 5n - 597, the tentative bound ([../../bounds-2026/CROSSINGS_PROOFS.md](../../bounds-2026/CROSSINGS_PROOFS.md) part B).
- The strip stability hypothesis of the 14n/3 theorem.
- All upper-bound constructions.

## What to submit

A note with the theorem statements, `#print axioms` output, the toolchain and Mathlib versions, and the build
command. Put the Lean code in your entry folder, or open a separate PR against `bounds-2026/ktlean/` and say so.
Partial work is welcome if the note lists every remaining `sorry`.
