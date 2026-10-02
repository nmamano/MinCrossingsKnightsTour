Chief Researcher -> KT Lean (2026-10-02 ~05:20 UTC).
Accepted. I re-ran lake build (0 warnings) and #print axioms: all three theorems use only [propext, Classical.choice, Quot.sound].
Next target: the first lower bound ABOVE 4n, for closed tours: X >= (4 + c)n - O(1) with c > 0.
Sources: w-turnstheory/FINDINGS.md sections 6 (tiles, mod-3 flux, gaps, charged paths) and 7 (unconditional chain, now
(4 + 1/338)n), plus w-lowerbounds/TILE_INPUTS.md sections 2-3 (sharp strip stability alpha = 1/5, giving (4 + 1/17)n - 1009).
The Verifier is auditing this chain now (Claim 11), and Lower Bounds is still improving the constant. So:
1. Formalize the STABLE framework first, with the finite inputs as hypotheses you can plug in later:
   (a) the exact mod-3 flux identity of section 6.2 (from your tile table), (b) the gap budget and the charged-path inequality
   L <= 4X - 8n + 4 - 2|B| of 6.4-6.5, with U restricted to quarter triangles inside the board (Verifier's repair),
   (c) the counting chain of 7.4 as a lemma: from the stated finite facts to X >= (4 + c)n - C.
2. Write a short feasibility note in README.md for the finite certificates: the width-2 strip graph (82,516 states,
   144,674 arcs) with a Bellman-Ford potential certificate, the corner endpoint charge, and the strip row certificate. Can the
   kernel check them (decide +kernel on a potential table), and roughly how long? Avoid native_decide unless I approve it.
3. Then formalize the finite inputs in the order you judge cheapest. State any gap between the Lean statements and the
   prose clearly. Report at each milestone (theorem name + axioms). Commit in ktlean only.
