# Minimum-turn LEFT gadget menu

Date: 2026-10-02. One CP-SAT worker; all solves ran in sequence.
Model: `kt/strip.py`, kind `left`, with the lane rule disabled. Q is rows per period; D is strip depth.
Each fixed class joins {c,c+d}, where c is the smaller line number and has the stated parity. The line is x+2y=c.
First minimize turns. Then fix that turn count and minimize crossings. Status T/X refers to these two solves for the selected size.
OPTIMAL proves the optimum for that size. A best menu entry is not a proof across other sizes whose runs remain incomplete.
Each template passes degree, symmetry, turn, crossing, and complete finite-path checks. Signed offsets and all run bounds are in `left_results.jsonl`.
Pairing `a+d` means {c,c+d} for c mod (2Q)=a, with c the smaller line number. Rows in each template are top-first.

| class | turns/row | crossings/row | status T / X | Q | D | pairing | template |
| --- | ---: | ---: | --- | ---: | ---: | --- | --- |
| d=1 low%2=0 | 3 | 2 | OPTIMAL / OPTIMAL | 4 | 3 | 0+1 2+1 4+1 6+1 | `01 24 25 / 01 24 25 / 01 24 25 / 01 24 25` |
| d=3 low%2=1 | 2 | 1 | OPTIMAL / OPTIMAL | 4 | 2 | 1+3 3+3 5+3 7+3 | `23 27 / 23 27 / 23 27 / 23 27` |
| d=5 low%2=0 | 2 | 2 | OPTIMAL / OPTIMAL | 4 | 2 | 0+5 2+5 4+5 6+5 | `02 24 / 02 24 / 02 24 / 02 24` |
| d=7 low%2=1 | 3 | 3 | OPTIMAL / OPTIMAL | 4 | 3 | 1+7 3+7 5+7 7+7 | `13 27 25 / 13 27 25 / 13 27 25 / 13 27 25` |
| d=9 low%2=0 | 3 | 4 | OPTIMAL / OPTIMAL | 4 | 4 | 0+9 2+9 4+9 6+9 | `02 14 26 25 / 02 14 26 25 / 02 14 26 25 / 02 14 26 25` |
| free | 2 | 1 | OPTIMAL / OPTIMAL | 4 | 2 | 1+3 3+3 5+3 7+3 | `23 27 / 23 27 / 23 27 / 23 27` |

## Classes with no gadget found

d=1 low%2=1: Q4 D2 INFEASIBLE, Q4 D3 INFEASIBLE, Q4 D4 INFEASIBLE, Q8 D2 INFEASIBLE, Q8 D3 INFEASIBLE, Q8 D4 INFEASIBLE.
d=3 low%2=0: Q4 D2 INFEASIBLE, Q4 D3 INFEASIBLE, Q4 D4 INFEASIBLE, Q8 D2 INFEASIBLE, Q8 D3 INFEASIBLE, Q8 D4 INFEASIBLE.
d=5 low%2=1: Q4 D2 INFEASIBLE, Q4 D3 INFEASIBLE, Q4 D4 INFEASIBLE, Q8 D2 INFEASIBLE, Q8 D3 INFEASIBLE, Q8 D4 INFEASIBLE.
d=7 low%2=0: Q4 D2 INFEASIBLE, Q4 D3 INFEASIBLE, Q4 D4 INFEASIBLE, Q8 D2 INFEASIBLE, Q8 D3 INFEASIBLE, Q8 D4 INFEASIBLE.
d=9 low%2=1: Q4 D2 INFEASIBLE, Q4 D3 INFEASIBLE, Q4 D4 INFEASIBLE, Q8 D2 INFEASIBLE, Q8 D3 INFEASIBLE, Q8 D4 INFEASIBLE.

## All size results

| class | Q | D | T | X | turn status | turn bound | cross status | cross bound |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: |
| free | 4 | 2 | 8 | 4 | OPTIMAL | 8.0 | OPTIMAL | 4.0 |
| free | 4 | 3 | 8 | 4 | OPTIMAL | 8.0 | OPTIMAL | 4.0 |
| free | 4 | 4 | 8 | 4 | OPTIMAL | 8.0 | OPTIMAL | 4.0 |
| free | 8 | 2 | 16 | 8 | OPTIMAL | 16.0 | OPTIMAL | 8.0 |
| free | 8 | 3 | 16 | 8 | OPTIMAL | 16.0 | OPTIMAL | 8.0 |
| free | 8 | 4 | 16 | 8 | OPTIMAL | 16.0 | OPTIMAL | 8.0 |
| d=1 low%2=0 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=1 low%2=0 | 4 | 3 | 12 | 8 | OPTIMAL | 12.0 | OPTIMAL | 8.0 |
| d=1 low%2=0 | 4 | 4 | 12 | 8 | OPTIMAL | 12.0 | OPTIMAL | 8.0 |
| d=1 low%2=0 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=1 low%2=0 | 8 | 3 | 24 | 16 | OPTIMAL | 24.0 | OPTIMAL | 16.0 |
| d=1 low%2=0 | 8 | 4 | 24 | 16 | OPTIMAL | 24.0 | OPTIMAL | 16.0 |
| d=1 low%2=1 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=1 low%2=1 | 4 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=1 low%2=1 | 4 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=1 low%2=1 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=1 low%2=1 | 8 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=1 low%2=1 | 8 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=3 low%2=0 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=3 low%2=0 | 4 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=3 low%2=0 | 4 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=3 low%2=0 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=3 low%2=0 | 8 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=3 low%2=0 | 8 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=3 low%2=1 | 4 | 2 | 8 | 4 | OPTIMAL | 8.0 | OPTIMAL | 4.0 |
| d=3 low%2=1 | 4 | 3 | 8 | 4 | OPTIMAL | 8.0 | OPTIMAL | 4.0 |
| d=3 low%2=1 | 4 | 4 | 8 | 4 | OPTIMAL | 8.0 | OPTIMAL | 4.0 |
| d=3 low%2=1 | 8 | 2 | 16 | 8 | OPTIMAL | 16.0 | OPTIMAL | 8.0 |
| d=3 low%2=1 | 8 | 3 | 16 | 8 | OPTIMAL | 16.0 | OPTIMAL | 8.0 |
| d=3 low%2=1 | 8 | 4 | 16 | 8 | OPTIMAL | 16.0 | OPTIMAL | 8.0 |
| d=5 low%2=0 | 4 | 2 | 8 | 8 | OPTIMAL | 8.0 | OPTIMAL | 8.0 |
| d=5 low%2=0 | 4 | 3 | 8 | 8 | OPTIMAL | 8.0 | OPTIMAL | 8.0 |
| d=5 low%2=0 | 4 | 4 | 8 | 8 | OPTIMAL | 8.0 | OPTIMAL | 8.0 |
| d=5 low%2=0 | 8 | 2 | 16 | 16 | OPTIMAL | 16.0 | OPTIMAL | 16.0 |
| d=5 low%2=0 | 8 | 3 | 16 | 16 | OPTIMAL | 16.0 | OPTIMAL | 16.0 |
| d=5 low%2=0 | 8 | 4 | 16 | 16 | OPTIMAL | 16.0 | OPTIMAL | 16.0 |
| d=5 low%2=1 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=5 low%2=1 | 4 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=5 low%2=1 | 4 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=5 low%2=1 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=5 low%2=1 | 8 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=5 low%2=1 | 8 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=0 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=0 | 4 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=0 | 4 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=0 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=0 | 8 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=0 | 8 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=1 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=1 | 4 | 3 | 12 | 12 | OPTIMAL | 12.0 | OPTIMAL | 12.0 |
| d=7 low%2=1 | 4 | 4 | 12 | 12 | OPTIMAL | 12.0 | OPTIMAL | 12.0 |
| d=7 low%2=1 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=7 low%2=1 | 8 | 3 | 24 | 24 | OPTIMAL | 24.0 | OPTIMAL | 24.0 |
| d=7 low%2=1 | 8 | 4 | 24 | 24 | OPTIMAL | 24.0 | OPTIMAL | 24.0 |
| d=9 low%2=0 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=0 | 4 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=0 | 4 | 4 | 12 | 16 | OPTIMAL | 12.0 | OPTIMAL | 16.0 |
| d=9 low%2=0 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=0 | 8 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=0 | 8 | 4 | 24 | 32 | OPTIMAL | 24.0 | OPTIMAL | 32.0 |
| d=9 low%2=1 | 4 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=1 | 4 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=1 | 4 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=1 | 8 | 2 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=1 | 8 | 3 | — | — | INFEASIBLE | 0.0 | — | — |
| d=9 low%2=1 | 8 | 4 | — | — | INFEASIBLE | 0.0 | — | — |
