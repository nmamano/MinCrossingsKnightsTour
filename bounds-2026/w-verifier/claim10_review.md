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
