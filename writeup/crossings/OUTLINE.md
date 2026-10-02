# Crossings blog post: outline (draft 1, 2026-10-02)

Writer: KT Lower Bounds. Same format and voice as writeup/turns/post.mdx (MDX, code-span math, one idea per
section, one picture per idea, dense parts in a short "Details" section). Its own post; Nil decides on a merge.
Working slug: `knights-tour-crossings` (images under /blog/knights-tour-crossings/).

## Headline

Crossings on an `n x n` board, closed tours, even `n`:

| | paper | Shisheng Li | now |
|---|---|---|---|
| upper | `12n` | `11.5n` | `19n/3 + 142 ~ 6.33n` (every even `n >= 96`) |
| lower | `4n - O(1)` | - | `14n/3 - 407 ~ 4.67n` (even `n >= 32`) |

Gap: from `3x` (12/4) to about `1.36x` (19/14).
One idea links the two halves: a mod-3 "charge" that the corners of the board create. The upper bound pays to
carry it; the lower bound makes every tour pay for it.

Status to state in the post (check again before the draft): 19n/3 proof in PROOF_fold.md (Verifier Claim 12:
check the verdict); 14n/3 audited as Claim 19 (PASS), the consolidated PROOF_crossings_lower.md is in audit
(Claim 20).

## Sections

0. **Intro (3-5 one-line paragraphs).** Where the first post left crossings (12n vs 4n, "low-hanging fruit"),
   Shisheng's 11.5n, the new numbers, the gap. TODO markers: title (3 options), how this came about, credits.
   Figure: none, or the cover (a full fold tour).

### Part 1: upper bound

1. **Crossings live at the sides.** Recap: inside the board, parallel straight lines never cross; all crossings
   come from the sides, where the lines turn around. So the cost is "crossings per row or column, per side".
   Figure: a TT16/H16a tour with crossings marked red (reuse the style of tour48.png, crossings instead of turns).
2. **First step: 9n.** A new heel with 16 crossings per 8 columns (vs the paper's 28), found once the four
   knights may come out of the heel in any order (Nil's permutation idea). Sides at 2.5 per row. 2+2+2.5+2.5 = 9.
   Figure: the H16a heel next to the paper's heel, crossings marked. (Fold-set owner: Structures; I can make
   this one from the tour files if Structures does not.)
3. **Dropping the formation.** Short: lane-free pieces reach 343n/48 ~ 7.15n. One paragraph only, as the bridge
   to the next idea (no figure, or a small strip). Possibly cut.
4. **The fold design: 4n + n + 4n/3 = 19n/3.** Fill the board with 8 triangles of straight lines. Where two
   families meet along a "free fold", there are no crossings. Each side uses the cheapest U-turn pattern:
   1 crossing per row, which is the lower-bound rate. That is the 4n.
   Figure (Structures): the 8-triangle field, folds drawn, colours per line family.
5. **Problem 1: trapped lines (+n).** Near the middle of each side, lines turn around twice ("chevrons") and
   close into many short cycles instead of one tour. Fixing them ("arch flips") costs n in total.
   Figure (Structures): one chevron trapped into a short cycle, then the arch flip.
6. **Problem 2: the corners' charge (+4n/3).** Each corner creates a mod-3 charge that has to travel to the
   centre. Along a diagonal fold, a corridor carries it at 2/3 crossing per step: 4 diagonals x n/2 x 2/3 = 4n/3.
   Figure (Structures): the four diagonal corridors.
   HARD PLACE: "charge" must be introduced here before the lower bound defines it. Plan: here only the
   picture-level story ("a defect that cannot vanish, only move"); the definition comes in Part 2, section 9.
7. **Why it stops at 19n/3.** Every way to untrap the chevrons costs about n in this family (UNTRAP.md:
   chevrons are always trapped; edge repair >= 1 per trapped row; jog bands carry an odd charge). Mark clearly:
   this is a limit of one family of layouts, NOT a lower bound for tours.
   Figure: none (or the cost bar 4n | n | 4n/3).
   Also: one line on the all-n proof (block insertion, matching period 48: a +24 step switches between two
   matchings that are both one cycle), with the details in section 13.

### Part 2: lower bound

8. **The old 4n, as one picture: knight tiles.** Each knight move owns a parallelogram of area 1 (its long
   diagonal is the move, its short diagonal is a unit grid edge). n^2 tiles of area 1 on a board of area
   (n-1)^2: about 2n of area too much. Two tiles overlap only if their moves cross, and then by at most 1/2.
   So X >= 4n - 2. Lean-checked (theorem names in Details).
   Figures (me): (a) one tile and its 4 quarter triangles; (b) the two overlap sizes (1/4 and 1/2); (c) a
   small board covered by tiles, overlaps red, gaps white.
9. **Gaps cost too, and the corners force gaps.** Area is exact: every uncovered quarter must be paid by more
   overlap. The colour flux (black/white cells) through a path of unit squares, mod 3, gives each path a
   "charge". If a path is charged, some square on it is defective.
   Figure (me): a dual path through square centres, one step with its two neighbouring quarters.
   HARD PLACE: the mod-3 flux. Plan: state it as a conserved quantity with a picture ("count the moves that
   cross the path, black-to-white minus white-to-black, plus the grid edges; mod 3 it only depends on the
   ends"), skip the derivation, point to the companion proof.
10. **Corners: about 2n charged paths.** Around each corner, the square path at radius R (right side and top
   side of the box [0,R]^2) is charged, if the boundary rows at its two ends look normal. Radii 12..n/2-4 at
   4 corners give 2n - 60 disjoint charged paths.
   Figure (me): the four corner families of nested paths; one corner box with its path and the two end rows.
   HARD PLACE: why the charge is 1 mod 3. Plan: "the box boundary has total charge 0; the outside part is a
   short computation from the two end rows; so the inside part carries the rest". Computation in Details.
11. **Each charged path costs half a crossing.** A defective unit square has at least two bad quarters: each
   tile covers two adjacent quarters of a square, so m0 - m1 + m2 - m3 = 0. The bad quarters of different paths
   are different, and two bad quarters cost at least one extra crossing (2L <= 4E + 44). With all ~2n paths
   charged: about n extra crossings, so X >= 5n - O(1) for tours with no abnormal end rows.
   Figure (me): a square with the alternating sum, one bad quarter forcing a second one.
   HARD PLACE: the accounting from bad quarters to crossings. Plan: give the rate only ("two bad quarters
   cost at least one extra crossing"), the inequality in Details.
12. **Abnormal rows: stability (from 5n-if-normal to 14n/3 for every tour).** A tour can switch a path's charge off by making an end row
   abnormal. But an abnormal row costs at least 1 extra crossing in its side strip (computer certificate on the
   width-2 strip; sharp: the pattern (1,y)-(0,y+2), (2,y)-(0,y+1), (2,y)-(1,y+2) costs exactly 1 more per row).
   Balance: b abnormal rows remove b paths (saving b/2) but add b crossings: E >= n - b/2 and E >= b - O(1),
   so the best a tour can do is b = 2n/3, E = 2n/3: X >= 14n/3. (With the old per-row rate 1/2 this gave 4.5n.)
   Figure (me): the strip, a normal row pattern (1 crossing/row) and the sharp abnormal pattern (2/row).
   HARD PLACE: the strip certificate is a computer proof on 82,516 states (shortest-path potential). Plan:
   explain as "the computer checks every possible strip, row by row, and finds no way to have an abnormal row
   for less than one extra crossing"; the certificate and the independent checker go to Details.

### Part 3: the gap and the details

13. **The gap.** 4.67n vs 6.33n. Where each side could move: lower bound limited by the 4-row corner windows /
   the 4E term; upper bound by the arch term (n) and the flux term (4n/3). Mark open questions; no promises.
   Figure: a number line 4, 4.5, 4.67 | 6.33, 7.15, 9, 11.5, 12 with the history.
14. **Details.** All-n proof of the fold tours (block insertion, the two matching states rho and rho^3);
   tile lemma (1,292 pairs); flux identity; corner charge computation; |B| >= 4n - 24; the stability
   certificate (potential [-29,0], two independent checkers); the final arithmetic; what is checked by whom
   (Verifier claims, Lean theorems for 4n - 2). Link TODO for the companion proofs and code.
15. **Open questions** (short) + TODO credits + TODO links.

## Figures: split

- Structures (writeup/crossings/figures/): fold set (sections 4-7), possibly 1-3.
- Me (same style, same folder, PNG for the post + vector PDF): sections 8-12 (tiles, quarters, overlaps, tiled
  board, dual path step, corner box, nested corner paths, square identity, strip patterns), 13 (number line).
- I will ask Structures for its palette and line widths before I draw, so that the two sets match.

## Hard places (summary)

1. The mod-3 charge appears in both halves; it must be introduced once, simply, and reused (sections 6, 9).
2. Why each corner box has charge 1 mod 3 (section 10): a computation, hard to make visual.
3. From bad quarters to crossings (section 11): an inequality with constants; give the rate only.
4. The strip certificate (section 12): a computer proof; explain what is checked, not how.
5. "19n/3 is where this family stops" must not read as a lower bound (section 7).
6. Length: two full constructions + one long proof. If the post runs too long, cut section 3 (lane-free) and
   compress 5-7, or split the post into "upper" and "lower" (Nil decides).

## Questions for the Chief Researcher

- Is the fold-proof audit (Claim 12) PASS? The post states the fold tours as proved only if so.
- Should the 9n and 7.15n steps stay (history), or go straight to the fold design?
- One post or two (upper / lower)?
