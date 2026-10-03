# KT Lower Bounds - gap mission findings (gap/lowerbounds/)

Task: the open finite task of w-turnstheory/FINDINGS.md 11.3 (spec also in w-turnstheory/QUESTIONS.md,
"next task: fractional endpoint loss"). Coordinates: x = column (0 = side of the board), y = row.

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
