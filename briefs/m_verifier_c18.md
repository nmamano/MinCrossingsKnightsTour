Chief Researcher -> KT Verifier (2026-10-02 ~06:55 UTC). Thanks for Claim 17 (noted: conditional only).
Claim 18: X >= 9n/2 - 585 for closed tours, w-turnstheory/FINDINGS.md sections 10.1-10.3.
New: (10.1) one critical scan row fixes the endpoint data needed by the corner charge; (10.2) the corner needs only that one row;
(10.3) the two corners on a side use disjoint scan-row intervals [12, n/2-4] and [n/2+3, n-13], so a bad scan row removes at most
one candidate path: L >= 2n - 60 - d; with |B| >= 4n - 24 (9.6) and whole-square charges 2L <= 4E + 44; per-row stability (7.7)
d <= 2E + 2250; hence 4n <= 8E + 4664, X >= 9n/2 - 585. Checkers: check_one_row_strip.py, check_corner_one_row.py,
check_col0_squares.py, check_square_defects.py.
Audit with your own code where you can: the one-row lemma (does one critical row really fix all endpoint edges the corner charge
uses, in all four column phases and both corner orientations?), the corner computation with only that row, the disjointness of the
scan-row intervals, that d counts exactly the rows tested, and the chain. Write as Claim 18. One CPU core.
