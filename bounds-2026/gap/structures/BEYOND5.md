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
