# KT Structures - gap mission findings (gap/structures/)

Role: UPPER bound. Arch term (n) of the fold design, and designs outside the fold family.
Conventions as in w-structures/FINDINGS.md (x right, y up; free-fold 8-cycle of LB F10a).
Run scripts from this folder with ../../.venv/bin/python.

## G1 (2026-10-03, PROOF): same-edge nests are chevron type; 4-fold and 7-fold nests do not exist

Statement. Let a tour path leave the left edge strip in direction (2,1) at A=(0,a) and return to the left edge
at B=(0,b) in a steep-family direction (-2,+-1), with the path between them simple and inside the board.
Then its total tangent rotation is exactly +126.87 deg, and b > a, and the end direction is (-2,1).
If all its turns are free folds (walk on the 8-cycle), the walk has net step +1.

Proof. Close the path with the edge segment from B to A (outside the path). The closed polygon is simple,
so its turning number is +1 or -1 (Umlaufsatz): +360 deg if b > a (the region is on the left of the downward
segment), -360 deg if b < a. Every turn of the polygon lies in (-180,180) deg: knight vectors are never
opposite on a simple path, and the two corner angles at A and B are between a knight direction and a
vertical direction. So the two corner angles are FIXED by the directions, and the rotation of the path is
fixed too (turning.py prints the table):
  end (-2,1): +126.87 (above) or -233.13 (below);  end (-2,-1): +180 or -180.
On the 8-cycle a back-and-forth step pair cancels exactly, so a walk with net step k has rotation R(k):
R(1) = 126.87, R(2) = 270, R(3) = 396.87, R(4) = 540, R(-1) = -143.13, R(-2) = -270, R(-3) = -413.13, R(-4) = -540,
and |R(k)| > 360 for |k| >= 3. Only R(1) = +126.87 is in the table (turning.py 11 confirms it by enumeration of all
walks of length <= 11).
So: a "4-fold spiral" (net step +-4, rotation +-540) and a "7-fold" nest are impossible for ANY simple
path, not only for monotone ones. This upgrades LB F14a (MEASURED) to PROOF and closes the BRIEF lead
"4-fold same-edge nests" (S9 Open).

Consequence (PROOF). The composite fold isometry g of a free-fold same-edge nest has the linear part of the
chevron (reflection in a horizontal axis). So g is a reflection or a glide reflection along a horizontal axis.
A nonzero glide (needed for an odd index shift, LB F10b) comes only from pairs of parallel non-horizontal folds
(diagonal pair = jog band, translation (d,-d); vertical pair, translation (2e,0)). Each such pair is a
corridor with odd shift, so odd current (w-structures S8 lemma), so charged ends. Thus free-fold geometry
alone can never untrap the midpoint arches; every untrapping mechanism pays for a defect structure
(edge flips, or charged corridors). The arch question is now a pure cost question.
Commands: `python turning.py 11`.
