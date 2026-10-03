# Residual end types: first reduction — 2026-10-03

**HAND ARGUMENT plus exact small enumeration; awaiting independent
review with the quarter-payment lemma (Claim 39).** Quarter order is
B,R,T,L. The side frame has inward coordinate x and scan coordinate y.
Translate the candidate endpoint square to lower-left corner (1,0).
Only S-minus-B crossing pairs can cause unpaid quarters on retained
paths, and only their two-quarter overlaps matter.

## 1. Complete geometric list

The following are the seven occurrences whose overlap meets row zero
at positive depth. The last column lists (square x, square y, quarter).

| Pair of edges | Overlap |
| --- | --- |
| (0,0)--(2,1); (1,0)--(2,2) | (1,0,T), (1,0,L) |
| (0,1)--(2,0); (1,1)--(2,-1) | (1,0,B), (1,0,L) |
| (1,-1)--(2,1); (1,0)--(3,1) | (1,0,B), (1,0,R) |
| (1,-1)--(2,1); (1,1)--(2,-1) | (1,-1,T), (1,0,B) |
| (1,0)--(2,2); (1,2)--(2,0) | (1,0,T), (1,1,B) |
| (1,0)--(3,1); (1,1)--(3,0) | (1,0,R), (2,0,L) |
| (1,1)--(3,0); (1,2)--(2,0) | (1,0,R), (1,0,T) |

Up to row translation and reflection there are four shapes: an outer
mixed pair, an inner mixed pair, a pair overlapping across adjacent
rows, and a pair overlapping across adjacent depth columns. These are
geometric possibilities, not claims of full degree-two completion.

Completeness is a small exact enumeration. If a tile covers a quarter
of row-zero square, every edge endpoint is within 3/2 of the square
centre, hence has row in [-1,2]. At least one endpoint of each S edge
has depth zero or one, and its other endpoint has depth at most three.
The script enumerates a larger row range [-4,4], rejects B pairs, and
checks exact tile intersections of size two. Thus it includes every
possible unpaid pair. Its coordinates also prove that NO unpaid
quarter is at square depth >=3, which sharpens the previous safe
threshold of four.

Command: `python3 gap/turnstheory/classify_unpaid_ends.py`.
Exact records: `unpaid_end_types.json`. No solver is used.

## 2. Only four end squares remain

A path with residual demand has at most one payable quarter in its
entire square set. Therefore all its squares at depth >=3 from every
side are good: any bad one would have two payable quarters by the
alternating identity. Outside the fixed corner exclusions, only two
squares per end, at depths one and two, can be bad. The original plan's
six-square end zone shrinks to FOUR squares over both ends.

At depth two, the only potentially unpaid quarter is L, caused by the
sixth pair in the table. If this square is bad, it has at least one
payable quarter. A deficient path can therefore have a bad depth-two
square at at most ONE end, and then its total residual demand is 1/4.
There is no residual-demand 1/2 path with a bad depth-two square.

If such a depth-two square occurs on a deficient path, its unpaid L
entry is two, it has precisely one other bad (payable) entry, and the
alternating identity restricts its (B,R,T,L) vector to

```
(2,1,1,2), (1,1,2,2), or (1,0,1,2).
```

These are necessary multiplicity patterns; their compatible incident
edges and degree-two completions remain to be classified.

## 3. Zero-payable ends and their local charge

If an end has no payable quarter, its depth-two square is good and
all depth-one multiplicities lie in {1,2}. For an outward-to-inward
horizontal end segment, the two possibly nonzero steps go from depth
one to two and from two to the good depth-three square. The audited
quarter-flux formula gives

```
theta_end = (-1)^(y+3) * (m_R(1,y)+m_L(2,y)-m_R(2,y)-1) mod 3.
```

In the zero-payable case this reduces to
`(-1)^(y+3)*(m_R(1,y)-1)`. Thus an end with m_R=1 contributes zero;
an end with m_R=2 contributes the one fixed nonzero sign at that parity.
In the latter case, the alternating identity restricts depth one's
vector to

```
(2,2,1,1), (1,2,2,1), or (2,2,2,2).
```

The coefficient changes under reflection or reversal; use the audited
endpoint table and both orientations to assemble two-end tests. The
formula here is for the stated local inward horizontal direction,
not a replacement for the full candidate-retention test.

This reduces the active zero-payable local states to three multiplicity
patterns before considering edge realizability. It does not price them.
Neighbouring side rows can provide holes or crossing capacity, and the
F1 certificate must account for sharing with earlier quarter payments.
