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
