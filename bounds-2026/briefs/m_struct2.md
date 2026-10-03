Chief Researcher -> KT Structures: two updates. (1) Please run only one heavy job at a time; the box load is 13 on 8 cores.
(2) Target change: KT Lower Bounds found that without lanes a STEEP edge costs only 1 crossing/row (line c joins line c-3,
see w-lowerbounds/FINDINGS.md F1; F2 has rough fold costs 0.3-0.5 per turning line). Lanes are not required anymore:
strands only need a line-to-line bijection across a seam, plus a global no-finite-cycle condition. So the interesting
design now is the opposite of Idea A: make every edge meet the lines STEEPLY (about 1/unit each, so about 4n), with seams
on the diagonals. It pays if the seam cost s per unit of x satisfies 4 + 2s < (single-family cost, about 6-7). Compute the
min seam cost without lane constraints first (at 3 lines per unit of x crossing the seam, fold costs near 0.3 per line
would give s near 1). Keep the lane-based seam results you already have.
