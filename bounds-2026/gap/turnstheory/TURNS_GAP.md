# Turns gap: corner traces, side phases, and the missing interior constraint

Date: 2026-10-04. Author: KT Turns Theory (Astra).

**Result for Lower Bounds.** A phase-only width-four ring with a free interior can attain corner residual `-28`, even with no cycle wholly in the ring. Explicit checked examples have `n = 40, 48, 64, 96`. They do **not** extend as supplied to degree-two boards. At `n = 48`, two inner cells receive three ring edges; another 38 inner cells receive two nonopposite ring edges and would have to turn. Thus a side-phase contradiction in this free-interior model cannot close the gap. The model must retain inner endpoint loads and the cost of forced inner turns. The relevant hand statements and reproducible data follow.

**Status.** No improvement of the global bound `8n - 28` is proved here. The corner pools are samples, not an exhaustive classification. The graph counts below are CHECK results from Lower Bounds' saved transfer graph; their row labels have been checked separately. The hand lemmas are marked PROOF.

## 1. PROOF: the exact slack that a stronger bound must force

Use the four-column lower terms from the audited proof. For a selected move pair at depth `x`, put

```
L_0 = 1,
L_1 = number of neighbours at depth 0 or 3, minus 1,
L_2 = number of neighbours at depth 0 or 3, minus 1,
L_3 = 1 minus the number of neighbours at depth 1 or 2,
L_x = 0 for x >= 4.
```

Let `t` be the turn indicator. Each side sums to `2n`. In a corner square, the audited certificate has `r=t-L_x-L_y >= alpha+D`, with `sum alpha=-7` and cancellation of `D`. Let `g_c=sum_corner r+7 >= 0`. At a cell in just one side strip put `rho=t-L_x >= 0`; let `I` be the cells in no strip. For `n>=8`, these sets partition the board, and

```
T - 8n + 28 = sum_four_corners g_c + sum_side_only rho + sum_I t.       (1)
```

All terms on the right are nonnegative integers. An exact `8n-14` lower bound is equivalent to proving that the right side is at least 14. In particular, equality at `8n-28` requires all four corners to be tight, every side-only cell to have zero local slack, and every interior cell to be straight. A ring that ignores the last requirement is only a relaxation.

This identity uses degree two, not connectivity.

## 2. PROOF: local equality cases and the row-current correction

The complete list of zero-slack move pairs has this short description:

| Depth | Equality condition | Number of pairs |
|---|---|---:|
| 0 | Any two of the four inward moves | 6 |
| 1 | Either two edges to depths 0/3, or a straight pair with exactly one such edge | 8 |
| 2 | Either two edges to depths 0/3, or a straight pair with exactly one such edge | 10 |
| 3 | Either two outward edges, or a straight pair with one backward edge | 10 |
| >=4 | A straight pair | 4 |

For depths 1 and 2, equality is `t=p-1`. Thus `p=0` is impossible, `p=1` requires straightness, and `p=2` requires a turn. At depth 3 it is `t=1-q`: `q=2` is impossible, `q=1` requires straightness, and `q=0` requires a turn. This proves the table without a solver.

**Zero slack does not mean exactly two turns in each row.** Orient each chosen strip edge between depth sets `{0,3}` and `{1,2}` from the former set to the latter. At a horizontal cut before row `y`, let `F(y)` be the signed number of these edges crossing the cut, positive upwards. Summing signed endpoints in row `y` gives

```
sum_x L_x(x,y) - 2 = F(y) - F(y+1),
row_turns(y) = 2 + F(y) - F(y+1) + sum_x rho(x,y).                    (2)
```

The `-2` is the degree-two contribution at depth zero. Each counted edge contributes `-1` at its depth-0/3 endpoint and `+1` at its depth-1/2 endpoint; this proves (2). On a periodic zero-slack strip the current telescopes, so the average is two. On a finite segment the two endpoint currents remain.

### 2.1. PROOF: an acyclic half-plane example with alternating one and three turns

The following table gives both moves at `(x,y)`. It is periodic in `y` with period two and extends to all `x>=0`:

| Depth | y even | y odd |
|---|---|---|
| 0 | `(1,2), (2,-1)` | `(1,-2), (1,2)` |
| 1 | `(-1,-2), (1,2)` | `(-1,-2), (-1,2)` |
| 2 | `(-1,-2), (1,2)` | `(-2,1), (1,-2)` |
| >=3 | `(-1,-2), (1,2)` | `(-1,2), (1,-2)` |

Every edge is reciprocal. All cells have degree two and zero local slack. The first four columns have one turn in an even row and three in an odd row. The odd-row depth-0/1 components are infinite zigzags along the side. Every other component has two rays going to unbounded depth. Thus there is no finite cycle. This example rules out the per-row interpretation even with a straight interior and no finite cycles.

### 2.2. PROOF: all eight translation-invariant half-plane patterns

For patterns invariant under `y -> y+1`, there are exactly eight zero-slack choices, indexed by signs `a,b,c in {-1,+1}`:

```
x=0:              (1,2a), (2,b)
x=1:              (-1,-2a), (2,c)
x>=2, x even:     +/-(2,b)
x>=3, x odd:      +/-(2,c).
```

Here all depths at least four are required to be straight.

To prove completeness, the two depth-zero edges cannot both go to depth one. That would fill depth one; depth two then cannot be straight through depth one or meet depth zero, and its only remaining zero-slack option would put two backward edges at depth three, which is forbidden. If both depth-zero edges go to depth two, depth one must send two edges to depth three, with the same contradiction. Hence depth zero sends one edge to each depth. Depth one cannot continue straight to depth two: the latter would then receive two nonopposite edges, only one of which is counted by `p`, violating equality. So depth one turns and sends its second edge to depth three. Depth two cannot also send an edge to depth three, since that would make `q=2`. The straight choices at depths two and three follow; straightness propagates each parity class to all larger depths. Conversely, all eight displayed fields satisfy every condition.

Each has two turns per row. They have no longitudinal phase. They are only the translation-invariant subfamily; they do not classify all zero-slack sides.

## 3. CHECK: finite side classification and phase propagation

Input: `gap/lowerbounds/turns_ring/strip_W4.pkl`, produced by Lower Bounds' `strip.py`. A cut state records the 16 possible in-strip edges crossing a horizontal cut. The saved reachable graph has 36,064 states and 856,330 arcs after keeping the cheapest row choice for each ordered state pair. This reduction preserves zero-cost reachability, since all local costs are nonnegative. Ghost endpoints beyond depth three have no degree constraint in this graph.

The recurrent zero-cost classes, in the order used in our JSON files, are:

| Class | States | Internal arcs | Period (gcd of closed-walk lengths) |
|---|---:|---:|---:|
| C0 | 1 | 1 | 1 |
| C1 | 1 | 1 | 1 |
| C2 | 2,657 | 16,636 | 1 |

C0 is `(a,b,c)=(+,+,-)` from Section 2.2; C1 is `(-,-,+)`. C2 contains the other six invariant fields and many nonconstant words. Every class has period one. Thus no universal parity or mod-3 restriction on a sufficiently long walk follows merely from membership in one of these classes. This does not assert that every small length connects every pair of states.

If one **additionally** requires two turns in every row, the recurrent classes instead have these `(states,arcs,period)` triples:

```
(1,1,1) twice; (2,2,2); (16,24,1) twice;
(122,259,1) twice; (370,988,1) twice; (511,1514,1).
```

That restriction removes valid zero-slack fields, including Section 2.1. It must not be imposed by the ring lower-bound calculation.

`turns_side_check.py` checks each saved zero arc directly from its move pairs and cut edges, checks (2), and recomputes the classes. It also saves a period-eight example with row counts `3,2,2,1,2,2,2,2`. This is an independent check of the labels, not an independent enumeration of all possible states or arcs.

A separate CP-SAT enumeration requires zero slack in a width-eight window, including straightness at depths 4..7, with unrestricted outgoing endpoints. Distinct vertical moves remain distinct in the lifted periodic graph, even when the period is one. It gives:

| Vertical period dividing P | Width | Labelled patterns | Enumeration status |
|---:|---:|---:|---|
| 1 | 8 | 8 | exhausted |
| 2 | 8 | 80 | exhausted |
| 2 | 12 | 80 | exhausted |
| 3 | 8 | 26 | exhausted |

For period two, 64 patterns have row counts `(2,2)`, eight have `(1,3)`, and eight have `(3,1)`. There are 36 primitive period-two orbits, plus the eight fixed patterns. For period three there are six primitive orbits, plus the eight fixed patterns. The finite windows alone do not prove that every listed pattern extends to the whole half-plane; Section 2 supplies proofs for its explicit families.

## 4. CHECK: corner optimum and near-optimum pools

`turns_gap_scan.py` uses the same model as `corner_integer_large.py`: degree two at every vertex of a `K x K` corner window, consistent edges inside it, and free endpoints outside. It fixes the total residual `sum(t-L_x-L_y)` to each requested level. A no-good cut after each accepted solution excludes its last-two-row move-pair projection on both four-column arms. Separate cuts remove any cycle wholly inside the window. Every saved witness is checked for internal reciprocity, its exact residual, and the absence of an internal cycle.

The unrestricted pool contains eight distinct interface samples for each of the eight `(K,residual)` combinations with `K=8,12` and residual `-7,-6,-5,-4`. Hence each window has a checked acyclic optimum at `-7`, since the audited corner bound already proves the matching lower bound. These are samples, not all optima.

A second pool requires each terminal four-column cut state to have a zero-cost continuation to some recurrent class. Results:

| K | Residual | Samples | Ordered continuation-class sets `(left,bottom)`, with multiplicities |
|---:|---:|---:|---|
| 8 | -7 | 8 | `({C1,C2},{C1,C2})` x7; `({C1,C2},{C1})` x1 |
| 8 | -6 | 8 | `({C1,C2},{C1,C2})` x5; `({C1},{C1,C2})` x2; `({C1,C2},{C1})` x1 |
| 8 | -5 | 8 | `({C1,C2},{C1,C2})` x8 |
| 8 | -4 | 8 | `({C1,C2},{C1,C2})` x8 |
| 12 | -7 | 8 | `({C1,C2},{C1,C2})` x4; `({C1},{C1,C2})` x4 |
| 12 | -6 | 8 | `({C1,C2},{C1,C2})` x7; `({C1,C2},{C1})` x1 |
| 12 | -5 | 2 | `({C1,C2},{C1,C2})` x2; next solve hit its time limit |
| 12 | -4 | 8 | `({C1,C2},{C1,C2})` x8 |

These are the exact forward zero-reachability sets of the recorded terminal states in the saved graph. A set is not a uniquely forced infinite pattern. All recurrent classes listed have period one, so the phase label is trivial at class level; the exact pending-edge state is still needed for short connections. All cut states, actual row words, moves, and arm slacks are in the JSON files. `turns_corner_interfaces.tsv` gives one line per witness and side.

The unrestricted samples often have terminal traces with no zero-cost infinite extension, despite zero-slack rows before the cut. This is a free-end artifact. The second pool removes that artifact at the width-four level. It still does not enforce degree two or straightness at the ghost endpoints.

## 5. CHECK: the free-interior ring does not supply the obstruction

Use sample 0 of the `K=8`, residual `-7` continuation pool at each corner, reflected into board coordinates. Keep its vertices at depth below four. Its terminal side states are 6995 and 15391. If a cut edge is represented as `(x,y,dx,dy)`, reflection of a cut sends it to

```
(x+dx, -1-y-dy, -dx, dy).
```

`turns_ring_witness.py` joins each terminal state to its reflected state by exactly `n-16` zero-cost rows. It checks every ring vertex and edge in the resulting coordinates. Successful examples:

| n | Ring residual | Cycles contained in ring | Ghost cells of degree >2 |
|---:|---:|---:|---:|
| 40 | -28 | 0 | 2 |
| 48 | -28 | 0 | 2 |
| 64 | -28 | 0 | 2 |
| 96 | -28 | 0 | 2 |

This particular sampled pair has no such join at `n=32`; that is not an impossibility result for other pairs.

At `n=48`, the overloaded cells and their ring neighbours are

```
(4,36):  (2,35), (2,37), (3,38)
(43,36): (44,38), (45,35), (45,37).
```

There are also 38 distinct ghost cells with two nonopposite incident ring edges. Even after fixing the overloads, these particular edges would force 38 inner turns. The complete ring is saved in `turns_ring_n48.json`.

**Consequence.** Any proof based only on corner residuals, width-four side traces, and the absence of ring-internal cycles accepts this example and cannot force an improvement over `-28`. This is not a counterexample to a stronger bound for tours or 2-factors. It identifies constraints absent from that relaxation.

## 6. PROOF: a compact exact description of a zero-turn interior

Let the interior be the `m x m` square at depth at least four, where `m=n-8`. Use the four unoriented knight directions `(1,2),(1,-2),(2,1),(2,-1)`. If an interior vertex is straight in direction `d`, then each adjacent interior vertex along `d` receives that edge and, if straight, must continue in the same direction. Induction propagates the choice along the entire lattice line segment in the interior square.

Introduce a Boolean variable for each such line segment. At each interior cell, exactly one of its four line variables must be selected. Conversely, any such exact cover gives consistent straight pairs throughout the interior. At line ends the same variables specify the incident ring edges, which must agree with the ring choices. For `m>=2`, each direction has `3m-2` lines, so this description has just `12m-8` Boolean variables.

This gives an exact interface contract for the zero-interior-turn case. It permits mixtures of line families; fixing one global direction is a restriction. For two different directions, compatibility of their lattice lines involves determinants of absolute value 3, 4, or 5. These congruences are possible sources of a true phase obstruction after the interior is included. No global modular inequality is asserted here.

For a near-optimum, (1) bounds the number of interior turns by the total slack budget. The same propagation holds along all line segments between those exceptional vertices. This suggests a bounded-defect extension of the line description.

## 7. Shared contract for Lower Bounds and remaining open steps

**PROOF / CHECK inputs that can reduce or correct the ring state space:**

1. Use the nonnegative cell slack in Section 2; do not require two turns in each row. If row turn counts are used as weights, include the current in (2).
2. A zero-cost arc need not carry a single binary or mod-3 phase. The large recurrent class and the explicit period-two half-plane field prevent that reduction without further constraints.
3. Track inner endpoint loads, at least through depth five. A degree-two ghost with nonopposite moves already costs an interior turn. The saved ring gives small explicit stop tests for both requirements.
4. At zero global excess, combine the ring with the exact line-cover contract of Section 6. The boundary ring alone does not enforce a single interior direction.
5. For tours, keep path-component pairings until the interior joins them. Acyclic corner windows and an acyclic ring are only necessary conditions. The complete union must have one component.

**OPEN.** Prove that every full-board configuration has total slack at least 14 in (1), or find tours with smaller slack. The sampled corner interfaces, even after zero-cost continuation, do not settle this. The corner pool is not exhaustive, and no minimal slack is claimed for the coupled ring-plus-interior problem.

A colour count over the entire even-width ring gives no new condition: degree two already makes its black and white cut-stub counts equal. A useful colour or congruence argument must use smaller regions or line families, rather than repeat that global equality.

## 8. Reproduction

Run from the research root with OR-Tools and NetworkX in `.venv`. Each CP-SAT solve uses one worker. No shared proof, blog, or Lower Bounds source was edited.

```sh
python3 gap/turnstheory/turns_hand_check.py
.venv/bin/python gap/turnstheory/turns_gap_scan.py --samples 8 --seconds 3
.venv/bin/python gap/turnstheory/turns_gap_scan.py --extend --samples 8 --seconds 8
.venv/bin/python gap/turnstheory/turns_side_check.py
.venv/bin/python gap/turnstheory/turns_periodic_side.py --width 8 --period 1 --limit 300
.venv/bin/python gap/turnstheory/turns_periodic_side.py --width 8 --period 2 --limit 300
.venv/bin/python gap/turnstheory/turns_periodic_side.py --width 12 --period 2 --limit 300
.venv/bin/python gap/turnstheory/turns_periodic_side.py --width 8 --period 3 --limit 1000
.venv/bin/python gap/turnstheory/turns_ring_witness.py
```

The two corner-pool commands, the side-graph check, and the ring-witness command read the saved Lower Bounds graph. The hand check uses only the standard library and independently enumerates all eight invariant patterns at widths 8 and 12. To regenerate that input, Lower Bounds can run `.venv/bin/python gap/lowerbounds/turns_ring/strip.py 4`; coordinate with that worker before overwriting its file. The graph-generation completeness is separate from our row-label check. Sample counts can change with time limits or solver versions. The saved coordinate witnesses are the objects checked here.

Measured on 2026-10-04: unrestricted corner pools used 35 seconds of solve time in total; continuation pools used about two minutes. Complete periodic enumerations took about 0.07, 1.14, 1.23, and 0.42 seconds respectively. These are discovery/check runs, not proof-producing SAT certificates.

## 9. CHECK / PROOF: integer windows through K=24 still attain -7

Date: 2026-10-04. **The integer minimum stays -7 at K=16, 20, and 24, with no internal cycle.** Thus these window sizes do not give the proposed `8n-24` lower bound. This is a checked local optimum, not a claim about a completed board.

### 9.1. Integer models and exact lower bound

`turns_large_corner.py` reruns the move-pair integer model of `w-turnstheory/corner_integer_large.py`, with two CP-SAT workers, 120 seconds per solve, and lazy cuts for any internal cycle. It adds the already audited redundant inequality `residual >= -7`. At K=16 and K=20 it optimizes the full integer model. At K=24 the `--tight` option keeps only equality cases of the audited local certificate: corner pairs have `r=alpha+D`, and all other pairs have `r=0`. Edge consistency is imposed on the union of possible edges at both endpoints, including edges whose opposite incidence was removed by this filtering.

The equality filtering is exact for deciding whether residual -7 is feasible. All local certificate gaps are nonnegative, and their sum is residual plus 7. Hence a -7 solution must use only these pairs. Conversely, consistent equality pairs sum to -7. The saved K=24 witness is also feasible for the original unfiltered integer model.

| K | Model | Solver status | Residual | Solver bound | Solve time | Internal cycles | Internal path components |
|---:|---|---|---:|---:|---:|---:|---:|
| 16 | Full integer optimization | OPTIMAL | -7 | -7 | 4.77 s | 0 | 24 |
| 20 | Full integer optimization | OPTIMAL | -7 | -7 | 114.74 s | 0 | 30 |
| 24 | Exact -7 equality model | OPTIMAL | -7 | -7 | 0.62 s | 0 | 38 |

All three final runs found an acyclic solution on their first trial, so no cycle cuts were needed. Solver: OR-Tools 9.15.6755. Times are measured on this machine on the date above. The saved JSON records the version and raw trial status.

**PROOF of local optimality, independent of trusting the solver bound.** The audited corner certificate plus the nonnegative residual outside the 4x4 corner gives a lower bound of -7 for every such window. The independently checked integer witnesses attain -7. Therefore the integer minimum is exactly -7, both with and without the internal-cycle restriction.

For each witness the residual split is exactly

```
4x4 corner residual = -7; side-only slack = 0; interior turns = 0.
```

### 9.2. What the K=20 boundary forces

The saved K=20 solution has 30 internal path components and 60 outgoing edges. Of these, 24 leave through the top only, 34 through the right only, and two leave through both coordinate bounds. They meet 58 exterior cells: 56 with one prescribed edge and two with two prescribed edges. No exterior cell is immediately overloaded, and the two prescribed pairs do not force a new interior turn.

Its entire 16x16 straight interior has the simple period-three rule

```
(x+y) mod 3 = 2:  moves +/-(1,2), at 86 cells;
(x+y) mod 3 = 0:  moves +/-(2,1), at 85 cells;
(x+y) mod 3 = 1:  moves +/-(2,1), at 85 cells.
```

This is a period-three mixture of two directions, distinct from the period-five fields reported in the whole-board data. Each direction changes x+y by 3, so the rule defines consistent straight lines in the bulk.

**CHECK.** This bulk rule agrees across the whole window boundary with both selected and unselected incidences at every exterior cell with x,y>=4. Thus it extends the straight bulk of this particular witness without changing any old window edge. The rows at depth 0..3 are not all periodic; the JSON records their exact choices and outgoing demands. Completing those two infinite side strips, and joining four corners on a finite board, remain separate requirements.

A zero-slack extension must propagate each deep outgoing edge straight until it reaches a side strip. The independent checker intersects every pair of the prescribed rays using exact rational arithmetic. For K=20 it finds no meeting that requires two distinct straight directions at one exterior lattice cell. This is a compatibility check of forced rays, not a proof of a full quadrant extension.

For comparison, the K=16 witness fails immediately outside the window: at `(16,5)` it prescribes edges from `(14,4)` and `(15,3)`. These moves are nonopposite, so extending that particular witness requires an interior turn. Its forced rays have 12 conflicting pairs in total. Larger windows can change the old witness, as the valid K=20 solution demonstrates.

The K=24 witness has 38 paths and 76 outgoing edges. Its straight interior uses `(1,2)` on residues 1 and 2 of x+y modulo 3, and `(2,1)` on residue 0. Its outgoing rays have no pairwise conflict, but extending that periodic bulk *unchanged* would add two edges absent from the old window: `(23,2)--(24,4)` and `(23,3)--(25,4)`. Thus absence of forced-ray conflicts alone is not an extension certificate. This distinction is included in the checker output.

### 9.3. Scope and independent checks

**OPEN.** These results neither establish tightness of `8n-28` on whole boards nor explain why the currently observed whole-board corners avoid -7. They rule out an improvement obtained merely by replacing the free 4x4 corner with these larger free integer windows.

There is also a logical distinction for any later positive result: a lower bound obtained *after forbidding internal cycles* applies to a corner of a sufficiently large single tour, but does not automatically apply to a general 2-factor, which may contain an entire cycle in that corner. A candidate `8n-24` theorem for all 2-factors would need the unrestricted window minimum to be at least -6, or a separate argument paying for excluded cycles. That issue does not affect the negative result here, since the sharp witnesses are acyclic.

`check_turns_large_corner.py` uses only the Python standard library. It checks every coordinate, knight move, degree-two pair, reciprocal internal edge, component, local corner certificate, exact residual, exterior load, and forced-ray intersection. It also checks the candidate period-three bulk against all possible boundary incidences, not only the selected outgoing edges. No solver result is needed for witness feasibility or for the matching -7 lower bound.

Reproduce the final runs and checks from the research root:

```sh
.venv/bin/python gap/turnstheory/turns_large_corner.py 16 --workers 2 --seconds 120
.venv/bin/python gap/turnstheory/turns_large_corner.py 20 --workers 2 --seconds 120
.venv/bin/python gap/turnstheory/turns_large_corner.py 24 --workers 2 --seconds 120 --tight
python3 gap/turnstheory/check_turns_large_corner.py \
  gap/turnstheory/turns_corner_integer_K16.json \
  gap/turnstheory/turns_corner_integer_K20.json \
  gap/turnstheory/turns_corner_integer_K24_tight.json
```

The witness files contain every selected move pair. Their `_check.json` companions contain the boundary ports, component counts, and extension tests. `turns_large_corner_checks.log` records the successful independent checks. Two-worker search may choose different witnesses on rerun; the files cited above are the checked objects. An audit can check those files first, then rebuild the integer model independently if it also wants to reproduce the search.
