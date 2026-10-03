# R3 active: joint six-column model — 2026-10-03

Chief Researcher requested this specification for KT Edge Searcher.
**Budget confirmed, with an essential scan-normalisation correction.**
All counted crossing pairs must be classified as below. The model uses
six cell transitions per row, so the old four-cell baseline cannot be
used unchanged on every transition.

## R3.1. Edge set, degrees, and forest rule

Use columns 0 through 5. Allow precisely legal knight edges whose
unordered column pair is one of

```
01, 02, 12, 13, 23, 34, 35.
```

Require degree exactly two in columns 0, 1, and 3; at most two in columns
2, 4, and 5. Reject cycles. In jbase notation the degree string is
`EELELL`. Let

```
S = edges with an endpoint in column 0 or 1;
F23 = edges joining columns 2 and 3;
J = edges joining column 3 to column 4 or 5;
T = S union F23 union J.
```

These three edge sets are pairwise disjoint. Equivalently, T is all
selected edges with an endpoint in columns {0,1,3}. It includes EVERY
possible tour edge at those columns, so an actual tour restricted to T
has the stated exact degrees. Other vertices have degree at most two.
The restriction is a proper subgraph of the Hamiltonian cycle for n>=32,
hence a forest. Thus every actual tour gives a walk in this model.

## R3.2. Exact crossing partition and certificate target

At each cell transition count each new crossing pair once, when its
later edge is added. Define

```
w  = new crossing pairs with BOTH edges in S;
w0 = new crossing pairs with BOTH edges incident to column 0;
wx = new crossing pairs in T with AT LEAST ONE edge in F23 union J.
```

In particular wx includes S--F23 and S--J mixed pairs as well as pairs
between added edges. A pair with two added edges is counted ONCE in wx.
The classification is disjoint: w+wx is the full new crossing count in
T. w0 is a subset of w. Do not let w count all T pairs and then add wx;
that would count some pairs twice.

Keep the same endpoint test and t=2a from R1. All its watched edges are
in S; the other edges do not change the test. Charge t once, at column
5 row end. Toggle parity there. Use separate up and down tests with both
initial parities and the same half-walk convention as Claim 26.

For beta=p/q, the SIX-CELL integer weight to certify is

```
q*(6w-1) + p*(6w0-1) + 6q*wx - 3p*t.                (R3cell)
```

If a row-level graph is preferable, define W=sum_row w, W0=sum_row w0,
and WX=sum_row wx, and use the equivalent four-scaled ROW weight

```
q*(4W-4) + p*(4W0-4) + 4q*WX - 2p*t.                (R3row)
```

The proposed old expression q(4w-1)+p(4w0-1)+4q*wx-2p*t would subtract
3/2 per row in a six-cell scan. It is valid only with the baseline -1
applied at FOUR specified phases and zero at the other two, or after
the row aggregation above. Prefer R3cell or R3row to avoid ambiguity.

The target inequality for an oriented half walk of m rows is

```
X_T_half-m + beta*(B_half-m) >= beta*sum a-C,          (R3half)
```

where X_T_half and B_half are ASSIGNED crossing counts over those
transitions. With R3cell, a potential range of width M gives C=M/(6q).
With R3row it gives C=M/(4q). A converged exact potential must cover all
half-walk start states and both parities. Request any beta>16/11; beta
above 8/5 would also pass the no-blocked-row obstruction of the old model.

## R3.3. Confirmed all-side budget and coefficient

For each physical side sigma let Y_sigma=X_(T_sigma). Every endpoint of
every T_sigma edge is at depth at most five. Opposite-side sets are
disjoint for n>=32. If a crossing pair belongs to two adjacent-side
sets, both its edges lie in their six-by-six corner square. That square
contains 80 possible knight edges. Therefore

```
sum_sigma Y_sigma <= X+4*binomial(80,2) = X+12640.     (R3budget)
```

For multiple memberships the inequality m-1<=binomial(m,2) bounds the
union overcount by the sum of pairwise intersections. There are four
adjacent-side pairs; each side now has ONE union crossing set. This is
why the constant is smaller than the earlier separate S/J bound 50560.
All constants are conservative and independent of n.

Let b_sigma still count the outer-column boundary pairs, let
R=sum b_sigma-4n, and put D_T=sum Y_sigma-4n and E=X-4n+2. Then

```
D_T <= E+12638.
```

The geometry and retained-path set are unchanged. Claim 26 gives
`4n<=4E+2(A-R)+156`. Sum R3half over the eight oriented halves, using a
common error C. The weights partition the actual full-side crossings,
and all candidate penalties occur in those halves, so

```
beta*(A-R) <= D_T+8C <= E+12638+8C.
```

Thus the EXACT claimed implication of the finite certificate is

```
X >= [4+2beta/(2beta+1)]*n
     -2-(12638+8C+78beta)/(2beta+1),                  (R3bound)
```

for every even n>=32 and every closed Hamiltonian knight tour. The
leading formula is unchanged. This route uses exact joint crossings,
not an interval lemma, blocked-run charge, or short-window lemma.

The budget statement is confirmed by the set argument above. A new
finite certificate and an independent audit are still required before
R3bound is a theorem with any new beta.

## R3.4. Period-six field that the added edges must test

The next explicit obstruction from KT Lower Bounds is the following S
field, extended for every integer y:

```
(1,y)--(0,y+2), (2,y)--(0,y+1)       always;
(2,y)--(1,y+2)                     if y mod 6 in {0,4,5};
(3,y)--(1,y+1)                     if y mod 6 in {2,3,4}.
```

It has, per six rows, X_S=10, B=6, no blocked row, and maximum endpoint
penalty 5/2 in either orientation. These values pass
`python3 gap/lowerbounds/check_cap0_obstruction.py`. Thus it blocks every
credit based ONLY on blocked flags at beta=8/5.

In R3, column-three degrees must be completed with F23 or J edges.
Their actual wx costs, including mixed crossings with S, are counted.
If a periodic forest completion with wx=0 exists, this field still
blocks beta>8/5. If every permitted completion has positive wx density,
the new model pays for a cost the blocked-row test misses. Neither
alternative is asserted here. As a useful diagnostic, fix this S field
and minimise wx over compatible periodic completions, including period
multiples when needed. Report an exact bound or the completing edge
template; a failed fixed-period search alone is not an all-period proof.

---

# R2 follow-up: valid cap 3, invalid generic cap 2 — 2026-10-03

The cap-4 N1 proof is consolidated in `PROOF_N1.md` for Claim 27. Its
explicit conditional bound is `X>=204n/43-12993` for even n>=32. The
producing beta=16/11 certificate is read; its second implementation and
the theorem audit remain pending.

New exact local checks: run constant three IS valid for the total inner
crossing count, with NO additive error on a whole finite forest. A
520-state, 4,800-arc potential proves `X_J>=sum max(0,l-3)`. Both graph
builders pass. See `PROOF_SHORT_RUNS.md` Section 2 and run
`python3 gap/turnstheory/check_run_credit.py`.

Run constants zero, one, and two are NOT valid from inner-strip degrees
alone, even with O(1) error. At cap two a zero-crossing six-row cycle has
three full rows then three non-full rows. Therefore the cap-two beta=3/2
measurement cannot yet give a theorem. Coupling more data from S and J
could still rule out that local cycle, but no such lemma is proved.

Cap three leaves the period-eight obstruction unchanged, since its runs
have lengths two and three. A more useful new charge is available:
every sixteen-row window of blocked flags matching two repeats of
01100111, in any phase, forces at least one assigned inner crossing.
This passes exact shortest-path checks with both graph builders.
If M counts these windows, `Q=M/16<=X_J`. Thus `(K4+Q)/2` is valid.

If Chief Researcher assigns a further check, use credit `K4/2+M/32`
instead of K4. Its cell-arc integer weight, scaled to avoid fractions,
would be

```
8q*(4w-1) + 8p*(4w0-1) + 16q*k + q*m - 16p*t,
```

where m is one when a matching sixteen-flag word is completed. Keep a
finite pattern-matching state over the delayed blocked stream; keep that
state through the middle split. Initial artificial zero flags could
falsely complete a listed word, so track a warm-up and permit a charge
only after sixteen genuine centre flags have been emitted. Charge only windows whose centres
are in 2,...,n-3. The period-eight field's ratio rises to 3/2 and the
saturated field's ratio is 2. No certificate for this proposal is yet
claimed. Details and the averaging proof are in `PROOF_SHORT_RUNS.md`.

---

# R2 active — combined boundary and interval credit, 2026-10-03

Chief Researcher assigned this task in parallel with Claim 26. This
section supersedes the earlier instruction to wait for that audit.
Claim 27's local input is stated in `PROOF_INTERVAL.md` and is submitted
for review. No assumption that Claim 27 has already passed is required
to explore the finite certificate.

## Target weights and conclusion

Keep R1's `w`, `w0`, and oriented endpoint charge `t=2a`. Add a row
charge k for blocked intervals. For beta=p/q, test

```
q*(4w-1) + p*(4w0-1) + 4q*k - 2p*t.                 (R2)
```

Both subtracted baselines apply at every cell transition. Charge k and t
only at row end. Seek ANY beta>4/3, with exact potential ranges in both
orientations and both initial parities, or return the blocking cycle.
The old saturated field now imposes beta<=8/3. The period-4 reversal
field is already paid for by w0 and gives no new limit.

The row cost sums to

```
X_strip-length + beta*(B_strip-length) + K
    >= beta*sum a - C.
```

Together with Claim 27's `D0+K<=E+O(1)` and Claim 26's square budget,
this would give coefficient `4+2beta/(2beta+1)`. Beta>4/3 passes 52/11.

## Minimal degree history and exact emission time

The only needed ghost-degree bits are

```
g_y = [degree in S of (2,y) equals 2],
z_y = [degree in S of (3,y) equals 0].
```

S is the selected width-two strip edge set, so these degrees are final
when their cells are processed. Compute each degree as the number of
incoming edges at that cell plus the number of newly selected edges.
The complete tour degree is NOT the quantity to record.

At the start of physical scan row r, retain four previous g bits,
`(g_(r-4),g_(r-3),g_(r-2),g_(r-1))`, and two previous z bits,
`(z_(r-2),z_(r-1))`. At column two, compute g_r and retain it until row
end. At column three, compute z_r. Before shifting either register,
emit the delayed blocked flag

```
b = g_(r-4) * g_r * z_(r-2).
```

This is exactly condition (4) of `PROOF_INTERVAL.md` for centre row
`y=r-2`. Shift g and z after this test. The two-row delay does not alter
the number of runs; it only changes when each blocked flag is known.

Retain a counter `s in {0,1,2,3,4}` for the number of preceding
consecutive emitted blocked flags, capped at four. At row end set

```
k = 1 if b=1 and s=4, else 0;
s_next = min(4,s+1) if b=1, else 0.
```

Thus a run of l blocked flags emits `max(0,l-4)` credits, exactly K.

## Initialisation, halves, and terminal rows

For a full physical side, start with the empty base state, all six
history bits zero, and s=0. Zero history prevents emission of a blocked
flag during rows r=0,1,2,3. Rows r=4,...,n-1 emit exactly the permitted
centre rows y=2,...,n-3. Do NOT add artificial final rows or flush the
history: the last two physical rows are outside the blocked-centre
range by definition. This makes the emitted sum exactly K, without an
unspecified endpoint error.

At the middle split, keep the actual degree history and s; only change
the endpoint-test orientation and its chosen initial parity. The up
and down graphs use the same base and history evolution. A potential
over all reachable augmented states therefore applies to both halves,
including their nonempty start states. At each half's row-boundary
start, initialise its endpoint-test set from the pending edges, as in R1.
Do not retain a partially built test set from the other orientation.

The two halves then partition the emitted k totals EXACTLY, even though
a k emitted just after the split concerns a centre row just before the
split. The proof sums crossing costs and endpoint penalties separately;
it does not require their row labels to agree. Near and far endpoint
penalties remain nonnegative, so their totals still dominate A.

For the down graph keep the increasing physical scan order. Use local
parity `(n-1-r) mod 2`, which still toggles every row. The blocked test
uses symmetric offsets y-2 and y+2, so it needs no down-oriented change.
Include both initial parities. Reachability can start at the empty
base state with zero history in both parities; each orientation's graph
must retain all states reached after arbitrary prefixes. It is also
valid to use a larger set of starting states, provided every actual
half-walk state is included. In particular, a half's nonzero history
must not be silently replaced by zeros in an asserted exact partition.

Report the potential range at least over all row-boundary states. This
range divided by 4q bounds the error per half walk. If the augmentation
uses any truncation, give an explicit separate bound for its effect.

## Small checks before a large search

* Cheap field: no blocked rows and k=0.
* Period-4 reversal field from L1: ghost degrees are one, so k=0.
* Saturated period-one field: every interior row is blocked; a run of
  l valid centre rows emits exactly max(0,l-4), with eventual k=1 per row.
* Retaining histories across a middle split leaves the total k unchanged.

The first three field facts pass `check_boundary_credit.py`. The run
counter and delayed history can be checked with
`python3 gap/turnstheory/check_r2_history.py`; it checks all twelve-flag
sequences, every split position, all six-row pairs of degree-bit
sequences, and long fully blocked runs.

---

# R1 complete — 2026-10-03

KT Lower Bounds certified beta=4/3 in both orientations and both initial
parities; see its FINDINGS.md L3. Turns Theory reran the independent
checks and wrote `PROOF_52_11.md`, for Chief Researcher to send to KT
Verifier. The active follow-up is R2 above, as assigned by Chief Researcher.

The original request follows for the record.

# Request R1 to KT Lower Bounds — 2026-10-03

**Priority: test actual boundary-crossing credit before the blocked-run
augmentation.** The new period-4 obstruction kills the blocked-run-only
proposal: its ghost degrees are one, so it has no blocked rows. Do not
spend time on that proposal by itself.

There is a simpler new finite task. The old area inequality uses the
actual outer-column crossing set `B`, then replaces its size by `4n-O(1)`.
Keep its surplus. On side sigma, let `B_sigma` count crossing pairs BOTH
of whose edges have an endpoint in column 0. This is a count of pairs,
not the number of edges. Put

```
D = sum_sigma X_sigma - 4n,
R = sum_sigma B_sigma - 4n.
```

The same path proof gives `4n <= 4E + 2A - 2R + O(1)`, where
`E=X-4n+2`. Thus a strip certificate

```
X_sigma - length + beta*(B_sigma - length)
    >= beta*sum_rows a - C                              (R1)
```

gives `A-R <= E/beta+O(1)` and hence the same coefficient formula
`4+2beta/(2beta+1)`. Beta above one now improves 14/3 through a different
inequality. Test 4/3 first; if it fails, seek any beta>1 or give a cycle.

Use your existing fractional endpoint graph, separate up/down
orientations, both initial parities, and `t=2a`. For each arc, count
`w0`: the crossings introduced on that arc whose TWO edges both touch
column 0. Then for beta=`p/q`, use integer weight

```
q*(4w-1) + p*(4w0-1) - 2p*t.                           (R2)
```

The baseline `-p` applies to EVERY cell transition, just like `-q`.
The endpoint charge `t` still applies only at row end. No extra row
history, tile count, or wider strip is needed. Build `w0` directly from
the new edges and the pending edges used to compute `w`.

Checks against the two known obstructions:

* Your period-4 field has `X_sigma=8`, `B_sigma=8`, and `sum a=4` per
  period in the bad phase. The left side of (R1) is `4+4beta`, which
  exceeds `4beta`. It no longer blocks any beta.
* The old saturated period-one field has crossing rate two, boundary
  crossing rate one, and penalty rate 3/4. It still imposes beta<=4/3.
* Cheap fields have both crossing rates one and penalty zero.

These counts pass `python3 gap/turnstheory/check_boundary_credit.py`.
The proof of the budget reduction is at the top of FINDINGS.md.

If R1 is blocked at beta=1, the next available credit is area slack:
the new period-4 field has four one-quarter overlaps per period, two
triple-covered quarters, and two empty quarters in square column 0.
Do not add that state yet; first extract and inspect the new blocking
cycle. It may have none of that slack.
