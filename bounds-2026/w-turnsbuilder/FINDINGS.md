# Turns search, 2026-10-02

## New candidate for full-tour checks: lane-free T16

`free-P8-D4-template.json` reaches 16 turns per 8 columns, or 2 turns per
column. The strip optimum is proved (OPTIMAL, lower bound 16, 1.38 seconds).
It has 26 crossings per period. All independent checks pass, including
complete cell coverage by finite terminal paths. It does not obey the
lane rule. With 2 turns per row on the side edges, this is a candidate
for 8n + O(1) only if the global pairing and corner construction work.

For c mod 8 = 0,1,2,3,4,5,6,7, the partner offsets are
`[9,-9,-7,7,-7,7,9,-9]`, respectively. Exact template and check details
are in `free-P8-D4.json` and the table below. The Chief Researcher can
test this row-list file with the full-tour assembler.

The secondary search also proved that 26 crossings is the minimum at
16 turns for P=8, D=4 with no lane rule. Its result is
`lex-free-P8-D4.json`. The P=8, D=5 lane-free turn minimum is also proved
to be 16. Its secondary crossing search returned 26, without a proof of
crossing optimality.

### Final search conclusions

The lane-rule searches at P=16 and P=24, D=4 and D=5, did not improve
on tiled T18. The final runs used complete solver hints and returned
36 or 54 turns. A rate of 2 turns per column under the lane rule remains
open for these cases. For P=8, D=4, it is impossible in this strip model:
the proved minimum is 18. For P=8, D=5, the search found 18 without an
optimality proof.

The lane-free T16 gadget can be tiled to P=16 or P=24 and extended to
D=5 with a straight row. The files `tiled-free-P*-D*.json` verify each
of these constructions and record all signed line offsets. Their rates
are exactly 2 turns and 3.25 crossings per column. These tiled gadgets
improve several time-limited solver outputs in the table. A tiling is
a feasible construction, not a new optimality proof.

All requested searches are complete within the stated time limits.
Each solve used one worker, and solves ran in sequence. The first large
lane runs used only edge hints; their outputs are retained in
`edgehint-lanes-*.json`. The final large lane runs first completed each
hint with a separate solve of at most 5 seconds with fixed edges, and
then searched for 30 seconds. Each final seed-completion solve reported
OPTIMAL. Lane-free searches used 45 seconds; secondary crossing searches
used 60 seconds. The load average was 16.15 before the last lane batch.

The remaining research action is the Chief Researcher's full-tour test
of `free-P8-D4-template.json` (or its lexicographic counterpart). This
report makes no claim that the lane-free pairing yields a single global
tour. No network messages were sent during this continued search.

## Verified result: 18 turns per 8 columns

Bottom gadget: P=8, D=4, lane rule enabled, offset 0. CP-SAT reports
OPTIMAL, objective 18, lower bound 18, in 8.0 seconds with one worker.
This is an optimum for this strip model only. Crossings: 31 per period.

The rate is 2.25 turns per column. With side gadgets at 2 turns per row,
the candidate total is 2(2 + 2.25)n + O(1) = 8.5n + O(1).
A full-tour construction is still required. This is not yet a proved
improvement to the published full-tour upper bound.

Exact template, top row first:

```text
26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16
```

The file `T18-P8-D4.json` holds this row list in the format accepted by
`w-integrator/assemble.py --bottom`. The file `lanes-8-4.json` holds
the chosen edge indices, solver result, template, and check results.

For line c = x + 2y, the matching within each pair of lanes is:
0--7, 1--4, 2--6, 3--5, with translation by 8.
Thus the four strands have a permitted permutation.

## Checks

`kt.verify_strip.check_bottom` reports no degree, symmetry, or off-board
errors. It confirms the lane rule and 31 crossings per period.
The separate checker in `run.py` reads the move codes directly. It checks
edge symmetry, the board boundary, and turns. It traces all eight terminal
paths and confirms that all 32 periodic cells belong to finite terminal
paths. It finds 18 turns. No separate strip cycle remains.

## Initial search state

The load average was 11.93 before the search. Only one worker and one job
were used. The next case, P=8, D=5, failed the unrolled lane check, and the
runner exited. No result from that case is accepted. Check whether the
finite unroll window truncates paths before accepting or rejecting it.
The other periods, lane-free search, and lexicographic search remain open.

The POST to the Chief Researcher returned no response. Under the task's
sandbox note, I made no network workaround and stopped. The Integrator
has not received a message. The Chief Researcher can pass
`w-turnsbuilder/T18-P8-D4.json` to the Integrator for full-tour checks.

Next: first build full tours with T18. Then inspect the D=5 verification
failure and continue the requested search grid. For lexicographic search,
fix the proved turn optimum and minimize crossings in a second solve.

## Continued search, 2026-10-02

The Chief Researcher is building full tours in `runs/t18/`. Further
results are passed through these files, as instructed. No POST is needed.
Load average at the start of this search was 7.97.

### The D=5 rejection was a truncated path

The repeated unseeded P=8, D=5 run returned a feasible gadget with 19 turns
and 29 crossings. Its objective lower bound was -30 after 30 seconds.
This result is a diagnostic, not an improvement to T18.

The old six-period checker starts at (33,4) and (37,4), and reaches
(48,1), outside its width of 48. It therefore reports a missing endpoint.
The central-period check in a 28-period unroll passes. The separate
periodic checker also passes: every cell belongs to a finite terminal
path, and all terminal pairs obey the lane rule. Thus the rejection was
caused by the checker window, not by a bad gadget.

Evidence: `diagnose-P8-D5.json` and `diagnose-P8-D5-template.json`.
`continue_search.py` leaves at least 2*P*D columns on each side of its
central start period. A finite strip path has at most P*D quotient cells
and changes x by at most 2 at each step. This margin is sufficient.
The legacy checker is still used for degrees, symmetry, and crossing
counts; its lane flag is not used to reject paths near its window edge.










## Search results, 2026-10-02

Each run used one CP-SAT worker. Time limits do not prove that a better gadget is impossible.

| Result file | Status | T | X | Objective bound | Seconds |
| --- | --- | ---: | ---: | ---: | ---: |
| `lanes-8-4.json` | OPTIMAL | 18 | 31 | 18.0 | 8.0 |
| `lanes-P16-D4.json` | FEASIBLE | 36 | 62 | -14.0 | 30.14 |
| `lanes-P16-D5.json` | FEASIBLE | 36 | 62 | -64.0 | 30.03 |
| `lanes-P24-D4.json` | FEASIBLE | 54 | 93 | -24.0 | 30.0 |
| `lanes-P24-D5.json` | FEASIBLE | 54 | 93 | -96.0 | 30.01 |
| `lanes-P8-D5.json` | FEASIBLE | 18 | 31 | -31.0 | 60.01 |
| `free-P16-D4.json` | FEASIBLE | 32 | 54 | -14.0 | 45.01 |
| `free-P16-D5.json` | FEASIBLE | 34 | 59 | -59.0 | 45.0 |
| `free-P24-D4.json` | FEASIBLE | 48 | 79 | -19.0 | 45.08 |
| `free-P24-D5.json` | FEASIBLE | 54 | 93 | -92.0 | 45.01 |
| `free-P8-D4.json` | OPTIMAL | 16 | 26 | 16.0 | 1.38 |
| `free-P8-D5.json` | OPTIMAL | 16 | 26 | 16.0 | 41.77 |
| `lex-free-P8-D4.json` | OPTIMAL | 16 | 26 | 26.0 | 2.2 |
| `lex-free-P8-D5.json` | FEASIBLE | 16 | 26 | 0.0 | 60.02 |
| `lex-lanes-8-4.json` | FEASIBLE | 18 | 31 | 0.0 | 60.01 |
| `tiled-free-P16-D4.json` | VERIFIED TILING | 32 | 52 | — | 0 |
| `tiled-free-P16-D5.json` | VERIFIED TILING | 32 | 52 | — | 0 |
| `tiled-free-P24-D4.json` | VERIFIED TILING | 48 | 78 | — | 0 |
| `tiled-free-P24-D5.json` | VERIFIED TILING | 48 | 78 | — | 0 |

A bound in a `lex-` row applies to crossings at the fixed turn count. All other bounds apply to turns.
Negative turn bounds are weak solver bounds. They have no geometric meaning.

For UNKNOWN rows, T and X describe the independently checked input seed. The main solver did not return a solution.

VERIFIED TILING rows use no solver; their zero time entry means no solve was run.

For each result, the full JSON records the solver status and independent checks. The adjacent `-template.json` file holds the row list for the assembler.

### Exact templates and line pairings

Each offset entry `[r, d]` means line c joins line c+d when c mod P = r. All offsets are signed.

#### lanes-8-4.json

```text
26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7]]`.

#### lanes-P16-D4.json

```text
26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7], [8, 7], [9, 3], [10, 4], [11, 2], [12, -3], [13, -2], [14, -4], [15, -7]]`.

#### lanes-P16-D5.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7], [8, 7], [9, 3], [10, 4], [11, 2], [12, -3], [13, -2], [14, -4], [15, -7]]`.

#### lanes-P24-D4.json

```text
26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7], [8, 7], [9, 3], [10, 4], [11, 2], [12, -3], [13, -2], [14, -4], [15, -7], [16, 7], [17, 3], [18, 4], [19, 2], [20, -3], [21, -2], [22, -4], [23, -7]]`.

#### lanes-P24-D5.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7], [8, 7], [9, 3], [10, 4], [11, 2], [12, -3], [13, -2], [14, -4], [15, -7], [16, 7], [17, 3], [18, 4], [19, 2], [20, -3], [21, -2], [22, -4], [23, -7]]`.

#### lanes-P8-D5.json

```text
26 26 26 26 26 26 26 26
26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7]]`.

#### free-P16-D4.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
36 26 36 26 26 46 26 46 26 46 26 46 26 46 26 46
26 25 25 26 25 26 26 25 26 25 26 25 26 25 26 25
16 67 16 67 06 16 06 16 06 16 06 16 06 16 06 16
```

Offsets: `[[0, 9], [1, -5], [2, 9], [3, -5], [4, -15], [5, 15], [6, -15], [7, 15], [8, 5], [9, -9], [10, 5], [11, -9], [12, 5], [13, -5], [14, 5], [15, -5]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### free-P16-D5.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
26 26 26 26 26 26 26 56 26 26 26 26 26 26 26 26
26 26 46 56 46 16 26 46 26 34 26 36 26 26 46 36
25 15 26 26 25 25 25 25 26 25 26 25 26 25 26 26
67 06 16 01 16 16 06 16 06 16 67 16 67 06 16 16
```

Offsets: `[[0, 3], [1, 5], [2, -13], [3, -3], [4, 6], [5, 13], [6, -5], [7, -15], [8, 15], [9, 4], [10, -6], [11, -13], [12, 3], [13, -4], [14, 13], [15, -3]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### free-P24-D4.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
46 26 46 26 46 36 26 36 26 36 26 36 26 26 46 26 46 26 46 26 46 36 26 26
26 26 25 26 25 26 25 25 26 25 26 25 26 25 26 26 25 26 25 26 25 26 25 25
16 06 16 06 16 16 67 16 67 16 67 16 67 06 16 06 16 06 16 06 16 16 67 06
```

Offsets: `[[0, -5], [1, -11], [2, 7], [3, 5], [4, -5], [5, 13], [6, -9], [7, 13], [8, -5], [9, -7], [10, 3], [11, -19], [12, 3], [13, -3], [14, 11], [15, -3], [16, 19], [17, 5], [18, -13], [19, 5], [20, -13], [21, 9], [22, -5], [23, 5]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### free-P24-D5.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26 26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46 36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26 25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16 16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7], [8, 7], [9, 3], [10, 4], [11, 2], [12, -3], [13, -2], [14, -4], [15, -7], [16, 7], [17, 3], [18, 4], [19, 2], [20, -3], [21, -2], [22, -4], [23, -7]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### free-P8-D4.json

```text
26 26 26 26 26 26 26 26
36 26 26 46 26 46 36 26
25 26 25 26 26 25 26 25
16 67 06 16 06 16 16 67
```

Offsets: `[[0, 9], [1, -9], [2, -7], [3, 7], [4, -7], [5, 7], [6, 9], [7, -9]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### free-P8-D5.json

```text
26 26 26 26 26 26 26 26
26 26 26 26 26 26 26 26
26 46 36 26 36 26 26 46
26 25 26 25 25 26 25 26
06 16 16 67 16 67 06 16
```

Offsets: `[[0, -7], [1, 7], [2, 9], [3, -9], [4, 9], [5, -9], [6, -7], [7, 7]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### lex-free-P8-D4.json

```text
26 26 26 26 26 26 26 26
36 26 26 46 26 46 36 26
25 26 25 26 26 25 26 25
16 67 06 16 06 16 16 67
```

Offsets: `[[0, 9], [1, -9], [2, -7], [3, 7], [4, -7], [5, 7], [6, 9], [7, -9]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### lex-free-P8-D5.json

```text
26 26 26 26 26 26 26 26
26 26 26 26 26 26 26 26
26 46 36 26 36 26 26 46
26 25 26 25 25 26 25 26
06 16 16 67 16 67 06 16
```

Offsets: `[[0, -7], [1, 7], [2, 9], [3, -9], [4, 9], [5, -9], [6, -7], [7, 7]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### lex-lanes-8-4.json

```text
26 26 26 26 36 26 26 26
36 26 36 36 26 26 45 46
25 25 25 26 15 27 26 26
16 67 16 67 67 06 01 16
```

Offsets: `[[0, 7], [1, 3], [2, 4], [3, 2], [4, -3], [5, -2], [6, -4], [7, -7]]`.

#### tiled-free-P16-D4.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
36 26 26 46 26 46 36 26 36 26 26 46 26 46 36 26
25 26 25 26 26 25 26 25 25 26 25 26 26 25 26 25
16 67 06 16 06 16 16 67 16 67 06 16 06 16 16 67
```

Offsets: `[[0, 9], [1, -9], [2, -7], [3, 7], [4, -7], [5, 7], [6, 9], [7, -9], [8, 9], [9, -9], [10, -7], [11, 7], [12, -7], [13, 7], [14, 9], [15, -9]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### tiled-free-P16-D5.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
36 26 26 46 26 46 36 26 36 26 26 46 26 46 36 26
25 26 25 26 26 25 26 25 25 26 25 26 26 25 26 25
16 67 06 16 06 16 16 67 16 67 06 16 06 16 16 67
```

Offsets: `[[0, 9], [1, -9], [2, -7], [3, 7], [4, -7], [5, 7], [6, 9], [7, -9], [8, 9], [9, -9], [10, -7], [11, 7], [12, -7], [13, 7], [14, 9], [15, -9]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### tiled-free-P24-D4.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
36 26 26 46 26 46 36 26 36 26 26 46 26 46 36 26 36 26 26 46 26 46 36 26
25 26 25 26 26 25 26 25 25 26 25 26 26 25 26 25 25 26 25 26 26 25 26 25
16 67 06 16 06 16 16 67 16 67 06 16 06 16 16 67 16 67 06 16 06 16 16 67
```

Offsets: `[[0, 9], [1, -9], [2, -7], [3, 7], [4, -7], [5, 7], [6, 9], [7, -9], [8, 9], [9, -9], [10, -7], [11, 7], [12, -7], [13, 7], [14, 9], [15, -9], [16, 9], [17, -9], [18, -7], [19, 7], [20, -7], [21, 7], [22, 9], [23, -9]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.

#### tiled-free-P24-D5.json

```text
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26 26
36 26 26 46 26 46 36 26 36 26 26 46 26 46 36 26 36 26 26 46 26 46 36 26
25 26 25 26 26 25 26 25 25 26 25 26 26 25 26 25 25 26 25 26 26 25 26 25
16 67 06 16 06 16 16 67 16 67 06 16 06 16 16 67 16 67 06 16 06 16 16 67
```

Offsets: `[[0, 9], [1, -9], [2, -7], [3, 7], [4, -7], [5, 7], [6, 9], [7, -9], [8, 9], [9, -9], [10, -7], [11, 7], [12, -7], [13, 7], [14, 9], [15, -9], [16, 9], [17, -9], [18, -7], [19, 7], [20, -7], [21, 7], [22, 9], [23, -9]]`.

Lane-free: a full-tour pairing check is required before this gadget can support an upper bound.





















## Left crossings against right d=3/odd, 2026-10-02

Final depth-5/6 result: no gadget below 2 crossings per row was found. For Q=4 and Q=6, both depths are proved unable to improve 2. For Q=8, both 45-second runs ended without a solution or an infeasibility proof. No further search was run after this budget.
The value 2 is attained by the verified d=5/even gadget below, so it is the exact compatible minimum in the four proved size cases.
Initial search: Q=4,8,12 and D=2..5. After the Chief Researcher update, only Q=4,6,8 and D=5,6 are searched, with a hard no-{odd,odd+3} rule. The lane rule is disabled. The crossing objective is constrained to X < 2Q.
Right gadget: `23 27 / 23 27 / 23 27 / 23 27`, with pairs {c,c+3} for odd c. One CP-SAT worker; all solves are sequential.
The model uses kt.search.build_model, an exact cut-parity constraint, and lazy exclusions of finite alternating MID cycles. Mixed left pairings are allowed.
Every proposed improvement must pass independent strip checks, an exact periodic MID test, and w-integrator/strands.py region_check at n=256 and n=258. Only the MID region is used for acceptance.
A no-improvement proof applies only to the stated strip size. UNKNOWN means the time limit left the case open.

| Q | D | hard no-odd+3 | result | accepted X/row | solves | cycle cuts | seconds |
| ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| 4 | 2 | False | PROVED no compatible X < 2Q | — | 2 | 4 | 0.01 |
| 4 | 3 | False | PROVED no compatible X < 2Q | — | 2 | 4 | 0.02 |
| 4 | 4 | False | PROVED no compatible X < 2Q | — | 2 | 4 | 0.08 |
| 4 | 5 | False | PROVED no compatible X < 2Q | — | 2 | 4 | 0.17 |
| 8 | 2 | False | PROVED no compatible X < 2Q | — | 2 | 8 | 0.01 |
| 8 | 3 | False | PROVED no compatible X < 2Q | — | 2 | 8 | 0.06 |
| 8 | 4 | False | PROVED no compatible X < 2Q | — | 2 | 8 | 2.68 |
| 8 | 5 | False | TIME LIMIT; no improvement found | — | 2 | 8 | 40.02 |
| 12 | 2 | False | PROVED no compatible X < 2Q | — | 2 | 12 | 0.01 |
| 12 | 3 | False | PROVED no compatible X < 2Q | — | 2 | 12 | 0.1 |
| 12 | 4 | False | TIME LIMIT; no improvement found | — | 2 | 12 | 40.0 |
| 4 | 5 | True | PROVED no compatible X < 2Q | — | 1 | 0 | 0.16 |
| 4 | 6 | True | PROVED no compatible X < 2Q | — | 1 | 0 | 1.06 |
| 6 | 5 | True | PROVED no compatible X < 2Q | — | 1 | 0 | 7.58 |
| 6 | 6 | True | PROVED no compatible X < 2Q | — | 1 | 0 | 28.66 |
| 8 | 5 | True | TIME LIMIT; no improvement found | — | 1 | 0 | 45.01 |
| 8 | 6 | True | TIME LIMIT; no improvement found | — | 1 | 0 | 45.01 |

### Verified reference at 2 crossings per row

Template file: `w-turnsbuilder/cross-left-baseline-template.json`. Check file: `w-turnsbuilder/cross-left-baseline-check.json`.

```text
02 24
02 24
02 24
02 24
```

Q=4, D=2: X=8, T=8. Add straight `26` columns to extend the depth, and repeat the constant row for Q=6 or Q=8.
Line pairs are {c,c+5} for even c. Signed offsets are +5 for even c and -5 for odd c.
Both MID checks, n=256 and n=258, report zero finite cycles, four strands, and cut count [4].

### Scope of the hard-rule model

Every terminal path is oriented from its smaller to its larger line number. Its smaller endpoint is propagated as a label along selected edges. An even larger endpoint c is forbidden to have label c-3. This excludes all {odd,odd+3} pairs, including mixed matchings and paths with different shapes.
Label ranges extend six times the number of quotient cells beyond the terminal range. A finite path cannot repeat a quotient cell, and each knight step changes the row by at most two, so this range does not impose an extra span restriction.
The selected-edge parity across c=1/2 is constrained to be odd. For finite paths this equals the matching cut parity. It is necessary for MID compatibility with the rotated d=3/odd right gadget on an even board.
Before each hard-rule search, a separate fixed-edge control solve checked the 2/row reference in the same model, before the strict improvement bound was added. All six control solves returned OPTIMAL at X=2Q.
None of the six hard-rule searches produced a candidate below 2. Thus no new template passed or failed the MID filter in that final batch. The reference template did pass the filter.


Run evidence: `w-turnsbuilder/cross_left_results.jsonl`. Candidate checks and rejected-cycle data are saved separately in `cross_left_candidates.jsonl`.
