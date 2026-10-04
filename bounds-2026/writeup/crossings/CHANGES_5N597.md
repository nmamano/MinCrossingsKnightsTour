# Crossings post: 5n-597 update

2026-10-03. Line numbers below refer to the source before this edit and to the updated `post.mdx`. Only `post.mdx` and this change list were written.

## Bound replacements

| Location | Old line | New line | Old → new |
| --- | ---: | ---: | --- |
| Frontmatter excerpt | 4 | 4 | `5n - 612` → `5n - 597` |
| Result Callout | 36 | 36 | `5n - 612` → `5n - 597` |
| Lean/Python scope | 226 | 226 | `5n - 612` → `5n - 597` |
| Body conclusion | 291 | 291 | `5n - 612` → `5n - 597` |
| The gap | 303 | 303 | `5n - 612` → `5n - 597` |
| Details link | 316 | 316 | `5n - 612` → `5n - 597` |

All 10 old bound occurrences (spaced or unspaced) were replaced or removed by the appendix rewrite. No `5n - 612` remains.

## Body proof changes

### Old line 198 → new line 198

Old: 4. A charged path needs two bad quarters. If they are in its middle, they pay for half an extra crossing. Different paths use different quarters.

New: 4. Each path we keep needs two usable bad quarters. Together, they pay for half an extra crossing. Different paths use different quarters.

### Old line 199 → new line 199

Old: 5. The side strips pay for paths that lose their charge, and for charged paths whose bad quarters stay near an end. Together, the paths add about `n` crossings to the tile bound.

New: 5. We discard paths with a failed endpoint test or a visible two-quarter strip overlap at an end. The side strips pay for those paths. Together, the paths add about `n` crossings to the tile bound.

### Old line 267 → new line 267

Old: The paths don't touch. There are `2n - 60` candidates. We keep those whose charge and endpoint conditions let us use the count below. Each discarded path has a failed test at an end.

New: The paths don't touch. There are `2n - 60` candidates. We discard a path if either end fails the endpoint test or has a visible two-quarter strip overlap. We call those end rows _strong_. Every path we keep is charged.

### Old line 279 → new line 279

Old: A charged path therefore has two bad quarters in one of its squares. The exact area identity lets us pay `1/4` for each of them, using gaps and overlap counts. A crossing can pay for at most two quarters. Different paths use different quarters, so these payments don't exceed the available count.

New: Each path we keep therefore has two bad quarters in one of its squares. The exact area identity bounds their number using gaps and overlap counts. A crossing accounts for at most two quarters. Different paths use different quarters, so we can add their counts.

### Old line 281 → new line 281

Old: There is one exception: two quarters covered by the same crossing pair in a side strip. That pair belongs to the side count instead. Away from the sides, this exception can't occur. A bad square in a path's middle therefore pays the full half crossing.

New: There is one exception: a quarter covered exactly twice by a pair in a side strip whose tiles share two quarters. Such an overlap can only meet a path near an end, where it makes the row strong. We already discarded those paths. All bad quarters on the paths we kept are therefore _usable_.

### Old line 285 → new line 285

Old: The remaining paths either lost their charge or have too few quarters paid by Step 4. In the second case, a bad quarter must come from the side-strip exception, near one of the path's ends.

New: Every discarded path has a strong end row: a failed endpoint test or a visible two-quarter strip overlap.

### Old line 289 → new line 289

Old: Each remaining path can choose a different counted row. The exact area identity combines the quarter payments with half of this extra side count. Thus every candidate path pays half a crossing, either through its quarters or through a side row.

New: Each discarded path can choose a different counted row. The exact area identity combines the usable-quarter count with half of this extra side count. Thus every candidate path pays half a crossing, either through its quarters or through a side row.

### Old line 316 → new line 316

Old: the exact endpoint test, strip stability, and `X >= 5n - 612`

New: the exact endpoint test, the cut-state certificate, and `X >= 5n - 597`

## Appendix B replacement

Old lines 491–764 → new lines 491–659. Replaced the full lower-proof details block from the audited `PROOF_5N_V2.md` (Claim 52).

| New line | Old → new |
| ---: | --- |
| 492 | `5n - 612` tour theorem → `5n - 597`; add the spanning simple 2-factor theorem, counting crossings between components |
| 500 | G/X1/W3 and private quarter capacity → D+X1=2E and the scalar usable-quarter bound; retain 4n-2 |
| 531 | Keep flux and the square identity; state all unit edges of the infinite lattice and board-contained vertex sets |
| 545 | Residue retention → the passing endpoint calculation and strong-row definition, with the same coefficient table and reflected row |
| 574 | Deficient-path payment cases → discard all strong-end paths first; z<=b and two usable quarters per kept path |
| 596 | Forest/full-mask certificate → degree-only cut-state graph: 3,136 states, 48,510 arcs; potentials [-24,0]/[-28,0], interface [0,4] |
| 627 | T+1160 and 612 → T+1130 and 597; the same proof applies to spanning simple 2-factors |
| 640 | Old certificate and OR-Tools requirement → NumPy author cut checker plus standard-library independent checker; correct separate exception check; public checker/proof/audit links |

## Scope and validation

- Part 1 and appendix A are byte-for-byte unchanged.
- Every BlogImage block is byte-for-byte unchanged; no image asset was edited.
- The turns post and all other proof/source files were not edited.
- MDX compile: `node writeup/crossings/check_mdx.mjs` passed. The site compiler accepted the post and both collapsed proof blocks.

## Follow-up after Claim 53 (2026-10-03, Chief Researcher)

- Line 241: "Around a closed loop the sum is zero." -> "Around a closed loop enclosing only board vertices, the sum is zero modulo 3." (Claim 53B domain clarification.)
- Claim 53D lists differences against the older Claim 46 snapshot that are NOT part of this update: demo URLs moved to the repository-site root (lines 51-52, 56), arXiv link on "paper" (62), and two image blocks, formation_moves.png (72-77) and heel_original.png (79-84). These were inserted earlier on 2026-10-03 at Nil's request.
