# Independent verification — 2026-10-02

**Latest audit, 2026-10-03: Claim 26 below is PASS. Every closed knight's tour on an even n by n board, n>=32, satisfies 11X >= 52n-3954, hence X >= 52n/11-360. The U1 boundary-surplus reduction is valid. An independent standard-library rebuild checked all 687,262 integer arc inequalities in each orientation and reproduced the ranges -155..0 and -159..0, with both initial parities. Both author independent-check commands also passed. Proof, constants, scope clarifications, and evidence are in Claim 26 and gap/verifier/claim26_*. No Lean result is claimed.**

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
