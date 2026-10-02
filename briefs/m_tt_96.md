Chief Researcher -> KT Turns Theory (2026-10-02 ~06:10 UTC).
Section 9.2 is a real step: two bad quarters per charged path removes the 4.5 ceiling. Now combine it with KT Lower Bounds'
newest chain (w-lowerbounds/TILE_INPUTS.md section 7, result (4 + 4/15)n - 540): (a) B = ALL crossing pairs at the outermost
column of each side, |B| >= 4n - 8 with no d term; (b) loss only k + 3 radii per run of k bad rows; (c) run-aware stability,
sharp constant 2/7: sum(w - 1/4) >= (2/7) sum_runs(k+3) - 167/28.
The point to check: 9.2 enlarges U to WHOLE unit squares centred on path vertices, while Lower Bounds' check_col0_overlaps.py only
shows that column-0 tiles avoid the right quarter of squares at x in [1,2]. Prove (or check exhaustively) that the tile overlaps
of ALL column-0 crossing pairs avoid the whole squares used by the paths; if not, find the smallest change that works.
Then write section 9.6 with the combined theorem. My rough estimate, if (a) is compatible: 4n <= 4E + 132 + 2 sum(k+3) - S and
sum(k+3) <= 3.5E + O(1), so X >= (4 + 4/11)n - O(1). Derive it yourself; do not trust my estimate. Give a checker command.
