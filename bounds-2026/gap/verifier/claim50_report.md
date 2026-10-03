# Claim 50: smaller cut-state strip certificate — 2026-10-03

**PASS.** Option C in `gap/lowerbounds/SIMPLE_STRIP.md` is a sound replacement for section 5 of `gap/turnstheory/PROOF_5N.md`. An independent implementation reproduces all 3,136 states, 48,510 row arcs, both potentials and the common-state interface. The hand identity (K) is correct. Section 6 can keep its current algebra and the stated bound X>=5n-612 for even n>=32.

No source proof or blog post was edited. This audit concerns option C, its interface and (K). It does not certify the separate impossibility/optimality claims about proposed hand proofs in SIMPLE_STRIP sections 2.4 and 3.

## 50A. Soundness of the graph — PASS

Fix a physical side and use inward column x and along-side row y. An edge touching column zero or one has both endpoints in columns zero through three. Knight edges have row span one or two and no horizontal edge occurs. There are eight possible edges whose lower endpoint is in a given row: four of span one and four of span two. Therefore the cut below row zero has twelve possible pending edges.

Use relative coordinates at each row r. The state below it consists exactly of selected strip edges with lower row less than r and upper row at least r. A row arc chooses all selected strip edges with lower row r. Its incoming degrees plus chosen outgoing degrees must equal two in columns zero and one and be at most two in columns two and three. Future upper-endpoint loads are at most two. These are necessary conditions for every actual S_sigma. No connectivity, forest, or pairing-label assumption is imposed.

After processing row r, remove edges ending at that row, retain every edge ending above it, and translate y by minus one. This is exactly the state below row r+1. An actual board starts with the empty state below row zero and ends with the empty state above row n-1. Induction on the rows maps its entire S_sigma to a walk in the generated graph. In particular every actual half-side boundary state is reachable from the empty board boundary through the actual preceding rows. The enumeration does not need to contain arbitrary abstract masks that cannot occur in such a prefix.

The potential inequalities hold at every generated state, so the half-side proof permits arbitrary generated start/end states. The initial all-zero Bellman-Ford vector supplies that uniform potential certificate; it must not be confused with the separate reachability argument for the graph itself.

### Crossing ownership

The row weight counts every new-edge/pending-edge proper crossing and every unordered pair of new edges that crosses. Consider any selected crossing pair and the later of its two lower endpoint rows. If those rows differ, the older edge must still be pending: an edge ending below the later row cannot cross the interior of an edge starting at or above that row. If both edges start in the same row, their pair is counted by the new/new term. Thus every proper crossing is counted once, including pairs that straddle the half-side split. Shared endpoints are excluded by the strict determinant test.

The strip walk has n row arcs, not 4n cell arcs. Their total weight is exactly X_sigma. Keeping the common pending set at row n/2 preserves crossing ownership across the orientation change; no crossing term is lost at the join.

### Endpoint tests and VIS

The full set of selected edges meeting row r is the incoming cut set union the new edges. Edges that merely pass through row r, with no endpoint there, are also included. All eight endpoint-test edges, the exception pair and both orientations' VIS edges meet that row. The needed flags are therefore functions of a row arc's mask. They are not asserted to be functions of a single cut state alone.

The independent checker derives VIS directly from exact tile-quarter intersections, rather than copying the author's seven-pair table. It finds seven pairs for square row zero in the up orientation and seven for square row minus one in the down orientation. Those sets agree exactly with the author's table and its reflection. The eight endpoint coefficients agree with the proof's table. Reflection changes the tested geometry; it does not reverse the scan or justify equating the two potentials.

No extra parity state is needed. The endpoint test is F=2 modulo three with the exception absent in either row parity, and VIS has no parity dependence. The parity-sensitive endpoint residue was already handled when deriving which candidates are retained.

## 50B. Independent reconstruction — CERTIFIED

`gap/verifier/claim50_check.py` is a standalone standard-library implementation. It imports neither project modules nor the author's checker. Its construction differs from the author's recursive degree choices: it enumerates all 256 subsets of the eight possible new edges, then filters by present and future degrees. States are 12-bit masks. Potentials are computed by synchronous integer relaxation in Python lists, without NumPy.

For geometry, it constructs each tile's four integer vertices and uses exact convex-hull half-plane tests on quarter centroids scaled by six. Every tile is checked to contain four quarters. It derives both VIS lists from those quarters and uses strict integer determinant tests for proper crossings.

| Quantity | Independent result |
| --- | ---: |
| Reachable cut states | 3,136 |
| Row arcs | 48,510 |
| Possible pending edges | 12 |
| Edges meeting a row | 20 |
| UP / DOWN VIS pairs | 7 / 7 |
| UP potential range | [-24,0] |
| DOWN potential range | [-28,0] |
| Fixed-point passes | 8 / 8 |
| Minimum arc slack | 0 / 0 |
| h_up - h_down | [0,4] |
| Conservative per-side error, scaled by four | 28 |

The independent script checks every inequality

    4w-4-4g+h(u)-h(v) >= 0.

It also maps all rows of all four sides of three saved closed tours to actual graph arcs: FOLD n=144, the Claim 47 patched n=288 tour, and FJOG n=132. On each of these twelve side strips it verifies empty initial/final states, equality of total arc weight with a direct proper-crossing count, both endpoint orientations, and the claimed side bound. These are extra implementation checks; the all-tour map is the argument in 50A.

The independent run, including these geometric and tour checks, took 8.17 seconds on 2026-10-03. The author checker was also rerun successfully, with its output arrays redirected by an isolated working directory under `gap/verifier/claim50_author_run/`. It reproduced its stated values. Finally `claim50_compare.py` matched states by their actual pending-edge sets and compared all row arcs, both flags, crossing weights and every potential value. All agree exactly. The author's saved potential arrays are not inputs to the independent reconstruction.

## 50C. Interface and section 6 — PASS

At the common cut m, sum the UP inequalities before the split and the DOWN inequalities after it:

    4(X_sigma-n-G_sigma)
      >= h_up(m)-h_up(a)+h_down(z)-h_down(m)
      >= min(h_up-h_down)-max(h_up)+min(h_down)
      = 0-0-28 = -28.

Hence each side has G_sigma<=X_sigma-n+7. The four sides give

    G_strong <= sum_sigma X_sigma-4n+28.

The audited corner overlap estimate is unchanged: sum_sigma X_sigma-s<=1104. With T=s-4n+2 this gives

    G_strong <= s-4n+1132 = T+1130 <= T+1160.

Thus option C supplies exactly the scalar input section 6 needs, with a stronger intermediate constant. It uses the same strong flag, the same half-side orientations, the same X_sigma crossing-pair counts and the same union s. No replacement of the quarter capacity nu or additional ownership assumption is required.

Keep the existing identity and inequalities:

    E+580 = nu+(T+1160)/2,
    nu >= (L-L_def)/2,
    G_strong >= D_loss+L_def.

The existing conclusion remains

    E+580 >= (L+D_loss)/2 = n-30,
    X = E+4n-2 >= 5n-612.

No reserve is spent twice. Connectivity is no longer an assumption of the finite strip input, because this graph permits cycles. Any change of the full theorem's stated scope should be made explicitly; it is not needed for this requested replacement.

### Integration details

Replace the cell-graph/forest and full-mask paragraphs with the row-cut construction. Use 4w-4-4g in the row-arc inequality, not the old cell-arc 4w-1-4g. Replace the interface range by [0,4] and the per-side calculation by -28. Equation (8) can display the sharper T+1130<=T+1160. Keeping the old looser T+1139 bound would also remain valid, but would hide the new calculation.

Remove the sentence that the forest condition is where connectivity enters section 5. Explain reachability through the actual whole-board prefix and that g belongs to the row arc. Update the reproduction paragraph to name the new checker and this audit. No change to section 6 or the stated theorem constant is required. The proposed optional 597 constant follows if the reserve identity is correspondingly rewritten with 1130, but this audit does not recommend a constant-only theorem edit.

## 50D. Hand identity (K) — PASS

Let a,b,c,d count strip edges joining column pairs {0,1}, {0,2}, {1,2}, {1,3}. The degree-two equations a+b=2n and a+c+d=2n are correct: each listed edge contributes once to the indicated boundary column. The tile masses in square columns zero and one are respectively 4a+2b and 2b+4c+2d. There are exactly 4(n-1) board quarters in each column, and all tiles meeting them belong to S_sigma.

Writing exc_j=sum(m-1)_+ and H_j for holes in column j gives

    exc0 = 2a+4+H0,
    exc1 = 4n-4a+2c+4+H1,
    exc0+exc1 = 2n+6+H0+c+(H1+exc1)/2.

Also H1+exc1=sum_col1 |m-1|. The tile-overlap identity for this strip is

    2X_sigma-X1_sigma = sum_q binom(m(q),2).

For covered quarters in columns zero and one split binom(m,2) into (m-1)+binom(m-1,2); in outer columns leave it unchanged. Substituting the displayed excess sum proves (K), with all the remaining terms nonnegative. Thus X_sigma>=n+3. Board-boundary tile containment is essential to the finite masses above and holds here.

The independent checker verifies exact equality in (K), using integer arithmetic after multiplying by two, on the same twelve actual side strips. This is a light check in addition to the complete algebra above. The identity uses degrees, not connectivity. It proves the base crossing rate; it does not alone prove the extra payment per strong row.

## Evidence, reproduction and proof size

From the research root:

    python3 gap/verifier/claim50_check.py
    OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim50_compare.py

The comparison command expects the author arrays from the saved isolated rerun. The standalone independent command needs no such arrays or NumPy. Results are in `claim50_check.json`, `claim50_potentials.json`, `claim50_compare.json` and their logs. `claim50_author.log` records the author rerun; `claim50_sources.json` records source hashes.

Proof size: a short row-cut soundness and telescoping argument plus a 3,136-state/48,510-arc integer potential certificate. The author checker is 111 source lines; the independent checker is 134 lines including its tour and hand-identity checks. Compared with Claim 42, this removes path labels, cycle rejection and the separate full-mask state augmentation while keeping the same geometric and scalar proof inputs. It is a genuine simplification of the finite input, not a weaker proof interface.
