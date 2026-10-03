# KT Lower Bounds - phase 1 plan: side machinery in the new ledger, and SAT window lemmas

2026-10-03. DESIGN ONLY, except one pilot SAT run (under one minute). Labels: PROVEN / CERTIFIED / ARGUMENT /
CONJECTURE. References: Turns Theory master skeleton gap/turnstheory/PLAN.md (ledger b, f, e, h; lemmas L0-L5).

## Part A. Endpoint restoration (skeleton L3) from the audited strip certificate

**Statement (ARGUMENT; all finite inputs already CERTIFIED).** Let S* be the set of crossing pairs whose two
edges both have an endpoint at depth 0 or 1 of the same side (the pairs counted by the four width-two strips),
let D be the number of uncharged candidates gamma_R, and put b_z = 1 on 4n - O(1) pairs of B (B is a subset of
S*). Then the weights e_z = 1 - b_z on S* satisfy

    sum_z e_z = sum_sigma X_sigma - 4n - O(1) >= D - O(1).

So endpoint restoration holds at any price p <= 1, in particular p = 2/3, with all of it inside S*.

**Proof route.** (i) Exact residues (audited 11.1): a candidate with no inward exception is uncharged iff
h_left + h_bottom = 0 mod 3. (ii) The penalty table 11.2 pays each uncharged candidate: D <= A. (iii) The
11.3 strip certificate at beta = 1 (gap/lowerbounds L1: up and down, both parities, C = 29/4 per oriented
half walk, two implementations) gives A <= sum_sigma X_sigma - 4n + O(1). (iv) Strip overlaps at the corners
are O(1) (1104). Nothing here uses the bad-quarter budget.

**Conditions the other pieces must meet (the plug-in contract).**
1. f (private flux price) and h (connectivity) are supported OFF S*. Crossing pairs with at most one edge in
   a side strip are free for them. If L2 needs S* pairs near the path ends, the split must be certified jointly
   (Part A2 below), not by adding two separate bounds.
2. If the new ledger no longer uses the bad-quarter budget, the inward-exception rule can be dropped: then
   discards are exactly the uncharged candidates and the table without the exception row is pointwise smaller,
   so (iii) still applies.
3. Spare strip capacity: sum_z (1 - b_z - e_z) over S* is at least D0 - A - O(1) >= 0. It is NOT free for h
   unless a joint certificate shows it.

**A2. Joint strip certificate for connectivity at the sides (finite task, CONJECTURE, for 6n).** Arch repairs
near the edge midpoints are side-strip patterns (re-paired line ends, Claim 28: 1/2 per end at width <= 4). If
Structures defines a repair obligation by local strip data (e.g. a row whose port partner differs from the P
pairing), I can certify in the existing strip graph

    X_sigma - length >= p*A_sigma + c*(obligations_sigma) - C,

the same Bellman-Ford machinery with one more row charge. The period-4 field of L1 (which re-pairs line ends
at 1 crossing per row) is the first test case: it would have to pay both its endpoint penalty and its repair.

## Part B. SAT window lemmas (skeleton L1, and support for the L2 red team)

Model: a k x k core of cells with degree exactly 2, a halo of width 2 with degree <= 2, all knight edges with an
end in the core, crossings counted between edges that both touch the core. This is a RELAXATION of every tour,
so any lower bound found holds for all tours, with no fixed exterior field.

**W1. Zero-cost phases (CONJECTURE, pilot evidence).** In a crossing-free window, every core cell is straight
(edges d, -d) or a sharp turn between two cyclically adjacent knight directions, e.g. (1,2)/(2,1) or
(2,1)/(2,-1). These are exactly the free-fold turn types of w-lowerbounds F3. Pilot (2026-10-03,
windows/pilot_center_types.py, k = 7, CP-SAT): 12 of 28 centre types are feasible: 4 straight + the 8 adjacent
turns; all 16 others are INFEASIBLE. Next: exhaustive enumeration of central type maps for k = 9, 11 (blocking
clauses on the central (k-4)^2 types) to classify crossing-free regions as: one field; two fields and a free fold;
junctions of free folds. Expected size: seconds to minutes per k.

**W2. Defect density (CONJECTURE).** Call a cell irregular if its radius-r window is not crossing-free. Certify by
SAT a charge rule: every crossing pair gives weight <= 1 to irregular cells within distance r, and every irregular
cell receives >= c_r. Then (irregular cells) <= X / c_r, which is the quantitative core of the structure lemma
(few crossings imply few non-field cells). Interface rates per unit length (phase A | phase B, by slope) need
long periods; that is the corridor engine of Edge Searcher. I provide SAT checks at short periods with FREE
exteriors, which turns their fixed-exterior rates into lower bounds valid for all tours where they survive.

**W3. Red-team windows for the private price (support for L2 and the Verifier).** The flux of each dual step is
linear in the selected edges (audited flux lemma), so "this dual path segment has total flux t mod 3" is a linear
mod-3 constraint in CP-SAT. Task: minimum crossings in a k x l window, free halo, given the boundary flux data.
If it is below 2/3 per unit length for some window, that is a candidate counterexample pattern for L2 (it then
needs a completion argument). If free-halo windows give a positive price, that is a robust local lemma.

## Feasibility on this box
Window models have about 8k^2 edge variables and about 40k^2 crossing clauses: k = 7 runs in seconds with 2
CP-SAT workers; k = 11 is about 1,000 variables and minutes per instance. Strip certificates (A2) reuse the 21,420
row-start states of L4; one extra row charge keeps the graph under 1 GB. All within one heavy job and 8 GB.

## Main risks
1. Nonlocal charge: with a free halo, flux can be absorbed by the halo, so W3 may give 0 for every fixed window.
   Mitigation: windows that span the whole corridor width with periodic rows, or anchored at a side.
2. W1 may not stay short: larger windows may admit more zero-cost textures (fold junctions of many arms).
   The classification is finite for each k, but it may be long.
3. The contract in Part A fails if L2 needs crossings inside S* (near the path ends). Then a joint strip/window
   certificate is needed. The certified strip surplus (beta = 16/11 with credits) gives some room.
