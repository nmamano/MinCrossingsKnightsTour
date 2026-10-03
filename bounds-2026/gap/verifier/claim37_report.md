## Claim 37: square Gap Lemma reduction and tree islands through size 10

**2026-10-03. Verdict: PASS for the reduction and the finite exclusion, with two wording repairs below. GAP for the unrestricted square Gap Lemma.** This audit does not restore the false half version. Sources: GAP_LEMMA.md section 11 and gap/lowerbounds/gaplemma/tree_islands.py. Source hashes are in claim37_sources.json.

### 37A. Reduction — PASS

Fix a finite set K of absorbing cuts and let U be the union of their gap squares. All squares of U are bad. Each cut follows adjacent squares, so its whole gap belongs to one 4-connected component C of U. Partition K accordingly; the quarter counts of different components are disjoint. If the Hall inequality fails, at least one component fails it.

Write s=|C|, A for the number of adjacent square pairs in C, r=A-s+1 for its adjacency graph's cycle rank, k for its number of selected cuts, and b for its number of bad quarters. The graph is connected, so r>=0. Counting square sides gives

    perimeter(C) = 4s-2A = 2s+2-2r.

Every selected cut has two distinct end sides between a bad square in C and a good square outside U. A boundary side can be such an end for at most one cut: the outside good square has one split, and the half of that split at the side has one continuation into C. Gaps on that chain are disjoint. Thus 2k<=perimeter(C).

For each square, the tile link identity gives m_B+m_T=m_R+m_L=N. If N differs from 2, each opposite pair has a bad quarter. If N=2, any bad quarter forces its opposite to be bad. Therefore b>=2s. In particular, if r>=1, then 2k<=2s<=b and this component cannot violate Hall.

If a tree component violates Hall, integrality gives

    2s <= b < 2k <= 2s+2.

Hence k=s+1, b<=2s+1, and all 2s+2 boundary sides are selected cut ends. Every side-neighbour outside C is consequently a good square. A component touching the board boundary cannot saturate its boundary sides, since no good square exists across a board-boundary side. The finite island model therefore covers every possible violating component, including components near a board side: treating the surrounding plane as available only relaxes the constraints.

**Wording repairs.** “Tree” must mean that the side-adjacency graph is a tree. It is not equivalent to “no 2x2 block and no hole.” In particular, the seven squares

    (1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,1)

form an adjacency path, but their closed union encloses the missing centre square, with diagonal self-contact at (1,1). Thus the parenthetical claim that a hole forces r>=1 needs a no-self-contact hypothesis or should be removed. The perimeter argument itself remains valid. Both finite enumerators include this shape.

Also, 2s+2 is the number of boundary *sides*, not always the number of distinct lattice vertices incident to C. There are at most 2s+2 such vertices; adding a leaf introduces at most two vertices. The displayed seven-square shape has 15 vertices, not 16. The code constrains the actual set of vertices, which is correct.

### 37B. Author enumeration and CNF — PASS

The shape generator starts with one square and attaches a square with exactly one side-neighbour, reducing by the eight lattice rotations/reflections and translation. This is complete: removing a leaf from any finite adjacency tree leaves a smaller connected adjacency tree. The transformations preserve degree, quarter multiplicity and the property that endpoint bits differ.

The label reduction in labellings() merges the endpoints of both slash and backslash chain segments, as well as repeated occurrences of the same outside neighbour. This initially looks stronger than necessary but is valid. For a slash segment, if either endpoint neighbour is slash, saturation forces the other endpoint to be slash. Thus the endpoint labels agree, including the case where both are backslash and that segment is inactive. The same argument applies to backslash segments. Coverage of every U square is checked, so U is the union of the selected gaps. The code does not assume there are only two labellings; it enumerates every assignment to the resulting classes. The observed two assignments per shape are the output of that procedure.

Each edge variable is a specific undirected knight edge. The link formulas agree with the audited tile halves. At a good neighbour, both halves of its split have exactly one link, and the other halves have none. Each U quarter has four distinct contributing link variables. The bad-budget variable is forced true for multiplicity zero or at least two. It need not be forced false for multiplicity one: under an upper bound, these optional true values cannot admit a false feasible assignment, and every genuine assignment can choose the exact bad indicators. A separate witness variable for each quarter is allowed true only if that quarter is bad; the disjunction of these witnesses requires each U square to be bad.

The two endpoint link clauses impose equality when the gap length is odd and inequality when it is even. This is exactly y0+yk+k odd, the absorbing-cut criterion. The sequential-counter bound is 2s+1. Degree clauses forbid every triple of incident selected edges. In DEGMODE=lecorners they are imposed only at the actual lattice vertices incident to U, with no lower degree bound and no degree constraints elsewhere. These are necessary constraints for every tour or 2-factor and for any edge set of maximum degree two.

The source can request Glucose proof output, but main() calls sat_check() with proof=False. Its normal logs are solver results, not checked DRUP certificates. This audit uses a second encoding and solver; it makes no independently checked DRUP or Lean claim.

### 37C. Independent finite check — PASS / computational certificate

The new standalone claim37_check.py imports no author code. It uses:

* a separate free-tree generator;
* convex tile polygons and integer quarter-centroid tests to obtain tile ownership;
* exact truth-table clauses for each bad-quarter indicator;
* free split variables for all outside neighbours, without the author's union-find labelling reduction;
* chain components derived from the two halves of each geometric tile;
* a direct inequality between the two good endpoint H-bit variables for every active cut, instead of a gap-length parity formula;
* degree at most two at vertices incident to U, with all other degree constraints omitted;
* a totalizer for the bad-quarter bound and Minisat22 as solver.

Only edges that cover a square in U or a side-neighbour are retained. Ignoring any other incident edges in a degree upper bound is a valid relaxation. A genuine violation therefore restricts to a satisfying assignment of this model. The script solves the outside split choices together in one SAT instance per shape.

| s | Free tree shapes | Author label instances | Independent SAT instances with a solution |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 2 | 0 |
| 2 | 1 | 2 | 0 |
| 3 | 2 | 4 | 0 |
| 4 | 4 | 8 | 0 |
| 5 | 11 | 22 | 0 |
| 6 | 27 | 54 | 0 |
| 7 | 83 | 166 | 0 |
| 8 | 255 | 510 | 0 |
| 9 | 847 | 1694 | 0 |
| 10 | 2829 | 5658 | 0 |

Total: 4,060 shapes. The independent run took about 30 seconds; the author rerun took about 48 seconds on this box on 2026-10-03. Both were single-thread solver runs, with at most two jobs active. Commands:

    .venv/bin/python gap/verifier/claim37_check.py 10
    DEGMODE=lecorners .venv/bin/python gap/lowerbounds/gaplemma/tree_islands.py 10 0

Evidence: claim37_check.py, claim37_check.json, claim37_check.log and claim37_author.log. Sanity tests find SAT examples when the bad-quarter budget is increased by two (all tested sizes 1 through 6), when the absorbing requirement is removed (sizes 1 through 6), or when degree constraints are removed (sizes 2 through 6). These tests do not establish extendibility of the relaxed witnesses; they check that the independent model is not identically inconsistent.

### 37D. Exact proved scope and remaining gap

The square Hall inequality holds for every K for which each tree component of its gap-square union has at most 10 squares; cyclic components may have arbitrary size. In particular, **it holds for every set of at most 11 absorbing cuts, with no restriction on individual gap lengths**. Indeed, a violating component must have k=s+1, so k<=11 would imply s<=10, which the finite check excludes.

Any counterexample to the unrestricted square lemma must contain a saturated adjacency-tree component with s>=11 squares, exactly s+1 selected cuts and at most 2s+1 bad quarters. No induction or all-size tree certificate has been established by this audit. The result applies to every closed tour and spanning 2-factor, without a perfect halo assumption: goodness of the one-square side-neighbour layer is forced by saturation in a putative counterexample. The SAT models do not impose connectivity or spanningness. No price or exclusion of boundary crossing pairs B follows from this combinatorial result; that remains a separate requirement in the ledger application.

**Pareto profile:** the reduction is a short perimeter and integrality argument. Its finite input is all 4,060 free tree shapes through size 10, checked with two encodings and two SAT solvers. It gives a bounded-cut Hall theorem, not a new asymptotic crossing coefficient. The unrestricted tree step remains GAP. No author files were edited; the audit is complete.
