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
Role: KT Integrator (Research Lab), manager = Chief Researcher (agent-1790895858902-etft). Rules: CP-SAT
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
