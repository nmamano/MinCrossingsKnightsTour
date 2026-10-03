# Short-run charges after the period-eight obstruction

2026-10-03. **New local results, pending independent audit.** All finite
calculations below pass two separate strip builders. They are not inputs
to `PROOF_N1.md`, which retains the original run constant four.

## 1. Constant four is sharp for assigned interval crossings

In the soft width-one forest of `PROOF_INTERVAL.md`, let W(I) count
crossings assigned within a complete-degree interval I. Exact shortest
paths between reachable row-boundary states give

```
min W(I) = max(0,l-4),  for l=1,...,16.
```

The checker also restricts the end state to states that can reach the
empty state and obtains the same minima. Thus a minimising walk extends
to a finite forest; a doomed state with a deferred cycle is not a witness.

In particular a four-row complete-degree interval can have zero assigned
crossings. No inequality W(I)>=l-c with c<4 holds in this model. Runs of
two or three rows cannot individually receive a positive assigned charge
from their lengths alone. The end states matter.

## 2. Constant three is valid for the total crossing count

**Theorem, finite-certificate proof.** Let J be any finite path forest of
legal knight edges in columns zero, one, and two, every edge incident to
column zero, and every vertex of degree at most two. Mark any subset of
the rows whose column-zero vertices have degree two. If their maximal
marked runs have lengths l_i, then

```
X_J >= sum_i max(0,l_i-3).                            (S1)
```

This is a total crossing bound, not an assigned bound for each run.
It permits a crossing near one run to pay for that run through a state
potential. There is no additive error for a whole finite forest.

Proof: use the 330-state soft scan from the interval lemma and compose
each three cell transitions into one row transition. There are 1,200
distinct row arcs (u,v,w,f), where f is one exactly when that row's
column-zero degree is two. Add a counter s in {0,1,2,3}. A full row
emits k=[s=3] and changes s to min(3,s+1). A non-full row emits zero and
resets s to zero.

There are 520 augmented row-boundary states and 4,800 arcs. The exact
integer potential p in [-4,0] satisfies

```
w-k+p(u)-p(v) >= 0                                   (S2)
```

on every augmented arc. The generator and a separate strip builder
check every inequality. Scan the finite forest from an empty row before
its first edge to an empty row after its last edge. Include a final
empty row to reset the counter. Both ends then have the same empty base
state and counter zero. The potentials cancel, proving X_J>=sum k.
Here sum k is exactly the run charge for ALL full-degree rows.

Deleting marks cannot increase the charge sum max(0,l-3): deleting one
mark shortens or splits a run, and
max(0,a-3)+max(0,b-3)<=max(0,a+b+1-3). Iteration proves monotonicity.
Thus any marked subset, including the blocked rows, has at most the
full-degree charge. This proves S1.

Consequently the blocked credit K3 with run constant three obeys the
same global budget as K4:

```
D0+K3 <= E+50558.
```

The separate budget and the constant come from `PROOF_INTERVAL.md`.
Only the one-column local certificate changes. No extra half-walk or
per-run error is introduced by S1.

The run constants zero, one, and two fail even for a total bound with
an arbitrary fixed additive constant in this soft-strip model. The
checker extracts repeatable negative cycles. For constant two it finds
a six-row cycle with zero crossings, three consecutive full rows and
three non-full rows. Repeating it earns one false credit per period.
A finite prefix reaches its base state from empty, and a suffix finishes
the pending edges with no new edges. These end costs are bounded while
the number of periods grows. This rules out a generic degree-only K2
bound; additional constraints coupling J to S could still give one.

## 3. A positive charge for the actual period-eight short-run pattern

The obstruction has blocked flags

```
0 1 1 0 0 1 1 1
```

repeated, up to phase. Its runs have lengths two and three, so S1 still
gives zero. Constant three alone does not remove this obstruction.

However, exact shortest paths for sixteen-row windows whose required
full-degree flags are two repeats of this word give minima, over its
eight starting phases,

```
2, 2, 2, 3, 3, 2, 1, 1.
```

All minima are at least one. A zero flag places no constraint on that
row's degree. Thus every sixteen-row window of blocked flags matching
two repeats of this pattern forces at least one assigned crossing,
even though each individual short run can have none.

Let M count all sixteen-row windows of the blocked-flag sequence that
equal one of the eight rotations of the doubled word. Their assigned
crossings are counted at most sixteen times in total, because each row
belongs to at most sixteen windows. Therefore

```
Q = M/16 <= X_J.                                     (S3)
```

For any 0<=lambda<=1, S3 and the old interval bound give

```
X_J >= (1-lambda)*K4 + lambda*Q.                      (S4)
```

For example, lambda=1/2 keeps half the old long-run charge and adds
M/32. The saturated field then has credit rate 1/2; the period-eight
obstruction has rate 1/32, or 1/4 per period. Its certificate ratio would
rise from 16/11 to (8+1/4)/(11/2)=3/2. The saturated field would limit
beta only at 2. Neither known field blocks an improvement above 16/11
with this credit. Other cycles remain untested.

**Next finite idea, not a certificate:** add a finite pattern matcher
for the eight length-sixteen words to the combined strip graph and use
credit (K4+Q)/2. Charge one occurrence when the delayed blocked-flag
stream completes a listed word. Keep the matcher state across halves,
just like the degree history. Counting only windows fully emitted
within the physical side prevents boundary overcredit. This task is
more specific than substituting an invalid run constant two.

## Reproduction and scope

From the research root:

```
python3 gap/turnstheory/check_run_credit.py
python3 gap/turnstheory/check_short_windows.py
```

The first program produces `run_credit_certificate.json`, containing
the potential and the counterexamples for constants zero through two.
It checks the potential against the second row graph as well as checking
that both row-arc sets agree. The second program computes each window
minimum independently on both row graphs and writes
`short_window_checks.json`. Both checks passed on 2026-10-03.

The two graph builders are the local direct generator and the old
`w-lowerbounds/strip_dp.py` builder with its boundary degree rule relaxed
in memory. No source outside `gap/turnstheory/` is changed.
