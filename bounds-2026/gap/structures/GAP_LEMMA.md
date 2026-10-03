# Gap Lemma: every absorbing ribbon cut owns two bad quarters (STATEMENT for red-team; proof in progress)

KT Structures, 2026-10-03. Status: CONJECTURE, with measured evidence. For the Verifier (Claim 34): please red-team the
STATEMENT (definitions, quantifiers, the use in Section 4) while I prove it.

## 1. Setting and definitions

H is a closed knight tour on the n x n board (cells V = {0,...,n-1}^2). D = [0,n-1]^2 is cut into the (n-1)^2 unit
squares; each square into four open quarters B, R, T, L. Tiles and multiplicities m_t are as in the audited
w-turnstheory/PROOF_crossings_lower.md, Section 1. A quarter is BAD if m_t != 1. A square is GOOD if its four
quarters are not bad. A HALF of a square is BR, TL (split '/') or RT, LB (split '\'); each half is two quarters.
By STRUCTURE.md Lemma 0 / T1 (audited, Claim 30), every tile is one half in each of two squares that share its
carried unit edge; a good square has one split, and its two halves of that split are covered by one tile each.

CHAINS. Write BR(i,j) etc. for the halves of the square with lower-left corner (i,j). The '/' chains are the paths
    ... BR(i,j) -a- TL(i+1,j) -b- BR(i+1,j+1) -a- TL(i+2,j+1) -b- ...
and the '\' chains are the paths
    ... RT(i,j) -d- LB(i+1,j) -c- RT(i+1,j-1) -d- LB(i+2,j-1) -c- ...
restricted to squares of D. A link joins two halves that can be covered by one tile, of the letter shown (a, b, c, d
= (2,1), (1,2), (1,-2), (2,-1) moves). Every half lies on exactly one chain, and a chain meets each square at most
once. Each quarter lies in exactly one '/' half and one '\' half, so on exactly two chains.

GOOD HALF: a half of the split of its square, in a good square. It is covered by exactly one tile, and that tile is a
link from it to one of its two chain neighbours (Lemma 0). Its BIT is H if that tile is an a or d move, V if b or c.

ABSORBING CUT. A sequence g-, h1, ..., hk, g+ (k >= 1) of consecutive halves on one chain such that g- and g+ are good
halves, every h_i lies in a BAD square, and bit(g-) != bit(g+). Its GAP HALVES are h1..hk; its GAP SQUARES are the
squares of h1..hk. (A sequence with equal bits, or with some h_i in a good square of the other split, is not an
absorbing cut. Two absorbing cuts on one chain have disjoint gaps.) Each absorbing cut counts as 2 absorbed ends.

## 2. Statement

**Gap Lemma (Hall form, square version).** For every set K of absorbing cuts of a closed tour, the gap squares of the
cuts in K contain at least 2|K| bad quarters in total.

**Gap Lemma (strong, half version).** The same with "gap halves" in place of "gap squares".

Equivalently (Hall's theorem): there is an assignment of 2 distinct bad quarters to every absorbing cut, each quarter
lying in a gap square (gap half) of its cut, no quarter assigned twice.

## 3. Evidence (2026-10-03; `python cluster_scan.py <tour>`, with ALLCUTS=1 for all cuts incl. the side collar)

Max-flow test of the assignment on four validated tours; every cut is matched in both versions:
| tour | E = X - 4n + 2 | absorbing cuts | gap lengths seen | square version | half version |
|---|---|---|---|---|---|
| w-structures/tours/layoutG_n32.json | 151 | 62 | 1-8 | 124/124 | 124/124 |
| w-integrator/tours/FOLD24_n96.json | 338 | 28 | 1-9 | 56/56 | 56/56 |
| w-integrator/tours/FJOG_n130.json | 1045 | 211 | 1-11 | 422/422 | 422/422 |
| gap/lowerbounds/conn/FIELD_n166_92_155.json | 578 | 45 | 1-7 | 90/90 | 90/90 |
The bound is tight: a gentle seam (w-structures S1) has exactly 2 bad quarters per absorbing cut (FINDINGS G11).
A single square does NOT always hold 2 bad quarters per cut that ends there (ratio 2 on a few squares), so the lemma
is per cut, not per square.

## 4. Intended use (the R5 price; this part is a corollary, not part of the conjecture)

Ledger (gap/searcher/PLAN.md (II), identity (I) PROVEN in Claim 29): for lambda = 1/2,
    E >= sum_t c(t) + R/2 - O(1),   c(t) = 1/4 [t uncovered] + 1/4 [t in an X1 pair] + 1/4 binom(m_t - 1, 2)
                                          + (1/2) sum over crossing pairs P not in B with t in overlap(P) of 1/|overlap(P)|,
where R = |B| - 4n >= -O(1) (audited boundary set B). Every bad quarter t whose overlap pairs are not in B has
c(t) >= 1/4. If every quarter assigned by the Gap Lemma has this property, then
    E >= (number of absorbed ends)/4 + R/2 - O(1).
Caveat to check: quarters in overlaps of B pairs (outer columns) have no c-charge from those pairs; cuts whose
assigned quarters lie there are side-collar cuts and must be priced by the side ledger instead. The intended
application uses only cuts at distance > 3 from the side.

## 5. Proof plan (in progress)

(a) k = 1: h between good g-, g+. The cut absorbs iff g- and g+ are both linked toward h (h covered twice: both its
quarters bad) or both linked away from h. In the "away" case, for h = BR(i,j), the good '/' neighbours forbid
'\' tiles across the R and B sides of S, and no '/' tile covers h. If B and R are covered once (by an RT tile across T
and an LB tile across L), S being bad forces extra cover on TL: the bad quarters are then T and L of S (not in h). This is the case that needs the sharing argument: T and L also lie on the
two '\' chains of S. (b) k >= 2: the two end halves h1, hk and the parity of k decide the bit change; enumerate.
(c) Sharing: a bad quarter lies on one '/' and one '\' chain; show that the cuts competing for it have enough other
quarters. (d) Finite exhaustive check of all gaps with k <= K0 in a window (CP-SAT, adversary maximising the Hall
deficit), to catch configurations missing from the four tours.

## 6. Proved so far (2026-10-03)

**L1 (link form, PROOF).** Give every chain link l an indicator x_l in {0,1} (1 iff the tour contains that tile's
edge). By Lemma 0 the tiles of the half's own split that cover a half h are exactly its two chain links, so
n_h := x_(l-) + x_(l+) in {0,1,2}, and the quarter multiplicities of a square are
m_B = n_BR + n_LB, m_R = n_BR + n_RT, m_T = n_TL + n_RT, m_L = n_TL + n_LB.
A good half has n_h = 1, and its bit is the letter of its present link.

**L2 (parity of a cut, PROOF).** For a sequence g-, h1..hk, g+ as in Section 1 with g-, g+ good, let y_0..y_k be the
indicators of its k+1 links (y_0 between g- and h1, y_k between hk and g+). Then bit(g-) != bit(g+) iff
y_0 + y_k + k is odd. (Letters alternate along a chain; g- has the letter of y_0's link if y_0 = 1, else the other
letter, and the same at g+.) Checked against the bit definition on 1216 bad-only gaps of two tours.
**L3 (defect halves, PROOF).** Call a gap half DEFECTIVE if n_h != 1 (n_h = 0 or 2). n_(h_i) = y_(i-1) + y_i is 1 iff
y_(i-1) != y_i; the number of i with y_(i-1) = y_i is congruent to k + y_0 + y_k. So an absorbing cut has an ODD number
of defective gap halves, in particular at least one. A defective half with n_h = 2 has both its quarters bad.

## 7. Finite adversary (hall_torus.py, CP-SAT, 2026-10-03)

Model: p x p torus, any edge set with degree exactly 2 (crossings and cycles allowed), all squares outside a window
forced good; CP-SAT looks for a configuration and a set K of absorbing cuts with 2|K| > bad quarters in the gap
squares (gap halves) of K. INFEASIBLE = no Hall violation in that model (solver proof, no DRUP log).
Sanity runs ("at least one absorbing cut", same window) show which windows admit cuts at all.
| torus | window (squares that may be bad) | cuts possible | Hall violation, square version | half version |
|---|---|---|---|---|
| 8 x 8 | 3 x 3 | NO (vacuous) | INFEASIBLE | - |
| 8 x 8 | 4 x 4 | yes | INFEASIBLE | - |
| 8 x 8 | 5 x 5 | yes | INFEASIBLE | INFEASIBLE |
| 8 x 8 | 3 x 8 band (seam-like, wraps) | yes | INFEASIBLE | - |
| 6 x 6 | whole torus | yes | best found 0, bound not closed (600 s) | - |
hall_batch1.log (2026-10-03): 8 x 8, 4 x 8 band, HALF version: Hall violation FOUND (OPTIMAL; one cut with 5 gap
halves), consistent with section 11. 8 x 8 4 x 8 band SQUARE and 10 x 10 window 6 SQUARE: no result (the shell timeout
1500 s equals the solver limit, so the runs were killed before printing). 10 x 10 4 x 10 band: see the log.
Rerun with a longer shell timeout if KT Lower Bounds still needs these windows.

## 8. Proof attempts that do not close (2026-10-03)

- Square-local counting fails: 64 bad-square types (n_BR, n_TL, n_RT, n_LB) have more defective halves than half their
  bad quarters (e.g. (1,0,0,0): 3 defective halves, 2 bad quarters). A proof must use which chains through a square
  can carry absorbing cuts (neighbour constraints), not the square alone.
- Entry rule: charge each cut the quarter of its first bad square next to the side it enters through (distinct sides
  give distinct quarters, so no sharing). It fails: some absorbing cuts have 0 bad entry quarters
  (tours: 6/62, 0/28, 7/211, 1/45 cuts). Facts at an entry from good square S0 into bad S1 across side s: no tile of the
  other split crosses s, so the other-split half of S1 at s has n <= 1.
Next: combine entry quarters with the defective halves of L3 (each cut has an odd number of them), or a computer
check of a local rule on chain segments.

## 9. A stronger per-cut form (CONJECTURE, measured) - the proof target

A bad quarter q in a gap half h of an absorbing cut is UNCONTESTED if the other-split half containing q lies in no
absorbing gap. Uncontested quarters of different cuts are distinct (q lies in one half of each split; gaps on one
chain are disjoint). So the following PER-CUT form implies the Hall form (half version) with no matching argument:

**Gap Lemma (per-cut form).** Every absorbing cut has at least 2 uncontested bad quarters in its gap halves.

Evidence (ALLCUTS=1, `python cluster_scan.py`): every cut has 2 or more: layoutG_n32 {2: 33, 3+: 29},
FOLD24_n96 {2: 12, 3+: 16}, FJOG_n130 {2: 130, 3+: 81}, FIELD_n166 {2: 38, 3+: 7}.
Proved piece: ENTRY QUARTERS ARE UNCONTESTED. At an entry from good g- (square S0, split s) into h1 (square S1)
across side e, the other-split half h' of S1 containing the quarter of S1 at e has its chain link across e into S0,
whose other-split half is a wall node; so h' is in no absorbing gap. (Entry quarters can be good, so this alone is
not enough: 14 of 346 tour cuts have < 2 bad entry quarters.)
A purely local substitute fails: "the other half has a chain neighbour that is a wall node" gives < 2 quarters for
some cuts (layoutG: 10 of 62). The proof must use the absorbing condition of the other chain (L2 parity).

Per-cut adversary (percut_torus.py, CP-SAT, 2026-10-03; contests modelled exactly: a quarter is contested only by a
truly absorbing cut of the other split): looks for an absorbing cut with <= 1 uncontested bad quarter in its halves.
8 x 8 torus, defects in a 4 x 4 window: INFEASIBLE; 5 x 5 window: INFEASIBLE; 3 x 8 wrapping band: INFEASIBLE.
Proved geometric piece for one-half gaps: a one-half '/' cut at BR(S) forces good '/' squares right of and below S,
which excludes a one-half '\' cut through S (its neighbours would have to be good '\' squares there). Longer gaps:
a '/' gap (slope +1 staircase of bad squares) and a '\' gap (slope -1 staircase) share at most 2 squares.

## 10. Local gap model (gap_local.py, 2026-10-03) - what it shows and why it does not close

Model: a '/' cut with gap length k in the plane; region = band squares + 1 ring; exact degree 2 at all region
corners (EXACT=1; every edge at a constrained point is a candidate); g-, g+ squares good '/', gap squares bad, cut
absorbing (L2). Contest of the crossing '\' chain at internal side s_i is RELAXED in the adversary's favour: allowed
unless one of its two outside neighbours is a wall node. Minimum number of uncontested bad quarters:
k = 1: 2 (OPTIMAL; matches the hand proof); k = 2: 1; k >= 3: 0 (or, FRAC=1, uncontested + 1/2 contested:
k = 1: 2, k = 2: 1.5, k = 3, 4: 1, k = 5, 6: 0.5). The k = 2 witness (`SHOW=1 EXACT=1`) has bad squares around the
gap, so the relaxed contest assumes crossing '\' chains that continue into absorbing cuts outside the region.
So the per-cut form is NOT a local consequence of a 1-ring neighbourhood with relaxed contests; a proof must use the
absorbing structure of the CONTESTING cuts (they are cuts too, and need their own quarters), e.g. a joint charging on
the bipartite crossing graph of '/' and '\' cuts (two crossing cuts share at most 2 squares and contest at most 2
quarters each way). The exact torus adversaries (Sections 7, 9) model contests exactly and found nothing.
Status: CONJECTURE, strongly supported (4 tours, 346 cuts; exact torus windows 4x4, 5x5, 3x8).

## 11. Half version FALSE; square-version notes (KT Structures, 2026-10-03; handed to KT Lower Bounds)

**Half version and per-cut form: FALSE (CHECK, degree-2 model).** `single_cut.py p kmin kmax time HALF`: p x p
torus, one fixed absorbing '/' cut, all other edges free (degree exactly 2). Minimum number of bad quarters in the
gap halves: 2 for k = 1..4, **1 for k = 5, 6** (10 x 10, OPTIMAL). Witness re-checked from the edge list by
`single_cut_show.py`: y = [1,0,0,0,0,1]; gap halves (2,1)TL, (2,2)BR, (3,2)TL, (3,3)BR, (4,3)TL with n = 1,0,0,0,1;
the only bad gap-half quarter is L of (4,3); the bad quarters sit in the PARALLEL '/' halves of the gap squares.
Agrees with Verifier Claim 34 (16 x 16 closed tour). Since the per-cut form implies the half version, it fails too.

**Every bad square has >= 2 bad quarters (PROOF).** m_B + m_T = m_R + m_L = N (both are the sum of the 8 links at
the square's sides, L1). If N != 2, one quarter of each pair {B,T}, {R,L} is bad. If N = 2 and m_B != 1, then
m_T = 2 - m_B != 1. So a bad square has 2 bad quarters in {B,T} or in {R,L} or one in each. Consequence: the square
version holds for any single cut (2k bad quarters in its k gap squares; `single_cut.py ... SQ` gives exactly 2k).

**Reduction of the square version to tree clusters (PROOF, short).** Fix K; U = U(K) its gap squares. Each cut end
is a side between a square of U and a good square, and one side is the end of at most one cut (only the chain of
the good square's split can end there; gaps on a chain are disjoint). A cut's gap squares are 4-connected, so work
per 4-component U1 of U. Polyomino perimeter: |boundary(U1)| = 4|U1| - 2A = 2|U1| + 2 - 2r, with A the adjacent
pairs and r the cycle rank of the adjacency graph (r >= 1 if U1 has a 2x2 block or a hole). So
    2|K1| = ends <= 2|U1| + 2 - 2r,   bad quarters >= 2|U1|.
If r >= 1 the square version holds for K1. **So a violation needs a tree component U1 (no 2x2 block, no hole) in
which EVERY one of its 2|U1| + 2 boundary sides is a cut end and the excess sum (b(S) - 2) over U1 is <= 1.**
Leaf structure (PROOF, hand): a leaf S of such a tree (U-neighbour on the right, say) has one one-half cut on two
adjacent boundary sides (TL with good '/' left and top, or LB with good '\' left and bottom, by reflection) and one
through cut entering at the third side (BR from a good '/' below, resp. RT from a good '\' above). The one-half
cut has both its quarters bad (vertex count at the shared corner; e.g. n_TL = 0, q_R = 1 puts degree 3 on (0,1)).
Leaf-local excess (`tree_leaf.py W RHO`, plane, exact degree on a point box): W = 3, RHO = 1: min excess 0 (OPTIMAL),
so a leaf and its 1-neighbourhood can all have b = 2; the excess must be found further along the tree (not done).

**Failed local reduction (CHECK).** "b(S) >= number of cut ends at S" (`local_entry.py`, plane, radius 3,
absorbing status of long cuts relaxed): max ends - b = 1. Witness: S with good '/' left, top, bottom; TL(S) a
one-half cut (n = 2, T and L bad), BR(S) a through cut with n = 1 and B, R good (S is a leaf of the tree case).
