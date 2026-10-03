# C5-J: trap parity and the chamber count at depth 5.5

2026-10-03. **PROOF for the labelled matching lemma and the conditional
single-chamber count. ARGUMENT / OPEN for the global payment.** This
is research toward `2J+BQx-2K >= 4n-C`; it changes no audited result.
Sources read: BEYOND5.md 13.1–13.7; SHEET.md 8.2–8.3, 9.5–9.6,
12–13.3; Verifier Claim 45F; Lower Bounds FINDINGS B5f.

Main conclusions:

* The exact P pairing at width six obeys the same parity rule as at
  width three. The geometric histogram in BEYOND5 13.4 does not identify
  the pairing: P and U have the same ports but DIFFERENT partners.
* Equal shifts are necessary in the four-piece trap statement. For
  returns with the stated label convention, equal even shifts suffice.
  General cross chords need an affine compatibility condition, given
  below; “even” by itself is coordinate-dependent.
* A proper chamber obeys `L <= 2R_in+c+G5/2+128+e_barrier` directly by
  tile coverage and port counting. No width-three degree identity is
  needed. This is a count, not yet a charge against J or BQx.
* A return alone with two P-class ends is not automatically trapped.
  A suitable partner, common transport, parity, and a proper subcycle
  must be established. L4', the global chamber errors and L5 remain.

## 1. Fixed definitions

**PROOF / definition.** In a left-side frame the cut is the geometric
line `x=11/2`. The collar contains lattice vertices `x<=5`; the interior
side contains `x>=6`. A port is a specific tour edge crossing the cut,
including its two endpoints, not just its crossing height or type.
The possible port types have column pairs `(4,6)`, `(5,7)`, `(5,6)`.
The last type is shallow (vertical displacement two).

Full width-six data include the port edges and their actual pairing
by paths in the collar. A finite side segment must also record paths
exiting its two transverse ends: do not pair those ends artificially.
A chord is a component on the interior side between two cut ports.
A return has its two ports on the same physical side. Other chords
may join different sides. Cut edges are split at the cut, so the two
sides partition the graph as arcs.

A chord is clean when all its interior lattice vertices are good
points: all four adjacent squares have multiplicity one. This is the
SHEET definition. Clean does not assert that a neighbouring chord or
the region between two chords is good. A good-point condition also
does not restrict all ports to steep ports (Claim 38F's caveat).

In a straight '/' steep-port patch, label a port by `c=x-2y` at its
interior endpoint. In a '\\' steep-port patch use `c=x+2y`. Labels
are fixed in the side frame; translating labels by an odd integer
changes which parity case names which partner. Record that translation.

Here P-class means the EXACT reference pairing on the relevant ports
in these labels, with no transverse exits among the pair in question.
It is stronger than equal port types or equal straddle counts. It
also does not imply a good geometric band between two ports.

## 2. Width-six P and U data

**PROOF.** Write the '/' P half-plane as follows:

```
x=0: neighbours (2,y+1), (1,y+2)
x=1: neighbours (3,y+1), (0,y-2)
x>=2: neighbours (x-2,y-1), (x+2,y+1).
```

Inside columns zero through five its collar path is

```
(4,r), (2,r-1), (0,r-2), (1,r), (3,r+1), (5,r+2).
```

Its outside endpoints are `(6,r+1)` and `(7,r+3)`, with labels
`4-2r` and `1-2r`. Consequently the P matching is

```
P6(c) = c-3 if c is even; c+3 if c is odd.          (P)
```

Reflection gives the same rule in the upper '\\' label `x+2y`.
This derives the rule from the field, not from sampled tour labels.

For U, reverse the column-zero/one joins. Its path is

```
(5,r), (3,r-1), (1,r-2), (0,r), (2,r+1), (4,r+2).
```

Its outside labels are `5-2r` and `-2r`. Thus `U6(c)=c+5` for even c,
`c-5` for odd c. Both fields have ports `(4,y)--(6,y+1)` and
`(5,y)--(7,y+1)` on every row. Both pair one type with the other two
rows away, and both have straddle count two. But P pairs `(4,r)` to
`(5,r+2)`, whereas U pairs `(5,r)` to `(4,r+2)`. These are different
labelled matchings. Lower Bounds B5f records the same distinction.

Therefore a zero-cost P class and a positive-cost U class are not
contradictory if they mean full labelled boundary data. They WOULD
be contradictory if “class” discarded which of the two port types
is the lower member. Correct BEYOND5 13.4's inference accordingly.

Light exact check, standard Python only:

    python3 gap/turnstheory/check_c5j_width6.py

It checks the displayed legal paths and partner rules at translated
rows, both affine parity cases below, and a matching-only stop shape.
Output: c5j_width6_check.json. No solver or closed-tour search is used.

## 3. L3: the exact four-piece trap

### 3.1 Matching statement

**PROOF.** Let two distinct interior chords have ports

```
rho:  a -> b
rho': a' -> b'.
```

Suppose the actual collar contains a path joining a to a' and another
joining b to b'. Suppose the four arcs have disjoint internal vertices.
Then their union is a cycle. Every vertex has degree two in that union,
so in a degree-two graph it is a whole connected component. In a closed
tour it is impossible if any tour vertex lies outside this union.

The proper-component qualification matters. “A cycle is impossible”
is false for the whole tour. For a chamber application establish that
its arcs stay in a proper part of the board. Otherwise retain a global
whole-tour exception; do not create an O(1) exception in each chamber.
Geometric proper crossings between arcs do not connect them and do
not affect this graph argument.

### 3.2 Same-side returns and equal even shift

**PROOF.** In the labels of Section 1, suppose the lower collar pairs
c with P6(c), the upper collar has rule P6, and the two actual returns
are

```
rho:  c     -> c+s
rho': P6(c) -> P6(c)+s.
```

If s is even, `P6(c+s)=P6(c)+s`. The upper ends are therefore paired,
and Section 3.1 gives the four-piece cycle. The proof uses only the
matching and equal shift. Cleanliness is not needed once these exact
end data are known.

For odd s, `P6(c+s)-(P6(c)+s)` is +6 or -6, so this particular pair
does not close. Equal shift is not a cosmetic hypothesis. A return
whose ends have P-class data only determines its TWO collar partners;
it does not assert that those partners are ends of one interior chord.

A matching-only stop shape illustrates the issue. Take lower labels
`0,-3,2,-1`, paired by P6, and returns

```
0 -> 100;  -3 -> 101;  2 -> 104;  -1 -> 97.
```

All four shifts are even. Upper P6 pairs are `(100,97)` and `(104,101)`.
The resulting component has four returns and four collar pieces, not
two returns and two collar pieces. This is a precise combinatorial
counterexample to dropping the equal-shift hypothesis. It is NOT a
claim of a clean geometric closed-tour realization; that would require
additional geometry. No counterexample to the qualified lemma is found.

### 3.3 Cross chords

**PROOF.** Let `f` transport lower labels to upper labels on the two
chords. The coordinate-free trap condition is

```
f(P_lower(c)) = P_upper(f(c)).                    (L3)
```

For the SAME rule (P) at both ends and `f(c)=epsilon*c+s`, direct
substitution gives compatibility exactly when

```
epsilon=+1 and s even, OR epsilon=-1 and s odd.
```

For example, with epsilon=-1 and s=0, c=0 has upper mate P6(0)=-3,
but f(P6(0))=3. Thus “even shift” is not the correct general statement
for cross chords in arbitrary local side frames. Transporting both
end frames to common orientation can put it back into the translation
case. Any cross-chord proof must state that normalization, or use (L3).
This algebraic mismatch is not asserted as a realized tour counterexample.

### 3.4 Development and existence of the partner

**ARGUMENT, conditional on the stated Lemma F hypotheses.** Moving
the cut does not change the chart-propagation argument in SHEET 12.
If the union of the squares around both clean chords, the intervening
region and the joining boundary bands is a connected simply connected
GOOD region, and those bands have the required H boundary data in
compatible charts, Lemma F gives equal composite maps. In the return
normalization this gives equal shifts. A common even shift then invokes
Section 3.2. For cross chords use the actual transported matchings.

This application needs all of the following; none follows just from
P-class collar pairings: existence of the partner chord, cleanliness
of that chord, the intervening good region, compatible boundary charts,
and even translation parity. In particular, a defect at a square
starting at x=5 touches the new cut and must not be discarded as a
purely external collar issue. It is in the depth>=5 inventory.

**OPEN for the unconditional chamber application.** Prove these
hypotheses on each block, or classify their failures and pay them.
L5 is meant to price deep failures; it cannot be replaced by the
claim that the two given clean paths make the whole region good.
The source calls Lemma F a proof; this note uses its stated result
conditionally and does not supply an independent audit of all charts.

## 4. L4: an exact local count at the new cut

### 4.1 Proper chamber hypotheses

**Definition / required input.** A proper chamber has a side interval
sigma on x=5.5 and a closed good barrier beta, bounding a region on
the interior side. Fix sigma's integer row interval I=[a,b] and
L=b-a+1. Assign a port to sigma when its cut intersection has height
in [a,b+1), with a consistent half-open endpoint convention.

Assume beta has crossing capacity at most `L+e_beta`: each actual
chord with just one end on sigma crosses beta at least once; each
return on sigma that leaves the region crosses beta at least twice.
Assume no other uncontrolled opening. These are the proper-barrier
hypotheses of Claim 45F, now placed at x=5.5. A ribbon-midline barrier
can supply the local crossing bound under SHEET 9.6's good-run and
joining hypotheses. A failed zigzag, a bad square on the barrier, or
an ending on another board side is NOT such a chamber without repair.

Write R_in for returns staying in the region (boundary permitted),
R_out for the other returns with two ends on sigma, and X for chords
with exactly one end on sigma. Let p be the number of ports on sigma.
Counting chord ends and using barrier capacity gives

```
p = 2R_in+2R_out+X,
2R_out+X <= L+e_beta,
p <= 2R_in+L+e_beta.                              (11)
```

**PROOF under those hypotheses.** The first identity counts endpoints
exactly. The second counts distinct barrier crossings with multiplicity;
use geometric generic position or a fixed local perturbation at joins.
A crossing chord cannot change sides without meeting the barrier.
The third inequality is their sum. No assertion of global chamber
existence is used.

### 4.2 Coverage replaces the old m12 identity

**PROOF.** In squares with lower-left x=5, the only covering tiles
are cut ports: p46 and p57 contribute one half-square each over all
rows, while shallow p56 contributes two. Let c be the shallow port
count on sigma. Let G5 count holes in these L squares, using ACTUAL
full-tour multiplicities.

The total quarter incidence in the L squares is at least `4L-G5`.
Thus in half-square units it is at least `2L-G5/2`. Apart from ports
near the two row ends, it equals `p+c`. A uniform explicit endpoint
bound is 128 half units: a discrepancy edge has an endpoint in columns
4..7 and within two rows of one of the two interval ends. These form
at most 32 lattice vertices; degree two bounds incident edges by 64.
Each edge's contribution has magnitude at most two half units. Hence

```
p+c >= 2L-G5/2-128.                              (12)
```

This deliberately loose bound is PER INTERVAL. It needs no P data,
no absent crossings, and no old width-three degree formula. In a
periodic/full-row formulation the endpoint discrepancy may vanish;
a global proof must demonstrate that cancellation rather than assume it.
The one/two-half counts follow directly from the four-quarter knight
tile: width-two edges cover one half in each of two square columns;
width-one edges cover two halves in their sole square column.

Combining (11) and (12) yields the width-six chamber count

```
L <= 2R_in+c+G5/2+128+e_beta.                     (13)
```

Thus rows are paid by inside returns PLUS the explicitly displayed
shallow-port, hole and endpoint terms. It is not correct yet to say
that returns alone pay every row.

### 4.3 From counts to capacity: the exact remaining requests

Partition inside returns into C_in and U_in by any stated criterion
that intends C_in to have a charged non-P end and U_in to be paid by
deep defects. Then (13) gives, by definition,

```
L <= 2C_in+2U_in+c+G5/2+128+e_beta.                (14)
```

**OPEN (L3-to-L4 implication).** L3 forbids a compatible paired return
block with a common even shift and P matchings. It does not on its
own put every return into C_in or into a quantitatively paid U_in.
The missing partner, a dirty partner, odd shift, changed charts and
whole-tour exception must all be handled. Cross chords require (L3).
Only one whole-tour component can exist, but this does not bound all
block ends or missing partners by an absolute constant.

**OPEN (Phi positivity).** BEYOND5 L2 specifies Phi=0 on P but does
not prove Phi>0 for EVERY non-P datum. That converse needs a zero-set
classification or a direct price for the actual escape data. One
costly segment may serve many returns: assigning a positive value
once is not a lower bound proportional to the number of such returns.
A disjoint or weighted allocation to J must be stated.

**OPEN (L4').** If a shallow port is the only non-P end of an inside
return, it occurs in both 2C_in and c in (14). Counting it twice is a
valid upper bound in (14), but not a disjoint payment from Phi or J.
The price lemma must pay the COMBINED demand, or refine (12)/(14),
or prove a paid bound on the overlap. Moving the cut has not removed
this issue; it replaces p23 by p56.

**OPEN (hole ownership).** G5 is a raw hole count at square depth five.
C5-J uses BQx AFTER the corner-path selections. G5/2 cannot simply
be charged to BQx if some of those holes were selected already.
Nor can the same quarter pay G5/2 and the U_in term of L5 again.
State a joint residual-capacity inequality, or subtract the selected
and otherwise spent quarters. This is separate from L4'.

**OPEN (L5, outside this assignment).** Establish the price of the
remaining U_in in the same residual BQx budget. This note proves no
coefficient for untrapping by deep defects, and does not reuse the
Gap Lemma's raw bad quarters as though they were all free.

## 5. Global summation and the list of error sites

**PROOF of the bookkeeping, conditional on a chosen disjoint family.**
For M proper chambers with disjoint side intervals, summing (14)
retains `128M+sum e_beta`, in addition to their raw counts. If one
local Phi estimate also loses C per segment or per junction, add
those losses explicitly. The claimed O(1) cannot conceal these terms.

**OPEN (L9).** Needed errors and interfaces are:

1. Two row ends in each coverage count (12): at most 128 per interval
   here, with a possible sharper exact boundary potential.
2. Barrier endpoints and joins: e_beta per chamber; additional wall
   pieces are not automatically free in a general zigzag.
3. Partner blocks for L3: unmatched first/last labels, chart changes,
   and transverse collar exits. Their number can grow.
4. Phi concatenation: one junction loss per join unless a common-state
   potential or other telescoping rule removes it.
5. Rows outside proper chambers: failed barriers, bad starts and
   cross-side endings require separate counts. Maximality alone does
   not prove global disjointness or handle these rows (Claim 45F).
6. The fixed board corners can cost one absolute constant; this does
   not justify an absolute constant for an unbounded chamber count.

To finish L4 as a payment theorem, give a global construction plus a
single allocation that dominates (14), including its shallow overlap,
selected-hole loss and boundary errors. Bounding M by O(BQ) is not
by itself enough: the numerical coefficient and the fact that those
quarters remain in BQx both matter.

## 6. Verdict and next audit

**L3: PROOF in the qualified form (L3).** The same-side translation
case is equal even shift with the exact P6 matching, proper component
and actual partner chord. General cross chords require their chart
orientation. Width six does not invalidate the matching lemma.

**L4: PROOF of (13)/(14) for a proper chamber; OPEN as the claimed
universal J/BQx payment.** The original L4' and per-chamber issues
remain, and the precise width-six formulation exposes the raw G5
ownership and the need to classify the zero set of Phi. No extra
claim of a geometric counterexample or a beyond-5 theorem is made.

Pareto profile: elementary six-cell P/U paths, parity algebra and
one coverage/chord count. The new check is standard-library Python,
well below one second on 2026-10-03. No SAT, large transfer graph or
saved-tour census was required. The development step retains Lemma
F's stated hypotheses; the universal payment still requires L2, L4',
L5 and L9. Suggested audit order: Section 2's exact labelled pairing,
Section 3.3's frame convention, then the explicit local ledger (13).
