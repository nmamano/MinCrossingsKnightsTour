# Audit request to Chief Researcher — 2026-10-03: proposed 52n/11 bound

**Full proof ready for KT Verifier: `PROOF_52_11.md`.** KT Lower Bounds
certified request R1 at beta=4/3 in both orientations and both initial
parities, with two implementations. I read its code and logs and reran
the independent certificate in each orientation. The ranges are -155..0
and -159..0 in units of 1/12. The complete reproduction runner is
`check_52_11.py`.

**PROOF SUBMITTED FOR REVIEW, not an audited result:** every closed tour
on an even board n>=32 satisfies

```
X >= 52n/11 - 360.
```

This improves the leading coefficient by 2/33. With the retained
boundary surplus R, the exact inequalities are

```
4n <= 4E + 2(A-R) + 156,
(4/3)*(A-R) <= E+1208,
4n <= (11/2)*E+1968,
X >= 52n/11-3958/11 >= 52n/11-360.
```

The pending external review should focus on the actual boundary union
budget, the eight half-walk sum with far-corner parity, and cancellation
of R. The full proof defines every quantity and gives the exact corner
overcount constants. The audited 14/3 theorem and published files remain
unchanged. Chief Researcher has assigned Claim 26 to KT Verifier. The
proof now includes an exact section-by-section delta against the audited
document and every component check command.

**Checks passed on 2026-10-03:** all six local checks, both freshly rerun
independent strip certificates, and the rational constant calculation.
`check_52_11_report.json` records the results. The aggregate run used
`--reuse-stability-logs` to read the two successful runs from this same
session; its default command reruns them. No check was omitted.

## Request status

R1 is complete at beta=4/3. No additional finite computation is requested
until the proof audit is complete. The saturated period-one field proves
that 4/3 is the exact limit of R1. Combining the inner-boundary lemma
with R1 is a possible later task, but is not an input to this proof.

## Route past 52/11: combine the two credits

2026-10-03. **ARGUMENT for a new finite task; no larger beta is claimed.**
The two known obstructions now have separate costs. R1 pays for the
period-4 reversal field with its boundary surplus. The blocked-interval
lemma below pays for the saturated field with interior crossings.
Together they suggest a stronger certificate than either alone.

Let `K` be the sum, over all sides, of `max(0,l-4)` over blocked runs of
length l. The interval certificate below gives additional crossings
outside each side's width-two strip, and only a constant corner
overcount across sides. Thus `D0+K <= E+O(1)`. Seek a finite certificate

```
beta*A <= D0 + K + beta*R + O(1).                     (N1)
```

The same square budget then gives
`X >= [4+2beta/(2beta+1)]n-O(1)`. Hence any beta>4/3 would pass 52/11.
With `k` the zero-or-one blocked-run charge per row and `t=2a`, the new
integer arc weight for beta=p/q would be

```
q*(4w-1) + p*(4w0-1) + 4q*k - 2p*t.                 (N2)
```

The ghost-degree history and run counter needed for k are specified in
Section 4 of the earlier report below. This augmentation is larger than
R1, so it should wait until Claim 26 is complete.

On the saturated field, `D0/length=1`, `K/length -> 1`, `R/length=0`,
and `A/length=3/4`; it imposes only beta<=8/3 on (N1). On the period-4
field in its costly parity phase, the respective rates are 1, 0, 1, 1,
so it imposes no beta limit. Cheap fields still have all four rates zero.
Thus neither known obstruction rules out beta>4/3 for the combined task.

**Unresolved:** another periodic field, or short saturated runs separated
by low-cost transitions, can still block (N2). The interval lemma loses
four crossings per run. No certificate beyond 4/3 follows without the
new finite check. The existing exact interval certificate itself still
needs the Verifier's separate review before use in a new global theorem.

---

# Earlier update — 2026-10-03: keep actual boundary crossings

**New priority: request R1 in `REQUESTS.md`. No global improvement is
claimed.** I read KT Lower Bounds' L1 and checked the new period-4 field.
It has no blocked rows, so it defeats the blocked-run-only proposal
below. The interval lemma remains valid, but that proposal alone cannot
pass beta=1. Its requested computation is superseded by R1.

The new field also gives a better lead: all eight crossings per four
rows belong to the outer-column boundary set. The current proof replaces
that set's size by its lower bound, and loses this surplus. Keeping the
actual size gives a stronger square budget and a new finite task with
the SAME strip state space.

## U1. Exact boundary surplus in the square budget

**PROVEN algebraic reduction, pending external review.** Let `b_sigma`
be the actual number of crossing pairs whose two edges both touch the
outermost column of side sigma. This is the size of that side's original
set `B_sigma` in the audited proof, not its width-two crossing count
`X_sigma`. Define

```
R = sum_sigma b_sigma - 4n,
D = sum_sigma X_sigma - 4n,
E = X - 4n + 2.
```

All candidate paths and endpoint tests stay as in old Section 11. The
union `B` satisfies `|B| >= sum_sigma b_sigma - O(1)`, since duplicate
pairs occur only in fixed corner regions. Each retained path still
avoids every overlap from `B`, regardless of how large `B` is. The
original bad-quarter budget therefore gives

```
2L <= 2E + 2(X-|B|) <= 4E - 2R + O(1).
L >= 2n - A - O(1).
4n <= 4E + 2(A-R) + O(1).                             (U1)
```

Suppose a finite certificate, summed over the eight oriented half-side
walks, gives

```
beta*A <= D + beta*R + O(1).                          (U2)
```

The actual strip crossings still give `D<=E+O(1)`. Thus
`A-R<=E/beta+O(1)`, and (U1) yields

```
X >= [4 + 2beta/(2beta+1)] n - O(1).                  (U3)
```

The new potential task for beta=`p/q` is

```
q*(4w-1) + p*(4w0-1) - 2p*t >= potential change,
```

where `w0` counts introduced crossing pairs with BOTH edges incident to
column zero and `t=2a` is charged at row end. The subtracted constants
apply to every cell transition. `w0` uses the same new and pending edges
as the old crossing weight `w`; it needs no larger state space. Splitting
a strip walk preserves these assigned crossing totals. Half-strip end
errors are bounded just as in 11.3.

**OPEN:** a certificate for any beta>1. R1 requests beta=4/3 first, then
any beta>1 or a blocking cycle. The saturated field still limits this
specific certificate to beta<=4/3. The period-4 field from L1 imposes no
such limit on the new inequality: it has `D=4`, `R=4`, `A=4` per period
in its bad parity phase, so (U2) has slack four for every beta.

## U2. Checks on the new obstruction

**PROVEN finite local calculations, checked on 2026-10-03.** Run

```
python3 gap/turnstheory/check_boundary_credit.py
```

The script directly checks proper crossings and column-zero incidence,
without the transfer graph. Per four rows it finds:

| Field | Width-two crossings | Outer-column crossings | Blocked rows |
| --- | ---: | ---: | ---: |
| New period-4 obstruction | 8 | 8 | 0 |
| Old saturated obstruction | 8 | 4 | 4 |
| Cheap field | 4 | 4 | 0 |

The new period-4 field also has four crossing pairs with a one-quarter
overlap per period, two triple-covered quarters, and two empty quarters
in square column zero. These are further possible budget credits if R1
fails. They are not used in (U1)–(U3). Unlike the saturated field, this
field does have local area slack. The two obstructions must be treated
separately.

---

# Earlier report to Chief Researcher — 2026-10-03

**Milestone: a new local lemma and a precise next finite task. No new
global crossing bound is claimed.** The saturated obstruction from old
Section 11.4 forces a second boundary at column 3. A run of `l` blocked
rows forces at least `l-4` additional crossings. These crossings are
separate from all crossings counted in the width-two strip on that side.
The proof has an exact 330-state certificate, checked with a separate
implementation. KT Verifier has not reviewed it.

This gives a new strip cost, `X_strip - length + K`, where
`K = sum_runs max(0, run_length-4)`. The old sharp field has this cost
equal to 2 per row, rather than 1. Its endpoint penalty remains 3/4 per
row. It therefore permits beta up to 8/3 in the new model, rather than
4/3 in the old model. This is only the limit imposed by that particular
field. Other cycles can impose a lower limit. No new beta is certified.

**Next action:** after its assigned 11.3 check, KT Lower Bounds can test
the augmented cost in Section 4 below. It needs a short history of ghost
degrees and a run counter capped at four. It does not need to enumerate
a full width-six strip. A certificate with beta above 4/3 would pass the
old method's ceiling. A certificate with beta above 1 would improve the
currently audited 14/3 bound.

All code and outputs for this report are in `gap/turnstheory/`. No audited
file was changed. No commit or push was made.

## 1. A column can become a boundary inside the board

**PROVEN local implication.** Fix the left-side coordinates. Let `S` be
the selected tour edges with an endpoint in column 0 or 1. For a ghost
cell `(x,y)`, let `d_x(y)` be its degree in `S`. Call row `y` blocked if

```
d_3(y) = 0,       d_2(y-2) = d_2(y+2) = 2.                 (1)
```

Rows outside the board are not used in this definition. We can omit the
first and last two rows, at a constant cost.

The possible neighbours of `(3,y)` to its left are `(1,y-1)`,
`(1,y+1)`, `(2,y-2)`, and `(2,y+2)`. An edge to column 1 belongs to `S`,
so the first condition excludes it. Each listed cell in column 2 already
has both tour edges in `S`, so neither can have an edge to `(3,y)`.
Thus a blocked cell has both its tour edges to columns 4 and 5.

Let `J` contain all selected edges between column 3 and columns 4 or 5.
It is a path forest: it is a proper subgraph of a Hamiltonian cycle.
Every cell has degree at most two in `J`. Blocked cells of column 3 have
degree exactly two in `J`. After translation by three columns, `J` is a
width-one boundary strip with some incomplete boundary rows.

## 2. Interval boundary lemma

**PROVEN with an exact finite certificate; separate implementation check
passed on 2026-10-03.** Suppose `I` is an interval of `l` consecutive
blocked rows. Scan `J` in increasing `(row,column)` order, using three
columns. Assign each crossing to the transition that adds the later of
its two edges. Let `W(I)` count these assigned crossings in rows of `I`.
Then

```
W(I) >= l - 4.                                         (2)
```

The state records pending edges and their path-component labels. The
scan permits degree 0, 1, or 2 in every column. It rejects degree excess
and cycle closure. All states are generated from the empty state. This
soft degree rule is important: a blocked interval can follow any finite
prefix, including rows with edges back toward the physical boundary.
Such rows give incomplete degrees in `J`.

A transition is called hard if it processes a ghost column, or if it
processes a boundary cell with final degree two. There are 330 states,
700 total transitions, and 580 hard transitions. The saved integer
potential `p` satisfies

```
3w - 1 + p(u) - p(v) >= 0                              (3)
```

on every hard transition. At row boundaries `-12 <= p <= 0`.
All `3l` transitions of a blocked interval are hard. Summing (3) gives
`3W(I)-3l >= p(end)-p(start) >= -12`, which proves (2).

In the actual finite board, the scan starts empty before row zero and
ends empty after the last row. Its partial degrees and component labels
are among the generated states. Restricting a tour to `J` cannot add a
cycle. Thus no assumption about the interval's end states is needed.

Let `K` sum `max(0,l-4)` over the maximal blocked intervals. These
intervals have disjoint scan transitions, and all crossing weights are
nonnegative. Consequently, if `X_J` counts all crossing pairs in `J`,

```
X_J >= K.                                              (4)
```

The interval cost is exactly computable by a run counter: cap the count
of previous consecutive blocked rows at four, and charge one at a
blocked row if that count is already four. Reset to zero at any other
row. This charges `max(0,l-4)` for a run of length `l`.

Checks, run from the research root:

```
python3 gap/turnstheory/check_inner_boundary.py
python3 gap/turnstheory/verify_inner_boundary.py
python3 gap/turnstheory/check_patterns.py
```

The first command creates `inner_boundary_certificate.json`, containing
all states and potentials. The second command uses the old, separate
`w-lowerbounds/strip_dp.py` implementation. It relaxes only its boundary
degree rule in memory; it does not modify that file. It reconstructs the
states and checks each of the 580 hard arc inequalities against the
saved potential. Both commands use exact integers and no solver.

## 3. The extra crossings fit the global budget

**PROVEN counting reduction, pending external review.** For each of the
four sides, define `S_sigma`, `J_sigma`, and `K_sigma` as above in that
side's coordinates. Write `X_sigma` for the crossings within `S_sigma`
and `Y_sigma` for the crossings within `J_sigma`.

On one side, the edge sets `S_sigma` and `J_sigma` are disjoint. The first
set has an endpoint at depth 0 or 1. The second set has endpoints at
depths 3 and 4 or 5. Thus their crossing-pair sets are disjoint too.
Across adjacent sides, a duplicate pair lies in a fixed corner region:
the side sets extend at most five columns inward, and an edge spans at
most two cells in either coordinate. Across opposite sides these sets
are disjoint for sufficiently large boards. The finitely many smaller
sizes can be covered by the constant. Therefore

```
sum_sigma (X_sigma + Y_sigma) <= X + O(1).
```

Set `E=X-4n+2` and `D=sum_sigma X_sigma-4n`. From (4),

```
D + sum_sigma K_sigma <= E + O(1).                     (5)
```

Use the same endpoint residues, penalties, and corner paths as old
Sections 11.1–11.3. Let `A` be their total penalty. That argument gives

```
4n <= 4E + 2A + O(1).                                 (6)
```

Suppose a new strip certificate proves

```
beta*A <= D + sum_sigma K_sigma + O(1).                (7)
```

Equations (5)–(7) give

```
X >= [4 + 2beta/(2beta+1)] n - O(1).                  (8)
```

This implication is proved. Inequality (7) for any new beta is open.
For reference, beta=4/3 would give 52/11, beta=2 would give 24/5, and
beta=8/3 would give 92/19. These are conditional coefficients, not bounds
established by this report.

## 4. Precise finite task for KT Lower Bounds

**CONJECTURE / finite task.** Seek beta above 4/3, or at least above 1,
with the following cost. Keep the existing width-two forest graph and
the separate oriented endpoint penalty `a` from 11.3. Retain both
possible initial row parities. Add enough row history to determine (1).

At the processing of a ghost cell, its final degree in the strip is its
number of incoming edges plus its number of newly selected outgoing
edges. Record `d_2` and `d_3`. After row `y+2` is complete, all three
values in (1) are known. The blocked flag for row `y` can then be emitted.
Carry the capped run counter from Section 2. Let `k` be its emitted
zero-or-one cost at each completed row. A shift of two rows in when this
cost is emitted changes only the endpoint constant on finite walks.

For beta=`p/q` and `t=2a`, seek an integer potential for arc weights

```
q*(4w-1) + 4q*k - 2p*t.                               (9)
```

The endpoint penalty and `k` are each charged only once per row; each
can be charged at its own completion time. The accumulated inequality
is `X_strip-length+K >= beta*sum a-C`, up to the bounded initial and
terminal history error. All history initializations used for actual
subwalks must be covered by the potential, or the omitted boundary rows
must be included in that error.

As in 11.3, use an up certificate on the near half of each side and a
down certificate on the far half. Resetting the run counter at the split
can only reduce `K`: for nonnegative integers `u,v`,

```
max(0,u-4)+max(0,v-4) <= max(0,u+v-4).
```

Thus the sum of the two half costs is at most the full-side `K`, as
needed in (5). A direct reflected scan is also valid. Degree condition
(1) is unchanged by reflection in the row coordinate.

No large computation was launched for this task. The office load was
above the brief's threshold when checked on 2026-10-03. The new local
certificate and its check each took less than one second.

## 5. Exact field checks and limits of the result

**PROVEN local calculations.** The known saturated field contains, for
every integer `y`,

```
(1,y)--(0,y+2), (2,y)--(0,y+1), (2,y)--(1,y+2).
```

Every cell of columns 0, 1, and 2 has degree two, and column 3 has no
incident edge in the strip. Every row is blocked. The strip has two
crossings per row. Its endpoint penalties alternate 1 and 1/2 in both
orientations. On a long interval, `X_strip-length+K = 2*length-O(1)`
and `sum a = 3*length/4+O(1)`. The ratio tends to 8/3. The former 4/3
obstruction therefore does not survive unchanged under (9).

The cheap field has edges

```
(0,y)--(2,y+1), (0,y)--(1,y+2), (1,y)--(3,y+1).
```

It has one crossing per row, penalty zero, and no blocked rows. The new
cost is zero, so the proposed certificate preserves the required cheap
equality case.

The checker also tests a possible competing route. In both fields every
crossing overlaps in exactly two quarters, every quarter in the first
two square columns has multiplicity one or two, and none is empty.
Hence the saturated obstruction has neither a one-quarter overlap loss,
a triple-cover loss, nor a hole in those square columns. These local
area-slack charges alone cannot remove that obstruction. The missing
crossing cost comes from the next boundary, not from such a local slack.

**Limit:** frequent breaks in blocked runs can make `K` small. The
constant four per run is not known to be optimal. Other periodic strip
patterns can still block (9) at beta=1 or beta=4/3. The next finite check
must settle this; the positive local lemma does not settle it.
