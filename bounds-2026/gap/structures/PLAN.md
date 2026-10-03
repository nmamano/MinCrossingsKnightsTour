# KT Structures - PLAN (phase 1): STRUCTURE LEMMA (L1) and ARCH / CONNECTIVITY (L4, L5)

2026-10-03. Design only; one light check (tiling_check.py, 6x6 torus, < 1 min). Lemma names follow
gap/turnstheory/PLAN.md. Squares = unit squares of D; quarters, tiles, B, U, E as in w-turnstheory/PROOF_crossings_lower.md.

## 1. Structure lemma: what is already PROVEN (new, G9)
Call a square GOOD if its 4 quarters are each covered once (m = 1), and a lattice point good if its 4 squares are good.
- T1 [PROOF]. A tile of an a=(2,1) or b=(1,2) move covers the half of each of its two squares below/above the '/'
  diagonal; c, d tiles use '\' halves. So a good square has a SPLIT ('/' or '\'), and its two tiles are of that class.
- T2 [PROOF]. In a connected '/' region, the half-triangles form chains along slope +1 ("ribbons"; ribbon k = squares
  on diagonals y-x = k, k-1). A chain is a path, so it has exactly two matchings: all-H (a moves) or all-V (b moves).
  Every H/V word gives degree 2 and zero crossings. So a crossing-free domain is a RIBBON FIELD: one bit per ribbon.
  Every strand moves y-x by exactly 1 per edge, so all strands are monotone, cross each ribbon once, and are
  translates of one another (generalized parallel lines; staircases {a,b} = mixed words; diagonal free fold = H|V
  word boundary; sharp fold = the same in '\').
- T3 [PROOF]. Angles at a good lattice point: tile corners are 45 deg (knight ends) and 135 deg (unit-edge ends), so
  45 deg(v) + 135 b(v) = 360, and deg = 2 gives b = 2 carried unit edges. Hand case check: a split change ("wall")
  cannot turn or end at a good point, and 4 walls cannot meet there. So walls are straight AXIS lines that end only
  at defects or sides; a horizontal wall forces H on all ribbons that meet it (A|A' fold), a vertical wall forces V.
- T4 [PROOF from audited (1)]. A bad square has >= 2 bad quarters, so the number of bad squares in U is <= E + X - |B|.
- Check: tiling_check.py 6 6: 252 crossing-free 2-factors = 128 single-split (exactly the 2 x 2^6 ribbon fields)
  + 124 with walls, all walls straight full axis lines. Explains LB F8/F9 (<= 2 move types) and all four free folds.
So L1's "parallel field" part is a theorem: outside <= E + X - |B| bad squares, a tour is a set of ribbon-field
domains cut by straight axis walls. OPEN part of L1: the defect squares (O(n) of them) - which defect CURVES exist and
their price per unit length ("interface tension"). This is now a finite problem (section 3, C3).

## 2. Arch / connectivity: the RIBBON-ABSORPTION route (new; CONJECTURE, parts proven)
R1 [ARGUMENT; finite check C2]. Beyond a depth-2 collar, a side in P/P' has steep lines, so the ribbons there are H on
  vertical sides and V on horizontal sides (both splits).
R2 [PROOF from T2-T3]. A ribbon keeps its bit along its good extent. A '/' ribbon from the left side runs to the top
  side, a '\' ribbon to the bottom side: every side ribbon is FRUSTRATED (H at one end, V at the other). Its end must
  be ABSORBED by (i) a wall face with the matching bit (horizontal face <- H ribbons, vertical face <- V), (ii) a
  defect, or (iii) a non-cheap side stretch (+1/row or more). Diagonal folds are parallel to ribbons: they absorb
  nothing. Count: there are 4n - O(1) side ribbon ends, a wall face absorbs 1 end per unit length, a defect cut of a
  ribbon absorbs <= 2 ends: faces + 2 cuts + non-cheap rows >= 4n - O(1).
R3 [CONJECTURE, geometry]. CHEVRON YIELD: a horizontal wall's two faces absorb ends from the same vertical side, and a
  face of length l yields >= l/2 - (defect correction) strands with both ends on that side, all trapped (extend G1 /
  LB F10d from free folds to ribbon-field strands: composite of axis reflections, shift 0).
R4 = L5 [CERTIFIED W <= 4 only]. Each trapped strand pays >= 1/2 privately (Claim 28 per changed end). Needed: W >= 5,
  an arbitrary ribbon field outside the strip (not the fixed (2,1) field), and interior repairs. Interior repairs
  are V ribbons inserted in H regions (jog bands): free inside, but each end is a defect with INTEGER charge +-3
  (S8, G2 step 1). So L5 needs integer-current accounting, not only Z_3 flux.
R5 [CONJECTURE, finite C3]. Defect tension: every defect pays >= 1/4 per absorbed ribbon end. Known prices, all >= 1/4:
  wall faces 1/4 (1/2 strand per unit face x 1/2), gentle seam 1/4 (1.0 per unit x, 4 ends), A|A' vertical seam 1/2,
  shallow side >= 1/4. Zero slack: the fold field and layout G tie.
Consequence if R1-R5 hold with a joint ledger: absorption >= n, so X >= 5n - O(1) WITHOUT the flux machinery (beats
204n/43 and the 5n ceiling of the strip method). Fold field = 4n + n (arch) + 4n/3 (flux) fits exactly.
For 6n: absorption n + flux n (only p = 1/2 per charged path, not 2/3) - but NOT additively for free: a gentle seam
absorbs AND carries +-1 flux at no extra cost (S3), so layout G has absorption + flux = 5n/3 before its trapping
fixes. The missing piece is a JOINT lemma J: absorbing defects that also carry flux leave trapped residue classes
(G3 coset theorem, PROOF in scope) whose repair is priced (G4/G6 measured +1.83/row). J is the hard core of 6n.

## 3. Finite computations (phase 2; all fit 8 GB, one job at a time)
C1 (seconds): machine check of T3 - all split/tile configurations of the 4 squares at a vertex.
C2 (minutes, CP-SAT): R1 - left strip in P/P', good beyond depth d = 2..4: the adjacent ribbon bit is forced.
C3 (main job): interface tension tau(v) for straight defect lines of direction v in {0, inf, +-1, +-1/2, +-2}
  between two ribbon fields, with ribbon bits as EXOGENOUS inputs per column (min over inputs), band width w = 3..5,
  minimum mean cost per absorbed end. State = pending edges + 2 bits, like band.cpp/corr2.cpp (w = 5 there: about
  10^6-10^7 states). Curved defects: tension per local piece + additivity (ARGUMENT; Wulff-type bound).
C4: L5 evidence at W = 5, 6 by periodic CP-SAT (Verifier's claim28_pairing.py approach, p <= 8, with ribbon-field
  exterior). arch.cpp at W = 5 likely exceeds 8 GB (W = 4: 7M states); pilot state count first.
C5: R3 - trace strands in random wall/ribbon layouts (cheap) to test the yield bound; then prove it.
Offer to the Edge Searcher (piece 1): by T1-T4, "arbitrary local configuration" outside the defect set is a ribbon
field, so the carrier model needs exogenous ribbon bits, not arbitrary tours.

## 4. Main risks
1. R5 has zero slack: one cheaper defect type (curved, dislocation, wall end) breaks the 5n route.
2. J (absorption vs flux sharing crossings) may fail: layout G is the template counterexample to naive addition.
3. R3/R4: jog bands and rung merges repair strands through interior defects whose price lives in integer charge
   transport (S8 is ARGUMENT only).
4. Constants: per-domain/per-wall losses must total O(1) or o(n) (number of domains is not bounded a priori).
First milestone I propose for me: C1 + C2 + write-up of T1-T4 for the Verifier, then C3 at w = 3 for the six slopes.
