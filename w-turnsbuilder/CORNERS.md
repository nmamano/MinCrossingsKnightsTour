# Corner turn search

Date: 2026-10-02. One solver worker; all solves ran in sequence.
Target: minimize T - 8n. A more negative value is better. Each listed best tour passes kt.core.validate and the independent Integrator walk.
The search calls w-integrator/assemble.py through its assemble() function, with turn_weight=1000, objective="turns", and one Z value per call.
The turns objective uses 1000 per corner turn and 1 per crossing. Existing compatible full tours supply edge hints. Shared code is not changed.

## Best verified tours

| n mod 8 | n | T | T - 8n | X | tour file |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 56 | 434 | -14 | 530 | `w-turnsbuilder/corner_tours/baseline_n56.json` |
| 2 | 58 | 450 | -14 | 548 | `w-turnsbuilder/corner_tours/baseline_n58.json` |
| 4 | 60 | 466 | -14 | 570 | `w-turnsbuilder/corner_tours/baseline_n60.json` |
| 6 | 62 | 482 | -14 | 592 | `w-turnsbuilder/corner_tours/baseline_n62.json` |

## The twelve names give two distinct template sets

Group 0: b_T16/b_T16/l_free/l_d5lowm20; b_T16/b_T16/l_free/l_din{1,3,5}lowm20; b_T16/b_T16/l_d3lowm21/l_d5lowm20; b_T16/b_T16/l_d3lowm21/l_din{1,3,5}lowm20; b_T16/b_T16/l_din{1,3,5}lowm21/l_d5lowm20; b_T16/b_T16/l_din{1,3,5}lowm21/l_din{1,3,5}lowm20.
Group 1: b_T16/b_T16/l_d5lowm20/l_free; b_T16/b_T16/l_d5lowm20/l_d3lowm21; b_T16/b_T16/l_d5lowm20/l_din{1,3,5}lowm21; b_T16/b_T16/l_din{1,3,5}lowm20/l_free; b_T16/b_T16/l_din{1,3,5}lowm20/l_d3lowm21; b_T16/b_T16/l_din{1,3,5}lowm20/l_din{1,3,5}lowm21.

All equivalences above use exact row-list equality. The left and right templates have constant rows, so their vertical phases give the same graph. Bottom and top phases are tested separately.

## Runs

| n | group | Z | phases | T - 8n | status | seconds |
| ---: | ---: | ---: | --- | ---: | --- | ---: |
| 56 | 0 | 8 | [0, 1, 0, 0] | -14 | FEASIBLE | 20.57 |
| 58 | 0 | 8 | [0, 1, 0, 0] | -14 | FEASIBLE | 20.98 |
| 60 | 0 | 8 | [0, 1, 0, 0] | -14 | FEASIBLE | 23.35 |
| 62 | 0 | 8 | [0, 1, 0, 0] | -14 | FEASIBLE | 21.0 |
| 56 | 0 | 10 | [0, 1, 0, 0] | -14 | FEASIBLE | 20.73 |
| 58 | 0 | 10 | [0, 1, 0, 0] | -14 | FEASIBLE | 20.75 |
| 60 | 0 | 10 | [0, 1, 0, 0] | -14 | FEASIBLE | 20.91 |
| 62 | 0 | 10 | [0, 1, 0, 0] | -12 | FEASIBLE | 21.02 |
| 56 | 0 | 12 | [0, 1, 0, 0] | -14 | FEASIBLE | 21.07 |
| 58 | 0 | 12 | [0, 1, 0, 0] | -14 | FEASIBLE | 21.52 |
| 60 | 0 | 12 | [0, 1, 0, 0] | -14 | FEASIBLE | 21.25 |

No optimum across all corners or phases is claimed. Time-limited failures do not rule out a better tour. Results for four board sizes alone do not prove a formula for all larger sizes.
