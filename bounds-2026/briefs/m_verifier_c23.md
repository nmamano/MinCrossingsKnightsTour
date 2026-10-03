Chief Researcher -> KT Verifier (2026-10-02 ~17:10 UTC). Claim 23, part A: the TURNS post appendix.
Nil decided that each blog post carries the FULL self-contained proof as a folded appendix (<details> blocks). He will read
and endorse only this version; a later arXiv paper derives from it. writeup/turns/main.tex is now SUPERSEDED.
File: writeup/turns/post.mdx, section "Appendix: full proofs" (parts A-F: definitions + theorem; four-column lemma, 8n - 64,
sharpness, Lean statement; corner certificate, alpha/beta tables, 209 cases, sharp -7; full TT16 construction with the 16
corner grids generated from the corner JSON files; hand turn count 82 + 8(n - 12); one-cycle block insertion, matchings,
M^2 = M, shift table, check C4).
Audit two things:
(1) COMPLETENESS: a careful reader can verify 8n - 28 <= T_min <= 8n - 14 (all even n >= 48 for the upper bound; the lower
    bound for every n where it is stated) from the appendix alone plus the named check commands. List every gap: a step
    used but not stated, a forward reference that does not resolve, a symbol not defined, a finite fact without a check
    command, a check command that does not run from a clean shell in the repo root or does not print what the text says.
(2) FAITHFULNESS: the appendix says the same thing as what you already audited (Claims 6, 7, 16 and the 8n - 28 corner
    certificate; the Lean theorem KT.ClosedTour.eight_mul_sub_64_le_numTurns). Re-run every check command the appendix names.
    Compare the 16 corner grids against the corner JSON files and against the tours you validated. Flag any number,
    range or statement that differs from the audited source.
Also check that the post body (above the appendix) agrees with the appendix.
Give exact text replacements for each defect. Write as "Claim 23A" in w-verifier/FINDINGS.md. One CPU core.
Part B (the crossings appendix, from Turns Theory) follows when it is ready.
