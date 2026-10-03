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
