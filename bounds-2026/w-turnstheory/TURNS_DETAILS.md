# Turns lower bound: 8n - 64

Date: 2026-10-02. Author: KT Turns Theory (Astra).
Status: PROVEN by the counting argument below. The proof does not depend on a solver.

## Result

Every closed knight's tour on an n by n board, for n >= 8, has at least

    T >= 8n - 64

turns. Thus liminf T_min(n)/n >= 8, where n ranges over board sizes that admit a tour.
This improves the paper's (6-epsilon)n bound to (8-epsilon)n for every epsilon > 0 and sufficiently large n.
It proves the asymptotic coefficient in the paper's 8n conjecture. It does NOT prove the exact inequality T >= 8n.

The proof also applies to every spanning degree-two subgraph of the knight graph, even if that subgraph has several cycles.

## Lemma: the first four columns contain at least 2n turns

Index columns by 0,1,2,3,... . Each column has n cells. A cell is straight if its two incident knight moves are opposite. Otherwise, the cell is a turn.
Let T_i count the turns in column i, for i = 0,1,2,3.
Let B count the chosen tour edges that join column 3 to column 1 or column 2.

1. All n cells in column 0 are turns. Both incident moves increase the column index, so those moves cannot be opposite. Thus T_0 = n.

2. For a cell v in column 1 or column 2, let p(v) count its chosen edges to column 0 or column 3. Its turn indicator is at least p(v)-1.

   For p(v) <= 1, this holds because a turn indicator is nonnegative.
   For p(v) = 2, the cell must be a turn: from column 1, the two counted types have horizontal displacements -1 and +2; from column 2, they have horizontal displacements -2 and +1. Neither set contains two opposite horizontal displacements. Two edges of the same type also cannot be opposite.

   Every edge at column 0 goes to column 1 or column 2. Column 0 has exactly 2n incident edges, since every cell has degree two and no knight edge stays within one column. Hence

       sum over v in columns 1,2 of p(v) = 2n + B.

   There are 2n cells in these columns. Sum the local inequality to obtain

       T_1 + T_2 >= (2n + B) - 2n = B.

3. For a cell v in column 3, let q(v) count its chosen edges to column 1 or column 2. Its turn indicator is at least 1-q(v).

   If q(v) >= 1, the right side is nonpositive.
   If q(v) = 0, both chosen moves increase the column index. Therefore, the cell is a turn.
   These are all cases: a knight changes its column index by exactly 1 or 2.

   Sum over column 3. Since sum q(v) = B,

       T_3 >= n - B.

Add the three bounds:

    T_0 + T_1 + T_2 + T_3 >= n + B + (n-B) = 2n.

This proves the lemma. The proof allows all edges from the strip to the rest of the board. It makes no assumption about their directions or endpoints beyond the knight move rule.

## Square-board theorem

Apply the lemma at the left, right, top, and bottom sides. The sum of the four strip turn counts is at least 8n.
For n >= 8, the left and right strips are disjoint, as are the top and bottom strips.
A turn can therefore belong to at most two strips. A turn belongs to two strips only in one of four corner squares, each of size 4 by 4.
There are 64 cells in these four squares.
Thus the sum of strip turn counts is at most T + 64, and

    8n <= T + 64.

Therefore T >= 8n - 64.
More precisely, if C is the actual number of turns in the four corner squares and I is the number of turns outside all four strips, then

    T >= 8n - C + I.

The constant 64 is a safe bound for C. No claim that 64 is best is made here.

For a w by h rectangle with w,h >= 8, the same proof gives T >= 4(w+h)-64.

## Why turns differ from crossings

The earlier crossing relaxation has a pattern with one crossing per boundary row, regardless of the strip width.
That pattern does not obstruct this turn bound. In that pattern, cells in columns 0 and 1 are turns and later columns are straight. Thus it has exactly two turns per boundary row.

For a direct check in coordinates (x,y), the pattern contains edges

    (0,y)--(1,y+2), (0,y)--(2,y+1),
    (x,y)--(x+2,y+1) for each x >= 1.

At x=0 the two moves are (1,2) and (2,1). At x=1 the two moves are (-1,-2) and (2,1). Both pairs are turns. For x>=2 the two moves are (-2,-1) and (2,1), so each pair is straight.
Every component runs to unbounded x in both directions from its single x=0 cell; the pattern has no cycle. Thus two turns per row is sharp for the one-side strip relaxation, even with its no-cycle condition.

The four-column count uses two facts that a boundary-leg count does not use: all cells in columns 1 and 2 must have degree two, and all cells in column 3 without a backward edge must turn. These facts account for all n additional turns, with the B term cancelling exactly.

## Verification and discovery

`check_proof.py` is an independent exhaustive check of the local statements in the proof. It uses integer arithmetic and no solver. It enumerates all 77 possible pairs of distinct knight moves at a cell in each of columns 0,1,2,3, subject only to not leaving the left half-plane. It checks each local inequality. Finite-board corner restrictions only remove possibilities from these lists.

The same script builds and validates four known tours, then checks each of their four strip counts and their total counts. Measured on 2026-10-02:

| n | Total turns | Left, right, top, bottom strip turns |
|---|---:|---|
| 16 | 138 | 45, 46, 47, 58 |
| 24 | 214 | 61, 62, 69, 80 |
| 40 | 366 | 93, 94, 113, 124 |
| 80 | 746 | 173, 174, 223, 234 |

Run from the project root:

    .venv/bin/python w-turnstheory/check_proof.py

The proof was found with `strip_lp.py`, a small linear relaxation with row-aggregated move-pair variables. Edges that leave the strip are unconstrained. The final script returns strip bounds 1, 1.5, and 2 at widths 2, 3, and 4. It checks the width-four integer dual exactly with Fraction arithmetic. Larger tested widths, through 80, retain bound 2.
The first exploratory model imposed unnecessary conditions on ghost columns. That model was replaced before the proof was accepted. The final model and the counting proof both leave outgoing edges unrestricted.

## Remaining question

The asymptotic lower coefficient 8 is proved. The exact finite-size bound T >= 8n, a better additive constant, and a construction with 8n+O(1) turns are not proved here.
The completed result is ready for independent review by the Chief Researcher. No shared source files were changed.
