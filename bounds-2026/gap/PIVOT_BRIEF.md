# Pivot: a structural lower bound near 6n (Chief Researcher, 2026-10-03)

STATUS: SPECULATIVE. Ordered by Nil. Everything found so far stays (audited: 52n/11 - 360, Claim 26; 204n/43 - 12993,
Claim 27). The strip-model increments stop: they cannot close the gap.

## Goal
Prove X >= c n - O(1) for every closed knight tour on an n x n board, with c near 6 (Nil: "at least 6n or something like
that"). The upper bound is 19n/3 ~ 6.33n. The leading coefficient is the objective; constants do not matter.

## Why the current method stops at 5n (please confirm or correct, Turns Theory)
All our lower bounds have the form X >= [4 + 2beta/(2beta+1)] n - O(1). Even for beta -> infinity this is 5n. The reason:
there are about 2n charged corner paths gamma_R (n/2 per corner; 2n - 60 candidates), and through the bad-quarter
budget each charged path pays only about HALF a crossing beyond 4n. beta only prices the paths lost at the endpoint tests.
So no strip certificate can pass 5n. To go further, a charged path must pay MORE, privately.

## The prices the construction pays (19n/3 = 4n + 4n/3 + n)
- Edges: 4n (1 per row per side). The lower bound already gets this.
- Flux: 4n/3. The 2n charged paths each cross a diagonal corridor once, at 2/3 crossing per path (diagonal carrier
  2/3 per step, certified optimal at widths 3..6 in fold fields; w-searcher, gap/searcher/RATES.md).
- Arch (one-cycle repair near the 4 edge midpoints): n. Each arch line needs a re-paired edge end at >= 1/2 (certified
  for strip depth W <= 4, Claim 28); universal version is ARGUMENT (Structures G2).
Target arithmetic: a private price of 2/3 per charged path gives 4n + 4n/3 = 16n/3 ~ 5.33n (flux alone).
Reaching 6n also needs at least 2/3 of the arch term, i.e. a connectivity (one-cycle) argument worth >= 2n/3.

## The program (three pieces, to hold for ALL closed tours, not only fold layouts)
1. PRIVATE FLUX PRICE (first milestone, 16n/3): each charged corner path pays >= 2/3 crossing (or some p > 1/2) under a
   weight rule in which every crossing distributes total weight <= 1 among the paths near it. This is a local theorem
   about any tour configuration around a dual path whose flux is nonzero mod 3. It generalizes the carrier certificates
   (Claim 17 counting, band.cpp/corr2.cpp) from fold bands to arbitrary local configurations.
2. STRUCTURE LEMMA: away from the sides, a tour with few crossings is a union of crossing-free regions that are parallel
   knight-line fields (with free folds), and every non-field cell or region boundary costs crossings in proportion to its
   size. Needed to make piece 1 and piece 3 tractable (finite local classification, SAT/transfer-matrix certifiable).
3. ARCH / CONNECTIVITY: the one-cycle condition forces re-paired line ends near the edge midpoints (or equivalent),
   priced >= 1/2 per arch line, giving up to n more.
The side machinery we already have (endpoint tests, strip certificates, beta) stays useful for the paths' ends.

## Phase 1: design (now; one turn each, written, no heavy computation)
Each worker writes gap/<you>/PLAN.md (max ~1.5 pages): the exact statement of your piece, why it is plausibly true
(evidence), how you would prove or certify it, the finite computation it needs (state space, feasibility on this box),
and the main risk. Read the sources first: w-turnstheory/PROOF_crossings_lower.md + gap/turnstheory/PROOF_N1.md (the
charged paths, flux identity, bad-quarter budget), w-structures/FINDINGS.md S3-S11, gap/structures/FINDINGS.md G1-G7,
w-searcher/FINDINGS.md (carriers), gap/searcher/FINDINGS.md + RATES.md, w-verifier Claims 17, 27, 28.
- KT Turns Theory: MASTER SKELETON gap/turnstheory/PLAN.md: confirm/correct the 5n diagnosis; design the accounting
  that lets a charged path pay a private price p (what replaces the bad-quarter budget); state the exact local lemma
  needed for 16n/3; say where the arch/connectivity term would enter for 6n. List every lemma with a status slot.
- KT Structures: the STRUCTURE LEMMA and the ARCH piece for general tours (what is provable about tours near the
  sides and the edge midpoints; layout rigidity).
- KT Edge Searcher: the finite certificate for piece 1: a transfer-matrix / Bellman-Ford model of ARBITRARY local tour
  configurations across a family of nested dual paths (not only fold bands); state space and feasibility.
- KT Lower Bounds: local window lemmas by SAT (crossing-free k x k windows: which patterns exist; cost of defects per
  unit boundary), and how the endpoint/side machinery plugs into the new accounting.
- KT Verifier: when the skeleton exists, RED-TEAM it: look for a configuration that pays less than the claimed private
  price (a counterexample to the local lemma), before anyone spends compute on it.
Then I merge the plans, choose the first milestone, and assign phase 2.

## Rules
As in gap/BRIEF.md (write only in your gap/<name>/ folder; public files; one heavy job; <= 8 GB; report to the Chief
Researcher; Astra workers write a report at the top of FINDINGS.md / PLAN.md and end the turn; Claude workers hand off at
~50% context). Honest labels: PROVEN / CERTIFIED / ARGUMENT / CONJECTURE.

## Pareto criterion (Nil, 2026-10-03)
Judge results on TWO axes: the lower-bound coefficient AND the simplicity of the argument. A short, clean proof of
5n - O(1) (or even 4.8n) is valuable even if a long proof gives more. So: keep simple routes alive (e.g. Structures'
ribbon absorption: 5n without the flux machinery), and for every result report its proof size and its finite inputs
(what a reader must check by computer). Prefer arguments a reader can verify by hand plus small checks.
