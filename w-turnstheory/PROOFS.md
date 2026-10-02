# All-size upper-bound proofs

Date: 2026-10-02. Status: proved, subject to the finite checks below.

**Theorem.** For each even integer n >= 48, there is a closed knight's tour
with 8n + O(1) turns. There is also a closed knight's tour with 9n + O(1)
crossings. These are two different families: TT16 and H16a.

The following argument closes the gap between finite tour certificates and
all-size constructions. It uses no solver. The important check is the path
matching of an inserted block, including a check that the block cannot add a
separate cycle.

## 1. The specified graphs

Use Cartesian board coordinates 0 <= x,y < n. Read the templates and corner
moves from `w-integrator/corners/TT16_res*.json` or
`w-integrator/corners/H16a_VE_res*.json`, with the residue of n modulo 8 or 24.
Each file gives all moves in the four 6 by 6 corner squares. Copy these moves
at the same local corner coordinates for each new size.

Outside the corners, the bottom and top bands have depth 4 and period 8.
The left and right bands have depth 2 and period 4. The top and right
placements rotate their templates through 180 degrees. All remaining cells
use the opposite moves (2,-1) and (-2,1). In the notation of
`kt/board.py:build_general`, TT16 has phases (0,1,0,0). H16a has phases
(0, (13-2n) mod 8, 2, (-n/2) mod 4).
These phases stay fixed when n increases by the relevant period.
The checker implements these placement rules directly; it does not import
`kt/board.py` or any solver.

## 2. Why size increase is block insertion

Label each cell by **c = x + 2y**. All straight interior edges keep c fixed.
For each c, each maximal run of interior cells is a straight path. A corner
square can split a line into more than one run. Suppress the interior
vertices of each such path. This operation
preserves connectivity and the number of connected components.

Away from the corners, the ends of a line meet the following band pairs:

| Range of c | Bands |
| --- | --- |
| 24 < c < n-24 | bottom and left |
| n+24 < c < 2n-24 | left and right |
| 2n+24 < c < 3n-24 | right and top |

The margin 24 is sufficient: a corner square has c-range of length 15,
and the changes between the band pairs occur within 12 of n or 2n.
Each non-straight edge changes c by at most 5. Thus an 8-label block
between two cuts in one row of this table has no edge that jumps over it.
Its reduced graph repeats under c -> c+8. At a horizontal band this is a
translation by 8 columns; at a vertical band it is a translation by 4 rows.

Here is an explicit description of the size change, which avoids an
assumption about the outside path matching. Select one 8-label block in
each of the three ranges. Replace it by 1+p/8 copies, where p=8 for TT16
and p=24 for H16a. Beyond each insertion, shift c by p. Thus the four
regions between the insertion sites shift by 0, p, 2p, 3p. Preserve band
depth. If a band cell has line-label shift r*p, its coordinate shift is:

| Band | Coordinate shift (x,y) |
| --- | --- |
| bottom | (r*p, 0) |
| left | (0, r*p/2) |
| right | (p, (r-1)*p/2) |
| top | ((r-2)*p, p) |

These translations agree with the corner translations: (0,0), (p,0),
(0,p), and (p,p). They preserve every template phase. The inserted
pieces add p columns to each horizontal band and p rows to each vertical
band. A straight interior path still joins the same two band or corner
ports; only its number of vertices can change. Consequently this operation
produces exactly the reduced graph specified for size n+p. It includes
all vertices: the suppressed vertices lie on straight paths and cannot
form a separate cycle.

For the induction, use n >= 96. Cut just before c=a and c=a+8. The checker
uses a=35 in the first TT16 range, a=36 in the first H16a range, the first
multiple of 8 at least n+32 in the middle range, and a=2n+32 in the last
TT16 range. In the last H16a range it uses the first multiple of 8 at least
2n+32. All these blocks lie in the stated ranges. As n grows, the local
block graph depends only on its phase, not on the length of an interior
straight path. This is why one finite check per phase suffices.

## 3. The inserted blocks preserve a single cycle

A *port* is an edge cut by one boundary of a block. Trace every component
inside the block. Check that each component is a path with two ports,
and that all block vertices occur in these paths. Record the resulting
perfect matching M of the left and right ports. Composition joins right
ports to the corresponding left ports of the next block. Check for closed
components during composition as well as in each block.

**H16a.** Each selected block has four paths, all from left to right.
Number its ports as in the checker: sort by band name, the depths of the
lower-c and higher-c edge ends, and their c-offsets from the cut. The three
permutations are:

| Band pair | Permutation rho on ports 0,1,2,3 | Order |
| --- | --- | --- |
| bottom-left | [1,3,2,0] | 3 |
| left-right | [0,1,2,3] | 1 |
| right-top | [0,2,3,1] | 3 |

Thus rho cubed is the identity in every range. Replacing one block by four
has exactly the same matching and cannot create a closed component.
This proves the required insertion step p=24.

**TT16.** A raw cut also meets short paths that return to the same cut.
Ignoring these paths would leave a gap in a permutation-only argument.
The complete matchings below include them. Write Li and Ri for port i at
the left and right cuts; list each pair once.

| Band pair | Complete matching M |
| --- | --- |
| bottom-left | L0-R3, L1-L3, L2-R2, R0-R1 |
| left-right | L0-R0, L1-R1, L2-R2, L3-R3 |
| right-top | L0-L2, L1-R3, L3-L5, L4-R0, R1-R5, R2-R4 |

Directly join two copies of each row. In every case **M squared = M**, with
no closed component at the join. For example, the first row joins
L0-R3 through the middle return path 3-1-0 to the second copy's L0-R3;
L2-R2 continues directly. The last row has the same property: the paths
through middle ports 3 and 0 continue through 3-5-1 and 0-2-4,
respectively. The outer return pairs stay fixed.
Thus insertion acts as the identity on the 2, 4, and 2 continuing strands,
with the return pairs retained. Replacing one block by two preserves the
full matching and adds no cycle. This proves the step p=8.

In both families, replacing disjoint path systems with the same port
matching preserves every connection in the full tour. The no-cycle check
rules out an extra component hidden inside an inserted block. Starting
from a single cycle, each insertion therefore gives a single cycle.

## 4. Counts and finite bases

Counts are local. A turn uses the two edges at one cell. A crossing uses
two knight edges, whose coordinate spans are at most 2 each. Straight
interior edges are parallel and do not cross one another. Thus all
crossings outside a fixed corner neighbourhood are determined by one
periodic band and its adjacent straight edges. The checker counts these
edges too; it does not count only edges wholly inside the band.

Exact per-period counts are:

| Family | Bottom or top: length, turns, crossings | Left: length, turns, crossings | Right: length, turns, crossings |
| --- | --- | --- | --- |
| TT16 | 8, 16, 26 | 4, 8, 4 | 4, 8, 8 |
| H16a | 8, 25, 16 | 4, 8, 10 | 4, 8, 10 |

Adding a full period leaves the local pattern at each join unchanged.
The corner neighbourhoods are translated copies. Hence the exact
increments are

- TT16 turns: 2*16 + 2*2*8 = 64 = 8*8.
- H16a crossings: 2*3*16 + 2*6*10 = 216 = 9*24.

The checker verifies all even TT16 sizes 48 through 102, and all even
H16a sizes 48 through 118. It checks legal reciprocal knight edges,
degree two, and one cycle containing all n squared cells. For TT16 sizes
48, 50, 52, 54 it reads the supplied full tour files; for the other sizes
it applies the corner files to the specified bands. In particular,
96,98,100,102 cover the four TT16 induction residues, and 96 through 118
cover the twelve H16a induction residues. The insertion argument now
covers every larger even n. The checked base counts and exact increments
give the claimed 8n+O(1) and 9n+O(1) bounds.

## Reproduce the finite certificate

From the repository root, run:

```sh
python3 w-turnstheory/check_upper_proofs.py
```

Only the Python standard library and the supplied construction JSON files
are required. The script checks the 64 base tours, all 48 regional block
matchings, absence of cycles during block composition, and the local cost
table. It also checks each base insertion directly, including the longer
block and its count increment. Its integer orientation tests count proper
crossings of open edge segments. It writes the exact ports, matchings,
base counts, and local costs to `w-turnstheory/upper_proof_checks.json`.
On 2026-10-02 all checks passed. These are finite local certificates for
the insertion proof, not an inference from testing many board sizes.


## 5. LF4: 343n/48 + O(1) crossings for all even n >= 96

Date: 2026-10-02. Status: proved by the insertion argument and the finite
certificate below. For every even n >= 96, the LF4 family gives a single
closed tour with

**X(n) = 343n/48 + b[r], where r = n mod 48.**

The bottom template is `w-integrator/gadgets/b_free.json` (period 6).
The top is `b_vsL3_P16_23125.json` (period 16). The left and right are
`l_d5lowm20.json` and `l_d3lowm21.json` (both supplied with period 4).
Use phases (1,1,0,0). The horizontal bands have depth 4 and the vertical
bands have depth 2, as before. The remaining cells have opposite moves
(2,-1) and (-2,1).

There is one corner certificate for each even residue r in
`w-turnstheory/lf-corners/LF4_resRR.json`. Its base size is n0=96+r.
Each file contains the four templates and all moves in the four 6 by 6
corner squares, so verification does not require a search. The certificates
reuse compatible corner squares from supplied LF4 tours and four additional
one-core corner completions at n=104,106,108,110. The `sources` field records
the origin of each square. The checker validates each assembled base as a
whole; local compatibility alone is not sufficient.

**Insertion.** Set p=48. Use the same line label c=x+2y and the three band
pairs in Section 2. Cut blocks starting at c=36, n+36, and 2n+36, with
widths 12, 8, and 16, respectively. All three blocks lie more than 24
labels from the transition regions for n >= 96. Their reduced graphs
repeat under their respective widths: the bottom-left block shifts the
bottom by 12 columns and the left by 6 rows; the left-right block shifts
both sides by 4 rows; the right-top block shifts the right by 8 rows and
the top by 16 columns. The left and right templates in this family have
identical rows, so the 6-row shift also preserves their phases.

Number ports by the rule in Section 3. The complete block matchings are:

- **bottom-left, width 12:** L0-L8, L1-L4, L2-L11, L3-R14, L5-L13, L6-R11, L7-L9, L10-L14, L12-L15, R0-R5, R1-R6, R2-R7, R3-R8, R4-R9, R10-R15, R12-R13.
- **left-right, width 8:** L0-R0, L1-R1, L2-R2, L3-R3.
- **right-top, width 16:** L0-R2, L1-R3, L2-L5, L3-L6, L4-L7, R0-R5, R1-R7, R4-R6.

These matchings include all paths that return to the same cut. Every block
vertex lies on a recorded path. Joining two copies of any row gives
**M squared = M**, with no closed component at the join. The checker traces
the paths and checks this identity exactly. In particular, the continuing
strand counts are 2, 4, and 2.

To pass from n to n+48, replace the three blocks by 5, 7, and 4 copies,
respectively. Each replacement adds 48 labels. Idempotence preserves the
complete outer port matching and rules out an extra cycle. The coordinate
translations in Section 2 show that the result is precisely the specified
size-(n+48) graph, up to subdivision of straight paths. Here 48 preserves
both horizontal periods, and the vertical translations by 24 preserve the
vertical templates. The corner squares translate without change.
Thus each checked single-cycle base gives a single-cycle tour for every
larger size in its residue class.

**Crossing count.** The exact periodic crossing costs, including adjacent
straight edges, are 11 per 6 bottom columns, 37 per 16 top columns,
8 per 4 left rows, and 4 per 4 right rows. The local count argument in
Section 4 therefore gives

X(n+48) - X(n) = 8*11 + 3*37 + 12*8 + 12*4 = 343.

The base counts give the following exact constants. Each row defines the
formula for all n=n0+48k, k >= 0. These constants describe the supplied
corner certificates; no optimality claim is needed.

| r | n0 | X(n0) | b[r] |
| --- | --- | --- | --- |
| 0 | 96 | 707 | 21 |
| 2 | 98 | 721 | 497/24 |
| 4 | 100 | 738 | 281/12 |
| 6 | 102 | 751 | 177/8 |
| 8 | 104 | 769 | 155/6 |
| 10 | 106 | 783 | 613/24 |
| 12 | 108 | 798 | 105/4 |
| 14 | 110 | 814 | 671/24 |
| 16 | 112 | 821 | 62/3 |
| 18 | 114 | 835 | 163/8 |
| 20 | 116 | 854 | 301/12 |
| 22 | 118 | 866 | 547/24 |
| 24 | 120 | 882 | 49/2 |
| 26 | 122 | 899 | 653/24 |
| 28 | 124 | 912 | 311/12 |
| 30 | 126 | 927 | 213/8 |
| 32 | 128 | 937 | 67/3 |
| 34 | 130 | 949 | 481/24 |
| 36 | 132 | 967 | 95/4 |
| 38 | 134 | 982 | 587/24 |
| 40 | 136 | 996 | 145/6 |
| 42 | 138 | 1012 | 207/8 |
| 44 | 140 | 1028 | 331/12 |
| 46 | 142 | 1041 | 631/24 |

**Finite checker.** From the repository root, run:

```sh
python3 w-turnstheory/check_lf_proof.py
```

This uses the standard-library graph and geometry routines in
`check_upper_proofs.py`; it imports no solver. It verifies all 24 corner
certificates, every base tour and its size-(n0+48) extension, the full port
matching at all 72 regional blocks, idempotence without closed components,
and equality with the actual enlarged block. It also checks the periodic
costs and the exact increment of 343 in each residue. All three block
matchings are the same across the 24 residues. The report
`w-turnstheory/lf_proof_checks.json` records the exact ports, pairs, and
rational constants. All checks passed on 2026-10-02.
