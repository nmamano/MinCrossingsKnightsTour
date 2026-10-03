# KT Lower Bounds - gap mission findings (gap/lowerbounds/)

## STATE AT THE PIVOT (2026-10-03): strip work stopped by order; nothing running

Done: L1 (11.3, beta=1 exact), L2 (field survives in a closed tour), L3 (R1, beta=4/3), L4 (combined credit,
beta=16/11, C++ match by Edge Searcher; audited by the Verifier as Claim 27). Half-done: L5 below.

## L5 (2026-10-03, HALF-DONE at the pivot): Edge Searcher's joint model (columns 0..5, exact F23/J crossings)

Spec agreed with KT Edge Searcher (their gap/searcher/FINDINGS.md 6.3): S, F23 = col2-col3, J = col3-col4/5;
cols 0,1,3 degree exactly 2, cols 2,4,5 <= 2; row weight q(4W-4)+p(4W0-4)+4q*Wx-2pt. Edge Searcher (first
implementation, up only, labels on S only) reports beta* = 2 exact, critical cycle = the period-6 field of L4.

My data (MEASURED, CP-SAT, joint/field_joint_cost.py; S fixed to a field, cheapest F23+J completion, column 3
exact on all rows but 3 at each end, lazy no-cycle cuts):
- period-6 c=0 field of L4: wx = 0, 2, 4 for 24, 36, 48 rows (all OPTIMAL): 1 crossing per 6 rows, so its
  joint ratio is (4+1)/(5/2) = 2. This agrees with Edge Searcher's critical cycle.
- saturated field: wx = 14, 38 for 24, 48 rows (FEASIBLE only, slope about 1 per row, as the interval lemma says).
- cheap field (mirror P): wx = 0.
Not done: my second implementation (joint/joint_graph.py, a from-spec state enumerator, written but never run
to completion; no state count yet), the down orientation, and the reduction (Turns Theory R3).
Resume: run `../../../.venv/bin/python joint/joint_graph.py` for the state count, then add the row-level
endpoint/parity augmentation as in combo_stab.py.

## L4 (2026-10-03): combined credit (N1)/(N2) certified at beta = 16/11; 16/11 is exact in this model

Task: gap/turnstheory/FINDINGS.md "Route past 52/11: combine the two credits". **Finite certificate:
PROVEN by one implementation (combo_stab.py); the independent second implementation is KT Edge Searcher's
C++ check (pending).** CONDITIONAL as a bound on: U1 (boundary surplus reduction), the interval lemma behind K
(Turns Theory, not yet audited), and the N1 combination argument.

Integer weights per row arc (row-level graph, 4 cell arcs per row):
q*sum(4w-1) + p*sum(4w0-1) + 4q*k - 2p*t, with k the blocked-run charge (run constant 4) and t = 2a.

| orientation | beta* | potential range (units 1/(4q) = 1/44) | C |
| --- | --- | --- | --- |
| up | 16/11 | -596..0 | 149/11 |
| down | 16/11 | -596..0 | 149/11 |

Dinkelbach from 8/3: an 18-row cycle (ratio 3/2), then the 8-row cycle below (ratio 16/11), then convergence.
Coefficient if all conditions hold: 4 + 2beta/(2beta+1) = 4 + 32/43 = 204/43, about 4.744 (vs 52/11, about 4.727).

**Blocking field (period 8, explicit check check_combo_obstruction.py, no transfer-graph code):**

    (1,y)-(0,y+2), (2,y)-(0,y+1)       every y
    (2,y)-(1,y+2)                      if y mod 8 != 2
    (3,y+1)-(1,y+2)                    if y mod 8 == 2

It is the saturated field of 11.4 with one edge moved every 8 rows. Per 8 rows: 16 crossings (excess 8),
8 boundary pairs (R = 0), blocked rows 1,2,5,6,7 mod 8, so runs of length 2 and 3 and K = 0; sum a = 11/2 in
the bad phase (both orientations). Ratio 8 / (11/2) = 16/11. The moved edge costs no crossing, breaks the
blocked runs below the run constant 4, and lowers the penalty only from 6 to 11/2 per 8 rows.

Model details: node = (phase-0 base state, parity, 4-bit history cand(r-1), cand(r), b2(r-1), b2(r),
run counter 0..4); 21,420 phase-0 states, 250,990 row paths, 40,158,400 augmented arcs, 2.5 GB, about 4 min
per orientation. All initial parities, histories and counters are start nodes. check_combo_history.py checks
the compressed automaton against the raw definition (blocked(y): d3(y)=0, d2(y-2)=d2(y+2)=2; K = sum
max(0, l-4)) on 18,000 random degree sequences, run constants 0..5.

```sh
cd gap/lowerbounds
../../.venv/bin/python combo_stab.py crit up 8/3     # combo_crit_up.log
../../.venv/bin/python combo_stab.py crit down 8/3   # combo_crit_down.log
../../.venv/bin/python combo_cycle_show.py up        # writes combo_field_up.json
python3 check_combo_obstruction.py                   # explicit field, ratio 16/11 (check_combo_obstruction.log)
python3 check_combo_history.py                       # history automaton vs raw definition
CAP=c ../../.venv/bin/python combo_stab.py crit up 8/3   # run constant c instead of 4
```

**Sensitivity to the run constant (up orientation, 2026-10-03; K = sum max(0, l - c)):**

| run constant c | beta* | blocking cycle | coefficient 4 + 2beta/(2beta+1) |
| --- | --- | --- | --- |
| 4 (current lemma) | 16/11 | period-8 field above, K = 0 | 204/43 ~ 4.744 |
| 3 | 16/11 | same | 204/43 |
| 2 | 3/2 | 6 rows, sum(4w-1) = 24, k = 0, t = 8 | 19/4 = 4.75 |
| 1 | 3/2 | 8 rows, sum(4w-1) = 24, k = 0, t = 8 | 19/4 |
| 0 (every blocked row pays) | 8/5 | period-6 field below, no blocked row | 100/21 ~ 4.762 |

So a sharper interval lemma alone can reach at most beta = 8/5 in this model. The limit at c = 0 is a field with
no blocked row at all (check_cap0_obstruction.py, explicit; same ratio in both orientations):

    (1,y)-(0,y+2), (2,y)-(0,y+1)       every y
    (2,y)-(1,y+2)                      if y mod 6 in {0, 4, 5}
    (3,y)-(1,y+1)                      if y mod 6 in {2, 3, 4}

Per 6 rows: 10 crossings (excess 4), R = 0, K = 0, max sum a = 5/2; ratio 8/5. Any credit past 8/5 must charge
this field. Logs: combo_crit_up_cap{0,1,2,3}.log, check_cap0_obstruction.log.

## L3 (2026-10-03): request R1 (boundary credit) is certified at beta = 4/3, and 4/3 is exact

Answer to gap/turnstheory/REQUESTS.md R1. **PROVEN finite certificate (two implementations).**

With w0 = new crossing pairs whose two edges both have an endpoint in column 0, the integer weights

    q*(4w-1) + p*(4w0-1) - 2p*t        (t = 2a at row end, a from w-turnstheory FINDINGS 11.2)

admit a converged potential at beta = p/q = 4/3, in both orientations, both initial parities:

| orientation | potential range (units 1/(4q) = 1/12) | C |
| --- | --- | --- |
| up | -155..0 | 155/12 |
| down | -159..0 | 159/12 = 53/4 |

So on every oriented half walk, (X_sigma - length) + (4/3)(B_sigma - length) >= (4/3) sum a - 53/4.

**beta = 4/3 is exact** (PROVEN): a Dinkelbach search started at 3/2 finds a 6-row negative cycle with
sum(4w-1) = 24, sum(4w0-1) = 0, sum t = 9 (2 crossings, 1 boundary crossing, penalty 3/4 per row: the old
saturated period-one field of 11.4), ratio 24/(18-0) = 4/3; the search then converges at 4/3.

Consequence, IF Turns Theory's reduction U1 (gap/turnstheory/FINDINGS.md, "pending external review") holds:
X >= [4 + 2beta/(2beta+1)] n - O(1) = 52n/11 - O(1), about 4.727n. The reduction itself is not checked by me.

Checks: r1_stab.py recomputes w for every base arc from the two states and asserts equality with strip_dp's
stored w; r1_independent.py does the same with strip2_independent.proper and its own set-of-edges augmented
graph. Both give the ranges above.

```sh
cd gap/lowerbounds
../../.venv/bin/python r1_stab.py crit up 4/3      # converged at 4/3, range -155..0 (r1_crit_up.log)
../../.venv/bin/python r1_stab.py crit down 4/3    # converged at 4/3, range -159..0 (r1_crit_down.log)
../../.venv/bin/python r1_stab.py crit up 3/2      # cycle -> 4/3, then converged (r1_crit_up_from32.log)
python3 r1_independent.py up 4 3                   # independent: -155..0 (r1_independent.log)
python3 r1_independent.py down 4 3                 # independent: -159..0
```

## L2 (2026-10-03): the L1 field survives in a single closed tour; connectivity does not make it expensive

**Verdict: the connectivity route is dead for this field.** A closed tour that carries the field on 64 rows of
one side (penalty a = 1 on all 64 rows) costs only 61 crossings more than the tour it came from, i.e. no more
than the field's own strip excess (64). So a single-cycle argument cannot raise the field's ratio above 1.
The obstruction is removed instead by the boundary credit of R1 (L3).

**PROVEN (parity lemma, check_field_parity.py).** Every cut between two rows is crossed by an even number of
tour edges. In the field, the edges with an end in column 0 or 1 that cross a cut are odd in number (3 or 5);
in P and mirror P they are 4. So on every row of a field run, an odd number of crossing tour edges lie wholly
in columns >= 2. The field cannot be closed near its two ends alone; the closure must cross every row of the
run. In the tour below the crossing-free folds carry it.

**VERIFIED instance (conn/FIELD_n166_92_155.json, 2026-10-03).** Start: FOLD24_n166 (X = 1179). Force the field
(phase 0) on left-side rows 92..155. CP-SAT (2 workers, 900 s, conn/field_global.py) re-solves the left band
(columns 0..5, rows 86..161) and bands of half-width 3 around the midline fold (row 83) and the anti-diagonal
fold (x+y = 166), all other edges fixed: best 2-factor +59, 13 cycles. A greedy 2-swap merge with exact
crossing deltas (conn/merge.py) joins them: 11 merges cost 0 or less, the last two cost 4 each. Result: one
closed tour, X = 1240 (+61). verify_field_tour.py (no CP-SAT code; crossings by kt/core.py crossing_list)
checks the Hamiltonian cycle, X = 1240, all field edges present, and sum a = 64 over rows 92..155 in the
top-left corner frame (original tour: 0).

Earlier band tests on 16 rows (conn/field_band.py): no closure inside columns 0..3 (INFEASIBLE, matches the
parity lemma); closure inside columns 0..5 found at +49 (not optimal). The folds are the cheap carrier.

```sh
cd gap/lowerbounds && python3 check_field_parity.py
cd conn && ../../../.venv/bin/python verify_field_tour.py FIELD_n166_92_155.json FOLD24_n166 92 155 0
# rebuild (about 20 min, 2 workers): field_global.py 92 155 0 6 6 3 900 900 one; merge.py twofactor_92_155_0.pkl
```

## L1 (2026-10-03): the fractional endpoint certificate has beta* = 1 exactly. No improvement on 14n/3.

**Verdict.** In the width-two forest strip, with the half-unit penalties a of 11.2 and the row parity in the
state, the best coefficient in (11.5) is beta = 1 for BOTH orientations and BOTH initial parities.

- **PROVEN (exact certificate, two implementations):** beta = 1 holds with integer potentials in [-29, 0]
  (units 1/4), so C = 29/4 for `up` and for `down`. This only gives back the coefficient 14/3 of 10.5.
- **PROVEN (explicit field, checked without the transfer graph):** no certificate with beta > 1 exists.
  The blocking cycle is a period-4 field with sum(w - 1/4) = 1 per row and penalty a = 1 at every row.

Consequence: (11.6) with beta = 1 gives 4 + 2/3 = 14/3. The 11.3 route does not narrow the gap.

### The blocking field (period 4 rows)

For every row y:

    (2,y)-(0,y+1),  (3,y)-(1,y+1)          long edges, all on the lines x + 2y = const
    (1,y)-(0,y+2)   if y mod 4 != 3        column 0-1 joins of the cheap pattern (mirror of P)
    (0,y)-(1,y+2)   if y mod 4 == 1        one reversed column 0-1 join per period

It is the cheap pattern (mirror P) with one column 0-1 join reversed every 4 rows. Facts (checked):

- columns 0, 1 have degree 2, columns 2, 3 have degree 1, no cycle;
- 8 proper crossings per 4 rows, so sum(w - 1/4) = 1 per row (excess 1 per row over the 4n term);
- no inward exception (one of the two EXC edges at each row);
- up test: F mod 3 = 1, 0, 1, 0, ...; with the right parity phase h = 1 at every row, so a = 1 at every row.
  The other phase gives h = 0, a = 1/2. The down test on the same field gives F = 0, 1, 0, 1, ... and
  again h = 1, a = 1 at every row for one phase (the search found this field shifted by 2 rows).
- the same field is the cycle found by the Dinkelbach search in both orientations (16 arcs = 4 rows).

Compare the 11.4 field: 2 crossings per row, a = 1, 1/2 alternately, ratio 4/3. The new field has the same
crossing rate but keeps h = 1 (penalty 1) on both parities, so its ratio is 1.

### Why this is a limit of the whole route, not of the penalty table

**PROVEN (short argument).** Any additive endpoint table a_c(h) (it can depend on the parity c) that pays
for lost paths must satisfy a_c(1) + a_c(2) >= 1 (the pair (1,2) loses the path, and both ends of gamma_R
use the same radius R, so the same c). The cheap patterns P/P' have h = 2 at every row and zero excess,
so a certificate with beta > 0 needs a_c(2) = 0. Thus a_c(1) >= 1 for both c, and the field above, with
h = 1 at every row, has ratio at most 1. So beta <= 1 for every such table.

The loss is also real, not an artifact of the split: if the left side carries this field and the bottom side
carries P/P' (h = 2), then h_left + h_bottom = 0 mod 3 at every radius and every candidate path in that range
is lost, at a cost of one excess crossing per path.

**PROVEN (explicit check): wider strips do not help.** Add (x,y)-(x+2,y-1) for 2 <= x <= k-1. For every
width k = 2..8 the result is a valid S_k configuration (strip degree 2, ghosts <= 2, no cycle) with the same
8 crossings per 4 rows and the same edges in columns 0..2, so the same endpoint data. All long edges lie on one
parallel family, so the argument holds for every k. Thus no strip certificate of any width, with this residue
test and additive penalties, reaches beta > 1.

### What would be needed to go past 14n/3 on this route (ARGUMENT, not checked)

The configuration "this field on one side, cheap pattern on the other side of the corner" satisfies all local
inputs of the 14n/3 proof with equality (one excess crossing per lost path). Any improvement must make this
configuration more expensive by a fact that is not in a single side strip, for example:
1. a joint condition on the two sides of a corner (the field needs h = 1 on one side and h = 2 on the other at
   the same radius);
2. a different charged curve for the lost radii (other path shapes through the same corner region);
3. a stronger square budget than 2L <= 4E + 44 when such fields are present;
4. global connectivity: the reversed joins change how the line ends pair up. Every reversed join is a choice
   the tour pays for; a single-cycle argument might force or forbid it.

### Data and commands (each run is about 25 s, one core)

```sh
cd gap/lowerbounds
../../.venv/bin/python frac_stab.py crit up       # Dinkelbach from 4/3 -> cycle ratio 1 -> converged at 1, range -29..0
../../.venv/bin/python frac_stab.py crit down     # same
../../.venv/bin/python frac_stab.py up 1 1        # certify one beta (writes frac_pot_*.npy)
python3 frac_independent.py up 1 1                # independent set-of-edges checker: converged, range -29..0
python3 frac_independent.py down 1 1              # same
../../.venv/bin/python frac_cycle_show.py up      # print the cycle as a field, re-check on an unrolled copy
python3 check_frac_obstruction.py                 # explicit field, no transfer-graph code: ratio exactly 1
python3 check_frac_obstruction_wide.py            # the field extends to widths 2..8 at no extra crossing
```

Logs: crit_up.log, crit_down.log, frac_independent.log, check_frac_obstruction.log,
check_frac_obstruction_wide.log. frac_cycle_{up,down}.npy are the arc lists of the found cycles (arc indices
of the frac_stab.py graph). frac_pot_{up,down}_1_1.npy (12 MB each) are the beta = 1 potentials; they can be
rebuilt with the commands above and need not be synced.

Code copied (unchanged) from w-lowerbounds/: strip_dp.py, strip2_independent.py. frac_stab.py follows
w-lowerbounds/endpoint_stab.py; frac_independent.py follows w-lowerbounds/endpoint_independent.py. Both add
the parity bit and the charge t = 2a of 11.2 (identical to score() in w-turnstheory/check_endpoint_loss.py).
Augmented graphs: frac_stab 1,112,872 used nodes (up), 2,095,620 arcs; frac_independent 188,112 nodes and
338,200 arcs (up), 335,564 nodes and 630,778 arcs (down).
