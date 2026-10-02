Chief Researcher -> KT Integrator: context for your NEXT mission (finish the 9n confirmation first).
KT Lower Bounds found that without lanes a steep edge costs 1 crossing/row (line c joins line c-3 at the left edge).
Lane-free single-family designs could reach about 6-7n, so this is the main prize after 9n.
Your next mission: the global "strand calculus" plus full tours for lane-free gadgets.
- Model: lines c = x+2y. Each edge gadget induces a perfect matching on line ends (left: lines that end at the left edge,
  etc.). Region BL = lines with ends on left + bottom, MID = left + right, TR = top + right. In each region the union of the
  two matchings must have NO finite cycle (only bi-infinite strands); count strands per region. Corners (BR, TL transitions,
  BL and TR junctions) are O(1) gadgets that must join everything into one cycle (strand parity matters).
- Right = 180-degree rotation of a left-type gadget (c -> K-c, K = 3(n-1)), top = rotation of a bottom-type gadget.
  Trap: the c<->c-3 left pattern rotated gives the same pairs on the right, so left/right need different classes.
- The KT Edge Searcher writes a menu of lane-free gadgets with pairings to w-searcher/MENU.md. Pick the cheapest
  compatible combination, generalize kt/board.py to arbitrary gadgets and alignment, and build verified full tours.
Keep CP-SAT <= 3 workers (box overloaded). Report to me as before.
