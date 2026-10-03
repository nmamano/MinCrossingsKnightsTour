# Independent verification — 2026-10-02

**Latest audits, 2026-10-03: Claim 31 is PASS: 5X>=24n-13012, hence X>=24n/5-2603, for every closed Hamiltonian tour on an even n by n board with n>=32. Claim 30 passes the local ribbon-run and wall lemmas and the full-2-factor defect budget, but the connected-domain/global-ribbon-word claim is FALSE: a validated n=96 tour has different bits on two runs of the same ribbon in one connected good domain. Exact scope repairs and independent exhaustive checks are in Claim 30. No Lean result is claimed.**

## Claim 1: full tours with 9n + O(1) crossings

**Verdict: all supplied finite witnesses pass. The general construction still needs a proof of connectivity for all board sizes. A fixed offset per residue class modulo 8 is false for these witnesses.**

At 00:19 UTC on 2026-10-02, `check.py` checked 69 JSON files in `w-integrator/tours/`. These are 44 H16a files (n = 48, 50, 52, 54, and every even n from 64 through 142) and 25 H16b files (every even n from 64 through 112).

Every file gives one closed knight's tour through all n² cells. Every stored crossing count and turn count matches the independent count. All files have 0 <= X - 9n <= 7. All files specify corner size Z = 6. The exact counts, source file names, and SHA-256 hashes are in `results.json`.

The checker uses only the Python standard library. It does not import `kt/` or worker code. It reads Definitions 1 and 2 in `paper.txt` as the specification. It checks square shape, move codes, two distinct neighbors, board bounds, reciprocal edges, and one walk through every cell. It counts a turn by a nonzero determinant of three consecutive cells. It counts each unordered pair of edges once, with strict determinant tests for a proper intersection. Inclusive bounding boxes in 4 by 4 bins remove impossible pairs; they cannot remove a crossing pair. All arithmetic is integer arithmetic.

A knight segment has a primitive integer direction, so it has no interior lattice point. Distinct knight segments with collinear open overlap cannot occur: their equal-length primitive directions force either the same segment or disjoint interiors. Thus the strict proper-intersection test agrees with the open-segment definition here. Shared endpoints do not count.

## Slopes and offsets

The following are the observed values of b = X - 9n, separated by template and n modulo 8.

| Template | residue 0 | residue 2 | residue 4 | residue 6 |
| --- | --- | --- | --- | --- |
| H16a | 5 | 0 | 7 | 1, 2, 3 |
| H16b | 2, 3 | 0, 2 | 4 | 2, 3 |

In the classes with one offset, every observed difference quotient is exactly 9. Other classes do not have an exact slope of 9 between consecutive samples. For example, H16a has X(70) = 632, X(78) = 705, and X(86) = 775. The increments for +8 are 73 and 70, not 72. H16b has X(66) = 596 and X(74) = 666, an increment of 70.

This defect does not refute 9n + O(1). It refutes the stronger statement that each class modulo 8 has one fixed offset. The interval 0 through 7 is correct on the supplied finite set.

## Independent strip counts and local crossing argument

`periodic.py` builds each infinite periodic edge strip with straight interior continuations. It counts pairs whose smallest longitudinal endpoint coordinate is in one reference period. A margin of eight cells is more than enough: each knight move spans at most two cells in either coordinate, so edges in a crossing pair cannot have arbitrarily distant endpoints.

Both H16a and H16b give 16 crossings per eight bottom columns. VerticalEdge gives 10 crossings per four left rows. Rotation preserves crossings. Thus the two horizontal bands contribute 2(16/8)n, and the two vertical bands contribute 2(10/4)n. Their sum is 9n. The straight interior has no crossings.

A fixed corner zone changes only a bounded number of edges. Each of these edges can cross only edges within a fixed distance, since all moves have bounded length and every cell has degree two. Thus corner changes, overlaps between bands near a corner, and incomplete periods contribute O(1). They cannot change the coefficient 9.

The read-only audit of `kt/board.py` shows fixed template depths of four bottom rows and two left columns for these files. `build_skeleton` uses four Z by Z corner zones. `assemble.py` tries the finite list 6, 7, 8, 10, 12 by default, although callers can supply another list. These 69 files all use Z = 6. The local phases depend on n modulo 8; no growing band or corner was found in these witnesses.

## Hidden dependence: outside path matching

**The local phase modulo 8 does not determine the global path matching.**

`topology.py` removes the four 6 by 6 corner squares and follows every remaining path. It records the two corner endpoints in coordinates relative to their corners. It also checks that no component outside the corners is a closed cycle.

For BOTH templates, EACH residue class modulo 8 has THREE distinct outside path matchings in the supplied data. The number of paths is constant within each such class, but the endpoint pairing changes. When grouped modulo 24, every tested class has exactly ONE matching. See `topology.txt`.

This is direct evidence of a size dependence that a proof based only on local phases modulo 8 would miss. The pattern is consistent with a finite permutation of strands of order three, but that cause has not been proved here. The modulo-24 result is a finite observation, not an induction proof.

A fixed corner size bounds the crossing cost IF a completion exists. It does not prove that a completion exists for every larger even n. Finite solver successes do not prove this either. A proof must show that the fixed outside graph has no closed component and that its corner endpoint matching has a bounded period for all sufficiently large n. Then one can reuse checked corner templates for every resulting state. The present data suggest that n modulo 24 is sufficient. This remains to be proved.

## Scope and next action

These are feasible witness checks. I did not independently verify any solver optimality certificate or any lower bound. In particular, an `OPTIMAL` field for a corner problem does not prove a globally minimum-crossing tour, nor does this audit verify such a claim.

The next action is to prove the outside path recurrence under n -> n + 24, then supply one reusable corner template for each even residue modulo 24. That would close the main gap in the general upper-bound claim. No solver was run in this audit. All scripts ran as single Python processes, one at a time.

# Claim 2: at least 8n - 64 turns — 2026-10-02

**Verdict: PASS. The counting proof is valid for every spanning 2-factor on an n by n knight board with n >= 8. No connectivity assumption is needed.**

I checked each step of `w-turnstheory/FINDINGS.md` against the move definition, without importing its checker.

1. Column 0 has n turns. Both edges have a positive column displacement, so the two edges cannot be opposite.
2. At column 1, the edges counted by p have column displacements -1 or +2. At column 2, they have displacements -2 or +1. No pair in either set is opposite. Thus p = 2 forces a turn; p <= 1 gives the trivial inequality t >= p - 1. An edge from column 0 or column 3 to columns 1 or 2 contributes exactly once to the sum of p. There are 2n edges from column 0 and B from column 3. No edge is counted in both groups. Thus T1 + T2 >= B.
3. At column 3, q = 0 excludes all negative column displacements. Both chosen edges then point to higher columns, so the cell turns. For q = 1 or 2, t >= 1 - q is automatic. Thus T3 >= n - B. This remains correct when B > n; a negative intermediate lower bound causes no problem.
4. Adding these inequalities gives 2n turns in the four-column strip. Restrictions at the top, bottom, or opposite side only remove allowed local choices. They do not invalidate an inequality.
5. Reflection and exchange of the coordinates give the same result at all four sides. For n >= 8, opposite strips are disjoint. Only the four disjoint 4 by 4 corner squares are counted twice. Their total turn count is at most 64. Therefore T >= 8n - 64. For n = 8, the four squares cover the board and the same counting identity holds.

This proves the asymptotic coefficient 8 in the lower bound. It does not prove the exact bound T >= 8n. The proof applies to simple degree-two subgraphs of the knight graph, not a graph that allows a doubled edge.

## Independent computational checks

`turn_audit.py` exhaustively checks all locally allowed pairs in the left half-plane. The counts in columns 0, 1, 2, 3 are 6, 15, 28, 28: all 77 pairs pass.

The script also scans all project JSON files with a top-level `tour` field. In the 2026-10-02 snapshot, it found 83 files. All four edge strips in every file have at least 2n turns. The smallest excess above 2n is 9. This check uses turn indicators from determinants of the decoded move vectors. Full tour validity is a separate check; the earlier 69-file audit supplies that check for its own snapshot.

For a small-board test, I generated 100 random 2-factors at each of n = 6, 8, 10, with fixed random seed 20261002. Each factor is the union of two edge-disjoint perfect matchings. The script checks degree two and reciprocal edges, counts components, and tests all four strips. All 300 factors pass. The smallest strip counts were 21, 26, 33, against required bounds 12, 16, 20. The samples include both single cycles and multiple cycles: component counts range from 1 to 4, 1 to 7, and 1 to 9, respectively. The samples are not uniform random factors and do not establish an exact minimum. No 2-factor exists for odd n, since the two color classes of the bipartite board then have different sizes.

Exact per-file and per-sample data are in `turn_results.json`. No solver was used. These tests support the proof; the finite local inequalities and the counting identity establish the theorem.

# Claim 3: T18 heel and candidate 8.5n turn rate — 2026-10-02

**Verdict: the strip and all nine available full-tour witnesses pass. The coefficient 8.5 follows from the fixed strips, conditional on a completion of bounded corner size for all larger n. General existence is not proved by these finite files.**

`t18_audit.py` independently checks the template codes, reciprocal edges, bottom boundary, turns, crossings, and terminal paths. It confirms 18 turns and 31 crossings per eight columns. The terminal matching is 0--7, 1--4, 2--6, 3--5, repeated by translation through eight columns. The eight traced terminal paths cover all 32 cell classes in one period, so no separate strip cycle remains. This verifies feasibility. It does not independently certify the reported optimum of 18 in the worker's search model.

The four-row VerticalEdge template has eight turns per four rows: each of its eight cells is a turn. With two T18 bands and two VerticalEdge bands, the total leading turn count is 2(18/8)n + 2(8/4)n = 8.5n. Every cell in the straight interior has zero turns. A bounded number of corner cells changes only the constant term.

The full-tour checker confirms one closed cycle, all n² cells, and the stored turn and crossing counts for these files in `runs/t18/`:

| n | Turns | Crossings | T - 8.5n | Turns in four 6 by 6 corners |
| --- | --- | --- | --- | --- |
| 64 | 529 | 796 | -15 | 88 |
| 66 | 542 | 816 | -19 | 82 |
| 68 | 560 | 843 | -18 | 84 |
| 72 | 597 | 897 | -15 | 88 |
| 74 | 612 | 916 | -17 | 84 |
| 80 | 666 | 999 | -14 | 89 |
| 82 | 679 | 1019 | -18 | 83 |
| 88 | 735 | 1099 | -13 | 90 |
| 90 | 748 | 1120 | -17 | 84 |

All four edge strips in each file also satisfy the 2n turn bound. Source hashes and full counts are in `t18_results.json`. All nine files report FEASIBLE, with Z = 6; they are not certified corner optima.

For n modulo 8 equal to 0, the observed turn slopes over steps of eight are 8.5, 8.625, 8.625. For residue 2, they are 8.75, 8.375, 8.625. These are not all exactly 8.5. The difference is entirely in the corner turns: after subtracting turns in the four 6 by 6 squares, the count is exactly 8.5n - 103 in residue 0 and 8.5n - 101 in residue 2. Thus the finite data support the stated asymptotic candidate, including its corner term.

Residue 6 has no full-tour witness in this snapshot. Residue 4 has only the n = 68 witness, so no within-class slope can be checked. As with Claim 1, a proof must show that the outside paths have a suitable finite recurrence and that fixed corner templates complete every required state. The strip permutation alone does not establish that result. The construction team must supply this argument before the general upper bound is called proved.

# Claim 4: period 24 and reuse of fixed corners — 2026-10-02

**Verdict: PASS, with the explicit path-coverage and induction argument below. The corner files give the claimed constructions for every even n >= 48.**

The Integrator's period argument has the correct mechanism. An endpoint matching alone would not be enough: it could omit a closed component outside the corners. The required invariant is the endpoint matching, with each endpoint identified by its corner cell and incident direction, PLUS coverage of every outside cell by those paths. The strip checks and the monotone four-strand transfers supply that extra condition here.

## Why matching permits corner reuse

Remove the four corner squares. Suppose every remaining component is a path with both ends at corner incidences. Contract each such path to an edge, keeping multiplicity and the endpoint incidences. The result, together with the unchanged corner edges, determines every cycle of the full graph. Changing path lengths does not change this cycle structure. Thus one checked base tour remains one tour whenever the incidence matching is unchanged and no extra outside cycle appears. Local equality of the interface moves also preserves degree two and reciprocal edges. These conditions are sufficient for every reuse, with no further global test needed.

`period24.py` does include the incident direction in its matching and rejects uncovered outside cells. Those are necessary details. The finite tests in that script alone do not prove all sizes; the transfer argument below supplies the induction.

## Independent local checks and transfer argument

`strand_audit.py` reads the template strings from the corner files. It traces all local strip paths, checks reciprocal path steps, and checks coverage of every cell class in one period. It imports no worker code. The exact endpoint maps, in local line labels c = x + 2y, are:

- H16a bottom: (0,4), (1,7), (2,5), (3,6), repeated by translation through 8.
- T18 bottom: (0,7), (1,4), (2,6), (3,5), repeated by translation through 8.
- VerticalEdge: (0,5), (1,4), (2,7), (3,6), repeated by translation through 8.

Translation through eight line labels is an exact symmetry of the template, so these finite traces specify the matching for every integer line label. Every strip cell is on one of the traced terminal paths; there is no omitted strip cycle. Straight interior segments stay on one line and contain no cycle.

After the published shifts and reflections, each pair of side matchings joins consecutive four-line groups. One matching joins one pair of groups, and the other joins the next pair. Thus the union consists of four strands that advance through the groups. It has no closed component in a pure region. Applying two successive four-line steps gives these permutations for an eight-line advance, with the starting group at a multiple of eight:

| Template | bottom-left region | middle region | top-right region |
| --- | --- | --- | --- |
| H16a | [1,2,0,3] | [0,1,2,3] | [0,2,3,1] |
| T18 | [2,1,3,0] | [0,1,2,3] | [1,3,2,0] |

Every listed permutation has cube equal to the identity. The script also checks the alternate four-line starting group. Its permutations have the same property. These are complete residue checks, not a sample of long paths. The exact output is in `strand_results.txt`.

Under n -> n+24, the four corner line coordinates shift by 0, 24, 48, 72 for BL, BR, TL, TR. The side phases stay unchanged modulo eight. Each of the three intervals between successive corner regions therefore gains 24 line labels. This inserts three eight-line transfers, with composite permutation equal to the identity. The finite transition pieces at the corners and the changes of side stay unchanged in relative coordinates. An inserted transfer consists only of four through-paths, so it cannot introduce a separate cycle. This proves both matching preservation and outside path coverage under the induction step.

The region limits c = n and c = 2n-2 in the Integrator's prose are schematic. The exact limits for the straight interior depend on the fixed band depths. These constant shifts belong to the finite transition pieces; they do not affect the induction.

## A conservative separation bound for the induction

To avoid an unstated assumption that the corner transition pieces are separated at the smallest size, the audit uses n >= 72 for the induction and explicitly checks the smaller base sizes.

A 6 by 6 corner square has line-label ranges [0,15], [n-6,n+9], [2n-12,2n+3], and [3n-18,3n-3]. An independent trace of each band path shows a line-label span of at most 12 (the largest case is the T18 path from line 3 to line 5, whose visited labels range from -2 through 10). VerticalEdge has span at most 5. The side switches of the straight interior rectangle also lie in the respective corner ranges.

Expand each corner line range by 16 on both sides. This contains every band path affected by a corner and the finite side-switch pieces. The gaps between consecutive expanded ranges have length n-53, which is at least 19 for n >= 72. A gap therefore has room for a complete four-strand transfer with its start aligned to a multiple of four. All cells between the finite transition pieces are in the pure strip/straight-line model described above. The induction can insert 24 labels in each such interval. The gaps only grow with n.

The twelve even sizes 48 through 70 are checked directly. The twelve sizes 72 through 94 are also checked directly from the same corner files. Induction from the latter twelve sizes covers every larger even size. This establishes the advertised threshold 48 without relying on an unproved small-size separation assumption.

## Independent rebuilds and counts

`reuse_audit.py` builds the entire grid directly from template move codes, phase formulas, and the zone-relative moves in each corner file. It imports only the verifier's own code and Python standard-library modules. It does not call `build_skeleton`, `apply_zone`, `complete`, or any worker checker. No solver was run.

For EACH of the 24 corner files (12 H16a and 12 T18), I rebuilt and checked n = n0, n0+24, and n0+192. This gives 72 independently checked tours, including all even large sizes 240 through 262 for each template family. Every tour has one closed cycle through n² cells. Every outside cell belongs to a corner-to-corner path. The full incidence matching agrees with the base matching in every case.

All counts agree with the claimed exact formulas. In particular:

| Family | n | Crossings | Turns |
| --- | --- | --- | --- |
| H16a | 240 | 2165 | 2433 |
| H16a | 246 | 2217 | 2494 |
| H16a | 254 | 2287 | 2573 |
| H16a | 262 | 2360 | 2660 |
| T18 | 240 | 3039 | 2023 |
| T18 | 246 | 3111 | 2071 |
| T18 | 254 | 3213 | 2139 |
| T18 | 262 | 3317 | 2207 |

Source hashes and every rebuilt-tour count are in `reuse_results.json`. For H16a, X - 9n equals 5,0,7,3,5,0,7,1,5,0,7,2 for residues 0,2,...,22 modulo 24. For T18, T - 8.5n equals -17,-19,-19,-20 for residues 0,2,4,6 modulo 8, for every checked base and reuse.

The exact count recurrence also follows from locality. Unchanged corners have unchanged local counts. Adding 24 to n adds three complete horizontal periods per horizontal side and six complete vertical periods per vertical side. Thus H16a gains 216 crossings and 246 turns; T18 gains 306 crossings and 204 turns. Straight interior length changes add no turns or crossings. The constant-size interactions between adjacent side bands stay in the unchanged corner neighborhoods. Together with the base counts, this gives the stated formulas for all induction steps.

## Remaining documentation work

The main gap from Claims 1 and 3 is closed by the transfer and path-coverage argument above. The final research write-up should include the corner-incidence contraction lemma, the complete local endpoint maps, and an explicit induction threshold. The checked constructions are upper bounds; this audit does not certify any global optimum or any solver claim that a particular corner completion is optimal.

# Claim 5: lane-free LF1, crossing rate 47/6 — 2026-10-02

**Verdict: PASS for the three full-tour witnesses, all four gadget rates, and the stated infinite-region strand counts. The finite-window search is a filter, not a general proof of absence of cycles. An independent exact periodic-state check supplies that proof for LF1.**

## Full tours

`lf1_audit.py` uses the independent checker from Claim 1. All three `LF1_*.json` files have valid reciprocal knight edges and exactly one closed cycle through every cell. Every stored crossing and turn count agrees with the independent count.

| n | Crossings | Turns | X - (47/6)n |
| --- | --- | --- | --- |
| 72 | 575 | 797 | 11 |
| 96 | 763 | 1073 | 11 |
| 120 | 951 | 1349 | 11 |

Each step of 24 increases crossings by 188, so the measured slope is exactly 47/6, not a rounded 7.8333. The measured turn formula is 11.5n - 31. All three files use phases (xb, xt, yl, yr) = (1,1,0,0) and four 6 by 6 corners.

## Independent gadget counts

The periodic crossing counter includes straight interior continuations and counts each unordered crossing pair once per period. It uses proper intersections with integer arithmetic. A separate local check verifies two distinct neighbors, reciprocal edges, the board boundary, and straight interfaces. Terminal path traces cover every cell class of each strip; no strip cycle is omitted.

| Side | Period in board units | Crossings per period | Rate |
| --- | --- | --- | --- |
| bottom | 6 columns | 11 | 11/6 |
| top, before rotation | 6 columns | 18 | 3 |
| left | 4 rows | 8 | 2 |
| right, before rotation | 4 rows | 4 | 1 |

Rotation preserves crossings. The sum is 11/6 + 3 + 2 + 1 = 47/6. The exact templates read from the tour files are:

Bottom:
```text
46 46 46 56 56 56
45 14 14 14 45 45
05 05 15 15 15 05
01 01 01 01 01 01
```

Top (rotate this template by 180 degrees):
```text
46 56 46 56 46 56
24 14 24 14 24 14
56 05 56 05 56 05
01 01 01 01 01 01
```

Left:
```text
02 24
02 24
02 24
02 24
```

Right (rotate this template by 180 degrees):
```text
23 27
23 27
23 27
23 27
```

## Exact line matchings

The independent terminal traces give these local involutions on integer line labels c = x + 2y:

- Bottom: c maps to c-3 for c modulo 6 in {0,1,2}, and to c+3 for residues {3,4,5}.
- Top, before reflection: even c maps to c+1; odd c maps to c-1.
- Left: even c maps to c+5; odd c maps to c-5.
- Right, before reflection: even c maps to c-3; odd c maps to c+3.

For the actual phases, the global maps are obtained by shifts xb and 2yl, and reflections about xt+2(n-1) and n-1+2yr. These shifts and reflections were applied independently in the checker. The resulting region certificates agree for n = 72, 96, 120.

## Exact proof of no finite region cycle

A bounded unroll can miss a cycle that extends beyond its window. To avoid that gap, the independent checker builds a finite state system that represents the whole infinite periodic region.

A state consists of a line label modulo P and the color of the next matching edge. P is a common period of the two matchings. Each step follows the selected matching and changes color. The checker verifies that this state map is a permutation and enumerates every state cycle. During each traversal it also tracks the actual integer line coordinate, not only its residue. The net displacement is an integer multiple of P.

A zero-displacement state cycle lifts to a finite region cycle. A nonzero displacement repeats with a fixed translation, so its lift is an infinite path. Thus checking every finite state cycle gives an exact decision for the infinite region. If a state cycle has displacement d, it gives |d|/P directed lifted paths. The two traversal directions describe the same undirected path, so the sum over all state cycles is divided by two to count strands.

Results:

| Region | Chosen period P | State-cycle displacements | Infinite strands | Finite cycles |
| --- | --- | --- | --- | --- |
| BL | 24 | -24, +24, -24, +24 | 2 | none |
| MID | 8 | four +8 and four -8 | 4 | none |
| TR | 24 | -24, +24, -24, +24 | 2 | none |

These periods need not be minimal; they cover all states exactly. The certificates, including every state in every cycle, are in `lf1_results.json`.

The cut counts are {2,4,6} in BL, {4} in MID, and {2} in TR. All are even. The varying BL count is not a defect: one strand can cross a line-label cut more than once. The number of strands and the number of edges across a cut are different quantities.

## Scope of the pairing argument

The local lane-free claim is sound for LF1: each region has the stated number of infinite paths and no finite cycle. `combos2.py` and `strands.py` test finite windows and cut parity. Those tests alone are not sufficient for arbitrary future gadgets; the exact periodic-state test above is a suitable replacement for the cycle check.

No finite region cycles, together with even cuts, does not by itself prove that four corners can join every path into one board tour. The three full-tour checks establish that completion for the supplied sizes. A bound for all larger board sizes still requires the complete corner-incidence recurrence and reusable corner completions, as in Claim 4. This audit does not claim that LF1 already supplies that global theorem, and it does not certify the solver's reported corner optimality.

All checks used one Python process at a time, no solver, and no worker-code imports. Source file hashes, exact counts, local maps, and the finite-state certificates are in `lf1_results.json`. The full audit runs with `python3 w-verifier/lf1_audit.py`.

## Claim 5 update: LF2, crossing rate 22/3 — 2026-10-02

**Verdict: PASS for all six LF2 witnesses, the new top rate, and the infinite-region checks. The exact offset +21 holds in the tested residue n = 0 modulo 24; it is not a single offset for every tested even size.**

`lf2_audit.py` independently checks all six available `LF2_n*.json` files. Every file has one closed knight's tour through all n² cells, and every stored crossing and turn count agrees.

| n | Crossings | Turns | X - (22/3)n |
| --- | --- | --- | --- |
| 72 | 549 | 765 | 21 |
| 74 | 564 | 786 | 64/3 |
| 76 | 578 | 809 | 62/3 |
| 78 | 592 | 832 | 20 |
| 96 | 725 | 1029 | 21 |
| 120 | 901 | 1291 | 21 |

For n = 72, 96, 120, each step of 24 adds 176 crossings: the slope is exactly 22/3. The Integrator's current findings correctly restrict the formula with offset +21 to n = 0 modulo 24. At n = 74 and 76 the expression (22/3)n+21 is not even an integer, so that restriction is necessary.

The new top template, before its 180-degree rotation, is:

```text
36 56 36 56 36 56
23 13 23 13 23 13
26 27 26 27 26 27
67 67 67 67 67 67
```

The independent periodic counter finds 15 crossings per six columns, or 5/2 per column. The other three templates are unchanged from LF1 and independently recount as 11/6, 2, and 1 per board unit. Their sum is 11/6 + 5/2 + 2 + 1 = 22/3.

The top terminal map is c -> c+7 for even c and c -> c-7 for odd c. Reciprocal edges, the board boundary, straight interfaces, and full strip-path coverage all pass. In particular, no separate cycle remains inside the top strip.

The exact periodic-state check from the LF1 audit was repeated with each LF2 file's actual phases. All six certificates have no zero-displacement state cycle. The strand counts are again BL = 2, MID = 4, TR = 2. The cut-count sets are {2,4,6}, {4}, and {4,6}, respectively. The top-right region has two strands although its paths cross some cuts more than twice; this is valid.

The stored right-side phase is 1 at n = 72 and 78 and 0 in the other files. These phases produce the same right strip because its four rows are identical. The checker nevertheless uses each stored phase explicitly.

No global LF2 induction or reusable-corner theorem is claimed by this audit. The six finite witnesses and the local region result are verified. The next step for a bound at all larger even sizes remains a corner-incidence recurrence and reusable completions.

One separate documentation error was found in the Integrator's LF1 section: it writes `23n/3 + 11`. Its listed LF1 counts and the independent rates instead give `(47/6)n + 11`. This is a transcription error in that section, not an LF2 defect. I did not edit the Integrator's file.

Exact hashes, rates, maps, counts, phases, and all state-cycle certificates are in `lf2_results.json`. Run `python3 w-verifier/lf2_audit.py`. No solver or worker code was used.

# Claim 6: TT16 has 8n - 14 turns — 2026-10-02

**Verdict: PASS for the construction, with the exact periodic-state and corner-reuse argument below. For every even n >= 48, the supplied TT16 corner files construct one closed tour with T(n) = 8n - 14. This is not a claim that 8n - 14 is the minimum.**

The Integrator's `periodic.py` detects a period in a finite sample. That scan alone is not an induction proof. The independent certificates below establish why period eight is sufficient and why no outside cycle is introduced.

## Witnesses and independent rebuilds

`tt16_audit.py` checked all 13 supplied TT16 tour files: nine under `tours/` and the four base certificates under `tours/certificates/`. Every file has exactly one closed knight's tour through n² cells. All stored crossing and turn counts agree with the independent recount.

The checker also assembled grids directly from the four corner files, with no worker-code import. It uses the supplied templates, phases (0,1,0,0), and zone-relative moves in four 6 by 6 squares. It checked every even n from 48 through 134, plus n = 312, 314, 316, 318: 48 independent rebuilds. All pass the one-cycle test, the outside-path coverage check, the full corner-incidence matching comparison within each residue modulo eight, and both exact count formulas.

| n | Turns | Crossings |
| --- | --- | --- |
| 48 | 370 | 454 |
| 56 | 434 | 530 |
| 58 | 450 | 548 |
| 60 | 466 | 570 |
| 62 | 482 | 592 |
| 312 | 2482 | 2962 |
| 314 | 2498 | 2980 |
| 316 | 2514 | 3002 |
| 318 | 2530 | 3024 |

The independent assembler successfully reuses the four supplied corners even at n0-8 = 48,50,52,54. It does not need the separately solved small-board corner choices to cover those sizes.

All source hashes, local certificates, and individual results are in `tt16_results.json`; the concise run log is `tt16_run.txt`. No solver was used. The audit does not certify the reported corner optimality.

## Exact local data

The bottom and top template is:

```text
26 26 26 26 26 26 26 26
36 26 26 46 26 46 36 26
25 26 25 26 26 25 26 25
16 67 06 16 06 16 16 67
```

The left template has four identical `23 27` rows. The right template has four identical `02 24` rows. Top and right are rotated by 180 degrees when placed on the board.

Independent counts and path traces give:

| Local template | Board period | Turns | Crossings | Largest line-label span of one band path |
| --- | --- | --- | --- | --- |
| bottom/top T16 | 8 columns | 16 | 26 | 9 |
| left | 4 rows | 8 | 4 | 3 |
| right | 4 rows | 8 | 8 | 5 |

Reciprocal edges, distinct neighbors, the board boundary, and straight interfaces pass. Terminal paths cover every periodic cell class, so there is no hidden strip cycle.

The local T16 terminal map on residues 0 through 7 is

```text
0 -> 9,  1 -> -8,  2 -> -5,  3 -> 10,
4 -> -3, 5 -> 12,  6 -> 15,  7 -> -2,
with f(c+8) = f(c)+8.
```

The left map is c -> c-3 for even c and c -> c+3 for odd c. The right map is c -> c+5 for even c and c -> c-5 for odd c. Shifts and reflections use the actual phases and n.

## Why the outside matching has period eight

Apply the exact periodic-state method from Claim 5. A state is (line label modulo eight, next matching color). Follow both alternating matchings, retaining the lifted integer coordinate. The checker covers all states for each even residue of n modulo eight.

| Region | Directed state cycles | Displacements | Undirected infinite strands | Largest span during one state-cycle traversal |
| --- | --- | --- | --- | --- |
| BL | 4 | two +8, two -8 | 2 | 15 |
| MID | 8 | four +8, four -8 | 4 | 8 |
| TR | 4 | two +8, two -8 | 2 | 17 |

No state cycle has zero displacement. Hence no pure region contains a finite cycle. Each winding number is +1 or -1, so translation by eight preserves each individual lifted strand; it does not permute different strands. This is the additional fact needed for period eight. Merely counting 2,4,2 strands would not establish it.

The state-cycle coordinates also bound every local reversal in line-label order. Each path repeats a finite coordinate sequence, of span at most 17, translated by eight per repeat. A component cut off by one end of a long region can therefore only make a bounded excursion near that end; it cannot reach across an arbitrarily long region. Inserting one additional period in a region leaves the local returning paths unchanged and extends each through-path on the same strand.

Under n -> n+8, the corner line coordinates shift by 0,8,16,24 for BL,BR,TL,TR. The global phases and all relative interface moves stay unchanged. Each of the three intervals between corner transition pieces gains eight line labels. The returning-path pattern at each end stays fixed, and each through-path is extended on its own strand. Thus the complete corner-incidence matching stays fixed, including the incident direction at every corner cell. All added cells lie on these paths; no new outside cycle can occur.

## Explicit induction threshold

As in Claim 4, the line ranges of the four 6 by 6 corner squares are [0,15], [n-6,n+9], [2n-12,2n+3], and [3n-18,3n-3]. Expand each range by 16. Since every complete band path has span at most nine, this contains all band paths affected by a corner, as well as the side-switch pieces of the straight interior.

Consecutive expanded ranges are separated by n-53. Use the conservative induction threshold n >= 128, giving a separation of at least 75. A buffer of twice the largest state-cycle span, 34, at each end contains all local returning pieces. These buffers are disjoint and leave a nonempty middle interval. An eight-label period can be inserted there: translation by eight fixes every strand, at any cut phase. The local caps and all returning pieces stay unchanged. The separation increases with n, so this step applies repeatedly.

The independent direct rebuilds cover all even n = 48..134. In particular, n = 128,130,132,134 provide the four residue bases for this induction, while 48..126 are covered directly. This proves the stated threshold 48 without assuming that the smallest boards already have separated proof buffers.

Contract every outside path to its two corner incidences. Since coverage and the incidence matching are unchanged, the resulting finite graph with the reused corner edges has the same cycle structure as the checked base tour. Therefore every induction step gives one closed tour.

## Exact count formulas and implication

The corner moves and their local neighborhoods stay unchanged. For each increase of eight in n, the two horizontal bands add 2·16 turns and the two vertical bands add 2·8·2 turns: 64 in total. Their crossing increment is 2·26 + 8·1 + 8·2 = 76. The straight interior adds neither turns nor crossings. The checked base counts therefore give

```text
T(n) = 8n - 14,
X(n) = 9.5n + c,
c = -2,-3,0,+3 for n modulo 8 = 0,2,4,6.
```

Together with the independently checked corner lower bound, the minimum turn count satisfies

```text
8n - 28 <= T_min(n) <= 8n - 14    for every even n >= 48.
```

Thus the asymptotic turn coefficient is exactly eight, with at most 14 turns between these bounds. The exact finite-size optimum remains open.

The paper's final open-question section in `paper.txt` states the literal conjecture that the minimum number of turns is at least 8n. These verified TT16 tours have fewer than 8n turns. They refute that literal inequality while establishing its proposed leading coefficient asymptotically. The two claims must be distinguished in the research summary.

The visualization set predates TT16. Its T18 figure remains a valid record of that improvement, but the turn summary should next be updated from [8,8.5] to the single leading coefficient 8, with the finite bounds [8n-28,8n-14] shown separately.

# Claim 7: audit of the explicit block-insertion proofs — 2026-10-02

**Verdict: PASS. `w-turnstheory/PROOFS.md` gives a valid finite-certificate proof of both all-size constructions. The H16a insertion preserves the complete port matching, introduces no cycle, and produces the specified larger reduced graph. I found no missing condition in the insertion step.**

## Standalone checker run

I ran a byte-identical copy of `w-turnstheory/check_upper_proofs.py` as `w-verifier/claim7_standalone.py`. This preserves its project-root path and puts its generated report in the verifier directory, so the run does not overwrite another worker's report. Both script files have SHA-256:

```text
b6ec11dd9ca3f814077ccddf268eac325085d4925a2f1307e478d45d21425595
```

The run passed all 64 base tours and all 48 regional transfers, including the larger physical slabs and count increments. The local cost table matches the independent counts from Claims 4 and 6. The output is `claim7_run.txt`; the complete generated certificate is `upper_proof_checks.json`. No solver or nonstandard library was used.

## H16a: ports and insertion

1. A raw knight edge changes c = x + 2y by at most five. A straight interior edge changes c by zero. Therefore no edge skips across an eight-label block. This is needed before its connections can be represented entirely by boundary ports.
2. A port name records the band, both endpoint depths, and both endpoint c-offsets relative to the cut. These data identify the cut edge. Equal port names at consecutive cuts give the correct gluing, not an arbitrary ordering of endpoints.
3. The slab checker traces from each unmatched boundary port and then checks that every slab vertex was visited. It therefore detects both cycles that touch a traced path and separate cycles with no port. It does not infer coverage merely from the expected number of strands.
4. For H16a, all ports are on through-paths: four left ports and four right ports, with no same-side return. The permutations are [1,3,2,0], [0,1,2,3], [0,2,3,1]. Their cubes are the identity. The nontrivial permutations have a different port basis from the line-label permutations in Claim 4; this is consistent and does not change their order.
5. Insertion replaces ONE eight-label block by FOUR copies. The relevant identity is rho^4 = rho, which follows from rho^3 = identity. It is not necessary for one block itself to have identity matching.
6. Since all H16a paths run from left to right, composition cannot produce an internal closed component. The checker still checks this explicitly. It also compares the complete actual 32-label slab in the larger board to the one-block matching, and checks coverage of all its vertices.

These steps establish the required topological replacement, including the condition that no new component is hidden inside the inserted material.

## Coordinate shifts: independent exterior-graph test

I wrote `claim7_transport.py` to check the part that a matching test alone does not establish: whether the rest of the larger board is the claimed translated copy of the old exterior.

This checker uses the verifier's own assemblers from Claims 4 and 6. It retains all band and corner vertices, suppresses each remaining straight path, and checks that this process covers all board cells. It then removes the three selected slabs. Every resulting cut edge becomes a labeled port. The checker translates every old exterior vertex using the proof's coordinate table and compares the entire graph against the new exterior obtained after deleting the three longer slabs. The comparison includes both the vertex set and edge multiplicities, not only the terminal matching.

The exact exterior graphs agree for all 16 cases: all 12 H16a residues at n = 96..118 and all four TT16 residues at n = 96..102. Output: `claim7_transport.json`.

The coordinate table is also correct algebraically. Each listed translation changes c by r*p and preserves band depth:

- bottom: (r*p,0);
- left: (0,r*p/2);
- right: (p,(r-1)*p/2);
- top: ((r-2)*p,p).

At the four corners, the formulas give (0,0), (p,0), (0,p), (p,p), as required. Since p is 8 or 24, the shifts preserve the horizontal period eight and vertical period four. The H16a phase formulas also remain unchanged under n -> n+24. For each straight run, translated ports retain a common line label. Straight runs can change length without changing their connection; no internal straight cycle is possible.

This finite comparison checks every local phase of the construction. The algebra and the fixed templates make the same comparison valid at every later induction step; it is not an extrapolation from the measured exterior graph sizes.

## Margins and induction coverage

The corner c-ranges are [0,15], [n-6,n+9], [2n-12,2n+3], and [3n-18,3n-3]. They lie outside the proof's three open working ranges with margin 24. The changes of band pair caused by the fixed strip depths also lie within those excluded transition ranges.

All selected blocks lie strictly inside their pure regions for n >= 96. The checker tests these inequalities. On a later step, the chosen middle cut shifts by p and the chosen last cut shifts by 2p, exactly as the insertion table requires; the first cut stays fixed. Their phases stay fixed, and their distance from a corner does not create a new boundary case as n grows.

The finite bases are sufficient: H16a directly covers every even n = 48..118, including one induction base in 96..118 for each residue modulo 24. TT16 covers every even n = 48..102, including one induction base in 96..102 for each residue modulo eight. The four small TT16 full-tour files are explicitly checked. There is no uncovered size between the finite checks and the induction.

## TT16 cross-check

The proof correctly retains the same-side return paths. The complete matchings in the document agree with the checker. For each region, M^2 = M and the composition has no closed component. Thus replacing one block by two keeps both the through-connections and the return connections. This is a more explicit certificate for the bounded-return reasoning in Claim 6 and confirms its conclusion.

The composition routine does not silently discard a cycle at the join: it traces from outer ports and then requires every gluing vertex to have been visited. Its larger-slab check also verifies the actual graph, not only an abstract composition.

## Locality of counts

Topology and geometry are separate parts of the proof. Equal port matching alone would not preserve turn or crossing counts. Here the coordinate construction inserts actual periodic band material and leaves the local joins and corner neighborhoods unchanged. Interior straight edges are parallel. All relevant band-to-interior crossings lie in a bounded neighborhood of the band.

The standalone counter includes the straight continuations, uses proper integer orientation tests, and charges each unordered crossing pair once to a longitudinal period. The resulting H16a counts are 16 crossings per eight columns at each horizontal side and 10 per four rows at each vertical side. For +24 in n, the increment is 2·3·16 + 2·6·10 = 216. The TT16 turn increment for +8 is 2·16 + 2·2·8 = 64. These agree with direct base insertions and the previous independent counters.

No additional proof gap was found. The document can now serve as the all-size proof, supported by its finite certificates. An optional clarity improvement is to include the four explicit corner c-ranges above next to the margin argument. The proof does not establish global optimality of the H16a crossing counts or the TT16 finite additive constant.

# Claim 8: LF4 period-48 insertion and 343n/48 crossings — 2026-10-02

**Verdict: PASS. Section 5 of `w-turnstheory/PROOFS.md` proves that the supplied LF4 family gives one closed tour with X(n) = 343n/48 + b[n mod 48] for every even n >= 96. All 24 printed constants are correct. No missing insertion assumption was found.**

## Standalone and independent checks

I ran byte-identical copies of `check_lf_proof.py` and its `check_upper_proofs.py` dependency in `w-verifier/claim8_runner/`, with copies of the 24 corner certificates. The supplied checker passed all 24 base tours, all 24 size-(n0+48) tours, all 72 block checks, and every crossing increment. The generated report is `claim8_runner/lf_proof_checks.json`; the run log is `claim8_run.txt`.

The LF checker SHA-256 is `53a8245b07e29898b0cf74731117013c3fa46beca1a1483c69447f6c6654f339`. The helper hash remains `b6ec11dd9ca3f814077ccddf268eac325085d4925a2f1307e478d45d21425595`, as in Claim 7.

I then ran `claim8_audit.py`, which imports only the verifier's own code and the standard library. It independently assembles every corner certificate at n0 and n0+48, checks one closed tour through n² cells, and recounts crossings and turns. All 48 tours pass. It parses the rational constants directly from Section 5 and checks every one against its own base count.

The independent exterior-graph transport test also passes all 24 residues. It suppresses straight interior paths, removes the three old blocks and the corresponding longer new blocks, applies the coordinate-shift table, and compares all remaining vertices and edges, including the labeled cut ports. The two exterior graphs are exactly equal in every case. Results, counts, and source hashes are in `claim8_results.json`; the run log is `claim8_independent_run.txt`.

## Complete block matchings

I compared the pairs printed in Section 5 directly against the generated certificates. All 16 bottom-left pairs, four middle pairs, and eight top-right pairs agree. The matchings include every same-cut return path. Their continuing strand counts are 2,4,2, but those counts alone would not suffice for insertion.

For each block, the supplied checker verifies:

- Every block vertex lies on a path between two boundary ports; no unrecorded closed component remains.
- Left and right port names agree under translation by the block width.
- Composing two complete matchings gives M² = M with no cycle at the join.
- The matching of the actual enlarged slab equals the original matching, with full vertex coverage.

Idempotence and the cycle check justify every positive power of M, not just the square. Once earlier pieces have been contracted to their outer matching, any new cycle at the next join would also appear when composing M with M. The checked composition excludes that case.

For widths 12,8,16, replacing one block by 5,7,4 copies adds exactly 48 labels in each region. The resulting widths are 60,56,64. All three replacements preserve the complete matching and introduce no component.

## Phase preservation and coordinate shifts

The nontrivial phase detail is the first region. Its 12-label translation moves the bottom by 12 columns and the left strip by six rows. Six is not a multiple of the nominal four-row period. The proof explicitly resolves this: the left template has four identical rows, so a six-row translation preserves it. The checker verifies identical rows and verifies that all certificates use the same templates. Thus there is no hidden assumption about the advertised period here.

The middle block translates both vertical strips by four rows. The last block translates the right strip by eight rows and the top by 16 columns. Both preserve the corresponding patterns. At each raw cut, an edge is identified by its band, endpoint depths, and offsets from the cut, so the matching composition glues the correct physical incidences.

The full size step p = 48 preserves both horizontal periods, six and sixteen. The vertical coordinate shifts are multiples of 24, which preserve the side templates. The coordinate table from Section 2 changes each line label by r·48, preserves band depth, and agrees with all four corner translations. The independent exterior-graph comparison confirms the complete geometric identification in every residue.

Straight interior runs remain on constant line labels and only change length. All vertices are either in the translated exterior, the substituted slabs, or those straight subdivisions. There is no unused interior region in which an extra cycle could appear.

## Margins and induction coverage

The cuts are 36, n+36, and 2n+36. Their widths are 12,8,16. At n = 96, the largest right extent relative to its region start is 52, below n-24 = 72; all lower extents exceed 24. These inequalities remain valid as n grows.

Every raw knight edge changes its line label by at most five, less than the smallest block width eight. Thus no edge jumps across a block and bypasses its port description. The blocks are disjoint and lie in pure band-pair regions, outside the corner and side-switch zones. The corner ranges listed in Claim 7 justify the fixed margin.

The 24 base sizes 96,98,...,142 contain one base for each even residue modulo 48. Each is checked as a whole tour. This matters because some corner squares were copied from different source tours: local compatibility alone would not establish a single global cycle. Whole-tour validation supplies the required base fact.

On the next step, the middle and last block starts shift by 48 and 96; the first start stays fixed. The proof's local phase and port checks therefore apply repeatedly. The bases and this insertion step cover every even n >= 96, with no missing residue or size.

## Crossing counts and constants

My independent periodic counter includes all nearby straight continuations. It gives:

| Side | Board period | Crossings per period | Rate |
| --- | --- | --- | --- |
| bottom | 6 columns | 11 | 11/6 |
| top | 16 columns | 37 | 37/16 |
| left | 4 rows | 8 | 2 |
| right | 4 rows | 4 | 1 |

The rates sum to 343/48. The added material has crossing count 8·11 + 3·37 + 12·8 + 12·4 = 343. This conclusion uses the actual periodic geometry, not merely equality of port matchings. Joins keep the same local pattern, corner neighborhoods are translated copies, and straight interior edges do not cross one another.

All 24 independent count differences are exactly 343. For example:

| Base n | X(n) | Extended n | X(n+48) | b[n mod 48] |
| --- | --- | --- | --- | --- |
| 96 | 707 | 144 | 1050 | 21 |
| 110 | 814 | 158 | 1157 | 671/24 |
| 130 | 949 | 178 | 1292 | 481/24 |
| 142 | 1041 | 190 | 1384 | 631/24 |

Every rational b in the document matches the independent count, including the least value 481/24 and greatest value 671/24. The resulting leading coefficient is 343/48 = 7.145833..., now an all-size upper bound for even n >= 96. No global optimality claim is made.

The audit is complete. The next presentation update can replace the proved crossing coefficient 9 in Figure 6 with 343/48 and identify LF4 as the proved family. LF2 remains a separate construction; this proof does not retroactively prove its own all-size formula.

# Claim 9: knight tiles, flux, torus theorem, and gap budget — 2026-10-02

**Verdict: the geometric lemma, flux identities, torus theorem, and global gap bound PASS. The auxiliary bad-triangle statement needs one domain restriction: U must be contained in the board rectangle. With this restriction, Section 6.5 is valid under its stated geometric hypotheses and the intended nonnegative loss constants. No unconditional improvement above coefficient four follows yet.**

## Independent exact geometry

`claim9_tiles.py` imports no worker code. It constructs each tile by its two diagonals, takes the convex hull, and clips pairs of polygons with exact rational arithmetic. It calculates intersection area by the shoelace formula. It also clips each quarter triangle against a tile to verify that each tile consists of exactly four whole quarter triangles. This is independent of the worker's separating-axis and interior-sample tests.

All 1,292 distinct relative edge pairs pass:

| Intersection area | Cases |
| --- | --- |
| 0 | 1,256 |
| 1/4 | 24 |
| 1/2 | 12 |

Positive tile intersection area is equivalent to a strict segment crossing in every case. All 56 tested shared-endpoint cases have area zero. Every tile has area one and covers exactly four quarter triangles. The result is recorded in `claim9_geometry.json`.

The enumeration is exhaustive for distinct planar lattice knight edges. Translate the left endpoint of the first edge to the origin; its positive-x direction is one of four choices. Tile bounds are the bounds of the edge endpoints, with spans at most two. A tile that overlaps the first therefore has its left endpoint within the tested [-4,4] square. All other placements have disjoint interior bounding boxes. There is no missing direction or translated-overlap case.

As elsewhere in this project, a 2-factor means a simple spanning degree-two subgraph. A doubled copy of one edge would not meet this hypothesis or the distinct-edge geometric lemma.

## Flux equations (6.1) and (6.2)

I independently checked 5,184 single-edge flux cases. The tests include horizontal and vertical grid edges, both choices of normal, both lattice colors, and all nearby knight-edge positions and directions. The flux is computed directly from the black-to-white edge orientation and exact proper intersection with the unit dual segment. Tile multiplicities are obtained from the independently clipped quarter triangles. Every case satisfies

```text
phi_H(s) = chi(a) [m_plus + m_minus - 3 g_q].
```

Linearity proves this identity for any finite selected edge set, and locally for a periodic set. The signed-triangle explanation is also sound: the two triangle boundaries reproduce the stated chain and their supports avoid square centers. Thus their net intersection number with the dual segment is zero. Knight edges cannot pass through a square center; the odd/even coordinate components of a knight direction rule that out. The flux has no endpoint ambiguity.

The unit grid graph Q contributes exactly chi(a). Adding that term and reducing modulo three gives (6.2), including the sign -chi(b) under the stated right-side convention. When both adjacent quarter triangles have multiplicity one, m_plus + m_minus + 1 = 3, so omega_H vanishes.

For a closed dual loop in a region where H has degree two, signed divergence of H+Q is (2+4)chi(v) at each enclosed lattice vertex. Its total is zero modulo three. Therefore omega_H integrates to a single-valued mod-three height on a simply connected such region. This remains true when knight edges cross each other. It does not require a reference field or a restriction to two move directions.

## Torus theorem 6.3

The torus proof is correct for a doubly periodic planar lift with no proper crossings and even horizontal and vertical periods. The no-crossing condition must include intersections between translated edges in that lift, as the statement specifies.

The tile lemma gives a packing. A period cell has N vertices and N undirected edge orbits, counted with the usual degree sum. Unit-area tiles therefore have total multiplicity area N per period. Periodicity justifies this area accounting even when tiles cross the chosen period-cell boundary. The cell itself has area N. A packing with that area leaves no uncovered quarter triangle, because any such gap has positive area. Thus every quarter triangle has multiplicity one.

Equation (6.2) gives omega_H = 0 on each unit dual step. On a full period cut, Q's flux cancels by alternation because the corresponding period length is even. The remaining H flux is consequently zero modulo three. Connectedness of the periodic 2-factor is not used.

The stated limitation for open patches is correct: a finite crossing-free patch need not satisfy the period-area equality. This proof does not establish gap-free interiors for arbitrary open patches.

## Global gap inequality (6.3)

This algebra is correct. Every tile is inside the coordinate rectangle [0,n-1]^2. A spanning 2-factor has n² edges, so total tile multiplicity is 4n² quarter triangles. The rectangle has 4(n-1)² quarter triangles, of which G are uncovered. Therefore

```text
sum (m_t-1)_+ = 4n² - [4(n-1)²-G] = 8n-4+G.
```

For each integer multiplicity, (m-1)_+ <= m(m-1)/2. Summing the latter counts common quarter triangles of unordered distinct tile pairs. Each crossing pair has at most two common quarters, and noncrossing pairs have none. Hence

```text
8n-4+G <= 2X,
X >= 4n-2+G/2 = 4n-2+2 A_gap.
```

No connectivity hypothesis is needed. Triple and higher tile overlaps cause no gap in the proof: the binomial count includes all pairs and dominates the multiplicity excess.

As a separate accounting check, `claim9_board_check.py` uses independently recounted tours and accumulates their tile multiplicities. TT16 at n=56 has X=530, G=183, multiplicity excess 627, and pair-overlap count 706. H16a at n=48 has X=437, G=230, excess 610, and pair-overlap count 689. Both satisfy the exact identities and inequalities. These tests are recorded in `claim9_board_results.json`.

## Required repair: the domain of U

The bound on multiply covered triangles in U is valid for any U: each such triangle needs a crossing pair outside B, and each available pair covers at most two common quarters.

The next step, bounding ALL bad triangles in U by

```text
2X-8n+4 + 2[X-|B|],
```

requires U to be a subset of the quarter triangles inside [0,n-1]^2. Only then does the number of uncovered triangles in U have the global bound G. Section 6.4 currently says “any set U” and does not state this restriction.

There is a direct counterexample to that unrestricted auxiliary statement. Use the verified TT16 n=56 tour with X=530. Let B contain all 530 crossing pairs. Let U be 617 distinct quarter triangles outside the board, for example triangle 0 in squares (56+j,0), j=0,...,616. All tile overlaps avoid U and every triangle of U is uncovered. The printed bound gives at most 2·530-8·56+4 = 616 bad triangles, but U has 617. The global gap theorem is unaffected because its G was explicitly defined inside the board.

**Required wording:** restrict U to quarter triangles inside the board rectangle. In Section 6.5, require the charged paths to use the internal dual graph so that both adjacent quarters of each step lie in that rectangle, and require their height changes to be measured in the stated degree-two height domain. Then the intended application has the required domain condition.

## Conditional implications 6.5

With that domain condition, the path-counting argument is correct. Nonzero total height change forces at least one step with nonzero omega_H, hence an adjacent bad triangle. Each quarter triangle has only one unit grid side and is adjacent to only one unit dual edge. Edge-disjoint paths therefore require distinct bad triangles, even if paths meet at vertices. This gives

```text
L <= 4X-8n+4-2|B|.
```

Substituting |B| >= 4n-C gives

```text
X >= 4n + L/4 - 1 - C/2.
```

Thus L = alpha*n-O(1), with alpha positive, would give coefficient 4+alpha/4. The example of four families with n/2-O(1) paths has total L=2n-O(1), and therefore gives coefficient 9/2 under the required hypotheses.

For the loss-tolerant version, put D=2C1+C2 and E=X-4n+2. Combining the first two lower estimates with the path inequality gives the exact algebraic statement

```text
4E >= alpha*n - D*d + 4 - 2C0 - C3.
```

Using d <= K(E+1), for K >= 0 and D >= 0, gives

```text
(4+KD)E >= alpha*n + 4 - 2C0 - C3 - KD.
```

Dividing by the positive denominator and returning to X gives (6.5), including an additive constant independent of n. Thus the displayed coefficient is correct for the intended nonnegative loss constants. The statement should explicitly require K,C1,C2 >= 0 (or at least K >= 0 and D >= 0); without a sign condition on D, the substitution can reverse the inequality. Alpha must be positive to conclude a strict coefficient improvement.

The existence of enough charged paths, the boundary-crossing set B, its overlap exclusion from U, and the loss estimates remain assumptions. The calculation does not establish any of them for arbitrary tours. The document is correct to retain the conditional status of an improvement above 4n.

**Next action:** add the U-domain restriction in Sections 6.4–6.5 and state the nonnegative loss constants. These are narrow statement repairs; the finite geometry, exact flux, all-period torus result, and global gap bound need no change.


# Claim 10: crossings above 4n — 2026-10-02

**Verdict: PASS for closed tours as submitted. PASS for every 2-factor after the explicit certificate replacement below.** The draft has a real scope gap: its strip graph forbids cycles. I supplied and checked a degree-only graph that repairs the gap and retains the claimed coefficient 4+1/7392. The local finite certificates, corner charge, and charging arithmetic pass.

## Scope defect in the submitted proof

The supplied strip graph forbids a cycle. This condition holds for the edges of a single closed tour that touch the first two columns, when n > 4. Such edges lie in the first four columns. A cycle among them would be a whole component of the degree-two tour, which cannot cover the rest of the board.

This condition does not hold for an arbitrary 2-factor. Here is a cycle in the allowed strip geometry:

```text
(0,0), (1,2), (0,4), (2,3), (0,2), (2,1), (0,0).
```

Every edge touches column 0 or 1. `claim10_counterexample.py` completes this cycle to a spanning 2-factor of the 6×6 board with a separate degree-only SAT model. It checks all degrees and saves the edges in `claim10_cycle_counterexample.json`. Disjoint copies of that 6×6 factor give the same obstruction on arbitrarily large boards of size 6k. This is a counterexample to the claimed transfer-graph representation, not to the crossing lower bound itself.

Both supplied graph programs reject the cycle when two incoming edges have the same component label. Thus two matching certificate outputs do not fix this scope error. The submitted proof applies to closed tours; the stronger 2-factor statement requires a graph that permits cycles, or another argument that accounts for them.

## Lemmas 1–4

Lemma 1 is correct. The elementary counter-clockwise dual loop has flux 2 chi(c), and subtracting its four right-cell colours adds 4 chi(c). Their sum is zero modulo three. Antisymmetry cancels internal dual edges when these elementary loops are added. The internal dual grid is simply connected.

The CNF used for Lemmas 2 and 3 is a valid relaxation of a global 2-factor. It includes every knight edge incident to the window, with a two-cell frame for all possible other endpoints. Window degrees are exactly two; frame degrees are at most two. Triple exclusion clauses enforce the upper degree bound, and clauses on each set of k-1 incident variables enforce the lower bound. The clauses forbid exactly the proper crossing pairs, apart from pairs of forced pattern edges in NE-M3. The last clauses exclude each local flux assignment of the claimed residue. Thus UNSAT proves the stated implication. There is no connectivity restriction in these CNFs.

For M3, the unshifted certified block occupies [a-3,a+3] × [b-3,b+3]. The shifted block occupies [a-4,a+2] × [b-3,b+3]. Both lie in the printed 8×7 window. The two horizontal shifts supply both colour classes for each direction. Restricting a global edge set to the window and frame remains feasible even when a frame cell is outside the board: its incident selected edges can simply be absent.

For NE-M3, the window is exactly x = 0,...,j+4 and y = r-6,...,r+7. Its frame ends at rows r-8 and r+9, within the stated pattern hypothesis. All forced or forbidden strip edges therefore agree with that hypothesis. Both patterns, both parities, and all j = 2,...,8 are covered. The checked CNF proves the mod-three claim; the stronger exact-flux sentence attributed to CP-SAT is not needed here.

Lemma 4's reduction to a finite corner check is sound. A column-zero vertex at height 4,...,R-3 contributes -2 chi(0,y), regardless of its two neighbours. Its two edges cross the left segment exactly once and cannot cross the other pieces of Q. The corresponding statement holds on the bottom. The seven remaining corner vertices have arbitrary incident pairs. The enumeration checks their actual degrees after the edge sets are joined, so inconsistent choices of an edge between two corner vertices are excluded.

The programs use pattern edges also in the middle region. This does not impose a missing hypothesis: the preceding fixed-contribution calculation permits that replacement. The enumeration does not constrain degrees at other endpoints of the arbitrary corner choices; this only enlarges the set of cases. Near the far ends of Q, the given pattern supplies every possible contributing edge. Increasing R by two adds two opposite-colour middle contributions per side and translates each end region by a colour-preserving vector. This proves the parity reduction for every R >= 12.

## Stability and charging

For a graph to which the strip restriction belongs, the potential argument is correct. Telescoping gives B_sigma = n + E_sigma + d(end)-d(start). The stated potential range gives the conservative loss 34. Each non-tight step has reduced cost at least one, so its count is at most E_sigma.

Split a walk at its non-tight steps. Each remaining tight subwalk can visit each of the two cyclic strongly connected components at most once. At most three parts of that subwalk avoid the cycle edges, and each has length at most 37. Hence

```text
N_nc <= N_nt + 3·37·(N_nt+1) = 112 N_nt + 111.
```

Each non-cycle step lies in at most three of the tested three-row intervals. Consecutive good rows cannot switch between the disjoint tight cycles. They therefore carry one fixed pattern. This proves the bound 336 E_sigma + 333 for the relevant bad rows. The square tests only use rows at least two from the scan ends, so no undefined three-row interval at an endpoint is used.

The one-defect-per-square step is sound. If the tested rows are good, the whole interval uses one pattern on each side. NE-M3 needs strip endpoints only in rows R-8,...,R+9, within the tested R-10,...,R+11 interval. A crossing pair in B_left that touches a near-left window is therefore a pair of pattern edges, which is an allowed exception. A failure of NE-M3 supplies a pair outside B_left. The window is too far from the other three boundary strips for that pair to be in their B sets. The interior M3 windows are also too far from every boundary strip. For example, the first horizontal interior window begins at column 5; an edge incident to column 0 or 1 ends by column 3. Thus a failed test supplies a pair in I, rather than reusing one of the boundary pairs already charged in the 4n term.

The counting constants are sufficient. A fixed bad row belongs to the interval R-10,...,R+11 for at most 22 radii in each of the two adjacent corner families. This gives 44. For any proper crossing pair, the four endpoints span at most four units in either coordinate. All top-side test windows lie within y = R-6,...,R+7; all right-side windows lie within x = R-6,...,R+7. Each orientation therefore allows at most 14+4 = 18 radii, for a total of 36.

The phrase “squares of different corners are disjoint” should explicitly include window incidence. Here is a sufficient argument for n >= 64. Write n = 2m. For R <= m-9 every bottom-left test window lies within [0,m-2]². The windows of the bottom-right family have x >= m+1, and those of the top-left family have y >= m+1. A single knight edge has coordinate span at most two, so it cannot touch windows from both such families, whose cell-coordinate ranges are separated by three. The same argument applies to the fourth family. A pair that supplies a defect must have both edges touching its window. Thus one crossing pair cannot be charged to two corner families. Mere disjointness of the dual squares alone would not establish this fact, but the printed margins do establish it.

A pair in two B_sigma sets has all its endpoints in one 4×4 corner box. There are only 24 candidate knight edges in such a box. The coarse bound C1 = 4 binomial(24,2) = 1104 therefore suffices. Opposite boundary strips cannot share a pair for the sizes under consideration. This makes the overlap correction independent of n.

There are exactly m-20 tested radii per corner. Odd n admits no spanning knight 2-factor, because the two colour classes have different sizes. Therefore the even-n count covers every nonvacuous case. The inequalities give

```text
2n-80 <= 36 |I| + 44 sum_sigma (336 E_sigma + 333),
14784 (|I| + sum E_sigma) >= 2n - 58688.
```

Combining them with X >= 4n-136-C1+|I|+sum E_sigma gives coefficient 4+2/14784 = 4+1/7392. For the certified graph constants, n >= 64 and additive loss 1244 are conservative explicit choices. The boundary term and interior defects are kept separate, so the extra term is not a second count of the same 4n crossings.

## Relation to Claim 9

Claim 9 supplies the same mod-three height identity as Lemma 1, and its tile-area identity gives the baseline X >= 4n-2 for every 2-factor. The latter does not by itself supply the strip stability estimate: the proof also needs to control the number of bad boundary rows by the excess cost of those rows.

Claim 9's torus theorem cannot replace M3 or NE-M3. A finite open patch has no period-area equality, and can contain uncovered tile quarters. Its gap identity and loss-tolerant charged-path inequality offer another route if all required boundary-pattern and overlap hypotheses are proved. They do not remove the cycle restriction in the supplied strip graph. The local certificates here avoid that additional open-patch argument.

## Repair for all 2-factors: new independent strip certificate

I wrote `claim10_allow_cycles.py` from the degree and geometry definitions. It imports no worker code. A state contains only the next column and the selected edges whose upper endpoints have not yet been processed. It stores no component labels and imposes no condition on cycles. It scans the four columns row by row, requires degree two in columns 0 and 1, and degree at most two in columns 2 and 3. It includes every possible upward knight edge that touches a strip column. Therefore the restriction of any spanning 2-factor gives a walk in this graph.

The transition cost counts crossings of newly selected edges with pending edges. Each crossing is counted exactly when its later lower endpoint is processed. An edge already removed ends on or below the current row and cannot cross a new edge properly. Incoming edges at the current vertex share that endpoint with the new edges and also cannot cross them properly. Thus the walk cost equals B_sigma, including when a cycle closes.

The exact exhaustive check gives:

| Quantity | New graph, cycles allowed |
|---|---:|
| Reachable states | 12,544 |
| Arcs | 25,536 |
| Potential range | [-1/4, 31] |
| Minimum positive reduced cost | 1 |
| Tight cyclic components | Two simple 4-cycles |
| Longest tight path after removal of cycle edges | 27 |

The code constructs the pending-edge states of P and P' directly and checks that these are exactly the two tight cyclic components. It also maps every step of the 6×6 counterexample's left strip into the new graph, including its closed cycle, and checks that the walk cost equals its 29 crossing pairs. The full graph search checks every reduced cost, the absence of a negative cycle, the cyclic components, and the remaining directed acyclic graph. Results are in `claim10_allow_cycles.json` and `claim10_allow_cycles.log`.

These constants satisfy all the weaker bounds used in the draft: potential range width at most 34, minimum positive reduced cost at least one, only P/P' tight cycles, and T* <= 37. Therefore substituting this graph repairs the theorem for every 2-factor without changing 1/7392 or any charging constant. It is a concrete certificate replacement, not an assumption that cycles are harmless.

The proof text must remove the forest requirement in Section 6 and replace the graph description and C7 certificate. Keep the old graph only as an additional check for tours. The new T* = 27 also gives bad rows <= 246 E_sigma + 243; the same algebra would improve the small coefficient to 1/5412. The Claim 10 verdict uses only the requested weaker coefficient.

## Certificate runs and reproducibility

I copied the seven supplied certificate sources to `w-verifier/claim10_runner/`; their hashes are in `source_sha256.json`. I did not change the source files in `w-lowerbounds/`, and I did not run CP-SAT.

- C1: regenerated all four M3 CNFs and Glucose4 proofs. All four are UNSAT and pass the standalone DRUP checker. Their checked proof-addition counts are 938, 594, 633, and 508.
- C2: all four wrong-residue M3 controls are SAT. The checker rejects an empty proof for the first M3 instance. The source has no implemented `sanity` command, so `run_checks.py` performs these controls directly.
- C3: regenerated all 28 NE-M3 CNFs and proofs. All are UNSAT and pass the standalone DRUP checker. An empty proof file can be valid when the original clauses already yield a unit-propagation contradiction; the checker performs that test.
- C4: the two wrong-residue NE-M3 controls, one for each pattern, are SAT.
- C5 and C6: all 16 primary corner cases (four pattern pairs, R = 12,...,15) give Q = 1 modulo three. All eight separate exact-rational cases (four pattern pairs, R = 12,13) inspect 2916 corner choices and give the same result. The primary program also completed unchanged. To reduce repeated arithmetic, `run_corners_cached.py` runs both enumerations with a cache of each program's own additive edge contributions: Q(E) = Q(empty) + sum_e [Q({e})-Q(empty)]. This preserves the complete enumeration and each program's geometric routine. `corner_results.json` records the 24 passing cases.
- C7: both supplied forest-graph implementations reproduce 82,516 states, 144,674 arcs, potential range [-1/4,135/4], minimum positive reduced cost one, two simple 4-cycles, and T* = 37. Those figures are correct for their forest model. The separate degree-only certificate above supplies the missing 2-factor case.

`claim10_runner/all_checks.log` contains the DRUP and SAT controls; the two strip logs contain their original graph results. The independent repair runs with `.venv/bin/python w-verifier/claim10_allow_cycles.py` from the repository root.

**Required action before publication:** replace the forest graph with the cycle-permitting graph in Section 6 and C7, and include the explicit window-separation argument above. With that repair, the requested theorem is verified. The source draft as submitted should not be labelled a complete proof for all 2-factors.


**Run-status note:** A redundant, unchanged `corner_charge2.py` run launched by `w-verifier/claim10_runner/run_checks.py` continued after its tool session returned an interrupted status. The complete cached rational enumeration has already passed all eight cases. The Chief Researcher can stop this redundant process (only the one with working directory `w-verifier/claim10_runner/`), or let its fixed eight-case loop finish. Its progress is in `claim10_runner/corner_charge2.py.log`. The audit does not depend on this extra run.


## Claim 10 scope closure — 2026-10-02

Per the Chief Researcher, the accepted Claim 10 result is the closed-tour theorem. The separate cycle-permitting graph recorded above is not part of that frozen draft or the Claim 11 argument. No further M3 or NE-M3 work was done. The redundant unchanged corner rerun has now finished: all eight exact-rational cases passed, and no Claim 10 check remains running.

# Claim 11: unconditional crossing lower bound for closed tours — 2026-10-02

**Verdict: PASS, for Hamiltonian cycles on every even n >= 32.** The tile and charged-path argument proves the stated bound X >= (4+1/338)n-1240. The sharp strip certificate improves it to X >= (4+1/17)n-1009. I found no gap in the endpoint charge, the path count, the exclusion of boundary tile overlaps, or the scope of the strip graph.

There are two small text repairs. In `TILE_INPUTS.md` Section 3, the displayed expansion gives 5E+5659, not 5E+5679. The latter is a weaker upper bound and is safe; change its equality to an inequality, or use 5659. Section 6.4 of `w-turnstheory/FINDINGS.md` still says “any set U” for the bad-triangle estimate. It must restrict U to the board rectangle. Section 7's actual U meets that condition, so this uncorrected general statement does not create a gap in Claim 11.

## Scope and the strip model

For n >= 32, the edges incident to columns 0 or 1 lie in the first four columns and form a proper subset of a Hamiltonian cycle. Such a subset cannot contain a cycle. This justifies the forest restriction in the transfer graph. It does not justify a claim about all 2-factors, and I make no such extension here.

The four-column scan has exactly 4n steps. Every edge with a lower endpoint at the current cell is selected at that step. Edges remain pending until their upper endpoints are processed. A pair of proper crossing edges is charged when its later lower endpoint is processed. An edge removed at an earlier row cannot cross a newly selected edge; edges ending at the current vertex share that endpoint and do not cross properly. Thus the walk weight is exactly X_sigma, the number of crossing pairs among edges incident to the two boundary columns.

My new `claim11_forest.py` builds this graph from the degree and geometry definitions. It uses my own transitions and exact intersection predicate; it imports no worker code. It returns 82,516 states and 144,674 arcs. The ordinary quarter-unit potential is in [-1,135], the tight graph has exactly two simple four-cycles, and deleting their eight arcs leaves a directed acyclic graph with longest path 37.

I checked that these critical states give exactly P and P' in all four column phases. I also checked that the stated crossing pair is pending at phase zero. Thus one good row, defined by its four critical transitions, fixes all incident edges at both strip vertices. It does not need the three-row definition from Claim 10. Consecutive good rows use the same pattern because their walks meet at the same state and the two critical cycles are disjoint.

## Original stability and the 1/338 coefficient

Let S be the sum of the four reduced-cost totals. Telescoping gives

```text
X_sigma >= n-34+E_sigma.
```

A tight subwalk visits each of the two cyclic components at most once after leaving it. Its non-cycle arcs split into at most three paths of length at most 37. Splitting a general walk at its m positive-cost arcs gives at most 112m+111 non-cycle arcs. Each positive cost is at least one, and each bad row contains at least one non-cycle arc. Hence

```text
d_sigma <= 112 E_sigma+111.
```

A pair counted in two strip crossing counts lies in a 4×4 corner square. Such a square has 24 candidate edges, so four times binomial(24,2) = 1104 bounds the total duplication. Opposite strips cannot share a pair. It follows that

```text
sum X_sigma <= X+1104,
S <= X-4n+1240,
d <= 112S+444.
```

With E=X-4n+2 this is d <= 112E+139100. There is no assumption that X_sigma or E_sigma is the same as the selected boundary set B below.

The remaining geometric argument gives 2n <= 4E+6d+152. Therefore

```text
2n <= 676E+834752,
X >= (4+1/338)n - 209026/169.
```

The exact additive loss is about 1236.840. Both the printed intermediate loss 1237 and the headline loss 1240 are valid.

## The selected boundary pairs and their tile overlaps

For P, row y supplies the pair (0,y-2)-(1,y) and (0,y-1)-(2,y). For P', it supplies (0,y+1)-(1,y-1) and (0,y)-(2,y-1). Both are proper crossings. The phase-zero pending state contains both edges, so a good row guarantees that they belong to the actual tour.

Within one pattern, a vertical translation changes the pair. Between the patterns, the edge with horizontal displacement one has the opposite slope. Thus different good rows cannot give the same pair, even across pattern changes. With y restricted to 6,...,n-7, the pair's endpoints are far enough from adjacent sides that their selected pairs cannot coincide. Each side offers n-12 rows, and removal of all bad rows loses at most d pairs in total. This proves

```text
|B| >= 4n-48-d.
```

The edge with horizontal displacement one has its whole tile in 0 <= x <= 1. Hence that pair's tile intersection also lies in this first unit strip. Reflection and transposition give the same statement for the other sides. The proof excludes entire tile intersections from U, as needed; exclusion of crossing points alone would not suffice.

## Four-row corner charge

I checked the supplied endpoint checker and wrote `claim11_corner.py` independently. My version uses four long directed segments for Q_R and exact integer intersection tests, rather than importing the worker's unit-step calculation.

Let c_e be the signed flux contribution of an edge to Q_R, and let M consist of the middle boundary vertices (0,y) and (y,0), for 4 <= y <= R-2. Define

```text
r_e = c_e + sum_{v in e intersect M} chi(v).
```

Because every vertex of M has degree two,

```text
sum_selected c_e = sum_selected r_e - 2 sum_{v in M} chi(v).
```

This is a linear identity; it does not assume a boundary pattern in the middle of the arcs. The grid-colour contribution to omega_H is then added separately.

Every nonzero residual coefficient belongs to an edge incident to either one of the seven corner vertices K or to a strip vertex in the four endpoint rows R-1,...,R+2. All other coefficients cancel. Candidate coverage is complete: an edge meeting either long boundary segment touches column zero or row zero, and an edge meeting one of the two short endpoint segments has an endpoint in column zero or one, or row zero or one. The knight's coordinate span is at most two. Edges farther from these sets cannot contribute. The bounded candidate range in the checker contains every such edge.

The endpoint coefficients are fixed by the two given patterns. No edge there meets K for R >= 12. At K the code enumerates every choice of two neighbours per vertex, joins the edge sets, and checks the resulting degrees. Exactly 2916 choices remain. In all four pattern combinations, the complete charge is 1 modulo three.

I tested R=12,...,31 and R=100,101, with all four pattern combinations and all 2916 corner choices at each radius. I also compared the residual coefficients after translation of the endpoint terms, and checked the constant term. The normalized data are identical within each parity class. The general parity argument is valid: the middle degree contributions add two opposite-colour vertices per side when R increases by two; the corner terms stay fixed; all remaining endpoint terms translate by a colour-preserving vector. The endpoint and corner regions are disjoint for R >= 12. This proves the reduction to R=12 and R=13 for all larger radii, rather than treating large-radius samples as a proof.

The mod-three height is single-valued on the internal dual grid, so the total around L_R is zero. The complementary right/top path gamma_R consequently has charge -1 modulo three. Reflections can change the sign or the colour convention, but preserve a nonzero charge. The argument uses the actual tour at the corner; it needs no reference tour or fold model.

## Path count, bad-row charges, and the domain of U

Write n=2m. At each corner R ranges from 12 through m-4, inclusive, so there are m-15 paths and 2n-60 paths in all. At n=32 this is one path per corner. Every larger n has the stated number as well.

Within a corner, gamma_R consists of a vertical arm at x=R+1/2 and a horizontal arm at y=R+1/2, both ending at coordinate 3/2. Different radii give disjoint arms: the outer vertical arm is beyond the end of the inner horizontal arm, and the outer horizontal arm is above the inner vertical arm. Between corners, the paths lie in disjoint boxes separated by a positive gap. Thus they are edge-disjoint, in fact vertex-disjoint.

A bad row y spoils only radii with R-1 <= y <= R+2, at most four choices. On one side the endpoint-row intervals from its two corners lie in [11,m-2] and [m+1,n-12]. They are disjoint. Therefore a bad row spoils at most four paths overall, not eight. Deleting all spoiled paths gives

```text
L >= 2n-60-4d.
```

Four consecutive good rows have one pattern, so every retained path satisfies the endpoint-charge lemma. Negative lower estimates for L cause no problem: the actual number L is nonnegative and still satisfies the inequality.

Take U to be exactly the quarter triangles adjacent to the unit dual edges of the retained paths. Every such triangle is inside the board rectangle. More strongly, all of its coordinates lie strictly beyond the first unit boundary strip on every side: for a bottom-left path, its smallest possible coordinate is 3/2 and its largest is R+1; reflection gives the other corners. Thus U lies in (1,n-2) squared. No pair in B has a tile intersection there.

This explicitly supplies the U-domain restriction missing from the general wording of Section 6.4. All paths also lie in the internal dual graph, where the height is defined. No sign issue arises in the loss constants: all constants used here are nonnegative.

My geometry check constructs every candidate path at n=32,48,64,72,96. It checks distinct dual edges, distinct adjacent quarter triangles, their board locations, the maximum of four path charges per bad row, and the exclusion of every possible selected boundary pair of both patterns. At n=96 it checks 132 paths, 7128 dual edges, 14256 adjacent quarter triangles, and 672 distinct candidate boundary pairs. These are additional finite checks of the geometric argument.

## Tile budget and the absence of double counting

A 2-factor has n² tiles of area one. For multiplicities m_t in the board rectangle and G uncovered quarter triangles, the exact count is

```text
sum_t (m_t-1)_+ = 8n-4+G.
```

Each crossing pair contributes at most two common quarters, and no noncrossing pair contributes one. Hence G <= 2X-8n+4 and E=X-4n+2 >= 0. This step does not need connectivity.

Inside U, every multiply covered triangle belongs to a crossing pair outside B. There are at most 2(X-|B|) such triangles. Thus U has at most

```text
G+2(X-|B|) <= 4X-8n+4-2|B|
```

bad triangles. A nonzero path charge forces a nonzero unit-step charge. If both adjacent triangles had multiplicity one, the exact local flux identity would make that step's charge zero. Each retained path therefore needs a bad triangle. A quarter triangle has one unit grid side and is adjacent to one unit dual edge; edge-disjoint paths require distinct such triangles. This proves

```text
L <= 4X-8n+4-2|B| <= 4E+92+2d.
```

Combining this upper bound with the path lower bound gives 2n <= 4E+6d+152. Boundary pairs have been excluded from the local multiple-coverage budget before this count. Uncovered triangles use the separate global area budget. There is no unsupported charge of a path to a nearby crossing, and no second use of a boundary crossing as an interior overlapping pair.

## Sharp stability and the 1/17 coefficient

On each graph arc define the integer cost

```text
C(u,v) = 20w-5-4[arc is not one of the eight critical arcs].
```

The exact Bellman-Ford certificate from a virtual source gives h in [-149,0] with C(u,v)+h(u)-h(v) >= 0 on every arc. Telescoping any walk gives total C >= -149. For a strip walk of 4n steps, this is precisely

```text
X_sigma-n >= N_nc(sigma)/5 - 149/20.
```

Every bad row contains a noncritical step. Summing the four sides and using the crossing-duplication bound gives

```text
d <= 5(sum X_sigma-4n) + 149
  <= 5(X+1104-4n) + 149
   = 5E+5659
  <= 5E+5679.
```

Thus the Chief Researcher's arithmetic is correct. The draft's larger constant is safe but must not be presented as the exact expansion.

Using the printed safe constant gives

```text
2n <= 4E+6d+152 <= 34E+34226,
X >= (4+1/17)n - 17147/17
  >= (4+1/17)n - 1009.
```

Using 5659 instead gives exact additive loss 17087/17, so loss 1006 would also be safe. The requested headline with loss 1009 is valid without that tightening.

My separate forest implementation checks the sharp potential on every arc and again obtains [-149,0]. It also extracts a reachable 12-step closed walk with total crossing weight 5 and exactly 10 noncritical steps. Therefore

```text
(total w - steps/4) / N_nc = (5-12/4)/10 = 1/5.
```

Repeating this reachable cycle shows that no larger coefficient can hold with a fixed additive constant for all walks in this transfer graph. At alpha=201/1000 its scaled cost is -40 in units of 1/4000. This proves exact sharpness. Testing only 201/1000 would bound the optimum above by 201/1000; it would not by itself prove the word “sharp”. The saved witness removes that small justification gap. I mapped the witness back to the original `strip_dp.py` states and checked all twelve arcs, costs, and critical-arc flags there too. The sharpness statement concerns the transfer-graph stability estimate, not optimality of the final tour bound.

## Reproduction and finite results

All new work used one CPU core, with one computation at a time and no solver. The old redundant Claim 10 corner run finished before these checks started. No M3 or NE-M3 certificate was rerun.

The copied supplied checkers and logs are in `w-verifier/claim11_runner/`:

- `check_knight_tiles.py`: PASS, 1292 tile pairs and 648 single-edge flux cases.
- `check_corner_endpoint_charge.py`: PASS, R=12,13,14,15, all four endpoint pattern pairs and 2916 corner choices.
- `check_strip_row_certificate.py`: PASS, all stated graph constants, one-row patterns, and pending crossing pairs.
- The exact alpha=1/5 computation from `alpha_star.py`: PASS, potential [-149,0].
- The separate `strip2_independent.py` alpha check: PASS, the same potential.
- `check_sharp_witness.py`: PASS on the original graph, exact ratio 1/5 and negative weight at 201/1000. This direct finite witness replaces the much longer repeated negative-cycle relaxation at 201/1000; no binary search is needed.

My own code and results are `claim11_forest.py` / `claim11_forest.json` and `claim11_corner.py` / `claim11_corner.json`. I also reran my independent Claim 9 rational-polygon checker: 1292 tile pairs, including 24 overlaps of area 1/4 and 12 of area 1/2, and 5184 signed flux checks all pass. The scripts import only my previous verifier code and standard or installed general-purpose libraries, not worker construction code.

**Next action:** correct the equality in `TILE_INPUTS.md` Section 3, add the internal-board restriction to the general statement in Section 6.4, and cite the exact sharpness witness. These changes clarify the text; the closed-tour bound X >= (4+1/17)n-1009 is verified.

## Claim 11 cross-reference: Edge Searcher's C++ checks — 2026-10-02

I read the C++ certificate report in `w-searcher/FINDINGS.md` and inspected its virtual-source initialization in `w-searcher/cert/strip2.cpp`. The reported graph size, sharp potential, row patterns, corner charges, and 12-step negative cycle agree with my independent results. Its negative weight -10 uses units of 1/1000; my -40 uses units of 1/4000. These are the same value.

I also reran my own forest graph with only the ordinary potential's source changed. A virtual source gives ordinary potential range [-10,0] in quarter units and T*=23. The original start-state source gives [-1,135] and T*=37. Both give the same two critical cycles, and both recover the sharp stability potential [-149,0] in twentieth units. Thus the different longest-path values are not a mismatch: the set of tight acyclic arcs depends on the chosen potential. The 1/17 proof uses the sharp stability certificate and does not use T*.

The new check is `claim11_virtual_potential.py`, with results in `claim11_virtual_potential.json` and `.log`. The original Claim 11 certificate files are unchanged. The verdict remains PASS for closed tours.


# Claim 12 (preparation): FOLD24 tours and the all-size proof requirements — 2026-10-02

**Verdict: finite evidence PASS. The all-size theorem is pending its proof.** All 36 FOLD24 files are single closed knight tours and have the stored crossing and turn counts. For every even residue modulo 24, both checked extensions add exactly 152 crossings and 304 turns. The largest exact crossing offset is 142. These checks establish the numerical claim for every even n from 96 through 166; they do not establish induction for arbitrary k.

## Independent checks

`claim12_prep.py` imports only my existing independent checker. It decodes the board.js moves, checks every move is on the board, checks two distinct reciprocal knight edges at every cell, and follows the cycle from one cell. The cycle must return to that cell after exactly n² distinct visits. It then counts turns and all proper intersections of open edge segments with exact integer predicates. Spatial bins only select candidate pairs; each candidate receives the exact intersection test.

All stored n, crossing counts, and turn counts agree. The four FOLD24 certificate copies at n=96,98,100,102 also pass and have exactly the same grids as their main tour files. File hashes and individual results are in `claim12_prep_results.json`; the run log is `claim12_prep.log`. No construction code or solver was imported or run.

The three entries in each count column below are for n0, n0+24, n0+48. The offset b is X-19n/3, calculated as an exact fraction.

| Base n0 | n mod 24 | Crossings | Turns | b |
|---:|---:|---|---|---:|
| 96 | 0 | 720, 872, 1024 | 1251, 1555, 1859 | 112 |
| 98 | 2 | 752, 904, 1056 | 1265, 1569, 1873 | 394/3 |
| 100 | 4 | 775, 927, 1079 | 1319, 1623, 1927 | 425/3 |
| 102 | 6 | 754, 906, 1058 | 1310, 1614, 1918 | 108 |
| 104 | 8 | 776, 928, 1080 | 1352, 1656, 1960 | 352/3 |
| 106 | 10 | 786, 938, 1090 | 1383, 1687, 1991 | 344/3 |
| 108 | 12 | 788, 940, 1092 | 1386, 1690, 1994 | 104 |
| 110 | 14 | 803, 955, 1107 | 1402, 1706, 2010 | 319/3 |
| 112 | 16 | 839, 991, 1143 | 1459, 1763, 2067 | 389/3 |
| 114 | 18 | 864, 1016, 1168 | 1500, 1804, 2108 | 142 |
| 116 | 20 | 850, 1002, 1154 | 1507, 1811, 2115 | 346/3 |
| 118 | 22 | 875, 1027, 1179 | 1529, 1833, 2137 | 383/3 |

Thus every tested tour satisfies X <= 19n/3+142. The maximum offset occurs at residue 18. The repeated turn increment is additional finite evidence; I make no all-size turn claim here.

I also checked the saved base data independently in `claim12_base_data.py`. All twelve bases use p=6, lo=8, band=1, rad=4. Each stores 72 corridor template entries: four corridors, six longitudinal phases, and three transverse offsets. Every stored template move agrees with the corresponding base-tour move at every middle cell, not just in the extracted sample period. Every copied-component move also agrees with its base tour, and the saved component cells are disjoint from each other and from the middle cells.

All twelve bases have the same multiset of normalized component shapes: four components of size 60, four of size 63, four of size 78, and one of size 204. This is 13 components and 1008 cells. There are nine distinct shapes, with multiplicities 1,1,1,1,1,2,2,2,2. Thus shape equality alone does not identify every component. The number of middle cells in these bases is 6n-264, so the total represented free-cell set has size 6n+744. These are checked properties of the saved bases; uniformity at larger sizes still needs proof. Results are in `claim12_base_data.json`.

## What the construction does

I read `w-integrator/fold_period.py`, `fold_assemble.py`, `w-lowerbounds/fold_board.py`, and `w-structures/fold3.py`, plus the `paste.py` and `repair.py` routines that define the field and free regions. I also read the FOLD findings and `w-integrator/runs/fold24.txt`.

The field splits the square into four quadrants and splits each quadrant along a diagonal. In the local bottom-left frame, with offset t=1, a cell chooses direction (2,1) above y=x+1 and direction (-1,-2) otherwise. The other quadrants rotate this rule. The undirected union of the on-board chosen edges is the initial field; it is not yet assumed to be degree two or connected.

`fold3.build` adds boundary U-turns at degree-one cells. The arch interval h-floor(n/4) <= y < h, where h=n/2, reverses the usual U-turn direction. The insertion has degree guards and a fixed scan order, so its exact output, including exceptions near interval ends, matters to a proof.

For FOLD24 the call uses an empty `tgs` dictionary. Thus the separate diagonal templates loaded by `paste_field` are not inserted. The solver's free set consists of radius-four boxes around linked degree-defect clusters, together with four diagonal corridors. Defect clustering uses Chebyshev distance at most four. In a corridor's local frame its cells satisfy 0 <= x < h and y-x in {0,1,2}.

The saved periodic middle is 11 <= x < h-11 in those same three diagonal rows. The code inserts a six-period table there. On increasing n by 24, each middle gains twelve longitudinal cells, or two periods. The remainder of the free set is split into components using eight-neighbour cell adjacency. These are geometric components of the free-cell set, not components of the knight graph.

Each such component stores moves relative to its minimum-coordinate offset. On a larger board the code matches equal shapes greedily, choosing the unused base component with the closest normalized offset, and copies its moves by translation. Fixed-cell moves come from the rebuilt field. This procedure produces no new solver completion for the larger sizes. The final validation detects a failure at a particular tested n; it does not prove that no failure can occur later.

## Facts the all-size proof must establish

1. **Exact domain and size changes.** Fix the twelve base data files and all parameters. For n=n0+24k, give formulas for the field regions, U-turn intervals, defect clusters, corridor cells, and copied-component offsets. The size change moves h by 12 and floor(n/4) by 6. A coordinate-shift table must cover all these motions, including the rotations and the centre. It must apply from n0 onward, not only after some larger threshold.

2. **The fixed field and all free components are accounted for.** Prove that all degree defects are within the stated free set, that the relevant defect clusters remain separated, and that free-set components retain their shapes for every k. Prove the number and size of copied regions stay bounded. The 13-component, 1008-cell inventory above is the finite base evidence. A component must not grow with n or split, merge, disappear, or acquire a new interface. The reported raw-field crossing count 5n also needs an exact all-size count if it is used in the slope proof.

3. **Component identities and phases are preserved.** Four pairs of saved components have the same shape. Prove that the normalized-distance rule assigns each to the intended base component for all k, including ties and iteration order, or replace that rule in the mathematical construction with explicit geometric labels and offsets. Equal shape does not by itself prove equal surrounding field phase or equal port connections. A ranking observed at k=0,1,2 is not a proof that the normalized-distance ranking never changes.

4. **Every local edge is consistent.** Prove on-board knight moves, degree two, and reciprocity at every cell after all replacements. This includes corridor-to-field, corridor-to-endpoint, copied-region-to-field, and any edges between distinct free components. Eight-neighbour separation of cell components does not by itself exclude knight edges between them. The solver ties constrain free-free corridor edges; the proof must also cover all other incident edges of the saved periodic moves. Any overlap of region definitions needs a consistent assignment.

5. **The complete graph is one cycle for every k.** Give an exact path or port description for the field, each periodic corridor, and each copied piece. Include paths that return to the same cut and rule out closed components wholly inside a piece. Prove that insertion of two six-period blocks per corridor preserves the relevant exterior connections, or give an equivalent inductive graph isomorphism. All vertices of the new board must occur in the described paths. Matching visible endpoints alone does not rule out extra internal cycles. A local period of six does not, by itself, imply that the global matching has period 24 in n.

6. **Crossing changes are local and exhaustively counted.** Show that the inserted material and the coordinate shifts preserve all old crossing pairs except the explicitly counted local changes. Count the new proper intersections, including those across every seam and those involving field edges outside a corridor. Specify a unique counting rule so a pair is neither lost nor counted twice. The claimed decomposition is 120 extra field crossings plus 32 from four corridors, for a total of 152 per +24. This needs a proof of the *net* corridor change after old edges are replaced; simply adding corridor crossings to the original field count is not enough. Bounded copied regions give a constant contribution only after their local surroundings and separation from other regions are proved stable.

7. **Close the induction and the uniform bound.** Use one valid base in each even residue class and the proven extension to cover every even n>=96. The finite offsets in the table then give X(n)=19n/3+b[n mod 24] and max b=142. State that the base search is used only to provide the fixed finite certificates; the extension must not require a new successful optimization, a larger repair window, or a changed gadget at some later n.

These are proof requirements, not counterexamples to the design. The finite data are consistent with the claimed theorem. The preparation verdict remains finite PASS until the extension and connectivity argument is supplied in `w-integrator/PROOF_fold.md`.


# Claim 13: per-row stability and the 4+1/8 crossing bound — 2026-10-02

**Verdict: PASS for closed knight tours on every even n >= 32.** The augmented graph proves the required per-row estimate, and the complete chain gives

```text
X >= (4+1/8)n-856.
```

I also found an exact sharpness witness. The optimal per-row coefficient for this strip-graph inequality is exactly 1/2, not just close to 1/2 at the search resolution. There is no new gap in the boundary or charged-path inputs from Claim 11.

## Independent augmented graph

`claim13_rows.py` rebuilds the forest strip graph using my own `claim11_forest.py` transition routine. It imports no worker code. The ordinary graph again has 82,516 states, 144,674 arcs, and the same eight critical arcs of the two P/P' cycles.

Let c(s) be the column to be processed next, and let f record whether an earlier transition in the current row was noncritical. For an ordinary arc s -> t, define

```text
a = 1 if the arc is not one of the eight critical arcs, else 0,
g = max(f,a).
```

If c(s) is 0, 1, or 2, the augmented transition keeps g as the new flag and charges zero bad rows. If c(s)=3, the transition charges g and resets the next flag to zero. The next state is then at column zero.

This tests membership in the two critical cycles, not merely zero reduced cost. A zero-cost arc outside those cycles makes its row bad, as required. The current arc enters the logical OR before the end-of-row charge, so a noncritical fourth arc is not lost. A row with several noncritical arcs is charged only once.

Starting with the empty strip state and flag zero, this rule charges exactly one for each row whose four arcs are not all critical. All four critical arcs of a good row must be on one cycle, because the critical cycles are disjoint and the walk is continuous. This is exactly the good/bad row definition used for the selected boundary crossings in Section 7.2 and the four endpoint rows in Sections 7.3–7.4. No three-row margin or change to the meaning of d is introduced.

The full doubled graph has 165,032 states and 289,348 arcs. Exactly 82,521 augmented states are reachable from the empty state with flag zero. The full graph includes flag assignments that are not reachable; proving a potential on that larger graph is safe. The exact sharpness witness below uses reachable states.

## Potential certificate and row bound

For an augmented arc with crossing weight w and bad-row charge b, use integer cost

```text
C = 8w-2-4b.
```

My exact Bellman-Ford computation from a virtual source gives an integer potential h in [-46,0]. The checker verifies C+h(s)-h(t) >= 0 on every augmented arc, not only convergence of the relaxation loop. Thus, for any augmented walk,

```text
sum C >= h(end)-h(start) >= -46.
```

A complete strip scan has 4n transitions, crossing weight X_sigma, and exactly d_sigma bad-row charges. Therefore

```text
8X_sigma-8n-4d_sigma >= -46,
X_sigma >= n+d_sigma/2-46/8.
```

There is no unfinished row in the tour application. For clarity, a general prefix should count completed rows under the charge rule. I also checked that h(s)-4f has minimum -46 on the reachable augmented states. This supplies the same constant if a prefix from the empty state counts its unfinished row as bad whenever its flag is set.

Both supplied implementations agree with the independent computation. `beta_cert.py` converges with range [-46,0], and `strip2_independent.py`'s `row_check(1,2)` converges after eleven in-place passes with the same range. All arithmetic in the verification is integral.

## Exact sharpness witness

The independent checker finds a closed walk in the zero-reduced-cost graph of the new certificate with:

```text
16 transitions = 4 complete rows,
6 crossings,
4 bad rows.
```

It rotates this walk to start at column zero with flag zero, and checks every row directly against the eight ordinary critical arcs. All four rows are bad. Hence

```text
[sum w - transitions/4] / bad rows
    = (6-16/4)/4
    = 1/2.
```

The walk is reachable from the ordinary empty start through the augmented graph. Repeating it makes any coefficient beta>1/2 fail for every fixed additive constant. Together with the potential certificate, this proves that beta*=1/2 exactly for the transfer-graph stability problem.

For example, at beta=501/1000 this cycle has total cost -16 in units of 1/4000. `claim13_runner/check_witness.py` maps its states back to the original `strip_dp.py` graph and verifies all sixteen original arcs, crossing weights, critical-arc flags, row-end charges, and flag resets. That separate check passes.

The capped binary search alone does not certify an upper endpoint: failure to converge before its cap need not mean a negative cycle. The exact witness removes that limitation and makes the approximate interval unnecessary. This sharpness statement is about the strip relaxation; it does not claim that the final coefficient 4+1/8 is optimal for tours.

## Constants and the complete bound

The Claim 11 overlap count gives sum X_sigma <= X+1104. With the exact loss 46/8 on each of the four sides, summing the row estimate gives

```text
d <= 2(sum X_sigma-4n)+46
  <= 2(X+1104-4n)+46
   = 2E+2250,                    E=X-4n+2.
```

Thus the Chief Researcher's tighter arithmetic is correct. The source's 2252 is also correct: it first rounds 46/8=5.75 up to 6 per side. That gives

```text
d <= 2(X+1104-4n+24)
   = 2E+2252.
```

Unlike the earlier alpha calculation, this displayed equality does not need an erratum; the two-unit difference is an explicit rounding loss.

All geometric inputs from Claim 11 still apply to this same d:

```text
|B| >= 4n-48-d,
L >= 2n-60-4d,
L <= 4X-8n+4-2|B| <= 4E+92+2d.
```

Here B contains one distinct crossing pair for each retained good boundary row. Its tile intersections lie in the unit boundary strips. The paths are edge-disjoint, each bad row can remove at most four paths, and all their adjacent quarter triangles U lie inside the board and beyond those strips. Thus the repaired U-domain condition is respected. The use of a per-row flag changes none of those facts.

Combining the last two inequalities and the safe row bound yields

```text
2n <= 4E+6d+152
   <= 16E+13664,
E >= n/8-854,
X = 4n-2+E >= (4+1/8)n-856.
```

With the exact 2250 one instead gets additive loss 3421/4 = 855.25. The requested integer loss 856 remains valid. The only connectivity assumption is the established forest restriction for a proper boundary strip of a Hamiltonian cycle. This audit does not extend the theorem to arbitrary 2-factors.

## Reproduction and status

The original sources were copied to `w-verifier/claim13_runner/`. `run_all.py` runs the two supplied positive certificates and my independent augmented-graph check sequentially, with one CPU core. The exact negative-cycle witness replaces the capped search; no solver or long search was run.

- `claim13_rows.py`, `claim13_rows.json`, and `claim13_rows.log`: independent graph, potential, reachable-state count, and complete exact witness.
- `claim13_runner/beta_primary.log`: supplied beta certificate, PASS.
- `claim13_runner/beta_separate.log`: separate supplied pure-Python row certificate, PASS.
- `claim13_runner/check_witness.py` and `witness.log`: the exact witness checked against the original graph, PASS.

All checks have finished. **Next action:** cite the saved sixteen-step witness and replace the search-resolution statement with the exact value beta*=1/2. The closed-tour bound X >= (4+1/8)n-856 is verified as stated.


# Claim 12: FOLD tours for all even n >= 96 — 2026-10-02

**Verdict: PASS.** The explicit placement rules, reduced-graph insertion argument, complete port matchings, and two-state outside check establish a closed knight tour with X <= 19n/3+142 for every even n >= 96. The state of the full block matching has period 48 in n. A +24 step switches between two states, each of which closes into one tour. This corrects the period-24 matching claim in the earlier preparation; it does not change the crossing increment or the family of board sizes.

I audited `w-turnstheory/PROOF_fold.md` and ran its standalone checker. I also wrote `claim12_full.py`, which imports only my own exact geometry code and general Python libraries. It independently rebuilds the field and the saved pieces, extracts all block and outside paths, composes the complete matchings, counts crossings, and tests the explicit reduced-graph transport.

## Placement and finite reconstruction

The new placement is a definition, not the earlier nearest-normalized-position heuristic. The thirteen component records have fixed geometric identities in their saved order. Their translations per +24 are exactly the table in Section 1. In particular, an end of an arch interval moves by 6 in its edge coordinate; a side midpoint moves by 12; and the centre moves by (12,12). Physical corners move with the board corners. The opposite arch endpoints move by 18 after the change in the board extent is included.

My assembler uses direct direction formulas in the four quadrants, forms the undirected field, adds U-turns in the stated rotation/row order, and then applies the corridor and component moves. For all twelve bases it reproduces the grids at k=0,1,2 exactly. Thus it also checks the previously saved component ordering. Every resulting edge is a legal reciprocal knight edge, every vertex has degree two, and the graph is one cycle.

As a larger check, I rebuilt k=8 for all twelve bases, giving n=288,290,...,310. All twelve are single tours, with X=X0+1216 and T=T0+2432. These checks cover 48 independently reconstructed full tours in total. They support the proof but are not used as a substitute for induction.

## The all-size geometric step

The line-label argument in Section 2 is sufficient when applied to the full retained set: boundary depths zero and one, all corridor cells, and all thirteen saved components. My transport test uses exactly that set.

Away from this set, a field path lies in a constant-direction triangle, or in the two triangles joined at one axis fold. It cannot cross a diagonal fold without meeting the retained band. The band has three transverse cell positions, while a knight move changes y-x by at most three. The finite patches cover the ends of the bands and the central junction. Each of the remaining triangular regions has only one axis-fold boundary. After a path crosses that fold, monotonicity through the fold prevents a return. Thus a suppressed piece has at most one fold and cannot close internally.

A straight (2,1) arm has label 2y-x; a straight (-1,-2) arm has label 2x-y. For the left chevron, the common label is 2y-x below the midline and 2(n-y)-x above it. An edge across the midline preserves that label. The integer line label, with its implied parity, fixes the lattice strand. Once its endpoint ports and these data are fixed, increasing its length cannot change its connection.

The growing blocks remain in the same geometric types for every k. If h0=n0/2, their upper cuts are

```text
corner: 30+12k = h-(h0-30) <= h-18,
side:   h+22+12k = n-(h0-22) <= n-26.
```

For a corner, max(2x-y,2y-x) >= max(x,y), so the block remains away from both quadrant axes. A left-side block starts at label h+16, which implies x <= h-16 and places its arms away from the diagonal corridor. Its fold lies away from both the boundary U-turns and the centre patch. The rotated statements are the same. These margins prevent a primitive block from entering a different triangle, a finite patch, or another block as n grows.

Outside the blocks, the five surviving boundary intervals shift in edge coordinate by 0,6k,12k,18k,24k. Their depths stay fixed. Before the corner block a diagonal piece is fixed; after it the piece translates by (12k,12k). These are compatible with all finite-component translations. The relevant separations from fixed-size patches are either constant in k or increase; the base margins therefore remain valid. The new explicit identities remove the duplicate-shape assignment issue found in preparation.

As an additional all-k check, `claim12_affine_margins.py` represents every copied cell coordinate and every cut as an exact pair (constant, coefficient of k). It checks the quadrant and label branches, board bounds, and all active component-to-block inequalities. In total, 36,288 affine margin inequalities pass across the twelve bases. Their slopes point away from the forbidden regions or keep the margin constant. Thus this check establishes that all 1008 copied cells stay on the board and outside every growing block for every k>=0; it does not infer that fact from sampled sizes. Results are in `claim12_affine_margins.json`.

The label changes at the ends agree:

- A corner arm's boundary endpoint shifts by 6k along the edge, and its corridor endpoint by (12k,12k). Both change its line label by 12k.
- An outer chevron's lower endpoint shifts by 6k and its upper endpoint by 18k, while n grows by 24k. Both ends change the common chevron label by 12k.
- The inner chevron endpoints shift by 12k along the boundary. Both common labels change by 24k.

Unshifted pieces keep their labels. All increments preserve parity, and the corridor shifts preserve its six-period move table. The same calculation applies to component ports using the explicit anchors. Thus all connections outside the eight blocks are preserved. The additional field vertices lie on these longer monotone arms or on the new block arms; they are not unaccounted components. This addresses the quadratic growth of the triangle interiors.

Inside a growing corner block, increasing its label by six advances the corridor phase by six and the boundary positions by three. Its straight-arm incidence is unchanged. Inside a side block, increasing the label by six advances the lower boundary arm by three and the upper arm by minus three, with the fold determined by the same common label. The boundary patterns are constant on these intervals. Therefore suppression gives 1+2k copies of the primitive block, not a new unclassified geometry at larger k.

I checked this geometric map at the level of the *whole reduced outside graph*, rather than only its terminal matching. For each base and k=1,2,8, the independent code maps every retained outside vertex by the stated boundary, corridor, or component rule. It checks that overlapping rules agree, that the map is a bijection onto the larger retained outside set, and that the multiset of all suppressed outside edges and labelled cut edges is preserved. Every outside vertex is traced. All 36 such transport tests pass. The general argument is the line-label calculation above; the transport tests check its implementation and all finite port cases.

## Ports, returns, and composition

My extractor identifies the full set of vertices in each label interval. A port is an actual selected edge leaving that set. I independently orient its endpoints by increasing label and recover the tag, depths, and offsets from the cut. Both cuts have the same ordered name list in each phase. All ports have distinct names on a cut.

I then find every connected component inside the block and require exactly two external ports. This checks all cells, including components with no visible port, rather than tracing only known strands. The resulting complete matchings are exactly:

```text
corner, four ports: Li-Ri for i=0,1,2,3;
corner, six ports: L0-R5, L1-R1, L2-L5, L3-R3, L4-R4, R0-R2;
side, four ports:  L0-R1, L1-R2, L2-R3, L3-R0.
```

There are two six-port name lists. They differ at diagonal port 4, whose offsets are (-3,0) or (-1,2), with depths (1,2). I retain those lists separately. Their common abstract matching is not used to erase a physical phase difference. A translation by six labels reproduces the full port list and matching in each case.

The four-port corner is the identity. For the six-port corner, the internal right return of one copy joins the left return of the next into the continued L0-R5 path. The other through paths and the outer returns persist. Every internal port belongs to one of these paths. Thus composition produces M again and no closed component: M is idempotent. The independent composition routine checks all internal nodes and rejects components with no outer port.

The side matching is rho=[1,2,3,0]. It contains only through paths, so its layered composition cannot create a hidden internal cycle. Its order is four. The power after growth is rho^(1+2k): rho for even k and rho^3 for odd k.

The outside extractor also visits every outside vertex and requires two ports per component. Its matching is unchanged in the reconstructions and in the geometric transport. For every base, joining this outside matching to all corner blocks and either side state gives exactly one cycle. The port graph has degree two, and the path-coverage checks account for every full-board vertex. This proves one-cycle connectivity for every k, including both parity states.

The corrected matching period is therefore 48. A +24 step is a valid extension because both alternating states work, not because it preserves the matching.

## Crossing locality and the exact increment

The claim that pure fields and free folds have no proper crossings has a direct geometric justification. At an axis fold, use the integer normal coordinate perpendicular to the axis. At a diagonal fold, use y-x in its local frame. Each relevant directed field edge changes this coordinate by one unit in the same direction on both sides. Within one open unit slab, all edges are parallel; edges from different slabs have disjoint interiors in that normal coordinate. They can meet on a slab boundary only at endpoints. Thus a free fold creates no proper crossing. Junctions and modified boundary/corridor cells are already in the retained regions or fixed patches.

Every remaining crossing is local to two length-sqrt(5) segments. The inserted boundary patterns repeat after six labels, and the corridor moves repeat after (6,6). The exterior pieces and finite-patch neighbourhoods retain their moves and relative cut margins. Consequently the join neighbourhoods are preserved, while each new primitive block contributes one repeated local crossing interval. Counting by the least endpoint label includes pairs that straddle a cut and assigns each such pair once. The disjoint blocks and their margins prevent a pair from receiving two block assignments.

The supplied and independent integer counters agree on the local counts, including enlarged intervals:

| Primitive block | Boundary | Corridor | Total |
|---|---:|---:|---:|
| Corner | 6 | 4 | 10 |
| Side | 9 | 0 | 9 |

The independent check verifies the expected counts for widths 6,18,30,102 at all twelve bases. It also verifies that the full crossing count minus the eight block counts is unchanged under transport. There are 76 crossings in the eight primitive blocks, and 76(1+2k) in their enlarged versions. Hence

```text
X(n0+24k) = X(n0)+152k,
152 = 4·2·10 + 4·2·9 = 120 boundary + 32 corridor crossings.
```

This is a net replacement count, including the seams. It does not assume that corridor crossings may simply be added to an unmodified field count. In particular, the proof does not need the earlier separate claim that the raw field has exactly 5n crossings.

The twelve base counts and exact offsets are independently recorded in Claim 12 preparation. Their largest offset X(n0)-19n0/3 is 142, attained for n0=114. Each even n>=96 has a unique representation n0+24k with one of these bases. The increment formula therefore proves the claimed uniform bound.

## Step-12 failures

I independently rebuilt the same completions at n0+12. They are legal degree-two graphs, but some are not connected. These graphs use the specified earlier base completion; they are not the separate saved FOLD24 tour having the same board size.

| Base n0 | Reused size n0+12 | Number of cycles |
|---:|---:|---:|
| 96 | 108 | 1 |
| 98 | 110 | 1 |
| 100 | 112 | 3 |
| 102 | 114 | 2 |
| 104 | 116 | 1 |
| 106 | 118 | 2 |
| 108 | 120 | 1 |
| 110 | 122 | 1 |
| 112 | 124 | 3 |
| 114 | 126 | 2 |
| 116 | 128 | 1 |
| 118 | 130 | 2 |

For the two examples in the proof, base 100 at n=112 has cycles of sizes 678,706,11160; base 102 at n=114 has cycles of sizes 1704,11292. I also checked that the step-12 outside matching is the same and its block matchings are the second powers. The finite matching graph gives exactly the same number of cycles as each full reconstruction. These are concrete counterexamples to unrestricted step-12 reuse.

## Files and completed checks

The supplied standalone checker was copied to `claim12_supplied.py` and run without a solver. It passes all its checks and writes `fold_proof_checks.json` in the verifier directory. Its output is `claim12_supplied.log`.

The independent code is `claim12_full.py`; its complete counts, port lists, component counts, large-size checks, and step-12 results are in `claim12_full_results.json`. The output is `claim12_full.log`. Both jobs ran sequentially on one CPU core and have finished.

**Conclusion:** the placement, geometric insertion, two matching states, and local crossing count establish the all-size FOLD theorem. No unresolved assumption from the preparation remains. Keep the period-48 matching correction explicit when presenting the result.

# Claim 14 — all boundary pairs and run stability (2026-10-02)

**Correction from Claim 15 (2026-10-02):** my one-pair corner argument below is wrong. I omitted the two edges incident to the corner vertex. There are four edges common to adjacent side classes and five possible crossing pairs. FOLD24 at n=96 has two shared pairs at each corner. Use |B| >= 4n-24, not the claimed 4n-8 from that argument. The historical Claim 14 proof and its advertised additive constant 537 are superseded. The run certificate, exact 2/7 witness, and quarter-overlap check remain valid. Claim 15 supplies a correct stronger asymptotic bound with full-square charges. Its sharpened constant, together with X>=4n-2 for small n, also recovers the requested Claim 14 bound; see the explicit comparison there. The code corner check is corrected, and the JSON boundary section is updated. The initial lines of claim14.log record the superseded run.

**Verdict: PASS for closed Hamiltonian tours, for every even n >= 32.**
The stated bound is valid:

```text
X >= (4 + 4/15)n - 540.
```

I checked section 7 of `w-lowerbounds/TILE_INPUTS.md`. The proof uses the tile identity and corner lemma audited in Claims 9 and 11. It does not need the intermediate constant 2/15 in section 6. The new finite inputs pass independent checks. The constant 2/7 is exactly sharp for the strip-walk inequality. Two proof sentences need more precise wording, as specified below; neither changes the theorem.

## Boundary crossings, including bad rows

Theorem 9 in the paper gives n-O(1) per side. It does **not**, by itself, supply the precise constant n-1. For that constant, use the width-one forest certificate F1 explicitly.

I wrote the width-one transition rules independently, using integer proper-intersection tests. Column 0 has degree two. Columns 1 and 2 have degree at most two. Every retained edge meets column 0. Component labels exclude closed components. The graph has 330 states and 580 arcs. With cost 3w-1 per transition, the shortest-path potential from the empty state has minimum -3. Every reduced arc cost is nonnegative. A walk of 3n transitions therefore has crossing weight at least n-1.

A closed tour restricted to these edges is a proper subset of a Hamiltonian cycle, so it is a forest. The scan starts with no pending edges. Thus the certificate applies to every side of the tour. It uses no good-row condition. The word “unconditionally” in section 7(a) is valid within the stated closed-tour scope; this check does not assert the same forest argument for arbitrary 2-factors.

Let B_sigma contain all proper crossing pairs whose two edges meet the outermost column of side sigma. Opposite sides cannot share such a pair for n>=32. At the bottom-left corner, an edge common to the left and bottom classes must join the two coordinate axes. Only two knight edges can do this:

```text
(0,1)-(2,0),  (0,2)-(1,0).
```

They give exactly one possible pair. The same statement holds at each corner. No pair belongs to three sides. Consequently

```text
|B| = |union B_sigma| >= 4(n-1)-4 = 4n-8.
```

This counts pairs of edges, not intersection locations. Distinct pairs at the same location remain distinct crossings.

## Tile overlaps and the domain of U

My exact polygon and quarter-triangle code checks the 115 crossing pairs formed by column-zero edges with source rows -6 through 6. It finds no violation. This is a complete local check up to vertical translation: a proper crossing can only use source rows at distance at most three, and all four outward knight moves occur in the list.

The independent check proves a stronger fact than the supplied test:

* every overlap quarter lies in a square with horizontal index 0 or 1;
* in a square with horizontal index 1, the only possible overlap quarter is the **left** quarter.

An edge with horizontal displacement one stays in the first unit strip. For a pair to overlap beyond x=1, both edges must have horizontal displacement two. Proper crossing then forces opposite slopes and source rows differing by one. Their overlap in the second square is its left quarter. This also gives a direct proof of the finite result.

That left quarter is adjacent to the horizontal dual step from x=1/2 to x=3/2. It is not adjacent to a step wholly in x>=3/2. Thus the pair overlaps avoid every quarter used by the charged paths. Reflections and transposition prove the same statement for all four sides.

**Text repair:** the statement that a single tile avoids the right quarter does not alone imply exclusion from every quarter adjacent to an arbitrary dual step in x>=3/2. Use the stronger fact about the overlap of a crossing pair above. Alternatively, refer only to the specified corner paths, whose steps near this boundary are horizontal. The conclusion used by the proof is correct.

I also rebuilt all candidate corner paths for n=32,48,64,96,120. I checked every possible column-zero crossing pair on all four sides against the actual quarter set U. All checks pass. Every quarter in U is inside the board; its square indices are between 1 and n-3. Each quarter belongs to one dual step, and no two candidate paths share a step. This respects the inside-board domain required by the repair in Claim 9.

The tile-budget inequality therefore gives, with E=X-4n+2,

```text
L <= 4X-8n+4-2|B| <= 4E+12.
```

The boundary-pair saving and the charges in U are disjoint. There is no second charge to the same overlap in this subtraction.

## A run of k bad rows loses at most k+3 paths

Put m=n/2. On one side, write each four-row endpoint window as [s,s+3]. The starts used by its two corners are

```text
s in [11,m-5] and s in [m+1,n-15].
```

These are disjoint sets of integers. A bad run [a,b], of length k=b-a+1, meets a window only if s belongs to [a-3,b]. That interval has k+3 integers. Therefore the run removes at most k+3 candidate paths on this side, even if it spans the middle. There is no extra cost of three at the second corner. Summing this upper bound over runs and sides is safe; repeated removal of one path only makes the upper bound larger.

Let Q be the sum of k+3 over the bad runs on all sides. The number of retained charged paths satisfies

```text
L >= 2n-60-Q.
```

Every retained endpoint window consists of four consecutive good rows. These rows use one common critical pattern, so the earlier corner-charge lemma applies. I also tested every single bad interval on each of the five board sizes above. The maximum overhead is at most three in every case.

**Text repair:** the added allowance of 12 in section 7 is safe but unnecessary. The interval argument already covers a run that reaches both corner ranges.

## Independent run graph and exact sharpness

The base graph has 82,516 states and 144,674 arcs. I rebuilt it with my own forest transitions. Its two critical cycles contain eight arcs. A row is bad exactly when at least one of its four arcs is outside those cycles. This is the same definition used by the corner proof.

The augmented state is (base state, current row dirty, previous row bad). At the last transition of a row, set b to its dirty flag, charge

```text
loss = b + 3b(1-previous_bad),
```

reset the dirty flag, and set previous_bad=b. Start both flags at zero. Thus each bad row costs one, and each run start costs three. Over a complete board scan, the total charge is exactly the sum of k+3, including the first and last runs.

The augmented graph has 330,064 states and 578,696 arcs; 82,569 states are reachable from the empty start. My exact integer potential h has range [-167,0] and satisfies, on every arc,

```text
7(4w-1)-8loss + h(source)-h(target) >= 0.
```

Summation gives

```text
X_sigma-n >= (2/7)Q_sigma - 167/28.
```

I found a reachable closed walk with 20 transitions, total crossing weight 7, and cyclic bad-row pattern 1,0,1,1,1. Around the cycle, this is one run of four bad rows, so its loss is 7. Its exact ratio is

```text
(7-20/4)/7 = 2/7.
```

Repeating this reachable cycle proves sharpness, since an initial path adds only a fixed cost. At 1431/5000 its integer weight, scaled by 20000, is -68. This is an explicit negative-cycle witness, not a failure to converge within a search limit. The full states and edge weights are saved in `claim14.json`. I mapped the witness back to the supplied strip graph and checked every transition, flag update, crossing weight, and run charge there. It passes.

I also reran the supplied positive test at 2/7: potential range [-167,0]. Its separate pure-Python implementation converges after 12 passes with the same range. I used the exact witness in place of the long capped negative-cycle search. The supplied overlap program reports 115 pairs and zero violations.

## Full chain and constant

The four width-two strip counts still satisfy sum X_sigma <= X+1104. This is the earlier corner-duplication bound; replacing B does not change it. The new run certificate gives

```text
Q <= (7/2)(sum X_sigma - 4n + 4*167/28)
  <= (7/2)(X+1104-4n+167/7)
   = (7/2)E + 7881/2.

2n <= 4E+72+Q
   <= (15/2)E + 8025/2.
```

In particular, the draft's weaker constant 4034 is safe. Its displayed conclusion E >= (4/15)n-538, and hence X >= (4+4/15)n-540, follows. With the exact arithmetic above and no unused middle allowance, this same argument gives the slightly stronger additive constant 537. The requested theorem therefore passes with room in its constant.

The proof remains a closed-tour proof. The strip graph excludes internal cycles, and no claim for general 2-factors follows from this audit. There is no hidden good-row assumption in B, no duplicate corner pair beyond the four allowed deductions, and no overlap between B's tile saving and the charged-quarter count.

## Reproduction files

Independent code: `w-verifier/claim14.py`. Run it from the project root with `.venv/bin/python -u w-verifier/claim14.py`. Results: `claim14.json`; output: `claim14.log`.

Copied supplied checks and the original-graph witness test are in `w-verifier/claim14_runner/`. Their completed logs are `primary.log`, `separate.log`, and `overlaps.log`. All jobs ran sequentially, with one CPU core and no solver.

# Claim 15 — full-square charges (2026-10-02)

**Verdict: PASS.** For every closed Hamiltonian tour on an even n by n board, n>=32,

```text
X >= (4+4/11)n - 736.
```

I checked Sections 9.1, 9.2, and 9.6 of `w-turnstheory/FINDINGS.md`. The square lemma, vertex separation, endpoint exclusion, corrected boundary-pair count, and final arithmetic are valid. The supplied two new checkers pass. My independent code imports only earlier verifier code, not worker or `kt/` code.

## Every square configuration

For a unit square, exactly eight possible knight tiles cover any of its quarter triangles. I found these edges by exact polygon clipping. I tested all 256 subsets of the eight edges, with no degree or connectivity restriction. These give 65 distinct multiplicity vectors. The numbers of subsets with 0, 2, 3, and 4 bad quarters are respectively 8, 80, 64, and 104. No subset has exactly one bad quarter.

I also checked 196 translated single tiles in the four unoriented knight directions. Every tile visits two squares and covers two adjacent quarters in each square. Thus each single tile contributes zero to

```text
m0-m1+m2-m3.
```

Addition proves this identity for every selected edge set. The all-one vector also has alternating sum zero. Changing exactly one coordinate cannot preserve it. This proves Section 9.1 for all square configurations, including gaps, double coverage, and higher multiplicities. The finite enumeration independently confirms the complete local case list.

## Two bad quarters per charged path

A path with nonzero total height change has at least one step with nonzero change. The flux identity implies that one adjacent quarter has multiplicity different from one. Its square is centred at an endpoint of the step, hence at a vertex of the path. The whole square has at least two bad quarters by Section 9.1.

Vertex-disjoint paths give different squares. Their quarter interiors are disjoint, even if their squares share a side. Therefore the L paths give at least 2L distinct bad quarters. For U equal to their whole squares, the previous gap budget and the exclusion of B give

```text
2L <= bad quarters in U
   <= (2X-8n+4) + 2(X-|B|).
```

This is Section 9.2. It uses the global gap bound once and the multiplicity bound once. It does not count a gap a second time as a multiply covered quarter.

## Vertex-disjointness for all sizes

Represent a dual vertex by the lower-left integer corner (x,y) of its square. At the bottom-left corner, gamma_R uses

```text
{(R,y): 1<=y<=R} union {(x,R): 1<=x<=R}.
```

Every vertex has max(x,y)=R. Distinct radii therefore share no vertex. All these squares have indices at most m-4, where m=n/2. Reflection at the opposite side maps an index x to n-2-x, so the opposite corner indices start at m+2. The corner boxes are separated. All square indices lie between 1 and n-3, so all four quarters of every square lie inside the board. The repaired domain condition from Claim 9 is respected.

There are 4(m-15)=2n-60 candidate paths. My independent checks at n=32,34,48,56,96,120,256 find exactly this number, with no repeated square centre. This finite check supports the coordinate argument; the proof for all sizes is the coordinate argument itself.

## Full-square boundary exclusion

The earlier quarter-only exclusion is not sufficient after U grows to whole squares. I independently enumerate all 20 normalized proper crossing configurations of two column-zero edges. Only two orientations of one pair can have tile overlap in a square with horizontal index 1:

```text
e=(0,j)-(2,j+1), f=(0,j+1)-(2,j).
```

Their common quarter there is the left quarter. All other overlaps have horizontal square index zero. No overlap reaches an index of two or more. Boundary source rows at distance at least four cannot cross in their open interiors, so the normalized enumeration is complete.

For gamma_R, the only square with horizontal index 1 is its endpoint square (1,R). Its possible exceptional pair uses source rows R and R+1. These rows belong to the four good rows required to retain the path. Consecutive good rows use the same critical pattern. In that pattern, both moves from column zero to column two have the same vertical sign. The exceptional pair requires opposite signs, so it cannot occur.

The argument works for each endpoint after reflection or transposition. Other vertex squares lie farther inside. It applies to **all** boundary crossing pairs, including pairs incident to bad rows elsewhere. Thus B avoids the whole U for the retained paths. No further discarded radius is needed for this exclusion.

Section 9.2's earlier discussion uses the older selected good-row boundary set. When using all column-zero pairs, the additional endpoint argument of Section 9.6 is necessary. The complete proof supplies it.

## Corrected corner overlap and my Claim 14 error

The common edge set of two adjacent side classes includes the edges at the corner vertex. At the bottom-left corner it consists of

```text
a=(0,0)-(1,2), b=(0,0)-(2,1),
c=(0,1)-(2,0), d=(0,2)-(1,0).
```

I independently enumerate these four edges and their five proper crossing pairs: ac, ad, bc, bd, cd. The pair ab only shares an endpoint and does not count. Opposite sides cannot share an edge for n>=32. Hence

```text
|B| >= 4(n-1)-4*5 = 4n-24.
```

The unchanged width-one forest certificate supplies n-1 per side. My Claim 14 reconstruction and the new supplied checker both verify its 330 states, 580 arcs, and potential minimum -3 in units 1/3.

I validated and recounted the saved FOLD24 tour at n=96: X=720, T=1251. Its four boundary side sets have 131,130,137,129 pairs. Each corner has two shared pairs, and their union has 519 pairs. This is a concrete counterexample to my earlier at-most-one argument. My Claim 14 audit was wrong on that point. I added a correction at the start of that report and corrected its code and JSON boundary section. Its original proof of the constants 540 and 537 is superseded; the new proof below is separate.

## Stability, path loss, and the final chain

The run graph and the meaning of a bad row are unchanged from Claim 14. I compared the current four source files with the copies used in that audit; they are byte-for-byte identical. The independent potential [-167,0], the two supplied positive checks, and the exact reachable 2/7 witness therefore remain applicable. No new strip certificate is assumed.

Let Rsum be the sum of k+3 over all bad runs on the four sides. With E=X-4n+2 and sum X_sigma<=X+1104, the checked stability inequality gives

```text
Rsum <= (7/2)(X+1104-4n+167/7)
     = (7/2)E + 7881/2.
```

The corrected boundary count and the full-square lemma give

```text
2L <= 4X-8n+4-2(4n-24) = 4E+44.
```

Section 9.6 safely allows an extra loss of 12 and uses L>=2n-72-Rsum. Therefore

```text
4n <= 4E+188+2Rsum <= 11E+8069,
X >= (4+4/11)n - 8091/11
  >= (4+4/11)n - 736.
```

All signs and constants in this chain are correct. The strip restriction to forests remains valid because the tour is Hamiltonian. This does not prove the result for arbitrary 2-factors.

The extra loss of 12 is unnecessary: on each side the four-row window starts form two disjoint sets of integers. A run [a,b] meets a window only if its start is in [a-3,b], which has k+3 integers. This covers a run spanning both corner ranges. Using L>=2n-60-Rsum gives the stronger, optional constant

```text
X >= (4+4/11)n - 8067/11.
```

This also recovers the requested Claim 14 inequality, despite its faulty original corner argument. For n<=2000, X>=4n-2 implies X>=(4+4/15)n-540. For n>=2000, the last displayed stronger Claim 15 bound implies it: their difference is (16n-31905)/165, which is positive there. This recovery relies on the new full-square theorem, not on the old Claim 14 proof. I withdraw the old advertised constant 537 from that proof.

## Files and checks

Independent code: `w-verifier/claim15.py`. Exact results: `claim15.json`; output: `claim15.log`. Run from the project root with `.venv/bin/python -u w-verifier/claim15.py`.

The supplied checkers `check_square_defects.py` and `check_col0_squares.py` both pass. Their output is in `claim15_supplied_square.log` and `claim15_supplied_col0.log`. The former also checks a seam example outside this claim's scope; this audit does not use that example. The new source checks and all independent work ran sequentially on one CPU core, without a solver.

# Claim 16 — turns write-up and hand count (2026-10-02)

**Verdict: PASS for the hand count, both finite certificates, Theorem 1, and Corollary 2.** The printed move rules agree with TT16. There is one false descriptive sentence about the right-side pattern and two small wording issues. These do not change the explicit construction or the theorems. Details follow.

## Hand count from the printed rules and corner files

I independently transcribed the move-code table and bottom template from `writeup/turns/main.tex`. I tested turns by collinearity or opposite vectors, rather than importing the write-up's turn function.

The bottom template has turns at every cell of row 0, at columns 0,2,5,7 of row 1, at columns 0,3,5,6 of row 2, and nowhere in row 3. Its column counts are exactly

```text
c = (3,1,2,2,1,3,2,2),
c[k] + c[(1-k) mod 8] = 4 for all k.
```

All four corner files have phases [0,1,0,0], identical bottom and top templates, and Z=6. Thus the top entry is the negation of bottom entry (1-x) mod 8, as printed. Negation preserves turns. Each column x=6,...,n-7 therefore gives exactly four turns across the bottom and top bands. This identity holds column by column, so there is no incomplete-period correction.

The printed side codes are also correct: left 23,27; right 46,06, ordered from the boundary inward. Each cell in these two columns turns. Hence each row y=6,...,n-7 gives four turns across the two sides.

I checked every one of the 144 cells in each residue's corner data. The counts are the same for all four residues:

| n mod 8 | BL | BR | TL | TR | Total |
|---:|---:|---:|---:|---:|---:|
| 0 | 21 | 21 | 20 | 20 | 82 |
| 2 | 21 | 21 | 20 | 20 | 82 |
| 4 | 21 | 21 | 20 | 20 | 82 |
| 6 | 21 | 21 | 20 | 20 | 82 |

The generated corner tables are byte-for-byte identical to the tables included by the current write-up. The corner cells and the two counted band sets are disjoint. Every remaining cell has code 26 and is straight. In particular, the unused parts of the six-cell margins add no turns. Therefore the hand sum is exact:

```text
T = 82 + 4(n-12) + 4(n-12) = 8n-14.
```

**Text correction:** “This is the left pattern turned by 180 degrees” is false for the listed right-side pattern. Rotating left codes 23,27 gives 67,36, not 46,06. The actual right file uses 02,24 before negation, which produces the printed 46,06. Keep the explicit moves and delete that sentence.

## Printed corner certificate

I ran `writeup/turns/check_corner.py`: PASS, 209 cases, sum alpha=-7, and an equality case at every cell.

I separately entered the alpha and beta tables as printed and enumerated all unordered pairs of distinct legal knight moves at the 16 corner cells. All 209 inequalities hold. The slack histogram is:

```text
slack 0: 65 cases; 1: 77; 2: 48; 3: 17; 4: 2.
```

Every corner cell has a zero-slack case. The nine beta edges lie wholly within the corner. Their signed contributions cancel when the local inequalities are summed, because each selected edge is used symmetrically at its endpoints. The sum of alpha is -7. These facts prove the corner inequality for every 2-factor; no connectivity assumption is used.

The enumeration is complete for n>=8: an endpoint at distance at most three from each corner side can reach at most coordinate five, so the opposite board sides impose no further move restriction. The local side contributions sum to exactly 2n for each side. Outside the four disjoint corner squares there is at most one side contribution. Thus the printed argument gives T>=8n-28, in agreement with the earlier turns audit.

## New TT16 script and independent comparison

I ran the full `tt16.py` script in a verifier copy. Only the project/output paths were changed, and a graph export was added. This avoids overwriting the other worker's figures and tables. Its original construction, checks, counts, and figure code all ran. It reports one closed tour and T=8n-14 for every even n=48,...,102, with 82 corner turns each time.

My separate program reconstructs each graph directly from the printed rules and the four corner JSON files. It imports no worker construction code. It agrees at every cell with all 28 exported graphs. My existing independent board checker confirms in-bounds reciprocal knight moves, degree two, one cycle through all n squared cells, and the exact turn count. It also recounts crossings; these extra measurements are in `claim16.json`. I separately check the four-turn band sums, 82 corner turns, and absence of other turns on every board.

**Checker detail:** the supplied `counts()` asserts T=8n-14, but it only prints the corner count. It does not assert `zone == 82`, although Appendix C3 says that it checks the 82 corner turns. My checker asserts it and it passes. Add that assertion to make C3's description exact.

## Theorem and corollary statements

Theorem 1(a), for n>=8, agrees with the audited lower bound and correctly includes all 2-factors. Theorem 1(b), for every even n>=48, agrees with the TT16 construction and the all-size block-insertion proof audited in Claims 6 and 7. The finite range 48,...,102 includes the four induction bases 96,98,100,102. The period-eight extension covers the remaining sizes. The turn-count lemma alone does not prove connectivity; the write-up correctly treats connectivity separately.

The paper's final open-question section states the literal conjecture that the minimum number of turns is at least 8n. A tour with 8n-14 turns refutes it at each even n>=48. The combined interval is

```text
8n-28 <= T_min(n) <= 8n-14.
```

Thus |T_min(n)-8n|<=28 is valid. The interval contains 15 possible integer values and has endpoint difference 14, as the write-up states. The construction does not establish T_min(n)=8n-14, and the write-up does not claim that equality.

Two small wording corrections:

* The abstract says “exactly two turns per row or column at each side.” The horizontal count varies by column; two is its period average. Use “an average of two turns per row or column at each side,” or refer to four turns in the combined opposite bands.
* Specify that T_min(n)/n tends to 8 **through even n**. T_min is defined here only for board sizes with closed tours.

The write-up's audit-status sentence saying its new text and two scripts are unreviewed can now refer to this audit, after the listed corrections. I did not rerun the Lean build in this small task and make no new claim about its formal status.

## Files

Independent code: `w-verifier/claim16.py`. Results and output: `claim16.json`, `claim16.log`. Supplied corner-check output: `claim16_corner.log`. The isolated full script run, its 28 exported graphs, figures, tables, and `tt16.log` are in `claim16_runner/`. All checks ran sequentially on one CPU core. No worker files were changed.

# Claim 16 addendum — blog and figure audit (2026-10-02)

**Verdict: mathematical bounds and figure numbers PASS; text corrections are required before publication.** I read `writeup/turns/post.mdx`, its figure script, the relevant paper text, the search record, `PROOFS.md`, and the saved independent results. I did not edit the draft or its source figures. The exact replacements below are proposed factual corrections for the author to apply.

## Requested checks

1. **Bases and margins:** the statements about direct checks at every even n=48,...,102 and induction bases 96,98,100,102 are correct. The n0=56,58,60,62 values in the corner files identify the sizes where those fixed corner data were saved. They are not the bases at which the block-insertion proof's separation margins start. `PROOFS.md` explicitly uses n>=96, margin 24, and the four bases 96,...,102. Claim 7 checks this argument. The blog must retain the n>=96 qualification and must describe equality of reduced graphs, not literal equality of boards.
2. **Sharp corner loss:** I independently reread and checked all 16 cells of `corner_witness.txt`. The residual sum is exactly -7; internal edges are reciprocal; all moves are legal; and the internal components have sizes 3,3,3,3,1,1,1,1, with no internal cycle. This proves sharpness of the local corner inequality with outgoing edges left free. It does not prove that a full tour attains the global lower bound.
3. **Independent rebuild range:** I checked the actual `tt16_results.json` entries. They contain exactly the 44 even sizes 48,...,134 and the four sizes 312,314,316,318. All turn counts are 8n-14. The current corner-file hashes still match that audit. The blog's large-size range needs “even” or an explicit list, because 313,315,317 were neither tested nor possible closed-tour sizes.
4. **Four-column argument:** the count is valid. If z,a,b cells in columns 1,2 have respectively zero, one, or two outward edges, then a+2b=2n+B and z+a+b=2n, so b=B+z>=B. In column 3, at most B cells have a back edge. If B>n, the lower bound n-B is negative but remains valid; cancellation still works. The four-strip overlap argument assumes n>=8. The corner residual argument is the same valid argument checked in Claim 16.
5. **Figures:** I ran the entire `blog_figs.py` in an isolated verifier copy, using the already checked TT16 builder. It produced all eight PNG files. The tour, bands, counts, and growth figure use the same graphs independently checked in Claim 16. I viewed the count, growth, and lemma images. The count figure uses columns 8,...,23, outside the corners. The bottom numbers are (3,1,2,2,1,3,2,2) repeated twice; the top numbers are (1,3,2,2,3,1,2,2) repeated twice. Every sum is four. The growth titles are n=48:370 turns and n=56:434 turns. The strip diagram uses n=16, width four, and four 4-by-4 overlaps. The lemma image is copied from `explain/turns_lemma.png`; its numeric argument is correct. Its multiple solid arrows show alternative moves, not a tour cell of degree four; a caption should say so.

The Lean statement is consistent with the recorded formal audit and current project README. I did not rerun Lean in this addendum. The four-column and corner proofs, all new numeric statements, and the claimed independent rebuild record have direct evidence above. I found no source in the checked material assigning the 21-turn optimization specifically to Parker; the paper attributes it collectively and already allows temporary breaks in formation and unrestricted final configurations. The replacement below removes the unsupported personal attribution. The sentence about what Nil's earlier blog post said is autobiographical and is not certified by this audit; the mathematical bounds in that sentence match the paper.

## Required exact replacements

These are replacements, not edits already applied. Each quoted original is from the current draft.

### 1. State the size range

Replace the front-matter excerpt with:

> For every even n >= 48, the minimum number of turns in a closed knight's tour lies between 8n - 28 and 8n - 14. Our old conjecture of at least 8n was wrong, but only by a constant.

Replace:

> It is also true, up to a constant: every closed tour has at least `8n - 28` turns.

with:

> It is also true up to a constant: for `n >= 8`, every closed tour has at least `8n - 28` turns.

Replace:

> So the minimum number of turns is `8n`, give or take 28.

with:

> For every even `n >= 48`, the minimum is between 14 and 28 turns below `8n`.

Add immediately after “The lower bound has a short proof.”:

> In this argument, assume `n >= 8`.

### 2. Define the two vectors from the same cell

Replace:

> Every cell is entered by one move and left by another. The cell is straight only if the two moves point in exactly opposite directions. Otherwise, it is a turn.

with:

> At each cell, look at the vectors from that cell to its predecessor and successor in the tour. The cell is straight exactly when these vectors are opposite. Otherwise, it is a turn.

The incoming and outgoing travel vectors themselves point in the same direction at a straight cell. The replacement fixes that ambiguity.

### 3. Give the old horizontal count as an average

Replace the second recap bullet with:

> `2.625` turns per column on average on each of the top and bottom sides (the optimized heels have 21 turns per 8 columns).

The number 21 is verified in the paper. The removed personal attribution is not established by the checked sources.

### 4. Correct the search history and the meaning of the lane rule

Replace the paragraph beginning “The heels on the top and bottom did not” with:

> The heels on the top and bottom averaged 2.625 turns per column. To improve the leading coefficient while keeping the side rate at 2, we focused on the heels.

Replace the paragraph beginning “The heels in the paper keep the four knights in formation” with:

> The paper's optimized heels already let the four knights break formation temporarily, while keeping the same entry and exit cells. Our first search kept each path within its assigned pair of lanes but allowed the four paths to be permuted. It found a piece with 18 turns per 8 columns, and no better rate in the tested sizes. With the side pieces, this gives `8.5n + O(1)` turns.

The paper explicitly permits temporary formation breaks. The search record's lane restriction does not preserve the identity of each of the four strands. The recorded 18-turn optimum is specific to period 8 and depth 4; larger tested models have time-limited results. The replacement makes no global optimality claim.

Replace:

> With this freedom, the search found a piece with 16 turns per 8 columns, which is exactly 2 per column:

with:

> With this freedom, the search found a piece with 16 turns per 8 columns, an average of 2 per column:

### 5. Scope the side and corner descriptions

Replace:

> The left and right sides use the simplest pattern possible. Columns 0 and 1 turn, and everything else goes straight:

with:

> Away from the corners, the two columns nearest each vertical side turn, and the other cells in that side region are straight:

Replace:

> So there are 4 sets of corners, and each set works for every board size in its class.

with:

> So there are 4 sets of corners, and each set works for every even board size `n >= 48` in its residue class modulo 8.

### 6. State the top phase exactly and exclude the corner columns

Replace the paragraph beginning “On the top and bottom, the number of turns per column is not constant” with:

> Outside the corner columns, the bottom counts repeat as `3, 1, 2, 2, 1, 3, 2, 2`. At board column `x`, the top uses bottom-template column `(1 - x) mod 8`, with both moves negated. Its counts repeat as `1, 3, 2, 2, 3, 1, 2, 2`. Each column from 6 through `n - 7` has exactly 4 turns across the two bands:

Replace:

> On the left and right, every row has 2 turns on each side, so 4 per row.

with:

> In every row from 6 through `n - 7`, the left and right bands have 2 turns each, so 4 in total.

The current count figure caption is correct: its 16 shown columns are 8 through 23 and exclude the corners.

### 7. Include legality and reciprocal moves before claiming cycles

Replace:

> The rules above give every cell two moves, so they always give a set of cycles that cover the board. We need it to be a single cycle, for every `n`.

with:

> For every even `n >= 48`, the construction gives each cell two distinct legal neighbours, and the choices are reciprocal. This gives cycles covering the board. We must also show that there is only one cycle.

Two arbitrary move choices alone do not imply a 2-factor.

### 8. Describe the blocks and the induction range correctly

Replace the paragraph beginning “The unit of the argument is a block” with:

> First contract the straight interior paths. A block consists of 8 consecutive diagonal-line labels and the pieces at both ends of those lines. Its paths meet the rest of the reduced graph through a few ports. Some paths cross the block, and some return to the same cut.

Replace:

> If that holds, inserting an extra block anywhere in that stretch leaves every connection of the rest of the tour as it was.

with:

> At a cut with the required template phase and enough space from the corners, inserting a second copy preserves the connections to the rest of the reduced graph.

Replace the paragraph beginning “There are three kinds of blocks” with:

> There are three kinds of blocks: bottom-left, left-right, and right-top. All three pass the matching check. For every even `n >= 96`, the chosen cuts have enough space for the insertion argument. It proves that one cycle at size `n` stays one cycle at size `n + 8`. The bases `96, 98, 100, 102` therefore cover all larger even sizes; direct checks cover the smaller even sizes from 48 to 94.

The direct-check sentence about 48 through 102 is correct and can stay. The growth figure at 48 and 56 is also correct, but it illustrates the family rather than the proof's separated-block base range.

### 9. Limit the local sharpness claim to its method

Replace:

> The `-7` is sharp for this method: there is a corner pattern that reaches it. So a better lower bound needs a different idea, not a better corner table.

with:

> The local corner bound `-7` is sharp: a pattern with reciprocal internal edges and no internal cycle attains it when the edges leaving the corner are left free. Improving the global constant needs more information than this independent `4 x 4` corner bound.

### 10. Compare reduced graphs, not literal boards

Replace:

> A separate check confirms that the board for `n + 8` is exactly the board for `n` with the three blocks doubled.

with:

> A separate check compares the reduced graphs after straight paths are contracted: the graph at size `n + 8` is obtained by doubling the three chosen blocks and translating the remaining pieces.

Replace the independent-rebuild bullet with:

> The tours were rebuilt and checked by an independent program for every even `n` from 48 through 134, and for `n = 312, 314, 316, 318`.

### 11. Clarify the copied lemma image and complete the status note

Add this caption to the first `BlogImage`:

> The arrows in the first two panels show possible moves. A tour uses two moves at each cell. The argument assumes n >= 8.

After the corrections are applied, replace the unreviewed-status bullet with:

> The post and figure script were independently reviewed on 2026-10-02, including the displayed turn counts and the scope of the insertion proof.

Until then, retain a note that this review found corrections. The figures themselves do not need numeric changes.

## Artifacts and limits

`w-verifier/claim16_blog.py` checks the local sharpness witness, exact saved rebuild range, unchanged corner hashes, and the plotted count arrays. Results are in `claim16_blog.json`. The isolated figure script, run log, and all PNG files are in `claim16_runner/` and `claim16_runner/blog_images/`.

No full-site build or live blog-link check was requested or performed. The MDX figure URLs still need the normal publication asset placement; generating images in `writeup/turns/images/` alone does not establish that a site's `/blog/knights-tour-turns/` URLs serve them. Title, date, credits, and other author TODOs remain the author's decisions. In particular, a title saying the conjecture was wrong “by 14 turns” should not imply that the unknown minimum is exactly 8n-14.

# Claim 17 — proposed carrier lower bound (2026-10-02)

**Verdict: conditional counting argument is sound; the stated general carrier theorem and the fold-family conclusion are NOT YET PROVED.** At audit time, `w-searcher/FINDINGS.md` ends with the strip certificates and contains no carrier section. I checked the argument in the Chief's brief, the carrier current-calibration code, and the already audited tile identities. This verdict concerns that supplied argument, not an unseen later proof.

## 1. When bad quarters are at most 4X

On a complete two-dimensionally periodic degree-two field, use a period quotient with N cells. There are N edge orbits and total tile area N. If G counts uncovered quarters and S=sum(m-1)_+ counts surplus multiplicity, area equality gives G=S. Also

```text
S <= sum binomial(m,2) <= 2X,
D := number of multiply covered quarters <= S.
```

Hence G+D<=4X. Here X counts proper crossing-pair orbits, including pairs crossing the period seam. One must use the lifted geometry, not count only segments drawn wholly inside a chosen period box. This is a valid consequence of the tile theorem. No connectivity is needed.

A field with only one translation period has an infinite cylinder as quotient. “Tile area equals cell count” is then an equality between infinite quantities and does not supply G=S in a chosen finite-width band. A finite band also has edges and tiles crossing its boundary. Its area balance must include them.

More generally, in any precisely specified finite region, let Delta=sum(m-1) over its quarter triangles and let P count crossing-pair contributions there. Then S-G=Delta and

```text
G+D <= 2S-Delta <= 2P-Delta.
```

If P<=2X_region, this becomes G+D<=4X_region-Delta. Dropping Delta requires a proof that it is nonnegative, zero, or bounded by the stated error. Degree two inside the band alone supplies none of these. A local window containing only gap quarters illustrates why crossings cannot be localized by position without a boundary balance. The audited gentle seam has gaps next to its multiply covered quarters.

A fixed-width carrier repeated for many periods may admit an end error O(width), but that needs a cancellation argument on the long side boundaries and a definition of the counted edge/pair orbits. If the width grows with n, the same error is not automatically O(1). The missing carrier section must settle these points before the claimed per-period local bound is accepted.

## 2. Which current forces a bad quarter

The relevant charge is

```text
omega_H = phi_H + phi_Q modulo 3,
```

where Q is the black-to-white unit-grid field. It is the height change from the tile identity. A path with nonzero total omega_H has a step next to a bad quarter. A quarter is next to just one unit dual edge, so edge-disjoint charged paths give distinct bad quarters.

A raw value phi_H=+1,-1,+2,or -2 is not enough unless the reference contribution phi_Q has been included or proved zero on the chosen transversal. I checked a concrete counterexample to that raw-current interpretation. Take the crossing-free degree-two field consisting of all edges p--p+(2,1). Every quarter near the test cut has multiplicity one. The dual segment from (1/2,1/2) to (3/2,1/2), with normal pointing up, has phi_H=1 and phi_Q=-1. Its height charge is zero. It requires no bad quarter despite raw current +1.

For **height charges**, all four integers +1,-1,+2,-2 are nonzero modulo three. The argument treats them alike: it does not give twice the cost for magnitude two. It gives no bound for a charge divisible by three. If “current” means a change relative to a crossing-free reference field, explicitly prove that this change equals omega_H modulo three on each transversal.

The files under `w-searcher/carrier/` contain several raw cut conventions, including x cuts and x+y cuts. The supplied `fluxcal.py` itself distinguishes these conventions. A target in such a search is not yet a proof of the required common height difference on every transversal.

## 3. Menger, planar duality, and route length

With unit capacities on dual edges, the maximum number of edge-disjoint paths between two specified boundary sets equals the minimum size of an edge cut separating them. Planar duality can identify such a cut with a primal barrier, but the domain, boundary wiring, and permitted ends must be specified.

For a periodic annular band, with the two sides as source and sink and no artificial finite-capacity attachment edges, a separating barrier contains an essential primal cycle. If one turn around the cylinder lifts to translation v=(p,q), that cycle has at least |p|+|q| unit grid edges. This follows because its horizontal and vertical steps must sum to p and q. The inequality is enough; equality needs an admissible monotone barrier and is not automatic.

This is a bound in terms of **net translation**, not the length of an arbitrarily selected route. A route from (0,0) via (0,2),(2,2) to (2,0) has length six, while the shortest unrestricted primal path between its ends has length two. A theorem about route length must prove that shortcuts are excluded by the carrier domain or use the shortest essential barrier length instead.

All the packed transversals must also be charged. One charged transversal alone does not suffice. A suitable hypothesis is a single-valued mod-three height on the cylinder, constant on each of its two boundary components, with different values on them. Check longitudinal height monodromy when passing from the plane to a quotient. If a period reverses chessboard colour, use a colour-preserving multiple of it and normalize all counts consistently.

Under these topological and charge hypotheses, let M be the minimum separating edge-cut size. Then at least M distinct bad quarters occur. If the same domain also has the valid period balance from part 1, it follows that

```text
X_period >= M/4 >= (|p|+|q|)/4.
```

For v=(p,p), p>0, this gives X_period>=p/2, or at least one half crossing per unit x displacement. This is a valid **conditional** carrier inequality. It is not established merely by naming Menger's theorem.

## 4. Why 4n+n/2 does not follow yet

Two lower bounds X>=4n-O(1) and X>=n/2-O(1) cannot be added. Their crossings can overlap, and the tile gap budget is global. The present brief gives no disjoint allocation or combined identity that makes the carrier cost additional to 4n.

There is an existing route to a correct combined statement. Let B be a boundary crossing set with |B|>=4n-C. Suppose the union U of the carrier quarters is inside the board and avoids **all tile overlaps** of pairs in B. If the carriers force at least M distinct bad quarters in U, the audited budget gives

```text
M <= 4X-8n+4-2|B| <= 4(X-4n)+4+2C,
X >= 4n + M/4 - 1 - C/2.
```

Thus M>=2n-O(1) would indeed give X>=4.5n-O(1). However, a fold-family proof still has to define that family, identify the charged bands, prove their total separating-cut bound, prevent duplicate quarter charges across bands and junctions, exclude the boundary-pair overlaps from U, and control endpoint errors. None of those facts is supplied by the carrier argument alone. Intersecting, merging, or cancelling carriers also require treatment. This audit gives no counterexample to the numerical 4.5 bound; it finds missing hypotheses and a missing global counting step.

## Checks and next proof needed

`w-verifier/claim17.py` independently checks the raw-current counterexample and the quarter multiplicities of the known degree-two gentle seam. Results are in `claim17.json`. The seam has two gaps, two double quarters, and one crossing per (1,1) period, so its total four bad quarters attain the 4X budget; it does not contradict the proposed one-half-per-x lower bound.

The next useful input is a precise carrier theorem specifying its quotient, charge convention, boundary conditions, crossing count, and shortest-barrier quantity. A separate lemma must establish the combined finite-board inequality for the proposed fold family. Until those are written and checked, label the per-carrier statement conditional and the 4.5n fold-family conclusion unproved. All work here used one CPU core and no solver.

# Claim 18 — one critical row per endpoint (2026-10-02)

**Verdict: PASS.** For every closed Hamiltonian tour on an even n by n board, n>=32,

```text
X >= 9n/2 - 585.
```

I checked Sections 10.1--10.3 of `w-turnstheory/FINDINGS.md`. My independent graph reconstruction, corner calculation, reflected endpoint tests, row-interval check, and final arithmetic all pass. All four supplied checkers also pass. This proof does not use the conditional carrier argument of Claim 17.

## What one critical row determines

My independently rebuilt forest strip graph has 82,516 states and 144,674 arcs. The exact ordinary potential identifies the same two four-state critical cycles as before. Each cycle visits column phases 0,1,2,3 in order.

For each cycle, I start at phase zero and follow all four transitions. I take the union of pending edges in the five states, shifting the final state's coordinates back by one row. There are exactly 20 possible strip edges whose endpoint rows straddle row zero, including an endpoint on that row. The critical row determines seven of these edges as present and thirteen as absent. The union is exactly the P or P' pattern restricted to these 20 edges.

This recovers edges incident to ghost columns as well as columns zero and one. In particular, an edge such as (0,-1)--(1,1), which skips row zero, is fixed. A proof based only on the two neighbours of the two strip cells in that row would be insufficient; the full scan state is essential.

The completeness argument is valid for any scan row. An edge whose lower endpoint precedes the row and whose upper endpoint reaches it is in the initial pending state. An edge whose lower endpoint is in the row appears after the appropriate column transition. Every knight edge in this strip has nonzero vertical displacement, so no edge can be introduced and consumed wholly within the same row. The union of the five states therefore includes every present edge straddling the row and specifies the absence of every other such edge.

The two critical cycles are disjoint. Four successive critical arcs cannot switch between them without using a noncritical arc. Thus the “good row” condition in the per-row stability certificate is exactly the condition used here.

## Independent one-row corner calculation

I used my own exact signed-intersection coefficient routine for Q_R and my own enumeration of the seven-cell corner data. I changed the degree cancellation to include boundary rows 4 through R-1, as required by the new proof.

I enumerate all knight edges in a box extending beyond the whole dual path, without assuming the residual support in advance. After cancellation, every nonzero coefficient lies either at the seven corner cells or at one of the two endpoint lists. Each list has eight edges. After normalizing by chi(0,R), the independently derived left list agrees entry by entry with the eight coefficients printed in Section 10.2. The bottom list is its transpose.

Every edge on the endpoint list straddles row R and belongs to the width-two strip model. Substituting the edges recovered directly from either critical cycle gives normalized contribution -1 in both cases. I did not substitute a full four-row neighbourhood.

For each R=12,13,14,15,24,25,60,61, all four choices of the left and bottom critical patterns and all 2,916 degree-consistent corner choices give

```text
integral over Q_R of omega_H = 1 modulo 3.
```

The residual support and constant have identical normalized signatures at each parity. Increasing R by two inserts opposite-colour middle cells and translates the endpoint terms by two. The direct degree cancellation proves the identity for all R>=12; the larger finite tests confirm the translation formula. No extra endpoint row is needed.

The total height change around the dual square is zero in a degree-two region. Its complementary path gamma_R is therefore charged. Reflection or transposition can change the overall sign of the charge, but cannot make it zero.

## Both corner orientations and whole-square exclusion

Use one scan direction for each physical side, rather than choosing a new scan for each corner. Reflection of a complete P straddling-edge set through its scan row gives the P' straddling-edge set, and conversely. I check this equality directly. Thus the corner at the far end of a side can use the same good-row classification as the near corner, even though its local inward coordinates reverse the scan direction.

The only column-zero overlap that enters the second unit square strip is the pair

```text
(0,j)--(2,j+1), (0,j+1)--(2,j).
```

For an endpoint square above a tested row R, j=R. For an endpoint square below it after reflection, j=R-1. Both possible pairs straddle the tested row. Neither P nor P' contains both members of either pair. My check tests both square positions and both reflected patterns.

All other path squares lie farther inside, as established in Claim 15. Hence the union of whole squares centred on retained path vertices avoids every tile overlap of the full boundary set B. There is no need to test the critical status of the adjacent row separately, and no extra loss of paths for this exclusion.

The previous vertex-disjointness and inside-board proofs are unchanged. Each retained charged path gives two distinct bad quarters in its own square set. With the corrected boundary count |B|>=4n-24, the full-square budget remains

```text
2L <= 4X-8n+4-2|B| <= 4E+44,
E = X-4n+2.
```

This uses the four possible common corner edges and five possible common crossing pairs, not the erroneous one-pair deduction corrected in Claims 14--15.

## Why one bad row removes at most one path

Put m=n/2. At the near corner, the tested scan row is R, for 12<=R<=m-4. At the far corner, the same physical scan coordinate is n-1-R, giving the interval [m+3,n-13]. Thus the two row sets are

```text
[12,m-4] and [m+3,n-13].
```

They are disjoint. Each row in either interval is assigned to exactly one candidate radius at one corner. Consequently a bad row of one side removes at most one candidate path. A path can be rejected at both of its sides, which only overcounts the number removed and is safe.

Here d is the sum of bad **side-scan rows** over the four width-two strips. It is not a count of distinct physical board rows or cells. This is exactly the d charged once per completed dirty row by the earlier per-row potential. No change of row definition, reflection-dependent recount, or run penalty has entered the argument.

The coordinate calculation holds for every even n>=32. I additionally check the intervals at n=32,34,48,64,96,128,256. Therefore

```text
L >= 2n-60-d.
```

## Stability and final constant

The per-row certificate from Claim 13 remains applicable: the graph, critical arcs, and dirty-row flag are unchanged. The primary certificate source files are identical to the checked copies. The separate implementation has only an added run-check function after its existing code; its per-row check is unchanged. The verified potential range is [-46,0] in units 1/8.

For each side,

```text
X_sigma-n >= d_sigma/2 - 46/8.
```

Summing without rounding 46/8 upward, and using the unchanged safe corner-duplication bound sum X_sigma<=X+1104, gives

```text
d <= 2(sum X_sigma-4n+23)
  <= 2(X+1104-4n+23)
   = 2E+2250.
```

Now combine the two bounds for L:

```text
4n-120-2d <= 2L <= 4E+44,
4n <= 4E+2d+164
   <= 8E+4664,
E >= n/2-583,
X = 4n-2+E >= 9n/2-585.
```

Every displayed constant is correct. The proof still requires a Hamiltonian tour because the strip graph excludes internal cycles. The local tile and corner facts alone apply more broadly, but this combined theorem is not claimed for arbitrary 2-factors.

## Reproduction

Independent code: `w-verifier/claim18.py`. Run from the project root with `.venv/bin/python -u w-verifier/claim18.py`. Results and output: `claim18.json`, `claim18.log`.

I ran all four supplied programs sequentially: `check_one_row_strip.py`, `check_corner_one_row.py`, `check_col0_squares.py`, and `check_square_defects.py`. Their output is saved in the corresponding `w-verifier/claim18_check_*.log` files. Each passes. All work used one CPU core and no solver. No proof defect remains in the audited Claim 18 statement.

# Claim 19 — weaker endpoint test, coefficient 14/3 (2026-10-02)

**Verdict: PASS.** For closed Hamiltonian tours, every even n>=32 satisfies X>=14n/3-407. The joint endpoint certificate is valid, its coefficient one is exactly sharp, and the path count uses its failure variable correctly.

## Sufficiency and the two orientations

The independent residual calculation in Claim 18 identifies exactly eight endpoint edge coefficients. Its normalized endpoint contribution is F, and the rest of the corner identity is fixed by degree two. Replacing F=-1 by F=-1 modulo three leaves the corner charge unchanged. The up test additionally excludes the only crossing pair whose tiles could overlap the whole endpoint square. Reflection of both the coefficient list and the exceptional pair gives the down test. A reflected charge can change sign, but remains nonzero.

Passing the joint test supplies the appropriate test at either corner of a side. It can reject rows whose one required orientation passes. This overcounts rejected paths and is safe. It need not characterize the weakest possible sufficient row condition.

I derive the tests from the eight coefficients independently computed in Claim 18. I enumerate all 16,384 masks on the union of their 14 watched edges: 4,064 masks pass each individual test and 1,014 pass both. This does not impose degree constraints, so it also checks the Boolean test and reflection on edge sets outside the strip model. The corner sufficiency itself follows from the exact linear residual identity, not from an assumption that every passing row has pattern P or P'.

## Independent stability certificate

I rebuild the forest graph using my own transitions: 82,516 states, 144,674 arcs. My augmented state stores the complete set of selected edges straddling the current row, rather than F and an exceptional-edge count. I use a 20-edge bit mask, so every relevant absence and presence is explicit.

At phase zero I include all pending edges. At each column transition I union the geometric edge sets before and after it. On the last transition I shift the target coordinates back by one row, evaluate the test, charge one failure, and reset. Each edge is represented by one bit, so repeated appearances in pending states cannot cause multiple counting. The final union is exactly the set of selected edges straddling the completed row. There are 184,006 augmented nodes and 343,631 arcs, including valid row histories from all base phase-zero states.

For up, down, and joint separately, integer Bellman-Ford converges with potential range [-29,0]. I explicitly check every inequality

```text
4w-1-4b+h(source)-h(target) >= 0.
```

Summing over a complete strip walk gives X_sigma-n>=b_sigma-29/4. The supplied separate implementation also passes when rerun for the joint test: 167,782 augmented nodes, 315,389 arcs, seven passes, the same potential range. The node counts differ because my state retains all straddling edges; its state retains only watched edges. Both models compute the same row tests.

## Exact sharpness witness

I independently unroll the proposed period-one edge pattern

```text
(1,y)--(0,y+2), (2,y)--(0,y+1), (2,y)--(1,y+2).
```

Columns 0 and 1 have degree two, as does ghost column 2; ghost column 3 has degree zero. I reconstruct the pending path components from processed vertices, match the four scan states to the reachable base graph, and check their cycle directly. The four arc weights are 0,0,2,0, for two crossings per row. A separate proper-intersection recount with periodic ownership gives the same two crossings.

Both endpoint sums are F=-2, hence F=1 modulo three, so every row fails either test and the joint test. The ratio (crossing weight minus base rate)/failed rows is (2-1)/1=1. The four-step cycle has cost -4 in units of 1/4000 at beta=1001/1000. Thus no beta>1 can hold with a fixed additive constant on all strip walks. This explicit reachable witness establishes exact sharpness without relying on capped search or Dinkelbach convergence. Its states and weights are in `claim19.json`.

## Failure count and arithmetic

Use the same fixed scan direction per side and the same disjoint endpoint-row intervals [12,n/2-4] and [n/2+3,n-13] as in Claim 18. Reject a path whenever either of its tested rows fails the joint test. Each failed side-row can remove at most one path. Counting failures elsewhere in the strip, or counting a path rejected at both ends twice, only weakens the bound. Therefore L>=2n-60-b, where b is exactly the total of the certificate's row-end charges over all four strips.

The corner charge and whole-square exclusion hold for every retained path. The corrected boundary count remains |B|>=4n-24. With E=X-4n+2,

```text
b <= sum X_sigma-4n+29
  <= X+1104-4n+29 = E+1131,
2L <= 4E+44,
4n <= 4E+2b+164 <= 6E+2426,
X >= 14n/3-1219/3 >= 14n/3-407.
```

The exact intermediate bound is E>=2n/3-1213/3. Section 9's decimal “404.4” is a safe upward rounding of 1213/3, not an equality; its claimed bound is valid. No orientation split or extra endpoint potential is needed because the joint test is certified in one walk. The Hamiltonian restriction remains necessary for the forest model.

Independent code and output: `claim19.py`, `claim19.json`, `claim19.log`. Supplied joint-check output: `claim19_supplied_joint.log`. All jobs used one CPU core, sequentially, without a solver.

# Claim 20 — standalone crossings proof (2026-10-02)

**Verdict: PASS.** I audited `w-turnstheory/PROOF_crossings_lower.md` after its status became “Ready for standalone audit.” The document gives a complete proof, with exact finite inputs, that every closed Hamiltonian tour on an even n by n board, n>=32, satisfies

```text
X >= 14n/3-407.
```

The exact bound obtained before rounding is X>=14n/3-1219/3. No unproved carrier claim, local search optimum, or general-2-factor extension is used.

## Complete chain

**Tile geometry and area, Sections 2--3:** the tile overlap lemma, quarter multiplicities, and local flux identity agree with the independently audited statements in Claim 9. All tiles stay inside D because their vertices stay in the endpoint box of a board edge. There are n squared edges and 4n squared tile incidences. The exact surplus identity gives G<=2E, with E=X-4n+2. For U inside D and B avoiding its tile overlaps, the combined bound is bad(U)<=2E+2(X-|B|). This counts gaps and multiply covered quarters separately and does not charge any quarter outside the board.

**Loop identity:** the standalone document now explicitly proves the existence of the mod-three height. I independently check its new geometric explanation. For all eight directed knight moves and four translation parities, a knight edge crosses exactly the same three unit dual edges, with the same signs, as the stated three-step unit-grid route. I compare each route against 200 nearby directed dual steps. This proves the signed boundary identity by telescoping for any finite set of cells. With a counterclockwise boundary and the cells on its left, the degree-two field contributes 2 sum chi and the unit-grid field contributes 4 sum chi. Their sum is zero modulo three. The signs in Equations (2), (3), and (3a) are consistent.

**Strip model and row data, Section 4:** the forest condition follows from restricting a Hamiltonian cycle to a proper boundary strip. The finite pending-edge and component state is sufficient: a knight edge spans at most two rows, crossings are counted when its later-created edge is introduced, and a closed component is rejected. The graph and complete critical-row edge data agree with Claim 18. The weaker joint test is the test independently certified in Claim 19; it does not require a row to follow a critical cycle.

**Boundary count, Section 5:** the width-one potential supplies n-1 per side. The four possible common corner edges, including both edges at the corner vertex, have five possible crossing pairs. Thus |B|>=4n-24 is valid. The exceptional inward-overlap pair is exactly the one excluded by the endpoint test. Both orientations are specified. The proof excludes tile overlaps from whole path squares, not merely crossing points or selected quarters.

**Two defects per path, Section 6:** the alternating square identity is valid for every selected edge set. A nonzero step has a bad quarter, and its square has a second one. Vertex-disjoint paths use different square centres. The complete whole-square union lies inside D. Therefore 2L<=4E+44, using the corrected boundary count.

**Stability, Section 7:** the joint failure is charged once at row end. The exact potential from Claim 19 has range [-29,0], and the current supplied implementation passes. The safe overcount of the four width-two strips is 4 times binomial(24,2)=1104. Hence b<=E+1131. No orientation split creates an additional endpoint error.

**Final path count, Section 8:** the nested arcs have no common vertex because their local maximum coordinate identifies their radius. The four corner boxes are separated. Each side's tested scan rows lie in the disjoint intervals [12,n/2-4] and [n/2+3,n-13]. Therefore each failed side-row removes at most one candidate path, giving L>=2n-60-b. Combining the two bounds for L gives

```text
4n <= 4E+2b+164 <= 6E+2426,
E >= 2n/3-1213/3,
X >= 14n/3-1219/3 >= 14n/3-407.
```

All dimensions, ranges, inequalities, and constants match the earlier independent audits. The scope is explicitly Hamiltonian tours, not arbitrary 2-factors.

## New larger-box corner proof

This is the material new to the standalone proof. Its auxiliary box encloses all cells (x,y) with 0<=x,y<=R. Its left and bottom dual sides are at -1/2, outside the board, and its right and top sides are at R+1/2. The counted path gamma_R is unchanged and remains entirely internal. The outside sides are used only for flux, never for an area or bad-quarter count.

No selected knight edge crosses the outside left or bottom sides. The unit-grid contribution on them is exactly

```text
2 sum from j=0 to R of (-1)^j = 1+(-1)^R.
```

The two top end steps have zero net unit-grid contribution. I independently enumerate all nearby knight edges in a region larger than the required endpoint box, derive the eight nonzero signed flux coefficients, and subtract the earlier F coefficient list. The difference is exactly the indicator of incidence at (0,R). Consequently the normalized top-end flux is

```text
F + deg_H(0,R) = F+2.
```

This identity holds for arbitrary selected edges, before applying degree two. If the up test passes, F=2 modulo three and the normalized flux is one. Transposition with reversal of the dual steps proves the same right-end identity. The reflected test supplies the corresponding result at the opposite corner orientation.

I check the actual outside and end unit-grid sums at R=12,13,14,15,24,25,100,101. Their formula follows for all R from the alternating sum. Combining both end fluxes gives

```text
integral over Q_R of omega = 1+(-1)^R+2(-1)^R = 1 modulo three.
```

The entire box boundary has zero height flux modulo three, since it encloses only degree-two board cells. Thus gamma_R is charged. This proves the needed endpoint lemma without enumerating any corner completion. The two exceptional edges still supply the independent whole-square exclusion condition. I found no missing corner or boundary assumption in this replacement argument.

## Supplied runner and independent evidence

I ran the unified runner with only its report-output path redirected into the verifier directory. It executes one process at a time. All six checks pass: tile geometry and flux; complete critical-row data; the larger-box corner identity; boundary count and whole-square exclusion; the square defect identity; and the joint endpoint stability certificate. The runner also checks the final arithmetic.

Its report is `w-verifier/claim20_supplied_checks.json`; its full output is `claim20_supplied.log`. The independent new-input checker is `claim20.py`, with exact results in `claim20.json`. The independent stability reconstruction and explicit sharpness witness are in `claim19.py/json`; the earlier geometry and path checks are identified in Claims 9, 15, and 18. The finite sharpness witness is not needed for the lower theorem itself.

`claim20_sources.json` records SHA-256 hashes of the audited document and its checker dependencies. No worker source or report was changed. All computation used one CPU core and no solver. No mathematical correction is required for this audited version.

## Claim 20 addendum — document audit and clean-shell checks (2026-10-02)

**Verdict: mathematical PASS; document edits required before release.** I read the standalone document from start to finish. The bound and the larger-box argument pass. No further mathematical lemma from FINDINGS or TILE_INPUTS is needed. However, the document leaves several conventions implicit. In particular, it must define the normalized strip graph and reduced costs, fix the scan direction on each side, and remove the history-dependent sentence in Section 9. The overlap statement must refer to positive-area overlap, not merely to tiles that meet a square. These edits do not change the bound.

### Larger box and comparison with Lean

The independent checker `claim20.py` passed again. It checks the three-step route for every knight direction and translation parity, the full end-flux coefficient identity, transposition with direction reversal, and both parities of the outside contribution. The identity is linear in selected edges. Thus it proves the weaker residue test for arbitrary selected endpoint edges, not only for P/P' patterns. The box includes row 0 and column 0. Only the four end steps of its complementary boundary can meet tour edges. The outside sides contribute unit-grid flux only. No bad quarter outside D is counted.

I read `ktlean/Ktlean/Corner.lean`, `CornerRow.lean`, and the relevant rotation and frame statements. `KT.box`, `KT.gammaSteps`, `KT.T4`, and `KT.outerSteps` give the same boundary split. `KT.corner_charge_row` assumes distinct knight edges with nonnegative endpoints, degree two on the whole box, R>=12, and exact P/P' data at both ends. It concludes that some step of gamma has flux plus colour nonzero modulo three. This agrees with the pattern case of the document.

**Scope limit:** that Lean theorem does not state the weaker F-residue and exceptional-pair test. The independently checked coefficient identity supplies that extension in the document. Do not describe `KT.corner_charge_row` as a formal verification of the weaker endpoint test. This was a source comparison, not a new Lean build. Lean uses the strict cut condition min_y<=R<max_y. The complete scan-row data use min_y<=R<=max_y and imply the required strict-cut data for a good row. The reflected strict-cut index and the reflected scan-row index differ by one; this is a convention difference, not a defect in the document's row intervals.

### Every listed command, from a clean environment

I copied the required checker files and their local dependencies to `w-verifier/claim20_clean/`. I ran each command separately from that root with `env -i`, a standard PATH, and Python bytecode output disabled. The snapshot uses the Python standard library only. No existing PYTHONPATH, virtual environment, solver, or previous JSON report was needed. I ran one process at a time.

All eight commands returned exit status zero:

```text
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_one_row_strip.py
python3 w-turnstheory/check_corner_box.py
python3 w-turnstheory/check_col0_squares.py
python3 w-turnstheory/check_square_defects.py
python3 w-turnstheory/check_lower_stability.py
python3 w-lowerbounds/endpoint_independent.py both 1 1
python3 w-turnstheory/check_crossings_lower.py
```

The exact command results are in `claim20_clean/commands.json`. Individual outputs are `claim20_clean/command_1.log` through `command_8.log`. The unified report is `claim20_clean/w-turnstheory/crossings_lower_checks.json`.

### Constant audit

| Quantity | Source and value |
| --- | --- |
| Excess tile incidences | 4n²-4(n-1)² = 8n-4 |
| Boundary union | 4(n-1)-4*5 = 4n-24 |
| Whole-square inequality | 2L <= 2E+2(X-4n+24) = 4E+44 |
| Strip overcount | 4*binomial(24,2) = 1104 |
| Four endpoint potential errors | 4*(29/4) = 29 |
| Failure bound | b <= X+1104-4n+29 = E+1131 |
| Candidate paths | 4*(n/2-15) = 2n-60 |
| Combined constant | 120+44+2*1131 = 2426 |
| Exact final bound | X >= 14n/3-1219/3 |
| Printed constant | 1219/3 < 407, so -407 is safe |

### Exact text replacements

The following replacements make the document readable without the research history. They are proposed text only; I did not change the author's file.

**1. Section 1, replace the paragraph from “Put the cell centres” through “opposite colours” with:**

> Put the cell centres at V={0,...,n-1} squared, with x the column and y the row. A knight edge has coordinate differences whose absolute values are 1 and 2. Let X count unordered pairs of tour edges whose open segments intersect properly: their relative interiors intersect and the segments are not collinear. The tour H is a connected simple degree-two graph on V and has n squared edges. Put chi(x,y)=(-1)^(x+y). Call a cell black when chi=1 and white when chi=-1. Every knight edge joins opposite colours.

**2. Section 1, after the paragraph that defines the internal dual grid, insert:**

> Every dual path below is a sequence of unit dual steps. Split each longer displayed segment into these steps. An integral along a path denotes the sum of its signed step fluxes.

**3. Section 3, replace “Its flux through s is chi(a). Therefore” with:**

> Its flux through s is chi(a). Define the integer flux omega(s)=phi_H(s)+phi_Q(s), and use its residue modulo three for height changes. Therefore

Also replace “Its flux out of A is therefore chi(p)(1_A(p)-1_A(q)), by telescoping along that lattice path.” with:

> For a knight edge with endpoints p and q, its signed flux out of A is chi(p)(1_A(p)-1_A(q)), by telescoping along this lattice path.

**4. Section 4, before “We first define the finite strip states”, insert:**

> Fix one coordinate frame for each side. Its first coordinate is inward distance and its second is the scan row. For the left, right, bottom, and top sides these coordinates are (x,y), (n-1-x,y), (y,x), and (n-1-y,x), respectively. Use the same scan direction at both corners of each side. Write sigma for a side and use local coordinates when discussing its strip.

**5. Section 4, replace the paragraph from “Scan cells in order” through “spans at most two rows” with:**

> Scan cells in increasing (row,column) order, starting at row zero, column zero, with no pending edges. There are four transitions per row. A state records the next column, all selected edges from processed to unprocessed cells, and the partition of their pending ends into paths through processed cells. Record coordinates relative to the current row and identify states that differ only in path labels. At each cell choose edges to later cells. Keep only knight edges incident to column 0 or 1. The processed cell must have final degree two in columns 0,1 and degree at most two in columns 2,3. Reject a choice if it exceeds a future cell's degree bound or closes a cycle. After column 3, subtract one from the row coordinates and return to column 0. Use only states reachable from the empty initial state. A transition has weight w equal to the number of proper crossings introduced by its new edges. Thus the weight sum over the 4n transitions of a board strip is its crossing count X_sigma. The state set is finite because a knight edge spans at most two rows.

**6. Section 4, replace the first two sentences of Lemma 3 with:**

> This reachable graph has 82,516 states and 144,674 arcs. Give each arc cost 4w-1, and let d(v) be its shortest-path distance from the empty initial state. The checker verifies finite integer distances and the inequalities 4w-1+d(u)-d(v)>=0. Call this last expression the reduced cost. The graph of zero-reduced-cost arcs has two cyclic components, each a four-cycle.

Retain “They give the patterns P_s, s=+1 or -1:” and the displayed patterns. This defines the term before it is used. It also states which potential selects the critical cycles.

**7. Section 4, replace “Now use the bottom-left corner and R>=12.” with:**

> Now use the bottom-left corner and an integer R with 12<=R<=n/2-4.

This states the board-containment condition at the point where the loop uses degree two on A_R.

**8. Section 4, replace “Their normalised flux equals F+deg_H(0,R)=F+2:” with:**

> Translate row R to zero and factor chi(0,R)=(-1)^R out of the signed flux. The resulting normalized flux equals F+deg_H(0,R)=F+2:

Replace “Transposition gives the same conclusion at the right end.” with:

> Transpose the coordinates and reverse the dual-step directions to obtain the same conclusion at the right end.

**9. Section 5, replace the first sentence of the width-one count paragraph with:**

> For the count, keep exactly the tour edges incident to column 0. Scan the resulting width-one forest strip as in Section 4, now with three columns per row: column 0 must have degree two, and columns 1,2 have degree at most two.

**10. Section 5, replace “For the overlap exclusion, a pair of tiles at column 0 can meet a square [1,2] x [j,j+1] only for the pair” with:**

> For the overlap exclusion, the positive-area overlap of two distinct tiles belonging to edges incident to column 0 can enter the square [1,2] x [j,j+1] only for the pair

Replace “No column-0 overlap reaches a square with left coordinate at least two.” with:

> No such positive-area overlap enters a square with left coordinate at least two.

The distinction matters: boundary contact is not counted by the quarter-area argument.

**11. Section 8, replace the sentence that starts “On a fixed side” with:**

> On a fixed side scan, the near corner tests row R and the far corner tests row n-1-R with reflected endpoint data. As R runs from 12 to n/2-4, these row sets are [12,n/2-4] and [n/2+3,n-13], which are disjoint.

Retain the next sentence about at most one lost path per failed row. This links the row counted by the stability certificate to the row used at each endpoint.

**12. Section 9, replace the first three sentences with:**

> Lemma 7 supplies the joint endpoint stability certificate with coefficient one. Sections 6--8 combine it with the two-bad-quarter charge to give the coefficient 14/3. The proof does not require this stability coefficient to be optimal.

This removes the undefined beta and the reference to a former proof slot that outside readers cannot identify.

No worker file was changed. The audit is complete. The remaining action is for the author to apply these document edits before release.

# Claim 21 — final crossings blog and proof audit (2026-10-02)

**Verdict: the two theorem results PASS. The blog needs factual corrections before release.** The final lower proof also needs one false sentence corrected and two short definitions restored. The fold proof has no new mathematical defect. No author file was changed.

The main blog defects are: a total stability bound is presented as a separate charge for every row; additive constants are dropped without notice; the tiled-tour caption calls triple coverage double coverage; and the post claims an unproved limit for the whole fold family. The explicit theorem callout is correct. The post consistently labels 19n/3 as an upper bound, not a universal lower bound, but the family-limit claim is still unsupported.

## A. Checks of the figures and numerical claims

I ran all three supplied figure scripts with output redirected into `w-verifier/claim21_figures/`. All 16 resulting PNG files are pixel-identical to the files beside the blog. I read all script labels and inspected a contact sheet of every image. I exported the scripts' source data, then checked those data with separate code that imports only verifier code. The supplied render/export program is `claim21_render.py`; the independent checker is `claim21_figcheck.py`. The exact results, labels, and image comparisons are in `claim21_figures/independent_checks.json`, `labels.json`, and `image_comparison.json`.

| Figure | Independent check and verdict |
| --- | --- |
| heels.png | Both sources are single tours. Paper n=48 has X=592, T=442; H16a n=64 has X=581, T=630. Each of the three displayed eight-column intervals has 28 and 16 crossings, respectively. PASS. The current gen_tour default is Sequence1Opt. |
| fold_field.png | Four move directions and eight triangular field regions match the construction. It shows the preliminary field, not a completed tour. PASS with this scope. |
| fold_closeup.png | The displayed unmodified fold has zero crossings. Its two highlighted bends are consistent with the field. PASS. |
| edge_uturn.png | Every one of the eight numbered interior rows has one crossing. PASS. |
| chevrons.png | The displayed left-side region has eight closed components before flips and zero after flips. These are local component counts, not a claim that the raw field is one full tour. PASS. |
| flux.png | The actual crop contains ten crossing pairs across sixteen columns. “16 steps” is ambiguous; replace it by “16 columns.” The four signed corner labels alternate and sum to zero. The left panel is a charge schematic, not a shortest-carrier certificate. |
| count.png | The leading terms 4n, +n, and +4n/3 agree with the audited local replacement count. They are not exact separate finite-board counts. The image already says “+ a constant.” PASS. |
| tour96.png | The saved FOLD24 tour is one closed tour; X=720 and T=1251. The caption's 608+112=720 is correct. PASS. |
| lb_tile.png | Area one and four quarters. PASS. |
| lb_overlap.png | The two depicted pairs cross properly; their tile overlaps contain one and two quarters. PASS. |
| lb_tiled.png | The displayed 640 quarters have multiplicities: 31 zero, 540 one, 53 two, and 16 three. Red means at least two, not exactly two. Caption correction required. |
| lb_square.png | The alternating identity and example (1,2,2,1) are correct. PASS. |
| lb_strip.png | Normal pattern: one crossing per row and F=-1 for both tests. Abnormal pattern: two crossings per row and F=-2 for both tests. The joint test passes only the former. PASS as periodic rates. |
| lb_corner_box.png | The boundary and path are correct schematically. The label R=7 lies outside the proof's chosen range R>=12. Use R=12 or label the image as a smaller schematic. |
| lb_nested.png | It draws nine paths per corner at n=48, one dashed. Its rotations use n-y instead of n-1-y, inconsistent with cell-centre coordinates. Correct the coordinate convention as stated below. |
| lb_numberline.png | The plotted positions 4,14/3,19/3,9,11.5,12 are correct leading coefficients. Its caption must say that constants are omitted. |

The lower square count uses the independently written polygon/quarter code from Claim 9. The full-tour checks use the independent integer segment checker. The figure data do not supply an independent claim of optimality for a search result.

### Exact blog text replacements

These are factual corrections. They do not choose Nil's title, credits, or personal account of the work.

**1. Opening historical upper bound.** Replace “Shisheng Li later brought the upper bound down to `11.5n`.” with:

> Shisheng Li later brought the upper bound down to `11.5n + O(1)`.

Replace “The ratio between the bounds went from `3` to about `1.36`.” with:

> The ratio of the leading coefficients went from `3` to `19/14`, about `1.36`.

The ratio is not a finite-n guarantee after including the constants.

**2. The common corner idea.** Replace “One idea shows up on both sides: each corner of the board creates a "charge" that has to go somewhere. The new tours pay to carry it to the centre. The lower bound shows that every tour pays for it.” with:

> One idea shows up on both sides: cheap side patterns force a charge around each corner. The new tours carry this charge to the centre. The lower bound balances the cost of charged paths against the cost of rows that fail the endpoint test.

The charge of every candidate path is conditional on its endpoint tests; it is not automatic for arbitrary side data.

**3. The heel and lane-free rates.** Replace “A computer search found a heel with 16 crossings per 8 columns, once the four knights could leave the heel in any order, as long as the whole tour still closes into one cycle:” with:

> A computer search found a heel with 16 crossings per 8 columns by allowing a different order of the strands within each paired lane group. Checked corner pieces then close the construction into one tour:

Replace “Dropping the four-knight formation altogether, the same kind of search reached `343n/48`, about `7.15n`.” with:

> Dropping the four-knight formation altogether, the same kind of search gave tours with `343n/48 + O(1)` crossings, about `7.15n`, for every even `n >= 96`.

The rates 28/8, 16/8, 2.5 per side row, and their sums 12 and 9 are correct. H16a's all-size count is 9n plus a residue-dependent constant; it is not exactly 9n. Claim 8 supports the LF4 sentence with the added scope.

**4. The preliminary field.** Replace “So the inside of the board costs nothing again. Everything depends on the sides.” with:

> The unmodified field has no interior crossings. Completing it into one tour will add crossings at the sides and in diagonal corridors.

**5. Corner charge and corridor length.** Replace “Each corner of the board creates an imbalance, modulo 3, in how the tour's moves cross the board. It is the same "charge" that the lower bound uses, explained in part 2.” with:

> In this layout, the cheap endpoint patterns create a corner charge modulo 3. Part 2 uses the same charge calculation when the endpoint tests pass.

Replace “Along each diagonal fold, a narrow corridor carries the charge at a cost of `2/3` crossings per step:” with:

> Along each diagonal fold, a narrow corridor carries the charge at an average cost of `2/3` crossings per unit of x:

Replace “Four corridors of length `n/2` each give `4 x n/2 x 2/3 = 4n/3`.” with:

> Four corridors, each spanning `n/2 + O(1)` in x, contribute `4n/3 + O(1)` crossings.

A unit of x is not a knight move, a dual step, or Euclidean length. The exact increment in the proof is a local replacement count, including the joins.

**6. No proved family limit.** Replace the paragraph starting “We tried several ways to untrap the chevrons more cheaply” with:

> The checked fold construction has `19n/3 + O(1)` crossings. We have not proved that this is the best possible rate within the whole fold family.

Retain the next statement that a different layout could do better. The Claim 17 carrier argument was conditional and did not establish this family minimum. The claim that every attempted alternative costs n or more is also not supported by Claims 1--20 as a universal statement.

**7. Five-step overview, item 5.** Replace it with:

> A tour can make some rows abnormal and lose some charged paths. Over the full side scans, `b` abnormal rows require at least `b - O(1)` extra crossings. Balancing the two bounds gives `14n/3 - O(1)`.

**8. Tile multiplicity caption.** Replace the lb_tiled caption with:

> Near a corner of a 48 x 48 tour. Blue: quarters covered once. Red: covered at least twice. White: not covered. The long straight lines inside tile the board perfectly. All the trouble is at the sides.

**9. The exterior flux.** Replace “The whole boundary of the box has total charge 0 (mod 3). Most of the boundary is outside the board, where nothing crosses it, and it is easy to compute.” with:

> The whole boundary of the box has total charge 0 (mod 3). No tour move crosses the left and bottom sides outside the board. The unit-grid part of the charge still contributes there, and its sum is easy to compute.

“Nothing crosses it” would omit the unit-grid flux essential to the corner calculation. Also, most of the entire perimeter is not outside the board; about half is.

**10. Define normal rows in both orientations.** Replace “"Normal" is a precise local test on the moves near the end row, also in the details. The rows of a typical cheap side pattern pass it.” with:

> A row is "normal" when it passes the local endpoint test in both orientations along that side. This is the joint test in the details. The periodic side pattern with one crossing per row passes it.

**11. Step 4, the boundary budget.** Replace the paragraph starting “The boundary crossings (the `4n` from step 1)” with:

> A separate boundary-strip count identifies at least `4n - 24` crossing pairs whose tile overlaps avoid the retained paths' squares. Write `E = X - 4n + 2`. The number of bad quarters on those squares is at most `4E + 44`. Thus four bad quarters require one unit of excess crossing count, up to the fixed boundary allowance.

This gives the intended meaning of “one extra crossing can pay for at most 4.” It is a total inequality. A single crossing is not assigned four particular bad quarters, and the tile-area proof of 4n-2 does not itself identify the boundary set B.

**12. Step 5, paths lost.** Replace “Each abnormal row removes one path, and so saves half a crossing.” with:

> Each abnormal side-row removes at most one candidate path. In the path-count lower bound, that can save at most half a crossing.

Rows outside the tested intervals remove none. Two failed endpoints can belong to the same discarded path.

**13. Step 5, what the computer certificate proves.** Replace “It shows that an abnormal row always costs at least one crossing more than the minimum of one crossing per row:” with:

> It proves a bound for the whole side: with `b_side` abnormal rows, the side strip has at least `n + b_side - 29/4` crossings. The cost of one extra crossing per abnormal row is an average bound with this fixed endpoint allowance:

The displayed normal and abnormal periodic patterns and their rates are correct. Their periodic comparison proves sharpness of this coefficient; it does not establish a separate charge at every individual row.

**14. Step 5, the balance.** Replace the block from “Now the tour has two options” through “so `14n/3` in total” with:

> Write `E = X - 4n + 2`, and let `b` count failed joint tests over the four side scans. The two bounds are:
>
> - The paths give `E >= n - b/2 - 41`.
> - The side scans give `E >= b - 1131`.
>
> Ignoring these fixed constants, the two lines meet at `b = 2n/3`, giving `E >= 2n/3 - O(1)`. Keeping the constants gives `X >= 14n/3 - 407`.

The first inequality follows from 2(2n-60-b)<=4E+44. These two bounds are combined by taking their maximum, not by adding their costs. No tour attaining the intersection is claimed.

**15. Finite bounds versus leading coefficients.** Replace the number-line caption with:

> The leading coefficients of the crossing bounds; additive constants are omitted.

Replace “The minimum number of crossings is between `4.67n` and `6.33n`.” with:

> For every even `n >= 96`, the minimum lies between `14n/3 - 407` and `19n/3 + 142`.

Replace “On the upper side, the fold tours pay exactly for the corner charge (`4n/3`) and for the trapped lines (`n`).” with:

> In the fold construction, the corridors add `4n/3 + O(1)` crossings and the arch flips add `n + O(1)` to the cheap boundary pattern.

The decimals 4.67 and 6.33 are rounded summaries, not exact coefficients of valid finite inequalities.

**16. Replace the whole fold Details paragraph with:**

> **The fold tours for every n.** The construction uses a fixed placement rule and twelve saved sets of thirteen finite patches, one set for each even residue of n modulo 24. The patches cover the physical corners, side midpoints, ends of the reversed U-turn intervals, and centre. After straight field paths are suppressed, there are four corner blocks and four side blocks, each initially six line labels wide. A +24 step adds twelve line labels, or two primitive blocks, at each of these eight positions. The line-label and coordinate-shift calculation preserves every outside connection. Each corner block has an idempotent complete port matching, including any paths that return to the same cut, and composition creates no hidden cycle. A side block permutes four strands in a cycle of order four. Thus +24 alternates between two side matchings, both of which close into one tour with each saved outside matching; +48 restores the matching. Local crossing counts give exactly 152=120+32 extra crossings per +24, from boundary and corridor regions. A standalone checker rebuilds all 36 saved tours and checks the complete block and outside matchings. The geometric insertion argument extends these finite checks to every even n>=96.

The original “12 more diagonal lines in 8 places” does not describe the side blocks correctly. “The true period is 48” must refer to the matching, not to the crossing recurrence or the set of valid sizes.

**17. Details, normal-row test.** Replace its first sentence with:

> In each orientation, the endpoint test sums eight signed coefficients modulo 3 and excludes one specified crossing pair. A normal row passes both orientations.

**18. Details, boundary set.** Replace “Let `B` be the crossing pairs among moves at the outermost column of each side. A computer certificate on the width-one strip gives `|B| >= 4n - 24`, and their overlaps avoid every unit square on the corner paths.” with:

> Let `B` be the union, over the four sides, of crossing pairs whose two moves are incident to that side's outermost column. The width-one strip certificate and the corner duplicate count give `|B| >= 4n - 24`. The endpoint tests ensure that their tile overlaps avoid every unit square on the retained corner paths.

**19. Details, the augmented graph.** Replace the first two sentences of “Abnormal rows” with:

> The strip of the two outer columns, with two more columns for partial neighbours, has 82,516 states in the base cell scan. The certificate augments these states with the test edges seen during the current row. On this augmented graph, an integer potential in `[-29,0]` proves `X_side - n >= b_side - 29/4`.

The potential is not asserted on the unaugmented 82,516-state graph.

**20. Review status.** Replace the final two review bullets with:

> - The consolidated `14n/3` proof and its finite certificates were independently audited. The mathematical bound passed.
> - The post and all sixteen figures were reviewed on 2026-10-02. The review lists factual text and caption corrections to apply before release.

After the corrections have been applied and checked, the second bullet can be removed. Do not mark the present text as corrected yet. The 4n-2 Lean theorem exists with the stated name in `Ktlean/Crossings.lean`; its documented axiom report lists only the standard axioms. I did not run a new Lean build in this audit.

**21. Open questions.** Replace “Where is the true minimum, between `4.67n` and `6.33n`?” with:

> How far can we close the gap between the leading coefficients `14/3` and `19/3`?

Replace “A better lower bound needs more than one defect per path, or wider windows at the sides.” with:

> Possible routes to a better lower bound include more defects per path, wider side windows, stronger endpoint tests, or a tighter crossing budget.

The listed two approaches are not proved necessary.

### Figure-script corrections

In `cross_figs.py`, replace the flux title with:

```python
ax.set_title(f'corridor on the diagonal: {len(pts)} crossings across {x1 - x0 + 1} columns', fontsize=10)
```

In `lower_figs.py`, set `R = 12` in `fig_corner_box()` to use an actual permitted radius. Alternatively keep R=7 and change its caption to “A smaller schematic of the corner path; the proof uses R>=12.”

For `fig_nested()`, keep cell-centre coordinates throughout. Replace the frame by `frame(ax, -1, n, -1, n, pad=.5)`, the board rectangle by `mp.Rectangle((-.5, -.5), n, n, ...)`, the rotation by `pts = [(n - 1 - y, x) for x, y in pts]`, and the failed-row rectangle by `mp.Rectangle((-.5, fail-.5), 2, 1, ...)`. Point its annotation at `(1.5, fail)`. This fixes the half-unit mismatch between the board boundary, side-row highlight, and rotated paths. It does not change the path count.

## B. Final proof comparison and clean-shell checks

Both proof hashes changed from the prior audits. I read both final texts in full and compared their mathematical statements with the Claim 12 and Claim 20 records and the earlier source passages. **Archive limit:** the earlier manifests saved proof hashes, not full copies of both old Markdown files. Thus I cannot supply a complete byte-for-byte old/new Markdown diff. The comparison below is a content comparison. Exact executable diffs are saved in `claim21_clean/checker_changes.diff`; all current source files and hashes are preserved in `claim21_clean/` and `sources.json`.

**Fold proof:** the placement rule, thirteen translations, retained set, line labels, growing intervals, complete port matchings with returns, the two side states, and crossing counts all agree with Claim 12. The changes clarify the argument and add figure instructions. The geometric calculation still does the all-n work; finite samples are not substituted for it. The standalone checker is byte-identical to the saved Claim 12 copy. All twelve corner/centre certificate files have unchanged hashes. The maximum offset remains 142, at base n0=114. The exact increment remains 152=120+32. The step-12 counterexample from base 100 still has three cycles at n=112. **PASS; no replacement required.**

**Lower proof:** the new text removes the unnecessary critical-cycle detour and uses the weaker endpoint identity directly. This is sound. It defines side frames, signed integer flux, the permitted box range, and positive-area overlap. It groups the main argument by leading coefficients and postpones explicit constants to the end. The area, endpoint, exclusion, square, stability, and final inequalities agree with Claim 20. The unified runner drops only `check_one_row_strip.py`, which the final argument no longer needs. The boundary checker removes only the illustrative FOLD96 counterexample to an old corner claim, and changes its message about the explicitly excluded pair. Its exhaustive overlap, five-pair corner count, and width-one potential checks remain. All other lower-proof checker dependencies listed in the Claim 20 manifest are unchanged.

The final lower proof needs these exact corrections:

1. In Section 5, replace “Their other endpoints lie in columns 2 or 3.” with:

   > Their other endpoints lie in columns 0 through 3.

   For example, the legal strip edge (0,y)--(1,y+2) has both endpoints in the outer two columns. The present sentence is false, although the checker uses the correct graph.

2. Replace “At each cell choose edges to later cells, enforce the degree bounds, and reject closed components.” with:

   > At each cell choose edges to later cells so that its final degree is two in columns 0,1 and at most two in columns 2,3. Reject any choice that exceeds a future cell's degree bound or closes a cycle.

   This states the exact-degree condition required by the finite model.

3. In Section 2, replace “Its signed boundary flux is chi(p)(1_A(p)-1_A(q)), by telescoping.” with:

   > For the knight edge with endpoints p and q, its signed boundary flux is chi(p)(1_A(p)-1_A(q)), by telescoping.

   The polished text otherwise uses p and q without defining them.

4. For a self-contained derivation of the explicit constant, replace the sentence “For the explicit constant, the same checks give |B|>=4n-24 and sum X_sigma<=X+1104.” with:

   > For the explicit constant, adjacent sides can share only the four corner edges (0,0)--(1,2), (0,0)--(2,1), (0,1)--(2,0), and (0,2)--(1,0), after rotation. They have five crossing pairs in total, while opposite sides share none. Hence |B|>=4(n-1)-4*5=4n-24. A crossing pair counted in two width-two strips has both edges in their 4 by 4 corner square. There are 24 possible knight edges there, so the strip overcount is at most 4*binomial(24,2)=1104. Thus sum X_sigma<=X+1104.

   These geometric arguments were explicit in Claim 20's version. The new checker still checks the finite numbers, but the polished text should explain why those finite corner counts apply to the board.

I ran all five named lower-proof checkers, its unified runner, and the fold checker in a fresh copied tree using a clean environment and the system Python. All seven commands returned zero. The jobs ran sequentially on one CPU core, without a solver. There is no additional cross-proof run-all script in the supplied files; the lower runner is the listed combined script.

Results are in `claim21_clean/commands.json`, `command_1.log` through `command_7.log`, and both generated proof reports. The lower bound is still X>=14n/3-407, with exact pre-rounding constant 1219/3. The upper bound is still X<=19n/3+142 for every even n>=96. The proof domains have not changed. A final hash check found no source change during the audit.

**Next action:** apply the factual replacements and regenerate the three affected figure outputs before release. The remaining changes are to the presentation, not to the two theorem bounds. The audit is complete.

# Claim 22 — interactive demo audit (2026-10-02)

**Verdict: local tour data PASS; display and caption corrections required. Live delivery is unverified.** The HTTP GET to `127.0.0.1:21018/data/summary.json` failed with connection refused. I did not start another server or change the app. The audit below covers the actual serving directory, the page's JavaScript, and its JSON files. It does not claim a successful browser or network test.

The main defects are mathematical labels on the chart, malformed fractional offsets in the live formula strings, and a reconstruction label that does not say that the 21-turn pattern differs from the picture in the paper. No sampled tour or numeric count failed.

## Tour data, formulas, and live count code

`claim22_sample.py` independently decodes the one-character cell format, checks reciprocal knight edges and a single cycle through all n² cells, and recounts crossings by strict integer orientation tests and turns by collinearity. It imports only verifier code. It checks **153 tours**: nineteen sizes for each of the seven families starting at 48, and ten for each family starting at 96. The samples include all four even residues modulo eight, the lowest sizes, n=96,98,100,102,114,120,144,192,198,200 where available. All pass.

I also compared every one of the **645** JSON records with its summary entry, checked all supported-size ranges, and checked every available same-residue count increment. All pass. The exact slopes are:

| Step | Increment period in n | Crossing slope | Turn slope | Example (n, X, T) |
| --- | ---: | ---: | ---: | --- |
| orig | 8 | 13 | 19/2 | (48,624,442) |
| paper | 8 | 12 | 19/2 | (48,592,442) |
| heel21 | 8 | 51/4 | 37/4 | (48,616,434) |
| P40 | 40 | 23/2 | 39/4 | (48,592,442) |
| H16a | 24 | 9 | 41/4 | (48,437,465) |
| LF4 | 48 | 343/48 | 43/4 | (96,707,1010) |
| FOLD | 24 | 19/3 | 38/3 | (96,720,1251) |
| T18 | 24 | 51/4 | 17/2 | (48,591,391) |
| TT16 | 8 | 19/2 | 8 | (48,454,370) |

TT16 has the exact sampled formula T=8n-14. FOLD obeys X<=19n/3+142. The offsets for other families vary with the size residue. P40 at n=48 equals the paper tour: no full 40-column replacement fits there. Its asymptotic label does not imply that each small displayed board improves the previous step.

`node demo/check.js` checks all 645 files with the same decoder and analyser used by the page. It reports **645 files checked, 0 problems**. Thus the page's numeric X and T values agree with the metadata on every file, and with the independent recount on all 153 samples. I also ran the page's actual `renderCounts()` and formula functions in a minimal DOM harness for all 645 records. This is a code-level display check, not a browser test.

The FOLD generator in `demo/build_data.py` still uses the older component-shape/nearest-position assignment. I compared its saved demo graphs at n=96,98,114,120,144,192,198,200 with the explicit independent assembler from Claim 12. Every edge agrees. Thus these demo records are covered by the audited construction. For future generation outside the demo range, prefer the explicit translation table used in the proof; the nearest-position rule is not itself the all-n proof.

Evidence: `claim22_samples.json`, `claim22_sample.log`, `claim22_js.log`, `claim22_ui.json`, and `claim22_extra.json/log`.

### Defect: 266 malformed fractional offsets

`fmtConst()` joins the whole part directly to a textual fraction when the denominator is four or 48. This changes the apparent number. Actual rendered examples are:

```text
H16a, n=50:  T = 486 = 10.25n − 262/4
LF4, n=98:   X = 721 = 343n/48 + 2034/48
heel21,n=50: T = 443 = 9.25n − 192/4
```

The intended offsets are -26.5, +20+34/48, and -19.5. There are 266 affected metric rows across the 645 records. The counts are correct; these written equalities are not.

Replace `fmtConst()` in `demo/app.js` with this exact function, which prints an unambiguous reduced fraction:

```javascript
function fmtConst(v, b) {
  const num = Math.round(v * b), sign = num < 0 ? '−' : '+';
  const q = Math.abs(num), g = gcd(q, b), a = q / g, d = b / g;
  return `${sign} ${d === 1 ? a : `${a}/${d}`}`;
}
```

For example, the offsets become `− 53/2`, `+ 497/24`, and `− 39/2`. `claim22_fraction_check.js` tests this proposed replacement on every affected case and passes. No app code was changed.

## Original, paper, P40, and reconstructed heel

The independent infinite-strip counter gives:

| Template | Period | Crossings | Turns |
| --- | ---: | ---: | ---: |
| Sequence1Default | 8 columns | 32 | 22 |
| Sequence1Opt | 8 columns | 28 | 22 |
| Reconstructed heel21 | 8 columns | 31 | 21 |
| SequenceP40 | 40 columns | 130 | 115 |
| VerticalEdge | 4 rows | 10 | 8 |

These yield exactly the slopes 13/9.5, 12/9.5, 12.75/9.25, and 11.5/9.75. Original, paper, and heel21 have the same complete periodic endpoint pairing. I independently traced all forty terminals of P40 and verified that its pairing equals five copies of the paper heel. The path traces cover every cell class and have no hidden local cycle. The default template's `xx` cells are straight continuations, not missing moves.

The corner replacement in `gen_alg1()` is real: optimized heels do not fit two Algorithm 1 corner cases, so the demo copies those small pieces from the original heel. The sample includes all affected residues and passes. These changes affect only the constant term. The UI should disclose this modification instead of implying an exact transcription of the paper's full-board algorithm.

### Exact comparison with Figure 11

The offline paper's Section 4.2 and Figure 11 state 22 turns/32 crossings for the original heel, 21/31 for the turn-optimized heel, and 22/28 for the crossing-optimized heel. The text explicitly includes crossings and turns caused by the path continuations. It also says that the search already allowed arbitrary final configurations, but its optima happened to restore the original configuration. Thus the new H16a explanation must emphasize using a changed matching and repairing corners, not the first-ever permission to search other orders.

I read the vector paths from the `/Im11` form on PDF page 20, using pypdf rather than a raster transcription. The cell pitch is 16 PDF units. I split long straight strokes into knight moves and compared them with the periodic move templates.

- The original and crossing-optimized panels each match their stored templates: zero mismatches in 62 tested directed edge incidences.
- The centre panel does **not** match the demo reconstruction: its best phase has twelve mismatches in the same comparison.
- The centre panel itself gives the following template in board.js row order. Two cells outside the drawn heel paths are filled by the straight continuation `26`:

```text
26 46 26 26 26 26 26 26
36 46 26 45 26 26 36 46
02 12 25 25 26 25 56 56
01 17 06 16 16 16 06 67
```

My periodic counter gives **21 turns and 31 crossings** for this printed template too. Its endpoint pairing agrees with the reconstruction and the other paper heels. The reconstruction is therefore valid and reproduces the published performance and pairing, but it is not the actual move pattern in Figure 11.

The existing audit line does say “We rebuilt the heel by an exact search,” so reconstruction is disclosed in part. It should also state the geometric difference. The saved `OPTIMAL` solver status is a report of the constrained model. I did not rerun CP-SAT or independently check its optimality certificate. This audit establishes feasibility, counts, complete pairing, and the difference from the printed pattern.

Evidence: `claim22_heel.py/json/log`, `claim22_figure11_stream.txt`, `claim22_pdf_page.txt`, and `claim22_extra.py/json/log`. No worker code is imported by these independent template and geometry checks.

## Chart lower bounds: correction required

The chart plots exact tour counts against lines currently named “4n lower bound (paper),” “14n/3 lower bound (ours),” and “6n lower bound (paper).” Its tooltip also presents their values as finite lower bounds. That is not what the audited theorems prove:

- The paper crossing result is 4n-O(1). The audited tile theorem gives 4n-2.
- The new crossing theorem is 14n/3-407 for even n>=32. This does not prove X>=14n/3.
- The paper turn result approaches coefficient six: for each epsilon>0 it gives (6-epsilon)n for sufficiently large n. It does not prove T>=6n on every displayed board.
- The new turn line 8n-28 is a valid finite lower bound throughout the demo range.

To keep the intended progression visible, use **reference-line labels**, not finite-bound labels. Replace the `LOWER` names by:

```text
X: 4n reference (paper leading term)
X: 14n/3 reference (new leading term)
T: 6n reference (paper asymptotic coefficient)
T: 8n − 28 lower bound (new)
```

Replace the chart title suffix “as n grows: every step, and the lower bounds” with:

> as n grows: tour counts and lower-bound reference lines

Add this exact visible note below the chart, switching its text with the measure:

> Crossings: the dashed 4n and 14n/3 lines show leading terms, not finite lower bounds. Proven here: X>=4n-2 and X>=14n/3-407.

> Turns: 6n is an asymptotic reference, not a finite bound from the paper. The new finite lower bound is T>=8n-28.

Alternatively draw the actual finite crossing bounds and remove the 6n line. Do not silently draw 14n/3 and call it a theorem at the current n.

## Captions, credits, dates, and audit lines

The step ordering, displayed size ranges, nine families, ten metric steps, and the numeric local rates are correct. The LF4 overlay depths agree with the supplied gadgets. The T18 and TT16 explanations agree with the audited constructions. The crossing-only note about Shisheng's block is correct. The H16a corner width is six. The displayed “Research Lab (ours)” credit is a collective project label; authorship wording remains Nil's choice.

The offline title page says **arXiv:1904.02824v2, 17 Jan 2022**. It also has a typesetting footer “January 19, 2022”; that is not the arXiv version date. Thus both Parker steps' current year 2022 is correct. A more precise replacement is `2022-01-17 (arXiv 1904.02824v2)`.

Nil's earlier local post, `/home/nil/nil/nilmamano.com/blog/knights-tour.mdx`, in “Unexpected help,” explicitly credits Parker with the improvements from 13n/9.5n to 12n/9.25n and says he joined as a co-author for the journal version. Keep Parker's credit for the improved heels. For a credit tied specifically to the original 2019 construction, replace the `orig.credit` value with `Besa, Johnson, Mamano, Osegueda (original construction)`. The current five-author list includes the later contributor. The 2019 first-version label is consistent with the paper identifier; the offline file is v2, not a separate copy of v1.

Shisheng's name, block dimensions, and performance agree with the local patch and independent checks. The month 2026-05 comes from BRIEF.md; I did not have the original dated email available in this project. Treat that month as project-supplied provenance, not an independently checked email date. The new construction and computation date 2026-10-02 agrees with the build/audit records.

### Exact remaining text replacements

**Global leading-term note.** Add under the progression list:

> Step labels show leading terms; exact counts include size-dependent constants. TT16's turn count is exactly 8n-14. The demo's board-size range is narrower than some constructions' full range.

**Original audit line:**

> Original formation construction from the paper. Claim 22 independently checks its strip counts and samples of this rebuild; the browser checks every displayed tour.

**Paper crossing-heel audit line:**

> Paper Figure 11, right: 28 crossings and 22 turns per heel. Claims 21 and 22 check the counts; Claim 22 also matches the PDF move paths. Two small corner cases use the original heel.

**Reconstructed turn-heel name:** replace `Parker Williams heel (turns)` with:

> Parker Williams turn bound (reconstructed heel)

**Reconstructed turn-heel audit line:**

> Reconstruction by constrained search, reported OPTIMAL. Claim 22 independently confirms 21 turns, 31 crossings, and the paper's endpoint pairing. Its moves differ from Figure 11's centre panel. Two small corner cases use the original heel.

Its current arithmetic caption can remain; the rates and same exits are verified. If the team instead adopts the template extracted above, recheck the rebuilt data before relabelling it as the printed heel.

**P40 audit line:**

> Shisheng Li's 4x40 block: Claim 22 independently checks 130 crossings and the pairing of five paper heels, plus full-tour samples. The demo uses the block on both horizontal bands where it fits.

Append to the P40 caption:

> A small board may have no room for a full block; at n=48 this step is the paper tour.

**H16a caption:** replace its first sentence with:

> We use a heel whose strand order differs within each paired lane group, then join the paths with searched 6x6 corner pieces.

The following 16/8 and 9n arithmetic can remain, with the global leading-term note. This states the construction without implying that the paper's search forbade other orders.

**FOLD caption:** replace all three current sentences with:

> Two diagonal folds and two centre lines divide the unmodified field into eight triangles of parallel moves. Boundary U-turns and arch flips contribute 5n+O(1) crossings. Cheap endpoint patterns force a mod-three corner charge; diagonal corridors contribute 4n/3+O(1). The completed tours have at most 19n/3+142 crossings for every even n>=96.

“Each corner has one extra square of one color” is not the audited reason for the charge and is false as an unrestricted corner-box statement: a box of even side length has balanced colours. The charge also includes unit-grid flux. Likewise “all moves are parallel” applies to the unmodified triangular field, not the added corridors and patches.

**Range note:** replace `This design needs n ≥ ...` with:

> This construction is certified here for even n ≥ ...

This avoids claiming nonexistence at smaller sizes.

**Footer crossing definition:** replace “Crossing = two moves of the tour whose line segments cross.” with:

> Crossings count unordered pairs of moves whose open segments intersect properly. A shared endpoint does not count; several pairs at one point count separately.

The turn definition is correct. The browser computes crossing pairs, even when their red dots coincide.

### Existing numbered audit references

| Step | Current reference | Check |
| --- | --- | --- |
| paper | Claim 21 | Correct for the heel figure and rates; Claim 22 adds direct PDF comparison and broader samples. |
| H16a | Claims 1,4,7 | Correct; Claims 4 and 7 close the all-size gap left in Claim 1. |
| LF4 | Claim 8 | Correct for all even n>=96. |
| FOLD | Claim 12 | Correct; Claim 21 also reviews the final proof. +24 is the count/reuse step, while the full matching repeats after +48. |
| T18 | Claims 3,4 | Correct; Claim 4 closes Claim 3's earlier conditional claim. |
| TT16 | Claims 6,7 | Correct for all even n>=48. Claim 16 supplies further hand-count checks. |

No numbered construction audit is falsely cited. The original, P40, and reconstructed heel steps now have the independent checks recorded in Claim 22; they should cite this claim rather than imply that a reported solver status is itself an independent certificate.

## Completion and scope

All computations used one CPU core, with the full-data JavaScript job and independent Python jobs run sequentially. `claim22_sources.json` records the audited source hashes. The local static-data audit is complete. No demo file, service, or worker file was changed.

Before release, fix the fraction formatter and chart labels, apply the caption corrections, and confirm the live page loads these files. The failed local HTTP request leaves that last delivery check open; it does not invalidate the local tour and count checks.

# Claim 23A — turns post, full-proof appendix (2026-10-02)

**Verdict: numerical and mathematical inputs PASS; completeness edits required.** The appendix gives the same lower and upper bounds as Claims 6, 7, and 16. All named commands passed, including both Lean commands. All sixteen printed corner grids are correct. The printed construction gives the same tours as the earlier independent audit. No change to either theorem bound is needed.

The remaining defects are definitions and scope, not a failed certificate: the strip sharpness example lacks its infinite-half-plane domain; the Lean explanation reverses the cross-product condition in a parenthesis; the retained graph and port ordering need exact definitions; and the all-n insertion argument should state why its cuts, phases, and outside connections remain valid for every larger n. There is also an unnecessary external existence theorem in part A. Exact replacements follow below.

`writeup/turns/main.tex` was not used as the authoritative text. I read the current post body and parts A--F in full.

## Independent checks of the appendix itself

`claim23a_independent.py` parses the printed alpha table, beta table, bottom template, and corner code grids directly from `post.mdx`. It does not import worker code.

- All **77** one-side local move pairs satisfy the four-column inequality.
- The printed corner tables have sixteen alpha values with sum **-7** and nine nonzero beta edges. All **209** legal corner move pairs satisfy the local inequality. Every one of the sixteen cells has a tight case. The slack histogram is 65,77,48,17,2 for slack 0,1,2,3,4, respectively.
- All **576** cells in the sixteen 6x6 corner grids match the corresponding move vectors in `TT16_res00.json`, `TT16_res02.json`, `TT16_res04.json`, and `TT16_res06.json`.
- For every residue, the four corner turn counts are **BL 21, BR 21, TL 20, TR 20**, total 82.
- The bottom counts are **3,1,2,2,1,3,2,2**. The top phase `(1-x) mod 8` gives the complementary counts. Their sum is four in every noncorner column.
- Applying the printed rules, including their override order, rebuilds all **28** tours for even n=48..102. Each is one closed knight's tour with **8n-14** turns, and every edge agrees with the graphs saved by the independent Claim 16 audit.
- The sharp corner witness still has residual **-7**, reciprocal internal edges, and no internal cycle. Its internal component sizes are 3,3,3,3,1,1,1,1. I rechecked it with the independent witness code.
- A fresh independent reduced-graph transport check passes for TT16 at n=96,98,100,102 and their +8 extensions. It compares every retained outside vertex and edge, not only the terminal matching. The three complete matchings agree with the printed table, including the return paths.

Files: `claim23a_independent.py/json/log`, `claim23a_transport.py/json/log`, and `claim23a_final_check.json`. The last file also records that no audited source changed during this audit.

## Named commands: clean-process results

I copied the Python checkers and their data to `w-verifier/claim23a_clean/`, preserving the repository paths. I ran them from that copy's root with a clean process environment, no PYTHONPATH, and the installed interpreter indicated by the appendix. The tour drawing script used the existing virtual environment for matplotlib. Its output stayed in the copied tree and its documented /tmp image paths.

The Lean commands ran in the existing `ktlean/` project, as the appendix directs, with its installed toolchain and dependency/build cache. This was not a fresh dependency installation. Each command ran sequentially; child processes were restricted to one CPU core. No author source was edited.

| Command | Result |
| --- | --- |
| `python3 w-turnstheory/check_proof.py` | PASS: 77 local cases; four generated-tour strip checks. |
| `python3 writeup/turns/check_corner.py` | PASS: 209 cases, alpha sum -7, every cell tight. |
| `python3 w-turnstheory/check_corner_certificate.py` | PASS: 209 cases, generated-tour checks, sharp witness and no internal cycle. |
| `.venv/bin/python writeup/turns/figures/tt16.py` | PASS: every even n=48..102, one cycle, T=8n-14, and an explicit assertion of 82 corner turns for each tour. It also writes its tables and figures. |
| `python3 w-turnstheory/check_upper_proofs.py` | PASS: 64 base tours and 48 regional transfers across TT16 and H16a; complete path coverage, compositions, enlarged blocks, and local costs. TT16 gains 64 turns per +8. |
| In `ktlean/`: `lake build` | PASS: build completed successfully. |
| In `ktlean/`: `lake env lean Axioms.lean` | PASS: the stated turns theorem has the stated domain; its axioms are exactly `propext`, `Classical.choice`, and `Quot.sound`. The 2-factor theorem and explicit 8x8 example have the same standard axiom set. |

All commands returned zero. Logs are `claim23a_clean/command_1.log` through `command_7.log`; commands and timings are in `claim23a_clean/commands.json`. The Python source snapshot and hashes are in that directory. The C4 report is written to **`w-turnstheory/upper_proof_checks.json`**, not to the repository root.

No listed command has a missing dependency in this environment, and none claims a result that its current output fails to support. In particular, C3 now asserts the corner count; the omission noted in the earlier write-up audit has been fixed.

## Exact completeness and scope corrections

### 1. Part A: remove an external theorem that this appendix does not prove

The assertion that a closed square-board tour exists if and only if n>=6 is even is a separate theorem. It is not needed here, and the appendix gives no proof or named check for it.

Replace:

> A closed tour of the `n x n` board exists if and only if `n >= 6` is even.

with:

> The construction below proves existence for every even `n >= 48`. We use `T_min(n)` only when at least one closed tour exists.

This keeps the main theorem self-contained without adding a proof of the small-board existence classification.

### 2. Part A: state the coordinate direction before “top” and “bottom” are used

Replace:

> Here `x` is the column and `y` is the row.

with:

> Here `x` increases to the right and `y` increases upwards; row zero is the bottom row.

All printed move codes and corner tables already follow this convention. Their grid rows run from top to bottom, as stated in part D.

### 3. Part B: restrict the sharpness example to its actual domain

The displayed pattern is reciprocal on an infinite half-plane. It is not a complete finite-board 2-factor: at the top and bottom it can leave the board. The sentence “every other cell” currently leaves this domain unstated.

Replace the whole paragraph starting “The rate of 2 per row is sharp” with:

> The local rate of 2 per row is attained on the infinite half-plane `x >= 0`, `y in Z`. Give column 0 the moves `(2,-1), (1,-2)`, column 1 the moves `(2,-1), (-1,2)`, and every cell with `x >= 2` the moves `(2,-1), (-2,1)`. These choices are reciprocal, and only columns 0 and 1 turn. This is a periodic side pattern, not a full finite-board tour. Away from its corners, the left side of the construction in part D uses this pattern.

The four-column lemma itself is correct for every finite-board 2-factor when n>=8.

### 4. Part B: fix the Lean parenthesis

Replace:

> `numTurns` counts positions `i` where the cells at `i - 1, i, i + 1` are not collinear (zero cross product), which is Definition 1 of the paper.

with:

> `numTurns` counts positions `i` where the cells at `i - 1, i, i + 1` are not collinear, equivalently where their cross product is nonzero. This is Definition 1 of the paper.

`KT.ClosedTour.IsTurn` is the negation of `Collinear3`. The printed formal theorem is otherwise faithful to the source and the new axiom report.

### 5. Part C: limit the consequence of the sharp -7 witness

Replace:

> So this method gives no constant better than 28.

with:

> Summing four independent bounds of this form cannot improve the constant 28. A stronger global bound could use further constraints between corners or charge slack outside the corners.

The witness leaves outgoing edges free. It does not prove that four tight corner witnesses can coexist in one finite tour. The body already states this scope more carefully.

### 6. Part D/F: give check C3 its name at first use

Replace the beginning “All checks of the moves:” in part D by:

> **Check C3 (construction and turn count):**

Keep the command and its description. The later C3 reference is otherwise resolvable, but the name is currently introduced only when part F refers back to it.

### 7. Part F: define the retained graph precisely

Replace the “Line labels” paragraph with:

> **Line labels and the reduced graph.** Retain every cell in the bottom and top bands of depth four, the left and right bands of depth two, and all four `6 x 6` corner squares. Every other cell has code `26`. Give each cell the label `c=x+2y`; those straight moves preserve `c`, and any knight move changes `c` by at most five. Suppress every maximal path whose internal vertices are not retained, replacing it by an edge between its retained endpoints. Keep parallel edges if they occur. No component can consist only of suppressed vertices: its moves follow a straight line monotonically and cannot close. This operation preserves the number of cycles. “Block cells” below means retained vertices of this reduced graph.

This avoids interpreting an “interior cell” as any cell with code 26, which would also suppress some band and corner cells. It also explains why suppression cannot remove a hidden component.

### 8. Part F: the block repetitions use different translations in different bands

Replace:

> Inside one range the side templates repeat when `c` increases by 8 (the bottom and top templates have period 8 in `x`, the left and right ones period 4 in `y`), so the blocks at cuts `a` and `a + 8` are translates with the same ports.

with:

> Within one range, increasing `c` by eight translates bottom and top band cells by `(8,0)` and left and right band cells by `(0,4)`. These shifts preserve the side templates. They also preserve the parity needed to solve `x+2y=c` at a fixed band depth. Thus the repeated blocks have the same named ports and the same reduced connections. They need not be translates by one vector in the original board.

The proof needs equality of the reduced structures; it does not claim that the entire two-band block is a rigid translate.

### 9. Part F: make the port numbering reproducible

Replace the two sentences starting “The ports of a cut are numbered” with:

> Orient each cut edge from its lower-label endpoint `u` to its higher-label endpoint `v`. Its description is `(band, depth(u), depth(v), c(u)-cut, c(v)-cut)`, where the band names are `B,L,R,T` in that lexicographic order and depth is distance from the corresponding board side. Sort these descriptions lexicographically and number them from zero. The checked lower and upper cuts have identical description lists. `L_i` and `R_i` denote the corresponding ports at cuts `a` and `a+8`.

The orientation of the two endpoints matters. The current text lists their depths and offsets without saying which endpoint comes first. The replacement is exactly the convention used by C4.

### 10. Part F: extend the chosen cuts explicitly to all n

After the matching table, insert:

> For every even `n >= 96`, use the same cut formulas: `a_0=35`, `a_1=8 ceil((n+32)/8)`, and `a_2=2n+32`. They satisfy `a_0+8=43<n-24`, `n+32<=a_1<=n+39` and `a_1+8<=n+47<2n-24`, and `a_2+8=2n+40<3n-24`. Thus every chosen block stays strictly within its band-pair range. The residue of each cut modulo eight depends only on `n mod 8`. The four checked base sizes therefore cover every template phase used by this induction.

This makes clear why checks at 96,98,100,102 suffice for the finite port types. The geometric repetition, not sampling larger boards, is the all-n step.

### 11. Part F: define the map only on the outside of the inserted blocks

Replace:

> Move each side-band cell by the vector below, where `r` in `{0, 1, 2, 3}` is the number of insertions before its label:

with:

> For a retained cell outside the three old blocks, put `r = #{j : c >= a_j+8}`. Move each such side-band cell by the vector below. Fill each doubled block with two consecutive copies of its periodic reduced pattern.

The shift table itself is correct. It does not define the duplicate copy of an old block, so applying it without this outside restriction is ambiguous.

Replace the sentence listing the four corner shifts with:

> The BL, BR, TL, and TR corner squares move by `(0,0)`, `(8,0)`, `(0,8)`, and `(8,8)`, respectively. On cells shared with a side band, these corner shifts agree with the side-band table. The same corner codes apply because `n mod 8` is unchanged.

### 12. Part F: state the connection and coverage argument, not just its conclusion

Replace “Each interior line still joins the same two ports; only its length changes. So the result is exactly the reduced graph of the tour for `n + 8`.” with:

> The two ends of each suppressed straight path have the same label. Outside the inserted intervals, both endpoint shifts add the same `8r` to that label. At fixed band depth, the equation `x+2y=c`, with its parity, fixes the line endpoint. The shifts preserve both depth and parity, so the endpoint pairing is unchanged. The cut margins keep every block away from the corners and from a change of band pair. Non-suppressed cut edges keep their move and port description because the adjacent template phases agree. The remaining new interior cells lie on the extended straight paths; such a path cannot contain a separate cycle. Together with the repeated blocks, these cells account for the whole enlarged board. Hence the constructed graph is exactly the reduced graph specified by part D at size `n+8`, with reciprocal legal edges and degree two.

This is the same argument audited in Claim 7. It belongs in the appendix because the reader is not assumed to have that report.

### 13. Part F: give the report's actual path

Replace:

> It writes the ports and matchings to `upper_proof_checks.json`.

with:

> It writes the ports and matchings to `w-turnstheory/upper_proof_checks.json`.

The named checker passes as written. Its actual larger-block check traces the full cell slab; this is stronger than checking only the suppressed paths, because it also accounts for every straight interior cell.

## Body versus appendix

The body agrees with the appendix on the domains n>=8 and even n>=48, the four-column inequalities, the two constants 28 and 14, the sixteen corner grids, the top phase, the exact turn count, and the conservative induction threshold n>=96. The displayed n=48 count 370 is correct. The old record of independent rebuilds through 134 and at 312,314,316,318 is the Claim 6 record; it is not being inferred from the new C3 range. The appendix's 96--102 induction bases are a valid later threshold, not a conflict with the earlier audit's smaller bases.

The body claim “and no better rate in the tested sizes” is a search-history claim, not a conclusion of the appendix's certificates. For a proof-focused version, replace:

> It found a piece with 18 turns per 8 columns, and no better rate in the tested sizes.

with:

> It found a piece with 18 turns per 8 columns.

This retains the audited result without implying that the reader's checks certify the search optimum. No upper-bound optimality claim is needed.

The body sentence that there is one of fifteen possible integer turn counts follows from the interval and is correct. The local -7 sharpness statement in the body already says that outgoing edges are free. The body link to `#details` resolves, and Details now points to the appendix. All A--F proof references resolve after the explicit C3 label above. The public repository location remains a TODO: fill it before publication so outside readers can obtain the named check scripts. That is a release-link task, not a mathematical gap.

## Final scope

The appendix can support the full self-contained claim after the definitions and insertion explanation above are made explicit. The finite data, Lean statement, and all constants agree with the audited sources. No unresolved numerical mismatch remains.

No post text, proof source, corner file, or service was edited. The remaining action is for the author to apply the exact replacements and supply the public repository link. Claim 23A is complete; the crossings appendix has not been audited in this claim.


# Claim 23B — crossings post, full-proof appendix (2026-10-02)

**Verdict: both mathematical bounds PASS. The appendix needs completeness and scope edits before release.** The finite certificates agree with Claims 9, 12, 19, 20 and 21. The explicit bounds remain `X <= 19n/3 + 142` for every even `n >= 96`, and `X >= 14n/3 - 407` for every closed tour with even `n >= 32`.

The main defects are an omitted statement of the Lean scope, an incomplete description of the strip scan, and an unsupported assertion that all component-to-cut margins are fixed. The margins can also increase. An exact affine check establishes the condition needed for every growth step. There are also incorrect output-file paths and a claimed text output that the command does not create. Exact replacements follow below. No author source was edited.

## Sources and reproduction

I read the whole post, including its body and both appendices. I compared the appendix with the two proof documents and the sources of its check commands. The requested `w-turnstheory/APPENDIX_STATUS.md` is absent. This does not prevent the audit: the appendix and its actual dependencies are present.

The snapshot is in `w-verifier/claim23b_clean/`. It includes the post, proof sources, checker sources, twelve base files, and 36 saved tours. `sources.json` records their SHA-256 hashes. `changes_since_claim21.json` records the comparison with my Claim 21 snapshot. Every named checker and its strip dependency is unchanged from that snapshot. `PROOF_fold.md` is also unchanged. The lower proof has the Claim 21 wording repairs: it defines the endpoints in the flux identity, corrects the possible endpoint columns, states the degree requirements, and restores the corner overcount argument. No changed numerical certificate was found.

I ran the following seven distinct commands from a fresh copied project root, with a clean environment and the system Python. The jobs were sequential and restricted to one CPU core. No solver was used. Repeated appearances of the same command in the appendix do not require separate runs; the combined lower runner also reran its five checks.

| Command | Result |
| --- | --- |
| `python3 w-turnstheory/check_knight_tiles.py` | PASS: 1,292 edge pairs; maximum two common quarters; 648 single-edge flux checks. |
| `python3 w-turnstheory/check_corner_box.py` | PASS: eight nonzero end-flux coefficients, degree-two identity, and both parities of the outside charge. |
| `python3 w-turnstheory/check_col0_squares.py` | PASS: 20 normalized crossing pairs; the unique inward overlap type; five possible duplicate pairs per corner; 330-state boundary potential. |
| `python3 w-turnstheory/check_square_defects.py` | PASS: the alternating identity and at least two bad quarters in each defective square. |
| `python3 w-turnstheory/check_lower_stability.py` | PASS: 82,516 base states / 144,674 arcs; 167,782 augmented states / 315,389 arcs; potential range `[-29,0]`; overcount 1,104. |
| `python3 w-turnstheory/check_crossings_lower.py` | PASS: all five lower checks and the final arithmetic. |
| `python3 w-turnstheory/check_fold_proof.py` | PASS: all 36 saved tours, complete matchings, both states, local and total counts, and step-12 counterexamples. |

The full logs are `command_1.log` through `command_7.log`; `commands.json` gives exits and times. All exits are zero. The commands work without a solver, installed project package, or `PYTHONPATH` setting.

## Independent checks and mathematical scope

I reran my own geometry and endpoint code, my own strip graph and potentials, my own fold assembler and exterior-graph transport test, and the exact affine margin check. These programs import no worker construction or checker code. The extra run log is `extra_commands.json`. My stability program uses the existing project virtual environment because an older independent helper imports NetworkX; the appendix's seven commands need only the standard library. An initial attempt to run this extra program with the system Python stopped at that missing import. It did not find a mathematical failure.

- `claim23b_geometry.py/json` checks all eight knight directions and four translation parities against 200 dual steps, the complete coefficient identity, and the outside-box flux at both parities. It passes.
- `claim23b_stability.py/json` rebuilds 82,516 base states and a separate 184,006-state / 343,631-arc augmentation. Potentials for up, down and joint tests all have range `[-29,0]`. Its exact period-one witness has two crossings and one failed row per period. It passes. The larger augmented state count comes from retaining all relevant row edges, not just the watched test edges.
- `claim23b_fold.py` independently rebuilds 48 tours: the 36 saved sizes and twelve larger sizes `288,290,...,310`. All are single closed tours. It checks every stored edge at the saved sizes, all full port lists and returns, both side states, 36 complete exterior-graph transports, crossing counts, and twelve step-12 graphs. It passes. Results are in `claim23b_fold_results.json`.
- `claim23b_margins.py/json` checks 36,288 component-to-block inequalities as exact affine functions of `k`, together with board and branch bounds. It proves these inequalities for every integer `k >= 0`, not only sampled sizes. It passes. The current script is self-contained apart from the twelve base JSON files.
- `claim23b_text_checks.py/json` parses the eight printed coefficients directly and compares them with the independently audited test. It checks the exact constants. It passes.

The largest fold offset is 142, at base 114. Each +24 adds 152 crossings. The three complete matching types in A.3 are correct, including both same-cut returns of the six-port corner. Both parity states close each of the twelve outside matchings into one cycle. The completion from base 100 has three cycles when reused at 112 with step 12; this does not refer to the separate valid saved base-112 tour.

The lower argument keeps every charged square inside `D`. Its joint test includes the exceptional-pair exclusion required for whole squares. The near and far scan intervals are disjoint. A failed side-row can remove at most one candidate path. The boundary sets have at most five duplicates per corner, and the width-two strip overcount is at most 1,104. There is no double charge of a square, a retained path, or the `4n-2` area term.

I also ran `lake env lean Axioms.lean` from `ktlean/`, on one CPU core with the existing toolchain and compiled library. It passed. The printed theorem agrees with the source statement quoted below. The reported axioms are only `propext`, `Classical.choice`, and `Quot.sound`. This run checks the existing Lean environment; it is not a fresh toolchain installation or a rebuild of every dependency.

The exact chain is

```
E = X - 4n + 2,
|B| >= 4n - 24,
2L <= 4E + 44,
L >= 2n - 60 - b,
b <= E + 1131,
4n <= 4E + 2b + 164 <= 6E + 2426,
X >= 14n/3 - 1219/3 >= 14n/3 - 407.
```

These statements agree with Claims 19--21. The tile proof of `4n-2` also applies to a spanning 2-factor. The stronger proof uses the forest strip model and therefore has the stated Hamiltonian-tour scope.

## Required replacements

### 1. State the computational input and the exact Lean scope

The appendix names no Lean theorem or Lean command. It also does not plainly distinguish the finite stability input from the part formalized in Lean. Add the following after the opening paragraph of part B:

> This proof uses the strip stability lemma in B.5 as a computer-certified input. The named Python checker constructs the finite graph and checks every integer potential inequality; it does not assume an unverified solver answer. Lean proves `KT.ClosedTour.four_mul_sub_two_le_numCrossings` without a stability hypothesis. The stronger Lean theorem `KT.ClosedTour.fourteen_mul_le_of_stability` takes the explicit hypothesis `card(badRows) <= X - 4n + 2 + C` and concludes `14n <= 3X + C + 132`. With `C=1131`, that statement gives `X >= 14n/3 - 421`. The sharper constant 407 in this appendix follows from the argument and Python certificates below; it is not the constant in that Lean theorem.

Add a root-relative Lean check command with this note:

> With the project's Lean toolchain and dependencies installed, the following command checks the theorem statements and prints their axioms:
>
> `cd ktlean && lake env lean Axioms.lean`

The current Lean statement uses its own rotated side frames and `badRows` set. Its far scan range is `[h+2,2h-14]`; the appendix uses fixed side frames, the joint test, and `[h+3,2h-13]`. These are different conventions. Do not describe the two finite row sets or final constants as literally identical. The Lean result has only the stated stability hypothesis; it does not assert that the Bellman-Ford certificate has been checked inside Lean.

### 2. Specify the quadrant frames in A.1

After “Write `h=n/2` and `R(x,y)=(n-1-y,x)`.” add:

> Use rotation index `r=0,1,2,3` on the bottom-left, bottom-right, top-right, and top-left quadrants, respectively. The left and bottom halves have coordinates less than `h`; the other halves have coordinates at least `h`. Rotating back means applying `R^(-r)`.

This fixes the quadrant boundaries and the rotation used by every later placement rule.

### 3. Make the all-size cut margins explicit in A.2

Replace “Component shapes and the relative cut margins are fixed; checking the margins at `n0` therefore checks them for every `k`.” with:

> Put `h0=n0/2`. The corner upper cut is `30+12k = h-(h0-30) <= h-18`. The side upper cut is `h+22+12k = n-(h0-22) <= n-26`. In a corner block, `max(2x-y,2y-x) >= max(x,y)`, so the block stays away from the quadrant axes. In a left-side block, the lower cut `h+16` implies `x <= h-16`, so this block stays away from the diagonal corridor. The rotated bounds are the same. For each copied component cell, the board coordinates and cut labels are affine functions of `k`. Each required separation from a forbidden block is nonnegative at `k=0` and has nonnegative coefficient of `k`. Thus each separation stays nonnegative for every `k >= 0`. The component shapes stay fixed, but some separations increase.

Add a finite check for the last assertion:

```sh
python3 w-verifier/claim23b_margins.py
```

This small standard-library checker is now available. Include it with the released certificate files, or move the same affine assertions into `check_fold_proof.py` and name that updated command. The current fold checker extracts cuts at `k=0,1,2`; it does not itself check the signs of all affine coefficients. The general inequalities above and the affine check supply that missing reproducible fact.

Also replace “It cannot cross a diagonal fold without meeting the retained corridor.” with:

> It cannot cross a diagonal fold without meeting the retained corridor: the corridor contains the three integer transverse positions `y-x=0,1,2`, while a knight step changes `y-x` by at most three. The finite components cover the corridor ends and the central junction.

### 4. Define the port order fully in A.3

Replace the paragraph starting “To number ports, orient a crossing edge” with:

> To number ports, rotate the block to its bottom-left or left reference frame. Write a cut edge as `(u,v)` with the label of `u` less than the label of `v`. Its name is `(tag, depth(u), depth(v), label(u)-cut, label(v)-cut)`. Sort names lexicographically and number them from zero, separately at each cut. For a corner, use tag `L` if both endpoint x coordinates are at most two, otherwise `B` if both endpoint y coordinates are at most two, and otherwise `D`. The corresponding depths are x, y, and `y-x`. For a side, use tag `lo` if the lower-label endpoint has `y<h`, and `hi` otherwise; its depth is x. The complete sorted lists are in `w-turnstheory/fold_proof_checks.json`.

The current short description gives the ingredients but omits the index origin, sort convention, and exact tag choice used by the matching table.

### 5. Correct the output paths and the absent text output

In the opening paragraph of A, replace the sentence ending “in `fold_proof_checks.json`.” with:

> Complete port lists and matchings, including the outside matching, are in `w-turnstheory/fold_proof_checks.json`, which the command generates.

In A.5, replace “It writes `fold_proof_checks.json`; the run output is `fold_proof_checks.txt`.” with:

> It writes `w-turnstheory/fold_proof_checks.json` and prints its checks to standard output.

The named command does not create a `.txt` file. In B.7, replace “It stops on any failure and writes `crossings_lower_checks.json`.” with:

> It stops on any failure and writes `w-turnstheory/crossings_lower_checks.json`.

### 6. Define the side coordinates and the finite scan precisely

In B.1, replace “with `x` the column and `y` the row” with:

> with `x` increasing to the right and `y` increasing upwards

In B.5, replace “At each cell choose edges to later cells so that its final degree is two in columns `0,1` and at most two in columns `2,3`.” with:

> At each cell choose only legal knight edges to later cells that have at least one endpoint in columns `0,1`. Require final degree two in columns `0,1` and at most two in columns `2,3`.

Replace the sentence defining the width-one scan with:

> The width-one scan in B.4 uses columns `0,1,2`, allows only edges incident to column `0`, requires degree two in that column, and allows degree at most two in the other two columns.

The earlier instruction to keep boundary-incident edges suggests this restriction, but the transition definition must also state it. The checker excludes inner-to-inner edges. A reader who generates all knight edges on the stated three or four columns gets a different graph.

After the sentence defining transition weight `w`, add:

> Count a new edge's proper crossings with the other new edges and with the still-pending edges, once per unordered pair. An edge whose two endpoints were already processed cannot cross a new edge, since every knight edge has nonzero vertical displacement and the scan processes rows in order.

Replace “Every test edge straddles that row, so these data suffice.” with:

> Every test edge has minimum row at most the test row and maximum row at least the test row. Thus it is either pending at row start or is selected while processing that row; these data suffice.

Some test edges only touch the test row at an endpoint. The inclusive condition matters for the row-end test.

### 7. State the potential telescoping step

In B.5, replace “Summing over the strip walk proves” with:

> For each arc `u -> v`, `p(u)` and `p(v)` are the potentials of its endpoint states. Summing the inequalities over the `4n` transitions gives `4X_sigma-4n-4b_sigma >= p(end)-p(start) >= -29`. Hence

The displayed inequality that follows can stay. This makes the endpoint allowance explicit and removes the undefined arc variables in the formula.

### 8. Make the free-fold argument explicit

In A.4, replace the sentences starting “At a free fold” and ending “shared endpoints.” with:

> At an axis fold, use the integer coordinate normal to that axis. At a diagonal fold, use `y-x` in its local frame. Each relevant field edge changes that coordinate by one unit in the same direction on both sides of the fold. Within each open unit slab all field edges are parallel. Edges in different slabs have disjoint interiors in that coordinate and can meet on a slab boundary only at endpoints. Thus the free fold has no proper crossing.

This is the geometric argument used in Claim 12. The current phrase “each family remains on its own side” does not explain the edge that crosses the fold or why it cannot cross another edge.

## Post body agreement

The theorem callout and the minimum interval have the correct size ranges. The ratios are explicitly leading-coefficient ratios. The body now treats 19n/3 as an upper bound and rejects an unproved optimum for the whole fold family. The 9n heel arithmetic, the 343n/48 progression, and the 720-crossing tour at n=96 agree with the audited record. The two inequalities `E >= n-b/2-41` and `E >= b-1131` agree exactly with B.6. The fixed allowance in the bad-quarter budget is now stated. The captions distinguish a periodic average from a separate charge for each row.

Two body replacements are still needed:

**Charge definition.** Replace the paragraph starting “The tool is a charge.” with:

> The tool is a charge. Colour the cells black and white, like a chess board. Orient both the tour moves and all unit grid edges from black to white. Along a path through unit-square centres, add their signed crossings from the path's left side to its right side, modulo 3. The exact rule is in the [details](#details).

The current paragraph mentions only tour moves. Their flux alone is not the charge with the two properties listed next. The unit-grid contribution is essential, including along the outside corner boundary.

**Five-step overview.** Replace item 1 with:

> 1. Each knight move owns a small tile. Their total area exceeds the area between the board's cells by `2n-1`. This gives the tile bound `4n-2`.

Replace item 3 with:

> 3. At each corner, a nested path is charged when both of its end rows pass the endpoint test. There are about `n/2` candidate paths per corner.

The current item 1 says the tiles almost cover the board exactly once, which need not hold for an arbitrary tour with many crossings. The current item 3 states the charge without its endpoint condition. The later sections already give the correct conditions.

The internal links to Details and to appendix parts A and B resolve. There is no public source download link in the post. Before publication, add the actual repository or archive link with the named scripts, their dependencies, the twelve bases, and the 36 tours. No external proof from FINDINGS or TILE_INPUTS is needed after the replacements above; the files serve as certificate data and check implementations.

## Final scope

The numerical results and all seven named commands pass. The all-size insertion argument and the lower-bound charging argument agree with the audited record after the explicit definitions and margin statement above. The exact sentence replacements distinguish the computer-certified stability input from the conditional Lean statement. No bound needs to change. The remaining action is for the writer to apply these replacements and include the named certificate files in the public source bundle.


# Claim 23A closeout — 2026-10-02

**Verdict: PASS. All Claim 23A corrections are closed.** I compared the current `writeup/turns/post.mdx` with the saved Claim 23A version and checked all thirteen numbered replacements. Every replacement is present as requested; the only literal variation is straight versus curly quotation marks. The body search-optimum sentence was also corrected. The requested repository URL, `https://github.com/nmamano/knights-tour-bounds`, appears in both the body and appendix. This confirms the links in the file, not the current public repository contents.

The full diff contains no other meaning change. All fenced blocks, including the sixteen corner grids and the Lean statement, are unchanged. All named checker sources, corner files, and other certificate inputs are byte-identical to the Claim 23A snapshot. Evidence: `claim23a_closeout.diff` and `claim23a_closeout_check.py/json`.

All seven named commands passed again, sequentially on one CPU core: the local lemma check, both corner checks, the TT16 builder for all even n=48..102, the upper-proof checker, `lake build`, and `lake env lean Axioms.lean`. Python checks ran in a fresh copied project with a clean environment; Lean used the existing project toolchain. The turns theorem reports only `propext`, `Classical.choice`, and `Quot.sound`. Logs, source hashes, and exit codes are in `claim23a_closeout_clean/`. No source changed during the check.

The bounds remain `8n-28 <= T_min(n) <= 8n-14` for every even n>=48, with the lower bound retaining its stated wider scope. No author source was edited. No further Claim 23A action is required.

# Claim 23B closeout — 2026-10-02

**Verdict: PASS. All Claim 23B corrections are closed.** I read `w-turnstheory/APPENDIX_STATUS.md` and compared the current crossings post with the saved Claim 23B snapshot. Every quoted replacement in numbered sections 1--8 is present verbatim, including the Lean scope and command. All three body replacements are also present. The requested `https://github.com/nmamano/knights-tour-bounds` link appears in both Details and the appendix. This confirms the links in the local file, not the public repository contents.

The full diff has no unrelated meaning change. The added margin command and its output description correctly reflect the new checker. The two bounds, their size ranges, all tables, and the lower-bound certificate inputs are unchanged. Among the previously snapshotted source and data files, only the post and `check_fold_proof.py` changed. The latter adds only an import and call to the new margin check before its existing checks.

`w-turnstheory/check_fold_margins.py` is stronger than my `claim23b_margins.py`. Its affine helpers and all original margin assertions are identical. It adds assertions that each base has exactly 13 components and 1,008 component cells. The other changes are the root-relative input paths and its output path. I checked the source and compared the function syntax trees after removing only these path changes and the two added assertions. The checker uses only the standard library and twelve base files; it has no verifier dependency.

Both requested commands passed from a fresh copied project root with a clean environment, sequentially on one CPU core:

- `python3 w-turnstheory/check_fold_margins.py`: all 36,288 affine inequalities passed.
- `python3 w-turnstheory/check_fold_proof.py`: the new margin check and all existing 36-tour, matching, crossing, and step-12 checks passed.

The generated margin report is identical to my independent Claim 23B report. The full fold report is identical to the original Claim 23B report. No source changed during this closeout. Evidence is in `claim23b_closeout.py`, the two `claim23b_closeout_*.diff` files, and `claim23b_closeout_clean/` (hashes, literal-text checks, command logs, report comparisons, and exits).

No author source was edited. No further Claim 23B correction is required.

# Claim 24: G1 same-edge free-fold nests — 2026-10-03

**Verdict: GAP as written. PASS for the corrected net-step theorem and its reflection linear part. FAIL for a literal ban on seven total folds. GAP for the general defect-cost consequence.**

I read `gap/BRIEF.md`, G1 in `gap/structures/FINDINGS.md`, its full `turning.py`, LB F3/F10/F13/F14, and Structures S8/S9. This is a light audit, with no solver and no change to an audited numerical bound. The audited G1 SHA-256 is `e78239dee547be28346117519b559a2406af38dab6ea7c206d0de0a666801637`; its script SHA-256 is `c4bc5143465421e149dba6510060ae461020fe13a6f8f2149b61180b93f4716f`.

## Correct statement and all-length proof

Replace the statement with:

> Let P be a finite polygonal arc made of knight moves, with no geometric self-intersection, from A=(0,a) to a distinct B=(0,b), contained in x>=0. Its first direction is (2,1), its last direction is one of (-2,1), (-2,-1), and every nonstraight transition is a free fold on the stated eight-direction cycle. Orient the cycle as printed in F10a. Then b>a, the last direction is (-2,1), the total tangent rotation is 180 degrees minus 2 atan(1/2), and the signed net step count on the cycle is +1.

Here atan is expressed in degrees. A path that is simple as a graph can have geometric crossings; that weaker meaning of simple is insufficient. Straight moves contribute zero rotation and zero cycle steps. Put the free-fold assumption in the first sentence: without it, the first assertion of G1 is false. For example, the simple knight arc `(0,2),(2,3),(4,2),(2,1),(0,0)` starts in (2,1), ends in (-2,-1), and returns below its start.

1. Close P by B to A on the boundary if P meets that segment only at its endpoints. Otherwise use the outside detour `B -> (-epsilon,b) -> (-epsilon,a) -> A`, with epsilon>0. This detour is disjoint from P. In both cases the closed polygon is simple. Its rotation is +360 degrees for b>a and -360 degrees for b<a. Thus the argument works even if P has other contacts with x=0. The direct boundary closure in G1 requires the extra contact condition.

2. Write theta=atan(1/2), so 0<theta<45 degrees. Subtracting the closing turns gives this exact table. The outside detour gives the same table as the direct closure.

| End direction | b>a | b<a |
| --- | --- | --- |
| (-2,1) | 180-2theta | -180-2theta |
| (-2,-1) | 180 | -180 |

3. The eight positive cycle increments alternate between `180-2theta` and `90+2theta`. Their total is 1080 degrees. Reverse steps give the negatives of the same increments. Lift a direction walk to the integer line of cycle indices. A potential on this line shows that its rotation depends only on its net displacement k, even if the walk goes around the cycle many times. For every integer m, including negative m,

```
R(2m)   = 270m,
R(2m+1) = 270m + 180 - 2theta.
```

4. Every positive increment is positive. Thus k>=2 gives R(k)>=270; k<=-2 gives R(k)<=-270. Every entry in the steep-end table is strictly between -270 and 270. Only k=-1,0,1 remain. Their endpoints are respectively (-1,-2), (2,1), (-2,1). Only k=1 is a steep left-facing endpoint, and its rotation selects b>a. This proves the result for arbitrary length. Enumeration through length 11 is not the all-length proof.

This closes the four-fold spiral lead of S9 and upgrades the corresponding exclusion in LB F14a from measurement to proof. It does not prove a lower bound on the arch term.

## Total folds versus net steps

Four total folds in a return with the stated steep ports would require net displacement +4 or -4; both are excluded. A reduced seven-step return is also excluded. But seven total folds can have net displacement +1.

A counterexample to the literal seven-fold ban has these successive leg endpoints:

```
(0,0), (8,4), (6,5), (8,6), (6,7),
(8,8), (6,9), (8,10), (0,14).
```

Subdivide each leg into knight moves. The directions alternate between (2,1) and (-2,1); the leg lengths in moves are `4,1,1,1,1,1,1,4`. There are exactly seven horizontal free folds. Every move increases y by one, all intermediate vertices have x>0, and the path is geometrically simple. Its cycle word is `+,-,+,-,+,-,+`, of net +1. Horizontal layers with these alternating directions are free-fold fields, so this example is not just an abstract word.

Replace the title by **“A simple free-fold same-edge return with steep ports has net cycle step +1.”** Replace each unqualified “7-fold” exclusion by “seven net cycle steps” or “a reduced seven-step walk.” Extra cancelling pairs remain possible.

## Script check

`python3 gap/structures/turning.py 11` ran successfully on 2026-10-03. Its arithmetic and enumeration are correct. However, `left = [d for d in CYC if d[0] < 0]` includes shallow ends. The actual output contains three cases:

| End | Position of B | Net steps | Walk count, lengths 1 through 11 |
| --- | --- | --- | --- |
| (-2,1) | above | +1 | 637 |
| (-1,-2) | below | -1 | 637 |
| (-1,2) | below | -2 | 286 |

Thus its final list is `[-2,-1,1]`, not `[1]`. To make its output match the theorem, filter both the printed table and the enumeration to `d in {(-2,1),(-2,-1)}`. Or retain the broader output and state explicitly that only the steep-end case is relevant. The script enumerates direction words, not geometric embeddings. A hit is a necessary rotation condition, not a proof of a realizable nest. The script currently prints results without assertions.

The independent standard-library check `gap/verifier/claim24_check.py` rebuilds the free-fold graph from the integer-normal equations `n.u=n.v=1`, verifies the exact symbolic rotation formula for all words through length 11, reproduces the three counts, and checks the seven-fold counterexample. It imports no worker code. Exact angle coefficient pairs decide equality; floating point only selects principal angle branches. The all-length result is the proof above. Commands:

```sh
python3 gap/structures/turning.py 11
python3 gap/verifier/claim24_check.py
```

Both ran as light single-process jobs. The saved outputs are `gap/verifier/claim24_author_output.txt` and `gap/verifier/claim24_check.json`.

## Reflection consequence and remaining gap

The composite fold isometry has linear part `(x,y) -> (x,-y)`: PASS. To make this explicit, reflection in a fold line sends the incoming direction to the negative of the outgoing direction. An arc of net step +1 has an odd number of folds. Therefore the linear part sends (2,1) to -(-2,1)=(2,-1). It is an orientation-reversing orthogonal map, so it is the horizontal reflection. Hence the full isometry has the form `g(x,y)=(x+t_x,-y+t_y)`, a horizontal reflection or glide reflection.

The remainder of G1 does not follow from this result. Cancelling opposite cycle steps cancels rotation, but reflections in parallel lines at different positions leave a translation. This explains how a glide can remain. It does not show that each algebraic pair is a separate physical corridor with the hypotheses of S8. Also, a nonzero glide need not have odd shift; nor does odd integer current alone imply nonzero current modulo three (a current of 3 is odd). S8 itself allows a free current of plus or minus 3 along a jog band.

To prove the claimed general cost consequence, supply a geometric decomposition into corridors, check the uniform exterior and strand hypotheses needed for the S8 parity argument, and prove an endpoint charge budget that permits cancellation between corridors and does not count an endpoint twice. No such argument is in G1 or `turning.py`. Replace that part by:

> The net-step theorem rules out reduced four-step and seven-step steep same-edge returns. It allows additional fold pairs and a horizontal glide. Whether every such glide forces a defect structure, and what total crossing cost those structures require, needs a separate proof.

No author file was edited. Claim 24 is complete. The next action is for Structures to apply these statement and scope repairs; the general defect-cost claim remains open.

# Claim 25: fractional endpoint strip limit — 2026-10-03

**Verdict: PASS for the four requested results, with the precise model and proof details below. The endpoint-table route has optimal coefficient beta=1. It does not improve the crossing lower bound 14n/3-O(1).**

I checked L1 in `gap/lowerbounds/FINDINGS.md`, the source of both fractional certificate programs, both explicit obstruction programs, and Sections 11.1--11.4 of `w-turnstheory/FINDINGS.md`. This audit concerns the stated side-strip relaxation and the same residue test. It does not assert that the blocking strips extend to a closed tour, or that they obstruct a different global lower-bound method. Source hashes are in `gap/verifier/claim25_check.json`.

## 1. Beta=1 and C=29/4: PASS

There is a short verification that uses the already audited certificate. Let b be the old oriented failure flag: b=1 if F is not 2 modulo three or the inward exception is present. For either parity, F=2 and no exception give h=2 and a=0. In every other case a<=1=b. Thus `a<=b` for each row and each orientation, including arbitrary initial parity.

Claim 23B independently checked integer potentials of range `[-29,0]` for the up, down, and joint binary tests. Its report `w-verifier/claim23b_stability.json` and run log `w-verifier/claim23b_clean/extra_2.log` agree. On each arc that certificate satisfies

```
4w - 1 - 4b + p(u) - p(v) >= 0.
```

Replacing b by a only increases the left side. Lift the state to include row parity; keep the same potential. On a walk of N complete rows, telescoping gives

```
X_strip - N >= sum_rows a - 29/4.
```

This proves the requested beta=1, C=29/4 result for both orientations and both initial parities. It also covers subwalks that begin at an internal row state, as needed for the eight half-side walks in 11.3. The constant is a valid error bound; this audit does not claim it is the smallest possible one.

The source of `frac_independent.py` correctly initializes pending test edges at row start, adds newly selected edges once, reflects the full test for the down orientation, charges `t=2a` only at row end, toggles parity, and uses integer weight `q(4w-1)-2pt`. Both parity choices are seeded at all base row states. Its finite graph and Bellman-Ford construction are sound. `frac_stab.py` uses the same charge with a larger accumulator graph; its extra accumulator states strengthen the check. Both base graph source files are byte-identical to the copies audited in Claim 23B.

I read the supplied convergence logs but did not rerun the large fractional graph searches or check the saved NumPy arrays. The office load was above 10 throughout these checks, so I used the stronger prior certificate and the independent 12-case local dominance check. This is a proof of the requested inequality, not a claim of a fresh run of the two fractional implementations.

## 2. Period-four obstruction: PASS

The given field has one long edge at each cell in columns 0 and 1. Its short edges pair every such cell exactly once. Consequently those columns have degree two and the two ghost columns have degree one. Every component has one short edge and two long edges ending at ghosts, so the infinite field is a forest. This proves acyclicity for all rows, beyond the finite unroll used by the script.

There are exactly eight proper crossing pairs per four rows, counted once by the later of the two lower endpoint rows. Thus a period has X_strip=8 and excess X_strip-4=4. There is no inward exception. For the printed field, the up test with phase 0 has h=1 at every row; the down test with phase 1 does too. Each period therefore has sum a=4. A proposed coefficient beta>1 gives period weight

```
(X_strip-4) - beta*sum a = 4(1-beta) < 0.
```

Repeating the field defeats every fixed endpoint error C. Translating the field by one row supplies the other initial parity in each orientation. The independent check tests all four orientation/parity cases. It also gives finite starting caps for both translates in width two: they change only rows 0 through 6, have valid degrees and no cycle, and then join the periodic field. Thus the obstruction is reachable from the empty strip scan; it is not merely a cycle in an unreachable state component.

The author script correctly establishes an obstruction for one phase in each orientation, which already defeats a certificate required to cover both phases. Add the one-row translation argument when claiming the result separately for either fixed initial parity.

## 3. Any common additive table a_c(h): PASS with the following explicit proof

The scope is a table used to bound the discarded-path indicator by the sum of its two endpoint entries, with the same table at both ends and with c the parity of the common radius. In the no-exception case, the lost pair (1,2) requires

```
a_even(1)+a_even(2) >= 1,
a_odd(1)+a_odd(2) >= 1.
```

The cheap field has h=2 at every row and zero excess. A valid strip certificate with beta>0 therefore requires

```
a_even(2)+a_odd(2) <= 0.
```

Summing the first two inequalities now gives

```
a_even(1)+a_odd(1) >= 2.
```

The blocking field has h=1 at every row, with equal numbers of even and odd rows, and excess one per row. Its mean table penalty is at least one, so beta<=1. This proof even allows signed table entries, provided the stated loss and strip inequalities hold.

L1 instead says the cheap pattern forces each a_c(2)=0. That pointwise conclusion needs a nonnegativity step: for an ordinary nonnegative penalty table it follows immediately; it also follows from requiring the loss inequality for the retained pair (2,2), since `0<=2a_c(2)`. State that step, or replace the paragraph by the averaged proof above. The averaged proof is enough and avoids any added assumption.

An exception-dependent extension of the table cannot evade this obstruction: the witness and cheap field both have no exception. This is a limit of this residue-based additive loss bound, not of all possible endpoint data, joint corner tests, or nonadditive bounds.

## 4. Every fixed wider strip: PASS

For S_k, k>=2, the full long-edge family can be written

```
(x,y)--(x+2,y-1),  0<=x<=k-1,
```

together with exactly the same short joins between columns 0 and 1. All long edges lie on parallel lines x+2y=constant. Cells in columns 2 through k-1 have one long edge toward smaller x and one toward larger x. Each ghost cell has only its edge toward smaller x. Each cell in columns 0 and 1 keeps its long edge and one short join. These statements give the required degrees for every k, including odd k.

Each component consists of one short join and two long chains. Moving away from that join increases x by two until a ghost column is reached. The chains cannot merge: distinct chains have distinct line labels, and the two start columns have opposite label parity. Hence no component is a cycle. This supplies the all-width acyclicity argument missing from the brief sentence in L1.

Added long edges cannot cross one another or an old long edge because they are parallel. They lie in x>=2, whereas short joins lie in 0<=x<=1, so they cannot cross a short join. Thus the crossing rate remains eight per four rows for every k. Every test edge has both endpoints in columns 0 through 2; none of the added edges is a test edge. Residues and penalties stay unchanged.

The cheap field extends by the same long chains, retaining its zero excess and h=2. Therefore the additive-table argument applies at each fixed width. Use the row-normalized inequality `X_strip-N >= beta*sum a-C_k`. A scan of S_k has k+2 transitions per row, so its baseline per transition is `1/(k+2)`, not `1/4` when k differs from two. Repetition removes any finite C_k. The statement concerns the periodic strip relaxation with its existing degree and forest conditions; extra conditions from a full tour are outside this obstruction.

## Check record and required scope wording

On 2026-10-03, these commands all passed, sequentially, with one Python process and no solver:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 gap/lowerbounds/check_frac_obstruction.py
PYTHONDONTWRITEBYTECODE=1 python3 gap/lowerbounds/check_frac_obstruction_wide.py
python3 gap/verifier/claim25_check.py
```

The author logs are `gap/verifier/claim25_obstruction.log` and `gap/verifier/claim25_wide.log`. The independent standard-library script imports no worker code. It checks the twelve penalty-dominance cases, reconstructs both periodic fields, checks their degrees and forests, counts crossings by exact determinants for widths 2 through 8, checks all orientation/parity cases, and checks the two width-two starting caps. Its report is `gap/verifier/claim25_check.json`. The proof above, rather than those seven sampled widths, establishes the extension to every fixed k.

Keep the last part of L1 labelled ARGUMENT. The residue sum `1+2=0 mod 3` does show that these local endpoint data discard every affected candidate path. It does not prove that a completed tour realizes those data on two adjacent sides or attains equality in the complete area and path budget. Replace “the loss is also real” by “the endpoint-residue loss bound is also tight for these local data.”

No author file was edited. Claim 25 is complete. Lower Bounds should add the parity translation, the averaged table proof (or the nonnegativity step), the all-width forest argument, and the local-data scope wording. The strip route closes at beta=1; a new lower-bound improvement needs information beyond this additive residue test.

# Claim 26: boundary surplus gives 52n/11-O(1) crossings — 2026-10-03

**Verdict: PASS, both parts. For every even n>=32, every closed knight's tour on an n by n board satisfies**

    11X >= 52n - 3954,
    X >= 52n/11 - 360.

The leading coefficient is 52/11, strictly larger than 14/3 by 2/33. This is a computer-certified mathematical proof. It uses the previously audited tile and charge lemmas and a new independently rebuilt finite potential. No Lean theorem for this result was checked or claimed. The forest condition retains the Hamiltonian-tour scope; this audit does not extend the result to all spanning 2-factors.

I checked U1 and its U2-to-U3 implication in gap/turnstheory/FINDINGS.md, request R1, L3 in gap/lowerbounds/FINDINGS.md, both R1 programs and their fractional-state dependencies, and appendix B of the audited crossings post. The audit input copies and SHA-256 hashes are in gap/verifier/claim26_sources/.

## A. Boundary surplus and retained paths

### Actual boundary sets and the exact union error

Keep the audited definitions. S_sigma consists of all tour edges with an endpoint in column 0 or 1 in side sigma's coordinates, and X_sigma counts crossing pairs within it. B_sigma consists of all crossing pairs whose two edges each have an endpoint in column 0. Put b_sigma=|B_sigma| and B=union_sigma B_sigma. Here b_sigma is a boundary crossing count, not the old failed-row count from appendix B.5.

Opposite boundary sets are disjoint for n>=32. An edge common to two adjacent boundary edge sets must be one of the four corner edges listed in appendix B.6. Those four edges have five possible crossing pairs. Thus each adjacent set intersection has size at most five, and the elementary union bound gives

    |B| >= sum_sigma b_sigma - 20.

This uses all actual boundary crossing pairs. It does not select a smaller subset of size n-1 per side. No sign assumption on their surplus is needed. Define

    R = sum_sigma b_sigma - 4n,
    D = sum_sigma X_sigma - 4n,
    E = X - 4n + 2.

Then |B| >= 4n+R-20. In particular, R is allowed to be negative.

### Fractional loss and full-square avoidance

At each corner retain the candidate curves gamma_r from the audited proof, for 12<=r<=n/2-4. There are exactly 2n-60 candidates, with disjoint dual vertices and whole squares inside the board. For each endpoint let c=(-1)^r, let F be its correctly oriented eight-edge sum, and set

    h = (1+c)/2 + c*(F+2) modulo 3.

The exact endpoint identity in appendix B.3 gives integral_Q omega = h_left+h_bottom modulo 3, without requiring F=2. Let e be its oriented inward-exception indicator. Use the Section 11 penalty: a=1 when e=1; otherwise a is 1/2, 1, or 0 for h=0, 1, or 2 respectively.

Discard a candidate if either endpoint has e=1 or its two residues sum to zero. Define A to be the sum of a over the two endpoints of every candidate, including discarded candidates. The 36 residue/exception cases give discard_indicator <= a_left+a_bottom. Therefore

    L >= 2n - 60 - A.

Every retained path is charged. More importantly for this change, its whole squares avoid the tile overlap of EVERY pair in B. The boundary overlap lemma is independent of the old F=2 test: a pair from B_sigma can enter a depth-one square only through the stated exceptional pair, and cannot enter a square at depth two or more. Retention excludes that exception at both endpoints. The other path squares are too far from all four boundary strips. Enlarging B to its actual size therefore does not invalidate the exclusion. The independent geometry check enumerates all ten unordered boundary crossing types up to translation, equivalent to the author's twenty anchored orders, and confirms the unique inward exception.

The fractional rule is essential here. One must use these charged, nonexceptional paths rather than silently retain the old rule that discards every failure of the joint binary test.

### Square budget with the surplus retained

The audited tile identity gives at most 2E uncovered quarters. If U is the union of the whole squares on retained paths, each multiply covered quarter in U belongs to a crossing pair outside B, and each such pair accounts for at most two quarters. Each charged path forces two bad quarters in its own squares. Consequently

    2L <= bad(U) <= 2E + 2(X-|B|)
       <= 2E + 2[(4n-2+E)-(4n+R-20)]
        = 4E - 2R + 36.

Combining this with the bound on L yields the explicit U1 inequality

    4n <= 4E + 2(A-R) + 156.                       (26.1)

This is a direct use of the old area budget before replacing |B| by its minimum. The same R will occur in the strip certificate and cancel algebraically; no assumption that the two inequalities use separate crossing pairs is needed.

For the width-two strip counts, the audited overcount bound remains unchanged. A pair counted at two adjacent sides has both edges in that corner's 4 by 4 square. It contains 24 possible knight edges, so the total excess count is at most 4*binomial(24,2)=1104. Opposite strips cannot share a pair. Thus

    sum_sigma X_sigma <= X+1104,
    D <= E+1102.                                    (26.2)

## B. R1 weights, parity, and half walks

### Exact crossing ownership

Scan each full side in increasing (row,column) order, with four transitions per row. Every edge is selected once, at its earlier endpoint. The transition that selects the later edge of a crossing pair owns that pair. An edge whose endpoints were both processed cannot cross a new edge because their open row intervals are disjoint. Edges that end at the current cell share that cell with new edges and cannot cross them properly. Therefore it is sufficient to compare new edges with still-pending edges and with earlier new edges at that transition.

The new weight w0 counts such a pair if and only if BOTH of its edges have an endpoint in column zero. This is precisely membership in B_sigma, not merely incidence of one edge, nor incidence of the crossing point. The author code uses the correct test. The independent program counts w and w0 directly while it generates chosen edges; it does not recover w0 from an author graph or an author weight array.

Summed over the full side, w gives X_sigma and w0 gives b_sigma, each pair once. Splitting at row n/2 preserves those totals, including pairs with edges on both sides of the split. For a half walk, call these assigned counts X_H and b_H. They need not equal counts in the subgraph induced by the half-board cells.

### Normalization of the potential inequality

Let a be the fractional penalty above and charge t=2a only at row end. For beta=p/q the proposed integer arc cost is

    q*(4w-1) + p*(4w0-1) - 2p*t.

The constants -q and -p occur on every transition. Over m complete rows, division by 4q therefore gives exactly

    (X_H-m) + beta*(b_H-m) - beta*sum_H a.

At p=4, q=3 the cost is 12w+16w0-7-8t. An integer potential of width M gives

    (X_H-m) + (4/3)*(b_H-m) >= (4/3)*sum_H a - M/12. (26.3)

This is exactly U2's required cost. There is no missing factor of four, extra boundary baseline, or double row-end penalty.

### Both orientations and both initial parities

Use the up test on scan rows 0..n/2-1 and the down test on rows n/2..n-1. The near-corner candidate endpoint rows are 12..n/2-4; the far rows are n/2+3..n-13. They are disjoint and lie in the respective halves. The far corner's local radius is n-1-y, so its parity is opposite to the global row parity when n is even. At the start y=n/2 of that half its radius parity is (n/2-1) mod 2, and it toggles on every row. The certificates explicitly permit either initial parity, so they cover this choice.

Both half walks keep the actual pending edges and component labels from the full scan. They do not restart the strip at an empty state. The row accumulator is initialized from pending test edges at that row, and both certificates cover every reachable base state at row start with either parity. Thus a midline cut introduces only the potential endpoint error. It introduces no additional crossing or row-history error.

All a are nonnegative. The eight half walks pay for every row, so their penalty sum is at least A, the smaller sum over candidate endpoint rows. With four up halves and four down halves, summing (26.3) gives

    (4/3)*A <= D + (4/3)*R + C_total,
    C_total = 4*(155/12) + 4*(159/12) = 314/3.        (26.4)

Using the common bound 53/4 for every half is also valid; it gives C_total=106 instead.

## C. Independent finite certificate and source audit

gap/verifier/claim26_certificate.py is a new standard-library checker with no worker imports. It generates all legal degree-two choices in columns 0 and 1 and degree-at-most-two choices in columns 2 and 3, using only edges incident to the first two columns. Pending component labels reject cycle closure. The graph starts from the empty state. The independent transition construction is the same mathematical forest model as the audited proof.

It rebuilds 82,516 base states and 144,674 base arcs. Its augmentation retains all twenty possible edges that meet the current row, and also its parity. It seeds both parities at every base row-start state. This gives 368,012 augmented states and 687,262 arcs. It has more states than the author's test-edge-only graphs; it does not copy their accumulator implementation.

The checker independently derives both oriented penalties from the retained row edges. Bellman-Ford uses exact integers and a virtual source to all nodes. After convergence it checks EVERY arc inequality again. On 2026-10-03 the results were:

| Orientation | Potential range | Arc inequalities checked | Error C |
| --- | --- | ---: | --- |
| up | [-155,0] | 687,262 | 155/12 |
| down | [-159,0] | 687,262 | 159/12=53/4 |

Both minimum reduced costs are zero. The range is over all generated states, not only the empty start or one parity. The exact potential arrays are retained as claim26_potential_up.json.gz and claim26_potential_down.json.gz, in the deterministic node order defined by the checker. Their uncompressed hashes are in claim26_certificate.json.

I also reran r1_independent.py up 4 3 and r1_independent.py down 4 3, sequentially on one core. Both independently rebuilt author graphs and reproduced their stated ranges. The audit wrapper required the convergence text and exact range, not just exit code zero. The author logs are claim26_author_up.log and claim26_author_down.log; command results are in claim26_author_runs.json.

The source checks of r1_stab.py and r1_independent.py pass: both use the correct two-edge boundary-incidence test, reconstruct new versus pending edges in a common row frame, verify their reconstructed total w against the base weight, and charge t only at row end. Their reflected tests and parity updates agree with the independent checker. The former maps each accumulator copy back to the proper base arc when adding w0. I did not rerun the NumPy Dinkelbach search, since the direct certificate and sharp witness settle the requested coefficient.

The independent checker also checks the old saturated field over two rows: X_H=4, b_H=2, and sum a=3/2 in each orientation and either parity phase. Thus the boundary surplus is zero and its certificate ratio is 2/(3/2)=4/3. This proves that beta=4/3 is the limit of this particular strip inequality. Its optimality is not needed for the global lower bound.

## D. Explicit final algebra

Combine (26.2) and (26.4):

    (4/3)*(A-R) <= E + 1102 + 314/3 = E + 3620/3,
    A-R <= (3/4)*E + 905.

Insert this into (26.1):

    4n <= 4E + 2*((3/4)*E+905) + 156
        = (11/2)*E + 1966,
    8n <= 11E + 3932,
    11X = 44n-22+11E >= 52n-3954.

Hence X >= (52n-3954)/11 >= 52n/11-360. If one uses 53/4 uniformly for all eight halves, the same proof gives 11X >= 52n-3958, which still implies the displayed rounded bound. The sharper constant 3954 uses the separate orientation ranges and no extra assumption.

The constants 20, 1104, 60, 155, and 159 have distinct sources: boundary-set duplication, width-two strip duplication, omitted candidate radii, and the two potential widths. No corner or half-walk error is omitted. The size condition n>=32 is the same sufficient condition used for the audited candidate paths and strip separation.

## Evidence and required presentation repairs

Commands from the project root:

~~~sh
python3 gap/verifier/claim26_certificate.py
PYTHONDONTWRITEBYTECODE=1 python3 gap/verifier/claim26_geometry.py
PYTHONDONTWRITEBYTECODE=1 python3 gap/lowerbounds/r1_independent.py up 4 3
PYTHONDONTWRITEBYTECODE=1 python3 gap/lowerbounds/r1_independent.py down 4 3
~~~

All passed on 2026-10-03, sequentially with at most one computation process at a time. claim26_geometry.py uses only earlier verifier tile/tour helpers and the new independent scan. It checks boundary overlap types, the two corner overcount constants, the endpoint coefficient identity at both parities, all 36 loss cases, candidate geometry and far-half parity for even n=32..100, and the exact final arithmetic. It also validates the saved n=96 and n=98 tours independently, then checks every scan transition on all four sides against their selected edges. The direct crossing counts equal the assigned half-walk totals for both w and w0. These finite examples verify the implementation; the all-n scope follows from the proof above.

Reports and logs are gap/verifier/claim26_certificate.json/log and gap/verifier/claim26_geometry.json/log. No author proof or program was edited.

For the final proof, define A as the candidate-endpoint sum, distinguish the new b_sigma from the old failed-row variable, use assigned half-walk counts in L3's display, and give the explicit far-half parity rule. Replace U1's pending status only with the theorem and certificate scope established here. This is a new Python-certified bound; the existing Lean statements remain unchanged. The next action is for the proof authors to add this audited reduction and certificate to the proof and result index before publication. Claim 26 is complete.

### Claim 26: full draft and reproduction follow-up, same audit

Turns Theory added PROOF_52_11.md and check_52_11.py during this audit. I read both. The draft's geometric reduction, penalty definition, far-half parity, state continuity across the split, and common-error constant 3958/11 agree with the proof above. Its section-by-section comparison correctly identifies the changes to the audited 14/3 proof. The new text already supplies the A, b_sigma, and half-walk scope clarifications requested above. Its coefficient and rounded constant need no change. Using the separate orientation ranges would optionally improve its exact numerator from 3958 to 3954.

Two small definitions should be made explicit in Section 4. Replace “The transition chooses edges to later cells, meets the degree rule, and rejects cycle closure and excess future degrees.” with:

> The transition chooses only legal knight edges to later cells that have an endpoint in column zero or one. It meets the stated degree rule and rejects cycle closure and excess future degrees.

Replace “Every test edge straddles the tested row, so none is omitted.” with:

> Every test edge has minimum row at most the tested row and maximum row at least the tested row. It is therefore pending at row start or is selected during that row.

Some test edges touch the tested row only at an endpoint. The implementation correctly includes them. These are presentation clarifications, not failed proof steps.

I ran all six local component commands listed in the new draft: tile geometry, corner flux, boundary overlap, square defects, endpoint loss, and boundary credit. All passed. Their logs, source hashes, and exits are in gap/verifier/claim26_local_runs.json and the six claim26_local_*.log files. Together with the two author certificate runs already completed, this reruns all eight component commands required by the new runner. I also inspected its exact rational calculation and its assertions on convergence and potential range. I did not invoke the aggregate runner itself because it writes to the author's directory, which is read-only for this audit.

Final source comparison found only additions to Turns Theory's FINDINGS.md and REQUESTS.md: the new full-proof status, the reproduction summary, and a separate future proposal. The U1 proof and R1 request body audited here did not change; all lower-bound implementation inputs stayed byte-identical to the snapshots. The two new proof/runner files are also copied into claim26_sources/. The separate future proposal is outside Claim 26. Final verdict remains PASS.


## Claim 26 consolidated-document verdict — 2026-10-03

**Audit object: gap/turnstheory/PROOF_52_11.md. Verdict: PASS.** U1--U3 and L3 are its supporting sources. The current document is byte-identical to the full draft read during Claim 26; its SHA-256 is 761f3d3f6c590aa1ff5319b3394ff352598581b4f3c85a09cc2a814bd6e246a6.

The document proves, for every closed knight's tour on an even n by n board with n>=32,

    11X >= 52n-3958,
    X >= 52n/11-360.

These are the document's own constants, using the common half-walk error 53/4. Claim 26's optional sharper numerator 3954 uses the separate orientation errors; it is not the numerator printed in this document. Both versions have the same rounded constant 360 and the same size range.

I checked check_52_11_report.json: all eight component checks are listed as passed, with the correct potential ranges and exact constant 3958/11. That aggregate report reuses its two stability logs. My Claim 26 audit freshly reran both stability checks and all six local checks, and also rebuilt the certificate independently, so its verdict does not depend on accepting those reused logs without verification.

The two Section 4 wording clarifications already quoted in Claim 26 remain applicable. They make the strip-edge restriction and inclusive row-incidence condition explicit; the surrounding definitions and checked implementation already supply those conditions. They do not change the PASS verdict. The author can update the draft's pending-review status and the results index after applying them. No author document was edited. The document audit is complete.


## Claim 28: the proposed arch floor for the fold family — 2026-10-03

**Verdict: PASS / CERTIFIED for the stated periodic edge-strip repair price at W<=4; PASS for the requested independent W=4 checks at periods 1 through 8. GAP / ARGUMENT for the proposed universal arch floor. G7's local non-neutrality conclusion is PROVEN; its carrier-network consequence is still ARGUMENT.**

Sources: gap/structures/FINDINGS.md G2 and G7; gap/searcher/FINDINGS.md Section 5; gap/searcher/arch.cpp; gap/searcher/RATES.md. The endpoint lemma is from the audited w-turnstheory/PROOF_crossings_lower.md, Section 3. Claim 27 is reserved and is not part of this audit. This audit does not change the proved upper construction or Claim 26's lower bound.

### 28A. What the edge certificate measures

The strip has free columns 0 through W-1, degree two at each cell, and the fixed (2,1) field outside. The two forced exterior ports per row lie at columns W-2 and W-1. A line has index c=x-2y. Its cheap P partner is c+3 for odd c and c-3 for even c. N_re counts port ends whose actual strip partner differs from this partner. Each wrongly paired strand contributes two ends. This is not the number of locally non-P rows, changed edges, or current-carrying rows.

The transition weight in arch.cpp is 2 times newly counted crossings, minus a bonus of two when two exterior rays close into a non-P pair. The code keeps the origin c+2r of each pending ray. At closure a known pair is P precisely when its origins differ by three and the smaller origin is odd. Origins age by two per row. An origin above RMAX, or an unspecified warm-up origin, becomes unknown; a closure with an unknown origin receives the non-P bonus. Thus the machine certifies 2X-N_tilde, where N_tilde is the closure reward and can overcount the true N_re. This relaxation has the correct direction: a lower bound for 2X-N_tilde also bounds 2X-N_re from below. Equal results at two cutoffs are useful checks, but are not needed to justify this direction.

The scan records pending edges and their pair connections, rejects a finite cycle, enforces degree two after warm-up, and counts each proper crossing when the later edge is inserted. The exterior ghosts supply the fixed line ends. At W<=4 a component with no exterior port can only occupy columns 0 and 1; its degree-two continuation is infinite, so this case does not introduce an untested finite cycle. Translation parity is in the state. An odd geometric period can be represented by doubling it.

The steady graph is pruned to its directed core, with the base current class selected. Exact integer relaxation checks the arc inequalities for the target mean two per row. No floating-point minimum-mean result is needed for the LAMBDA=2/1 run. Consequently, every periodic strip in this model satisfies

    2X-N_re >= 2p, or X >= p+N_re/2.

This is exactly the per-end price needed by a *fixed-chevron, edge-repair-only* version of G2 step 3. It does not establish G2 step 2 for arbitrary interior changes.

I copied arch.cpp without changes, compiled it, and reran all three base classes with RMAX=16 and LAMBDA=2/1:

| W | Base current | States | Arcs | Core states | Integer potential range | Crossing error C |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 0 | 48 | 48 | 48 | 24 | 3 |
| 3 | -1 | 3,488 | 3,972 | 1,444 | 60 | 6 |
| 4 | 0 | 6,950,475 | 8,546,081 | 2,429,580 | 78 | 6.5 |

All runs certify the target without refinement. The integer potential unit is 1/(W+2) of an objective-weight unit. Hence C=range/[2(W+2)]. Width 4 took about 38 seconds for graph generation, using one CPU core. Logs and JSON output are claim28_arch_w2.*, claim28_arch_w3.*, and claim28_arch_w4.* under gap/verifier/.

**Required finite-interval wording repair.** The error 6.5 applies to a path of complete rows between states of this current-class core, with N_tilde counted when strands close in that path. It does not directly apply to N_re defined as repaired port ends whose physical rows lie in the interval. A strand can enter before the interval and close inside it, or enter inside and close afterward. Changing counting conventions requires a frontier correction depending on W. The finite statement must either retain the closure-reward convention or prove and include that correction. Transient states and joins between current classes also need a bound. On a whole period, these endpoint distinctions disappear and the advertised inequality is valid.

The output and comments should call the optimized weight 2X-N_re (or its relaxed closure form), rather than crossings. The code's arithmetic is correct; generic output labels can hide the quantity being proved.

### 28B. Independent CP-SAT check with lifted pairing labels

New code: gap/verifier/claim28_pairing.py. It imports no worker implementation. It builds all internal knight-edge orbits on four columns and p rows, fixes the exterior edges, and imposes the degree constraints. A perfect matching of the 2p port vertices specifies their partners. Selected edges propagate pairing labels. Integer row lifts impose the actual vertical displacement along every port-bearing path. The test for P uses integer c values in the infinite cover, not c modulo the period. This distinction matters at small periods.

This model covers every periodic configuration in the stated width-4 class. A quotient component containing ports is a path with exactly two degree-one ports and at most 4p vertices. Its lift displacement is less than 8p, so the lift range [-10,10] loses no such path. Components without ports may use a separate label; at this width their lifts are infinite paths in columns 0 and 1. Parallel quotient edges retain their distinct vertical displacement. The base current is imposed at the cut below row zero; odd periods cause no problem for the zero class.

The objective is 2X-N_re. Boolean conjunctions count proper crossing pairs, with orbit multiplicity. There is no imposed lower bound of 2p. After solving, a separate traversal traces each actual lifted port-to-port path and recounts N_re. It also checks that a portless component has nonzero winding. A second crossing count uses a different row-ownership convention.

Command:

    .venv/bin/python gap/verifier/claim28_pairing.py 8 90

Each solve used two workers. Every status was OPTIMAL, with matching objective and lower bound:

| Period p | Minimum 2X-N_re | Objective per row |
| --- | ---: | ---: |
| 1 | 2 | 2 |
| 2 | 4 | 2 |
| 3 | 6 | 2 |
| 4 | 8 | 2 |
| 5 | 10 | 2 |
| 6 | 12 | 2 |
| 7 | 14 | 2 |
| 8 | 16 | 2 |

All extracted cover checks passed. Total solve time was about 17 seconds. The P witnesses have X=p and N_re=0. As a separate check that the model permits nonzero repairs and their lifts, I forced N_re=2p at p=1 and p=2. Both solves were OPTIMAL with X=2p and objective 2p, and both cover checks passed. Results are claim28_pairing.json, claim28_pairing.log, and claim28_pairing_calibration.json. These finite solves independently support the all-period certificate; they do not alone prove the all-period theorem.

### 28C. G2, step by step

| Step | Status | Scope and repair |
| --- | --- | --- |
| Difference of two degree-two colour currents is divergence-free | PROVEN | Apply to a region on which the base configuration has degree two; handle base defects explicitly. Closing an arch by an outside segment then gives zero net difference current through its boundary. |
| Uniform through-corridor shift has the same parity as its current | PROVEN within the S8 corridor hypotheses | It is a statement about a uniform field and a specified through-corridor with matching cuts. It is not a classification of all changes to a tour. |
| Every possible way to untrap a line produces the required edge repair | ARGUMENT | Conservation and shift parity do not establish this for branches, returning paths, glides, arbitrary local surgery, or a combination of them. G2 itself admits interior loop merges. A measured cost for one rung-swap construction is not a lower bound for all interior merges. |
| Every strand in a fixed P-compatible chevron nest needs a changed end if only edge pairings change | PROVEN | If a strand retains its P partner at both ends, the matching involutions also force its partner to retain those same two connections. These two strands remain an isolated closed component. A larger single tour cannot retain it. Thus each strand has at least one changed end, apart from exceptional components in a bounded endpoint region. |
| Changed port ends cost at least 1/2 crossing each above the edge baseline | CERTIFIED | True per period in the specified W<=4 base-current strip. For finite intervals use the closure convention and frontier/core qualifications in 28A. A locally non-P row need not change its ultimate port pairing. |
| Four standard midpoint nests contain 2n arch strands in total, up to bounded rounding | PROVEN for that fixed layout | Each midpoint contains n/2 strands. The edge-only matching argument and strip price then give n extra crossings, provided a bounded number of admissible strips and controlled joins cover the repairs. |
| Every free-fold steep layout with chevrons has this count and satisfies these repair hypotheses | ARGUMENT | Neither G1's net-step theorem nor G2 supplies a classification with total chevron edge length 2n. Cancelling fold pairs and glides remain possible. Merely having chevrons does not specify the four standard nests. |
| The universal family pays arch >= n-O(1), and this adds to an independent flux floor | ARGUMENT | Widths >=5, general interior repairs, joins, the layout count, and separation of crossing charges remain unproved. A constant loss per segment is O(number of segments), not automatically O(1). The same crossings may contribute to both repair and flux costs. |

The repaired conditional conclusion is useful: for the standard fixed nests, repairs made solely by strip re-pairings at depth at most four pay at least half a crossing per repaired end. With a bounded number of core stretches and controlled endpoints, this yields arch >= n-O(1). It is not a theorem about every free-fold layout or every untrapping mechanism.

The rates in RATES.md concern fixed straight bands at the listed widths and currents. They do not remove these qualifications. I checked their scope against the proposed use; I did not rerun every carrier entry in that table as part of this light audit. In particular, a non-base-current price per row is not by itself an additional per-repaired-end price, and the two must not be added without a joint charge inequality.

### 28D. G7: a charged corner, not a general carrier decomposition

**PROVEN:** If both local endpoint windows of the audited corner path gamma_R are P or P-prime, the path is charged, whatever lies inside the corner. This holds for 12<=R<=n/2-4, with the board, orientation, and endpoint conventions of the audited proof. Both cheap patterns have F=2 modulo three and lack the forbidden pair. The up and down tests both pass, so reflection and transposition give all four corners.

I reran corner_test.py and independently substituted the two patterns into the audited eight-edge coefficient table. The independent check covers both scan directions and both row parities; see claim28_corner_check.py and its JSON output.

**Sign repair:** With gamma_R oriented as in the audited proof, the complementary path Q_R has flux 1 modulo three. The closed-boundary flux is zero, so gamma_R has flux -1=2 modulo three, not 1. Reversing orientation changes the sign. G7 should state “nonzero modulo three” unless it fixes the orientation. This does not affect its non-neutrality conclusion.

**ARGUMENT:** Nonzero flux across each such gamma_R does not alone produce a single carrier crossing them all, or an unrestricted network with the measured band rates. If an endpoint test fails, its window is not P/P-prime; the converse does not hold. Nor does that failure establish a uniform extra crossing per row or a changed port partner. G7 excludes a neutral corner behind two cheap tested windows. Its sentence “only carrier rates matter” requires the missing general decomposition and accounting theorem; Claim 17's gap remains.

### Repairs and audit evidence

Replace G2 step 3's local non-P-row price by the precise per-end certificate, restricted to W<=4. State the fixed-chevron matching lemma separately. Keep the universal mechanism claim, the universal layout count, and the additive flux-plus-arch floor labelled ARGUMENT. State finite-strip errors with their closure convention and account for joins. In G7 change the signed residue or state only nonzero charge, and separate that theorem from the proposed carrier consequence.

All new code and logs are under gap/verifier/ with prefix claim28_. claim28_source_hashes.json records the inspected source versions and independent checker hashes. The copied arch.cpp matches the author file byte for byte. No author source, construction, or blog post was edited. The requested checks are complete; a universal arch floor still needs the listed mathematical steps.


## Claim 27: interval credit gives 204n/43-O(1) crossings — 2026-10-03

**Audit object: gap/turnstheory/PROOF_N1.md. Verdict: PASS.** For every closed Hamiltonian knight tour on an even n by n board with n>=32,

    43X >= 204n-558664,
    X >= 204n/43-558664/43 >= 204n/43-12993.

The theorem, its size range, and its explicit constant pass as submitted. The coefficient exceeds 52/11 by 8/473. The argument uses connectivity to exclude cycles in proper tour subgraphs; no result for arbitrary disconnected 2-factors is established. The finite certificates are checked by integer computation. No Lean result is claimed.

The audited proof's SHA-256 is c9e72712b5204618348331b3d54fec221938cbf9e13eac1a8096bb65c3e3a753. Its Sections 1–3 are byte-identical to the corresponding sections of PROOF_52_11.md as read in this audit. These are the tile budget, endpoint residues and fractional loss, retained boundary surplus, and the inequality

    4n <= 4E+2(A-R)+156,    E=X-4n+2.

Their Claim 26 audit therefore applies unchanged. The new material is checked below.

### 27A. Interval lemma, including arbitrary interval ends

**PASS.** The lemma applies to a finite forest whose edges join column zero to column one or two and whose vertex degrees are at most two. The scan permits degrees zero and one in column zero outside the chosen intervals. This soft rule is necessary: a run can begin or end at an arbitrary pending-edge state, rather than at an empty state.

The state contains the current column, each pending edge, and the path-component partition of pending edges. Maximum row span two makes the state space finite. A new edge can only reach a future vertex. Thus a component with no pending edge can be forgotten. Two incoming edges in the same component would close a cycle and are rejected. Otherwise the transition merges their component labels, checks future endpoint degrees, and records the selected outgoing edges. This represents every legal forest prefix.

Each crossing is counted when its later edge is added. An edge already completed before the current cell cannot properly cross a new edge: its largest row is at most the new edge's smallest row. Incoming edges share the current endpoint with the new edges. Comparing new edges with the other pending edges therefore counts all proper crossings exactly once. The row assignment is valid even when one edge started before the interval.

The complete soft graph has 330 states and 700 arcs. A hard arc either processes a ghost column or completes degree two in column zero. There are 580 hard arcs. The saved integer potential satisfies

    3w-1+p(u)-p(v) >= 0

on every hard arc. Its row-boundary range is [-12,0]. A blocked interval of length l follows 3l hard arcs, so telescoping gives W(I)>=l-4. Applying this only to intervals longer than four, and using nonnegative crossing weights on all other transitions, gives

    X_J >= sum_runs max(0,l-4).

Disjoint row intervals have disjoint assigned transition sets. There is no crossing counted twice when these interval lower bounds are summed.

I reran the author's generator and its separate verifier from copies under gap/verifier/. I also rebuilt the soft graph with the verifier's own forest transition code, without importing either author's builder, and checked the saved potential against all 580 hard arcs. The independent state set is exactly the saved 330-state set, and the row-boundary range is exactly [-12,0]. Evidence: claim27_interval.log, claim27_interval_independent.log, claim27_interval.py, and inner_boundary_certificate.json.

### 27B. Why blocked rows supply separate crossings

**PASS.** Let S_sigma contain all tour edges incident to depth zero or one, and let d_x(y) denote degree in this edge set. At a blocked centre row y,

    d_3(y)=0,    d_2(y-2)=d_2(y+2)=2.

All legal neighbours of (3,y) to its left are (1,y-1), (1,y+1), (2,y-2), and (2,y+2). The first condition excludes the two column-one edges. The other two vertices already have their full tour degree in S_sigma, so neither can supply a new edge to (3,y). Its two tour neighbours must therefore be in columns four or five.

The graph J_sigma of all selected edges joining column three to columns four or five has maximum degree two and is a proper subgraph of the Hamiltonian cycle. It is a forest. After translation by three columns it has exactly the form of the interval lemma. This translation is applied to the entire J_sigma, not only to edges induced by the blocked rows. The latter restriction would lose the lemma's interval assignment. Each blocked run has degree two at all its column-three boundary vertices, so X_(J_sigma)>=K_sigma follows.

For the same physical side, S_sigma and J_sigma share no edge. A crossing pair internal to one set therefore cannot be a crossing pair internal to the other. There is also direct geometric separation: S_sigma has endpoints at depths at most three, while a proper crossing internal to J_sigma lies strictly deeper than three. No K credit is taken from X_(S_sigma) on that side.

Opposite sides' S/J sets cannot share an edge for n>=32. A crossing pair shared by sets from adjacent sides must have both its edges wholly inside the six-by-six corner square. That square contains 80 possible knight edges. The bound 3160=binomial(80,2) on a shared pair set is conservative and valid; it need not test whether every such pair crosses. Four adjacent side pairs and four choices of S/J give overcount at most 50560. For a pair present in m sets, m-1<=binomial(m,2), so pairwise intersection bounds control all multiplicities, including any higher-order overlap.

It follows that

    sum_sigma [X_(S_sigma)+X_(J_sigma)] <= X+50560,
    D0+K <= X-4n+50560 = E+50558.

Thus the separate budget N0 is valid, with the stated constant. Crossings credited to K may belong to the other side's strip near a corner; the proof does not assume otherwise and pays for that overlap explicitly. No K term is added to the square-area budget. It is used only in this separate crossing-count inequality, which prevents double use of the extra credit in N1.

### 27C. Raw blocked rows, compressed history, and half splits

**PASS.** After row r, the compressed state is

    (cand_(r-1), cand_r, g_(r-1), g_r),
    cand_y=z_y*g_(y-2),    g_y=[d2(y)=2], z_y=[d3(y)=0].

At row r+1, its emitted flag is cand_(r-1)*g_(r+1), exactly z_(r-1)*g_(r-3)*g_(r+1). This is the raw blocked condition for centre y=r-1. Its new candidate is z_(r+1)*g_(r-1). The state update therefore preserves the defining identity. Ghost degrees are measured when the corresponding cell is processed, as incoming plus newly selected edges; they are final degrees in S_sigma.

Zero initial history makes the first four emitted flags zero. Rows 4 through n-1 emit exactly centre rows 2 through n-3, so there are no unproved boundary flags and no artificial terminal rows. The counter starts at zero, increments on a blocked flag, resets on an unblocked flag, and is capped at four. It pays one on the fifth and each later flag in a run. Hence its total equals sum max(0,l-4), including a run that ends at the final emitted flag.

I checked the compression identity on all 64 raw history-bit states, all four next degree-bit inputs, and all five counter states (1280 cases). I checked all 4096 length-twelve flag words against direct run lengths and all thirteen split positions. The two author history checks also passed, including their longer runs and 18,000 random degree sequences. These finite checks verify the implementation; the displayed update identity proves it for arbitrary sequences.

At n/2 the actual base state, history, and counter must continue. The proof does this. A k charge emitted in the far half can concern a centre row in the near half. That causes no error: the certificate uses additive transition weights and never requires the penalty a and credit k on one transition to have the same geometric centre row. Summing both halves recovers K_sigma exactly.

Near-half parity is the physical row parity. Far-half parity is the local radius parity (n-1-y) mod two, which is opposite for even n. Both certificates include both initial phases and every history/counter at every base row-boundary state. They therefore include the actual split state with the required phase. Test-edge data are initialized from pending edges at the new orientation's first row; the state is not emptied.

### 27D. Combined weights and independent certificate

**PASS.** On a row arc, W=4(sum w-1), W0=4(sum w0-1), and t=2a. Here w0 counts a crossing pair if and only if BOTH of its edges are incident to column zero, counted once with the same later-edge assignment as w. It is not a count of pairs with only one boundary edge.

For beta=16/11 the exact integer inequality is

    11W+16W0+44k-32t+p(u)-p(v) >= 0.

Dividing its sum by 44 gives exactly

    X_H-m+(16/11)(b_H-m)+K_H
        >= (16/11) sum_H a - 149/11.

X_H and b_H here mean crossings assigned to the half's transitions, not crossings in a subgraph induced by its rows. The coefficient of K_H is one and the coefficient of sum a is 16/11, as N1 requires. No scale factor is missing.

I read combo_stab.py and the C++ implementation. The Python graph adds four cell transitions per row, accumulates the listed endpoint edges, obtains both ghost degrees, and attaches the compressed history. Its endpoint coefficient and exception rules agree with Section 2. Its exact fixed-point relaxation has the correct potential-inequality direction.

I then rebuilt the graph independently. claim27_rows.py uses the verifier's previously audited Claim 26 forest transition routine, with no worker implementation imports. It retains the full selected edge set over each row and recomputes both endpoint orientations from that set. It records the ghost degrees directly, along with both crossing counts. It gives 82,516 base states, 144,674 cell arcs, 21,420 row-boundary states, and 250,990 complete row paths.

claim27_relax.cpp forms the product with both parities, all sixteen compressed histories, and all five counters. It keeps this graph implicit and starts an integer potential of zero at every node. It uses in-place relaxation and then checks every arc again. This differs from the author's array-based Python relaxation. No author potential is used. The results are:

| Orientation | Nodes | Checked augmented row arcs | Passes | Potential range | Minimum reduced cost |
| --- | ---: | ---: | ---: | --- | ---: |
| up | 3,427,200 | 40,158,400 | 20 | -596..0 | 0 |
| down | 3,427,200 | 40,158,400 | 19 | -596..0 | 0 |

The graph includes all row-boundary histories, even combinations that do not arise on an actual tour. This can only strengthen the certificate requirement. The potential error is exactly 596/44=149/11 in each orientation. The deterministic row records and both potential arrays are saved with hashes.

I also compiled a byte-identical copy of gap/searcher/lower/r2.cpp and reran both allhist certificate commands. Up used 13,817,578 nodes and 26,603,962 arcs; down used 20,645,732 nodes and 40,130,652 arcs. Both converged with zero violated arcs. Their full cell-state ranges are [-667,0] and [-687,0]. Those larger ranges are consistent with a different graph and are not used for the theorem's constant. The independent row rebuild above directly validates the smaller ranges that the theorem needs.

The C++ allhist option seeds every raw history at the empty base state and then explores reachable states; the Python and new verifier row graphs seed every history at every base row-boundary state. These are different state sets. Actual whole-side scans and their intermediate half starts are covered by the former, while the latter explicitly supplies the stronger arbitrary row-state statement used in the proof. There is no need to identify their potential ranges.

### 27E. N1, final constants, and the blocking field

The eight oriented half walks partition all full-side transitions. Their w sums give sum X_sigma, their w0 sums give sum b_sigma, and their delayed k sums give K. All penalties are nonnegative, so the penalty total over all scanned rows is at least A, the total over candidate endpoints only. Summing the eight half inequalities gives

    (16/11)(A-R) <= D0+K+1192/11.

Combining N0 yields

    (16/11)(A-R) <= E+50558+1192/11,
    A-R <= (11/16)E+557330/16.

Substitution into the unchanged square budget gives

    32n <= 43E+558578,
    43X >= 204n-558664.

All constants were recomputed with exact rational arithmetic. The constant 558664/43 is at most 12993. The required size is even n>=32: it supplies the candidate path range, separated corner boxes, and all opposite-side separation conditions. No additional size restriction enters the interval lemma or certificate.

The period-eight field in check_combo_obstruction.py also passes. I reran that checker and independently enumerated its degrees, crossings, boundary pairs, blocked flags, and both endpoint orientations/phases. Per eight rows it has X=16, b=8, blocked rows {1,2,5,6,7} modulo eight, runs of length two and three, and K=0. Up penalties are 11/2 and 5 in the two phases; down penalties are 5 and 11/2. Thus its ratio is 8/(11/2)=16/11.

Its forest property is not limited to a finite test window: following a nonterminal strand through successive column-zero vertices changes their row by three in one direction. The replaced edge terminates such a strand at a ghost port. No finite cycle can occur. The periodic field therefore obstructs beta>16/11 for this strip method. Optimality is not needed for the all-tour theorem, whose proof uses only the verified certificate.

### Reproduction and repairs

No mathematical repair to the submitted theorem is required. The author can change its conditional status to audited PASS. Keep the existing definitions of assigned crossing counts, the empty initial history, preserved split history, and the Hamiltonian-tour scope; these are essential to the proof.

Run the independent certificate from the research root:

    .venv/bin/python gap/verifier/claim27_rows.py
    g++ -O2 -std=c++17 gap/verifier/claim27_relax.cpp -o gap/verifier/claim27_relax
    gap/verifier/claim27_relax
    .venv/bin/python gap/verifier/claim27_interval.py
    .venv/bin/python gap/verifier/claim27_local.py

The interval checker reads the copied interval potential in gap/verifier/inner_boundary_certificate.json. The copied generator and separate verifier can regenerate and recheck it. The two C++ author-check commands are:

    gap/verifier/claim27_r2 up cert 16 11 allhist
    gap/verifier/claim27_r2 down cert 16 11 allhist

The author's fixed-beta combo_stab.py command reports convergence but does not print or save the potential range in that command branch. For reproducible constants, use its critical branch or add an explicit range and final-arc report. This is a reporting improvement, not a defect in the checked inequalities. The verifier commands above print and assert the range and all-arc check directly.

Sources are copied in gap/verifier/claim27_sources/. Logs, row records, potentials, exact local results, and hashes have prefix claim27_. No author file, proof post, or result index was edited. Heavy jobs ran sequentially, one process at a time. Claim 27 is complete. The remaining publication action is for the proof author or integrator to update the theorem's status and result index with this audited bound.


## Claim 29: red team of the private flux price — 2026-10-03

**Verdict.** L2 in gap/turnstheory/PLAN.md remains **CONJECTURE / GAP**. I found no completed-tour counterexample to the existence of some fixed radius r and some absolute error C0. I did find a valid forest patch that breaks a zero-error open-patch price greater than 1/2, and valid near-side patches where all local crossing resources belong to B. These are stop tests for a local certificate, not a disproof of the all-tour statement. The short tile identity in gap/searcher/PLAN.md is **PROVEN after an explicit convention for W3**. It does not supply L2's crossing allocation.

This report uses light finite searches and exact checks. It does not launch a carrier transfer graph or claim a new global lower bound. The master plan correctly separates endpoint restoration, connectivity, and their common capacity constraint. Its diagnosis of the old reduction's ceiling at coefficient five is also correct; this is a ceiling of that reduction, not of every method that uses strips.

### 29A. First fix the quantifiers and the required payment

The request describes a payment of at least p to each retained path. The exact displayed L2 in the master plan requires only

    sum_(i,z) f_(z,i) >= p|C|-C0.

It imposes no minimum on an individual path. These statements differ. With no individual demand, any crossing near at least one path can send its whole unit to that path. Ignoring the extra finite-local-rule requirement, aggregate feasibility then asks only for enough crossings in the union of the collars.

For a private demand p on each path and a fixed radius, form a bipartite graph with paths on one side and eligible non-B crossing pairs on the other. Fractional allocation with unit crossing capacities exists exactly when every subset S of paths satisfies

    |N_r(S)| >= p|S|.

This is the fractional Hall condition. For price 2/3 it can be checked with integer flow: source-to-path capacity two, path-to-eligible-crossing capacity larger than total demand, and crossing-to-sink capacity three. An allowed *total* deficit C0 can be represented by per-path deficits whose sum is at most C0. A constant allowance per path is different and would remove the desired leading gain.

**Required statement repair:** choose whether L2 requires individual demand, individual demand with a bounded total deficit, or aggregate payment only. A Hall obstruction for a subset refutes the individual version; it need not refute the aggregate version. A fixed finite patch cannot refute an unspecified absolute C0. A disproof of the stated all-tour lemma needs a growing completed-tour family that defeats every proposed fixed collar, or a proved repeatable obstruction with unbounded deficit.

### 29B. A genuine half-price obstruction for an open corner patch

**CERTIFIED finite witness; independently verified geometry and forest.** There is a legal forest with degree two at every vertex of the core {0,...,7} squared and degree at most two at its two-cell outer halo. There are no vertices at negative coordinates. It has two corner paths of the exact L shape, at radii 3 and 4. Both have combined height charge 1 modulo three. Neither endpoint has the inward exceptional pair.

The patch has 46 crossing pairs. Forty-five belong to the local boundary set B (both edges touch x=0, or both touch y=0). Its sole non-B crossing is

    (1,4)--(3,5)  crossing  (1,6)--(2,4).

Thus the two charged paths together have at most one eligible crossing unit in the *entire patch*, irrespective of how that unit is shared. A zero-error local requirement p>1/2 fails. In particular, price 2/3 would require 4/3 units and has deficit at least 1/3. There is no hidden finite cycle in this witness.

The CP-SAT model used degree constraints, proper geometric crossing tests, the exact endpoint residues, and the exception exclusions. A separate check traces components, counts crossings directly, builds exact tile quarters, and calculates the two path charges from the local quarter-flux formula. The result is not based only on the solver's endpoint-residue constraints. Witness edges: claim29_corner.json, first entry. Independent check: claim29_seeds.py and claim29_seeds.json.

**Limits:** these radii are below the audited candidate cutoff 12. The outer ports have not been completed to a Hamiltonian tour. A completion can add non-B crossings near the paths, and an isolated deficit can be absorbed by C0. This is a counterexample to a proposed zero-error free-halo patch input, not to L2 itself. A 12-by-12 search also found six charged paths with three non-B crossings, but that result contains two finite cycles. I reject it as a larger-tour patch witness; it is saved with that warning.

The next useful mathematical question is whether the acyclic two-path pattern can occur repeatedly, with compatible outer states and bounded total interface cost. Do not turn its local deficit into an all-tour claim before proving that step.

### 29C. Holes: the interior and a physical side behave differently

**CERTIFIED finite exclusion in the interior.** I searched a 6-by-6 degree-two core with a two-cell halo of degree at most two. Every legal edge incident to the core was allowed. All crossings between selected edges were forbidden, and a central tile quarter was required to be uncovered. CP-SAT returned INFEASIBLE. The same test on an 8-by-8 core was also INFEASIBLE. Solve times were below two seconds each, with two workers.

Every edge capable of covering the tested central quarter is in the model. Every actual degree-two tour restricts to a feasible degree configuration of this model. The finite result therefore excludes that central hole when the surrounding core is crossing-free. Rotations and translations give the corresponding local statement for the other quarter orientations. This does not prove price 2/3, but it blocks the simplest proposed interior counterexample: a hole with all crossings arbitrarily far away. At least for this local geometry, a hole forces a crossing in a bounded neighbourhood. The global area identity alone could not prove that fact.

**CERTIFIED finite witnesses near a side.** Next I used a 6-by-8 core at x>=0, with no edges beyond the physical side x=0. I allowed crossings in B_left and forbade every other crossing. I excluded the inward exceptional pair at row 4 and required a hole in one of the four quarters of the endpoint square (1,4). All four choices were feasible. Direct component checks find no finite cycles in these four witnesses.

For the right quarter of that square, the hole lies directly next to the first inward dual step of a corner path. Since the only crossings are in B and the exceptional pair is absent, its neighbouring quarters cannot gain a non-B overlap to supply the requested crossing resource. Thus retention does not by itself make every local endpoint hole payable by a non-B crossing.

These are free-halo witnesses. They have not been extended indefinitely along the side or inward. A further short periodic test at width four and period four, with each of the four fixed exterior line directions (2,1), (2,-1), (1,2), and (1,-2), found no B-only endpoint-hole extension of the tested right-quarter pattern. All four models were INFEASIBLE. This rules out those small fixed-field extensions, not all extensions.

**Implication for L2:** excluding all B may be stronger than the intended common-capacity accounting needs. Boundary surplus is still crossing capacity after the 4n baseline has been reserved. The local witnesses suggest that some retained-path costs may need that surplus, not only endpoint restoration or connectivity. Before an expensive certificate, either prove that these endpoint states must incur enough non-B costs on extension, or consider allowing f on the unused capacity of B under the same b+f+e+h<=1 rule. The latter changes L2 and needs joint accounting; it is not an automatic proof.

Evidence: claim29_window.py / claim29_windows.json; claim29_boundary.py / claim29_boundary.json; claim29_periodic.py / claim29_periodic.json. No exported proof trace is claimed for the CP-SAT infeasibility results.

### 29D. Completed-tour Hall tests

I checked the saved FOLD24 tours at n=96 and n=98, and the n=166 single tour carrying the period-four endpoint field. Each full tour was independently validated. I reconstructed the exact retained candidate family using both endpoint residues and the exception rule, and excluded the union of all four B_sigma sets.

The test neighbourhood is deliberately generous: a pair is eligible if its full edge-support bounding box meets the L-infinity collar of a path. The bounding box contains the true support, so this is a necessary-test relaxation. A failed flow is an obstruction even under that generous support convention. A successful flow is only a screening result; it does not prove an allocation for a stricter support rule or a translation-covariant finite local rule.

| Tour | Retained paths | Radius-zero maximum scaled flow / demand | Same test at radii 1,2,4,8 |
| --- | ---: | --- | --- |
| FOLD24 n=96 | 125 | 214 / 250 | Full demand met |
| FOLD24 n=98 | 124 | 216 / 248 | Full demand met |
| Field tour n=166 | 206 | 348 / 412 | Full demand met |

At radius zero the cut witnesses contain respectively 18, 16, and 32 retained paths with no eligible non-B pair at all. Thus a strict “a crossing must touch its path” version is false even on completed tours. Their repeated locations along the fold carrier are a useful test pattern. A collar of positive width removes these measured obstructions. This does not refute the master plan, which permits an unspecified fixed radius and a bounded error.

No Hall deficit was found for the larger generous collars on these three tours. This is finite evidence only. The full cut subsets and all counts are in claim29_tours.json; the independent checker is claim29_tours.py.

### 29E. The requested starting fields

**Exact checks, not universal lower bounds.** I rebuilt the period-four, period-six, and period-eight endpoint fields from their edge formulas. Their crossing counts per period are:

| Period | X | Boundary pairs | Non-B pairs |
| --- | ---: | ---: | ---: |
| 4 | 8 | 8 | 0 |
| 6 | 10 | 6 | 4 |
| 8 | 16 | 8 | 8 |

The period-four seed is an important warning about using endpoint penalties as retained-path charge. In its bad phase it has h=1 on every row. Against a cheap endpoint with h=2, the candidate is *uncharged* and discarded. Zero non-B capacity in that seed therefore does not refute a price on retained paths. The period-six and period-eight seeds have incomplete ghost degrees and require a completion before they define a full charged-path neighbourhood. Their penalty ratios must not be mistaken for private prices.

For alternating free folds, take every edge

    (x,y)--(x+1,y+2s_x),    s_x in {-1,+1},

with any prescribed sign sequence in x. Every vertex has one neighbour in the preceding column and one in the next. Edges in one column band are parallel; edges in different band interiors cannot cross. These patterns tile every interior quarter exactly once, as the independent check confirms for an alternating sample. Their combined height flux is zero. Arbitrarily frequent free folds are therefore not a cheap *charged* carrier.

For the audited gentle seam, use edges from (x,y) to (x+1,y-2) when y>=x, and to (x+2,y-1) otherwise. Its exceptional square row y=x-2 has multiplicities (0,2,2,0), while all other squares are perfect. I directly checked nine nested L paths at radii 4 through 12: each is charged, and the seam contributes nine crossings across those nine levels. Its price is one per level, not below 2/3. The two holes next to each crossing demonstrate why counting only overlap quarters misses part of the charge, but this seam does not produce a large-distance or half-price obstruction.

### 29F. The exact identity and what it does not prove

**PROVEN.** Define

    W3 = sum_(t: m_t>=1) binomial(m_t-1,2).

Equivalently, only quarters with m_t>=3 contribute. Do not use the polynomial (m-1)(m-2)/2 at m=0: that would count one extra unit for every hole. The implementation correctly excludes zero multiplicities; the plan's definition should state this convention explicitly.

For a closed degree-two spanning graph there are n² tiles, each with four quarters, and 4(n-1)² board quarters. Hence

    sum_t (m_t-1) = 8n-4.

The audited overlap lemma gives sum_t binomial(m_t,2)=2X-X1, where X1 counts crossing pairs with exactly one overlap quarter. At m>=1,

    binomial(m,2)=(m-1)+binomial(m-1,2),

and at m=0 the missing term is one hole. Therefore

    2X = 8n-4+G+W3+X1,
    E = (G+X1+W3)/2.

This does not require connectivity. Independent exact tile counts on the three validated tours give:

| n | E | G | X1 | W3 |
| --- | ---: | ---: | ---: | ---: |
| 96 | 338 | 400 | 230 | 46 |
| 98 | 362 | 429 | 247 | 48 |
| 166 | 578 | 611 | 466 | 79 |

All satisfy the identity exactly. The n=166 result reproduces the searcher's claimed measurement without importing its tile or crossing implementation.

**The global interpolation is valid.** Let delta=sum_sigma b_sigma-|B|, so 0<=delta<=20, and define R=sum_sigma b_sigma-4n. Then

    E = X_int+R+2-delta >= X_int+R-18.

For c_lambda as defined in the searcher plan, its *global* sum is lambda X_int+(1-lambda)E. Consequently

    E >= sum c_lambda+lambda R-18lambda.

The sign of the boundary term is correct. This is a nonnegative, mixed local density with a valid global budget.

**GAP in identifying that density with L2 resources.** A hole unit is not a crossing pair. A unit of W3 is not an unused crossing capacity independent of the other terms either. Assigning each mixed-density unit at most once proves a statement in this mixed budget; it does not define f_(z,i) on actual non-B crossing pairs with unit capacities. The identity relates global totals, not a local transport from holes to crossings, and it does not specify how that transport would avoid B or share capacity with e and h.

Thus a theorem in c_lambda currency could be a different valid route, but it would need its own joint global argument. It must not be presented as proof of the master plan's crossing-only L2. The boundary-hole witnesses are concrete tests for this distinction. The searcher's fixed-field wall rates and its assumption of cancelling transverse area terms also remain restricted to the stated band setting; the identity alone does not extend those rates to arbitrary open windows.

### Recommended stop tests and next step

Before building a large graph, specify the L2 demand version, the distance convention, and whether unused B capacity is forbidden or available. Include the saved acyclic two-path patch and all four B-only endpoint-hole states as mandatory tests of any proposed local rule. A rule may reject their boundary states only with a proved extension obstruction. Test joint subsets and interface states, not only one charged path at a time. Do not sum a fixed loss per patch over O(n) patches.

The most useful next step is a bounded-state extension or incompatibility proof for the B-only endpoint-hole witnesses and the acyclic two-path deficit. This directly tests whether the obstruction repeats or must pay later. A full all-tour counterexample would require completion and an unbounded deficit; neither has been established here. L2 stays CONJECTURE. The earlier audited bounds remain unchanged.

All new sources, witness edges, logs, and exact-check reports are under gap/verifier/ with prefix claim29_. The searches used at most two workers and small free-halo windows; no large transfer graph was run. No author plan or proof was edited. This red-team assignment is complete.


## Claim 31: exact joint-strip crossings give 24n/5-O(1) — 2026-10-03

**Audit object: gap/turnstheory/PROOF_R3.md. Verdict: PASS.** Every closed Hamiltonian knight tour on an even n by n board, n>=32, satisfies

    5X >= 24n-13012,
    X >= 24n/5-13012/5 >= 24n/5-2603.

The proposed coefficient, explicit constant, and size range pass. No mathematical repair is required. This is a computer-assisted integer-certificate proof, not a Lean result or a theorem about arbitrary disconnected 2-factors. The inherited Sections 1–3 are the audited Claim 27 inputs. The interval lemma and blocked-run credit are not used in this proof.

### 31A. The edge restriction and crossing budget

The selected tour edges incident to depth 0, 1, or 3 have exactly the column pairs

    01,02,12,13,23,34,35.

A vertex in columns 0,1,3 has all its tour edges in T_sigma, hence degree two. The other three columns have degree at most two. For n>=32 this is a proper subgraph of the Hamiltonian cycle, hence a forest. The decomposition T=S union F union J is disjoint as an edge decomposition. Y_sigma must count *all* crossing pairs of T, including pairs involving two different parts. The implementation and the independent checker both do so.

Opposite side sets share no edge. A pair counted at two adjacent sides has all four endpoints in their six-by-six corner square. There are 80 legal knight edges in that square, hence at most 3160 unordered pairs. The four adjacent side intersections give excess count at most 12640. Higher multiplicities are controlled by m-1<=binomial(m,2). This yields

    sum Y_sigma <= X+12640,
    D_T=sum Y_sigma-4n <= E+12638.

There is no claim that the component crossing counts are separate resources: the mixed pairs are included before this union bound. This avoids the separate S/J bookkeeping of Claim 27 and correctly improves its corner error.

### 31B. State completeness, cycles, and local weights

The degree rule EELELL means exact degree two in columns 0,1,3 and an upper bound of two in columns 2,4,5. Every selected edge is introduced at its lower-row endpoint; knight edges have nonzero row displacement. Pending edges record all possible future contacts. Processing an incoming edge at the current cell completes it; it cannot cross a new edge at that same shared endpoint. An already completed edge has maximum row at most the minimum row of a new edge, so it cannot cross it properly. Counting intersections of new edges with the remaining pending edges therefore counts all pairs once.

Only S edges carry component labels in slab mode. Two incoming S edges in the same component would close an S cycle and are rejected. Non-S edges are retained for degree and crossing counts but do not join S labels. A cycle involving F or J can be admitted. This is a valid relaxation: it enlarges the set containing all actual tour restrictions. The larger set need not itself be a forest in T. Its precise description matters; a theorem for the stronger full-label model is not needed.

The author's three counts satisfy w+wx=all new T crossings and w0=the new pairs whose BOTH edges touch column zero. Both counts use the same later-edge convention. At beta=2 the cell cost is

    4*(w+wx)+8*w0,

with the row-end subtraction 12+4t, where t=2a. Thus the sum over m complete rows is

    4(Y_H-m)+8(b_H-m)-8 sum_H a.

Subtracting the baseline once per row is essential: the old four-column expression cannot be applied separately at all six cells. The code uses the correct row-end subtraction.

### 31C. Endpoint memory and arbitrary half starts

Each watched endpoint edge has minimum row at most the tested row and maximum row at least that row. Of those present at row start, exactly the edges whose upper endpoint is in the tested row can disappear by row end. Their bits are retained. Every other watched edge is still pending at the next row start, including watched edges selected during the row. The union of those two sets therefore gives the complete endpoint test without omission or duplicate counting. The up orientation has two disappearing watched edges and the down orientation has four.

At each row start the disappearing bits are initialized from that actual base state. No history from an earlier row remains. Both parity phases are admitted. The base transition graph is parity independent, so switching initial parity switches every later phase on the same walk. Consequently the actual base state at the midpoint occurs with the needed parity in the appropriate orientation's graph. Restarting the *test memory* from its pending edges is valid; restarting the base scan at an empty state would not be valid.

The near half uses physical row parity, and the far half uses (n-1-y) mod two. For even n these are opposite. The certificate includes both choices. The crossing weights are assigned counts, not crossing counts of induced half-board subgraphs, so crossing pairs across the midpoint are preserved.

### 31D. Independent rebuild and exact certificate

New code: gap/verifier/claim31.cpp. It imports no producer implementation. It builds the six-column graph directly from the legal column pairs and degree rules, orders pending edges by row first, and labels only S paths. It counts total crossings Y directly rather than splitting them into w and wx. It then forms the endpoint-memory product implicitly. Every base row-start state is seeded with both parities; six phase sweeps generate the possible within-row memories. This is sufficient because the row-start memory has no older history.

The checker performs fixed-beta integer relaxation from potential zero at every augmented node. It uses no critical-cycle search or producer potential. A separate final pass verifies every reduced arc cost. Potentials use signed 16-bit storage with an explicit overflow guard; all arithmetic before storage is integer arithmetic of larger width. The observed range is far within the storage limit. Results:

| Graph | States | Arcs checked | Potential range | Row-boundary range | Minimum reduced cost |
| --- | ---: | ---: | --- | --- | ---: |
| base | 35,372,696 | 71,090,636 | — | — | — |
| up | 83,780,188 | 171,579,088 | -104..0 | -104..0 | 0 |
| down | 162,690,236 | 343,695,792 | -104..0 | -104..0 | 0 |

The state and arc totals independently reproduce the producer's totals despite different state numbering and pending-edge order. The full arc checks pass in both orientations. The complete run took about 320 seconds on one CPU process. Maximum resident memory was 1,842,736 KiB, about 1.76 GiB. I also set a 7 GiB virtual-memory limit. This stayed well below the requested 8 GB cap.

The producer source was read in full, including its bit encoding, degree checks, cycle handling, endpoint bits, reachable variants, relaxation, and final verifier. The independent rebuild is the second implementation requested for this audit. I did not run a redundant second copy of the large producer graph after the independent checks passed.

### 31E. Telescoping, eight halves, and exact arithmetic

Since every potential lies in [-104,0], summing the arc inequalities and dividing by four yields

    Y_H-m+2(b_H-m) >= 2 sum_H a-26.

The half walks partition the four full side scans. Their row counts total 4n; their Y and b counts give the full side totals, including all crossings assigned across the middle cut. The candidate endpoint intervals lie in the stated near and far halves and are disjoint. Extra penalties are nonnegative. Summing the eight inequalities gives

    2(A-R) <= D_T+208 <= E+12846.

The inherited square budget is 4n<=4E+2(A-R)+156. Therefore

    4n <= 5E+13002,
    5X >= 24n-13012.

All constants were independently recomputed with exact rational arithmetic. The rounded constant is 2603, since 13012/5=2602.4. The retained path ranges and side separation remain valid for every even n>=32; no new threshold enters the six-column scan.

### 31F. Optional sharpness in the stated relaxation

I extracted the producer's final critical fields and independently checked their degree rules, allowed column pairs, S acyclicity, crossing counts, and endpoint penalties in both phases. The up field has period six: Y=11, S crossings=10, b=6, and maximum sum a=5/2. Its ratio is (11-6)/(5/2)=2. The down field has period four: Y=7, S crossings=7, b=4, and maximum sum a=3/2. Its ratio is (7-4)/(3/2)=2; wx=0.

The periodic S-component check excludes finite cycles; on a period quotient, any such cycle would have zero winding and fit within the checked unroll bound. These fields confirm the coefficient limit of this relaxation. They do not prove that beta=2 is optimal in a model with all T components labelled, and that stronger assertion is not an input to the theorem.

### Evidence and next action

Reproduce the independent certificate from the research root:

    g++ -O2 -std=c++17 gap/verifier/claim31.cpp -o gap/verifier/claim31
    gap/verifier/claim31
    .venv/bin/python gap/verifier/claim31_local.py

Check for both PASS lines, the two [-104,0] ranges, and the stated checked-arc totals. An exit status alone is not the certificate. Logs are claim31.log, claim31_resources.log, and claim31_local.log/json. Source snapshots and hashes are in claim31_sources/ and claim31_source_hashes.json. The new checker keeps the graph and potentials in memory and records deterministic potential checksums; it does not require producer data arrays.

The author can update PROOF_R3.md and the result index to audited PASS with the explicit theorem above. No author file was edited. Claim 31 is complete; Claim 30 follows in the requested order.


## Claim 30: perfect squares, ribbon runs, and straight walls — 2026-10-03

**Audit object: gap/structures/STRUCTURE.md. Verdict: the local T1–T3 statements PASS, and T4 PASSES for full spanning 2-factors with the stated overlap exclusion. The stronger connected-domain/global-ribbon-word conclusion is FALSE as written.** The exact repair is one H/V bit per uninterrupted good ribbon run. A connected two-dimensional good domain can contain distinct runs of one ribbon with different bits. I give a counterexample in a validated closed tour below. T4 also needs an explicit global degree-two hypothesis; Section 0's arbitrary partial edge-set scope is too broad for that budget.

Both requested machine checks reproduce, including every advertised count. I also independently enumerated their solution sets using exact cover and the verifier's exact tile geometry, without CP-SAT or worker code. These checks support the corrected local statement; a defect-free torus cannot test the missing scope condition on domains with holes.

### 30A. Tile shape and T1

**PASS.** The a=(2,1) tile occupies BR in its left square and TL in its right square. The b=(1,2) tile occupies TL in its lower square and BR in its upper square. Reflection gives d tiles in RT of the left square and LB of the right square, and c tiles in RT of the lower square and LB of the upper square. These descriptions agree with the independent exact quarter sets.

Every tile therefore occupies one half of each of two squares that share its carried unit edge. The carried edge is one of that half's two axis-aligned legs. In a good square, tile multiplicities are one in all four quarters. A tile cannot cover only one quarter of the square. Thus exactly two complementary halves occur. Halves of different diagonal splits overlap in a quarter, so the two tiles have the same split. The possible partitions are exactly BR+TL and RT+LB.

If two adjacent good squares have different splits, no tile can be carried across their common edge: such a tile would require its own split in both squares. This implication does not assert that every same-split edge carries a tile, nor is that converse needed.

The hypothesis is *good*, meaning exact multiplicity one, not merely absence of an overlapping tile pair in a chosen patch. Crossing-free open patches can contain holes. The title should not be read as replacing this hypothesis by local absence of crossings.

### 30B. T2 is a run statement, not a connected-domain theorem

**PASS for T2(a) with “run” made precise.** In the slash class, the allowed half-square partner graph is

    ... BR(i,j), TL(i+1,j), BR(i+1,j+1), TL(i+2,j+1), ... .

It is a bi-infinite path with alternating a and b links. Restrict to an uninterrupted sequence of good halves on this path. Each good half has exactly one matched link. Once a link is selected, its neighbours are absent and the next links are selected, until the good run ends. Hence the selected tiles along that run have one common type, H or V. Endpoint tiles may leave the good domain; they fix the matching phase but do not justify propagating through a bad square. A finite segment has at most two compatible phases, not automatically two perfect matchings internal to the segment.

**PASS for T2(b).** For the full-plane construction defined by a word w on the integer ribbon indices, a point on diagonal d has exactly one edge toward d-1: the outgoing a edge if w(d)=H, or the incoming b edge if w(d)=V. It also has exactly one edge toward d+1, selected by w(d+1). This proves degree two. Each half-square ribbon is completely matched, so all quarters have multiplicity one and no selected tiles overlap. The audited tile lemma then gives zero proper crossings.

**PASS for T2(c) in that full ribbon field.** Each step changes d=y-x by one, and each vertex has one edge in either direction. Strands are monotone in d and traverse every ribbon once. The decreasing-d step is (2,1) for H and (-1,-2) for V. Since the bit depends only on d, translating by (1,1) maps a strand to the next strand. Reflection gives the other split. These conclusions concern the complete field constructed from one word; they do not identify the shapes or endpoints of arbitrary disconnected restrictions of its strands.

**FAIL for the Section 2 heading “a connected domain of one split is a ribbon field,” and for the same interpretation of the summary.** Connectivity of a two-dimensional good region does not imply connectivity of its intersection with every half-square ribbon. A domain can go around a bad portion of a ribbon and join two runs whose matching phases differ.

Here is an exact counterexample in the independently validated closed tour w-integrator/tours/FOLD24_n96.json (n=96, X=720):

* TL(2,2) is covered by the a tile of (1,2)--(3,3), so it forces H on ribbon k=1.
* BR(5,6) is covered by the b tile of (5,5)--(6,7), so it forces V on that same ribbon k=1.
* Both squares belong to one connected good slash domain. A path of good slash squares, listed by lower-left corner, is

      (2,2),(3,2),(3,3),(3,4),(3,5),(3,6),(4,6),(5,6).

All four quarters in every listed square have multiplicity one and slash split. Yet the ribbon between the two marked halves is interrupted by bad squares. For example, square (4,4) has multiplicities (0,0,2,2), square (4,5) has (2,2,1,1), and square (5,5) has (1,1,2,2), in B,R,T,L order. Thus this does not refute T2(a): the two bits lie on different good runs. It directly refutes one global word for the connected good domain.

The complete witness, its source hash, the good-square path, tile owners, and intervening multiplicities are in claim30_counterexample.json. claim30_counterexample.py validates the full Hamiltonian tour before checking these facts. The same diagnostic also finds incompatible runs in the n=98 tour and the n=166 field tour; only the explicit n=96 witness is needed for the refutation.

### 30C. T3: straight walls at good degree-two points

**PASS.** Tile sides are primitive lattice segments, so a lattice point cannot lie strictly inside one of them. A point in an adjacent square also cannot lie in a tile interior. At a good lattice point, the eight incident 45-degree sectors are therefore filled by tile corners. A knight-edge endpoint contributes 45 degrees, and an endpoint of a carried unit edge contributes 135 degrees. This gives

    45 deg_H(v)+135 b(v)=360.

At a degree-two point, b(v)=2. Good coverage also prevents two tiles from carrying the same unit edge at v, so b counts distinct carried unit edges there.

The circular binary split sequence has 0, 2, or 4 changes. Four changes would prohibit all four carried edges, contrary to b=2. Two noncollinear changes make one square differ from the other three. The two cases at an odd NE square exhaust the configurations up to lattice symmetries. If NE has backslash split, its LB half has both possible carried legs on walls and cannot be covered. If NE has slash split, the remaining S and W edges must both carry tiles; their d and c tiles both cover RT of SW, contradicting good coverage. Only zero changes or two opposite changes remain.

At a horizontal wall, the half adjacent to the wall must use its other carried leg, forcing an a or d tile. This forces H on the corresponding good ribbon run. A vertical wall similarly forces b or c, hence V. T2 propagates this condition only along the uninterrupted good run. It does not propagate across a defect or between distinct runs of the same ribbon.

Thus wall edges cannot turn, branch, cross, or terminate at a good degree-two point. Their straight segments can end at bad points or at the board boundary. The local conclusion and the forcing at wall contacts are valid. It does not bound the number of wall segments or defect contacts by a constant.

### 30D. T4: defects and the precise global hypotheses

**PASS with explicit scope.** Let H be a full spanning degree-two graph on the board (a closed tour is sufficient). Let U be a union of whole unit squares contained in D. Let B be a set of its crossing pairs such that *all tile overlaps of those pairs* avoid U. Then

    bad(U) <= G+2(X-|B|) <= 2E+2(X-|B|).

A square with one nonunit multiplicity has at least two, by the alternating-sum identity. Since U consists of whole squares, division by two gives

    number of bad squares in U <= E+X-|B|.

Taking B empty and U=D gives at most E+X bad squares globally. Triple coverage causes no missing term: each multiply covered quarter belongs to at least one crossing pair, and each pair supplies at most two overlap quarters. No extension of the estimate outside D is valid from this proof.

**Scope repair required.** Section 0 permits H to be an arbitrary edge set or part of a tour. T4 cannot use that scope with E=X-4n+2. The estimate G<=2E uses n² selected edges, which requires a full spanning 2-factor. For example, on n=32 the empty edge set has X=0, E=-126, and 961 bad squares, so “bad squares<=X+E” is false. State the global degree-two hypothesis at the start of T4. The final summary already restricts to closed tours, so this repair does not weaken its valid defect-count part.

“Bad” means a failure of exact tile coverage, including holes. It does not mean only squares containing crossing points or overlapping tiles. A good point is defined using all four incident squares; the wall conclusion applies only where those squares lie in D and are good. These conventions must remain explicit in later structure or defect-price arguments.

### 30E. Independent exhaustive checks and author reruns

I reran both supplied commands, with one worker and bytecode writes disabled. Both finished with OPTIMAL exhaustive enumeration and all their assertions passed. The independent checker claim30_checks.py imports no worker implementation and uses no SAT/CP solver. It uses exact tile quarters from prior verifier geometry and a complete exact-cover search.

For the plane check it lists the 24 possible tiles meeting the four squares around v. It covers their 16 quarters exactly once and imposes degree two only at v. It finds exactly 48 choices: 32 single split, 8 horizontal walls, and 8 vertical walls. All have two carried unit edges at v; the wall-direction tile types agree with T3.

For the 6-by-6 torus it uses the 144 undirected knight-edge orbits and their exact quarter sets modulo the period. It enumerates quarter exact covers with vertex degree at most two. A cover has 36 tiles, hence total degree 72; the degree upper bounds force degree two at all 36 vertices. Conversely, every crossing-free torus 2-factor is such a cover, by the tile-area identity. Period six is large enough that a tile has four distinct quarter orbits and there is no ambiguity between the distinct knight-edge directions. This enumerates the same model by a different method.

Results:

| Check | Total | Single split | Horizontal walls | Vertical walls |
| --- | ---: | ---: | ---: | ---: |
| four-square plane neighbourhood | 48 | 32 | 8 | 8 |
| 6-by-6 torus | 252 | 128 | 62 | 62 |

The 128 single-split torus solutions give every one of the 2 times 2^6 ribbon words. The other 124 have straight full horizontal or vertical walls, never both. The independent exact-cover search visited 119 nodes for the plane check and 3141 for the torus check. This is a complete enumeration, not a sample. It took about 0.14 seconds after startup.

Evidence: claim30_checks.py/json/log, claim30_tiling_author.log, and claim30_wall_author.log. The checks do not test arbitrary domains with bad squares; the full-tour counterexample in 30B explains why their success cannot prove that stronger conclusion.

### Exact wording repairs and usable theorem

Replace the Section 2 heading by “Each uninterrupted good ribbon run has one matching phase.” Replace “one H/V bit per ribbon” in the general-domain summary by “one H/V bit per maximal uninterrupted run of good halves on a ribbon; different runs of the same ribbon may have different bits.” Keep the full-plane word construction and its monotone-translate conclusion as the separate statement T2(b)–(c).

A valid replacement summary is:

> In a closed tour, at most X+E unit squares fail exact quarter coverage. Each remaining square has one diagonal split. On each uninterrupted run of good halves in a fixed-split ribbon, the covering tiles have one H/V matching phase. At a degree-two lattice point incident to four good squares, split walls are absent or form one straight horizontal or vertical line. Horizontal wall contacts force H, and vertical contacts force V, on their incident good ribbon runs. Wall segments end only at bad points or the board boundary. A complete defect-free single-split field is the full ribbon field of one word, whose strands are monotone translates.

At the start of T4 add: “Here H is a full spanning 2-factor, U is a union of whole unit squares inside D, and every tile overlap from B avoids U.” Add that definition of good to any title or informal use of “crossing-free parts.”

The corrected theorem is useful local structure. It does not prove one word per connected domain, an interface cost, a constant number of domains, or a private arch/flux price. In particular, a later carrier model must permit distinct bits at distinct defect-separated runs unless a new theorem relates them. The Claims 26, 27, and 31 lower bounds do not use the failed global-domain assertion and are unchanged.

No author files were edited. Claim 30 is complete. The proof author should apply the scope repairs before calling the full structure summary audited.


## Proof-size and finite-input profiles — 2026-10-03

These profiles apply Nil's coefficient/simplicity criterion to the recent audited results. Sizes are whitespace word counts of the current Markdown proof files, including displayed formulas, tables, and check commands. They measure the written argument, not formal proof length. The finite graph size is listed separately because a short reduction can still require a large computer check.

| Audit / coefficient | Written proof size | Essential new finite input beyond the shared tile and endpoint facts |
| --- | --- | --- |
| Claim 26: 52/11 | PROOF_52_11.md: 2,654 words, 385 lines | Two oriented width-two strip potentials; independent checker verifies 687,262 augmented cell arcs per orientation. Boundary overlap and corner duplication also have small exact geometric checks. |
| Claim 27: 204/43 | PROOF_N1.md: 3,515 words, 558 lines | Interval potential: 330 states, 580 hard inequalities. Combined row certificate: 40,158,400 augmented arcs per orientation. A four-bit history identity and a capped run counter are additional mathematical inputs. |
| Claim 31: 24/5 | PROOF_R3.md delta: 1,303 words, 208 lines; inherited Sections 1–3: 1,194 words, 195 lines. Total reading: 2,497 words, 403 lines. | Six-column joint certificate: 171,579,088 up arcs and 343,695,792 down arcs. The independent implementation uses about 1.76 GiB peak RSS. No interval potential or blocked-run automaton is needed. |
| Claim 30: local structure, no new coefficient | Submitted STRUCTURE.md: 2,060 words, 139 lines; scope repairs in Claim 30 remain necessary. | No large certificate. T1–T3 have elementary local proofs. The 48 plane configurations and 252 torus configurations are exhaustive corroborating checks, not premises replacing those proofs. T4 inherits the audited tile-area budget. |

The shared ingredients are the four knight-tile shapes, their one/two-quarter overlap rule, the local flux identity, the endpoint coefficient table, and the finite endpoint-loss cases. They have exact small geometric checkers and short finite case proofs. Counting them as shared does not remove them from a self-contained proof.

Claim 31 improves the coefficient and simplifies the written reduction relative to Claim 27, but greatly enlarges the certificate. Claim 26 keeps a much smaller graph. These are different simplicity tradeoffs; I do not discard the smaller-certificate route merely because its coefficient is lower. Claim 30's repaired ribbon-run statements offer a mostly hand-checkable structural input, but no 5n conclusion has yet been audited from them.

Optional optimality witnesses, diagnostic tour checks, and torus samples do not add premises to the stated crossing lower bounds. For each future audit, report the theorem, proof size, essential finite checks, and which checks are only corroborating. A hand proof or a small certificate can therefore remain valuable even after a larger computational bound is known.

## Claim 30 addendum: W1 local SAT/DRUP cross-check — 2026-10-03

**PASS for the precise 9-by-9 / central 3-by-3 statement.** I read the W1 model generator, fold-stack map generator, and standalone DRUP checker. I independently rebuilt the entire CNF in `gap/verifier/claim30_w1.py`, without imports from the authors. The rebuilt model has 424 edge variables, 7,144 clauses, and 156 excluded central maps. Its clause multiset equals the supplied CNF exactly. The independent crossing test solves the two segment parameters with integer determinants. Results and the CNF hash are in `gap/verifier/claim30_w1.json`.

The variables are every knight edge with an endpoint in the 9-by-9 core. Each core vertex has exactly two selected edges, each halo vertex at most two. Every strictly crossing pair of represented edges is forbidden. The central map records both incident edge directions at every one of its nine vertices. Each exclusion clause contains the negatives of all edges in one map; core degree two makes this equivalent to excluding that exact map. Duplicated literals from edges between central vertices do not affect the clause. Cycles are allowed, so the statement also applies to tours. Edges with both endpoints outside the core are absent; restricting a full configuration to represented edges gives the required relaxation.

I reran the standalone checker against both supplied proofs. Glucose: **2,942 RUP additions, PASS**. Lingeling: **2,989 RUP additions, PASS**. Both derive the empty clause. Logs: `gap/verifier/claim30_w1_glucose.log` and `claim30_w1_lingeling.log`. Thus every configuration meeting these window hypotheses has one of the 156 fold-stack maps at its centre.

**Scope unchanged.** This finite local theorem supports the local structure classification. It does not prove one ribbon bit throughout an arbitrary connected good domain, where bad squares can interrupt a ribbon. The full-tour counterexample in Claim 30B remains valid. Neither this CNF nor its proofs certify the subsequent global gluing/no-junction corollary as worded; any such use must specify complete translated window hypotheses and prove the gluing step. The four functional families in W1 are exhaustive **up to sign** within the stated search range; add those words to its definition paragraph (the source code already uses that convention).

**Proof-size / finite-input profile.** W1 supplies a short local reduction to a 424-variable, 7,144-clause CNF and two checked proofs of about 3,000 RUP additions each. One proof suffices for the theorem; the second is corroboration. It adds no lower-bound coefficient and does not replace Claim 30's required scope repairs. No large graph rebuild was repeated. Claims 29, 31, and 30 remain complete in the requested order; Claim 31's bound is unchanged.


## Claim 32 — RED TEAM: ribbon absorption toward 5n — 2026-10-03

**Verdict: GAP for the proposed 5n theorem; FAIL for an unconditional wall-face yield lemma.** The simpler route remains worth pursuing, but the supplied steps do not yet give a private price of 1/4 per original side end. I found an exact zero-crossing field that defeats R3 if its only correction is for defects. This is a counterexample to that intermediate geometric statement, not a closed-tour counterexample to X >= 5n-O(1).

Sources: gap/structures/PLAN.md point 2, FINDINGS.md G9–G10, STRUCTURE.md, and the audited tile/boundary budget. I also read G11's pilot description to distinguish its fixed straight-interface model from the proposed universal claim. Source hashes and sizes: claim32_sources.json. All checks were light, single-process checks; no optimisation or large graph job was run.

### 32A. PROVEN counterexample: a wall can send its strands to other walls for free

On the whole integer plane choose every edge

    (x,y) -- (x+2,y+1)     when y is even,
    (x,y) -- (x-2,y+1)     when y is odd.

Every vertex has one edge to the row above and one to the row below. Edges in one open horizontal slab are parallel; different open slabs are disjoint. The field therefore has degree two and no crossings. It is the fold stack with f=y and alternating choices (2,1), (-2,1).

Every square in an even row has slash split; every square in an odd row has backslash split. The tiles cover all quarters exactly once. Thus **every integer horizontal line is a wall and there are no defects anywhere**. All ribbons incident to a wall have the required H bit. The complete strands are explicitly

    P_k(y) = (k + 2*(y mod 2), y),    y in Z.

They are strictly monotone in y and stay between x=k and x=k+2. In a rectangle, all strands whose two x coordinates are strictly inside it run from bottom to top. They do not return to a vertical side. A horizontal wall segment can have arbitrarily large length while almost all its incident strands are of this type. Only O(1) strands near either vertical boundary can meet that boundary. No defect correction explains this loss, because there are no defects.

This breaks R3 as a statement that each face of length l yields l/2-O(defects) distinct same-vertical-side strands. It also breaks any attempt to price all wall faces independently: this field has arbitrarily many wall faces at zero crossing cost. The same strand meets arbitrarily many faces. The existence of many such faces cannot create many independent connectivity obligations.

Independent exact check: claim32_pleats.py enumerates 625 edges in a padded window, checks all crossing pairs (zero), verifies degree two at 144 core vertices and exact coverage at 576 core quarters, and traces three interior strands from bottom to top. Output: claim32_pleats.json. The formulas above prove the family for every size; the window check only corroborates it.

**Required repair.** Give each original side end a persistent label. At a wall, either prove a return to the same side, or transfer that label through a precisely defined strand/face relation. A face has a price only for labels that ultimately create distinct connectivity obligations. A wall-to-wall transfer is free in this example. Any number of such transfers must be handled without a separate O(1) loss per wall. If R3 was intended only for isolated chevrons already connected to one vertical side, state that hypothesis: deriving it from the general ribbon decomposition remains a new lemma.

The example is a full-plane field and an open-window restriction, not a closed Hamiltonian tour. It does not satisfy a specification of four cheap, closed board sides. It therefore leaves open whether global side conditions can force enough *labelled* returns. It shows that the asserted local geometry does not supply that conclusion by itself.

### 32B. PROVEN local propagation; GAP in the global end count and assignment

Claim 30's repair is essential here. A bit propagates along one uninterrupted good half-ribbon run. It need not propagate across a bad interruption, even within one connected good domain. The validated n=96 tour in Claim 30B has H and V on two runs of ribbon 1 in the same connected slash domain. Consequently, an end cannot be transported past that interruption using the full-plane word model. The interruption must be entered in the absorber ledger at that point.

For a straight uninterrupted ribbon that actually reaches perpendicular cheap sides, incompatible H/V requirements do force an interruption or wall encounter. This supports the local obstruction in R2. It does not establish the full accounting inequality as written. The count 4n-O(1) requires a defined scan curve with one side-end slot per row, including rows whose collar has defects or a non-cheap pattern. G10 optimises a side attached to a *fixed* exterior word; it does not prove that every arbitrary tour has this collar decomposition or price a nonperiodic side carrying current.

The revised count should map each of these fixed boundary slots either to one labelled good run or directly to a paid side exception. Count the first absorber of that label once. Do not count the two sides of an interior run as two new original side ends. Do not replace defect-separated runs by a single word. The statement “a defect cut absorbs at most two ends” can hold for a specified cut of a specified ribbon, but does not mean one bad square is one such cut: a slash square contains halves of two different ribbons.

### 32C. GAP: a price in crossings is not yet an extra price above 4n

There are two different baseline arguments. The area proof gives X >= 4n-2 from total tile area; it does not identify 4n particular crossing pairs that can simply be removed. The audited boundary certificate does identify a set B with |B| >= 4n-24. A clean sufficient version of the new route is therefore a total absorption allocation of at least n-O(1) supported on crossing pairs outside B, with total allocation at each such pair at most one.

Side repairs can also use surplus crossings inside B, but then they need one combined residual budget. For example, reserve a baseline of 4n-24 inside B and allow only its remaining capacity plus X-|B| to pay absorbers. The total available capacity is X-4n+24. A crossing counted in a side-strip objective cannot also pay a nearby defect or seam at full strength. Unit capacity is global across all absorber types, not merely within each type.

This distinction matters for holes. A bad square need not contain a crossing at all. T4 bounds bad squares in U by E+X-|B|, with E=X-4n+2. With only |B| >= 4n-O(1), that is at most 2E+O(1). It does not assign a distinct crossing unit to each defect. For illustration, even if one separately proved at most four end labels per bad square, this budget alone would give at most 8E+O(1) labels and hence only E >= n/2-O(1) from 4n labels. This is a diagnostic calculation, not a new certified bound. A stronger defect inequality or an explicit allocation is needed for E >= n-O(1).

The gentle-seam price of 1/4 per end has no spare capacity for duplicate labels or overlap with side charges. A finite band optimum with fixed exterior fields does not certify arbitrary bent, merged, or terminated defect sets. G11 itself records the width and period restrictions. Its zero-cost walls also require the global connectivity argument refuted in its unconditional form in 32A.

### 32D. Status of the proposed steps and smallest useful repair

| Step | Audit status |
| --- | --- |
| Good-run H/V propagation and local wall orientation | PROVEN, with Claim 30's run and degree hypotheses |
| Cheap arbitrary side implies the required labelled H/V collar | GAP; G10 supplies restricted model evidence |
| Every original boundary end reaches a first absorber | ARGUMENT until slots, collars, run interruptions, and transfers are defined |
| Every wall face yields l/2 same-side strands up to defect losses | FAIL without added global hypotheses; alternating horizontal walls are a counterexample |
| A fixed P-compatible chevron strand needs a changed edge end | PROVEN in Claim 28's fixed-matching scope |
| Changed-end price 1/2 | CERTIFIED for the fixed exterior, W<=4 model in Claim 28; universal version remains GAP |
| Every defect/seam/side absorber pays 1/4 privately | CONJECTURE; no general allocation is provided |
| Adding the absorber prices to 4n | GAP until one baseline-residual ledger is proved |

The next hand lemma should describe labelled side ends under wall-to-wall transfers, with no per-wall loss. It must explicitly pass the alternating-wall field above and Claim 30's interrupted-ribbon example. Only then is a finite defect-price search measuring the needed quantity. A sufficient final target is: at least 4n-O(1) original labels receive weight 1/4, and the total weight charged to all residual crossing capacity is at most that capacity. This target includes side, wall, and defect repairs in one inequality.

**Pareto profile.** No new lower-bound coefficient is proved or refuted here. The counterexample is a two-line edge formula with an elementary slab argument; its finite input is zero. The exact 625-edge check is optional corroboration. The proposed 5n route has short geometric components, but its unresolved global transfer and residual-budget lemmas cannot yet be counted as a short proof. It remains a useful primary target after these repairs.

Claim 32 is complete. No author files were edited. The outstanding mathematical work is to replace R3 by a labelled transfer/return lemma and then prove a joint extra-crossing budget.


## Claim 33 — W1 and W3 window encodings — 2026-10-03

**PASS for the precise finite window lemmas. PASS for their use in every tour when the core fits in the board and the stated crossing hypothesis holds.** I independently reconstructed the clause multisets, then reran every required DRUP proof. No encoding error was found. The broad wording needs the scope repairs below: a crossing need not be inside the core, one side's strip is different from the union of all four strips, and the depth >=4 extension uses the depth-6 certificates plus a translated interior window.

Evidence: `gap/verifier/claim33_windows.py`, `claim33_windows.json`, `claim33_windows.log`, and `claim33_sources.json`. W1 also uses the independent reconstruction `claim30_w1.py`, rerun for this audit. The new checker imports no author geometry or model code. All computations were light and sequential. No SAT search was necessary.

### 33A. Variable meaning and degree / halo constraints — PASS

Each variable is one undirected knight edge with at least one endpoint in the core. IDs are the lexicographic order of sorted endpoint pairs, starting at one. Interior windows include all eight possible moves at each core vertex. Side windows discard edges with a negative x endpoint, so x=0 is a genuine board side. Edges with both endpoints outside the core are not represented.

At every represented vertex, all negative triples of incident variables impose degree at most two. At a core vertex with incident list L, the positive clauses L minus {i}, for every i in L, impose degree at least two: zero chosen variables fails every such clause; one chosen variable fails the clause omitting it; two or more satisfy all of them. Together these clauses impose degree exactly two in the core. There are no connectivity or cycle constraints.

The width-two halo is the set of possible external endpoints. “Halo degree at most two” refers only to represented edges, not a requirement to complete the halo into a tour or to close it periodically. The four extreme corners of the bounding halo need not have any incident variable. Nothing requires every halo vertex to be used.

**Restriction of any tour is valid.** Retain all tour edges with an endpoint in the core. Every core vertex keeps both tour edges; halo vertices retain at most their two tour edges. Assign false to variables outside the physical board. This also works when the artificial halo extends outside the board. Only the core must fit. A true hole imposes the required absent edges, and the appropriate absence-of-crossings hypothesis imposes the binary clauses. Thus UNSAT proves the stated contrapositive for every closed tour. In fact these local lemmas apply to any degree-two graph on the core with the same degree bound outside, including disconnected 2-factors.

### 33B. Crossing and hole geometry — PASS

For each forbidden properly crossing pair, the CNF has the binary clause (-e,-f). Shared endpoints do not count. The independent checker solves the segment intersection parameters using integer determinants and requires both parameters to lie strictly between zero and one. This reconstructs every crossing clause, not a sample.

For W3 the quarter labels are b,r,t,l, relative to the square sides. A hole means that every edge whose tile covers that quarter is absent. The independent checker uses exact quarter centroids with denominator six and integer tile vertices scaled by six. It searches all possible covering edges in a box larger than the maximum tile span, verifies that all are represented, and reconstructs exactly four negative unit clauses for each quarter. The audited fact that each tile is a union of whole quarters makes the centroid test exact. This independent calculation also checks the result of the author's 0.33-offset floating-point test; the saved CNFs have the correct exact constraints.

For the side model, an allowed pair has **both edges incident to a vertex in columns {0,1}**. Either endpoint may be the incident endpoint. The clause test “both touch column zero OR both touch columns <=1” is equivalent to this condition, since the first case is a subset of the second. The model does not allow all pairs containing just one strip edge, and does not mean edges wholly contained in the two columns. Denote this permitted class by S_left. It is not automatically the union S* of four side classes.

### 33C. W1: central fold-stack map — PASS

The 9-by-9 core is {0,...,8} squared. The central block comprises the nine vertices {3,4,5} squared and their full incident-edge choices. The CNF forbids all crossings between represented edges. The four fold-stack families and all relevant binary level words produce exactly 156 distinct maps on these nine vertices. The independent reconstruction enumerates these maps without importing the author's list.

Each map is excluded by one clause containing the negatives of its chosen edges. Since each central vertex has degree exactly two, satisfying all chosen edges would give precisely that map; it cannot have extra edges there. Repeated literals for edges joining two central vertices are harmless. UNSAT therefore proves that every admissible window has one of the 156 maps.

The complete reconstruction matches 424 variables and 7,144 clauses. The Glucose proof verifies 2,942 RUP additions; the Lingeling proof verifies 2,989. Both derive the empty clause. One proof suffices; the second corroborates it.

**Scope repair.** State “the central 3-by-3 incident-edge map agrees with a fold stack.” This certificate alone does not prove one global word throughout an arbitrary connected domain. Claim 30's interrupted-ribbon repair remains in force. In the functional-family description add “up to sign.” Any global classification or no-junction corollary needs its own continuation argument and complete translated-window hypotheses. None is needed for the W3 certificates.

### 33D. W3: exact finite statements and checked proof sizes — PASS

Interior statement: let C={0,...,6} squared. If a quarter of [3,4] squared is a hole, there is a proper crossing between two selected edges each having an endpoint in C. All four quarter orientations are certified. The crossing point and other endpoints need not lie in C; endpoints can lie in [-2,8] squared.

Side statement: let C={0,...,11} times {0,...,8}, with no vertices at x<0. For d=4,5,6, a hole in any quarter of [d,d+1] times [4,5] forces a proper crossing outside S_left between two edges each touching C. I included all four depth-6 proofs, which now exist on disk, to close the depth-extension issue in the request.

| Window | Variables | Clauses per quarter | RUP additions in b,r,t,l order |
| --- | ---: | ---: | --- |
| 7-by-7 interior | 272 | 4,260 | 606, 773, 574, 427 |
| 12-by-9 side, d=4 | 496 | 7,918 | 682, 551, 563, 687 |
| 12-by-9 side, d=5 | 496 | 7,918 | 896, 435, 1,041, 734 |
| 12-by-9 side, d=6 | 496 | 7,918 | 784, 621, 633, 680 |

Every reconstructed CNF matches the supplied clause multiset exactly. Interior CNFs contain 3,192 degree clauses, 1,064 crossing clauses, and four hole units. Side CNFs contain 6,156 degree clauses, 1,758 forbidden-crossing clauses, and four hole units. The 16 W3 proofs verify 10,687 RUP additions in total. The checker validates each added clause by reverse unit propagation and derives the empty clause. Ignoring proof deletions is sound because every retained learned clause was already proved.

### 33E. Depth extension and union-of-sides scope — PASS with explicit hypotheses

The literal claim “all d>=4 among edges touching the same side-anchored 12-by-9 core” is too broad: that fixed core does not even contain arbitrarily deep target squares. Use the following argument instead.

For square lower-left coordinates (d,c), the translated interior core is [d-3,d+3] times [c-3,c+3], and all represented endpoints lie in [d-5,d+5] times [c-5,c+5]. If d>=7, every represented edge endpoint has x>=2, so no represented edge touches the left width-two strip. The interior lemma then forces a crossing outside S_left. At d=6 this reasoning does not work, because represented edges can touch column 1. The four depth-6 side proofs fill that case; depth-4/5 proofs alone do not supply it.

For d=4,5,6 use the side-anchored core [0,11] times [c-4,c+4]. Its endpoints have x in [0,13] and y in [c-6,c+6]. Provided this core lies on the board, the side lemma applies. Hence under the hypothesis “the only crossings are in S_left,” these holes are impossible. In an arbitrary tour they instead imply the existence of a nearby crossing outside S_left. No assumption about the tour beyond the represented window is needed.

To obtain a witness outside the **union** S* of four strips, keep the entire endpoint box away from the other three strips. The revised Turns Theory PLAN uses n>=128 and removes vertices within distance 32 of two adjacent sides. This is ample: if a square has depth 4–6 from one side outside these corner boxes, its side-window endpoints cannot touch another strip. If the square has depth at least seven from every side, the interior-window endpoints touch no strip at all. Under these conditions every endpoint of the witness pair is within L-infinity distance at most ten of the target square's centre. The informal “about six” is not established by the side-window certificate; radius ten is a safe explicit replacement.

At multiplicity at least two, the audited tile lemma supplies a crossing directly. A tile from an edge incident to columns {0,1} has no area at square depth >=4, since that edge reaches column at most three. Thus the same strip exclusion holds for an overlapping quarter at these depths. Together with the hole lemmas, this proves bounded support for bad quarters in the stated middle region.

The proof does not give distinct crossings to distinct holes or paths. It does not prove a private price, a Hall condition, or a finite decision procedure for an arbitrary number of paths. Those allocation claims remain open. The shallower-depth SAT witnesses and the separate B-only threshold were not needed or audited in Claim 33.

### Repairs and Pareto profile

Required wording repairs: retain the exact central-map scope of W1; specify represented halo degree; say “crossing between edges touching the core”; distinguish S_left from the four-side union; include d=6 and translated interior windows in the d>=4 statement; use a safe explicit radius and exclude corner interactions before asserting an off-S* witness. The current Turns Theory support discussion already includes d=6 and radius ten, and its support conclusion passes under the stated window and corner hypotheses.

The W1/W3 source sections total 1,028 whitespace words and 74 lines as read on 2026-10-03, including ancillary claims not used here. Their essential finite inputs are one W1 CNF plus one of its two DRUP proofs, and 16 W3 CNF/DRUP pairs. The largest CNF has only 496 variables and 7,918 clauses. There is no large state graph and no new crossing coefficient. The geometric scope and translation argument are short; the allocation problem is not solved by these certificates.

Claim 33 is complete. No author files were edited.


## Claim 34 — Gap Lemma red team and W1 comparison closeout — 2026-10-03

**FAIL: the strong gap-half lemma.** A validated closed 16-by-16 knight tour has an absorbing cut with five gap halves but only **one** bad quarter in their union. Every gap square is at distance at least five from the board sides, so the intended side-collar exclusion does not fix this counterexample.

**GAP / CONJECTURE: the original gap-square Hall lemma.** The counterexample does not refute that version. I found no counterexample to it in the limited searches below; this is not a proof. **PASS: the independent W1 comparison reproduces 200, 164, 156 central maps at R=1,2,3.**

GAP_LEMMA.md was absent at the first read and appeared during the search. I then used its precise definitions, strong version, and intended cost application. A copy of that 1,049-word, 75-line draft is saved as `claim34_GAP_LEMMA_reviewed.md`. Source hashes are in `claim34_sources.json`. No author files were edited.

### 34A. Closed-tour counterexample to the strong version — PROVEN by explicit witness

File: `gap/verifier/claim34_tour_n16.json`, in the repository's standard two-direction-code tour format. It has 256 vertices, 256 undirected knight edges, one connected cycle, and X=318 crossing pairs. The solver-free checker `claim34_validate.py` checks degrees, board containment, knight moves, connectivity, exact quarter coverage, endpoint bits, and the claimed cut. It also calls the prior independent tour checker on the standard encoding. The full edge list and cyclic order are in `claim34_closed_tour.json`.

The backslash-chain cut is

    RT(6,9), LB(7,9), RT(7,8), LB(8,8), RT(8,7), LB(9,7), RT(9,6).

Its two endpoint squares are good. The initial half RT(6,9) is covered by the d-tile of edge (6,10)--(8,9), so its bit is H. The final half RT(9,6) is covered by the c-tile of edge (9,8)--(10,6), so its bit is V. The five intervening squares are all bad. Hence this is an absorbing cut under the draft's definition, with two absorbed ends.

| Gap half | Multiplicities (B,R,T,L) in its square | Bad quarters in that half |
| --- | --- | --- |
| LB(7,9) | (1,0,0,1) | none |
| RT(7,8) | (2,1,1,2) | none |
| LB(8,8) | (1,1,2,2) | L only |
| RT(8,7) | (2,1,1,2) | none |
| LB(9,7) | (1,0,0,1) | none |

Thus the union of the gap halves contains exactly one bad quarter, L(8,8), of multiplicity two. The strong inequality already fails for the singleton set K containing this cut: 1 < 2|K|. Sharing between different cuts is not needed to break it. In contrast, the five gap **squares** contain ten bad quarters.

The tour has five absorbing cuts in total. My independent bipartite matching check finds 10/10 assigned quarters for the square version and only 9/10 for the half version. The author's current scanner agrees when run on this tour with ALLCUTS=1: square matching 10/10, half matching 9/10, and one cut with fewer than two bad quarters in its own halves. See `claim34_cluster_author.log` and `claim34_validation.json`.

**Repair:** remove the strong half statement. Any proof must allow bad-quarter assignments to leave the chain half and enter the rest of a gap square. The original square statement permits precisely that repair. The witness does not show that the square statement is sufficient to finish the global absorption route.

### 34B. Search model and limits of the square-version evidence

`claim34_gap_search.py` independently constructs all knight edges touching a square window's vertex core, with exact degree two on that core and degree at most two on the endpoint halo. Quarter multiplicities use the verifier's exact tile geometry. For every candidate chain interval it can select an absorbing cut only if the endpoint halves are good with different bits and every intervening square is bad. All cuts are generated in one fixed direction, without reversed duplicates.

The model selects an arbitrary subset of candidate cuts. It counts each bad quarter in their allowed union only once, then asks for 2 times the number of selected cuts to exceed that count. This tests a Hall deficit directly; it does not merely count single cuts. Local SAT witnesses are not automatically tours. I therefore completed the half-version witness to a closed tour using a circuit constraint, then validated it without the solver.

Results, one worker per job:

| Window of unit squares / maximum gap length | Version | Result |
| --- | --- | --- |
| 3-by-3 / 4, 28 candidate cuts | square | INFEASIBLE, about 0.10 s |
| 3-by-3 / 4, 28 candidate cuts | half | INFEASIBLE, about 0.14 s |
| 4-by-4 / 6, 88 candidate cuts | half | Counterexample found, about 0.43 s |
| 4-by-4 / 6, 88 candidate cuts | square | UNKNOWN after 20 s |
| 5-by-5 / 8, 200 candidate cuts | square | UNKNOWN after 30 s |

The small INFEASIBLE results are bounded CP-SAT checks, not general proofs or separately checked DRUP certificates. UNKNOWN is no evidence of impossibility. The square conjecture remains open. The saved tour demonstrates why passing four construction-family tours was insufficient for the stronger conjecture.

Definition repair: regard a cut and its reverse as one cut, or require the displayed forward chain orientation. Otherwise a set of sequences could count the same physical gap twice. The scanner uses the forward convention. Also, when applying an interior version, every gap square must satisfy the distance condition, not just the first square to which cluster_scan assigns its two ends.

### 34C. Conditional use of the square lemma in the mixed cost — PASS

For the exact cost identity, define X1(t) as the number of one-quarter-overlap crossing pairs whose overlap quarter is t. Define W3(t)=binom(m_t-1,2) when m_t>=1 and zero at a hole. In particular, do not evaluate the polynomial at m_t=0. With quarter shares of all crossing pairs outside B,

    sum_t c(t) = (G+X1+W3)/4 + (X-|B|)/2
               = E/2 + (X-|B|)/2.

Using E=X-4n+2 and R=|B|-4n gives the exact equality

    E = sum_t c(t) + R/2 + 1.

If the draft's X1 brackets mean only a Boolean indicator, they undercount multiple pairs at a quarter. The stated lower-budget inequality remains valid with that smaller cost, but the exact identity requires the count above.

A hole has cost at least 1/4. At a multiply covered quarter with an overlap pair outside B, that pair contributes at least (1/2)*(1/2)=1/4, because a crossing overlap has at most two quarters. For gap squares at distance >3 from all sides, no B overlap reaches them. Thus, **if the square Hall lemma is proved**, two distinct assigned bad quarters per cut give at least 1/2 per cut, or 1/4 per absorbed end, without spending that quarter twice. This deduction is sound and does not require the false strong version.

The mixed identity is already a residual-budget identity above 4n; it should not be added again to another independent copy of the baseline. Nor does this conditional result establish that 4n-O(1) original side labels become absorbing cuts. Walls, same-bit gaps, side exceptions, and free transfers still require the global accounting identified in Claim 32. The half counterexample and the conditional square price are separate issues.

### 34D. W1 comparison and Claim 30 closeout — PASS

I read `w1_compare.py`. It imposes exact coverage on the (2+2R)-by-(2+2R) square window and degree two at its (1+2R)-by-(1+2R) interior lattice points. It counts the incident-edge maps at the central 3-by-3 vertices. It does not impose degree bounds at other points. These are the local T1–T3 hypotheses, not the same model as W1's crossing-free 9-by-9 core.

The author's full-solution enumeration at R=3 was stopped to keep the check light. Instead, `claim34_w1_check.py` builds the model independently from exact tile quarters and enumerates only **new central maps**. It first excludes all 156 fold-stack maps, then excludes each additional central map as found. The final residual model is INFEASIBLE for every R. Separately, the checker constructs a full-plane extension for each fold-stack map and verifies all finite-window degree and quarter constraints. This proves both inclusion directions in each tested window.

| R | Edge variables | Fold-stack maps | Extra maps | Total central maps |
| --- | ---: | ---: | ---: | ---: |
| 1 | 80 | 156 | 44 | 200 |
| 2 | 168 | 156 | 8 | 164 |
| 3 | 288 | 156 | 0 | 156 |

The projected searches took about 1.47, 0.35, and 0.08 seconds respectively, excluding setup. Outputs: `claim34_w1_check.json/log`. These are exhaustive finite comparison checks. They support the new dictionary in STRUCTURE.md Section 5b, but do not identify the hypotheses of its model with those of W1 or prove a global word per connected domain.

The current STRUCTURE.md explicitly incorporates Claim 30's repairs: one bit per uninterrupted run, T4 restricted to a full spanning 2-factor, and the corrected summary. The prior connected-domain objection is resolved in that revised text. The old counterexample remains a useful test against reintroducing the stronger statement.

**Pareto profile.** The 1,049-word gap draft is still a conjecture in its square form and false in its strong form. This audit adds no lower-bound coefficient. Its decisive finite input is one explicit 16-by-16 tour plus a short exact witness check; no solver trust is needed to verify the counterexample. The W1 comparison uses three small finite models, with at most 288 edge variables, and a direct fold-stack extension check. The next mathematical task is a square-level assignment proof that explicitly permits off-half quarters and handles sharing; the false half lemma must be removed first.

Claim 34 is complete. All computation started for this audit has stopped.


## Claim 35 — rational-shear wall witness and L2 scope — 2026-10-03

**PASS: the 19-edge periodic witness achieves 1/2 crossing per row, has nonzero transverse psi jump, and admits perfect exteriors.** I give an explicit extension to the whole plane, stronger than the supplied finite-cylinder feasibility result. The extended graph has degree two everywhere and no finite cycles.

**GAP: the advertised disproof of L2-v3 at p=2/3.** The example refutes a universal price above 1/2 for unrestricted charged paths across a straight wall. It does not provide the closed tours, actual retained candidates, or unbounded total deficit required to refute L2-v3. The sentence “the 16n/3 route via flux alone fails as stated” is not established for the current skeleton's quantifiers.

Evidence: `claim35_wall.py/json/log`, `claim35_extension_author.log`, `claim35_witness_author.log`, and `claim35_sources.json`, all in gap/verifier. The independent checker imports the verifier's exact tile geometry, not the author's model or witness checker. I read the rational-shear geometry and row-weight code and reran both small author checks. I did not rebuild the 10.6-million-state minimum-mean graph. Thus this audit proves an achievable rate of 1/2; it does not independently certify that no cheaper witness exists in that finite model.

### 35A. Exact periodic graph, degrees, cycles, crossings — PASS

Use the 19 listed edges and translate them by T=(2,4). Write

    u(x,y)=x-floor((y+1)/2).

Modeled vertices have 0<=u<4. Each represented edge has a modeled endpoint, every modeled vertex has degree two, and every other endpoint has degree at most two. There are exactly 19 distinct edge orbits; no duplicate edge is hidden by the period.

To check cycles for all periods, I form the finite quotient graph and retain the integer translation of each edge. It has three components, all paths, on 8, 6, and 8 vertices. Their edge counts are 7, 5, and 7. Hence every lifted component of the represented band is a finite path; no finite cycle can be concealed beyond an unrolling cutoff. This is stronger than merely finding no cycle in a long finite sample.

There are exactly two crossing-pair orbits. Representatives, assigned by the later lower endpoint row, are

    (1,0)--(3,1) with (2,0)--(3,2),
    (2,0)--(3,2) with (2,1)--(4,2).

Both overlaps contain two quarters. There are no one-quarter crossings. Therefore X=2 per four-row period, or 1/2 per row. Since T advances four L-infinity levels along a ray in the region y>x, the rate is also 1/2 per such level. This is a count of unordered crossing pairs, even though the two pairs share one edge.

### 35B. Quarter multiplicities and psi — PASS

I independently enumerate every tile that could cover each tested square. A square is complete exactly when every such tile has a modeled endpoint. The complete-column intervals alternate in width because the witness starts at shear phase one.

Quarter order below is B,R,T,L. Unlisted complete squares have multiplicities (1,1,1,1).

| Square row y | Complete x columns | Non-perfect square and multiplicities | Left-to-right omega sum | psi mod 3 |
| --- | --- | --- | ---: | ---: |
| 0 | 0,1,2,3 | x=2: (1,1,2,2) | 2 | 2 |
| 1 | 1,2,3 | x=2: (2,2,1,1) | -1 | 2 |
| 2 | 1,2,3,4 | x=3: (1,1,0,0) | -4 | 2 |
| 3 | 2,3,4 | x=3: (0,0,1,1) | -1 | 2 |

The first and last complete square in every row are perfect margins. The period has four uncovered quarters and four doubly covered quarters, with no multiplicity above two. These statements initially concern complete squares only; the bare 19-edge band leaves incomplete exterior squares uncovered.

For a horizontal dual step from square (x-1,y) to square (x,y), the lattice endpoint on its left is (x,y+1). The audited residue formula gives

    omega = (-1)^(x+y+1) * (m_R(x-1,y)+m_L(x,y)+1) mod 3.

Summing across the complete interval gives the table. The C++ row check omits a common checkerboard sign depending on the row/frame; that does not change the zero-versus-nonzero test. The supplied verify_witness.py does not itself print or test psi, despite its descriptive header. The independent computation above fills that omission.

### 35C. Perfect exterior: finite check and explicit infinite construction — PASS

I reran `extend_witness.py 2 8`. It reports 160 cylinder vertices, 416 free edge variables, 38 fixed witness edges, 336 quarter constraints, and OPTIMAL feasibility. Its period is (4,8). It imposes degree two away from its soft outer boundary and exact coverage on the specified inner exterior squares. It allows cycles. By itself, this finite-window result would not prove an infinite perfect extension or acyclicity.

There is, however, a direct extension. Let f(x,y)=x-y and define the full-plane fold stack by

    c[t]=(-1,-2) for even t, and c[t]=(2,1) for odd t;
    neighbours of v are v+c[f(v)] and v-c[f(v)-1].

Keep every translated witness edge. Add every edge of this fold stack whose two endpoints are outside the modeled band. The same stack is used on both sides. **Exterior-phase scope:** this is an alternating zigzag field with strand direction (1,-1). At every exterior vertex, one incident edge has move class (2,1) and the other has move class (1,2). It is not a pure straight (2,1) or pure straight (1,2) field. The achieved 1/2 rate is verified for these two matching zigzag exteriors; this audit does not certify the same rate with prescribed pure straight exteriors. The reported straight-field extension infeasibility tests are outside this audit. No knight edge can jump from u<0 to u>=4 without a modeled endpoint, since its u displacement is at most three.

For each of the four row phases I checked every external vertex that could have an edge into the band (u=-3,-2,-1 and u=4,5,6). Its fold-stack neighbours inside the band are exactly its fixed witness neighbours. Thus the union has degree two everywhere. Away from this finite transverse interface it is precisely the full-plane fold stack.

The exact check covers a 24-column transverse range through all four row phases: 96 vertex degrees and 384 quarter multiplicities. Every quarter outside the complete band squares is covered once; complete-square multiplicities remain those in 35B. This range contains the entire interface and every tile that can meet it. Beyond it, perfect coverage follows from the fold-stack formula. There are no additional crossing pairs. This proves two perfect infinite exterior regions, not just a fixed number of perfect collar columns.

For acyclicity, orient the fold-stack strands by increasing f. The even step (-1,-2) leaves u unchanged; the odd step (2,1) increases u by one or two. Therefore u is nondecreasing and increases over every pair of steps. An exterior strand cannot leave the band and return to it while staying in that exterior half-plane. Each finite witness-band path attaches to two infinite exterior tails. Together with the quotient-path check in 35A, this excludes finite cycles in the full-plane extension.

### 35D. What the price obstruction proves

In the extended plane, all crossings and waste are confined to this wall. Each four-row period has

    crossings = 2,   holes = 4,   X1 = 0,   W3 = 0.

Consequently, the mixed local currency lambda*X+(1-lambda)*(G+X1+W3)/2 is exactly two units per period for every lambda. At lambda=2/3, this is 4/3 from the two crossing pairs plus 2/3 from the four holes. Pure crossing capacity is also two units per period. No claim about a finite board's global E is needed for this local calculation.

Take M consecutive charged transverse paths, one per row, in this plane field. For a fixed support radius, their entire eligible atom union contains at most M/2+O(1) capacity, because there are only two capacity units per four wall rows and the radius adds only a bounded number of rows. A requested price p>1/2 therefore has an unbounded Hall deficit (p-1/2)M-O(1). This refutes the broad straight-wall rule even with one total constant allowance.

The paths need not be very small. The standard corner-path shapes

    gamma_R: (R+1/2,3/2) -> (R+1/2,R+1/2) -> (3/2,R+1/2)

cross this wall on their top arm for large R; the other arm lies in a perfect region. The checker explicitly verifies residue 1 for R=12,...,80 in the extended plane. Periodicity and the perfect-region residue zero explain the continuation. Thus restricting the geometric radii to start at 12 does not by itself remove this open-plane obstruction.

### 35E. Why this does not yet refute L2-v3 — GAP

L2-v3 quantifies over closed Hamiltonian tours on even boards n>=128. Its demanded family is the **actual retained** family after the endpoint-residue tests and both exception exclusions. It permits a single unknown finite total deficit C_flux, independent of n and the tour. Its eligibility rule requires the entire atom support to be within radius ten of one path vertex. The revised pure-crossing proposal at the top of PLAN.md keeps these family and error requirements.

The witness and its infinite extension establish neither of the following necessary facts:

1. A family of closed tours can contain arbitrarily long copies of this wall, while linearly many corresponding corner paths pass the actual retention tests.
2. Completing the sides, corners, and one-cycle connections adds only O(1) eligible capacity to the selected Hall family, rather than enough linear capacity to pay its deficit.

Both are material. The perfect infinite exteriors have no board-side degree conditions. Cutting them at x=0 and y=0 does not produce a tour. Nor may an arbitrary charged path be substituted for a retained candidate. All edges in the explicit plane construction have move class (2,1) or (1,2), so they preserve x+y modulo three; a Hamiltonian completion necessarily uses additional structure. No cost or support estimate for that structure is supplied here.

A finite completed example with a positive deficit would still not refute the quantified theorem: C_flux could cover that fixed deficit. A valid disproof needs an unbounded family of completed-tour deficits, or a theorem that embeds these wall patches while controlling both retention and all extra eligible atoms. I have not proved or assumed such an embedding.

**Required wording repair:** “A straight (1,2) wall between perfect infinite regions achieves rate 1/2 and refutes an unrestricted charged-path private price p>1/2. It is a candidate obstruction to L2-v3; closed-tour completion, actual retained-path density, and the total eligible-capacity bound remain open.” Do not mark L2-v3 or the current 16n/3 reduction false on this evidence alone.

**Pareto profile.** Source Section 7.1 is 523 words and 39 lines as read. The verified construction needs only 19 edge orbits, four exact row checks, a three-component quotient graph, and a two-letter exterior formula. The cylinder solver is now corroboration rather than an essential input. The large minimum-mean certificate is not needed to prove the achieved upper rate and was not audited here. No new finite-board lower or upper coefficient follows without the missing global completion argument.

Claim 35 is complete. No author files were edited, and all checks have finished.


## Claim 36 — SHEET connectivity red team — 2026-10-03

**FAIL for the original requested (B), and FAIL for the trapping premise of (C).** The already audited FOLD tour family is a counterexample to the proposed current-tour count: W=3n-O(1), but SSR=2n/3+O(1), so W-2SSR=5n/3-O(1). No absolute constant repairs (B). The reason is simpler than a new defect gadget: the construction's arch flips make one end of each long chevron an exception. Its other end can still generate a wall label, but the chord is excluded from the draft's SSR definition, which requires two cheap ends.

For (C), periodic corridor returns connect the opposite phase of the cheap collar matching. They coexist with unchanged cheap collars in one closed tour. They are not P-compatible chevrons and do not form the isolated cycles used in Claim 28. This refutes the stated trapping explanation, not every possible 1/2 lower price for those chords.

**FAIL for (A)'s literal label count. GAP for (D)'s separate prices and capacity assignment.** The final algebra is correct if its premises are supplied, but those premises need revision. No counterexample to X>=5n-O(1) is claimed.


**Version scope.** SHEET.md changed during this audit. Its revised (B) is BQ+2SSR+2EXC>=4n-O(1), and it introduces I for the previously undefined interface labels. The counterexample below refutes the original 2SSR>=W-O(1), which the author has now withdrawn; it does not refute the revised BQ inequality. The revised inequality and B0 remain GAP. Section 36E audits the new barrier argument and records a separate error there. The saved 2,874-word, 171-line source is the revised version.

Sources: SHEET.md, saved as claim36_SHEET_reviewed.md; the audited FOLD construction in Claim 12; its independent assembler claim12_full.py; and the saved n0=96 template. Hashes are in claim36_sources.json. All new checks were light, single-process geometry and graph checks. No optimisation was run.

### 36A. A convention issue that changes the main count — FAIL

The draft gives a label to each **cheap** slot only. An exception slot has no starting label. W,D,X_E count the destinations of these cheap-slot labels. Even if all labels terminate as intended, the literal identity is

    W + D + X_E = number of cheap slots
                = 4n-O(1)-EXC,

not (A). The draft's pleat-stack row silently changes the convention by setting X_E=4n when every starting slot is an exception. Under the stated definition all three counts would instead be zero.

A repair can give an exception slot its own immediately absorbed label, or retain EXC explicitly. The price and multiplicity of an exception absorber must then be reconsidered: its own label and incoming ribbon labels cannot be counted under incompatible conventions.

There is also a missing stopping case. After a bad interruption the next good square may have the other split. This is neither a same-bit continuation on the old chain nor an absorbing cut with two good halves of that chain, and it is not a direct wall face between good squares. The scanner below records this case as UNDEFINED rather than silently making it a wall. The revised draft now calls this fourth label type I, which addresses this stopping case. Its amended equality still omits EXC from the starting-label count.

### 36B. Counterexample to the Sheet Lemma using audited closed tours — FAIL

I used the n0=96 FOLD construction from Claim 12, which is already proved to give a closed Hamiltonian tour for every n=96+48k. These tours are also spanning 2-factors, as required by (B). I rebuilt n=144,192,240,288 with the prior independent assembler and validated each tour again. The n=96 saved tour was checked directly.

For reproducibility I made the collar convention precise: d=3; a slot is cheap when every incident edge at local columns 0,1,2 in rows y-3,...,y+3 agrees with P or P'. In the left P frame the neighbours are

    (0,y): (2,y+1), (1,y+2);
    (1,y): (3,y+1), (0,y-2);
    (2,y): (4,y+1), (0,y-1).

P' reverses the row direction. Reflections/transposition give the other sides. Interior vertices have both coordinates in [3,n-4]; interior squares have lower-left coordinates in [3,n-5]. Chord ends use the row of the exterior endpoint of the cut edge, consistent with the two ports per row in the fixed-field strip convention. Labels start at the corresponding first interior half and are followed exactly along their half chains.

The chosen collar is a concrete version of the draft's intended window. Changing a fixed depth or the bounded offset used to name a port changes only O(1) rows at the finitely many collar phase boundaries in this family. It does not change the coefficients below.

| n | Cheap slots | W | D | Undefined continuations | SSR | W-2SSR |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 96 | 205 | 195 | 3 | 7 | 47 | 101 |
| 144 | 349 | 339 | 3 | 7 | 79 | 181 |
| 192 | 493 | 483 | 3 | 7 | 111 | 261 |
| 240 | 637 | 627 | 3 | 7 | 143 | 341 |
| 288 | 781 | 771 | 3 | 7 | 175 | 421 |

These finite deficits alone would not refute an unspecified O(1). The periodic geometry explains their unbounded growth:

* On each side the construction flips the cheap U-turns on an interval of length n/4. The remaining 3n/4-O(1) slots are cheap. Their H or V ribbon labels reach a midline wall. Diagonal corridor cells run parallel to these ribbons; only O(1) ribbons near the corners or the fixed patch windows are affected. Thus W=3n-O(1).
* Long midpoint chevrons have one end in the flipped interval and one in the unflipped interval. Their interior geometry remains a return, but they are **not SSRs under SHEET's current definition** because one endpoint is not cheap.
* The remaining bulk returns come from the four period-six diagonal corridors. Each corridor period has exactly six path components: one A-to-A return, one B-to-B return, and four A-to-B through paths. A and B denote the pure (2,1) and (1,2) arms of the corner. The quotient components each have five vertices and four edges, so there are no hidden long through components. Every corridor has n/12+O(1) periods. Therefore its two same-side returns per period contribute n/6+O(1), and all four contribute SSR=2n/3+O(1). The finitely many patch windows affect only O(1) chord ends.

The finite corridor claim is independently checked in claim36_corridor.py/json: all four saved templates have 24 edge orbits and the stated six paths. Translating a corridor period by (6,6) preserves these connections; pure-field arms extend them to the same two board sides. The global tour existence and the fixed number of patch windows are the already audited Claim 12 facts. Hence the asymptotic count is not an extrapolation from the five rows of the table.

Consequently 2SSR=4n/3+O(1), while W=3n-O(1), disproving (B). The sample counts satisfy W=3n-93 and SSR=2n/3-17; the exact constants are diagnostic and are not needed for the counterexample.

Evidence: claim36_scan.py, claim36_scan.log, claim36_initial_scan.json, claim36_family_scan.log, claim36_scan.json, the four generated claim36_FOLD_n*.json tours, and claim36_corridor.py/json/log. A separate diagnostic on the saved n=166 FIELD tour also gives a positive deficit (W=306, SSR=66), but is not needed for the infinite-family argument.

**Repair:** distinguish reference returns before a repair from current chords after the repair. If a wall label is to be covered by a current return with an exception endpoint, count that object and route its charge to the exception budget. Alternatively add an explicit wall-label loss term to (B). An O(1) defect term cannot fix this example. Any exception term must share capacity with the exception labels already charged in (D).

### 36C. Actual same-side returns need not be trapped by P — FAIL for the stated premise

The same corridor check gives an explicit non-chevron return. In frame zero, one lifted A-to-A corridor path is

    (0,3), (2,4), (1,2), (-1,1), (-3,0).

Its two A-line labels c=x-2y are -6 and -3. Every translate by (6,6) gives the same pairing phase. The corresponding returns in the actual FOLD tours have two cheap endpoints; the large-board checker traces them as maximal interior chords.

The cheap collar matching is

    P(c)=c-3 for even c, and P(c)=c+3 for odd c.

The corridor returns instead pair an even line c with c+3. Let I denote this opposite matching on one residue-class chain. Then for even c,

    P(I(c)) = c+6.

Thus alternating the unchanged collar matching and these return chords advances along a chain. It does not close each return and a partner into the isolated component used in Claim 28. The finite ends of these chains connect through the construction's bounded patches; the resulting graph is one Hamiltonian cycle.

This is a direct counterexample to “same-side return with two cheap endpoints implies the P-compatible trapping relation.” There are linearly many such returns and no changed cheap collar at their endpoints. Claim 28's trapping proof depended on the **fixed chevron interior matching**, not merely on the names of the sides at the two ends.

The corridor contains crossing defects and pays a substantial cost. Therefore the separate assertion that every such return can receive 1/2 from a suitable joint budget is still GAP, not disproved here. It would need an interior-repair or chord-matching price theorem. It cannot be justified by counting changed side ends alone.

### 36D. Baseline and joint capacity — GAP, with an exact safe budget

The mixed cost c=c_{1/2} is not simply the count of non-B crossing pairs. With W3 zero at uncovered quarters and X1 counted with multiplicity at its quarter,

    sum c = (G+X1+W3)/4 + (X-|B|)/2,
    E = sum c + R/2 + 1,       R=|B|-4n.

This is already a budget above the 4n baseline. Its atoms include holes as well as fractional crossing contributions. Spending disjoint crossing pairs is not, by itself, enough to show that a Gap-Lemma allocation in c and a second pure-crossing repair allocation have disjoint capacity. The same outside crossing contributes to c, and the hole/waste part has already used the global excess identity.

A safe formulation puts the D-label, exception, and return payments into one allocation on c, plus a controlled allocation from the boundary-surplus term R/2. Prove that their total is at most that budget. A side proof granting a full unit of boundary surplus cannot be appended automatically: this particular decomposition exposes only half that surplus separately; the other half is represented in the mixed identity. A different decomposition is possible, but its reserve must be explicit.

Further, one changed local row can make several overlapping width-seven slot windows exceptions. Claim 28 certifies a price per changed **pairing end** in its fixed strip model, not a price per exception window. The claimed >=1/2 per exception slot needs an independent packing or allocation proof. Enlarging the starting-label set to fix (A) also changes how many labels an exception absorber receives.

With genuinely disjoint allocations the final inequality in (D) would be valid. The present draft has no such allocation, and the false current-return count cannot supply it. Lemma F's development on good regions does not fix this: the actual corridor returns pass through bad squares, precisely where that good-region hypothesis stops.

### 36E. Revised barrier argument: wall edges do not block strands — FAIL for that proof step

The revised Section 6 says a wall edge carries no tile, so no tour edge crosses it, and then assigns no crossing capacity to the wall part of a chamber boundary. The first statement concerns proper intersection with an open unit edge. It does not imply the second statement about strands.

Consider the exact crossing-free fold stack with f=y, choosing c[y]=(2,1) for y<0 and c[y]=(-2,1) for y>=0. Squares below y=0 have slash split; squares above have backslash split. All quarters are perfect and every vertex has degree two. The line y=0 is a horizontal wall. For every integer x the strand contains

    (x-2,-1) -- (x,0) -- (x-2,1).

The strand passes from below the wall to above it **at the wall vertex (x,0)**. Neither incident knight edge properly crosses an open unit wall edge. Nevertheless the strand exits a chamber bounded by that wall. Along a wall segment of length l there are l-O(1) such passages, with no bad quarters to pay for them. This is an elementary whole-plane field, not a completion claim for a finite board; it directly tests the local permeability assertion used by the chamber proof.

A Jordan-curve crossing count must either route the barrier away from tour vertices and count the resulting edge intersections, or give an explicit vertex-crossing convention. A small displacement of this wall does not preserve zero capacity. Therefore the displayed chamber estimate and its asserted additivity are not established by the present proof. Adding BQ alone cannot pay these wall-vertex passages, since this local example has BQ=0. This does not refute the revised final inequality, which can use exception terms and different barriers.

For clarity, the revised BQ inequality passes the two examples recomputed after the update: at n=96, BQ=622 and EXC=155 give BQ+2SSR+2EXC=1026; at n=288, BQ=1646 and EXC=347 give 2690. These are larger than 4n. See claim36_revised_scan.log. The original counterexample therefore cannot be relabelled as a counterexample to the revised inequality.

**Pareto profile.** The decisive new finite input is four tiny periodic corridor graphs (24 edge orbits each), together with the previously audited all-size FOLD construction. Five complete tours give direct regression checks; no SAT solver is needed for this audit. The result adds no crossing bound. The simpler 5n goal remains open, but a revised statement must count repairs already made, not demand that their former returns still have two cheap endpoints.

Claim 36 is complete. No author files were edited; all computations have finished.


### 36F. Explicit closeout of the REVISED Sheet Lemma — GAP (2026-10-03)

This section answers the queued request to test the revised statement, rather than the withdrawn original B. The revised universal inequality

    BQ + 2 SSR + 2 EXC >= 4n - O(1)

is **GAP, not refuted** by this audit. The old FOLD counterexample does not refute it. Section 36E refutes a proposed local barrier step, not this final inequality. The new I label repairs one missing stopping case; it does not repair the missing EXC term in (A): since only cheap slots receive labels, the available identity is W+D+I+X_E = 4(n-6)-EXC for d=3, provided the stopping rule is exhaustive.

**Independent direct tests (CERTIFIED for these saved tours only).** I used actual P/P' collar windows and required both SSR endpoints to be cheap, as in SHEET. Interior BQ uses exact quarter multiplicities. These are complete validated tours, hence also spanning 2-factors.

| tour | n | BQ | SSR | EXC | revised left side | 4n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FOLD | 96 | 622 | 47 | 155 | 1026 | 384 |
| FOLD | 288 | 1646 | 175 | 347 | 2690 | 1152 |
| FJOG | 130 | 2544 | 137 | 193 | 3204 | 520 |
| FIELD | 166 | 912 | 66 | 303 | 1650 | 664 |

The first two results are in claim36_scan.json; the two additional runs are in claim36_revised_extra.json. They have substantial slack and provide no evidence for the sharp coefficient near equality. No finite test establishes a statement with an unspecified O(1).

**Measurement mismatch (FAIL as a test of the stated quantities).** The author script sheet_measure.py counts every same-side interior chord, including chords with exception endpoints. SHEET defines SSR to require two cheap endpoints. The script also replaces EXC with the number of rows whose collar crossing count is not one. Equality of a row crossing count does not assert equality of the full P/P' window. For FOLD n=96, running

    PYTHONPATH=w-verifier python3 gap/structures/sheet_measure.py 3 w-integrator/tours/FOLD24_n96.json

returns SSR=223 and EXCp=95, whereas the exact-window test gives SSR=47 and EXC=155. BQ=622 and X=720 agree. Thus the reported proxy left side 1258 is not the stated left side 1026. The two substitutions have opposite effects; a passing proxy total cannot be used as a certificate for B. Repair: check the full collar pattern at both endpoints, use the same inclusive slot interval as SHEET, and report proxy counts separately.

**C and D remain unresolved by the revision.** The explicit opposite-matching corridor in 36C still disproves the claim that actual cheap-ended SSRs must be P-trapped. A separate half-unit price theorem could still hold, but Claim 28 does not establish it. Section 36D's common-capacity requirement also remains: BQ, exception windows and SSR payments need one allocation in the excess budget. None of these gaps is fixed merely by adding BQ to B.

**Required repairs before a 5n proof:** use the corrected label identity; replace the wall-impermeability step with a valid strand count including wall vertices; establish the joint Hall/capacity bound for the revised B (including cheap-to-exception chords); prove a price theorem that covers non-chevron returns; and allocate all three payments in a single excess ledger. These are proof obligations, not requests for further large computation.

**Pareto profile:** this follow-up uses two additional direct tour scans and one small diagnostic script run, with no SAT or transfer-graph input. The obstruction to the proposed proof is the elementary three-vertex wall passage in 36E. The audit establishes no new lower-bound coefficient. Revised B remains a conjecture; C's stated trapping premise is false; the joint price conclusion is a gap. Claim 36 is complete for the revised request.


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


## Claim 38: SHEET v2, T5 and clean returns — 2026-10-03

**Verdict: FAIL for T5 as written. D_T with the exact exception-window count is false, including its O(1) allowance. B_T and the numerical clean-return inequality remain GAP. The proposed clean-return proof has two missing implications. The repaired label count and the local barrier convention pass with their stated qualifications.** Audit object: gap/structures/SHEET.md section 7. No author files were edited.

### 38A. A repeatable counterexample to D_T — FAIL

D_T asserts E >= BQ/4 + EXC - O(1), where E=X-4n+2 and EXC counts the non-P/P' windows with d=3. I found a finite replacement in the pure left P collar, in columns 0 through 5 and rows 0 through 15. The replacement changes 12 edges to 12 edges, preserves every vertex degree, has no internal cycle, and preserves **every exterior port pairing**. It can therefore be inserted into a closed Hamiltonian tour without changing the tour's connectivity. In the reference P field its exact changes are

    delta X = 20,   delta BQ = 34,   delta EXC = 18,
    delta(E - BQ/4 - EXC) = 20 - 34/4 - 18 = -13/2.

The complete removed/added edge list is in claim38_gadget.json. The box has 22 exterior-port pairs, including trivial components with both external edges incident to one vertex; the replacement preserves the entire pairing. A solver-free validator checks the edge list, knight moves, degrees, absence of cycles, the actual *external edge* pairings, exact proper crossings, quarter multiplicities, and both P/P' window tests. No SAT lower bound is needed: this is a finite explicit witness.

The gadget does not simply exchange two paths and hope that the tour remains connected. It preserves their exterior connections. Any number of spatially separated copies therefore preserves one Hamiltonian cycle. Copies at a fixed sufficiently large row spacing, for example 40, have disjoint crossing, quarter and window supports. Reflection and transposition give the other side orientations.

Use the audited all-size FOLD family n=96+48k from Claim 12. Its unchanged bulk has pure collars on intervals of length proportional to n; the finitely many construction patches and phase transitions remove only O(1) rows at any fixed collar depth. Thus a positive linear number of these fixed-size replacements fits. For the unmodified family,

    E = 7n/3 + O(1),   BQ = 16n/3 + O(1),   EXC = n + O(1).

The first coefficient is the audited X=19n/3+O(1) construction. For the second, claim38_corridor_bq.py counts 16 bad quarters per (6,6) period in each of the four diagonal corridors. Each has n/12+O(1) periods; the pure/fold bulk has no bad quarters, and the remaining patches and endpoints contribute O(1). The collar arch flips are outside the interior BQ region. The third coefficient is the quarter-side arch-flip count, with fixed-window and patch effects O(1), already used in Claim 36. Consequently the unmodified D_T surplus is O(1), whereas m disjoint gadgets change it by -13m/2. Taking m proportional to n disproves D_T with any uniform additive constant. This conclusion is not an extrapolation from the finite table.

Five complete modified tours were also checked from their stored grid encodings by the independent tour and geometry checks:

| n | Gadget copies | X | E | BQ | EXC | E-BQ/4-EXC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 96 | 2 | 760 | 378 | 690 | 191 | 14.5 |
| 144 | 6 | 1144 | 570 | 1082 | 311 | -11.5 |
| 192 | 12 | 1568 | 802 | 1542 | 467 | -50.5 |
| 240 | 19 | 2012 | 1054 | 2036 | 641 | -96 |
| 288 | 26 | 2456 | 1306 | 2530 | 815 | -141.5 |

These are one-cycle Hamiltonian tours, not only degree-two witnesses. B_T is satisfied on these examples; the counterexample attacks D_T.

Evidence: claim38_gadget.json; claim38_validate_gadget.py; claim38_gadget_validation.json/log; claim38_patched_n96.json through claim38_patched_n288.json; claim38_corridor_bq.py/json. CP-SAT with one worker was used only to discover the local replacement. claim38_gadget.py --replay fixes the saved edge choices and checks the model; its OPTIMAL status concerns this fixed-witness replay, not a claim that the gadget is globally best. The exact validator is the decisive check.

An earlier exploratory search also produced a validated n=96 tour with D_T surplus -88.75 by successive cycle-preserving two-edge switches. That single-size result alone would not defeat O(1), so the proof above uses the pairing-preserving gadget instead. The exploratory files are claim38_switch.py/log and claim38_switched_n96.json.

### 38B. N_re is a different quantity — repair requires a new statement

The gadget preserves all exterior partners. Thus N_re, if defined from these actual collar-port partners relative to P, does not change, while EXC increases by 18 per copy. This gives a direct unbounded separation between exception windows and pairing repairs. Replacing EXC by N_re/2 avoids this specific counterexample; it does not establish the resulting D_T.

If only D_T is changed, B_T still contains EXC and the advertised conclusion E>=n-O(1) no longer follows. One must either prove a geometric inequality involving the same pairing variable, such as an appropriate BQ+2N_re bound, or prove a different common-budget relation. In particular, N_re/2>=EXC-O(1) is false for these insertions.

The witness uses a width-six replacement. Claim 28's price is for a fixed-field strip of width at most four and a specified current class, with finite-interval qualifications. Nothing here contradicts that certificate. A new arbitrary-collar pairing price, or a reduction to its certified strip class, is still needed. Measuring a constant surplus on the unmodified FOLD family cannot establish a universal joint ledger.

### 38C. Clean-return argument — FAIL for the stated implication; GAP for C'

C' is SSR_clean<=EXC+O(1). I did not find a counterexample to this numerical inequality. Its proposed proof is incomplete even after removing returns through bad squares.

First, “the return's interior lies in good squares” must specify what happens at lattice vertices. There is a degree-two local edge configuration containing

    (0,0) -> (2,1) -> (3,3)

in which all four squares traversed by the two open knight segments are good:

    (0,0), (1,0), (2,1), (2,2).

At the turning vertex (2,1), the other two incident squares are bad. Their quarter multiplicities, in B,R,T,L order, in the saved witness are

    square (1,1): (0,0,1,1);   square (2,0): (1,1,2,2).

Thus the path goes through good squares yet makes a gentle (2,1)->(1,2) turn, which is not an allowed transition of G1's free-fold eight-cycle. The point (2,1) itself belongs to the closure of good squares, so requiring containment in that closed union does not remove the issue.

claim38_clean.py constructs the local witness with exact degree two on the point box [-4,7] x [-5,7], degree at most two outside, the two forced moves, and exact goodness of the four traversed squares. A direct recount of its 172 selected edges confirms these assertions. The full edge list is in claim38_clean.json. This is a local counterexample to the claimed implication, not a completed closed-tour counterexample to C'. A repair could require a full good neighbourhood at every interior turning vertex, then prove that this implies the free-fold hypothesis. Such a stronger definition changes SSR_clean and requires a new geometric count in (B).

Second, even when the free-fold hypothesis is separately ensured, G1 proves a *net cycle step* of +1. It explicitly allows cancelling fold pairs and a composite reflection or glide, and explicitly says it does not prove a general arch price. This is not a proof of the fixed P-compatible matching relation required by Claim 28C. That claim assumes fixed chevron interior matchings and changes only to edge pairings. A single clean arc does not establish that its partner arc survives, that its nest has that matching, or that all nests share a disjoint supply of exception slots. A charging proof of SSR_clean<=EXC+O(1) must address these points.

The saved FOLD, FJOG and FIELD diagnostics were also tested for clean SSRs using goodness of every square traversed by their interior edges. Results are in claim38_clean.json/log. These tests do not supply the missing universal implication or matching theorem.

### 38D. Label count and barrier convention

**PASS, conditional on exhaustive stopping:** W+D+I+X_E=4(n-2d)-EXC is the correct starting-label count under the stated slot convention. No labels are initially assigned to exception slots. The revision correctly retains the qualification that all label paths stop in one of the listed classes. This count alone supplies no price for a slot.

**PASS for the local barrier repair; GAP for a global chamber argument.** A slash strip midline y-x=k-1/2 avoids lattice vertices. Within a good square of its split, an intersecting tour edge is the corresponding present chain link. Likewise a transversal passage through a wall edge's midpoint avoids the uncounted wall-vertex passages from Claim 36E. A knight edge crossing that unit edge in its interior would be its carried tile link, which the good wall does not permit. Thus the revised convention removes that particular defect.

The withdrawal of the old half-chamber and attached-wall claims is necessary. A full-triangle count can only be invoked after the two complete boundary paths, their good-strip hypotheses, and the partner's arrival at the side are established. It cannot be applied to the pleat deflector by the midpoint convention alone. In particular, the convention proves neither B_T nor the clean-return version of (B).

### 38E. Scope and Pareto profile

T5 with window EXC is false because D_T is false. B_T remains GAP; C' remains GAP, with the clean-to-free-fold and free-fold-to-P-matching steps unproved. The proposed replacement of EXC by N_re/2 is a new conjecture, not an audited repair. The counterexample does not refute X>=5n-O(1); all modified tours have many more crossings than that.

The decisive finite input is one 6-by-16 pairing-preserving collar replacement, independently checked without a solver. Its unbounded use relies only on the previously audited FOLD construction and a 16-bad-quarter period count. Five full tours are regression evidence. The clean-turn objection uses one small local degree-two witness. There is no large transfer graph and no new lower-bound coefficient. All computations are finished; Claim 38 is complete.


### Claim 38 follow-up: latest SHEET section 8 — 2026-10-03

**Verdict: GAP for (B'), (C*) as an input sufficient for the lower bound, and (D*). No counterexample to these numerical targets was found. PASS for the good-point/free-fold local step and the conditional trap-parity calculation. FAIL for the unrestricted statement that every clean return is a steep-port horizontal chevron.** The section-7 EXC counterexample remains valid for that withdrawn price; it is not a counterexample to section 8's pairing price.

The current file is more specific than the queued summary. Its actual geometric target is

    (B') BQ + 2 RET_clean + 2 N_re' >= 4n-O(1),

where N_re' counts changed ports that are NOT ends of clean returns. This distinction is required for the final addition. I audited this version.

#### 38F. Good-point repair and the missing port hypothesis

Requiring all four squares at each interior chord vertex to be good fixes the gentle-turn objection from the previous audit. The local classification used in 8.1 is correct. At a one-split point, the four possibilities given by T2 are two straight pairs and two free-fold pairs. The wall classification gives the remaining axis-fold pairs. Thus the turns of such a clean chord are free folds. Goodness also rules out proper edge crossings along the interior arc. The previous witness with two bad squares at its turning vertex is excluded by the new definition.

However, RET_clean explicitly allows ANY port type. G1 requires steep ports. The cut x=5/2 can also be crossed by a shallow (1,2) or (1,-2) edge. Good points do not exclude them. A concrete whole-plane perfect field provides the counterexample to the asserted classification:

    w(k)=V for k<=-1, and w(k)=H for k>=0,

in T2's slash ribbon-word construction. Its strand contains

    (2,-2), (3,0), (4,2), (5,4), (3,3), (1,2).

The portion in x>5/2 returns to the same boundary. Every point and square is good. Its entrance is shallow (1,2); its exit is steep (-2,-1). Both ports have slash sign. The turn from (1,2) to (-2,-1) is a valid diagonal free fold. The composite reflection is diagonal, not the asserted horizontal reflection. The two intersections with x=5/2 are (5/2,-1) and (5/2,11/4).

This is a whole-plane perfect-field counterexample to “clean return implies G1's steep-port hypotheses,” not a completed closed-tour counterexample to (C*). claim38_v3_local.py checks the word-field edges, degrees and all quarter multiplicities on a surrounding box. The infinite extension is exactly T2's word formula.

**Repair:** first separate shallow and steep ports. Under the census convention a shallow port is automatically changed, so any return with a shallow end already satisfies the required changed-end alternative. Apply G1 only to the remaining two-steep-port returns, and obtain only its actual net-step and reflection/glide conclusion. The definition of N_re should explicitly classify shallow ports as changed, since P/P' has no reference port of that type. This is a definition choice currently implemented by the script, not supplied by the phrase “its P/P' partner.”

A short odd-shift free-fold candidate was also tested with every interior vertex required good; the local degree-two SAT model was UNSAT. That single failed candidate is not a parity proof and supplies no new claim about 8.5.

#### 38G. Trap parity is conditional; the exceptions are not controlled

The algebra in 8.2 passes. Write P(c)=c-3 for even c and c+3 for odd c. Then

    P(c+s)=P(c)+s                  if s is even,
    P(c+s)=P(c)+s +/- 6            if s is odd.

If two distinct returns have the stated partner endpoints, equal even shift, and unchanged collar partners at both ends, these two chords and their two collar paths form a closed component. A larger single tour cannot contain it as a proper component. This is the fixed-matching trapping result, not a proof that the partner return exists or that the shifts agree.

Section 8.3 explicitly assumes P/P' WINDOWS at the ports and a defect-free region between the two returns, and still depends on the unwritten Lemma F. “Unchanged partner” alone does not imply a P/P' window. Those hypotheses must be established when applying the development argument to an arbitrary return. The good-point condition on the return itself does not establish goodness of the partner or of the enclosed region.

More importantly, the proposed exceptions (i) dirty/nonreturn partner, (ii) a bad square between the returns, and (iii) odd shift are not bounded in number. They are not merely the O(1) geometric board-corner exceptions. Even if the alternatives in 8.3 are made exhaustive, listing them gives no estimate sufficient for the target. A bad cluster can be enclosed by many nested regions, and the same dirty partner or bad-quarter capacity must not be charged repeatedly without a matching/allocation proof.

Here is the exact missing term. Let U_0 be the number of clean returns with zero changed ends, and N_c the number of changed ports incident to clean returns. Distinct interior chords have distinct ports, so

    N_re = N_c + N_re',     N_c >= RET_clean-U_0.

Consequently (B') and (D*) would give only

    E >= n - U_0/2 - O(1).

To conclude E>=n-O(1), prove U_0=O(1), or prove a stronger joint inequality that pays this loss. Merely permitting the cases (i)-(iii) in (C*) does not do so. The BQ/4 term is already fully present in (D*); it cannot be used a second time to pay these cases. Similarly, the Parity Lemma remains a conjecture, as the source itself states. G1's net-step result does not prove even shift or absence of defects inside the return's disk.

**Status:** the conditional trap calculation is PROVEN. The universal changed-end count, or a version with quantitatively paid exceptions, is GAP. No closed-tour counterexample to the strengthened, exception-free count is claimed here.

#### 38H. Independent census of the actual section-8 quantities

claim38_v3_census.py traces each interior chord and each collar path directly, tests goodness of all four squares at every interior vertex, and uses the fixed parity rule for P. It does not infer the rule from whichever cheap windows happen to occur in the test tour. It marks shallow, cross-side, cross-sign and ambiguous corner ports changed, as the author census intends. It traces collar paths to completion rather than imposing a 4n-step cap; the collar contains about 12n vertices, so that cap is not justified for arbitrary tours.

The author's learned `exp` table has another scope issue: if a side/sign/parity class has no sampled cheap ports, a genuinely P-paired port in that class is automatically counted as changed. Hard-code the proved reference matching and handle nonreference port types explicitly. The reference rule can be derived directly from the short P paths; its use should not depend on the test tour's training samples. The independent counts below agree with the published FOLD and FJOG rows.

| Tour | n | BQ | RET_clean | N_re | N_re' | B' left side minus 4n | E-BQ/4-N_re/2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FOLD | 96 | 622 | 138 | 194 | 53 | 620 | 85.5 |
| FOLD | 288 | 1646 | 522 | 578 | 53 | 1644 | 85.5 |
| FOLD with 26 audit gadgets | 288 | 2530 | 288 | 786 | 485 | 2924 | 280.5 |
| FJOG | 130 | 2544 | 0 | 148 | 148 | 2320 | 335 |
| H16a | 96 | 0 | 0 | 362 | 362 | 340 | 306 |

Every tested clean return had one or two changed ends. These are finite tests with substantial geometric slack, not certificates for (B') or (C*) on arbitrary tours or 2-factors.

**Important cut-depth distinction:** Claim 38's collar replacement preserves all port pairings at the boundary of its six-column box. It does NOT preserve all ports or pairings at the depth-three cut now used in section 8. In the displayed 26-gadget tour, N_re at that cut increases by 208, while RET_clean decreases by 234. Thus the earlier EXC counterexample does not refute (D*) at this cut. Do not transfer the “unchanged pairing” statement between these two different port sets. The claim that RET_clean is flip-invariant also needs a specified class of flips: general collar modifications crossing the chosen cut can create bad interior points and destroy clean returns, as this example does.

(B') still needs a global geometric proof. The local midline convention from section 7 repairs the wall-vertex issue, but it does not provide partner paths or bound shared defect regions. (D*) still needs one joint allocation of quarter and pairing charges. Claim 28's certificate has its fixed-field, width-at-most-four, current-class and finite-interval hypotheses; it is not by itself a theorem for every depth-three collar with arbitrary exterior ports.

#### 38I. Closeout for section 8

The clean-point correction is valid. Restrict the chevron classification to the steep-port case, state how nonreference ports enter N_re, replace the learned matching rule and fixed collar-path cutoff, and quantify the U_0 exception term in the shared budget. These repairs are necessary before the revised route can prove 5n. The new numerical targets remain GAP, not refuted by this audit.

**Pareto profile:** one explicit perfect word field disproves the unrestricted local classification; five direct tour scans check the revised quantities. One small rejected odd-shift SAT candidate provides only a diagnostic. No large computation and no new asymptotic crossing coefficient are involved. Evidence: claim38_v3_local.py/json/log and claim38_v3_census.py/json/log. This follow-up completes the latest Claim 38 request.


## Claim 39: half-price quarter-payment hand kernel — 2026-10-03

**Verdict: PASS for Sections 2–3 of gap/turnstheory/PROOF_5N_PLAN.md and the conditional reduction to F1, with the flux wording clarified below. F1 remains GAP/OPEN. No 5n theorem is established.** The proof is a valid private allocation in the stated mixed currency, rather than an aggregate support count. I also checked the ledger and final constant needed for its intended use.

### 39A. Currency and quarter-payment rule — PASS

Use the audited full-tour quarter multiplicities and crossing pairs. Write X1 for the number of pairs with a one-quarter overlap, and define W3(q)=binomial(m(q)-1,2) for m(q)>=1, zero for m(q)=0. The exact identity is

    G+X1+W3 = 2(X-4n+2) = 2E.

For S* the UNION of the four width-two strip pair sets, T=|S*|-4n+2, the stated capacity therefore satisfies

    nu(total) = (X-|S*|)/2 + E/2 = E-T/2.

A pair outside S* has a half-unit pair atom. Hole atoms, X1 atoms and each W3 unit have quarter-unit capacity. These are distinct summands even when associated with the same physical crossing or neighbourhood.

The four-case allocation is correct:

* A hole uses its own quarter-unit atom.
* A quarter with multiplicity at least three uses one of its W3 units; at least one exists. W3 units at different quarters are distinct.
* At multiplicity two, a pair outside S* pays a quarter unit. The two tiles overlap in at most two quarters, so the same half-unit pair atom receives at most two requests, even if the requests come from different paths.
* At multiplicity two, a pair in S* with one-quarter overlap pays from its X1 atom. This atom can receive a request at only that quarter.

The only excluded bad-quarter type is multiplicity two with its pair in S* and a two-quarter overlap. Calling this type “unpaid” means that the specified direct rule does not pay it; it does not rule out payment from other nearby residual atoms in F1.

This proves the allocation for ANY set of distinct payable quarters, including all payable quarters at once. It does not require a hole-to-crossing injection, an assumption about phases, or a no-sharing conjecture. In particular, using one W3 unit at a multiplicity-four quarter is safe even though that quarter has several incident crossing pairs.

### 39B. Locality and distinct path squares — PASS

If a knight tile covers a quarter of a square, its endpoint box contains the full coordinate intervals of that square. The integer endpoint extrema have coordinate span at most two, so each endpoint is within L-infinity distance 3/2 of the square centre. Both edges of a pair covering the quarter obey this bound. A closed quarter triangle is within distance 1/2 of its centre. Thus the whole support of the chosen atom is within radius two of ONE dual vertex of the path, as required; radius ten is more than sufficient. This uses the precise support definition, not a bounding-box intersection with the union of a path neighbourhood.

A dual vertex is the centre of one unique unit square. The audited candidate paths are vertex-disjoint: in a corner frame their maximum square coordinate identifies their radius, and the four corner boxes do not meet. Therefore the chosen quarters for different paths are distinct. Picking any two payable quarters per eligible path and applying the global quarter rule gives a simultaneous half-unit allocation. This proves all subset/Hall inequalities for those paths, including when one crossing pair supplies quarters to two different paths.

The author support check passes: four unoriented move types, 16 covered quarters, maximum endpoint distance 3/2. The independent check uses the previously audited exact polygon-quarter geometry and reproduces these values without importing the author script or its microtile implementation.

### 39C. Reduction to end zones — PASS

The square identity m_B-m_R+m_T-m_L=0 implies that exactly one bad quarter is impossible. Every bad square has at least two bad quarters.

Membership in a side's width-two pair set means BOTH edges have an endpoint at depth zero or one from that same side. Each edge endpoint box reaches depth at most three. Hence its tile, and therefore the pair's overlap, cannot have positive area in a square starting at depth at least three. The source uses the weaker safe cutoff four; that is valid. Every quarter in its defined middle is payable if it is bad.

A bad middle square therefore supplies two payable quarters and pays its path in full. After choosing min(2,s_i) quarters for every path, the explicit atom allocation leaves a nonnegative residual capacity nu'. Any path with positive residual demand has no bad middle square. This reasoning concerns actual full-tour multiplicities, not a local patch with missing exterior edges.

For even n>=128 and r>32, the corner path has exactly six squares at square-depth below four: depths 1,2,3 at each of its two ends. The opposite board sides are far away. The remaining squares are in the middle. At each corner there are 21 possible radii 12 through 32; discarding these only for payment loses at most 84 paths, hence 42 units. Keeping them in L and D_loss, while assigning their unmet demand to the one total error, is consistent. C_side must include this allowance, as the source states.

Retention excludes B overlaps from every path square by the audited endpoint exception rule. Thus an unpaid quarter on a retained path has its covering pair in S* minus B. This exclusion is inherited from the audited retained family; it is not true merely because a candidate path has the right radius.

**Wording repair:** “the flux across the good middle is zero” should say “zero modulo three.” For a step with two good adjacent quarters, the flux formula gives omega=3 chi(a)(1-g), which need not be the integer zero. Its residue is zero, which is exactly what the charge reduction uses. Include the transition steps between the end zones and the good middle when assigning the remaining charge to the ends.

**Optional tightening:** with square depth defined as min(x,y,n-2-x,n-2-y), the endpoint-box argument actually makes every bad square of depth at least three fully payable. A deficient path can therefore have bad squares only at depths one and two, four end squares in total. The stated six-square reduction is conservative and requires no change for correctness.

### 39D. Independent checks — PASS

New check: claim39_check.py, standard Python, one process, no author imports. Evidence is in claim39_check.json/log and claim39_sources.json. It checks:

* the exact endpoint support bound on all 16 template quarters;
* all 81 choices of half multiplicities in {0,1,2}, confirming the square identity and exclusion of one bad quarter;
* 232 overlapping pairs from a sufficient local set of width-two side edges, all with overlap-square depth at most two;
* candidate-square disjointness, exact candidate count 2n-60, the 84 small-radius candidates, and the six end squares at n=128,130,144,288;
* the complete atomic allocation on two independently validated tours, choosing EVERY payable quarter at once, and checking that no atom exceeds its capacity;
* the exact mixed identity and the residual-good-middle implication on those candidate paths.

For FOLD n=96 the check obtains X=720, |S*|=541, E=338 and 4 nu=1034. It simultaneously assigns 901 quarter units to all payable quarters without overuse. At n=144 it obtains X=1024, |S*|=781, E=450, 4 nu=1386 and 1253 assigned quarter units. These finite runs support the elementary allocation proof; they do not establish F1. The n=96 run is a local-allocation test, not an assertion of the proposed theorem's n>=128 scope.

Commands:

    python3 gap/turnstheory/check_quarter_payment_support.py
    python3 gap/verifier/claim39_check.py

### 39E. Conditional 5n conclusion and exact remaining obligation

The audited beta=1 certificate has error 29/4 per oriented half walk. Eight halves give 58. The strip sum exceeds the S* UNION count by at most 1104, so

    D_loss <= A <= |S*|-4n+1162 = T+1160.

Combining this with nu(total)=E-T/2 gives the exact stated reserve identity and restoration inequality:

    E+580 = nu(total)+(T+1160)/2,
    (T+1160)/2 >= D_loss/2.

If F1 supplies the residual payments in the SAME nu' after the baseline quarter choices, with total error at most C_side, then nu(total)>=L/2-C_side. Since L+D_loss=2n-60,

    E+580 >= n-30-C_side,
    X >= 5n-(612+C_side),       for even n>=128.

The constant and sign pass. The 42-unit small-radius allowance is already included in C_side and is not to be added again. To extend to smaller even boards by the trivial X>=0 bound, one may enlarge the final constant to at least 630.

F1 is the single remaining NEW price lemma in this conditional chain. Its existence is not proved by the hand kernel. In particular, fully paid paths may already have spent pair capacity near a deficient path's end windows. The side proof must use the actual residual atom capacities and one total error, not independently reset each window's budget. The good-middle reduction localizes possible path defects and the residue calculation; it does not automatically prove that end-local resources suffice. As written, F1 allows radius-ten eligible resources along the path. A certificate restricted to end windows would be a sufficient, potentially stronger implementation and needs its own domination and joining proof.

The proposed finite-state description in Section 4 is explicitly a specification, not an audited completed reduction. No claim is made here that it has finitely many sufficient marks with proved compatibility, that an LP/transfer certificate exists, or that W1/W3 substitute for it. Their support results and the full allocation are different statements.

**Pareto profile:** the new proof consists of four local allocation cases, the square identity, disjoint square centres and a bounded end-zone argument. It needs no new SAT or large graph certificate. Its inherited finite inputs are the audited tile/flux facts and beta=1 endpoint-restoration certificate. If F1 admits a short side proof, this is a valid simple route to 5n. At present the hand kernel passes and F1 remains open. Claim 39 is complete; no author files were edited.


## Claim 40: F1 and the R4 side-certificate specification — 2026-10-03

**Verdict: PASS for F1's sufficiency and R4's Hall-based certificate logic. PASS for the degree/edge-set relaxation. GAP for F1 itself and for a completed finite-state certificate. A naive use of halo quarter atoms is invalid and needs the explicit repair below.** I found no counterexample to F1 in the light tests. The section-8 recheck requested after this task was already completed in Claim 38F–I.

Sources: PROOF_5N_PLAN.md section 4, the current R4 at the top of REQUESTS.md, and END_TYPES.md. This audit uses the Claim 39 hand kernel. No author files were edited and no large graph was built.

### 40A. F1 is sufficient for the claimed algebra — PASS

The baseline must be the actual simultaneous quarter allocation f0 from Claim 39. Each path gets min(2,s_i)/4, with the prescribed atom type for each selected quarter. Subtract its consumption atom by atom to obtain nu'. The residual demand d_i is the difference from one half. F1 asks for a permitted baseline choice and a nonnegative residual allocation from that same nu', with one absolute bound on the sum of deficits. Thus f0+g pays L/2-C_side from nu, without exceeding any atom capacity.

The separate audited reserve pays D_loss/2. Its identity is

    E+580 = nu(total)+(T+1160)/2,
    (T+1160)/2 >= D_loss/2.

Adding gives X>=5n-(612+C_side), exactly as in Claim 39. No extra raw S* crossing capacity, 4n baseline capacity, or endpoint reserve is available in g. X1 and W3 atoms associated with S* pairs remain legitimate components of nu; using them is not double counting, because the mixed identity explicitly separates these atom types.

The quantifier is existential over permitted baseline choices, not “every greedy baseline succeeds.” R4's proposed proof for EVERY locally allowed baseline marking is a stronger sufficient condition. Failure of that stronger marked-state model would not refute F1. Conversely, optimizing convenient marks in a scan proves nothing unless every actual tour has a compatible permitted global choice. The deficit allowance must be one total constant; it cannot restart at a deficient path, selected subset, gap, or artificial window. State g>=0 explicitly when restating R4's equations alone; it is already explicit in the mathematical F1 definition.

### 40B. Hall augmentation and endpoint pairing — PASS as a sufficient scheme

The old scalar “total capacity minus total demand” scan was insufficient. Current R4 repairs this by allowing every subset of target rows, demanding t(tau_r) only on selected rows, and counting an atom once exactly when at least one selected endpoint can use it. For fixed geometry and residual capacities, a bound

    capacity(N(J)) - sum_(r in J) t(tau_r) >= -M

for all J is precisely a bound M on total max-flow deficit in quarter units. It yields individual endpoint payments with total error at most M/4, not M/4 per row. Nonnegative endpoint demands whose sum dominates each paired path's residual demand then give path payments with no larger total error.

The anchor (3/2,r+1/2) is an actual path vertex. Restricting to atoms wholly within radius ten of this anchor is therefore safe, but stronger than F1's whole-path eligibility. Its eligible row interval is exactly the stated ceiling/floor interval, provided the entire depth support is within ten of 3/2. A 21-row selection history is conservative for these supports. Activation at the upper eligible row is a valid way to count each atom once, provided its identity, residual capacity and earlier selection history survive until that event.

For targets at local radius at least 33, different physical sides' anchor neighbourhoods are disjoint. For example, a left-side neighbourhood has x<=11.5 and y>=23.5 near the bottom corner; a bottom-side neighbourhood has y<=11.5 and x>=23.5. Opposite sides are separated for n>=128. This justifies summing the four side allocations. The two ORIENTED HALVES of one side are different: their neighbourhoods can overlap. R4 correctly requires continued marks and Hall history and one ownership rule across the orientation change. Resetting the scan and crediting the same atom on both halves would be invalid.

With an integral quarter-unit table and potential width M per half, eight half-walk errors give 2M ordinary units. Thus C_side<=42+2M is correct if all ownership and boundary-state conditions pass. The resulting conditional bound is X>=5n-(654+2M). For rational tables use the full scaling denominator. A potential on only convenient start states is insufficient; actual marked half-walk boundary states must all be covered.

### 40C. Degree relaxation — PASS; halo atoms require a repair

Retain exactly the actual tour edges with an endpoint in columns 0 through 5. Every vertex in these columns still has degree two. Columns 6 and 7 have degree at most two in the retained graph, and every retained edge ends by column 7. Therefore the proposed edge/degree model includes every actual tour restriction. Optional forest constraints are safe on this proper subgraph of a Hamiltonian cycle, provided the scan's component handling is correct. They are not required for a certificate valid on the larger degree-only class.

However, this does NOT give full-tour multiplicities at every square inside the apparent eight-column strip. Squares at depth 6 may have covering edges with neither endpoint in columns 0 through 5. A missing tile can create a false hole.

An explicit example is the perfect P half-plane. For x>=2 its edges are (x,y)--(x+2,y+1), with the standard P pairings in columns 0 and 1. After retaining only edges touching columns 0 through 5, the B and R quarters of square (6,y) become uncovered. In the full field they are covered once by the omitted edge (6,y)--(8,y+1). Thus the truncated model would invent TWO quarter-unit hole atoms per row if its halo multiplicities were treated as full multiplicities. These false atoms lie within the endpoint anchor's radius-ten depth range. This is a real resource-encoding error, not just an unextendible edge assignment.

**Exact safe repair:** use hole and W3 quarter atoms only in square columns 0 through 5, where every possible covering edge is represented. Alternatively represent the missing covering edges and their effect on the full multiplicity. Restricting quarter atoms to the complete columns is sufficient and simpler. For pair and X1 atoms, require both edges to be represented and compute their one/two-quarter overlap from the two full tiles. Their geometric pair capacity does not depend on absent third tiles. Omit all other resources. This is a safe restricted resource pool, not an equality with the tour's full nu.

For a represented pair atom, baseline consumption can come from either overlap quarter, including one in an incompletely represented square. The state must still subtract ALL actual f0 consumption of that pair. Allowing all feasible 0/1/2 consumption marks is a safe relaxation; declaring “no visible mark, no consumption” without accounting for the missing quarter is not. Similarly, quarter multiplicity zero must never be inferred from an incomplete owner set.

### 40D. Baseline flags and finite-state scope — GAP until mapped

Actual tours map into the proposed marking relaxation if the state admits the actual selected quarters, exact atom consumptions, candidate quotas and deficiency flags. For a deficient path all its payable quarters are mandatory baseline selections, and its two end records must agree on the total count and flag. A single-side relaxation may omit remote consistency and admit more states; a bound valid on all those states is sufficient. It may also become too strong to certify.

For fully paid paths, local marks do not determine which two quarters the global baseline selected. For deficient paths, locally good represented middle squares do not prove the unseen entire middle is good. These are reasons to permit additional flags/marks, not reasons to discard states. Any restriction based on realizability, a preferred baseline policy, remote compatibility, or good-middle continuation needs a mapping proof. No one-bit continuation through interrupted runs is available.

The listed finite domains and delayed Hall rule are plausible sufficient state ingredients, not a completeness theorem. Resource ownership, possible consumption from unrepresented squares, finalization of late endpoint types, and all actual boundary states must be checked in the implementation. R4 correctly asks for that proof before declaring a certificate. The recommended next stage is the small end-type/table pilot with the halo repair, not a full transfer graph yet.

### 40E. Light red-team tests and their limits

**Actual tours, baseline-subtracted Hall tests.** claim40_residual.py uses the audited exact retained-path/atom builder, then independently selects baseline quarters, subtracts their prescribed atom capacities, and solves the variable-demand residual flow. It tries three permitted tie policies: lexicographic, deepest-first and shallowest-first. It omits r<=32 for payment, reserving the allowed corner error. For each policy it tests the whole path collar, the union of the two endpoint-anchor neighbourhoods, and the more restrictive side-strip resource pool with the safe complete-column quarter rule above.

| Tour | n | Retained r>32 | Deficient paths | Residual demand | Unpaid after residual flow |
| --- | ---: | ---: | ---: | ---: | ---: |
| LF5 | 156 | 120 | 0 | 0 | 0 |
| LF5 | 208 | 194 | 0 | 0 | 0 |
| FIELD | 166 | 143 | 1 | 1/2 | 0 |
| Claim 38 modified FOLD | 288 | 365 | 0 | 0 | 0 |

All nine policy/resource combinations pass for each tour. The FIELD path supplies a nonvacuous residual test. The LF5 tours that stressed the earlier 2/3 currency have no remaining demand at half-price after this baseline. Neither does the pairing-preserving-gadget tour used to refute the EXC price. These tests do not prove that every marking works, that an additive endpoint table exists, or that F1 holds universally.

**Periodic starting fields.** claim40_periods.py fixes the period-four blocking field in columns 0 and 1 and permits degree-two completion through column 5, with degree-at-most-two halo columns. Requiring squares 3 through 5 good on every row and minimizing payable quarters at row zero yields an extension with both end squares good on every row. Such an end has zero local charge; two such good ends and a good middle do not produce a retained charged path. It is not a residual-demand counterexample by itself.

The period-eight single-shift blocking field, and the same single-shift construction at period six, are INFEASIBLE under that all-rows-good-middle restriction. This is only a small periodic-model result: it does not exclude a completion with some bad middle rows, isolated deficient rows, a different exterior, or a different period. The solver used one worker and a five-second limit per instance; the reported INFEASIBLE results are completed statuses. The check also exhibits the two false halo holes described above. Separately, exact geometry reproduces all seven anchored S-minus-B double-overlap pairs in END_TYPES.md; see claim40_endpairs.json.

**The (1,2) wall.** Its plane witness is not a side completion. If its bad squares meet a path at depth at least three, Claim 39 pays that path already. To challenge F1 it must instead produce the correct retained endpoint states with the bad squares confined to the shallow end zone. A fixed-width straight (1,2) wall intersects a fixed-depth zone of a vertical side over only a bounded row interval; translating it there does not create a growing family of deficient endpoints. Cutting off its zigzag exterior at the board side also changes degrees and demands a new completion. No closed-tour or repeated-end-zone counterexample follows from that wall witness. This remains a useful local stop test, but its original half-price measurement is neither a proof nor a refutation of F1.

Evidence: claim40_residual.py/json/log; claim40_periods.py/json/log; claim40_endpairs.json. No local patch was promoted to a completed-tour claim. No counterexample to F1 was found.

### 40F. Closeout and Pareto profile

F1 is the correct remaining allocation statement for the conditional 5n algebra. R4's all-subsets augmentation is necessary and sufficient at the endpoint-allocation level once the table, actual-state mapping and ownership are proved. The edge relaxation passes; restrict or complete halo quarter atoms before using it for a resource certificate. Baseline marks and their global interpretation remain part of the required proof.

This audit adds one explicit halo-resource counterexample, seven-pair geometry, three small periodic checks and four actual-tour residual-flow screens. It adds no lower-bound coefficient and no large finite input. The mathematical F1 remains OPEN. Claim 40 is complete, and the lower-priority Claim 38 section-8 recheck is already in the audit log.


## Claim 41: the square Gap Lemma — 2026-10-03

**Verdict: PASS, computer-assisted.** For every finite set K of absorbing cuts, the union of their GAP SQUARES contains at least 2|K| bad quarters. This proves the square Hall form and hence an assignment of two distinct bad quarters to every cut, with no quarter assigned twice. It does not prove the false gap-HALF version or a quarter assignment restricted to the particular half of each cut.

Audit objects: gap/lowerbounds/FINDINGS.md section G and gap/lowerbounds/gaplemma/tree_automaton.py, using the tree reduction audited in Claim 37. I checked Uniformity by hand, independently rebuilt every projected local patch with a different geometric encoding and SAT solver, and implemented the rooted-tree recurrence independently. The resulting fixed point and root lower bound agree.

### 41A. Tree reduction and Uniformity — PASS

By Claim 37, any violation has a 4-connected gap-square component U whose side-adjacency graph is a tree. Writing s=|U|, all 2s+2 boundary sides are selected cut ends, there are s+1 selected cuts, and

    sum_(S in U) (bad_quarters(S)-2) <= 1.

Every side-neighbour of U is therefore good. “Tree” means the adjacency graph, not a no-hole geometric assumption; diagonal self-contact remains allowed. Also 2s+2 counts boundary sides, not necessarily distinct lattice vertices. The code includes these cases.

Here is a precise version of the Uniformity proof. Make one vertex for each boundary side of U. For EACH split, follow its half-chain through U and join the two boundary sides at which that segment ends. The resulting graph is the union of two perfect matchings. Actual outside split labels are equal at each matched pair: if either end has the segment's split, saturation requires the other end to have it; if neither has it, both have the other split. Thus labels are constant on connected components of this graph. Identifying sides facing the same good neighbour can only add equalities.

For a one-square tree the graph is a four-cycle. Suppose a leaf L is added at boundary side f of a smaller tree. In the smaller boundary graph, f has one partner g_slash and one partner g_backslash. The three new external sides of L replace f. Two halves of L extend the two old segments to two of these sides; the other two halves connect the three new sides in a path. Therefore the old two-edge passage through f is replaced by a four-edge passage through the three new boundary vertices. The boundary graph remains one cycle. This proves connectivity by induction, including shapes with diagonal self-contact. All boundary labels are the same. Reflection interchanges the two splits, so taking all good neighbours to be backslash loses no case.

The independent claim41_uniform.py also checks this boundary-matching graph on all 4,060 free trees through size 10. Each graph is one cycle on 2s+2 boundary-side vertices. This supports the induction; the induction is the all-size proof.

### 41B. Every real tree island maps into the automaton — PASS

The block-type rules are exhaustive relaxations of a real island:

* Each side-neighbour is either in U or good with the uniform split.
* A diagonal touching two U side-neighbours cannot itself be in U, since that would form a 2x2 adjacency cycle; it is good.
* A diagonal touching exactly one U side-neighbour is either in U or good.
* A diagonal touching neither U side-neighbour is recorded as O and its constraints are omitted. It may have a more specific actual status; forgetting it enlarges the model.

These choices give 82 block types. The local constraints require the central square bad, every recorded good square exactly tiled with its specified split, and degree at most two at the central square's four lattice corners. Incident edges owned by an O square are omitted from the degree sum. Omitting them weakens a degree upper bound, so every actual edge set still satisfies it. Other block links are local existential copies. Global correlations between these copies may be lost, but no real configuration is excluded for that reason.

For adjacent U squares C and X, the key records the shared side's two links, the four surrounding square types, the four links across the two neighbouring parallel sides, and both partial degree sums at the shared corners. In a real embedding these are the same geometric objects from either view. Translation preserves the ordering of the two shared corners; reversing C and X swaps the two partial-degree summands and the two type groups. Both implementations perform exactly these swaps. At a shared corner, the surrounding recorded squares are known, so the two partial sums partition the corresponding incident-edge contributions. Real parent and child patches therefore have equal keys.

The automaton need not reconstruct a globally embedded plane island from every accepted abstract tree. It is permitted to accept extra trees, inconsistent remote coincidences or unextendible local copies. Its LOWER bound is useful because every real island maps into an accepted tree with the same central-square costs. That direction passes.

### 41C. Chain states and cost — PASS

Uniformity makes slash segments inactive: their labels are all backslash and they are not the selected cuts. Their parity can be omitted. Each backslash half of a node joins two sides, RT or LB. A state records the endpoint link bit plus the number of gap halves already traversed, modulo two.

At an external boundary side its parity is the actual selected backslash link bit. Passing through one central half toggles parity. If two branches finish a segment, the absorbing condition is

    p1+p2+1 = 1 mod 2,

so the two incoming parities must be equal. If one side goes to the parent, the outgoing parity is one minus the other incoming parity. This is the author's combine() rule specialized to the uniform case, and it is exactly the audited absorbing-cut identity. The independent recurrence uses only these two rules and omits the redundant inactive slash state.

Each node's cost is the number of its bad quarters minus two. The four central quarter multiplicities are determined by its eight side-link values. Costs are nonnegative by the square identity. Their sum is the actual island excess for every mapped real tree. No costs from the repeated neighbour descriptions are added.

### 41D. Independent finite reconstruction — PASS

New code: claim41_check.py. It imports no author automaton or tree-island code. It reconstructs links by exact geometric tile halves from the independently audited Claim 37 geometry, encodes good quarters and bad-quarter truth tables separately, and uses Glucose4 to enumerate projected patch assignments. The author uses link formulas, badness witness variables and Minisat22. The projection keeps the central link bits, cross-side bits and partial degree sums.

I separately reran the author's patch enumerator through claim41_author.py. For each of the 82 block types, sorted normalized patch sets have identical SHA-256 digests in the two implementations. They agree on all 117,612 projected patches, not merely their total count. Evidence: claim41_author_patches.json, claim41_independent_patches.json and claim41_patch_comparison.json.

The independent bottom-up recurrence then uses geometric interface keys and the two-state backslash parity rule. It checks monotonicity of the height iterations and requires an EXACT fixed point before accepting an all-size result. The key counts were:

| Iteration | Keys | Exact fixed point? |
| ---: | ---: | --- |
| 0 | 928 | no |
| 1 | 3540 | no |
| 2 | 6724 | no |
| 3 | 8332 | no |
| 4 | 8660 | no |
| 5 | 8660 | no |
| 6 | 8660 | yes |

Iteration zero introduces leaf subtrees. The table size stabilizing at iteration four is NOT enough: some values still change later. The equality of the full value dictionaries on iteration six is the decisive check. There are 25,026 feasible root-patch/child-state combinations after closure, and their minimum total excess is exactly 2.

The independent run took about 162 seconds on this box on 2026-10-03; the author patch rerun took about 43 seconds. Each solver was single-threaded, with at most two audit jobs active. No large transfer graph was built. Exact output and the final 8,660-entry value table are in claim41_check.json/log and claim41_values.json.

Commands:

    .venv/bin/python gap/verifier/claim41_author.py
    .venv/bin/python gap/verifier/claim41_check.py
    .venv/bin/python gap/verifier/claim41_uniform.py

The author also records an exhaustive size-12 SAT cross-check (33,724 shapes at size 12). I inspected its completed log but did not rerun that longer enumeration. Claim 37 already independently checked through size 10. The all-size conclusion here depends on the independently reconstructed fixed point, not on extrapolating the size-12 tests or on the author's finite sample of real-patch mappings.

This is a computer-assisted proof with two independent encodings/solvers and exact integer DP. I make no DRUP-checker or Lean claim for this computation.

### 41E. Why the fixed point proves all finite sizes

Start with no realizable child keys. One recurrence step attaches a node to already realizable finite child trees, including the empty child list for a leaf. Thus iteration h gives the minimum costs among bounded-height finite subtrees. Every finite tree occurs at some finite height. The recurrence is monotone from the empty table; keys already present cannot disappear and their values cannot increase.

Once the complete table is unchanged by an iteration, the same recurrence cannot add a cheaper or new subtree at any later height. Alternatively, the fixed table's local inequalities prove the cost bound by structural induction on an arbitrary finite rooted tree. Closing all root half-chains leaves minimum cost two. Hence every real saturated tree island has excess at least two, contradicting the at-most-one excess required for a square Hall violation.

**Small execution repair:** the author's command accepts a maximum iteration count but prints an all-tree ROOT claim even if the cap is reached before equality. The submitted run does reach equality, so this does not affect the proved result. Make the program fail closed unless the full value table has stabilized; the independent checker already does so. Record the full table or its digest with the result. “Six rounds” should be understood as stabilization on iteration index six, with leaf initialization at zero, not stabilization merely because the key count stopped growing.

### 41F. Exact theorem scope and use

The proof needs maximum knight-edge degree two, not Hamiltonian connectivity or exact degree two. For every such edge set with the stated full tile multiplicities, and every finite set of absorbing cuts defined by good endpoints and bad-only gaps, its gap-square union has at least twice as many bad quarters as cuts. In particular it holds for every tour and spanning 2-factor in the research problem. The finite-set Hall theorem then gives the simultaneous two-quarter assignment.

The theorem does not control the gap-half version, which is already false, or assert that the assigned quarters avoid B/S* overlap capacity. A later price application must separately ensure that its quarters are payable in its chosen currency, and must not reuse them for another demand. The theorem also does not by itself establish the clean-return count, trap exceptions, or F1. The audited 5n route still needs F1.

**Pareto profile:** the mathematical part is the short tree reduction, a leaf induction for one boundary-label class, and the real-island-to-tree mapping above. The new finite input is 82 local types, 117,612 projected patches and an 8,660-key fixed-point certificate; the independent implementation is 147 lines before auxiliary reporting. This closes the unrestricted square Gap Lemma without a large state graph. It establishes no new crossing coefficient on its own. Claim 41 is complete; no author files were edited.


## Claim 40 addendum: scalar F1 and the joint-test reserve — 2026-10-03

**PASS for the reserve split and the conditional scalar reduction. The scalar inequality itself remains OPEN.** Sources checked: the audited PROOF_crossings_lower.md Section 5, PROOF_52_11.md endpoint retention and row intervals, Lower Bounds A1, and the newly added PROOF_5N_PLAN.md Section 9. No new finite computation is needed.

The audited JOINT-test potential counts every failed row, not only failures selected by candidate paths. Its four whole-strip inequalities and the 1104 union correction give b <= s-4n+1133 = T+1131 <= T+1160. Use joint failure consistently: failure of the unused orientation may be counted and safely overpaid. Each side-row is an endpoint of at most one candidate, since the near and far row intervals are disjoint. Both passing oriented tests give e=0 and h=2 at each end, so their sum is nonzero modulo three and the candidate is retained. Thus every lost candidate has a failed joint end. Choose one failed end for each lost candidate and each deficient retained candidate with a failed joint end; these are distinct rows.

Let D be the number of lost candidates, F the deficient retained paths with a failed joint end, and P the deficient retained paths whose joint tests both pass. Then

    b >= D+|F|,    b/2 >= D/2+sum_F d_i,    0<=d_i<=1/2.

This is one allocation of b/2. It does not first spend the entire reserve on D and then spend it again. With T'=T+1160-b and the SAME actual atomwise residual nu' after the baseline, the proposed scalar inequality implies

    E+580 = sum_retained(1/2-d_i)+nu'(total)+b/2+T'/2
          >= L/2-sum_F d_i-sum_P d_i+D/2+sum_F d_i+sum_P d_i-C
          = (L+D)/2-C = n-30-C.

Therefore X >= 5n-(612+C), in the audited range of even n>=128. C must be one total board constant; include the 42-unit small-radius allowance if those paths are omitted by the side certificate. Section 9's version that includes fully paid paths in F and P is equivalent, since their deficits are zero.

**Scope repair:** Hall subset bits are unnecessary for this GLOBAL lower-bound target. This weaker scalar statement does not imply the earlier private, radius-constrained F1 allocation. Claim 40B's objection to a scalar scan concerns that stronger allocation target only. Residual atoms must still be counted once, with all baseline consumption subtracted; neither the 4n baseline nor the allocated b/2 may be credited again.

A1 identifies a constant height modulo three only along a vertical dual segment whose adjacent quarters are all good. Passing end tests and separate good path middles do not by themselves make the whole interval between those rows clean. Apply A1 on actual clean stretches and account for breaks; no separate unbounded error per stretch is allowed. This caveat does not affect the scalar algebra above.

**Pareto profile:** a short counting argument and ledger identity, using the already audited joint-test stability certificate. No new finite inputs. This proves a simpler sufficient target for 5n, not the missing scalar price inequality.


## Claim 42: strong visible-overlap test and the 5n bound — 2026-10-03

**Verdict: PASS, with a repaired orientation-join argument. For every even n>=32, every closed knight tour has X >= 5n-612 proper crossing pairs. The same inequality holds for smaller positive even n by X>=0. No 42-unit small-radius allowance is required.**

There is one material correction to the submitted certificate description: UP has potential range [-29,0], but DOWN has range [-33,0] in both the independent reconstruction and the author's current program. Adding eight separate half-side errors would give T+1164, not T+1160. The independently checked common-state interface below repairs this and proves the requested T+1160 bound with room to spare. The theorem does not require the private F1 allocation or a Hall certificate.

Sources: Lower Bounds FINDINGS.md section F; f1v_stab.py and its frac_stab.py/strip_dp.py dependencies; PROOF_5N_PLAN.md; PROOF_52_11.md; audited PROOF_crossings_lower.md. Source hashes are in claim42_sources.json. No author files were changed.

### 42A. Claim V — PASS, with a shorter proof

Use all N=2n-60 candidate paths, including radii 12 through 32 when present. Retain exactly the candidates with neither endpoint exception and nonzero total residue. A lost candidate has a failed oriented test at an end: if both tests pass, each endpoint residue is 2 for either parity, the exceptions are absent, and the sum is nonzero modulo three. Thus a lost candidate owns a strong row.

For a retained deficient path, the Claim 39 baseline selects at most one payable quarter. The path is charged, so the audited flux identity gives a bad quarter in a square centred on a path vertex. The square identity gives at least two bad quarters in that square. At least one is therefore UNPAYABLE. Its multiplicity is exactly two, and its covering pair belongs to S* and has a two-quarter overlap.

Every tile of an edge incident to depth zero or one has its inward coordinate at most three. Its open quarters have square depth at most two. Hence this unpayable quarter is near one physical side. On a candidate path with r>=12, such a square can only be in one of its two end zones; the other physical sides are too far away to supply its covering pair. In that side's up coordinates it is in square (1,r) or (2,r), hence in the stated larger list (1..3,r).

The pair cannot be in the outer-column set B_sigma. The only B_sigma pair with a common quarter at square depth at least one in row r is

    (0,r)--(2,r+1), (0,r+1)--(2,r),

which is precisely the excluded up exception. It has no overlap at square depth two or greater. Reflect this statement for the down end. Thus the unpayable quarter witnesses VIS at that endpoint. This proves V for deficient retained paths even without assuming that both end tests pass.

This also validates the longer submitted charge-localization proof: a deficient path has no bad middle square, and its end-zone nonzero flux leads to the same unpayable quarter. The shorter argument avoids the need to sum separate end-zone fluxes.

Independent exact polygon geometry in claim42_geometry.py finds exactly one outer-column exception pair and seven eligible VIS pairs at an up row. It verifies that every VIS pair crosses properly, has two common quarters, and both edges are pending after that row. The source's square depth three is a harmless extra column; two-quarter strip overlaps reach square depth at most two.

### 42B. The small-radius issue and row ownership — PASS without an extra error

The earlier cutoff r>32 was used for separated local payment neighbourhoods and the proposed side allocation. It is unnecessary for this scalar proof. The quarter-payment rule is valid simultaneously for ANY distinct selected payable quarters. The audited candidate paths have distinct square centres for every radius in [12,n/2-4]. Thus their baseline payments remain private even when neighbourhoods overlap.

For n>=32, each candidate has precisely six squares of depth below four: depths 1,2,3 at each of its two ends. All remaining squares are at depth at least four from every side. Indeed the corner radius is at least 12 and at most n/2-4, while the opposite-side square depths are at least n/2+2. The same inequalities apply after a rotation. The independent code checks every even n from 32 through 258, including every candidate, in addition to this general argument.

Each side-row belongs to at most one candidate endpoint. The near and far intervals [12,n/2-4] and [n/2+3,n-13] are disjoint. Assign one strong end to each lost candidate and each deficient retained candidate. These are disjoint classes of candidates and their chosen rows are distinct. Therefore the strong-row count G satisfies

    G >= D_loss + L_def.

A candidate with two strong ends is assigned only one. Rows from different physical sides are counted separately, as in the strip sum. The corner overcount correction concerns crossing resources, not row ownership.

### 42C. Independent strip reconstruction — PASS

claim42_check.py imports only prior verifier code: the independent forest transitions from Claim 26 and the exact polygon tile geometry from Claim 37. It imports none of the author's graph, endpoint accumulator, VIS, or potential code.

The reconstructed base graph has 82,516 states and 144,674 arcs. Its states retain pending edge geometry and the connectivity partition. Core columns 0 and 1 have degree two; columns 2 and 3 have degree at most two; cycles are rejected. Every restriction of a closed tour to a width-two side is such a forest, since it is a proper subgraph of the one-cycle tour. Crossings are counted once when the later of their two lower endpoints is processed.

Instead of the author's F/exception accumulators, the independent augmentation retains the full selected-edge mask for a row. There are 20 possible strip edges meeting that row. The mask retains edges removed during processing and includes every newly introduced edge. At row end it evaluates the audited endpoint test and the exact geometric VIS predicate from that full set. It then resets the mask. Every base phase-zero state is admitted as a start, so the certificate covers arbitrary actual half-side boundary states.

The independent augmented graph has 184,006 states and 343,631 arcs. Both orientations use this SAME graph. No parity bit is needed: g depends on F modulo three, exceptions and visibility, all independent of row parity. This covers both initial parities; the retention implication F=2 implies h=2 was checked separately for both parities in the audited endpoint proof.

For each orientation the arc cost is exactly

    c = 4w-1-4g,

with g charged only at row end. Four cell transitions per row give 4(X_half-rows-G_half) on a row-aligned subwalk. Integer Bellman-Ford starts from zero at every node and runs to an exact fixed point. A separate final pass checks c+h(u)-h(v)>=0 on EVERY arc. The resulting ranges are UP [-29,0] and DOWN [-33,0]. Both runs stabilize after 41 passes. Full potential arrays and SHA-256 digests are saved with the report.

The independent checker also extracts a zero-slack directed cycle with positive strong-row count, confirming critical rate one for its relaxation. The extracted cycle has 16 arcs, four strong rows, and sum(4w-1)=16. The independent rebuild and certificate checks took about 22 seconds on this box on 2026-10-03. Criticality is not needed for the lower bound; the verified rate-one arc inequalities are the finite proof input.

### 42D. Down orientation and the repaired join — PASS

Reflection y -> -y sends up row r=0 to down row zero, but square row zero to square row minus one. Therefore the down test must inspect VIS in (1..3,r-1), not (1..3,r). The independent code reflects the exact endpoint terms and exception, computes all overlap quarters afresh, and verifies that its seven down VIS pairs are exactly the reflected seven up pairs.

The author's current down code carries the previous row's visibility bit. This is correct: at the end of row r-1, all edges covering its square row are pending; that bit is then used with the down test at r. In the independent full-mask model, those edges are present at the start of row r and are retained in the accumulated mask, so no separate previous-row bit is needed. This provides a different implementation of the same attribution.

Reflection alone does not justify copying the UP potential range: the scan direction and crossing-attribution boundary terms also change. In fact the down range is 33. To retain the claimed constant, use the two independent potentials on their common row-mask state space. The checker verifies at EVERY row boundary

    -4 <= h_up - h_down <= 4.

Split each physical side at row n/2, using up tests on the first half and down tests on the second. Let a,m,z be its start, middle and end states. Summing the two arc inequalities gives

    4(X_sigma-n-G_sigma)
      >= h_up(m)-h_up(a)+h_down(z)-h_down(m)
      >= -4-33 = -37.

Here h_up(a)<=0 and h_down(z)>=-33. This bound permits arbitrary boundary states; it does not need an empty-state shortcut or any assumed agreement of separately optimized baseline marks.

Summing four physical sides gives

    G <= sum_sigma X_sigma - 4n + 37.

The audited union overcount is at most 1104: a pair in two adjacent strips uses edges in a four-by-four corner square, with 24 possible knight edges. Opposite strips do not overlap. With s=|S*| and T=s-4n+2,

    G <= s-4n+1141 = T+1139 <= T+1160.

This is the required repair. Using only the two separate potential widths would instead give T+1164 and would not prove the requested constant by that calculation. The interface inequality above is part of the independently checked finite certificate, not an unverified symmetry claim.

### 42E. Exact ledger and final theorem — PASS

Keep the audited nonnegative mixed currency nu. The tile identity gives

    E=X-4n+2,  nu(total)=E-T/2,
    E+580 = nu(total)+(T+1160)/2.

For each retained path choose min(2,s_i) payable quarters, where s_i is its total payable-quarter count. The simultaneous Claim 39 allocation gives f0_i=1/2-d_i, with 0<=d_i<=1/2. All retained paths with d_i>0 are counted in L_def. The geometric and strip steps above prove

    (T+1160)/2 >= (D_loss+L_def)/2.

Thus

    E+580 >= sum_retained(1/2-d_i)+(D_loss+L_def)/2
           >= (L+D_loss)/2
            = (2n-60)/2 = n-30.

Rearranging gives X>=5n-612. There is no second use of the reserve for D_loss, no residual-capacity claim, and no additional use of the 4n baseline: the exact mixed identity separates these contributions. The baseline uses only its permitted atoms; the single reserve sum pays both disjoint classes once. No per-path or per-stretch error remains.

The proof applies directly for every even n>=32. For positive even n<32 the right side is negative, so X>=0 proves the same stated inequality. Consequently it holds for every positive even board size that admits a closed tour. This audit does not extend the forest certificate to arbitrary disconnected 2-factors or open tours.

### 42F. Evidence and Pareto profile

Run from the research root:

    OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim42_check.py
    .venv/bin/python gap/verifier/claim42_geometry.py

Evidence: claim42_check.json/log; claim42_potential_up.npy; claim42_potential_down.npy; claim42_geometry.json; claim42_sources.json. The author's current down certificate was also rerun, with output in claim42_author_down.log.

The new hand proof is the short deficient-square argument, distinct-row counting, potential joining and final ledger. Its new finite input is the width-two strong-test certificate: an 82,516-state base graph, independently checked through a 184,006-state full-mask augmentation and two integer potential arrays, including their interface difference. It uses no new SAT window lemma, square Gap Lemma, wide-strip graph, private flux allocation, or Hall augmentation. This is a computer-assisted proof with a full independent reconstruction, not a formally verified or DRUP-certified theorem. The required source repair is to state the down range correctly and include the orientation-join inequality. No further price lemma remains for this 5n bound.


### Claim 42 update: revised Lower Bounds section F — 2026-10-03

Checked the current source after the queued update. PASS for the revised separate-half calculation: 4*(29/4)+4*(33/4)=62, hence G<=T+1164, E+582=nu+(T+1164)/2, and X>=5n-614. Its displayed consequence still uses T+1160 and E+580; those lines need the 1164/582 replacement if using only separate-half ranges. No 42 allowance is needed, by 42A–B.

The stronger audited conclusion X>=5n-612 stands: the independent common-mask potentials give h_up-h_down>=-4 at every row boundary, so 42D proves G<=T+1139<=T+1160. This is an additional checked interface input, not a claim that the down width is 29. The source can either use its simpler separate-half proof with constant 614 or cite the checked join for constant 612. No rerun is needed: both orientations and this join were already rebuilt and checked in Claim 42.


## Claim 43: red team of BEYOND5_FLUX — 2026-10-03

**Verdict: GAP for F-beyond(p) and for a proof above 5n. PASS for the exact ledger identity and the conditional algebra. FAIL for P6's proposed proportionality to bit alternations, and FAIL for the geometric justification of mu<=2.** These are explicit counterexamples to intermediate claims, not closed-tour counterexamples to F-beyond(p). I found no such tour counterexample in this light audit. The large wall graphs were not rerun.

Sources: gap/searcher/BEYOND5_FLUX.md, WALL12.md, FINDINGS.md sections 7–8, wall/ribbon_ends.out, and the colour-balance lemma in w-integrator/FINDINGS.md. Source hashes: claim43_sources.json. Independent checks: claim43_check.py/json/log.

### 43A. Exact identity and reduction — PROVEN / PASS

With the SAME union S* in both definitions, X_out=X-s and T=s-4n+2. Thus

    E=X-4n+2 = T+X_out

is exact. It agrees with Claim 42's mixed identity: nu(total)=E-T/2=X_out+T/2. The mixed currency does not supply an independent lower bound for X_out; a large T can pay much of the mixed budget.

If X_out>=pL-C, T>=D_loss-1160, and 0<p<=1, then

    E >= p(2n-60)+(1-p)D_loss-C-1160,
    X >= (4+2p)n-(60p+C+1162).

So the stated reduction to a coefficient above five is correct. This does not require local eligibility or a Hall allocation. It still requires a count of distinct crossing-pair capacity in X_out.

**Currency gap in the evidence and zone-end argument.** The cited tests in the design concern crossings outside B, not outside S*. Since B is a subset of S*, they test a larger resource pool. An explicit pair away from the board corners is

    (0,20)--(2,21), (1,20)--(2,22).

Its two overlapping quarters are L and T of square (1,20). Both edges belong to the width-two left strip; only the first edge touches column zero. Thus the pair is in S* minus B: it contributes to the non-B count and contributes NOTHING to X_out. This exact pair is among the independently enumerated Claim 42 VIS types. Its role here is to distinguish the currencies, not to assert a complete tour containing a prescribed repeated patch.

Likewise an end lying in a corner square need not lie outside S*. The end price must either count only pairs outside S*, or be combined with an explicitly revised joint ledger that accounts for its use of T. Merely locating an end near some retained path does not solve this issue. Aggregate accounting also needs wall and end charges whose combined use of each pair is at most one.

### 43B. Mixed-word current counterexample — PROVEN / FAIL for P6

Use the audited perfect '/' word field. Put t=x-y, c_t=(2,1) for H and c_t=(-1,-2) for V, and give vertex v the neighbours

    v+c_t and v-c_(t-1).

Every word gives a degree-two perfect field, with no bad quarters. For a word of period k, let P=k if k is even and P=2k otherwise. Directly count signed edge stubs across x=1/2, with the sign at the left endpoint, over one P-row period. The mean is

    J_x = -(3/P) * sum_(t=0)^(P-1) (-1)^t [w_t=V].

The same parity imbalance determines the other component. It is NOT the number of bit alternations. One derivation is to orient each t-to-t+1 edge with sign (-1)^t: c_t=(2,1)-3[V_t](1,1), and the constant term cancels over an even period. Equivalently count the finitely many edges crossing the cut, as the independent checker does.

Examples, with this fixed phase convention:

| Word | Cyclic bit alternations | Mean vertical-cut current |
| --- | ---: | ---: |
| HV | 2 | 3/2 |
| HHVV | 2 | 0 |
| HHV | 2 | 0 |
| HVVH | 2 | 0 |
| HVVVHV | 4 | 1 |
| VVHHVHVV | 4 | -3/8 |

Thus a nonstraight perfect field can have exactly zero current. Every odd-period word has zero mean over its doubled period. The checker tests all 510 binary words of lengths one through eight; 252 mixed words have zero current. It separately checks degrees, reciprocal neighbours, and exact perfect-quarter coverage for the displayed fields.

There is also no uniform positive current density for words with many alternations. For

    w_m = (HV)^(m+1) (VH)^m,

length is 4m+2, the number of cyclic alternations is 4m, and |J_x|=3/(4m+2), tending to zero. For m=2,4,8,16 the exact currents are 3/10, 1/6, 3/34, 1/22. These are perfectly tiled mixed fields, not noisy patches. Opposite zigzag phases can cancel their signed current.

**Repair:** replace P6 by the exact signed parity statistic and prove a quantitative relation between a wall's discount below 2/3 and a noncancelling current demand. The conservation identity alone cannot give that relation. A price per unit of signed net current cannot control all mixed-word regions or provide a uniform positive addition per level without it. These examples do not show that a cheap psi wall can actually use the zero-current words; that is the missing test/theorem.

**Saved-witness caution.** Interpreting the printed (2,3) margin strings literally as repeating full-plane words gives current magnitudes 3/8 for VVHHVHVV and 3/4 for VHHVVHVH. Cyclic shifts or phase reversals cannot remove this magnitude mismatch. Hence these strings cannot, in that interpretation, be the two fixed exteriors of a colour-balanced bounded-width periodic interface along (2,3). The author already notes that the one-column margins have free ghost cells and are not full exterior fields. This calculation makes that limitation concrete. One must construct and check the actual exteriors before using the strings as current evidence. The corresponding (1,3) strings HVVVHV and HVHHHV both give magnitude one; this consistency check does not prove their extension.

### 43C. One straight ribbon can meet three corners — PROVEN / FAIL for the stated mu<=2 rationale

Take n=200 and the single '/' ribbon indexed by square centres with x-y=40. Use the audited corner paths and their square coordinates. The same uninterrupted line meets candidates from:

- BL: radii 41 through 96, for example square (96,56);
- BR: radii 79 through 96, for example square (119,79);
- TR: radii 41 through 96, for example square (142,102).

It does not meet TL candidates. These are actual candidate-square intersections, verified by the independent path generator. The BR intersections are between the BL and TR parts along the very same line. Therefore the sentence that a '/' stripe passes near only BL and TR is false. It can pass through a third corner box. This is a geometric counterexample, not an assertion that all the intersected paths are retained in a particular closed tour.

An extra restriction on carrier orientations or which intersections are assigned could still prove a useful bound on sharing, but it must be stated and proved. For straight lines the geometry permits three corner families. If mu counts only distinct corners, mu<=4 is automatic and does not itself need field geometry. Neither observation controls repeated use within one corner when carriers branch, have several components, or revisit the same ribbon.

The displayed linear-fractional calculation IS correct under its premises F>=B>=0 and a valid sharing bound. At c=1/3 and mu=3 it gives 11/18, not 2/3; at mu=4 it gives 7/12. Thus this geometric correction alone does not rule out a coefficient above five. The unresolved issue is proving that those premises cover the actual carrier system and that end prices are private in X_out.

### 43D. Bent carriers, finite regions and shared capacity — ARGUMENT / GAP

**Carrier existence is not automatic.** A retained path is charged modulo three. This implies a bad adjacent quarter; it does not by itself specify one connected curve of defects crossing all its corner's levels. Nor does it imply that every such witness is a crossing outside S*. Before cutting a carrier into straight pieces, define its components, how it is selected from the tour, and how it covers the retained paths. Holes and higher multiplicities remain present in the geometry even if the final currency counts only crossings.

**Periodic prices do not add for arbitrary short pieces.** A minimum-mean certificate for a straight band gives a price times length minus a boundary-potential term for a finite segment. Cutting at k bends can introduce k such terms. Nonnegative crossing counts at the bends do not imply that these boundary terms are nonnegative. Rapid switching can make this a linear loss, not one absolute constant. A valid repair is a common state space and a telescoping potential with checked transition costs at bends and branches, or a direct certificate for the whole nonstraight carrier. Claim 42's explicitly checked orientation join is an example of the additional input needed; reflection alone was not enough even there. No bent knight-wall counterexample was built in this audit.

**Conservation gives a signed constraint, not a price.** The finite-set identity in P3 is correct: internal bipartite edges cancel and the boundary signed count is 2(B_S-W_S). The stated periodic-band consequences need their fixed exteriors and periodic colour balance. For a finite irregular region, current can leave through transverse ends, neighbouring opposite-current zones, or a defect region. An O(width) transverse bound does not exclude a region of width proportional to its length. There is no bound here charging that transport or cancellation to a positive density of crossings outside S*. The HHVV and w_m examples show why the word and sign information cannot be suppressed.

**Uniform end price is still missing.** The width-four straight-interface results are author-certified finite-model results. They do not prove a lower bound for wider interfaces: allowing more width enlarges the configuration set and can reduce the optimum. The finite list of rational slopes does not prove an all-slope theorem. Free ghost cells make the finite model a relaxation of its specified fixed-width transitions, not a relaxation containing every arbitrary-width curved end. A positive price at every fixed width also does not imply one uniform c>0 as width increases.

**Shared ends need joint capacity accounting.** Even if a ribbon segment has two ends, several segments can terminate in one defect region. A turn price already counts ends on both sides of that turn. A wall crossing can also be in the endpoint region. The proposed addition of carrier costs and 2c times segment count requires a simultaneous assignment or one combined inequality preventing reuse of those pairs. The global rather than local target removes the radius constraint; it does not remove this capacity constraint.

### 43E. Labels and next useful test

PROVEN: E=T+X_out and the conditional coefficient calculation; the signed colour identity; the mixed-word zero/small-current examples; the three-corner ribbon geometry; the linear-fractional formula under its assumptions.

FAIL: current proportional to bit alternations (P6); the stated geometric reason for mu<=2; using non-B test success as if it certified X_out.

CERTIFIED only in the author's stated finite models, not independently rebuilt here: the width-four straight-wall and end-price tables. Their arbitrary-width, all-slope and curved-interface extensions remain ARGUMENT. The global F-beyond(p) statement remains CONJECTURE, with no counterexample established here.

Before more straight-slope runs, the most discriminating small test is a charged wall with complete fixed exteriors HHVV (zero current), and then w_m with increasing period and small nonzero current. Measure crossings outside the side strips and the current separately. Independently, a whole-window carrier-and-two-ends model should price all crossings once and allow bent interfaces; separate segment minima cannot answer that question. These are proposed tests, not jobs launched by this audit.

**Pareto profile:** this audit uses a short exact current formula, finite quarter checks, 510 word checks, and one candidate-geometry example. It launches no transfer graph or solver. It adds no crossing coefficient. The above-5n route still needs a uniform carrier/end theorem with the correct currency and sharing rules; completing a finite slope table alone will not supply it.


## Claim 44: connectivity surplus in BEYOND5 — 2026-10-03

**Verdict: GAP for B5 and C5. FAIL for the claimed implication from B5-strip to the N_free/2 term in B5: the mixed ledger introduces a factor of two. PASS for deep-first quarter selection, with the capacity and shallow-user qualifications below.** No closed-tour counterexample to C5 was established. The gentle-seam replay confirms that flux can change at zero extra crossing cost, but does not establish vanishing residual BQx.

Sources: gap/structures/BEYOND5.md, beyond5_ledger.py/log, and w-structures/FINDINGS.md S3/S10 with seam_flux.py. Hashes: claim44_sources.json. This is a light audit; no new strip graph was built.

### 44A. What route (i) owns — PASS with precise units and scope

Claim 42 uses the exact identity E=nu+T/2. A retained candidate selects min(2,s_i) PAYABLE QUARTERS and receives one quarter-unit per selection from the prescribed atoms. Deep-first is a valid tie rule. It changes neither the deficient-path condition s_i<2 nor Claim V, which uses all payable quarters on the path.

A selected quarter is not necessarily a whole atom. A two-quarter overlap outside S* has one half-unit pair atom; one selected quarter consumes only one quarter-unit of it. The other quarter may be selected elsewhere using the remainder. Thus the phrase “two quarter atoms” should be replaced by “two quarter requests with their actual atom consumption.” The Claim 39 packing lemma makes this simultaneous fractional use valid.

Each lost or deficient retained candidate owns one distinct strong side-row. That numerical row unit is paid from (T+C)/2, at one half-unit per row. T itself is an excess count, not a separate list of crossing atoms assigned by physical row. The strip potential gives an aggregate inequality. Spatial exclusion from strong rows is therefore a proposed NEW joint certificate condition, not an existing disjointness theorem.

Route (i) can overpay a deficient retained path: when d_i=1/4 it uses its baseline 1/4 plus a full strong-row payment 1/2. This is harmless but must be retained when defining the actual residual budget. Its total is N/2 plus the baseline payments on deficient paths, not always exactly N/2.

**Do not switch to deep-only deficiency.** A path with fewer than two deep quarters can still have two payable shallow quarters and no strong end. Claim V does not classify it as deficient. The source correctly acknowledges these shallow users. The displayed LF4 and TT16 rows have a linear number of them, so an O(1) exception is not a repair.

### 44B. Deep capacity — PASS; shallow ownership remains GAP

At a square of depth at least five from every side, every covering edge endpoint has depth at least four. A width-three strip edge has an endpoint at depth at most two. Thus a pair covering such a deep quarter cannot belong to the width-three crossing union S3. Hole and W3 atoms there also have deep support.

All deep bad quarters are payable. Their simultaneous quarter-unit payments, including selected baseline quarters and the unselected BQx quarters, obey the same packing lemma. Distinct quarters need not use distinct pair atoms; their total usage stays within the pair's half-unit capacity. Accordingly deep baseline plus BQx/4 is sound with actual fractional consumption.

Shallow baseline quarters can use pairs in S3 minus S*. These were legitimate half-unit atoms in nu, but disappear from the analogous outside-S3 currency. A widened strip lemma must subtract their actual usage or jointly include their demands. Merely requiring changed ports to be far from g rows does not remove this conflict. Shallow users need not themselves own a g row. The source identifies this issue as open; it is a real missing input.

### 44C. Factor-of-two defect in the strip-to-E step — FAIL as a deduction

This problem exists even when every retained baseline payment is deep, so it is independent of the shallow-user issue.

Let s3=|S3|, T3=s3-4n+2, Y=s3-s, and define

    nu3 = (X-s3)/2 + E/2 = nu-Y/2.

Then, exactly,

    E = nu3+T3/2.

Deep quarters remain payable from nu3. After summing sides and absorbing corner overcounts into one constant, the requested B5-strip says

    T3 >= g + N_free/2 - O(1).

Put o=D_loss+L_def, so G_free=g-o. The resulting budget is only

    E >= f0 + BQx/4 + g/2 + N_free/4 - O(1)
      >= N/2 + G_free/2 + N_free/4 + BQx/4 - O(1).

It does NOT supply N_free/2 as written in B5. In general a strip coefficient a on N_free becomes a/2 in this mixed ledger. The extra pairs in Y cannot simply be credited again: Y/2 was exactly what was removed from nu to form nu3.

Two possible repairs are concrete. Ask the strip certificate for coefficient one on N_free, with shallow consumption handled, to obtain B5 as stated. Or retain the requested coefficient one half and weaken B5 to N_free/4. If the original C5 were later proved and the three counts were nonnegative, that weaker B5 would still give a coefficient at least 5+c/8, since

    2G_free+N_free+BQx >= (2G_free+2N_free+BQx)/2.

This is a conditional salvage, not a proof of C5. A stronger joint currency argument could also repair the factor, but none is specified in the design.

### 44D. What the existing table actually tests — FAIL as evidence for C5

beyond5_ledger.py returns C5_ratio=(2*N_re+BQx)/n. It does not compute g rows, G_free, N_free, d0, or the exclusion neighbourhoods. I checked the 11 JSON rows currently in beyond5_ledger.log against that formula. The Markdown table includes additional rows, but has the same proxy column.

There is no supplied inequality converting this proxy to 2(G_free+N_free)+BQx. In particular, many changed ports may lie near already-owned g rows; those ports and rows then contribute to neither free count. Thus the sentence that all tours satisfy C5 with the quoted ratio is not established by this table. Also, the column E-route(i)-N_re/2 omits both BQx/4 and G_free/2; its positivity alone is not a check of full B5.

Repair: implement the requested R-b census using the fixed up/down half-side convention from Claim 42, count every owned row once, and evaluate the exact C5 expression separately for each d0. Use the same deep-first baseline and exact collar partner rule. Do not infer the new counts from T_left or all changed ports. Rows 8..n-9 exclude only O(1) boundary data, but the orientation change and neighbourhood convention still need one fixed definition.

### 44E. Gentle seams and the C5 sharing risk — verified local obstruction, global GAP

I reran the small gentle-seam model with period vector (3,3), width three on each side, one solver worker and a five-second limit per solve. The unconstrained optimum is three crossings per period. Both current -1 and current 0 also have OPTIMAL cost three; current +1 has OPTIMAL cost nine in this phase convention. Saved assignments are in claim44_seam.json. This confirms the precise useful fact: switching between two current classes need not add any crossings to a seam already present for the field transition.

The saved low-cost seams were also unrolled and checked, with independent exact tile-quarter counting. Both have twelve bad quarters per period: six holes and six multiplicity-two quarters. This is four bad quarters per unit seam displacement. This is a local periodic seam test, not a closed tour or a verification of the proposed residual K lemma. No model here includes the actual retained-candidate selections or subtracts their two quarters. Therefore it cannot prove either K in BQx or a counterexample to C5.

The general accounting obstruction is direct: a lower bound on raw bad quarters of a carrier does not survive subtraction of flux-owned quarters without a joint statement. If a carrier supports k freed returns and q retained candidates, a raw bound BQ>=4k yields at best BQx>=4k-2q before any other losses. No relation between q and k, or positive residual density, is proved in the design. The same seam can be relevant to both tasks; separate proofs about it cannot be added.

Nor does a collar odd-current price automatically leave a free row. If its strong rows are the rows already assigned to deficient candidates, K-collar's cost is entirely owned. A constant distance d0 removes some nearby changed ports from consideration; it does not create a new payment for their returns. C5 must show that a one-cycle tour has sufficiently many resources left AFTER these two removals.

The old layout-G computations are not a counterexample: S10 reports that the tested minimal seam templates leave fixed trapped cycles, and the completed n=32 example uses a free seam band with additional cost. Treating those incomplete templates as closed tours would discard exactly the connectivity requirement under examination. Conversely, the finite failures do not prove that all wider or more general sharing layouts are trapped.

### 44F. Labels, repairs and Pareto profile

PROVEN / PASS: the exact mixed identities; deep-first selection among all payable quarters; simultaneous deep-quarter packing; geometric separation of deep quarters from S3; distinct strong-row ownership inherited from Claim 42.

FAIL as stated deductions: B5-strip with coefficient one half implies the requested B5 coefficient one half on N_free; the table's proxy ratio establishes C5. The corrected deductions and required census are above.

CERTIFIED in the small replayed model: two different gentle-seam currents attain the same minimum crossing cost. ARGUMENT / GAP: a uniform residual carrier price after flux subtraction, the ownership version of K-collar, B5 with shallow consumption removed, and C5 for closed tours. No closed-tour refutation was found.

The most useful next action is the exact R-b census, followed by a JOINT small seam window with actual candidate-quarter marks and residual bad-quarter objective. Before building the width-three graph, choose whether the target is coefficient one for the stated B5 or coefficient one half for the weaker conclusion. This audit launches no such graph.

Proof size and finite input: short ledger algebra, a code/data check of the current table, and four small single-worker CP-SAT seam solves plus saved-witness checks. No new crossing coefficient follows. The above-5n connectivity route remains open.
