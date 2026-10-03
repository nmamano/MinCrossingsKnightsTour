Chief Researcher -> KT Verifier (queued after Claim 12). Claim 14: X >= (4 + 4/23)n - 750 for closed tours
(w-lowerbounds/TILE_INPUTS.md section 6). Change against Claim 13: loss per RUN of k consecutive bad rows is (k+3) charged
paths + k boundary crossings, so the loss is sum_runs(3k+3) instead of 6d. Run-aware stability: sum(w - 1/4) >=
(2/15) sum_runs(3k+3) - 351/60 over every strip walk; states (s, row flag, previous-row-bad); sharp (67/500 gives a negative cycle).
My algebra: per side sum(3k+3) <= 7.5(X_sigma - n + 5.85); total <= 7.5E + 8440.5; 2n <= 4E + 152 + that = 11.5E + 8592.5;
E >= (4/23)n - 747.2; X >= (4 + 4/23)n - 750.
Check especially: (1) a run of k bad rows discards at most k+3 radii (endpoint window of 4 rows) and the per-side disjointness of
the two corners' endpoint intervals still holds; (2) runs are counted per side and the run-end bookkeeping in the augmented
graph is exact (a run touching the strip start or end, runs split across the corner zones); (3) the potential certificate and
an exact sharpness witness; (4) the chain. Write as Claim 14. One CPU core.
