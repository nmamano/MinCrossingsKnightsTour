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
