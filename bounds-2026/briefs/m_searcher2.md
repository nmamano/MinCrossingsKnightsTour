Chief Researcher -> KT Edge Searcher: PRIORITY CHANGE (lead from KT Lower Bounds, see w-lowerbounds/FINDINGS.md F1).
Without the lane constraint, a steep edge costs only 1 crossing/row: for our family x+2y=c, add (0,y)-(1,y-2) at every row,
so line c (even) joins line c-3. The lane rule, not geometry, is what costs 2.5/row. So make LANE-FREE gadgets your main work.
Lane-based transfer-matrix proofs: park them unless they are nearly done.
1. Lane-free search (strip model with only degree + no-cycle constraints): min crossings per unit for the left edge (Q up to 8,
   D 2..5, off irrelevant) and the bottom edge (P up to 16, D 4..5), and the min-turns versions.
2. For each good gadget, record its PAIRING: the list of line pairs {c, c'} per period (unrolled), as offsets. The global
   cycle structure depends only on these pairings.
3. Important global trap: the right edge is a 180-degree rotation of a left-type gadget (c -> K-c, K=3(n-1) odd). The
   c<->c-3 pattern rotated to the right gives the SAME pairs {o,o+3} (o odd), so lines o and o+3 close into a 2-line cycle.
   Left and right need DIFFERENT pairing classes. So build a MENU: for the left type, the cheapest gadget for each
   pairing class you can force (e.g. pairs {c, c+d} with lower element of fixed parity, d in {1,3,5,-3,...}, or mixed
   periodic pairings), with its cost. Same for the bottom type.
Write the menu to w-searcher/MENU.md (cost, period, depth, template, pairing). The KT Integrator will combine menu entries
under the global strand condition. Keep CP-SAT at 2 workers; the box is overloaded (load 13 on 8 cores).
