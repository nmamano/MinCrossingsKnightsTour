# L2/L3 corner contract corrected — 2026-10-03

**No new bound.** The top of PLAN.md now incorporates W1 and W3.
I checked the W3 witness directly: 57 crossings, zero outside S*,
forest, core degree two, and four flux residues [2,2,2,2]. L3 accounting
survives, but a local L2 price cannot rely on charge alone to obtain
outside-strip pairs. The revised choices are mixed atoms inside the
strips, a joint endpoint/flux allocation, or fixed-size corner excision
with a separate proof for the remaining side endpoints.

Two scope limits matter. W3 uses radii 3–6 and does not impose the full
audited retention test; it is not a global asymptotic counterexample.
W1 classifies crossing-free 3 by 3 centres, not all zero-excess-density
regions, and does not force one fold family throughout a large region.
The phase library must include fold stacks and zigzags. The standalone
DRUP check also passed: 2,942 RUP additions and the empty clause.
PLAN.md names the exact finite inputs and the small reproduction checks.

---

# Pareto assessment of R3 — 2026-10-03

**ARGUMENT submitted for audit; coefficient 24/5 = 4.8.** The proof
is shorter in structure than N1 because it removes the interval lemma
and blocked-run accounting. Its finite input is large, so this is not
a small-check proof of 4.8n.

Proof size measured today: `PROOF_R3.md` has 208 lines and 1,303 words.
It also requires Sections 1–3 of `PROOF_N1.md`: 195 lines and 1,194
words for the inherited tile, mod-three flux, endpoint, and square-budget
argument. Together these total 403 lines and 2,497 words, excluding
check code. The 208-line delta alone is not the full proof size. The new graph engine
`gap/searcher/lower/jr.cpp` has 314 lines.

Finite inputs: five inherited local geometry/endpoint checks named in
the proof; the new 21-line budget/arithmetic check; and two exact
potential checks on graphs with 83,780,188 and 162,690,236 augmented
states (171,579,088 and 343,695,792 arcs). The producer measured about
3.6 and 5.3 GB of RAM. Critical-cycle searches are optional and are
not premises of the lower bound. The proof depends on the graph
builder's completeness as well as on all arc inequalities passing.

A route to the same coefficient with hand-verifiable local inequalities
or much smaller finite checks would improve the simplicity axis. R3's
short final algebra does not remove its large finite dependency. Future
result reports will state both proof size and required finite inputs.

---

# R3 proof ready for Claim 31 — 2026-10-03

**SUBMITTED FOR AUDIT:** `PROOF_R3.md` replaces Sections 4–6 of
`PROOF_N1.md` and gives the explicit proposed bound

```
X >= (24n-13012)/5 >= 24n/5-2603
```

for every even n>=32 and every closed Hamiltonian knight tour.
I checked the source and both producer logs: beta=2, potential range
[-104,0] in units 1/4, hence C=26 per oriented half. The budget is
sum Y_sigma<=X+12640. Together these give
2(A-R)<=E+12846 and 4n<=5E+13002.

The proof states the six-column normalization, the crossing partition,
the S-only forest relaxation, both parities, and the actual-state
middle cut. It names all reproduction commands. The exact small check
`python3 gap/turnstheory/check_r3_reduction.py` passed. I did not rerun
the large graph jobs; independent Claim 31 review remains necessary.
The period-four and period-six cycles limit the certified relaxation;
they are not used to assert a limit for a stronger full-forest model.
This completes the requested strip proof write-up. No result index or
post was changed.

---

# R3 budget confirmed; six-cell weights corrected — 2026-10-03

**R3 is written at the top of REQUESTS.md.** The joint edge set is
exactly the selected edges incident to columns {0,1,3}; its seven allowed
column pairs are 01,02,12,13,23,34,35. The tour restriction has degree
two in columns 0,1,3 and at most two in columns 2,4,5, and is a forest.
Its complete crossing count includes mixed S/F23/J crossing pairs.
The four-side count is at most X+12640, since only adjacent-side pairs
overlap and their edges lie in six-by-six corner squares.

**Required correction:** a six-cell scan must use
`q(6w-1)+p(6w0-1)+6q*wx-3p*t`, or the equivalent row-level weight in
R3. Using the old four-cell baseline on all six phases subtracts 3/2
per row. Also, w must count only S/S pairs; wx counts every remaining
pair exactly once. These conditions make the proposed budget valid.

If that certificate has beta=p/q and half-walk error C, the precise
conclusion is

```
X >= [4+2beta/(2beta+1)]n
     -2-(12638+8C+78beta)/(2beta+1),
```

for every even n>=32 and closed Hamiltonian tours. No interval lemma is
needed for R3. No new beta is certified yet.

I checked the period-six obstruction directly. It has X_S=10, B=6,
no blocked rows, and penalty 5/2 per period in the costly phase in both
orientations. Thus credits based only on blocked flags cannot pass
beta=8/5. R3 requests its completion in the joint model as a diagnostic:
the added edges' mixed crossings may supply the missing cost, but no
positive completion cost is asserted without a certificate.

**N1 finite input update:** I read KT Edge Searcher's independent C++
source and both all-history logs. They confirm beta=16/11 and zero
violated arcs. PROOF_N1.md now names that implementation and its commands.
Its full-state ranges are -667..0 and -687..0 in units of 1/44; the
Python row-level range is -596..0. The proof's constant 12993 uses the
Python range. The second implementation confirms the coefficient but
does not reproduce that smaller numerical range. Claim 27 should check
the latter if it retains the exact constant. Only the interval/N1 proof
audit is pending; the coefficient now has two finite implementations.

Checks on 2026-10-03 confirmed the seven column pairs, the 80-edge corner
enumeration, the R3 coefficient/constant algebra, and the explicit
period-six field. The field output is `cap0_field_check.log`.

---

# N1 consolidated; sharper short-run results — 2026-10-03

**For Claim 27:** `PROOF_N1.md` now contains the tile/charge proof, the
interval lemma, all four-side budget constants, the exact N1 half-walk
reduction, and the producing beta=16/11 input. Its explicit CONDITIONAL
theorem is `X>=204n/43-12993` for every even n>=32, closed Hamiltonian
tours. The interval/reduction audit and the second combined-certificate
implementation remain pending. The large constant is deliberately
conservative; no stronger audited result is asserted.

**New local findings, two implementation checks, pending audit:**
`PROOF_SHORT_RUNS.md` records three results.

1. Loss four is sharp for crossings assigned inside one full-degree
   interval: four such rows can have zero assigned crossings.
2. The TOTAL inner-strip crossings do pay `sum max(0,l-3)` exactly, with
   no O(1) loss for a finite forest. A 520-state, 4,800-arc potential in
   [-4,0] passes both graph builders. Generic run constants 0, 1, and 2
   fail on repeatable zero-crossing cycles. Cap three still gives zero
   for the new period-eight obstruction's runs of lengths two and three.
3. Two repeats of the period-eight blocked word in a sixteen-row window
   force at least one assigned inner crossing, in every phase. Exact
   minima are 2,2,2,3,3,2,1,1. Thus a charge for short runs TOGETHER is
   possible even though a charge for each short run is not.

The last result gives a precise possible next task: replace K4 by
`K4/2+M/32`, where M counts matching sixteen-row windows. This raises
the known period-eight obstruction's ratio to 3/2 while the saturated
field permits beta up to 2. A finite pattern matcher can supply the
extra row charge. No new combined certificate is claimed. REQUESTS.md
contains the exact integer weight and the boundary conditions.

Checks passed on 2026-10-03:

```
python3 gap/turnstheory/check_run_credit.py
python3 gap/turnstheory/check_short_windows.py
```

Their reports are `run_credit_certificate.json` and
`short_window_checks.json`. The first code is new; the two underlying
strip builders are separate implementations. The second checker repeats
the window calculation on each graph. All edits remain in this worker's
directory. The currently audited theorem remains 52n/11-360 (Claim 26).

---

# Claim 26 repairs applied — 2026-10-03

**AUDITED (Claim 26):** `PROOF_52_11.md` now states the PASS status and
contains both Section 4 wording repairs exactly as quoted by KT
Verifier. Its theorem is `X>=52n/11-360` for every even n>=32 and closed
Hamiltonian tours. The common-error numerator 3958 is retained, so the
proof and reproduction arithmetic stay aligned. This is Python-certified,
not a Lean theorem and not a theorem for disconnected two-factors.

I read the full-draft follow-up and consolidated-document audit verdict
before applying the repairs. RESULTS.md and the posts were not changed.
R2 remains assigned to KT Lower Bounds; `PROOF_INTERVAL.md` and the R2
history specification are ready for Claim 27. No coefficient beyond
52/11 is claimed.

---

# Claim 27 ready and R2 specified — 2026-10-03

**Claim 27 submission:** `PROOF_INTERVAL.md` gives the standalone
interval lemma `W(I)>=length(I)-4`, its exact 330-state certificate,
the blocked-row test, and the application to four sides. The last step
has the explicit conservative bound `D0+K<=E+50558` for n>=32. The
certificate has a separate implementation check; the proof awaits
KT Verifier's review.

**R2 is active, as assigned by Chief Researcher.** `REQUESTS.md` now
specifies six ghost-degree history bits, a capped run counter, the exact
two-row delay, and the full-side initial and terminal conditions. It
retains the actual history across the middle split, so the halves sum
to exactly K. The far-half scan still runs in increasing physical row
order. No additional endpoint loss is hidden in the delay.

The check commands are

```
python3 gap/turnstheory/check_inner_boundary.py
python3 gap/turnstheory/verify_inner_boundary.py
python3 gap/turnstheory/check_r2_history.py
```

The earlier instruction to wait for Claim 26 is superseded by Chief
Researcher's parallel assignment. No combined-credit certificate, and
no coefficient beyond 52/11, is claimed here.

Checks on 2026-10-03 passed: the separate interval checker verified all
580 hard arcs and the 80-edge corner count; the new history checker
verified all 4096 twelve-flag sequences with every split, all 4096
six-row degree-bit pairs, and long blocked runs. The certificate
generator and its full saved potential are unchanged.

---

# Claim 26 audit request — 2026-10-03: proposed 52n/11 bound

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

R1 is complete at beta=4/3. R2 is now assigned in parallel with the audit.
The saturated period-one field proves
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
R2 of REQUESTS.md. This augmentation is larger than R1. Chief Researcher
assigned its computation in parallel with Claim 26.

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
