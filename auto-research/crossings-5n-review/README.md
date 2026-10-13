# Track: review of the 5n - 597 lower bound

Goal: an independent, human-readable check of the tentative bound X >= 5n - 597 (every closed tour and
2-factor, even n >= 32), or a simpler proof of a bound of the form 5n - O(1).

## Status

Agents wrote the proof, and a verifier agent on a different model audited it (Claims 50, 51 and 52 in
[../../bounds-2026/gap/verifier/](../../bounds-2026/gap/verifier/)). No human has reviewed it. It has no Lean
proof. The crossings blog post asks for help here, and says that it could become a paper collaboration.

## What to read and run

- The proof: [../../bounds-2026/CROSSINGS_PROOFS.md](../../bounds-2026/CROSSINGS_PROOFS.md) part B (B.1 to B.7),
  and [../../bounds-2026/gap/turnstheory/PROOF_5N_V2.md](../../bounds-2026/gap/turnstheory/PROOF_5N_V2.md).
- The check commands: [../../bounds-2026/RESULTS.md](../../bounds-2026/RESULTS.md), section
  "Crossing lower bound: 5n-597". The 3,136-state cut-state certificate
  (`gap/lowerbounds/simple_strip/check_cut_certificate.py`) needs NumPy.

## What to submit

A note that goes through the proof step by step and says, for each step, whether you checked it by hand, by
your own code, or not at all. If you find a gap, give its exact location and, if you can, a counterexample to
the step. A missing proof, a failed check, and a counterexample are different findings. Say which one you have.
