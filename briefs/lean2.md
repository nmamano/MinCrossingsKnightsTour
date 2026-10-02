Chief Researcher -> KT Lean: great work on the turns theorem (I re-ran the build and #print axioms myself). Next target, in the
same project: the CROSSINGS lower bound X >= 4n - 2 for every 2-factor (hence every closed tour) on the n x n board, by the
tile argument of KT Turns Theory (w-turnstheory/FINDINGS.md sections 6.1 and 6.4; finite certificate check_knight_tiles.py).
Discrete version (no measure theory):
 - Quarter triangles: each unit square [i,i+1]x[j,j+1] of the board's coordinate box [0,n-1]^2 is cut by both diagonals into 4
   quarter triangles; there are 4(n-1)^2 of them.
 - Tile of a knight edge e = ab: the parallelogram with long diagonal ab and short diagonal the unit grid edge with the same
   midpoint; as a set it is exactly 4 quarter triangles (give it as an explicit function of a and the direction), all inside the
   bounding box of a, b.
 - Finite lemma (decide over relative positions, as in check_knight_tiles.py): for distinct edges e, f, tiles share at most 2
   quarter triangles, and share one only if e, f cross properly (open segments intersect; use integer orientation tests).
 - Count: sum over triangles of multiplicity = 4 * (number of edges) = 4n^2; (m-1)_+ <= C(m,2); sum of C(m_t,2) = sum over edge
   pairs of shared triangles <= 2X; and sum of (m_t - 1)_+ >= 4n^2 - 4(n-1)^2 = 8n - 4. So X >= 4n - 2.
Define the crossing count for TwoFactor and for ClosedTour faithfully (Definition 2 of the paper: two distinct moves whose open
segments intersect) and prove the theorem for both. Same rules as before: no sorry, standard axioms only, readable statements,
README update, report to me when done or blocked.
