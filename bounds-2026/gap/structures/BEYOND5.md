# BEYOND5: paying the connectivity cost on capacity that route (i) does not use

KT Structures, 2026-10-03. DESIGN for the Chief Researcher (statement + plausibility + data). Nothing below is
proved unless marked. Scripts: `beyond5_ledger.py` (log `beyond5_ledger.log`), `chamber_ledger.py`, `g2_check.py`.

## 1. Currency and what route (i) spends

Route (i) (PROOF_5N_PLAN.md sections 1-5, Lower Bounds FINDINGS F) uses the exact identity
    E = X - 4n + 2 = nu + T/2,   nu = X_out/2 + E/2 (2E = G + X1 + W3),   T = |S*| - 4n + 2,
and pays each of the N = 2n - 60 corner candidates 1/2:
  - a retained candidate takes f0 = min(2, s_i)/4 from nu (s_i = payable quarters in its squares);
  - a lost or deficient candidate takes 1/2 from T, through F1-V: T + C >= #(strong rows) >= D_loss + L_def.
Route (i) OWNS exactly: (a) at most two quarter atoms per retained candidate, (b) the T capacity of at most one
strong row per lost / deficient candidate. Everything else in E is free for a second price.
Choose (a) deep-first (depth >= 5 from every side): a tile that covers a quarter of a depth-5 square has both ends
at depth >= 4, so these atoms never meet the collar columns 0..2.

## 2. The target

    (B5)  E >= N/2 + (1/2) (G_free + N_free) + (1/4) BQx - C,
    (C5)  2 (G_free + N_free) + BQx >= c n - C'      for every closed tour, some c > 0.
Together: E >= n + (c/4) n - C'', i.e. X >= (5 + c/4) n - O(1).
Definitions (all per side, local frame, rows 8..n-9 as in LB tour_scan.py):
  - g(r): the F1-V strong row test (up or down). G_free = #(g rows) - #(rows owned by route (i) under (b)).
  - N_free: changed ports (nre_scan.py definition: collar partner is not the P / P' partner; non-steep ports are
    changed) whose row is at distance > d0 from every g row. d0 is a parameter the strip certificate fixes
    (B5 cycle 4 says d0 >= 1 is needed: a collar defect changes ports in neighbour rows that pass the test).
  - BQx: bad quarters at depth >= 5 minus the deep quarters route (i) takes under (a).
(B5) splits into two disjoint payments:
  (B5-strip) width-three strip lemma, per half side: X3_sigma - rows >= #g + N_free/2 - C, where X3 counts crossing
    pairs of edges that both have an end in collar columns 0..2 (LB XW=3). It contains F1-V (N_free = 0), and the
    extra N_free/2 is exactly the U-collar price LB found outside S* (1/2 per changed end, 2 crossings per row).
  (B5-deep) BQx/4 is paid by the hole / W3 / pair atoms of those quarters (Section 2 of PROOF_5N_PLAN, the same
    quarter-payment lemma); they are disjoint from (a) by definition and from X3 by depth.
Open in (B5): route (i) also spends shallow atoms on 'shallow users' (retained candidates with fewer than two deep
payable quarters); (B5-strip) must hold with those atoms removed. On the FOLD family there are none (table).

## 3. Why (C5) is the connectivity statement

(C5) is SHEET (T*') BQ + G2/2 + 2 N_re >= 4n with two changes: the side defects are counted by the strong test g
(this is where (R2) frustrated rows and bad boundary squares go), and interior bad quarters count only beyond the
flux payment (BQx). The SHEET chamber ledger (section 13) is the proof plan for (C5): every side row in a chamber is
paid by an inside return, and a return is trapped unless it has a changed end (N), or it is freed by bad quarters
(U_in), or by a current-carrying collar stretch. The two finite prices needed, in E units (1/2 per freed return):
  - (K) [interior carriers] an odd-current carrier pays >= 4 bad quarters per '/' ribbon it crosses. For (C5) it must
    hold in BQx, i.e. with the flux paths' two quarters per path removed. NEEDED. Status: SHEET 13.4, tight
    horizontally (4.000 OPTIMAL at p=6 w=2), parallel >= 2.000 at w=5; joint (BQx) form untested.
  - (K-collar) [collar carriers] a collar stretch carrying odd current pays 1 per row in E. In crossings this is
    the known edge rate (flux 3 along the edge: 2 per row, LB F12, exact W <= 4), so the content left is OWNERSHIP:
    those rows must be g rows not owned by route (i), or carry 2 far changed ports. NEEDED, but in this form it is
    part of (B5-strip).
Risk (from w-structures S3 / layout G): a gentle seam carries flux AND absorbs side ribbons at no extra cost. If a
closed tour can untrap or absorb with the same defects that pay the corner flux, (C5) fails with BQx and only a
weaker joint statement survives. All 13 tours keep (C5) with a large margin, but none of them is designed to share.

## 4. Data (CHECK, 2026-10-03, `beyond5_ledger.log`; all retained candidates paid, r <= 32 included)

route(i) = f0 + (D_loss + L_def)/2 (= N/2 up to deficiency); E_left = E - route(i); T_left = T - D_loss - L_def.
| tour | n | E | route(i) | N_re/2 | E_left - N_re/2 | T_left | nu - f0 | shallow users | BQx | (2 N_re + BQx)/n |
|---|---|---|---|---|---|---|---|---|---|---|
| FOLD | 96 | 338 | 66 | 97 | 175 | 152 | 196 | 0 | 292 | 7.08 |
| FOLD | 144 | 450 | 114 | 145 | 191 | 200 | 236 | - | - | - |
| FOLD | 192 | 562 | 162 | 193 | 207 | 248 | 276 | 0 | 420 | 6.21 |
| FOLD | 240 | 674 | 210 | 241 | 223 | 296 | 316 | - | - | - |
| FOLD | 288 | 786 | 258 | 289 | 239 | 344 | 356 | 0 | 548 | 5.92 |
| FIELD | 166 | 578 | 136 | 188 | 254 | 244 | 320 | 3 | 420 | 7.06 |
| FOLDB1 | 144 | 471 | 114 | 154 | 203 | 225 | 244.5 | 0 | 304 | 6.39 |
| FOLDP | 96 | 341 | 66 | 96 | 179 | 153 | 198.5 | 0 | 271 | 6.82 |
| FOLDX | 100 | 358 | 70 | 104 | 184 | 160 | 208 | 0 | 268 | 6.84 |
| FJOG | 130 | 1045 | 100 | 74 | 871 | 149 | 870.5 | 0 | 1845 | 16.47 |
| FJOG | 132 | 699 | 102 | 43 | 554 | 98 | 548 | 0 | 1336 | 11.42 |
| LF4 | 96 | 325 | 66 | 181 | 78 | 232 | 143 | 103 (all) | 0 | 7.54 |
| TT16 | 72 | 396 | 42 | 132 | 222 | 350 | 179 | 41 (all) | 0 | 7.33 |
Readings.
  1. On the FOLD family route (i) is paid entirely by deep quarters (f0 = N/2 - 3.5, D_loss = 7, no shallow users),
     and N_re/2 = n + 1 sits in T_left = n + 56: the arch flips are S* excess that route (i) never touches. E =
     route(i) + N_re/2 + (n/3 + 143): the n/3 is the flux surplus (BQ/4 = 4n/3 against the n route (i) needs).
  2. E - route(i) - N_re/2 >= 78 on all 13 tours (least: LF4). So (B5) with N_re in place of N_free already holds
     on the data with a margin; the d0 and ownership refinements are for the proof, not forced by the data.
  3. LF4 and TT16 are the opposite regime: every retained candidate is a shallow user (its payable quarters are in
     the collar end zones), BQx = 0, and the changed ports are the non-steep ports of the frustrated V sides, where
     (LB B5) S* excess = #g exactly. There the second price must be G_free (g rows that route (i) does not own:
     T_left = 232 and 350), not N_free. This is why (B5) carries G_free.
  4. The proxy (2 N_re + BQx)/n is >= 5.9 on every tour (needed: any c > 0). It is NOT (C5) as defined (Claim 44D);
     R-b gives the real counts. The tours do not test the sharing risk of Section 3.

## 5. Requests (exact definitions for KT Lower Bounds)

R-a (B5-strip, highest value). Width-three strip graph as in joint_stab.py (XW=3; columns 0..2 collar, degree 2;
  ghost columns 3, 4), with the F1-V strong test g. Certify the largest c with
      X3 - rows >= #g + c * #(changed ports in rows at distance > d0 from every g row) - C
  for d0 = 1, 2, 3 (changed = NLOC, the local over-count, which equals N_re on all tours). Target c = 1/2.
  If c = 0 again, return the zero-slack cycle: it is a candidate counterexample to (B5) and I will build it into
  a closed tour.
R-b (on tours, cheap). With tour_scan.py: per side, #g, #g rows owned by route (i) (strong end rows of lost and
  deficient candidates), N_free for d0 = 1, 2, 3. This turns the table's N_re/2 column into (G_free + N_free)/2.
R-c ((K), local form). Window model: a '/'-H field with one '/' ribbon crossing a cut that carries relative colour
  current +-3 (seam_flux.cur_terms convention). Minimise bad quarters in the window. Need >= 4 per ribbon crossed.
  The banded versions (SHEET 13.4, carrier21.py) give 4.000 horizontally at small sizes; the local form would
  cover all widths. Second step (joint form): the same with route (i)'s two quarters per crossing corner path
  removed.

## 6. Repair after Verifier Claim 44 (2026-10-03)

**44C accepted: the factor of two.** With S3 = width-three crossing union, T3 = |S3| - 4n + 2, the exact ledger is
E = nu3 + T3/2, nu3 = (X - |S3|)/2 + (G + X1 + W3)/4. A strip excess unit is worth 1/2 in E, so the pure-crossing
strip lemma of R-a with coefficient c on N_free gives only (c/2) N_free in E. The U collar caps the pure-crossing
coefficient at c = 1/2 (one extra crossing per row, two changed ports per row), so the pure-crossing route can
only give N_free/4, never N_free/2.
**Where the other half is.** Each collar crossing also has its quarter atoms (holes, one-quarter overlaps, W3) in the
(G + X1 + W3)/4 part of nu3. They lie in squares at depth <= 4, so they are disjoint from the deep quarters that
route (i) takes deep-first and from BQx (depth >= 5); only shallow users can consume them (44B). The repaired strip
lemma therefore uses the joint currency:
    (B5-strip')  per half side:  (X3 - rows) + Q3/2 >= #g + c * N_free - C,
    Q3 = quarter-atom units (G, X1, W3) in the strip squares at depth <= 4, minus the actual consumption by
         route (i)'s shallow users (their min(2, s_i) selected shallow quarter requests, 44A units).
Then E >= f0 + BQx/4 + (T3 + Q3/2)/2 - O(1) >= N/2 + G_free/2 + (c/2) N_free + BQx/4 - O(1).
  - c = 1 restores (B5) as written (N_free/2). The U collar allows c = 1 only if its quarter atoms give Q3/2 >= 1 per
    row (two quarter units per extra crossing, the global average of 2E = G + X1 + W3); that is the first thing
    to measure.
  - Fallback, no Q3: pure-crossing c = 1/2 gives (B5'') E >= N/2 + G_free/2 + N_free/4 + BQx/4 - O(1), and with (C5)
    X >= (5 + c_5/8) n - O(1) (Verifier's salvage: 2G_free + N_free + BQx >= (2G_free + 2N_free + BQx)/2).
So the corrected target is: c = 1 in (B5-strip') for X >= (5 + c_5/4) n; c = 1/2 in the pure-crossing lemma as the
floor, X >= (5 + c_5/8) n. Both still need (C5) (GAP) and the shallow-user subtraction (44B, GAP).
**44D accepted.** The table's last column is a proxy (N_re for N_free, no G_free); it is not evidence for (C5) as
defined. R-b (g rows, owned rows, N_free(d0) per tour) is the real check, and the 'ratio >= 5.9' sentence in
section 4 stands only for the proxy.
**R-a, changed target (for KT Lower Bounds).** Certify the largest c in (B5-strip') with Q3 counted per row from
the tile quarters of the strip squares (depth <= 4; holes 1 unit, X1 1 unit, W3 binomial(m-1, 2) units), for
d0 = 1, 2, 3; target c = 1. Also report c for the pure-crossing form (Q3 dropped), where the target is 1/2.
Ignore the shallow-user subtraction in the first run (it is zero on the FOLD family) and say whether the critical
cycle uses quarters that a shallow user could select.

## 7. Lower Bounds R-a / R-b results and what they give (2026-10-03)

LB B5b (gap/lowerbounds/FINDINGS.md, beyond5/joint_free.py, r_b.py; one implementation, rebuild pending):
pure-crossing strip lemma X3 - rows >= #g + c N_free(d0) - C per half side: c* = 1/2 EXACTLY at d0 = 2 (both
orientations, C = 9.7 per half side; U collar is the tight case), c* = 0 at d0 = 1 (5-row P'-collar-with-defects
cycle). So the FLOOR form of section 6 is certified, with d0 = 2:
    (B5'')  E >= N/2 + G_free/2 + N_free/4 + BQx/4 - O(1)
modulo the 44B shallow-user subtraction (still GAP; zero on the FOLD family) and the independent rebuild.
The joint Q3 form (target c = 1, giving N_free/2) is the next request.
R-b gives the real (C5) counts (d0 = 2; BQx from beyond5_ledger.log). b'' = right side of (B5'') without O(1);
b' = the same with N_free/2 (the c = 1 target).
| tour | n | E | G_free | N_free(2) | BQx | (2(G_free+N_free)+BQx)/n | b'' | b' | (b'' - route(i))/n |
|---|---|---|---|---|---|---|---|---|---|
| FOLD | 96 | 338 | 12 | 102 | 292 | 5.42 | 170.5 | 196.0 | 1.089 |
| FOLD | 144 | 450 | 12 | 198 | 356 | 5.39 | 258.5 | 308.0 | 1.003 |
| FOLD | 192 | 562 | 12 | 294 | 420 | 5.38 | 346.5 | 420.0 | 0.961 |
| FOLD | 240 | 674 | 12 | 390 | 484 | 5.37 | 434.5 | 532.0 | 0.935 |
| FOLD | 288 | 786 | 12 | 486 | 548 | 5.36 | 522.5 | 644.0 | 0.918 |
| FIELD | 166 | 578 | 25 | 244 | 420 | 5.77 | 314.5 | 375.5 | 1.075 |
| FOLDB1 | 144 | 471 | 14 | 201 | 304 | 5.10 | 247.2 | 297.5 | 0.925 |
| FOLDP | 96 | 341 | 11 | 97 | 271 | 5.07 | 163.5 | 187.8 | 1.016 |
| FOLDX | 100 | 358 | 18 | 107 | 268 | 5.18 | 172.8 | 199.5 | 1.028 |
| FJOG | 130 | 1045 | 47 | 3 | 1845 | 14.96 | 585.5 | 586.2 | 3.735 |
| FJOG | 132 | 699 | 22 | 5 | 1336 | 10.53 | 448.2 | 449.5 | 2.623 |
| LF4 | 96 | 325 | 89 | 161 | 0 | 5.21 | 150.8 | 191.0 | 0.883 |
| TT16 | 72 | 396 | 55 | 112 | 0 | 4.64 | 97.5 | 125.5 | 0.771 |
Readings. (1) b'' <= b' <= E on every tour (consistency of the two ledgers). (2) The real (C5) ratio is >= 4.64 on
all 13 tours; on FOLD it tends to 4 + 4/3 (N_free = 2n - 90: the arch flips; BQx = 4n/3 + 164: the flux surplus).
(3) So the natural sharp form is
    (C5-4)  2 (G_free + N_free) + BQx >= 4n - O(1),
the (T*) count of SHEET 11.3 with route (i)'s own rows and quarters removed. With (B5'') it would give
X >= 5.5 n - O(1); with the c = 1 strip form, X >= 6 n - O(1) (still below the 19n/3 tours). These are the two
conditional targets. (C5-4) is the connectivity lemma; it is unproved, and its risk is the joint use of flux defects
for absorption (section 3; Claim 44 replay).

## 8. (C5-4): exact statement and proof plan (2026-10-03; STATEMENT for red team, plan is ARGUMENT)

**(C5-4).** There are constants C, n0 such that every closed knight's tour of the n x n board, n even >= n0, has
    2 (G_free + N_free) + BQx >= 4n - C,
with, all four sides in the local side frame, side rows r = 8..n-9 (LB tour_scan.py convention):
  - g(r) = 1 iff the F1-V strong row test fails at r in the up or the down orientation (LB FINDINGS F, Claim V);
  - owned rows: for each lost or deficient candidate of route (i) (r > 32 or not), the end row that Claim V gives it
    a g = 1 (one per candidate, fixed tie rule: the vertical side first); G_free = #(g rows) - #(owned rows);
  - N_free = changed ports (nre_scan.py: collar partner is not the P / P' partner; non-steep ports are changed;
    corner ports excluded) whose collar row is at distance > 2 from every g row of its side;
  - BQx = #(bad quarters in squares at depth >= 5 from every side) - sum over retained candidates of
    min(2, #deep payable quarters on its path), with the deep-first selection of beyond5_ledger.py.
Measured (section 7): the left side / 4n is >= 1.16 on all 13 tours (TT16 4.64 / 4); FOLD tends to 4n + 4n/3.
Consequences: with (B5'') X >= 5.5 n - O(1); with the c = 1 joint strip form, X >= 6 n - O(1).

**8.1 Units.** Every side row demands 1. A free g row supplies 2, a far changed port 2, a free deep bad quarter 1.
The plan pays every row of the run-end identity 4(n - 7) = bdry_bad + 2T + W' + D' (SHEET 9.1), split into
chamber rows and the rest (SHEET 13).

**8.2 Steps.**
  S1 [PROOF, SHEET 9.1, 13.1] Row partition: maximal chambers (disjoint side segments sigma, disjoint regions) and
     the other rows (frustrated 2T, bad boundary squares, D' runs that end outside every region, failed W').
  S2 [PROOF modulo (L4'), SHEET 13.1] Chamber rows: L(sigma) <= 2 C_in + 2 U_in + c + G2/2 + O(1).
  S3 [GAP P1] Changed ends of trapped inside returns go to N_free unless they are within 2 rows of a g row. Near a
     free g row, the g row's 2 units must cover its <= 4 neighbour rows; near an OWNED g row nothing does. Needed:
     (P1) the rows within distance 2 of g rows carry, besides g itself, enough far evidence; or a per-g-row
     neighbourhood price (a finite strip check, LB's joint_free graph with a neighbourhood tally).
     Data: FIELD has 67 owned g rows and still ratio 5.77; LB cycle (d0 = 1) shows the neighbour ports exist.
  S4 [GAP P2, uses (C_T') and (K)] Untrapped inside returns: 2 U_in <= BQx(REGION) + O(1). Even block boundaries:
     two ribbon interruptions, each >= 2 bad quarters by the square Gap Lemma (now PROVEN, LB G). Odd: (K), >= 4 per
     '/' ribbon crossed by the carrier (SHEET 13.4; R-c). JOINT point: the quarters must be DEEP and not selected
     by route (i). Shallow ones (depth <= 4) near sigma are not in BQx: they must be g rows (P4).
  S5 [GAP P3] The terms c (shallow ports) and G2/2 (column-2 holes): shallow ports are changed, so c is in N_free
     unless near g; a column-2 hole must lie within distance 2 of a g row or of a far changed port (to check: G2 is
     linear only on LF4, 265, where sides 2, 3 are g-heavy).
  S6 [GAP P4] Rows outside chambers: frustrated rows by (R2) localised (SHEET 13.3): F(I) <= N(I) + bdry_bad(I) +
     G2(I)/4; bdry_bad and the D' runs need a g row nearby when their bad squares are shallow (depth <= 4), and
     deep free quarters otherwise. (P4) is a Claim-V-type local statement: a bad square at depth 1..4 next to side
     row r makes some row within distance 2 of r a g row, or holds a far changed port. Finite; not yet checked.
**8.3 Why FJOG pays through BQx (CHECK, `c5_chamber.py`, `c5_chamber.log`).** FJOG untraps its nests with jog
bands, not with collar changes, so N_free(2) = 3 / 5. Inside its chambers the need L - 2 C_in is 306 / 380 and
2 U_in = 258 / 346, while BQx in the chamber regions is 1517 / 1034, and route (i) selects NO quarter inside any
chamber region (sel = 0 on FJOG, FOLD, FIELD, FOLDX): deep-first takes the deepest bad quarters of each corner hook,
which lie at the hook's turn near the board diagonal, outside the side-midpoint chambers. So on the data the
flux payments (diagonals) and the untrapping payments (chamber interiors) are spatially separated. The proof must
not assume this: a tour with clean diagonals would make route (i) select inside chambers (S4 joint point).
FOLD, FIELD and FOLDX have BQx(REGION) = 0 and need 22 / 9 / 30 = O(1) inside chambers (paid by changed ends).
**8.4 Red-team targets.** (i) A family with owned g rows dense near trapped nests (P1). (ii) A tour whose corner
flux defects also untrap a nest, so that route (i)'s selections and U_in share quarters (S4; gentle seams, w-structures
S3 / layout G, Claim 44 replay). (iii) Frustrated V sides whose changed ports all sit within 2 rows of g rows while
the g rows are owned (S3 + S6; LF4 has G_free 89 of 118 g rows, so not there).
**8.5 First data on the gaps (CHECK, 2026-10-03).** (P4) `p4_check.py` / `p4_check.log`, 9 tours: a shallow bad
square (local depth 1..4) that is NOT within 2 rows of a g row or of a far changed port occurs only on FOLDB1 (2),
FJOG n=130 (1) and FJOG n=132 (2, 15, 1, 3 by side). The FJOG n=132 side-1 cases are depth-3 / depth-4 squares at
rows 64..69 (the side midpoint), where a jog band meets the side. So (P4) as worded is FALSE on the data; the repair
is to let such a cluster pay through its own deep continuation: a shallow bad cluster at row r is within 2 rows
of a g row or a far changed port, OR it is joined through bad squares to >= 2 free deep quarters per row it
serves. To check next. (P1) from LB r_b.log: the changed ports within 2 rows of g rows (N_re - N_free(2)) are 60 on
every FOLD n (constant), 103 FIELD, 113 / 55 FJOG, 160 LF4, 112 TT16; on LF4 and TT16 they sit on g-dense frustrated
sides, where the g rows themselves (mostly free) cover the rows. The owned g rows (FIELD 67, TT16 43, LF4 29) are the
real P1 question.
Repair test (p4_check.py cluster_deep; bad-square clusters by edge adjacency): FJOG n=132 side 1 (15 squares): cluster of
244 bad squares with 159 free deep bad quarters; FJOG n=132 side 0 (2 squares): 98 squares, 10 free deep; FJOG
n=130 (1 square): 254 squares, 313 free deep. FOLDB1 side 2 (2 squares, one row 71): a 149-square cluster with 0 free
deep quarters (it runs along the shallow zone, or route (i) took its deep quarters). That is one row; the repaired
(P4) must allow O(1) such rows per side, or such a shallow cluster must cost a g row elsewhere along it. Not yet
understood.

## 9. Removing P1 (owned rows): ask the joint strip lemma for coefficient 2 on g (2026-10-03, PROPOSAL + CHECK)

**Idea.** At an owned g row the collar is broken, so it has an extra crossing (F1-V rate 1), and route (i) takes
1/2 of E for it from T. In the joint currency of section 6 that crossing ALSO brings its quarter atoms (holes, X1,
W3; two quarter units per extra crossing on average, since 2E = G + X1 + W3), worth another 1/2 of E. So the joint
lemma should be asked with coefficient 2 on g:
    (B5-joint)  per half side:  (X3 - rows) + Q3'/2 >= 2 #g + N_free(2) - C,
    Q3' = quarter-atom units (hole 1, X1 1, W3 binomial(m-1, 2)) in local squares x = 0..4 of the side rows, minus the
          consumption of route (i)'s shallow users: each shallow quarter a shallow user selects costs 1/2 in the
          left side (a Q3 atom: one unit of Q3'; an S3-minus-S* pair: in E = nu3 + T3/2 it is no longer in nu3, so
          route (i) must take that quarter from the X3 excess, 1/2 unit).
Then E >= f0 + BQx/4 + #g + N_free/2 - O(1), and route (i) needs f0 + owned/2 = N/2 (+ deficiency overpay), so
    E >= N/2 + (#g - owned/2) + N_free/2 + BQx/4 - O(1) >= N/2 + (2 #g + 2 N_free + BQx)/4 - O(1),
using owned <= #g. The connectivity target becomes, with NO ownership in it:
    (C5-all)  2 (#g + N_free(2)) + BQx >= 4n - C,
and (B5-joint) + (C5-all) give X >= 6n - O(1). P1's owned-row question disappears (owned rows count in #g).
**Check (q3_check.py, q3_check.log, 10 tours, before the shallow-user subtraction).** (B5-joint) holds on every side
of every tour; per-tour slack: FOLD 139.5 (n = 96 and 192, constant), FIELD 136, FOLDB1 177.5, FOLDP 161.5, FOLDX
157.5, FJOG 351 / 175.5, LF4 104.5, TT16 259. The tight sides are the U-collar-like sides with no g (LF4 sides 0, 1;
TT16 sides 0, 1): slack 0, with Q3/2 = X3 - rows exactly, i.e. two quarter units per extra crossing, so c = 1 on
N_free is tight there. Shallow-user subtraction, worst case 1 per shallow user: LF4 104.5 - 103 = 1.5 >= 0,
TT16 259 - 41, FIELD 136 - 3, others 0 shallow users. So the data allow (B5-joint), but LF4 is nearly tight once the
shallow users are charged; an exact subtraction is the next check.
(C5-all) on the data: (2(#g + N_free) + BQx) / n = 5.56 FOLD96, 6.58 FIELD, 5.28 FOLDB1, 5.24 FOLDP, 5.40 FOLDX,
10.8 FJOG132, 5.81 LF4, 5.83 TT16 (least 5.24 >= 4). On FOLD it tends to 4 + 4/3.
**R-a, changed target again (for KT Lower Bounds):** certify (B5-joint) with a = 2 on #g and c = 1 on N_free(2);
first without the shallow-user subtraction, then report whether the critical cycles use quarters a shallow user could
select.
**9.1 Exact shallow-user consumption (CHECK, shallow_sub.py / shallow_sub.log): the per-side form fails on LF4.**
Selected shallow quarters in the strip squares, at 1/2 each, per side: LF4 [0, 0, 55, 48], TT16 [0, 0, 21, 20],
FIELD [2, 0, 0, 1]. LF4 side 2 has joint slack 28 < 55, so (B5-joint) WITH the subtraction is false on LF4 side 2
(by 27); TT16 and FIELD keep it. Repair (PROOF of the bookkeeping, no new input): do not subtract per side. Pay every
candidate that lacks two deep payable quarters (lost, deficient, or shallow user; K of them) from the joint side
capacity at 1/2 each, which is what both owning a g row and selecting shallow quarters cost there. Then, with
(B5-joint) WITHOUT subtraction,
    E >= N/2 + #g + N_free(2)/2 + BQx/4 - K/2 - O(1),
and the connectivity target is
    (C5-K)  4 #g + 2 N_free(2) + BQx - 2K >= 4n - C          (gives X >= 6n - O(1)).
K counts route (i)'s demand on the side capacity; K <= #g + (shallow users without a g end). Data: K = 7 (FOLD, every
n), about 70 (FIELD), 132 (LF4: 29 lost + 103 shallow users), 84 (TT16), 17 / 27 (FJOG). (C5-K) / n: FOLD96 5.81,
FIELD 6.84, LF4 5.52, TT16 6.22, FJOG132 11.1: all >= 4. LF4 is the least, and it is a frustrated-side tour, not a
nest tour.

## 10. (C5-K): statement, two regimes, proof plan (2026-10-03, KT Structures, fifth session; STATEMENT + ARGUMENT + CHECK)

Scripts: `c5k_sides.py` (log `c5k_sides.log`: per side g, owned, SU, K, N_free(2), near rows), `trap_h.py` (log
`trap_h.log`: re-pair one vertical collar by the P rule and count cycles), `q3_check_h.log`, `beyond5_ledger_h.log`
(the six new H-regime tours LF1, LF2, LF3, LF5, H16a, H16b from w-integrator/tours).

**10.1 Statement.** There are constants C, n0 such that every closed tour, n even >= n0, has
    (C5-K)  4 #g + 2 N_free(2) + BQx - 2K >= 4n - C,
#g, N_free(2), BQx as in section 8 (no ownership), K = N - #(retained candidates with two deep payable quarters)
= lost + deficient + shallow users (SU). With (B5-joint) without subtraction (9.1) it gives X >= 6n - O(1).
Units: a side row demands 1; a g row supplies 4, a far changed port 2, a free deep bad quarter 1; a K candidate
demands 2. Two exact rewritings (owned rows are distinct, Claim 42; K = owned + SU):
    (C5-K) = (C5-all) + 2 (#g - K) = (C5-4) + 2 (#g - SU).
So (C5-K) follows from (C5-4) if SU <= #g + O(1). That reduction is FALSE on the data: LF1 has SU = 121 > #g = 93.
(C5-K) is a new count; it is not (C5-4) plus a local fact.

**10.2 Data (CHECK, 2026-10-03, 19 tours; rows = 4(n - 16) in LB r_b.py convention).**
| tour | n | #g | owned | SU | K | N_free(2) | BQx | (C5-K)/n |
|---|---|---|---|---|---|---|---|---|
| FOLD | 96 / 144 / 192 / 240 / 288 | 19 | 7 | 0 | 7 | 102 / 198 / 294 / 390 / 486 | 292 / 356 / 420 / 484 / 548 | 5.81 / 5.65 / 5.57 / 5.53 / 5.49 |
| FIELD | 166 | 92 | 67 | 3 | about 70 | 244 | 420 | 6.84 |
| FOLDB1 | 144 | 27 | 13 | 0 | 13 | 201 | 304 | 5.47 |
| FOLDP | 96 | 19 | 8 | 0 | 8 | 97 | 271 | 5.47 |
| FOLDX | 100 | 29 | 11 | 0 | 11 | 107 | 268 | 5.76 |
| FJOG | 130 / 132 | 74 / 39 | 27 / 17 | 0 | 27 / 17 | 3 / 5 | 1845 / 1336 | 16.1 / 11.1 |
| LF4 | 96 | 118 | 29 | 103 | 132 | 161 | 0 | 5.52 |
| TT16 | 72 | 98 | 43 | 41 | 84 | 112 | 0 | 6.22 |
| LF1 | 96 | 93 | 11 | 121 | 132 | 160 | 0 | **4.46** |
| LF2 | 96 | 133 | 45 | 87 | 132 | 160 | 0 | 6.13 |
| LF3 | 96 | 113 | 37 | 95 | 132 | 160 | 0 | 5.29 |
| LF5 | 104 | 123 | 42 | 106 | 148 | 184 | 0 | 5.42 |
| H16a / H16b | 96 | 100 | 33 / 35 | 99 / 97 | 132 | 161 | 0 | 4.77 |
(C5-K) holds on all 19 tours; the least is LF1 (4.46). (B5-joint) without subtraction also holds on every side of the
six new tours (q3_check_h.log; slack 0 on the U-collar sides, as on LF4). FOLD tends to 4 + 4/3 (K = 7).

**10.3 Two regimes.**
FOLD regime (all fold tours, FIELD, FJOG): K = O(1) (FIELD: K about #owned), because route (i) is paid by the deep
flux quarters. (C5-K) is then (C5-all) up to O(1), and the section 8 plan applies, with P1 replaced by P1' below.
H regime (LF1-5, TT16, H16a/b): the interior is a perfect field (BQx = 0) and EVERY candidate is K (K = N = 2n - 60).
So (C5-K) asks for 4#g + 2 N_free >= 4n + 2N, about 8n: twice the run-end row count. Per side (c5k_sides.log):
  - all 4(n - 16) side rows are through-run ends (2T, 9.1); the frustrated ends are on the two horizontal sides;
  - the horizontal sides carry the g rows: density #g / (frustrated rows) = 0.53 (LF1) .. 0.75 (LF2, TT16 0.75);
    LF1 side 3 has g rows on alternate rows exactly (40 of 80);
  - the vertical sides carry N_free = 2(n - 16) +- 1 on all 8 tours: one full U collar (LF1-5, TT16: every port of
    one vertical side changed) or two half-U collars (H16a/b: one changed port per row on each vertical side).
In units: the g rows pay the rows (4#g >= 4(n - 16) on all 8; LF1 372 >= 320), and the U collar pays the K demand
(2 N_free = 4n - 64 >= 2K = 4n - 120). The vertical changed ports are NOT used by the run-end row ledger (their rows
are the happy ends of through runs, paid at the frustrated end). So in the H regime (C5-K) contains a second
connectivity statement besides the row ledger: trap parity of the through strands (P5).

**10.4 Steps and status.**
  S1 [PROOF, SHEET 9.1, 13.1] row partition. S2 [PROOF modulo L4', SHEET 13.1] chamber rows.
  S3 [GAP P1', replaces P1] Ownership is gone: an owned g row pays its own row 1 and its candidate 2 from its 4 units,
     and keeps 1. What is left is the neighbourhood: the <= 4 rows within distance 2 of a g row lose their changed
     ports (they are not N_free(2)). An isolated owned g row inside a chamber can leave a deficit of up to 3 units.
     Data: FOLD has 19 g rows, 39 near rows, 60 near changed ports (constant in n), so the deficit is O(1) there.
     Needed: g rows inside chamber regions are O(#chambers) + O(BQx(region)), or an LB strip coefficient b > 0 on
     the near changed ports (the d0 = 1 cycle of LB B5b shows b = 0 in the pure-crossing form; the joint form is
     untested).
  S4 [GAP P2] unchanged: untrapping quarters must be deep and not selected (Gap Lemma for even boundaries, (K) for
     odd ones, R-c). In the FOLD regime route (i) selects no quarter in a chamber region on the data (8.3).
  S5 [GAP P3] unchanged (shallow ports c, column-2 holes G2).
  S6 [GAP P4, repaired form of 8.5] unchanged; FOLDB1 row 71 is the open O(1) case.
  S7 [GAP P5, NEW, H regime] the K demand when K is linear.
     (a) [PROOF of the mechanism, ARGUMENT for its count] Cross-chord trap parity. SHEET 8.2 is written for returns;
         the same development works for two cross chords that join P pairs on side 0 to P pairs on side 1 through a
         good region: with an even transfer shift they close a 4-piece cycle (chord, P pair, chord, P pair). A
         closed tour must break one P pair of each such cycle; both ports of the broken pair are changed.
     (b) [CHECK, trap_h.py] Re-pair the changed vertical collar of each H tour by the P rule (other sides kept):
         LF4 n = 96 / 144: 57 / 89 cycles; LF1 n = 72 / 96 / 120: 41 / 57 / 73; LF5 n = 104 / 156: 64 / 97; TT16
         n = 72 / 96: 33 / 45; H16a: 35 (side 0), 29 (side 1), 63 (both). So c = 2n/3 - O(1) (LF family), n/2 - O(1)
         (TT16). Along LF4 side 0, the upper half is a stack of one-pair loops (one per row), the lower half has one
         loop every 3 rows inside one big cycle.
     (c) Count: every cycle but one needs a broken P pair, so N_changed(vertical) >= 2(c - 1), about 4n/3 (LF), n
         (TT16). The tours use 2n - 32, the full U collar. Trap parity alone does NOT force the full U collar.
     (d) Risk. With only 2(c - 1) far changed ports, (C5-K) in the H regime needs 4#g >= 4n + 2K - 8n/3, i.e. g
         density >= 2/3 on the frustrated rows when K = N. LF1 has 0.53. So an LF1 variant whose vertical collar
         changes only the trapped pairs (rotations in the one-pair stack, one switch per 3 rows below) still keeps
         (C5-K) at n = 96 (372 + 224 - 264 = 332 >= 320). For large n, if LF1's density 0.53 persists, the left side
         is about 4.24n + 2.67n - 4n = 2.9n < 4n: (C5-K) fails by about 1.1n, IF the variant is a tour and IF its
         switches are not g rows (a g row is worth 4, more than its 2 far ports). Such a variant does NOT threaten
         X >= 6n: LF1 has E = 381 = 3.97 n, and the saved collar crossings are about n/2. It only shows that the
         split (B5-joint) + (C5-K) can be wrong in this regime.
     (e) Repair if (d) happens: move the frustrated sides' extra strip capacity into the price side. The (B5-joint)
         slack on the horizontal sides is 28 to 240 per side on the 8 H tours, i.e. at least 0.76 per non-g
         frustrated row (LF2-5 side 2: 28 / 36, 28 / 35, 29 / 38). A term a_F * F' in (B5-joint) (F' = frustrated
         rows that are not g rows) adds 2 a_F F' units to (C5-K). LF1 has F' = 83, about 0.94n for large n, so the
         gap of (d) needs a_F >= 0.6; a_F = 3/4 is the natural target (data allow 0.76). This is a finite strip
         question for Lower Bounds (frustrated boundary half imposed).

**10.5 Recommendation (for the Chief Researcher).** P5 first: it is the only gap where (C5-K) may be FALSE, not just
unproved, and it is testable by construction. Step 1 (Structures, moderate: a CP-SAT / DP search for collar paths in
columns 0..2 with prescribed port pairs): build the LF1 variant of S7 (d) from the trap_h.py pair list (re-pair only
the trapped vertical pairs, minimise collar crossings), check it is one cycle, and measure #g, N_free, (C5-K)
and (B5-joint). Step 2 (Lower Bounds, only if step 1 breaks (C5-K)): the a_F strip run. P1' and P2 then follow in the
FOLD regime, where K = O(1) and the section 8 plan stands.
