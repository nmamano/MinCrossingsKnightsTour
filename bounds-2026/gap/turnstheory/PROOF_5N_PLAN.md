# Five-n route: quarter payments, then one side certificate

2026-10-03. **PARTIAL HAND PROOF + OPEN CERTIFICATE PLAN.** The hand
step in Section 2 is proved below from audited tile facts. It removes
the interior sharing problem at price 1/2. Sections 2–3 and their conditional reduction passed Claim 39.
Claim 40 also checked the seven end-pair types and the R4 logic. The remaining side statement is
open; this document does not claim X>=5n-O(1).

## 1. Shortest proposed lemma chain

Use the audited retained corner paths C, N=2n-60, L=|C|, and
D_loss=N-L, with the exact endpoint and exception tests. Work at
n>=128; a later theorem can absorb the finite smaller range in its
constant. Let S* be the union of width-two side crossing-pair sets.
Let E=X-4n+2, s=|S*|, and T=s-4n+2. The capacity is

```
nu = (1/2)*(unit pair masses outside S*) + (1/2)*mu,
mu = (G+X1+W3)/2,
E+580 = nu(total)+(T+1160)/2,
(T+1160)/2 >= D_loss/2.                              (1)
```

The last inequality is the audited beta=1 endpoint-restoration input.
Thus nu has half a unit per outside-S* crossing, and a quarter unit
per hole, one-quarter crossing, or W3 unit. W3 is zero at multiplicity
zero. These are separate types of atoms in the proved mixed identity.

| Step | Statement | Status / input |
| --- | --- | --- |
| H0 | Two payable bad quarters per path give private half-price payments, even for arbitrary path subsets | Hand proof, Section 2 |
| H1 | Any unpaid path has a completely good middle and all bad squares in its two bounded end zones | Hand corollary, Section 3 |
| F1 | Residual end-zone demands can be paid in the SAME remaining nu capacity, with one total constant error | OPEN side certificate, Section 4 |
| H2 | Add proved endpoint restoration to obtain X>=5n-(612+C_side) | Hand algebra, Section 5 |

This avoids a global ribbon-word lemma and a universal wall-tension
classification. W1, W3, and Claims 33/35 constrain possible F1 proofs
and stop tests; they are not replacements for the missing F1 capacity
inequality. In particular, bounded support is weaker than a price.

## 2. First hand step: exact quarter-payment packing

A quarter q is bad when its tile multiplicity m(q) is not one. Call
it **payable** in any of these four disjoint cases:

1. m(q)=0;
2. m(q)>=3;
3. m(q)=2 and the unique covering edge pair z lies outside S*;
4. m(q)=2, z lies in S*, and its two tiles overlap in only one quarter.

The ONLY excluded case is m(q)=2 with z in S* and tile overlap of two
quarters. Call this an unpaid quarter. This definition is pointwise
and uses actual full-tour tiles, not multiplicities in an open patch.

**Quarter-payment lemma (PROVEN).** For any set Q of distinct payable
quarters, one can send 1/4 to every q in Q using nu, without exceeding
any atom's capacity. If q is in the square centred on a path vertex,
its paying atom is eligible at radius 2, hence also at radius 10.

**Proof.** In case 1 use the hole atom at q, whose capacity is 1/4.
In case 2 use one W3 unit at q: binomial(m(q)-1,2)>=1. Its capacity is
1/4. Different quarters use different such atoms. In case 3 use 1/4
of the half-unit pair atom z. The tile lemma says a pair covers at most
two quarters, so z receives at most two requests. In case 4 use the
one-quarter-crossing atom z. It has capacity 1/4 and covers exactly one
quarter, so it receives at most one request. The four resource types
are distinct. A pair's X1 atom, if any, and its non-S* pair atom are
separate summands of nu; the rule above does not spend either twice.

For locality, a knight tile has coordinate span at most two in either
axis, with integer extrema. If it covers a quarter of a unit square,
that square lies between these extrema in each axis. Each edge endpoint
is therefore at coordinate distance at most 3/2 from the square centre.
The same holds for both edges of a pair covering q. A quarter closure
lies within distance 1/2 of its centre. All paying supports meet the
strict one-vertex eligibility rule with radius 2. This proves the lemma.

**Private-path corollary (PROVEN).** If each of a collection of the
audited vertex-disjoint paths has two payable quarters in its squares,
choose two for each path. All chosen quarters are distinct, since the
paths have disjoint square centres. Apply the lemma and send both
quarter payments to their path. Each path receives 1/2. This gives an
explicit allocation and hence every Hall inequality for this collection,
not merely enough aggregate capacity in the union of its collars.

No hole-to-crossing injection is needed: holes already carry a quarter
unit in this currency. This is why W3's potentially many-to-one crossing
witness does not obstruct this interior half-price proof.

## 3. Hand reduction to the ends

The audited alternating multiplicity identity in each square is

```
m_bottom-m_right+m_top-m_left = 0.
```

Consequently a square with any bad quarter has at least two bad
quarters: exactly three entries equal to one would force the fourth
to equal one as well.

Every tile of an edge incident to depth zero or one has depth at most
three. Thus an unpaid quarter is within the shallow zone of at least
one physical side. In particular a square at lower-left depth at
least four from ALL sides contains no unpaid quarter. If such a square
on a retained path is bad, it supplies two payable quarters, so that
path is fully paid by Section 2.

For each path let s_i be the number of payable quarters in all its
squares. Choose min(2,s_i) of them, with a fixed tie rule, and apply
Section 2 simultaneously to the whole family. Write f^0 for these
payments, nu'=nu-sum_i f^0_(alpha,i) for the nonnegative residual
capacity, and

```
d_i = (2-min(2,s_i))/4 in {0,1/4,1/2}.               (2)
```

A path with d_i>0 has no bad square in its middle (depth at least four
from every side). Every middle quarter has multiplicity exactly one;
this is stronger than zero flux on its middle steps.

Discard, for purposes of payment only, the candidates with r<=32.
There are at most 4*(32-12+1)=84 such paths. Record at most 42 units
in the ONE global error; do not change the retention or restoration
counts. For the remaining paths, n>=128 keeps other-side interference
away. Each path's shallow squares are exactly three near each end:
local depths 1,2,3 at side-row r. Thus unpaid paths have only six
possibly bad squares, all in two fixed-size side windows. The flux
across the good middle is zero modulo three, so their charge is determined by these
end zones, including the two transitions into depth four.

Retention also excludes every B-pair overlap from all path squares.
Therefore a pair causing an unpaid quarter on a retained path belongs
to S* minus B. F1 must price precisely this remaining side phenomenon.

This reduction does NOT establish that nu' pays (2). Fully paid paths
can already have used pair capacity near these end windows. The side
proof must account for that consumption explicitly.

## 4. F1: exact missing lemma and proposed finite certificate

**F1 (OPEN).** There is an absolute C_side and a permitted choice of the
Section 3 baseline quarters such that, for every tour, nonnegative
residual payments g_(alpha,i) satisfy

```
g_(alpha,i)=0 unless alpha is strictly radius-ten eligible for i;
sum_i g_(alpha,i) <= nu'(alpha);
sum_alpha g_(alpha,i)+epsilon_i >= d_i;
epsilon_i>=0; sum_i epsilon_i<=C_side.               (3)
```

C_side includes the at-most-42 corner allowance. It is not an error
per deficient path, per run, or per window. Together f=f^0+g is the
exact L2-v3 half-price allocation. First try to prove (3) by hand for
the possible end-zone types; only then build a finite scan.

### Finite end types and additive side certificate

A conservative side model uses columns 0..7, with exact degree two
in columns 0..5 and at most two in columns 6,7. Include EVERY knight
edge incident to columns 0..5. This represents all tiles and crossings
needed for the end squares and their immediate neighbourhood. All
actual tour restrictions are admitted; rejecting cycles is optional
for a lower-bound certificate. Near corners are already in the fixed
error above. Use two orientations and both checkerboard parities.

A row type must contain:

* the audited endpoint residue and exception flag;
* multiplicities in the three end squares and the depth-four interface;
* payable-quarter classifications, including whether a covering pair
  is in S, B, and whether its overlap has one or two quarters;
* marks of baseline quarters selected by f^0, and the exact already
  spent fraction of each resource whose support intersects the window;
* a capped count 0,1,2 of baseline payments for that candidate, with 2
  meaning its demand is already fully paid.

The two end types of a corner path are paired at the same radius.
A finite table must cover ALL type pairs compatible with retention and
an unpaid good middle. A safe first relaxation allows every pair with
the correct residue/exception tests and capped payable counts. Seek
nonnegative endpoint demands t(type) whose paired sum covers d_i,
and a side potential that pays these demands from the residual atoms.
An over-demanding relaxation can fail without refuting (3).

For a cell scan, the state records the phase, pending selected edges
(up to two rows of knight span), incoming degrees, the test history,
and the baseline-consumption marks on atoms not yet charged. A crossing
is charged once, when the later edge enters; quarter atoms are charged
once when all their covering edges have been decided. Keep sufficient
row history to finish all recorded endpoint types. Optional component
labels forbid finite cycles but are not needed to include actual tours.
The finite domains are: phase 0..7, parity 0/1, quarter multiplicity
0..4 (four possible covering tiles), selected-quarter mark 0/1,
pair consumption 0/1/2 quarter-units, and candidate quota 0/1/2. A
conservative endpoint record uses the six rows r-2 through r+3; the
scan delays evaluation until their represented edges are decided.
Pending-edge masks and, if used, component partitions complete the
state. These describe finite domains, not a measured reachable-state
count. Every disappearing demand, atom, and baseline mark must be
reconciled before it leaves the state. Arbitrary half-side start states must be
covered, with potentials cancelling at internal cuts.

Finite certificate target, after scaling by four: integer arc weights
`new residual capacity - new endpoint demand` have a bounded-range
potential in both orientations and parities. All pair-type domination
inequalities must also pass. Their sum gives (3), with the potential
range paid a fixed number of times, not per path. Fractional endpoint
tables can be scaled by their common denominator instead.

### Feasibility and honest limits

This is a SPECIFICATION of a sufficient certificate class, not a
completed finite-state reduction. Baseline-mark realizability and
pair-type compatibility still need proofs. Do not encode a single
ribbon bit across interrupted runs (Claim 30). Do not assume all walls
are diagonal or axis-aligned (Claim 35).

Width eight with all edges can have a large reachable state set.
Start with exact local end-type enumeration in a bounded row window
and an LP for the endpoint table. A pilot should count states and
memory before a full transfer graph. The alternative is a SAT/DRUP
local discharging certificate with explicit boundary potentials. A
negative cycle or local patch disproves only that chosen certificate
class until it is shown extendable with the required marks and full
retention. No fixed collection of windows decides the all-tour lemma.

W1/Claim 33 can prune a local crossing-free 9-by-9 window to 156 central
maps, but cannot give one global fold-stack word. W3/Claim 33 supplies
bounded support at the side and permits a radius-ten fallback when a
chosen direct local charge fails. Its 16 checked hole certificates do
not control sharing; the quarter-payment lemma does control sharing
where its hypotheses hold. Claim 35's plane wall is a required stop
test for any proposed price greater than 1/2, not a proof of F1.

## 5. Final algebra if F1 is proved

Section 2 and (3) give nu(total)>=L/2-C_side. Add (1):

```
E+580 >= (L+D_loss)/2-C_side = n-30-C_side,
X >= 5n-(612+C_side).
```

This chain contains no connectivity charge beyond the already audited
closed-tour hypotheses. It is independent of the failed SHEET counts.

## 6. Pareto profile and work completed this turn

The new hand content is the four-case quarter-payment lemma, its
private-path corollary, and the good-middle reduction. These use only
the audited tile geometry, square identity, and boundary exclusion.
No large computation is needed for them. The safe-quarter definition
also spends X1 and W3 atoms explicitly, rather than treating them as
unused surplus. F1 is the single remaining new price lemma.

The exact support bound has a small check:

```sh
python3 gap/turnstheory/check_quarter_payment_support.py
```

Existing finite inputs are the audited endpoint-restoration certificate
and tile/flux checks. W1/W3 are available support and pruning inputs;
they need not be dependencies if F1 admits a direct side proof. The
193-tour Hall screen supports the full half-price statement but does
not yet test this more restrictive baseline-plus-F1 certificate class.
No new SAT search or large state graph was launched.

## 7. Shared D* ledger with Structures — 2026-10-03

**Identification: valid as a conditional implication, not yet a shared
proved D*.** Structures' `fold_exact_scan.py` defines BQ using all bad
quarters in squares with lower-left coordinates 3<=x,y<=n-5. An S*
edge tile reaches at most coordinate depth three, so has no positive
area in any such square. All these bad quarters are payable by
Section 2. Apply that lemma to the ENTIRE set, not just path witnesses:

```
nu(total) >= BQ/4,
E = nu(total)+T/2 >= BQ/4+T/2.                       (4)
```

This is the common hand-proved allocation: reserve BQ/4 from nu, with
no overlap between its quarter payments. Therefore a separate proof
`T>=N_re-C` WOULD give D*: `E>=BQ/4+N_re/2-C/2`.
But audited L3 gives `T+1160>=D_loss`, not a bound on changed collar
ports. Claim 28's fixed-strip repair price does not identify these two
quantities or prove that its full price is in T.

I counted the actual S* UNION on the five audited Claim 36 FOLD tours.
The N_re column is Structures' reported port census (not a new audit
of the port-partner definition):

| n | s=|S*| | T=s-4n+2 | N_re | T-N_re |
| --- | ---: | ---: | ---: | ---: |
| 96 | 541 | 159 | 194 | -35 |
| 144 | 781 | 207 | 290 | -83 |
| 192 | 1021 | 255 | 386 | -131 |
| 240 | 1261 | 303 | 482 | -179 |
| 288 | 1501 | 351 | 578 | -227 |

These samples fit T=n+63 and N_re=2n+2. Thus the proposed side-reserve
identification has a growing deficit on the very examples motivating
D*. These finite data alone do not refute an unspecified O(1); proving
the repeating strip count for the full family would do so. They are
already sufficient reason not to treat that identification as proved.

The exact repair is to keep the residual bulk capacity

```
M_bulk := nu(total)-BQ/4 >= 0,
E = BQ/4 + (T+2*M_bulk)/2.                           (5)
```

D* is equivalent to `T+2*M_bulk >= N_re-O(1)`. For the five measured
FOLD tours, M_bulk is 103,127,151,175,199, respectively. Thus
`T+2*M_bulk-N_re=171`, exactly accounting for Structures' margin 85.5.
Part of the available repair price is in unused nu, not in T alone.

Both routes can share (4) and the nonnegative residual allocation
M_bulk. To share D* itself, prove the last inequality with the same
changed-port definition and one common capacity assignment. Do not add
N_re/2 and D_loss/2 as separate prices against the same T reserve.
Likewise, quarter payments used for Structures' BQ and for our flux
paths are alternative uses of the same allocation, not extra credits.

This section is a short hand reduction plus five exact strip-union
counts. It introduces no large certificate. Reproduce the counts with
`python3 gap/turnstheory/check_shared_dstar.py`; data are in
`shared_dstar_check.json`. The remaining changed-port price is OPEN.

## 8. R4 hand classification update — 2026-10-03

The exact request is now R4 at the top of REQUESTS.md. END_TYPES.md
sharpens the end zone to depths one and two: seven anchored geometric
S-minus-B double-overlap pairs, four shapes up to row translation and
reflection, exhaust unpaid quarters. At depth two only L can be
unpaid. A deficient path can therefore have a bad depth-two square at
only one end, and then needs 1/4 rather than 1/2. Active zero-payable
ends have only three possible multiplicity vectors before degree
completion. These new hand deductions await audit.

R4 corrects one important certificate-design gap in Section 4: total
residual side capacity minus total endpoint demand is not enough for
individual demands. The finite potential must cover ALL selected-row
Hall subsets. R4 supplies a marked-row formulation: credit each atom
once if its eligible row interval contains a selected target. A bounded
selection-history state plus delayed resource ownership makes this a
finite sufficient certificate class. Positivity would prove private
allocation; a negative result rejects the chosen relaxation only.

The next Lower Bounds task is local edge-type enumeration and endpoint
table feasibility, before any large graph. The baseline-mark choice,
complete-quarter requirement, both orientations/parities, and exact
cut ownership are part of the request, not optional implementation
details.


## 9. Scalar F1 with the unused joint-test reserve — 2026-10-03

**HAND REDUCTION; scalar price OPEN.** This accepts Lower Bounds' R4
simplification for the GLOBAL 5n bound. It does not assert the private
L2 allocation, or replace the Hall criterion for that stronger claim.
Claims 39–40 audited the earlier private formulation; the following
new reduction is submitted for review.

### 9.1 Failed ends use distinct rows

Use the JOINT test of w-turnstheory/PROOF_crossings_lower.md Section 3:
both up and down tests pass. Let b count all failed joint rows over
four sides. Section 5's audited integer potential gives

    X_sigma-n >= b_sigma-29/4.

The union correction is sum_sigma X_sigma <= s+1104. Hence

    b <= s-4n+1133 = T+1131 <= T+1160.              (9)

This uses the joint-test certificate, not the fractional a-table.
We keep 1160 to preserve the existing ledger constants.

Partition the retained paths into F (at least one joint-failed end)
and P (both joint tests pass). Every lost candidate has a failed
joint end: two joint-passing ends satisfy the oriented tests and
imply retention. Every path in F also has such an end. Choose one
failed end for each of these candidates. No row is shared: on each
side the near rows [12,n/2-4] and far rows [n/2+3,n-13] are disjoint,
and each radius supplies only one endpoint in its interval. Thus

    b >= D_loss+|F|.                               (10)

Joint failure includes failure of an unused orientation. That causes
no problem: F is defined with the same joint test as b. If a later
model uses only oriented failures, it must state and check that
change; it must not silently identify the two counts.

### 9.2 Exact scalar obligation and proof

Keep the actual baseline f0 and deficits d_i from Section 3 for ALL
retained paths; let nu' be its atomwise residual. Define

    T' = T+1160-b >= 0.

The weaker sufficient side statement is

    nu'(total)+T'/2 >= sum_(i in P) d_i-C.          (F1-scalar)

Only deficient paths contribute to the sum. One absolute C must
cover the whole board, including any small-radius omissions. No
radius restriction on the use of residual capacity is needed for
this scalar theorem. Indeed,

    E+580 = L/2-sum_F d_i-sum_P d_i
            +nu'(total)+b/2+T'/2
          >= (L+D_loss)/2-C + |F|/2-sum_F d_i
          >= n-30-C.

Here d_i<=1/2. Therefore F1-scalar implies

    X >= 5n-(612+C), for even n>=128.

The reserve pays failed-end deficits without spending nu' twice.
This is a complete algebraic reduction, not a proof of F1-scalar.
Hall bits are unnecessary for THIS target. The earlier private F1
would still require them or an equivalent allocation proof.

An optional further simplification is to put NO baseline marks on F.
Let f0_P be the baseline only on P and nu_P'=nu-f0_P. The same scalar
obligation with nu_P' is sufficient: the full half unit for F is paid
by b/2. This enlarges residual capacity and removes irrelevant marks.
It requires one stated choice of the baseline on P; it does not make
all remaining baseline consumption vanish.

### 9.3 First certificate to try: strip counts alone

For each deficient path in P with r>32, its good middle has zero
flux modulo three. Include the steps between the end squares and
that middle in the two end fluxes. Their oriented sum is nonzero,
so at least one end has nonzero end flux with a passing joint test.
Assign the path to one such end. Distinct candidates again give
distinct side rows. A local marked-row relaxation may include extra
rows but must include these assigned ends.

Let m_sigma count marked, JOINT-PASSING, nonzero-end-flux rows for
that side; count each row at most once, even if both orientations
qualify. A sufficient universal finite certificate is

    X_sigma-n >= b_sigma+m_sigma-C_sigma.          (F1-T)

Use actual end fluxes, with the actual orientation at candidate rows.
A stronger model may admit arbitrary orientation flags. A periodic
check is evidence only; a path potential must cover all actual
boundary states. No error per clean stretch is allowed.

If K=1102+sum_sigma C_sigma, summing F1-T gives T+K>=b+m.
The baseline pays all nondeficient paths in P; m/2 pays all deficient
ones except the at most 84 omitted small-radius paths. Thus

    X >= 5n-(32+K/2+42).

The 42 is omitted if those radii are also certified. For an oriented
half-walk potential with error C0 per half, K=1102+8C0 and the displayed
constant is 625+4C0. F1-T uses no residual-atom or baseline marks.
It may be stronger than necessary; failure would return us to
F1-scalar, not refute the 5n route.

### 9.4 Limits and safe resource model

Lower Bounds' A1 propagates height mismatch only along a side stretch
whose entire specified interior dual boundary is good. A deficient
radial path does not establish this condition between nearby rows.
Deep defects may change the height. Their cost must enter one global
certificate; each change cannot receive a free new endpoint error.
The reported periodic J checks under H do not prove F1-T with deep
defects allowed. This is the right next stop test.

If the scalar model needs nu' atoms, retain Claim 40's safe ownership
rules. In the eight-column model (edges touching columns 0..5), use
quarter atoms only where all covering edges are represented; square
columns 0..5 are safe. Columns 6 and 7 can contain false holes in the
truncated graph. Represented pair atoms must subtract baseline use
from BOTH overlap quarters, including a quarter outside the complete
region. No visible mark is not evidence of no consumption.

Proof size: this scalar reduction needs the row injection and one
ledger calculation. Its only new finite input would be F1-T or
F1-scalar. The older joint-test potential and the Claim 39 packing
lemma are inherited inputs. No new computation was run for this
reduction. Source checks: old proof Sections 3,5,6; verifier Claims
39–40; Lower Bounds FINDINGS section A. Existing reproduction commands:

    python3 gap/turnstheory/check_quarter_payment_support.py
    python3 gap/verifier/claim39_check.py

These commands check the hand kernel, not the open scalar certificate.
