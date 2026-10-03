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
