# Claim 56: improved turn bounds, including the all-size proof

Audit date: 2026-10-04. Reviewer: KT Verifier (Astra).

## Verdict: PASS

For every even n ≥ 48:

- If n ≡ 6 (mod 8), a closed knight's tour exists with exactly **8n - 16** turns, so T_min(n) ≤ 8n - 16.
- If n ≡ 2 (mod 8), a closed knight's tour exists with exactly **8n - 17** turns, so T_min(n) ≤ 8n - 17.

The supplied families, finite base cases, and period-16 insertion certificates pass independent checks. The proof covers both classes modulo 16 in each stated class modulo 8. It makes no new claim for residues 0 and 4 modulo 8, and does not prove optimality.

This completes Parts 1 and 2 of Claim 56. The original finite-only report is retained as `claim56_part1_report.md`.

## Audited source and data

The exact requested sources were copied to `gap/verifier/claim56_alln/` before running tests:

| File | SHA-256 |
|---|---|
| allsize_check.py | `f3925853ab20f57416678ee81aa2b4322c7e5074fe4065ff3ef29730353bc5d6` |
| allpipe.py | `2dfc8f14657e04ef2315d3cafa609d691ae59d7223675a00466a5c7f644316d8` |
| allsize_regress.py | `a86d08dcd60ac716d0cf04de1d1cb8a2b2f1bebb3458c271faf51af2d57b8708` |

The two pipeline directories `ES_res2` and `ES_res6` were copied into that audit directory. Tests did not edit the worker's source or certificates. At most two cores were used.

The new `allpipe --extract` reads the four band patterns in the stated coordinate convention and uses phases zero. `--period` and `--residues` select candidate residue data and finite outside-matching tests. The generator remains a candidate generator, not a theorem checker. For these actual outputs, independent reconstruction from the exported templates and zones agrees exactly with every stored tour. Thus the result does not depend on trusting extraction or the searcher's metadata.

## All listed pipeline tours: PASS

All **20** pipeline tour files were checked with independent code: exact n by n coverage, two distinct knight neighbors per cell, reciprocal edges, one cycle of length n², and an integer-determinant turn recount. Every turn count matches the metadata and the claimed constant. Each graph also agrees edge for edge with an independently reconstructed band-and-corner graph.

| Pipeline | Every supplied size | Turns |
|---|---|---|
| ES_res2 | 50,58,66,74,82,90,98,106,114,122 | 8n - 17 |
| ES_res6 | 54,62,70,78,86,94,102,110,118,126 | 8n - 16 |

The earlier Part 1 audit also checked all eight searcher files, including n=50 and n=54, and independently checked the finite extensions through n=210 and n=206. Those checks remain valid; the all-size conclusion here comes from the insertion proof below, not extrapolation from those finite ranges.

Evidence: `claim56_alln_check.py`, `claim56_alln/independent.log`, and `independent_proof_checks.json`. The JSON includes a SHA-256 hash and recount for every supplied pipeline tour. The earlier evidence remains in `claim56_run/results.json`.

## Geometric and cost conditions: PASS

All four residue files use:

- The fixed straight interior with moves `(2,-1)` and `(-2,1)`, on lines `ell=x+2y`.
- Four bands of depth 4; bottom/top period 8 and left/right period 4; phases `[0,0,0,0]`.
- Four full 8 by 8 corner patches: 256 effective zone cells per file, radius R=8.
- p=16, line period w=8, and insertion step s=16.

Independent code checks nonnegative inward corner coordinates, full coverage of each band-overlap rectangle, and the corner radius. Each induction base satisfies N≥max(96,2R+6). The selected slabs have at least six lines of clearance from both the patch spans and the band-overlap spans. They are in the bottom/left, left/right, and right/top regimes. These separations persist when n increases by 16.

The independent checker also verifies the reciprocal incidences of every local band state and its adjacent straight field. Each band has exactly the following cost per period:

| Band | Period | Turns per period | Turns added at step 16 |
|---|---:|---:|---:|
| Bottom | 8 | 16 | 32 |
| Top | 8 | 16 | 32 |
| Left | 4 | 8 | 32 |
| Right | 4 | 8 | 32 |

Hence dT=128=8s exactly. The finite recount confirms this increment at each induction base. Because all corners and band-overlap corrections remain fixed, and the interior paths are straight, the same additive increment holds at every later step.

## Independent insertion checks: PASS

The independent slab checker uses connected components of the induced slab graph, not the worker's path-walk function. It requires every component to have exactly two boundary edges, so it rejects any hidden internal cycle. It separately reconstructs the full port labels and path matching.

A separate connected-component gluing routine checks `M³=M` and rejects any component with no exterior port. For every regional transfer, the independent code also checks the actual shifted width-8 slab and width-24 slab at N+16. Their port alphabets and matchings agree exactly with the base matching and with the recorded certificate.

| n mod 16 | Induction base N | Three cut values at N | Constant |
|---:|---:|---|---:|
| 2 | 98 | 27,117,207 | -17 |
| 10 | 106 | 27,125,223 | -17 |
| 6 | 102 | 27,121,215 | -16 |
| 14 | 110 | 27,129,231 | -16 |

Totals: **12 regional transfers, 36 independently reconstructed slabs, and 12 independent cycle-free `M³=M` tests.** All pass.

Why these finite checks give induction: translating a cut by the line period preserves the band phases, while straight interior paths can change length without changing their endpoints or turn count. The checked geometric conditions keep the exceptional corner pieces outside the repeated gaps. Since s/w=2, replacing a single slab by three has the same external matching and no added cycle. Associativity lets this two-slab insertion repeat. Doing it in all three gaps preserves the one closed tour and adds exactly 128 turns. No unbounded empirical-period assumption is used.

## Complete base-case coverage

The checker directly verifies the following finite cases in each induction class:

| Class mod 16 | Checked sizes through N+s |
|---:|---|
| 2 | 50,66,82,98,114 |
| 10 | 58,74,90,106,122 |
| 6 | 54,70,86,102,118 |
| 14 | 62,78,94,110,126 |

All are transplants from the claimed family; no fallback is used here. These lists include every relevant size below its induction base and the required base and successor. Since `{2,10}` modulo 16 equals class 2 modulo 8, and `{6,14}` modulo 16 equals class 6 modulo 8, the induction proves exactly the two bounds in the verdict.

## Partial mode: scope is sound

The new mode checks that the supplied residue values are distinct, even, and in `[0,p)`. Without `--partial`, it still requires all even residues. With `--partial`, the induction loop checks precisely every even c modulo s with `c mod p` in the supplied set. Thus it also handles s>p correctly: a retained class modulo p is checked in every applicable lifted class modulo s.

The final PASS and the JSON `scope` report exactly that supplied set, unless the set is complete. For these families, the actual output scopes are:

```text
n mod 16 in [2, 10] (PARTIAL: other classes not covered)
n mod 16 in [6, 14] (PARTIAL: other classes not covered)
```

`claim56_partial_tests.py` ran eight scope/adversarial tests:

- A partial dataset without `--partial` is rejected.
- Removing residue 10 succeeds only with scope `[2]`; all direct checks and transfers are in class 2 modulo 16.
- Duplicate, odd, and out-of-range residues are rejected.
- A residue inconsistent with its `n0` is rejected.
- Renaming `res02.json` to `res99.json` does not change coverage: scope follows the validated payload, not a filename.
- A p=8, s=16 test with only residue 2 checks both lifted classes 2 and 10, and reports only class 2 modulo 8.

All eight tests pass. The full ten-case regression suite also passes on this checker version. Evidence: `partial_tests.log`, `partial_tests.json`, and `regress.log`.

The checker does not certify any omitted class. The JSON alone should not be treated as a PASS: as before, require successful process exit and the final PASS line.

## Reproduction

From the project root:

```sh
python3 gap/verifier/claim56_alln/allsize_check.py gap/verifier/claim56_alln/ES_res2 --partial
python3 gap/verifier/claim56_alln/allsize_check.py gap/verifier/claim56_alln/ES_res6 --partial
python3 gap/verifier/claim56_alln_check.py
```

The theorem is limited to the two stated residue classes and the straight-field constructions. Mixed interiors and optimality remain outside this claim. There is no remaining audit blocker for these two all-size bounds.
