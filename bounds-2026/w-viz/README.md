# Knight-tour figures — 2026-10-02

Six figures for Nil. Each has a 200-dpi PNG and an editable SVG with text retained as text. All figures use the same light background, blue-grey tour edges, red crossings, dark turn dots, and teal highlights. Four additional colors distinguish the four paths in a lane pair.

| Figure | Files | Caption |
| --- | --- | --- |
| 1. Crossing heels | [PNG](01_crossing_heels.png) · [SVG](01_crossing_heels.svg) | Equal 40-column windows contain 140 paper-heel crossings, 130 Shisheng-block crossings, and 80 H16a crossings; four colored paths expose the change in terminal pairing. |
| 2. Full-board crossings | [PNG](02_crossing_boards.png) · [SVG](02_crossing_boards.svg) | On the same 72 × 72 board, the paper, Shisheng, H16a, and LF2 tours have 880, 860, 653, and 549 crossings. |
| 3. LF2 anatomy | [PNG](03_lf2_anatomy.png) · [SVG](03_lf2_anatomy.svg) | Four boundary pieces contribute 11/6, 5/2, 2, and 1 crossings per board unit; their line-end pairings give 2, 4, and 2 strands in the three regions. |
| 4. Turn improvement | [PNG](04_turn_improvement.png) · [SVG](04_turn_improvement.svg) | The requested paper heel has 22 turns per eight columns, T18 has 18, T16 has 16, and the displayed 56 × 56 TT16 tour has 434 = 8n−14 turns. |
| 5. Turn lower bound | [PNG](05_turn_lower_bound.png) · [SVG](05_turn_lower_bound.svg) | A real 16 × 16 tour illustrates the four-column lemma with 45 strip turns; the corner certificate reduces the four-corner allowance to 28 and gives T ≥ 8n − 28. |
| 6. Bound summary | [PNG](06_bound_summary.png) · [SVG](06_bound_summary.svg) | Number lines show the turn coefficient gap closed at 8, the finite interval [8n−28,8n−14], and the LF2 finite-size crossing result separately from proved all-size bounds. |

[Contact sheet](contact-sheet.png) gives a quick view of all six figures. Use the individual images or SVGs for reading small labels.

## Count and proof checks

Every full tour drawn here passed the independent verifier: two reciprocal knight moves at every cell and one closed cycle through all cells. Crossings were recounted as unordered edge pairs with proper open-segment intersections. Turns were recounted by a determinant test at each cell. The plotting code independently reconstructs crossing locations and checks its count against the verifier. Coincident crossing locations can share a plotted dot; the reported count is the number of intersecting edge pairs.

The heel panels count crossings in a half-open 40-column periodic window, including seam interactions. The LF2 anatomy panels use 24 board units per view and include the straight continuations. They contain 44, 60, 48, and 24 crossing pairs, respectively. The LF2 arc panels show local line-end matchings, not extra knight moves. Top and right templates are shown before rotation onto the board; side views place the boundary horizontally for comparison.

The 8n−28 corner certificate was independently checked against all 209 allowed local move pairs before rendering. Its corner weights sum to −7. In the drawn four-column example, the column turn counts are 16, 15, 7, 7 and B = 16.

[Counts and source hashes](counts.json) record every displayed tour count, source, strip count, and certificate check.

## Interpretation

- The Shisheng full-board baseline places the 40-column block on both horizontal sides. This is the version with leading crossing coefficient 11.5.
- `Sequence1Opt`, requested for the heel comparison, is the paper's **crossing-optimal** heel with 22 turns. The published **9.25n turn upper bound** uses the separate 21-turn heel. Figure 4 states this distinction.
- H16a's 9n crossing construction and TT16's 8n−14 turn construction passed the all-size corner-reuse audit for even n ≥ 48. The turn lower bound is 8n−28 for n ≥ 8. Thus the leading turn coefficient is exactly 8; the finite-size interval has width 14.
- LF2's displayed tour and local rate are verified. These figures do not promote the finite LF2 witnesses to an all-size theorem. The summary marks 22/3 as verified at n = 72,74,76,78,96,120, without an all-n theorem, and also shows the proved coefficient 9.
- Number-line endpoints are leading coefficients, not counts at a particular n. The paper's turn lower endpoint 6 represents its (6−ε)n−Oε(1) bound.

## Rebuild

From the project root:

```sh
.venv/bin/python w-viz/make_figures.py
```

The baseline generator is `kt/gentour.py`; all count checks use independent code in `w-verifier/`. The new tours come from `w-integrator/tours/` and its `certificates/` directory. The script uses one Python process and runs no solver. The source and build log are retained in this directory.

## TT16 update — 2026-10-02

Figures 4 and 6 now include the independently audited TT16 result. The original file names are retained. Figures 1, 2, 3, and 5 are unchanged. Rebuild only the updated pair with `.venv/bin/python w-viz/make_figures.py --only 04,06`. The contact sheet reflects the update.
