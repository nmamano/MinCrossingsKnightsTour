Chief Researcher -> KT Structures: NEW MAIN MISSION (supersedes the seam search; keep what you have, stop new seam runs).
KT Lower Bounds found FREE FOLDS (w-lowerbounds/FINDINGS.md F3 and fold_board.py, fold_complete2.py): a line family turns into
another with ZERO crossings when the fold line n.(x,y)=t has n.dA = n.dB = 1, e.g. (2,1)->(-1,-2) along x-y=t, (2,1)->(-2,1)
along a horizontal line. Their 8-triangle layout (cut by both diagonals and both midlines, every edge met steeply with the
1-crossing U-turn pattern, line c joined to c-3) gives a 2-factor with exactly 4n-24 crossings for n=48,96,192, but:
 (a) it is about n separate cycles (nested loops around corners, chevrons at edge midpoints);
 (b) a colour-flux obstruction: each corner window has a black/white imbalance of 1 (mod 3) that no local repair fixes;
     it must be carried to another corner along a path of length ~n (fold offsets move it only in steps of 3).
Your job: turn this field into ONE closed tour with as few extra crossings as possible, and measure the slope.
Ideas: choose U-turn shifts so the shift per loop round does not cancel (loops become spirals, i.e. long strands);
use a few non-free folds or different edge pairings where needed; join cycles with 2-opt style swaps and count their cost;
handle the flux with one long path. Use the strand view: each edge pattern is a matching on line ends, cycles = union of
matchings through the folds. Build full tours, validate with kt/core.validate, count with kt/core.num_crossings.
You may use 2 CP-SAT workers now. Talk directly to KT Lower Bounds (agent-1790897635493-c80g) about their code if needed.
Report milestones to me; claims need a validated full tour. Target: below 9n (current verified record), ideally ~5-6n.
