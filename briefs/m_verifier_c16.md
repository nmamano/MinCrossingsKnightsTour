Chief Researcher -> KT Verifier (queued after Claim 15). Claim 16 (small): new material in the turns write-up
(writeup/turns/main.tex, by KT Lower Bounds), not reviewed yet:
 (a) a HAND proof of the TT16 turn count: in the bottom+top bands every column has exactly 4 turns (per-column counts
     (3,1,2,2,1,3,2,2) with c_k + c_{1-k mod 8} = 4 for top phase 1); left+right 4 per row; the corner squares have 82 turns for
     every residue; so T = 82 + 8(n - 12) = 8n - 14. Check every step against the templates and the corner files.
 (b) writeup/turns/check_corner.py (corner certificate as printed in the write-up: 209 cases) and writeup/turns/figures/tt16.py
     (builds tau_n from the corner files; one closed tour and T = 8n - 14 for even n = 48..102). Run them, and compare with your own
     independent checker.
 (c) Read the write-up's statements (Theorem 1, Corollary 2: the paper's ">= 8n" conjecture is false for every even n >= 48 and
     true up to |T_min - 8n| <= 28) for exact agreement with what was audited in Claims 6-7 and the turns-lower audit.
Write as Claim 16. One CPU core.
