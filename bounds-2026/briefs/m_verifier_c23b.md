Chief Researcher -> KT Verifier (2026-10-02 ~18:05 UTC). Thanks for Claim 23A (sent to the writer to apply). Claim 23, part B:
the CROSSINGS post appendix, same scope as 23A. File: writeup/crossings/post.mdx, section "Appendix: full proofs", parts
A (19n/3 + 142 upper bound, adapted from w-turnstheory/PROOF_fold.md) and B (14n/3 - 407 lower bound incl. 4n - 2, adapted
from w-turnstheory/PROOF_crossings_lower.md with the Claim 21 corrections). Turns Theory's note: w-turnstheory/APPENDIX_STATUS.md.
(1) COMPLETENESS: a careful reader can verify both bounds from the appendix alone plus the named check commands. List every gap
    (step used but not stated, unresolved reference, undefined symbol, finite fact without a check command, command that does
    not run from a clean shell in the repo root or does not print what the text says). The lower bound uses strip stability
    as a stated input (Lean theorem KT.ClosedTour.fourteen_mul_le_of_stability takes it as a hypothesis, by Nil's decision):
    check the appendix says so plainly and names how stability is certified.
(2) FAITHFULNESS: the appendix says the same as what you audited (Claims 12, 19, 20, 21 and Claim 9 for 4n - 2; the Lean
    theorems). Re-run every named check command; flag any number, range or statement that differs from the audited source.
Also check the crossings post body agrees with the appendix. Exact text replacements for each defect. Write as "Claim 23B" in
w-verifier/FINDINGS.md. One CPU core. Live render (for reference only): http://127.0.0.1:21019/blog/knights-tour-crossings
