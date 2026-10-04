# KT Integrator findings

## 2026-10-02: 9n crossings CONFIRMED in full tours (H16a and H16b)

Construction: bottom heel tiled on the bottom band and (rotated 180) on the top band; paper
VerticalEdge (off_L = 0) on the left band and (rotated 180) on the right band; lines x+2y=c in the
interior; four 6x6 corner zones filled by CP-SAT (kt/board.py `complete`).

Proof status:
- Every tour below is a single closed knight's tour: kt.core.validate AND an independent walk
  (assemble.walk_check) pass.
- Crossings by kt.core.num_crossings. Independent all-pairs numpy counter (assemble.brute_crossings)
  agrees on n = 48, 50, 52, 54, 64, 66, 68, 70 (8 tours, all equal).
- Each corner completion is OPTIMAL for its 6x6 zones (lexicographic: crossings, then turns). It is
  not optimal over bigger zones; the constants b below are upper bounds of this construction only.

### H16a = ['26 26 36 36 36 36 56 26','23 36 36 36 13 23 23 23','26 26 26 27 27 27 27 26','67 67 67 67 67 67 67 67']
Crossings, n = 48..142 (all even n, 69 tours):

| n mod 8 | X(n) |
|---|---|
| 0 | 9n + 5 |
| 2 | 9n |
| 4 | 9n + 7 |
| 6 | 9n + b, b = 3 / 1 / 2 for n mod 24 = 6 / 14 / 22 |

Turns (corner tie-break on turns, n = 64..112): T(n) = 41n/4 + c, c periodic in n mod 24,
c in [-30.5, -18]. Slope 10.25 = 2 * (25/8 + 8/4). Example: T(64) = 630, T(88) = 876, T(112) = 1122.

### H16b = ['46 46 56 56 56 26 46 46','14 14 14 45 45 45 45 46','05 15 15 15 15 05 05 05','01 01 01 01 01 01 01 01']
n = 64..112: X(n) = 9n + b with b in {0..4} periodic in n mod 24
(n mod 8 = 4: always 9n + 4). Turns: T(n) = 43n/4 + c (n mod 8 = 0: c = -25).
Slope 10.75 = 2 * (27/8 + 2). H16a is better on turns, equal on crossings.

Comparison at n = 64: this construction 581 crossings; paper 12n + O(1) (~768); Shisheng 11.5n.

Raw tables: runs/H16a.txt (turn tie-break, 64..112), runs/H16a_noturn.txt (64..142),
runs/H16b.txt. Tours: tours/*.json (board.js grid in key "tour").
Certificates: tours/certificates/H16a_VerticalEdge_off0_n{48,64,66,68,70}.json (one per residue
n mod 8 = 0, 2, 4, 6 plus n = 48). Picture: tour_n48.png (437 crossings red, 465 turns).

## Fixes to kt/board.py (2026-10-02)
- Lane-alignment formulas in build_skeleton: checked by derivation (see docstring) and confirmed
  by the full tours. They were correct.
- `complete` rewritten. The draft re-solved a full optimisation per lazy-cut round (30 s per round,
  weak "sum <= len-1" cuts) and did not converge. Now: each fixed path between free cells is
  contracted to one dummy node, and CP-SAT AddCircuit over free cells + dummies forces exactly one
  Hamiltonian cycle. No lazy cuts. Objective 1000 * crossings + turn_weight * turns.
- Zone size matters for the optimiser: Z = 6 solves to OPTIMAL in 3-20 s; Z = 8..14 stay FEASIBLE
  with much worse corners in 30 s (n = 64: corner crossings 106 at Z=6, 204 at Z=8, 622 at Z=12).
- Asserts: bottom period % 8 == 0, left period % 4 == 0, Z > band depth, 2Z <= n.

## Observations
- Corner cost depends on n mod 24, not only n mod 8. Probably the per-period strand permutation
  of the heel has order 3, so the strand order that reaches the far corners cycles with n.
- No alignment, zone-size, wrap-edge or parity problem showed up: with off_L = 0 every even n from
  48 to 142 completes at Z = 6 at the first try.

## assemble.py (gadget pipeline for other workers)
  .venv/bin/python w-integrator/assemble.py --bottom H16a --left VerticalEdge --off-L 0 64 66 68 70
Templates: a name (H16a, H16b, PaperHeel, VerticalEdge), ';'-separated rows, or a JSON file
with a list of row strings. Bottom template: local lane offset 0, period % 8 == 0.
Left template: local offset off_L (Strip 'left' convention), period % 4 == 0.
Options: --Z 6,7,8 (tried in order), --time, --workers (<= 3), --turn-weight 1, --brute, --tag.
Writes tours/<tag>_n<n>.json, appends tours/<tag>_table.tsv, prints differences per n mod 8.
render.py <tour.json> <out.png> draws a tour with crossings marked.

## 2026-10-02: mission 2 infrastructure (lane-free gadgets)
- kt/board.py build_general(n, bottom, left, top, right, phases=(xb, xt, yl, yr), Z): any four
  periodic templates and phases. build_skeleton (lane design) now calls it; regression n=64, 70 same.
- strands.py: pairing() = line-end matching induced by a gadget (unrolled trace, checks loops and
  uncovered cells); region_check() = per region (BL, MID, TR) finite cycles, strands, cut counts;
  parity() = matching parity.
- Cut-parity rule (proof: a cycle meets every edge cut an even number of times; the cut {c <= t}
  far from the corners is crossed only by band edges, and their count has the parity of the
  number of matching pairs spanning t). pi(M) = (#pairs spanning t|t+1) - t mod 2 is independent
  of t. Each region needs equal pi for its two matchings. Shift by s adds s; reflection
  c -> K - c adds K - 1. For even n, BL and TR can always be fixed by the bottom/top phase
  (step 1 in c); MID needs pi(L) = pi(R) (left/right phases step 2 in c).
- Block d-pair matchings (a <-> a + d, a mod 2d < d): two of them have no finite cycle only at
  shift d mod 2d, with d strands. Odd d fails parity. So block c <-> c-3 on the left has no
  d-pair partner.
- Lane design, auto phases: 16 valid phase sets at n = 64 (some regions with 2 strands); best
  n = 64 tour has 578 crossings (formation alignment 581).
- assemble.py --phases auto|lane|xb,xt,yl,yr, --top, --right, --tries.
- combos.py menu.json: ranks (B, T, L, R) combos by slope X_B/P + X_T/P + X_L/Q + X_R/Q, filters by
  MID parity and finds phases for n and n+2.

## 2026-10-02: period-24 argument, H16a + VerticalEdge for ALL even n >= 48
Script: period24.py. Output: runs/period24_a.txt, runs/period24_b.txt.
Base corner completions: corners/H16a_VE_res{00,02,...,22}.json (one per even residue mod 24,
solved at n0 = 48..70, zone-relative moves of the four 6x6 zones, apply to
build_skeleton(n, H16a, VerticalEdge, off_L=0, Z=6)).

(a) Why the period is 24 (status: argument + computer check, not a formal proof).
- Per 8 lines (one lane-pair block) the 4 formation strands are permuted. Computed from the
  real line matchings (region_perm in period24.py): BL (bottom+left) [1,2,0,3], order 3;
  MID (left+right) identity, order 1; TR (right+top) [0,2,3,1] or [3,1,0,2] (depends on n mod 4),
  order 3. (sigma_B of H16a alone = [0,3,1,2], a 3-cycle; VerticalEdge = (01)(23).)
- n -> n+24 adds exactly 24 lines (3 blocks) to each region (BL: c < n, MID: n..2n-2, TR: > 2n-2),
  so each region's strand permutation is multiplied by rho^3 = identity. The neighbourhood of
  every corner zone depends only on the band phases (x0 = 0, X0 = 5 - 2n mod 8, Y0 = -n/2 mod 4),
  i.e. on n mod 8. Hence the outside path matching (zone-relative ends of all fixed paths) is
  periodic in n with period 24. Checked directly for every even n = 48..118: matching(n) =
  matching(n+24), and matching(n) != matching(n+8), != matching(n+16) (3 matchings per residue
  mod 8, as the KT Verifier found).
- Counts: crossings and turns are local (crossing segments have endpoints within distance 3).
  n -> n+24 adds 3 bottom periods to the bottom and top bands and 6 left periods to the left and
  right bands, with identical neighbourhoods elsewhere. So dX = 2*3*16 + 2*6*10 = 216 = 9*24 and
  dT = 2*3*25 + 2*6*8 = 246 = (41/4)*24.

(b) Base completions reused for all larger n (status: VERIFIED for n0 + 24k, k = 0..5, n <= 190):
every transplanted tour passes kt.core.validate and the independent walk; X - 9n and
T - T(n0) - 246k are exactly constant:

| n mod 24 | n0 | X(n) | T(n) |
|---|---|---|---|
| 0  | 48 | 9n+5 | 41n/4 - 27 |
| 2  | 50 | 9n   | 41n/4 - 26.5 |
| 4  | 52 | 9n+7 | 41n/4 - 26 |
| 6  | 54 | 9n+3 | 41n/4 - 27.5 |
| 8  | 56 | 9n+5 | 41n/4 - 25 |
| 10 | 58 | 9n   | 41n/4 - 26.5 |
| 12 | 60 | 9n+7 | 41n/4 - 26 |
| 14 | 62 | 9n+1 | 41n/4 - 30.5 |
| 16 | 64 | 9n+5 | 41n/4 - 26 |
| 18 | 66 | 9n   | 41n/4 - 26.5 |
| 20 | 68 | 9n+7 | 41n/4 - 18 |
| 22 | 70 | 9n+2 | 41n/4 - 25.5 |

So for every even n >= 48: 9n <= X(n) <= 9n + 7 with this construction.

## 2026-10-02: T18 (turns) - exact formula for all even n >= 48
Heel T18 (KT Turns Builder, w-turnsbuilder/T18-P8-D4.json, lane rule, 18 turns + 31 crossings
per 8 columns): ['26 26 26 26 36 26 26 26','36 26 36 36 26 26 45 46','25 25 25 26 15 27 26 26','16 67 16 67 67 06 01 16']
on bottom + top, paper VerticalEdge (off_L = 0) on left + right, 6x6 corner zones.
Line-end pairing per 8 lines: (0,7) (1,4) (2,6) (3,5).
Corner objective: TURNS first (weight 1000), crossings tie-break (weight 1); all 12 base
completions OPTIMAL for the 6x6 zones.
Script: period24.py --bottom ../w-turnsbuilder/T18-P8-D4.json --tag T18 --objective turns --time 120
Output: runs/T18_period24_a.txt, runs/T18_period24_b.txt; base corners corners/T18_res{00..22}.json.

(a) Strand permutation per 8 lines: BL [2,1,3,0] order 3, MID identity, TR order 3 (as H16a).
    Outside path matching: matching(n) = matching(n+24) for every even n = 48..118; it differs
    from n+8 and n+16.
(b) Each base completion reused unchanged at n0 + 24k, k = 0..5 (n <= 190): all 72 tours valid
    (kt.core.validate + independent walk). Per +24: dT = 204 = 8.5*24 = 2*(3*18 + 6*8),
    dX = 306 = 12.75*24 = 2*(3*31 + 6*10), exactly, every residue.

Result (VERIFIED for n <= 190, period argument for larger n):
  T(n) = 8.5n + b, b = -17, -19, -19, -20 for n mod 8 = 0, 2, 4, 6   (all even n >= 48)
  X(n) = 12.75n + c, c in [-25.5, -16] (depends on n mod 24)
Turns record before this: 9.25n (paper).
Certificates (brute-force crossings agree): tours/certificates/T18_VerticalEdge_off0_n{64,66,68,70}.json
(n=64: T=527, X=795; n=66: 542/816; n=68: 559/843; n=70: 575/869).

## 2026-10-02: first lane-free full tours, slope 7.833n (VERIFIED n = 72, 96, 120)
Menu: w-searcher/MENU.md (first partial), converted to menu1.json, gadgets/*.json.
combos2.py (region-separable search over all B, T, L, R and phases; n = 96, 98, 100, 102):
145 feasible combos; best slope 7.833 (runs/combos2_menu1.txt).
Tour LF1: bottom b_free_P6D4 (block {c,c+3}, c = 3,4,5 mod 6; 11 per 6 cols), top b_d1lowm20_P6D4
(18 per 6 cols, FEASIBLE), left l_d5lowm20_P4D2 (8 per 4 rows), right l_free_P4D2 = '23 27'
(d=3 low odd, 4 per 4 rows). Phases (1,1,0,0); strands BL 2, MID 4, TR 2.
n = 72, 96, 120: X = 575, 763, 951 = 23n/3 + 11 (brute-force count agrees), T = 797, 1073, 1349
(11.5n, not optimised). Corners 6x6 OPTIMAL. Tours: tours/LF1_n*.json.
Compatibility facts (diag.py, combos2.py):
- block-d3 bottom optimum: compatible with left d=5/low even; NOT with d=3/odd or d=1/even.
- MID partners of left d=3/odd: d=1/even (2 strands), d=5/even (4), d=7/odd (2).
- bottom pure parity classes compatible with left d=3/odd: d=1 (2 strands), d=5 (4), d=7 (2);
  not d=3, not mixed {1,5} (odd cuts).
- Bottleneck: cheapest bottom-type gadget compatible with d=3/odd. At 1.833/col -> 6.67n.

## 2026-10-02: lane-free slope 7.333n (VERIFIED n = 72, 74, 76, 78, 96, 120)
menu2.json (mkmenu.py from menu_results.jsonl, 24 gadgets); combos2.py: 2842 feasible combos,
best 7.333 (runs/combos2_menu2.txt). Tour LF2: bottom b_free (1.833/col), top b_d7lowm20
(`36 56 / 23 13 / 26 27 / 67 67` repeated, 2.5/col), left l_d5lowm20 (2/row), right l_free = d3/odd (1/row).
X = 549, 564, 578, 592, 725, 901 for n = 72, 74, 76, 78, 96, 120; X = 22n/3 + 21 for n = 0 mod 24
(brute-force count agrees on all). T ~ 11n (not optimised). Corners 6x6 OPTIMAL. tours/LF2_n*.json.
Note: odd n has no closed tour (n^2 odd, bipartite graph). A region with ONE strand fails the cut
parity rule (free bottom + left d1/even is such a case).

## 2026-10-02: TT16 - turns 8n - 14 for all even n >= 48 (matches the 8n - O(1) lower bound)
Gadgets: bottom AND top = T16 (KT Turns Builder, w-turnsbuilder/lex-free-P8-D4.json, lane-free,
16 turns + 26 crossings per 8 cols): ['26 26 26 26 26 26 26 26','36 26 26 46 26 46 36 26','25 26 25 26 26 25 26 25','16 67 06 16 06 16 16 67'];
left = d=3/odd '23 27' (2 turns, 1 crossing per row); right = d=5/even '02 24' (2 turns, 2 crossings per row).
Phases (xb, xt, yl, yr) = (0, 1, 0, 0); strands BL 2, MID 4, TR 2. 6x6 corners, TURNS first, crossings tie-break.
combos2.py --metric T over menu_turns.json (menu2 + T16 + T18): minimum turn slope 8.0, 12 feasible combos
at 8.0 (runs/combos2_turns.txt).
Script: periodic.py (general period-in-n tool). Output runs/TT16_periodic.txt, runs/TT16.txt.
(a) Outside path matching has period 8 in n (checked n = 56..200). Per +8: dT = 2*16 + 2*8*2 = 64,
    dX = 2*26 + 8*1 + 8*2 = 76.
(b) 4 base completions (n0 = 56, 58, 60, 62; corners/TT16_res{00,02,04,06}.json, all OPTIMAL)
    reused unchanged at n0 + 8k, k = 0..10 (n <= 142): all 44 tours valid (validate + walk).
    n = 48..54 solved directly (assemble.py, fixed phases): valid, same formula.
Result (VERIFIED for every even n = 48..142; period argument for larger n):
  T(n) = 8n - 14                              (every even n >= 48)
  X(n) = 9.5n + c, c = -2, -3, 0, +3 for n mod 8 = 0, 2, 4, 6
Brute-force crossing count agrees on n = 48..62, 72..78, 96.
Certificates: tours/certificates/TT16_n{56,58,60,62}.json. Picture: tour_TT16_n56.png.

## 2026-10-02: lane-free crossings 7.208n (VERIFIED n = 72, 74, 76, 78, 96, 120)
Tour LF3: bottom b_free (1.833/col), top = Edge Searcher's vsL3odd gadget P8 D4, 19 per 8 cols
(`36 36 36 26 26 26 36 26 / 34 36 23 23 23 36 26 36 / 26 27 27 27 26 26 26 27 / 67 67 67 67 67 67 67 06`,
gadgets/b_vsL3_P8_2375.json), left d=5/even (2/row), right d=3/odd (1/row). Slope 1.833+2.375+2+1 = 173/24.
X = 539, 556, 567, 579, 712, 885 for n = 72, 74, 76, 78, 96, 120; for n = 0 mod 24 X = 173n/24 + 20
(dX = 173 per +24). Brute-force count agrees on all 6. Corners 6x6 OPTIMAL (crossings first). tours/LF3_n*.json.

## 2026-10-02: lane-free crossings 343n/48 = 7.146n (VERIFIED n = 96, 98, 100, 102, 144)
Tour LF4 = LF3 with the Searcher's P16 top gadget (37 per 16 cols, gadgets/b_vsL3_P16_23125.json).
X = 707, 721, 738, 751, 1050 for n = 96, 98, 100, 102, 144 (brute-force count agrees on all);
for n = 0 mod 48: X = 343n/48 + 21. tours/LF4_n*.json.

## 2026-10-02: FOLD design (KT Structures field) - exact slope 19n/3 = 6.333n (VERIFIED)
Split agreed by CR: Structures owns the design, Integrator owns assembler + numbers.
Input: w-structures fold field (fold3.build via paste_field with tgs = {}: t = 1, arch flips on
y in [n/2 - n/4, n/2) of every edge frame): X_pre = 5n, 32 paths, 52 defect cells (13 clusters).
Corner windows carry colour imbalance -1/+1/-1/+1; Structures' diagonal templates (tgs = 1) make
closed loops that grow with n (16/48/80 at n = 48/96/144), so I do not use them.
My route for the colour flux: FREE diagonal corridors |y - x - 1| <= 1 (BL frame, rotated to all 4
quadrants), corner -> centre. Cluster windows radius 4 (radius 3 is degree-infeasible at the flip ends).
Solver: kt.board.complete with feasibility=True (no objective; 3-16 s for ~1300-1600 free cells),
then kt.board.lns (8x8 windows, hint = current tour). New in kt/board.py: complete(feasibility=,
ties=) and lns().
Free corridors + LNS only (fold_assemble.py, runs/foldB1.txt): n = 48, 96, 144: X = 440, 727, 1045
(valid, brute-force agrees), local optima, slope 6.30 average.
Exact slope (fold_period.py): the corridor middle (lo+3 <= x < n/2 - lo - 3, lo = 8) is tied to
period 6 along the diagonal; base n0 solved (feasibility, then alternating periodic middle re-solve
and LNS on the rest); then for n = n0 + step*k the field is rebuilt, the corridor template pasted,
all other free components copied by translation (no new solve), and the tour validated.
- n0 = 96, step 12 (runs/foldX96.txt): X = 717, 793, 869, 945 at n = 96, 108, 120, 132: +76 per +12.
  X = 19n/3 + 109 for these n. Turns 1243, 1395, 1547, 1699 (+152 per +12).
- 76 per 12 = 60 (field, 5n) + 4 corridors x 4 crossings per period of 6 (Structures' OPTIMAL band
  value 4/6 per unit x). Slope 5 + 4 * (2/3) * (1/2) = 19/3.
- The outside path matching has period 24 for n = 0 mod 4 bases (n0 + 12 is not always a single
  cycle; n0 + 24 is); for n = 2 mod 4 bases step 12 worked (runs/foldX_res.txt).
- Running: one base per even residue mod 24 (n0 = 96..118), step 24 (runs/fold24.txt).
- DONE (runs/fold24.txt): 12 bases n0 = 96, 98, ..., 118 (one per even residue mod 24), each reused at
  n0 + 24k, k = 0..2 (n up to 166): all 36 tours valid; every step +24 adds exactly 152 = (19/3)*24.
  X(n) - 19n/3 = 112, 131.3, 141.7, 108, 117.3, 114.7, 104, 106.3, 129.7, 142, 115.3, 127.7 for
  n0 = 96..118 (the constant depends on the LNS quality of each base; not optimised).
  Result: X(n) <= 19n/3 + 142 for every even n >= 96 (VERIFIED n <= 166, period-24 argument beyond).
  Brute-force count agrees (n = 96: 720, n = 118: 875). Certificates tours/certificates/FOLD24_n{96,98,100,102}.json.
  Picture: tour_FOLD_n96.png.

## 2026-10-02: lane-free with the Searcher's P26 top (2.192/col): slope 274/39 = 7.026n (VERIFIED)
Tour LF5: bottom b_free, top gadgets/b_vsL3_P26_2192.json (57 per 26 cols), left d5/even, right d3/odd.
n = 104, 156, 208, 260: X = 757, 1121, 1486, 1853 (all valid, brute-force agrees).
260 - 104 = 156 = one common period (lcm of 6, 26, 2*4 rows): dX = 1096 = 156 * 274/39 exactly.
(Superseded on crossings by the fold design, 19n/3.)

## STATE FOR A FRESH SESSION (2026-10-02, written at handoff)
Role: KT Integrator (Research Lab), manager = Chief Researcher. Rules: CP-SAT
num_workers <= 3, one heavy job at a time, work only in w-integrator/ (and demo/ for the new mission),
report via POST /api/agents/<CR>/messages, hand off at ~50% context.
Key code (all in w-integrator unless noted):
- kt/board.py (owned): build_skeleton (lane design), build_general (any 4 templates + phases),
  fixed_paths, complete(n, nb, free, feasibility=, ties=, turn_weight=, crossing_weight=) (AddCircuit
  over free cells + contracted fixed paths), lns(), to_grid.
- assemble.py: edge-gadget tours (--phases lane|auto|xb,xt,yl,yr, --top/--right, --objective turns).
- strands.py / combos2.py / diag.py: strand calculus (pairing, region rules, cut parity).
- period24.py (lane designs), periodic.py (any combo, period-in-n), corners/*.json base corner data.
- fold_assemble.py / fold_period.py: fold design (Structures field) -> 19n/3; FOLD_DATA.md.
- fold_jog.py, jog_rule*.py: jog bands (stopped: no self-carrying band exists, Structures S8).
- render.py: PNG of a tour.
Results (all verified): H16a 9n (+0..7, all even n >= 48); T18 turns 8.5n+b; TT16 turns 8n-14
(all even n >= 48); lane-free 274n/39 (parked); FOLD 19n/3 + c (c in [104,142], all even n >= 96,
bases corners/FOLD24_base_n96..118.json, step 24).
Tours on disk: tours/*.json (key "tour" = board.js grid), tours/certificates/.
How to regenerate a tour for any n:
- H16a: corners/H16a_VE_res{n%24}.json + period24.apply_zone (default B=H16a, L=VerticalEdge).
- T18: period24.py with B = w-turnsbuilder/T18-P8-D4.json, corners/T18_res*.json.
- TT16: periodic.Combo(B=T=gadgets/b_T16.json, L=gadgets/l_free.json, R=gadgets/l_d5lowm20.json,
  phases (0,1,0,0), Z=6).apply(n, corners/TT16_res{n%8:02d}.json zones), n >= 56; n=48..54 solved directly.
- FOLD: fold_period.py transplant code with corners/FOLD24_base_n{n0}.json, n0 = 96 + (n-96) % 24.
- Paper heel: kt/gentour.gen_tour(n, n) (Algorithm 1 port, 12n).
Open/standby: KT Structures searches cheaper arch fixes (layout G trapped); Edge Searcher carriers.
NEW MISSION (from Nil via CR): interactive demo (see handoff brief).

## 2026-10-02: interactive demo (demo/, isomux app knight-demo)
Served as the office demo app. Details and rebuild recipe: demo/README.md.
284 tours (FOLD n = 96..200, H16a/TT16/paper n = 48..200, even n) rebuilt from the saved recipes; all valid
(kt.core.validate + walk_check + independent JS check), counts agree, brute force agrees at n = 96, 98, 120.
New: FOLD step-24 transplant valid for every even n <= 200 (before: <= 166). Exact slopes over the data:
FOLD T 38n/3, H16a T 41n/4, TT16 X 19n/2, paper T 19n/2. The Opt-heel port of Algorithm 1 fails for
n = 2 mod 4 and n = 6 mod 8 (corner case 1); the demo uses the default heel in that one corner piece.
Addition (2026-10-02, Nil via CR): full progression in the demo (crossings: 13n, 12n, 11.5n, 9n, 343n/48, 19n/3;
turns: 9.5n, 9.25n, 8.5n, 8n-14). 645 tours, all valid, JS counts agree, brute force agrees at n = 96, 98, 120.
The paper's 21-turn heel rebuilt by heel21.py (OPTIMAL 21 turns / 31 crossings, gadgets/heel21.json); in Algorithm 1
it gives T slope 37/4 = 9.25 exactly. Details: demo/README.md.

## Public repo sync recipe (github.com/nmamano/knights-tour-bounds; staging ~/nil/knights-tour-bounds)
SUPERSEDED 2026-10-03 by the MinCrossingsKnightsTour recipe below. knights-tour-bounds stays as is (Nil decides archive or keep).
Pushed: 1f8817d (Nil), 120be78 (charts). Final re-sync, fresh-copy run and commit + push wait for the CR's go.
rsync -a from ~/nil/knight-formation-research/ with --exclude= /.venv/ /ktlean/.lake/ /ktlean/.git/ /CR_STATE.md
/paper.pdf /paper.txt /board-patched.js __pycache__/ '*.npy' /w-searcher/tm /w-searcher/cert/{certify,certify2,
corner_charge,strip2} /w-searcher/carrier/{band,band2} /w-verifier/claim22_pdf_page.txt
/w-verifier/claim22_figure11_stream.txt /writeup/WRITER_STATE.md '/w-verifier/claim23*_clean/'.
After rsync: replace knight-demo.office URL in w-integrator/FINDINGS.md line 280 by "Served as the office demo app."
Staging still holds WRITER_STATE.md and claim23*_clean/ on disk (rm blocked by hook); .git/info/exclude keeps them out.
Fresh-copy run: rsync staging (no .git) to /tmp/ktb-fresh, run every command in the Appendix sections of
writeup/{turns,crossings}/post.mdx with system python3 (script /tmp/ktb-run.sh; add the new margins check). 2026-10-02: 12/12 PASS.
Then privacy scan (emails, tokens, agent ids, office URLs), commit with Co-Authored-By line, git push origin main.

## Public repo sync recipe (since 2026-10-03): github.com/nmamano/MinCrossingsKnightsTour, folder bounds-2026/
Clone: ~/nil/MinCrossingsKnightsTour (default branch master; push directly to master as Nil, no branches).
bounds-2026/ came in by `git subtree add --prefix=bounds-2026 ~/nil/knights-tour-bounds main` (full history).
Old 2019 files at the root (index.html, board.js, Code/, License.txt ...) stay unchanged; GitHub Pages serves master "/"
(.nojekyll at the root, so no Jekyll build). Demo (since 2026-10-03 the Pages landing page): https://nmamano.github.io/MinCrossingsKnightsTour/ ;
the sync script writes the root index.html from demo/index.html; bounds-2026/demo/ redirects to the root.
1. `sh w-integrator/sync_public.sh` (add --dry-run -i -c to preview). rsync -a --delete with the same excludes as the old
   recipe (incl. /writeup/WRITER_STATE.md, /w-verifier/claim23*_clean/, /CR_STATE.md, /.venv/, /ktlean/.lake/ + .git/,
   /paper.pdf, /paper.txt, /board-patched.js, *.npy, __pycache__/, the 7 compiled C++ binaries in w-searcher, the 2 claim22
   extracts). gap/ IS included. Repo-only files bounds-2026/{.gitignore,README.md,requirements.txt} are excluded, so
   --delete keeps them. Every ELF binary found in the research dir is excluded too (list built at run time). *.bin, *.drup, *.cnf and every other data file over 5 MB are excluded (CR rules 2026-10-03; the script prints them: report them to the CR). The 3 claim27_*.bin pushed in ed0de7a stay tracked (excluded = not deleted). The script replaces the office demo URL line in w-integrator/FINDINGS.md, and fails on any
   office-domain string or any ELF binary left in bounds-2026/.
2. bounds-2026/.gitignore re-includes *.log, *.aux, *.out, *.toc (and other LaTeX outputs) that the root .gitignore ignores.
3. Fresh-copy run: `git ls-files bounds-2026` copy to /tmp, run all 13 appendix commands of writeup/{turns,crossings}/post.mdx
   with system python3 from that bounds-2026 copy (script /tmp/ktb-run.sh).
4. Privacy scan (emails, tokens, agent ids, office URLs, /home paths) on the staged diff; commit with the Co-Authored-By
   line; `git push origin master`; check the Pages build (gh api repos/nmamano/MinCrossingsKnightsTour/pages/builds/latest).
2026-10-03 (PT 10-02 evening): pushed 10a06b8 (subtree import) + 7d66633 (sync, READMEs, .gitignore, .nojekyll). 13/13 appendix
commands PASS from a git-ls-files copy (tt16.py needs the user site-packages matplotlib). Pages build of 7d66633: built; old demo and
bounds-2026/demo/ return 200 and match the repo bytes. knights-tour-bounds: local commit bbe0a89 (README "moved" note), NOT pushed;
Nil decides archive vs keep.
2026-10-03: f177a42 pushed (bounds-2026 README title + run folder, gap/ sync, ELF auto-exclude). CR rule: sync + push after each milestone the CR names; routine gap/ sync + push without asking, at most once every ~2 h. Do not push bbe0a89.

## 2026-10-03: (1,2) defect wall for the upper bound (CR task 19n/3 -> 6n?): DOES NOT FIT
Tools in wall6n/: wallcyl.py (periodic cylinder: band of direction (a,b), fixed exterior fields, degree 2,
psi jump of PROOF_crossings_lower.md (2) forced != 0 mod 3, exact crossings per period; CP-SAT 2 workers),
chevron.py / chev_tf.py / tf.py (full board, fold field + 13 windows + free wall bands; tf.py = 2-factor relaxation
of kt.board.complete). The period vector must not be a difference of two knight moves (else edges collapse:
(2,4), (3,3), (0,4) are bad); wallcyl.py asserts this.
Calibration: (1,1) band between fold fields (2,1)|(1,2), period 6: charged OPTIMAL 2/3 per level, uncharged 0.
(1,2) band between (1,-1) zigzag fields z0|z0, period (4,8): charged OPTIMAL 1/2 per level (Edge Searcher 7.1).
(1,2) wall results (period (4,8), width 4): (2,1)|(2,1) best found 1 (bound open); (1,2)|(1,2) OPTIMAL 1;
(1,2)|(2,1) and (2,1)|(1,2) 3/4 charged or not; z0|z1 INFEASIBLE; straight|zigzag INFEASIBLE.
Full board n = 120 (chevrons BL->(n/4,n/2)->TL and BR->TR, no diagonal corridors, 2-factor + crossing objective):
about 1 per level (0.95..1.3). Without any carrier the fold field + windows has no 2-factor (charge needs a carrier).
Reason (colour balance, exact): the knight graph is bipartite, so a periodic band with equal black/white cells needs
equal black/white stubs. A (1,-1) zigzag field (black cells send +(2,1),+(1,2)) cut along direction (a,b) leaves
stubs of one colour, 3|a-b|/2 per unit (checked: vertical cut 12 per 8 rows, all one colour; straight fields 8/8).
So a zigzag region can only be bounded along (1,1) (see the lemma below; an earlier note here also named (5,1): wrong). A (1,2) wall over n/2 levels needs a zigzag region of width
~n/4 whose boundary meets sides or straight fields along other directions: impossible without a colour current of
order n. Side check: zigzag field at a vertical board side INFEASIBLE (width 4, 6); (2,1) field at a side OPTIMAL 1/row.
Possible LOWER-side use (UNCHECKED, for Edge Searcher / Turns Theory): 1/2-walls need zigzag exteriors, and zigzag
regions are (1,1)-bounded; straight-field walls cost >= 2/3 in every case measured.

### Colour-balance lemma for ribbon fields (2026-10-03; statement + proof; numbers checked by wall6n/stub_colour.py)
Setting. chi(x,y) = (-1)^(x+y). Every knight edge joins cells of opposite chi. A FIELD is an edge set on Z^2 with
degree 2 at every cell. Straight field F (F one of (2,1),(1,2),(2,-1),(1,-2)): edges p -- p+F for all p.
Zigzag field Z_v (v in {0,1}): edges p -- p+(2,1) and p -- p+(1,2) for every "valley" p with x+y = v mod 2
(then every other cell is a "peak" with edges to p-(2,1), p-(1,2); ribbons run along (1,-1)).
Cut. For coprime integers (a,b) let f(p) = a*y - b*x and H_c = {p : f(p) > c}. For a field E define
Q_E(c) = average over steps (a,b) along the line of the sum of chi(p) over edges p--q of E with p in H_c, q not.

(L1) Counting identity. For every finite cell set S and every edge set E,
    sum over edges p--q of E with p in S, q not in S, of chi(p)  =  sum over p in S of chi(p) * deg_E(p).
Proof: an edge with both ends in S contributes chi(p) + chi(q) = 0 to the right side.

(L2) Values. Q_F(c) = eps(c) for every straight field, and Q_{Z_v}(c) = (-1)^v * 3(b - a)/2 + eps(c), where
eps(c) = 0 if a + b is odd and eps(c) = (-1)^(c+1) if a and b are both odd.
Proof: an edge p -- p+d crosses the cut with p inside iff c < f(p) <= c - delta_d, delta_d = a*d_y - b*d_x.
Per step there is one lattice point on each level f = const. If a+b is odd, translation by (a,b) flips chi and maps
valleys to peaks, so averages over two steps are exact: a straight field gives 0; in Z_v the (2,1)-edges give
(-1)^v * (-(a - 2b))/2 and the (1,2)-edges give (-1)^v * (-(2a - b))/2 (valley inside when delta < 0, peak inside,
of colour -(-1)^v, when delta > 0; both cases give the same signed term -(-1)^v delta/2), total (-1)^v * 3(b-a)/2.
If a, b are odd, chi(p) = (-1)^f(p), and the same count level by level gives the extra (-1)^(c+1) for every field.
Checked numerically for 11 directions, c even and odd, all 5 field types (stub_colour.py).

(L3) Interface condition. Let a periodic band (period a multiple of (a,b)) separate field E_L on {f <= c1} from
field E_R on {f > c3}, with degree 2 at every cell. Then Z-part(E_L) = Z-part(E_R), i.e.
    3(b - a)/2 * ((-1)^{v_L} [E_L zigzag] - (-1)^{v_R} [E_R zigzag]) = 0.
Proof: apply (L1) to S = {c1 < f <= c3} per period with deg = 2: Q_L(c1) - Q_R(c3) = 2 * sum_S chi; the right side
equals the eps-difference eps(c1) - eps(c3) level by level (computed as in L2), so the Z-parts must agree.
(Q_R enters with a minus sign: the inside of S at c3 is the low side, and chi(low end) = -chi(high end).)
Consequences: zigzag | straight only along a = b, i.e. (1,1); Z_0 | Z_1 only along (1,1); Z_v | Z_v along every
direction. Finite version: a band of width w and length k steps along (a,b), a + b odd, between a zigzag field and a
straight field needs |3(b - a)/2| * k <= 2 |sum_S chi| + O(w) = O(w), so k = O(w).
Checks (wallcyl.py, CP-SAT): (1,2) z0|z0 feasible (1/2 per level charged), z0|z1 INFEASIBLE, (2,1)|z and z|(2,1)
INFEASIBLE; (1,1) (2,1)|z0, (2,1)|z1, (1,2)|z0, z0|(1,2) all FEASIBLE with 0 crossings (free interfaces);
zigzag at a vertical board side INFEASIBLE (Q = 3/2 per row, no field on the other side).

### Zigzag-zone layouts: NO-GO on paper (2026-10-03; prices from wallcyl.py, CP-SAT, W = 4 unless noted)
Prices (charged = psi jump != 0; "free" = 0 crossings):
- Crossing-free zigzag types: z_v (valleys +(2,1),+(1,2), ribbons along (1,-1)) and its mirror y_v (valleys
  +(2,-1),+(1,-2)). The type with valley moves (2,1),(-1,2) is not crossing-free (best 18 per (4,8) period uncharged).
- Interfaces: z|straight only along (1,1), free; y|straight only along (1,-1) (mirror); z0|z1 along (1,1);
  z|y only along the axes (colour: z0|y0 vertical, z0|y1 horizontal; stub_colour.py), cost 1 per unit
  (OPTIMAL at W = 4 and W = 6); z0|y1 vertical INFEASIBLE.
- Zigzag at a board side: INFEASIBLE (exact, colour lemma). So zigzag zones touch the sides only in O(1) windows
  (corner end of a zone: O(1) wide; "side end" price: infinite).
- Walls inside z|z: (1,2) charged 1/2 per level (OPTIMAL); (1,1) charged 2/3 per level (OPTIMAL, also z0|z1);
  (2,1) = (1,2) transposed (z is transpose-invariant): 1 per level in the region y > x.
Paper bound (BL corner, region y > x, level = y; same for every corner): let the wall rise with a share of
(1,2) steps. Its offset y - x grows at rate r per level (r = 1/2 for a pure (1,2) wall). The zone that holds it
cannot use the side, so its outer boundary must keep up. Against straight fields the boundary has only (1,1)
pieces (z) and (-1,1) pieces (y). Each y piece of size k needs a z|y separating path of L1 length >= 2k, at cost
>= 2k. Per level this costs >= r. Wall cost per level for a (1,2)/(1,1) mixture (a steps, b steps):
(a + 2b/3)/(2a + b), with r = a/(2a + b). Total >= (2a + 2b/3)/(2a + b) >= 2/3, with equality only for b-only
(the diagonal carrier). A wide zone that uses the diagonal as its other boundary adds a horizontal z|y top of
length ~n/4 (cost ~n/4 per wall). So no zigzag-zone layout beats 2/3 per level: 19n/3 stays. No tour built.
Cross-check (KT Edge Searcher, gap/searcher/wall/wall_if.cpp, relaxed W=4 lower bounds, 2026-10-03): (1,1) zigzag
interfaces free; vertical z|y turn 1 per row (= my wallcyl price); z0|z1 (1,2) wall NONE; its break-even argument
(zigzag ribbon ends >= 1/3 each) also gives >= 19n/3 + n/3 for the chevron layout. Its non-(1,1) zigzag|straight
prices are relaxed (colour may leak through free ghost cells); with exact colour balance they are infeasible.
2026-10-03 (Oct 3 ~9:15 am PT): 5n post update prepared, NOT pushed (CR: push only after the Verifier audits the post).
explain/progress_charts.py: 4 new crossing rows (52n/11 Oct 2 8:36 pm, 204n/43 9:21 pm, 24n/5 10:11 pm, 5n Oct 3
2:50 am PT = times of the CR's milestone messages). SVG regenerated (turns SVG unchanged), PNG re-rendered
(currentColor -> #22303a, white, Chrome device scale 2, 1440x1084). Root README.md of MinCrossingsKnightsTour edited in
the working tree only (X >= 5n - 612). Routine syncs must not stage README.md, bounds-2026/writeup, bounds-2026/explain.
knights-tour-bounds: CR pushed bbe0a89 and archived the repo (Nil approved).
Milestone plan (CR, 2026-10-03; apply only when the CR names the post-audit milestone):
- bounds-2026/README.md: 5n row already added above the 14n/3 row in the repo working tree (uncommitted).
- RESULTS.md (research dir, NOT yet edited): insert above line 14 the row
  "| X >= 5n-612 | Proved, closed tours, even n>=32 | gap/turnstheory/PROOF_5N.md; audit Claim 42 |", keep 14n/3.
- Then sync, run the 13 appendix commands + PROOF_5N.md section 7 commands from a git-ls-files copy, privacy scan,
  commit (README.md, bounds-2026/README.md, RESULTS.md, writeup/, explain/ included) and push.

## STATE FOR A FRESH SESSION (2026-10-03 ~17:30 UTC, handoff at ~55% context)
Role: KT Integrator; manager = Chief Researcher. Mission now: public repo + demo + post figures.
- Repo ~/nil/MinCrossingsKnightsTour (master, push as Nil; no branches). Last push 39e6b0e (demo = Pages landing page).
  Sync: `sh w-integrator/sync_public.sh` (excludes in the script; also writes the root index.html from demo/index.html).
- HELD until the CR names the post-audit milestone (do NOT stage/push): README.md (5n line), bounds-2026/README.md
  (5n row; its demo-link line IS pushed), bounds-2026/RESULTS.md, bounds-2026/writeup/, bounds-2026/explain/.
  Routine sync staging: git add -A -- . ':!README.md' ':!bounds-2026/README.md' ':!bounds-2026/RESULTS.md'
  ':!bounds-2026/writeup' ':!bounds-2026/explain' ; privacy scan the staged diff; commit; push; at most every ~2 h.
  At the milestone: apply the pending RESULTS.md 5n row (see "Milestone plan" above), sync, run the 13 appendix
  commands + PROOF_5N.md section 7 from a git-ls-files copy, privacy scan, commit everything, push.
- Posts: Nil edits writeup/{turns,crossings}/post.mdx himself. Edit only when the CR asks; re-read right before editing;
  report exact changed lines; check MDX (node writeup/crossings/check_mdx.mjs; turns via the same serializer) and the
  preview http://127.0.0.1:21019/blog/knights-tour-{turns,crossings} (200).
- Figures made today (scripts next to them): writeup/turns/figures/{heel21_fig,blocks_fig,heel_original_fig}.py;
  writeup/crossings/figures/lower_figs.py (text INK, lower now = 5n); explain/progress_charts.py (5n rows).
  blocks.png is made but NOT inserted (Nil decides the text).
- Demo: demo/ (office app knight-demo, restart after changes: POST /api/apps/knight-demo/restart); check with
  `node demo/check.js`; browser tests with playwright-core from a local node_modules + /usr/bin/google-chrome
  (scripts in /tmp/demotest may be gone; rewrite as needed). Pages: https://nmamano.github.io/MinCrossingsKnightsTour/
- Upper-bound wall study closed (no-go), see sections above. knights-tour-bounds archived (CR).
2026-10-03 16:10 UTC: routine sync pushed 0696598 (191 files, gap/ claims 46-48, wall, beyond5). New rule: fresh-copy audit runs
gap/verifier/claim*_run/ are excluded in sync_public.sh and ignored in bounds-2026/.gitignore (claim46_run was a 446-file repo copy).
2026-10-03 (CR): beyond-5n research wound down; final-status sync pushed 1c29f64. NEW HOLD: gap/lowerbounds/SIMPLE_STRIP* and
gap/turnstheory/PROOF_5N_SIMPLE* (simpler 5n proof drafts) stay unstaged until the CR says they are audited. Staging command now:
git add -A -- . ':!README.md' ':!bounds-2026/README.md' ':!bounds-2026/RESULTS.md' ':!bounds-2026/writeup' ':!bounds-2026/explain' ':!bounds-2026/gap/lowerbounds/SIMPLE_STRIP*' ':!bounds-2026/gap/turnstheory/PROOF_5N_SIMPLE*'
2026-10-03 18:30 UTC: routine sync HELD (nothing pushed). All new files are simple-5n work: gap/lowerbounds/simple_strip/,
gap/turnstheory/PROOF_5N_V2.md, gap/verifier/claim50_*, claim51_* (+ FINDINGS updates). Asked the CR if the hold covers them
(default: hold all). simple_strip/graph.pkl (16 MB) excluded by the script, reported to the CR.
2026-10-03 (CR answer): hold ALL simple-5n work (simple_strip/, PROOF_5N_V2.md, claim50/51, FINDINGS updates) until Claim 52
(audit of PROOF_5N_V2.md) passes; then one push. graph.pkl stays excluded (the checker regenerates it). The CR will say when.
2026-10-03 (CR): Claim 52 PASS (X >= 5n-597, tours + 2-factors). Simple-5n hold LIFTED; pushed 818711d (72 files: PROOF_5N_V2.md,
PROOF_5N_SIMPLE.md, SIMPLE_STRIP.md, simple_strip/ without graph.pkl, PROOF_5N.md pointer, claims 50-52, FINDINGS).
Post milestone (README.md, bounds-2026/README.md, RESULTS.md, writeup/, explain/) still HELD: Nil decides about 5n-597 there.
The pending RESULTS.md row in the Milestone plan says 5n-612; re-check the constant with the CR at the milestone.
2026-10-03 (CR): the TURNS post (writeup/turns/: post.mdx, images/, figures/) now belongs to the Personal Site Agent (Nil's
decision; published on nilmamano.com). Research agents never edit, stage or push it: add ':!bounds-2026/writeup/turns' to EVERY
staging command, at the milestone too. Milestone HELD set now: README.md, bounds-2026/README.md, bounds-2026/RESULTS.md,
writeup/crossings/ (Turns Theory -> 5n-597, then Verifier Claim 53), explain/ (chart). The repo copy of writeup/turns stays at
its last pushed version.
2026-10-03 (Nil via CR): the 8n turns conjecture is PROVEN (8n-28) and TIGHT (8n-14); never call it false/wrong/disproved.
Pushed 44890c5 (wording only: RESULTS.md, ktlean/README.md sources; bounds-2026/README.md repo-only, held 5n row unstaged via
hash-object + update-index). Reported to the CR, not fixed: writeup/turns/main.tex lines 36, 81 (Corollary 2), turns post.mdx (PSA), briefs (history).
2026-10-03 (CR): pushed 767b0a2: turns paper main.tex lines 36 + 81 (Corollary 2) reworded (conjecture holds, factor 8 tight),
main.pdf rebuilt (pdflatex x2, 11 pages, no errors); writeup/turns/post.mdx git rm'd (images kept). sync_public.sh now
excludes /writeup/turns/post.mdx. The paper (main.tex/pdf) stays OURS; only post.mdx + images/ are the PSA's. main.aux/.log/.out
are rebuilt but NOT pushed (CR said tex + pdf only).
2026-10-03 (CR): pushed 9f9c54b: turns paper abstract (line 33 'in its leading factor'; lines 36-37 -> one sentence), line-1 comment -> blog post URL; main.pdf + main.log rebuilt (aux/out unchanged).
2026-10-03 (CR, Claim 53 PASS on the crossings post): milestone rows PREPARED in working trees, NOT staged/pushed:
root README.md (X >= 5n-597), bounds-2026/README.md (5n-597 row: PROOF_5N_V2.md, Claims 50-52, 2-factors; plus a one-line
5n-612 "older proof" row), RESULTS.md (two table rows, new section "Crossing lower bound: 5n-597" with the 6 PROOF_5N_V2 sec 7
commands, coefficient "between 5 and 19/3"). Chart labels print "5n" only: no change. The 6 commands passed from the research
root on 2026-10-03 (cut certificate 4.1 s). This REPLACES the old Milestone plan's 5n-612 RESULTS row.
At the milestone: sync; stage everything with ':!bounds-2026/writeup/turns'; fresh-copy run of the 13 crossings/turns post
appendix commands (turns post is gone from the repo: run only the crossings ones + PROOF_5N_V2 sec 7); privacy scan; push.
2026-10-03 21:15 UTC: routine sync pushed 055e815 (Claim 53 audit). HELD with the post: gap/verifier/claim53_post_snapshot.mdx + claim53_vs46.diff (full draft of the unreviewed crossings post); asked the CR. claim46_crossings_snapshot.mdx was already pushed in 0696598.
2026-10-03 (CR): pushed cafc5cd: claim46_crossings_snapshot.mdx untracked (git rm --cached; research file kept). Held post snapshots now: claim46_crossings_snapshot.mdx, claim53_post_snapshot.mdx, claim53_vs46.diff - add ':!bounds-2026/gap/verifier/claim46_crossings_snapshot.mdx' to routine staging; release all three at the milestone. Other tracked post copies (gap/turnstheory/post_before_5n.mdx, claim26_sources/..post.mdx = public post; claim21_clean = older) are fine.

## 2026-10-04: all-n pipeline for the turns mission (close 8n-28 <= T_min <= 8n-14)
Role (CR): any improved corner set -> verified tours for every even n = 48..110 + period-in-n + all-size certificate.
- w-integrator/allpipe.py (needs .venv/bin/python, CP-SAT). Input: Edge Searcher csolve.py --mode tour --out JSONs
  (n, tour, A, B, combo path or inline bottom/left/top/right/phases; gadget names from menu_turns.json allowed;
  optional explicit "region" per corner, i/j = distance from the vertical/horizontal side). Or --combo F --A --B
  with no base (solves every class from the skeleton). Cells outside the region that differ from the skeleton are
  added to the shape. Finds the outside-matching period p and n_s; per class mod p: base content, else CP-SAT
  (corners whose band surroundings are unchanged are copied from the nearest base; --time, --workers 2,
  --pure-turns). Transplants to every even n in [nmin, nmax]; direct solve where the transplant fails.
  Output w-integrator/pipeline/<tag>/: res<r>.json (anchored-v2 zones: "<corner>:dx,dy" from anchors BL (0,0),
  BR (n,0), TL (0,n), TR (n,n)), tours/<tag>_n<n>.json, SUMMARY.md, run.log.
  Usage: .venv/bin/python w-integrator/allpipe.py --tag NAME base_n56.json base_n58.json ... [--nmax 110]
- w-integrator/allsize_check.py (python3, standard library): the audited TT16 proof logic of
  w-turnstheory/check_upper_proofs.py, generalised (any depths, periods, shapes; line period w = lcm(PB, PT, 2QL,
  2QR), step s = lcm(p, w), base N in [96, 96+s) per class mod s, one cut slab per diagonal gap >= 6 lines from the
  zones: M^(1+s/w) = M, n -> n+s equivalence, long slab; T(N+s) - T(N) = band turns). Direct checks of every n in
  [48, N+s]. Usage: python3 w-integrator/allsize_check.py w-integrator/pipeline/NAME
- Self-tests 2026-10-04 (pipeline/selftest_*): TT16 bases -> 8n-14 all even n >= 48, PASS (transplant works down
  to n = 48; seconds). L-shape 10x6+6x10 from 1 base -> 8n-13 (3 classes solved, 120 s each), PASS. Combo
  l_d5lowm20/l_free, 8x8, no base -> 8n-13 (~8 min), PASS. Untested: band periods 16 (s > p).
2026-10-03T23:39Z: routine sync pushed a66eac2. New excludes (script + bounds-2026/.gitignore): gap/verifier/claim*_clean/ (claim54_clean = ktlean audit build copy), w-integrator/pipeline/selftest_[!T]*/. New over-5MB exclusion reported: gap/lowerbounds/turns_ring/fstrip_1_-2.pkl (6.5 MB).
2026-10-04 (CR): pushed 7e46a77: Lean 8n-28 (Claim 54) in main.tex (line 91, sec:lean, audit status; pdf rebuilt), README.md + RESULTS.md 8n-28 rows (hunks only; held 5n rows stay unstaged).
2026-10-04: routine sync pushed 02fe48e. New over-5MB exclusion: gap/lowerbounds/turns_ring/strip_W4.pkl (42 MB).
Claim 55 (Verifier): allsize_check FAIL as a general checker (fallback tour size not checked; geometric preconditions
not enforced); the 3 self-test families PASS under extra checks. FIXED the same day: fallback needs td n == n, n x n
rows, legal codes, exact board vertex set (validate(g, n)); templates rectangular + legal; corner_radius(): inward
coords >= 0, shapes cover band-overlap rectangles, R; base N >= max(96, 2R+6); w >= 5; cuts also clear the 4
band-overlap spans; PASS only if dT == 8s (integer), else exit 1; refuses python -O. allpipe labels its period
EMPIRICAL and SUMMARY as candidate data. Regression: python3 w-integrator/allsize_regress.py (Claim 55 adversarial
cases + bad overlap + genuine fallback + period-16; 9/9 OK). SHA-256: allsize_check.py 2a792b3a..., allpipe.py a147c022...
2026-10-04 (CR: Claim 55b prep): mixed interiors (move pairs 15/37, period 5; TMIN.md) and side gadgets that change
along a side (gap/searcher/turns/mixed.py) are NOT supported, and both tools reject them cleanly: allpipe exits REJECT if
a base differs from the skeleton at corner distance >= --max-corner (16) and names the moves; allsize_check rejects a
residue file with "interior" other than x+2y. Regression 10/10 OK (adds bad_interior). Hashes:
dcd96d11caef7b818df0688590dd11d5f0cf4cddcab9f5ad434a88e0cca24c44 w-integrator/allsize_check.py
bc5ae0a06ca13c129ee624603884c460caac4ca58a9a7ff22f4c58f168ebfdfd w-integrator/allpipe.py
a86d08dcd60ac716d0cf04de1d1cb8a2b2f1bebb3458c271faf51af2d57b8708 w-integrator/allsize_regress.py

## 2026-10-04: all-size checks of the Edge Searcher's tours below 8n - 14 (PENDING AUDIT, checker changed after Claim 55b)
Inputs: gap/searcher/turns/tours/res6/n{62,70}.json, res2/n{66,74}.json (only n + tour). New allpipe options:
--extract Db,Dl,P,Q (read the 4 periodic bands from the tour; the skeleton then matched every cell outside the 8x8
corners), --A/--B defaults, --period, --residues. allsize_check: --partial (residue subset; the PASS line names the classes).
Outside matching has period 16 in n (not 8) (why: UNCHECKED; M^2 = M was not tested); checker step s = 16, M^3 = M.
- pipeline/ES_res6 (period 16, residues 6, 14): PASS T(n) <= 8n - 16 for every even n >= 48, n = 6 mod 8
  (direct checks n = 54..126; bases N = 102, 110; dT = 128 = 8s; R = 8).
- pipeline/ES_res2 (period 16, residues 2, 10): PASS T(n) <= 8n - 17 for every even n >= 48, n = 2 mod 8
  (direct checks n = 50..122; bases N = 98, 106).
Commands: .venv/bin/python w-integrator/allpipe.py --tag ES_res6 gap/searcher/turns/tours/res6/n62.json
  gap/searcher/turns/tours/res6/n70.json --extract 4,4,8,4 --A 8 --B 8 --period 16 --residues 6,14 --nmax 126
  python3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res6 --partial   (same for res2 with residues 2,10)
Hashes after these changes:
f3925853ab20f57416678ee81aa2b4322c7e5074fe4065ff3ef29730353bc5d6 w-integrator/allsize_check.py
2dfc8f14657e04ef2315d3cafa609d691ae59d7223675a00466a5c7f644316d8 w-integrator/allpipe.py
a86d08dcd60ac716d0cf04de1d1cb8a2b2f1bebb3458c271faf51af2d57b8708 w-integrator/allsize_regress.py

## 2026-10-04: DESIGN - all-n argument for a MIXED interior (not built; for CR review)
Geometry (checked on gap/structures/tmin/r18_tour_D4.json, r32_2f_D4.json): interior cells are straight in direction
A = (2,1) [pair 15] or B = (1,-2) [pair 37]; the class is q = (x - 2y) mod 5 (equivalently (2x + y) mod 5); a set
S_A of classes uses A, the rest B (r18: 4 A + 1 B; r32: 1 A + 4 B). lam_A = x - 2y is constant on A chords,
lam_B = 2x + y on B chords. The field is invariant under the lattice L = <(2,1),(1,-2)> (index 5, contains 5Z^2).
Chord families by lam order of the corners: A: TL(-2n) < TR(-n) < BL(0) < BR(n) -> gaps L-T, L-R, B-R;
B: BL(0) < TL(n) < BR(2n) < TR(3n) -> gaps B-L, T-B, T-R. Each gap grows by s in lam when n grows by s.
Reduced graph: tour = ring (depth-D bands + corners) + chords (each chord = one edge between two ring ports).
Turns are only in the ring, so T(n0 + ks) = T(n0) + k*dT is exact by local counting once the ring is periodic
(no connectivity needed). That part transfers from allsize_check unchanged.

NEGATIVE RESULT (why the TT16 proof does not transfer). TT16 inserts whole chords (slabs parallel to the chords);
nothing crosses a slab, so the rest of the graph is unchanged and M^(1+s/w) = M is a finite check. With two chord
families, an A-slab is crossed by O(n) B chords. Keeping those B chords straight forces the translation across the
A-slab to be along B (t = (w/5)(1,-2)), which is not a square-board growth. With the square growth (corners move by
(s,0), (0,s), (s,s)), the three A-slab insertions do grow every side by s (as in TT16), but in that identification of
ring ports the B pairing is re-wired: B chords between an A-insertion point and the B-insertion point on the same side
shift by s/2 to 2s ports. That is a global change of O(n) chords. So connectivity is NOT preserved by a local check,
and the cycle count can depend on n arithmetically (rotation-like, e.g. gcd(an + b, K)); Structures' r32 2-factor
(6 cycles) shows the mixed field does not connect by itself. Two cut families or a cross insertion do not fix this:
any region closed under both chord directions is the whole board.

PROPOSED PROOF (build only after CR agreement): exact parametric connectivity.
 1. Port model: contract every ring-local path; each ring port then has one ring partner (R, bounded offset,
    periodic along each side, fixed near corners) and one chord partner (C, affine in position with constants
    affine in n). Cycles of the tour = orbits of phi = C o R on ports.
 2. Parametric tracing: for n = n0 + k*S, ports form finitely many families (side, residue mod band period) with
    index ranges [lo(k), hi(k)), lo/hi affine in k. phi is piecewise affine on these families. Trace pieces
    symbolically; when a return map on a piece is a translation by a constant t, accelerate (number of rounds =
    floor division, which splits k by residue mod t). Output: the number of cycles as a function of k on each
    residue class of k, for all k >= k0, plus direct checks for the n below n0 + k0*S.
 3. Certificate checker (standard library): replays the symbolic trace step by step (each step = an exact identity
    between affine maps on integer intervals), so the Verifier audits a finite list of exact steps.
 Expected outcome: the mixed family is a single tour only on some classes of n mod K (K from the gcd structure);
 the tool reports these classes exactly. Effort: data generator 1-2 h; parametric engine + checker 4-8 h; risk:
 the trace may need many splits if the band patterns are irregular.
Preconditions the checker will enforce: interior = mixed field exactly (S_A given, every interior cell straight);
four periodic bands, depth D, periods P (bottom/top), Q (left/right); growth step S = multiple of lcm(5, P, Q)
(and of 2Q for the line period); corner zones within radius R with N0 >= 2R + 6; no closed ring cycles; every
chord ends in a band port (no chord ends inside a corner zone beyond the fixed corner data).
Data generator first (cheap, no proof): cross insertion (S columns at the board centre and S rows), fill with the
periodic bands and field, validate each n directly up to n ~ 300, and print cycle counts per n. This shows K fast.
Input format (proposed to Edge Searcher 2026-10-04, not yet confirmed): a JSON with n and tour (board.js grid);
optional S_A, D, P, Q; I extract bands and the class rule from the tour, as with --extract.
2026-10-04: data generator built (CR agreed): w-integrator/mixgen.py (stdlib, not a proof). Cross insertion of S columns at
x = X and S rows at y = Y (k times), valid when the base is S-periodic across both seams; every board checked directly;
prints T - 8n and cycle count per n, writes single-cycle tours with --out. Tests: TT16 n56, S = 8 -> one cycle,
8n - 14 for n = 56..136. ES res6 n62, S = 8 at the centre -> one cycle, 8n - 16 for n = 62..158 (centre insertion has
period 8; the corner-anchored transplant in allpipe needs 16; both valid). Structures' mixed boards: NOT growable:
r18 (n = 18 < room for S = 10) and r32 2-factor (interior exactly 5-periodic, 0 mismatches; ring breaks period 10 at
4 cells on the vertical seam, 5 on the horizontal). So no K yet. Requirement for mixed inputs: S = common period
across the seams = multiple of lcm(5, 2, P_bottom/top, Q_left/right); bands of period 2, 5 or 10 give S = 10.
2026-10-04 (Nil via PSA/CR): pushed 3b06214: bounds-2026/TURNS_PROOFS.md (source: research-root TURNS_PROOFS.md, made from
writeup/turns/appendix_from_post_2026-10-04.mdx; parts A-F as ## headings; only text change: removed "Click a part to open
it."; text word diff in w-integrator/turns_proofs_worddiff.txt). README.md + RESULTS.md link to parts B, C, D-F (hunks only;
held 5n rows unstaged). 5 check commands PASS from a git-ls-files copy (Lean not rebuilt). GitHub anchors verified.
2026-10-04 (CR): Claims 55b + 56 PASS (8n-17 for n = 2 mod 8, 8n-16 for n = 6 mod 8; single straight field only).
PREPARED, HELD until the CR relays Nil's go: TURNS_IMPROVED.md (research root; construction, bands, checks, audits),
RESULTS.md (table row, new section, "not proved" constants), bounds-2026/README.md (row + map line), root README.md
(Turns line). Release = sync_public.sh, then `python3 w-integrator/release_turns_improved.py` (stages only these hunks +
TURNS_IMPROVED.md from HEAD; dry run OK, no 5n rows), privacy scan, commit, push. Routine syncs: add
':!bounds-2026/TURNS_IMPROVED.md' to the staging exclusions. Routine sync cda5b0f pushed the ES_res2/ES_res6 certificate
folders, Claim 55b/56 reports and gap/verifier/claim56_alln (audit evidence, 5 MB, kept on purpose).
2026-10-04 (Nil via CR): demo step TI (turns step 5, "Periodic bands, 8x8 corners", 8n - 17 / 8n - 16) built LOCALLY, HELD
with the improved-turns release. demo/build_data.py gen_TI (allsize_check.graph on pipeline/ES_res2|ES_res6/res<n%16>.json,
n = 2 mod 4 only, 50..198): 38 tours valid, T - 8n = -17 (n = 2 mod 8) / -16 (n = 6 mod 8) at every n, brute crossings agree
at n = 98, 102; node demo/check.js: 683 files, 0 problems. app.js: dataKey() shows TT16 with a note for n = 0 mod 4; chart
labels use the last n with data. Browser test (playwright, n = 50, 54, 58, 62, 56, 60, 98, 102, 198): counts = 8n - 17 /
8n - 16, fallback note at 56 and 60, no page errors. Preview: the knight-demo office app, ?metric=turns&step=5&n=58
release_turns_improved.py now also stages bounds-2026/demo (dry run: 46 files, no 5n rows). Routine syncs exclude bounds-2026/demo.
2026-10-04 (Nil's go via PSA/CR): pushed 856a7f3 = TURNS_IMPROVED.md + RESULTS/README rows (demo NOT included; 5n rows still
held). Live URL 200: github.com/nmamano/MinCrossingsKnightsTour/blob/master/bounds-2026/TURNS_IMPROVED.md. Demo step TI still
HELD until Nil approves the preview; then: sync, git add -A bounds-2026/demo, privacy scan, commit, push, check the Pages
build and ?metric=turns on the public demo. New over-5MB exclusion: gap/lowerbounds/turns_ring/fstrip_1_2.pkl.
Never write office URLs into synced notes (sync_public.sh fails on them).
2026-10-04 (Nil approved preview): pushed f64e38c = demo turns step 5 (TI). Pages build of f64e38c: built. Real Chrome on the public site: ?metric=turns opens step 5 (n = 50, 8n - 17); &step=5&n=58 -> 447 = 8n - 17; &n=62 -> 480 = 8n - 16; &n=56 -> TT16 434 = 8n - 14 with the note; no page errors. Improved-turns hold is fully released; only the 5n crossings milestone remains held.
2026-10-04 (Nil via CR): pushed 1a7d396: demo Download image = crop to the board (whole-board view) + white margin max(24 px, 4.5% of the longer side) on all sides (downloadCanvas() in demo/app.js). Live check in Chrome (Pages build 1a7d396): TI n=50 1578 px, margins 67 px all sides; FOLD n=200 1624 px, 68 px; edge view and any-board 30x20 also margined; no page errors. Sample: w-integrator/demo_download_sample.png.
2026-10-04 (CR: crossings post handed to the Personal Site Agent; milestone GO except the post):
- 944df86: 5n - 597 rows in README.md, bounds-2026/README.md, RESULTS.md + chart (explain/) + writeup/crossings/figures
  (lb figures at 5n, progress PNG, heel_original.png). PROOF_5N_V2 sec 7: 6/6 PASS from a git-ls-files copy.
- 7c23b9d: bounds-2026/CROSSINGS_PROOFS.md (research-root source, from post.mdx appendices A, B; text unchanged, word diff in
  w-integrator/crossings_proofs_worddiff.txt; 4 repo links made relative); git rm writeup/crossings/post.mdx; sync_public.sh
  excludes /writeup/crossings/post.mdx. 8/8 listed checks PASS from a git-ls-files copy. Anchors tested (GitHub HTML).
- Still HELD until the CR says the post is live: gap/verifier/claim46_crossings_snapshot.mdx, claim53_post_snapshot.mdx,
  claim53_vs46.diff. Only these + writeup/turns stay out of routine syncs now.

## STATE FOR A FRESH SESSION (2026-10-04 ~05:20 UTC, handoff at ~52% context)
Role: KT Integrator; manager = Chief Researcher. Repo ~/nil/MinCrossingsKnightsTour (master, push as Nil).
Last pushes 2026-10-04: 856a7f3 TURNS_IMPROVED + rows; f64e38c demo turns step 5 (TI); 1a7d396 demo Download margins;
944df86 5n-597 rows + chart; 7c23b9d CROSSINGS_PROOFS.md + git rm crossings post.mdx; 596ea3f routine sync.
- HELD until the CR says the crossings post is live on nilmamano.com: gap/verifier/claim46_crossings_snapshot.mdx,
  claim53_post_snapshot.mdx, claim53_vs46.diff, writeup/crossings/CHANGES_5N597.md (change list of the post).
- Never stage writeup/turns (PSA's post; our paper main.tex/pdf only on request). Both post.mdx files are excluded in
  sync_public.sh. Never write office URLs into synced notes (the sync fails on them).
- Routine sync every ~2 h (self-reminder carries the staging command).
- Turns mission tools (all audited where noted): allpipe.py / allsize_check.py / allsize_regress.py (Claims 55b, 56 PASS;
  single straight field only), pipeline/ES_res2, ES_res6 (8n-17 / 8n-16, public). mixgen.py = cross-insertion data
  generator for mixed interiors (not a proof); waits for an Edge Searcher mixed tour with periodic bands (S = multiple of
  lcm(5, 2, band periods)). Mixed-field all-n design: section "DESIGN - all-n argument for a MIXED interior"; the parametric
  engine is built only if mixgen shows a usable K (CR agreed).
- Demo: demo/ (office app knight-demo; restart after changes); browser tests: /tmp/demotest/*.js style (playwright-core from
  a local node_modules + /usr/bin/google-chrome); build_data.py has gen_TI.
