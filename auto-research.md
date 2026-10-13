# Auto-research: guide for agents

This file is for AI agents, and the people who run them, who want to contribute to this repository.
It says what the maintainer, Nil Mamano, needs help with. Read it before you start. Then pick one
research track below. Do not spend your session on small incremental optimizations.

This file follows the auto-research convention proposed by Rohan Arun
([post](https://x.com/RohanArun/status/2110022929048056246)): an `auto-research.md` guide for agents,
plus an `auto-research/` folder where contributors share results, including negative ones.

## The problem

A closed knight's tour on an n x n board visits every cell once and returns to the start. A turn is a
cell where the knight changes direction. A crossing is an unordered pair of tour moves whose segments
cross properly; a shared endpoint does not count. We want the minimum number of turns, T_min(n), and the
minimum number of crossings, X_min(n), of a closed tour, as functions of n. The 2019 paper is
[arXiv:1904.02824](https://arxiv.org/abs/1904.02824). The 2026 results, found mostly by AI agents, are in
[bounds-2026/](bounds-2026/). All bounds below are for even n.

## Current state

Turns. The leading term 8n is exact. Only the additive constant is open.

- Lower: T >= 8n - 24 for n >= 20 ([TURNS_LOWER24.md](bounds-2026/TURNS_LOWER24.md); no Lean proof).
- Lower: T >= 8n - 28 for n >= 8 ([TURNS_PROOFS.md](bounds-2026/TURNS_PROOFS.md) part C; Lean:
  [Turns28.lean](bounds-2026/ktlean/Ktlean/Turns28.lean)).
- Upper: tours with T = 8n - 14 for every even n >= 48 ([TURNS_PROOFS.md](bounds-2026/TURNS_PROOFS.md) parts D-F),
  8n - 17 for n = 2 mod 8, and 8n - 16 for n = 6 mod 8 ([TURNS_IMPROVED.md](bounds-2026/TURNS_IMPROVED.md)).
- Single sizes: 12 tours from n = 24 to 88 with T - 8n between -15 and -19, for example 8n - 18 at n = 48
  ([TURNS_SINGLE_SIZES.md](bounds-2026/TURNS_SINGLE_SIZES.md)). They are not families.

Crossings. The leading coefficient is open.

- Upper: X <= 19n/3 + 142 for every even n >= 96, the fold construction
  ([CROSSINGS_PROOFS.md](bounds-2026/CROSSINGS_PROOFS.md) part A).
- Lower, tentative: X >= 5n - 597 for every even n >= 32, for closed tours and 2-factors
  ([CROSSINGS_PROOFS.md](bounds-2026/CROSSINGS_PROOFS.md) part B). Agents wrote and audited it. No human has
  reviewed it yet, and it has no Lean proof.
- Lower: X >= 4n - 2 for every tour and 2-factor (Lean: [Crossings.lean](bounds-2026/ktlean/Ktlean/Crossings.lean)).

Blog posts: [turns](https://nilmamano.com/blog/knights-tour-turns) and
[crossings](https://nilmamano.com/blog/knights-tour-crossings).
[bounds-2026/RESULTS.md](bounds-2026/RESULTS.md) is the index: every result, its proof, its audit claim
(in [w-verifier/FINDINGS.md](bounds-2026/w-verifier/FINDINGS.md) and [gap/verifier/](bounds-2026/gap/verifier/)),
its Lean status, its check command, and a list of what is not proved.

## What counts as a contribution

In order of value to the maintainer:

1. A new leading coefficient for crossings: a construction below 19n/3, or a lower bound above 5n.
2. A careful, human-readable review of the tentative 5n - 597 proof. A found error counts as much as a confirmation.
3. A shorter or simpler proof of a known bound. A clean proof that a reader can check by hand, with small
   finite checks, has value even if it does not beat the current bound.
4. A Lean proof of a bound that has none.
5. Progress on the additive constant for turns.
6. A negative result: a proved limit of a method, or a well-scoped failed search.

Not wanted: better additive constants for crossings (for example 597 or 142), a rerun of a closed search
with more compute and no new idea, and cosmetic rewrites of existing files.

## How to verify

- A claim counts only after an independent check. Give a checker that does not import the code that
  produced the result. Use the Python standard library where you can, like
  [gap/verifier/claim58_check.py](bounds-2026/gap/verifier/claim58_check.py).
- Tours: save them as JSON with `n` and `order`, the n^2 cells `[row, col]` (0-based) in cyclic order, as in
  [TURNS_SINGLE_SIZES.md](bounds-2026/TURNS_SINGLE_SIZES.md). Check that every cell occurs once, that every move,
  with the closing move, is a knight move, and count turns or crossings directly. `bounds-2026/kt/core.py` has `validate`,
  `num_turns` and `num_crossings` for the move-code grid format.
- All-size claims: a list of sizes is not a proof. Give an insertion or period argument, like
  [TURNS_PROOFS.md](bounds-2026/TURNS_PROOFS.md) part F or [CROSSINGS_PROOFS.md](bounds-2026/CROSSINGS_PROOFS.md)
  A.2-A.3, plus its finite check. `bounds-2026/w-integrator/allsize_check.py` does this for turn families with a single
  straight interior field (audited scope: Claim 55b).
- Lower bounds: keep the hand argument and the finite certificate apart. Use exact arithmetic. Ship the
  certificate files and one command that checks them.
- Lean: from `bounds-2026/ktlean`, run `lake exe cache get`, `lake build`, and `lake env lean Axioms.lean`.
  No `sorry`, and only the standard axioms.
- If you change shared code, rerun the check commands in [RESULTS.md](bounds-2026/RESULTS.md) from `bounds-2026/`.
  Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` (see
  [bounds-2026/README.md](bounds-2026/README.md), section Reproduce).
- Label each claim with the labels used in `bounds-2026/gap/`: PROVEN, CERTIFIED (exact finite computation),
  ARGUMENT, or CONJECTURE.

## Research tracks

Each track has a folder with a short README. Read it first: it lists known dead ends.

| Track | Folder | Goal |
| --- | --- | --- |
| Crossings upper bound | [auto-research/crossings-upper/](auto-research/crossings-upper/) | Tours with X <= cn + O(1), c < 19/3, for all large even n. |
| Crossings lower bound | [auto-research/crossings-lower/](auto-research/crossings-lower/) | Prove X >= cn - O(1) with c > 5 for every closed tour. |
| Review of 5n - 597 | [auto-research/crossings-5n-review/](auto-research/crossings-5n-review/) | Check the tentative proof step by step, or simplify it. |
| Turns constant | [auto-research/turns-constant/](auto-research/turns-constant/) | Narrow 8n - 24 <= T_min(n) <= 8n - 14 (or - 16, - 17). |
| Formalization | [auto-research/formalization/](auto-research/formalization/) | Lean proofs of bounds that are not formalized yet. |

## How to share results

Put every result under `auto-research/<track>/`, including failed experiments and negative results, so that
other agents do not repeat them. Use one of two forms:

- One note: `auto-research/<track>/YYYY-MM-DD-<handle>-<short-slug>.md`
- A note with code or data: `auto-research/<track>/YYYY-MM-DD-<handle>-<short-slug>/README.md`, plus its files.

The note must include:

- Base commit of this repository.
- The question, and the approach you took.
- Outcome: positive, negative, or inconclusive, with a status label for each claim.
- Model or models and harness (for example, Claude Code with a named model), and what the human did.
- Cost, if you know it: tokens or dollars, wall time, CPU.
- One reproducible command, the directory to run it from, and its expected output.
- For a search: the search space, the solver and its settings, seeds, the stopping rule, and the coverage.
  "No solution found" is not an impossibility proof.
- Links to prior work you build on, in `auto-research/` and in `bounds-2026/`.

Open one pull request per result. It should add only files under `auto-research/<track>/`. If you also change
code elsewhere, for example a fix to a checker, say so in the PR description and keep that change minimal.
Do not edit `RESULTS.md`, the proof files, or the demo. The maintainer updates them after review.
