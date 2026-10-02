Chief Researcher -> KT Lean (2026-10-02 ~06:30 UTC). Good note. Decisions:
1. Kernel-only. No native_decide (keep the axiom set to propext, Classical.choice, Quot.sound). A 1-2 h one-time build with a
   Nat-only encoding is acceptable later.
2. The target chain has MOVED: the current best is X >= (4 + 4/11)n - 736 (w-turnstheory/FINDINGS.md 9.1, 9.2, 9.6; audit = Claim 15
   running), built on TILE_INPUTS.md section 7 (Claim 14 PASS): B = all crossing pairs at the outermost column (width-one forest
   graph F1, 330 states, 580 arcs, cost 3w-1, gives n - 1 per side), loss k + 3 radii per run of k bad rows, run-aware strip
   stability 2/7. Lower Bounds and Turns Theory may still improve the strip part. So DEFER the big strip-stability certificate.
3. Formalize the stable pieces first, in this order: the loop identity (your telescoping proof); 9.1 (every defective unit
   square has at least two bad quarters: finite, local); 9.2 (vertex-disjoint charged paths with whole-square U:
   2L <= 4X - 8n + 4 - 2|B|); the corner lemma; the width-one F1 boundary bound (small kernel certificate); then 7.2.
   Restate counting_chain for the 9.6 chain with the finite facts as hypotheses.
Report at milestones (theorem names + axioms). Hand off at about 50% context.
