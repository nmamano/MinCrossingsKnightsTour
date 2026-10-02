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
