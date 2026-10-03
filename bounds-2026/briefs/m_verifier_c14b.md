Chief Researcher -> KT Verifier (queued after Claim 12). Claim 14 (replaces my earlier Claim 14 brief):
X >= (4 + 4/15)n - 540 for closed tours (w-lowerbounds/TILE_INPUTS.md section 7; section 6 = intermediate 4 + 4/23, skip it
unless 7 depends on it). Two changes against Claim 13 / Turns Theory 7.4:
 (a) B = ALL proper crossing pairs among edges incident to the outermost column (column 0) of each side, not only good-row
     pattern pairs. The paper's strip bound gives n - 1 per side even in bad rows, so |B| >= 4n - 8 with no d term. Their tile
     overlaps must avoid U: column-0 tiles stay in x <= 2 and never cover the right quarter of squares at x in [1,2]
     (check_col0_overlaps.py, 115 pairs, 0 violations). Hence L <= 4E + 12.
 (b) Loss only k + 3 radii per run of k bad rows; run-aware stability with sharp constant 2/7:
     sum(w - 1/4) >= (2/7) sum_runs(k+3) - 167/28 over every strip walk (1431/5000 gives a negative cycle).
My algebra: total sum_runs(k+3) <= 3.5(X + 1104 - 4n + 4*167/28) = 3.5E + 3940.5; 2n <= 4E + 72 + that = 7.5E + 4012.5
(their 4034 is safe); E >= (4/15)n - 538; X >= (4 + 4/15)n - 540.
Check especially: the n - 1 per side bound for column-0 pairs (is it exactly the paper's lemma, and does it hold in bad rows?);
no double counting of B between two sides at a corner; the column-0 overlap/U disjointness for ALL pairs (not only pattern pairs);
the k + 3 count; the potential certificate and an exact sharpness witness. Write as Claim 14. One CPU core.
