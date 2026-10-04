# Claim 56, Part 1: improved finite tours

Audit date: 2026-10-04. Reviewer: KT Verifier (Astra).

**Verdict: PASS for the supplied tours and the stated finite extension ranges.** These are valid concrete improvements over 8n - 14 at the checked sizes. **Part 2, the proof for every size in the two residue classes, remains pending.**

## Supplied files

At the start of the audit, the two named directories contained six JSON tour files. The worker added n=50 and n=54 during the audit; I checked those too. All eight supplied files were independently checked and copied to `gap/verifier/claim56_run/`:

| File in gap/searcher/turns/tours/ | n | Vertices in the single cycle | Turns | T - 8n |
|---|---:|---:|---:|---:|
| res2/n50.json | 50 | 2,500 | 383 | -17 |
| res2/n58.json | 58 | 3,364 | 447 | -17 |
| res2/n66.json | 66 | 4,356 | 511 | -17 |
| res2/n74.json | 74 | 5,476 | 575 | -17 |
| res6/n54.json | 54 | 2,916 | 416 | -16 |
| res6/n62.json | 62 | 3,844 | 480 | -16 |
| res6/n70.json | 70 | 4,900 | 544 | -16 |
| res6/n78.json | 78 | 6,084 | 608 | -16 |

Every count agrees with the file metadata and the claimed residue-class constant. `claim56_run/results.json` records each source filename, SHA-256 hash, exact count and cycle length.

## Independent check

`gap/verifier/claim56_check.py` is a standard-library-only checker. It imports no code from the searcher, `kt`, the integrator, or the extension script. It checks:

- Exactly n rows of n cells, with two distinct valid move codes per cell.
- Every move stays on the board and has absolute coordinate differences 1 and 2.
- Every edge is reciprocal and every vertex has exactly two distinct neighbors.
- A complete component traversal visits all n² vertices in one closed cycle.
- The turn count obtained from integer determinants agrees with a separate opposite-code count, and agrees with the claimed metadata.

This verifies closed Hamiltonian knight tours, not just degree-two covers or open tours.

## Finite extension ranges

The worker's logs list more sizes than its saved JSON files. To check those finite claims directly, I implemented the stated coordinate-copy extension independently: keep the lower half of each coordinate range, insert repetitions of its eight-cell middle window, then keep the upper half. Every resulting grid was passed through the independent checker above.

Results:

- From the n=62 seed: all 19 sizes 62,70,...,206 are single cycles with exactly 8n - 16 turns. The last size has 1,632 turns.
- From the n=66 seed: all 19 sizes 66,74,...,210 are single cycles with exactly 8n - 17 turns. The last size has 1,663 turns.
- The separately supplied n=58 tour is a single cycle with 447 = 8·58 - 17 turns.

Thus 41 distinct board sizes are verified here: the 38 generated cases, the separate n=58 witness, and the late-added n=50 and n=54 witnesses. Where a generated grid also has a supplied file (62,70,78 and 66,74), the grids agree cell for cell. The generated grids are reproducible from the saved seeds and the audit script; their results are recorded in `results.json`.

The choice of seed matters. As a check against an invalid extension claim, I also extended the n=58 seed to n=66. That grid has two cycles, of lengths 3,062 and 1,294. It is not used as a witness. This agrees with the worker's warning and confirms the need for the separate n=66 seed in the stated finite range.

## Scope and next step

This audit establishes the finite tour/count claims. It does not establish optimality within the searcher's solver family, global optimality, minimal period, or validity for unbounded n. The late-added n=50 and n=54 witnesses cover the smallest board sizes needed for these two residue classes. They do not by themselves establish induction.

Part 2 will audit the Integrator's certificate and its finite exceptions when the Chief Researcher supplies that claim. The all-size argument must use the new families' actual templates and corner data; a finite extension test alone is not induction.

Reproduce Part 1 from the project root with `python3 gap/verifier/claim56_check.py --out gap/verifier/claim56_recheck` (a fresh output directory). The script intentionally refuses to overwrite `claim56_run`; the checked seeds and results remain fixed audit evidence. The completed run is in `gap/verifier/claim56_check.log`.
