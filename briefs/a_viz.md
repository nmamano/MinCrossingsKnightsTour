Chief Researcher -> KT Verifier: NEW TASK from Nil (your verification queue can wait; finish a running check first if any).
Make the best possible visualizations of each improvement, for Nil (a co-author of the original paper). Work dir: w-viz/.
Use .venv/bin/python (matplotlib is installed there). Read tours from the JSON files (key 'tour', board.js grid) and use
kt/gentour.py (gen_tour(n, n, heel=..., block=...)) for the paper and Shisheng baselines. Output PNG (dpi 200) + SVG.
Figures, one per change:
 1. Crossings, heel level: paper heel (28 per 8 cols, kt/templates.Sequence1Opt), Shisheng's 40-wide block (130 per 40,
    SequenceP40), our H16a (16 per 8 cols, BRIEF.md). Same strip length (40 columns, 4 rows + a few line rows above), crossings
    as red dots, per-column rate in each panel title. Make the strand permutation visible (colour the 4 strands of a lane pair).
 2. Crossings, full board, same n (e.g. n = 72): paper 12n, Shisheng 11.5n, H16a 9n (w-integrator/tours/), lane-free LF2
    7.33n (w-integrator/tours/LF2_n72.json). 2x2 grid, red crossing dots, exact count and formula in each title.
 3. Lane-free LF2 anatomy: the four edge pieces (w-integrator/gadgets/), each with its rate, and the line pairing at each
    edge (arcs between line ends), showing why the regions close into one tour (strand counts BL 2, MID 4, TR 2).
 4. Turns, heel level and full board: paper heel (22 turns per 8 cols; Sequence1Opt) vs T18 (18 per 8, w-turnsbuilder/
    T18-P8-D4.json), turn cells as dots; full T18 tour (w-integrator/tours/certificates/T18_*n64.json) with turns marked.
 5. Turns lower bound 8n - 28: a diagram of the 4-column lemma (column 0 all turns; p(v) at columns 1-2; q(v) at column 3;
    the B edges), drawn on a real tour's left strip, with the per-strip count >= 2n shown.
 6. One summary figure: for crossings and for turns, the old interval [lower, upper] vs the new one, on a number line.
Style: one consistent palette across all figures (tour segments muted blue-grey, crossings red, turns dark dots, highlights
one accent colour), light background, large readable titles stating the number and the date 2026-10-02, no chart junk.
Correctness first: every count you print must come from your own recount of the drawn tour. Write w-viz/README.md listing
each file with a one-line caption. End your turn with a short summary; I will show the figures to Nil.
