# Claim 47: per-distance port weights — 2026-10-03

**FAIL: C5-W is false at both proposed points (a,c1)=(2,1/2) and (2,2/3).** A new pairing-preserving 6-by-24 U-collar patch gives an unbounded family of closed tours with

    C5-W = (313/84)n + O(1)       at (2,1/2),
    C5-W = (23/6)n + O(1)        at (2,2/3).

The deficits from 4n are respectively (23/84)n-O(1) and n/6-O(1). No fixed additive constant repairs either statement. This refutes the proposed connectivity statistic, not a 6n crossing bound itself and not the conditional S-W plus C5-W algebra.

## 47A. Exact definitions and the old patch — PASS

The audited statistic from BEYOND5 section 12 is

    C5-W = 2a g + 2c1 P1 + 2(P2+P3) + BQx - 2K.

Pj counts changed ports at distance j from the nearest strong row, with P3 including every distance greater than two. Ports on a strong row receive zero. K is N minus the number of retained candidates with two deep payable quarters; BQx is deep bad quarters after the deep-first selection, as in section 10.1. Counts of g and ports have no row-ownership subtraction.

The old Claim 45 patch independently gives changes (g,P0,P1,P2,P3)=(4,6,14,14,-38). Its contribution changes by -18 at c1=1/2 and -40/3 at c1=2/3 when a=2. Section 12's -18 value is correct. That old patch with its stated spacing no longer refutes these points.

## 47B. New finite patch — CERTIFIED

The saved witness is `gap/verifier/claim47_U_gadget_24.json`. Its SHA-256 is `e8cc3900742a84230d86c48852e10e666b24b6272ef5ab613cf5099f8b2cedab`.

Use the pure U field in coordinates inward from a side:

    x=0: neighbours (2,y+1), (1,y-2),
    x=1: neighbours (3,y+1), (0,y+2),
    x>=2: neighbours (x+2,y+1), (x-2,y-1).

The patch changes only edges whose two endpoints are in 0<=x<6, 0<=y<24. The JSON gives all removed and added edges. Independent, solver-free checks establish:

* All edges are knight moves; every vertex retains degree two.
* The 30 boundary-stub pairs are identical before and after replacement.
* Every component inside the rectangle has two boundary stubs. There is no internal cycle.
* All changed tile quarters have square column at most four. Thus no deep quarter (depth at least five) changes.

Consequently insertion in any matching pure neighbourhood preserves the whole closed tour. It cannot split the tour or create a separate cycle. This is a boundary-pairing argument, not an inference from a small-board solver result.

The new strong rows are exactly

    1, 3, 5, 8, 11, 13, 14, 18, 21.

The independent local count gives

| Quantity | Change per isolated copy |
| --- | ---: |
| g | +9 |
| P0 | +18 |
| P1 | +9 |
| P2 | +5 |
| P3 | -50 |
| Deep bad quarters | 0 |

Thus the side contribution changes by 18a+18c1-90. At the two requested points this is -45 and -42.

Discovery used one CP-SAT worker for 40 seconds. Its status was FEASIBLE, not OPTIMAL. The search minimized an upper bound obtained by charging every selected collar-cut port, even an unchanged one. None of the proof uses optimality or that surrogate objective. The independent checker traces the actual collar partners and applies the P/P' rule to decide which ports are changed.

## 47C. Periodic repetition — CERTIFIED, with a finite locality proof

Copies every 28 rows have disjoint changed vertex sets and leave the four intervening rows fixed. Each copy preserves its boundary matching, so any finite sequence of copies preserves the exterior connections. The exact lifted periodic check enumerates the ports of one period and follows every collar path to its other port. All traces stay within row interval [-3,36], contained in the explicitly constructed periodic neighbourhood. Their endpoints and the strong-row patterns therefore determine the infinite-periodic count exactly. Translating by 28 preserves the P/P' parity rule. This is a finite-support check of the infinite pattern, not extrapolation from six repeated patches.

In one period of 28 rows:

    g=9, P0=18, P1=9, P2=5, P3=6.

There are 38 actual ports, all changed. The original U field has 56 changed ports per 28 rows. Its side contribution is 112. The new contribution is

    18a + 18c1 + 22,

which is 67 at c1=1/2 and 70 at c1=2/3, with a=2. This proves the losses 45 and 42 per period. The finite six-copy checker also finds exactly six times those losses. Periods 24 and 32 pass separate checks, but the counterexample below uses only period 28.

## 47D. Closed-tour family — PROVEN using the audited FOLD templates

Use the same audited n=96+48k FOLD family as Claim 45. Each side has a pure U interval of length n/4-O(1); the remaining fixed gadgets and end zones need only bounded buffers. Insert patches at spacing 28 in those four intervals. The number of copies is m=n/28+O(1). The finite pairing certificate above proves connectivity for every such insertion.

The deep part is unchanged. Claim 45's exact template counts give BQ_deep=(16/3)n+O(1). Its six-radius, four-frame hook check gives at least two deep bad quarters to every retained candidate except O(1) end-zone exceptions; those quarters are untouched. Thus, with L retained candidates and N=2n-60,

    BQx = BQ_deep - 2L + O(1),
    K = N-L + O(1),
    BQx-2K = BQ_deep-2N+O(1).

This cancellation remains valid even if the patch causes linearly many lost candidates. There is no assumption that K remains bounded.

Before insertion, the weighted side contribution is 4n+O(1): the U intervals supply two changed ports per row, with only O(1) strong rows, and the other side intervals contribute only bounded exceptions to this count. Hence the original C5-W is (16/3)n+O(1). After insertion it is

    (16/3)n - 45m + O(1) = (313/84)n+O(1),
    (16/3)n - 42m + O(1) = (23/6)n+O(1),

at the respective target points. This proves the stated linear deficits. The argument uses exact periodic templates and the patch pairing certificate; it is not a fit to measured finite-tour values.

As a separate end-to-end check, four patches were inserted into the saved n=288 FOLD tour. The complete tour passed the independent degree, reciprocity and single-cycle check. The census uses the author's actual g/changed-port definitions and separately recomputes deep quarter multiplicities and the retained-path selection:

| Quantity | Original n=288 | Patched n=288 |
| --- | ---: | ---: |
| Crossing pairs | 1936 | 2380 |
| g | 19 | 55 |
| P0 | 14 | 86 |
| P1 | 30 | 66 |
| P2 | 16 | 36 |
| P3 | 486 | 286 |
| BQ_deep | 1566 | 1566 |
| BQx | 548 | 590 |
| K = lost candidates | 7 | 28 |
| C5-W at c1=1/2 | 1644 | 1464 |
| C5-W at c1=2/3 | 1654 | 1486 |

Every retained candidate in these two tours has two deep quarters. The total changes are exactly -180 and -168, or -45/-42 per copy. Neither n=288 value itself lies below 4n; the counterexample to a universal additive-constant statement is the unbounded family above.

## 47E. Failure mechanism and repairs

**FAIL for the proposed worst-pattern argument.** The section 12.3 arithmetic keeps two changed ports per row and changes only their weights. The patch removes 18 ports per 28 rows while preserving the whole tour's boundary pairing. The strong rows cannot pay both for the deleted ports and for the remaining discounted neighbours at either requested point. Thus a g row every three rows in a fixed two-port-per-row collar is not the worst allowed configuration.

For this period-28 family alone, a necessary condition for the proposed universal count is

    16/3 + (18a+18c1-90)/28 >= 4,
    a+c1 >= 79/27.

At a=2 this requires c1>=25/27, so both proposed weights fail. This is a necessary condition, not a sufficient repair or a strip certificate. The data frontier is not a universal certificate either. Raising the neighbour weight to pass this family would require a new strip check and further red teaming.

An alternative repair must retain the collar capacity spent when ports disappear, for example an explicit residual shallow-capacity term with its own ownership proof. No corrected global inequality is asserted here. The patch changes no deep quarter, so this failure does not rely on double spending deep flux and untrapping quarters. The audited 5n proof remains intact.

## Evidence and proof size

Reproduction from the research root:

    .venv/bin/python gap/verifier/claim47_check.py gap/verifier/claim47_U_gadget_24.json gap/verifier/claim47_repeat_28.json
    .venv/bin/python gap/verifier/claim47_period.py
    .venv/bin/python gap/verifier/claim47_insert.py gap/verifier/claim36_FOLD_n288.json
    .venv/bin/python gap/verifier/claim47_scan.py gap/verifier/claim36_FOLD_n288.json gap/verifier/claim47_patched_n288.json

The first two commands do not run a solver. Witness, periodic traces, finite insertion and census are in `claim47_U_gadget_24.json`, `claim47_period.json`, `claim47_insert.json`, and `claim47_scan.json`. Search code and log are `claim47_search.py` and `claim47_search24.log`. Prior exact deep-template evidence is `claim45_hook_periods.json` and `claim38_corridor_bq.py/json`.

Proof size: one 6-by-24 finite patch, a 30-pair boundary check, one lifted period-28 collar trace, and the previously audited FOLD template counts. No large transfer graph or new lower-bound certificate is needed. The finite closed-tour census is an additional check, not the asymptotic proof.
