Chief Researcher -> KT Integrator: NEW TASK from Nil (2026-10-02): publish ALL our work as a PUBLIC repo on his GitHub
(account nmamano, gh is logged in), with a README that explains the METHODOLOGY. Repo name: knights-tour-bounds.
STEP 1 (prepare, do NOT push yet):
- Staging dir ~/nil/knights-tour-bounds (it is free; create it). rsync from ~/nil/knight-formation-research EXCLUDING:
  .venv/, ktlean/.lake/, ktlean/.git/ (keep ktlean sources), CR_STATE.md (internal notes with private emails), paper.pdf and
  paper.txt (copyright; link https://arxiv.org/abs/1904.02824 instead), board-patched.js (Shisheng Li's code; link his repo
  https://github.com/daizisheng/MinCrossingsKnightsTour and his page https://daizisheng.github.io/MinCrossingsKnightsTour/ instead),
  all __pycache__/, all *.npy (regenerable; say which script regenerates them), and any other file over 20 MB (list them).
  Keep briefs/ (the messages that directed the agents: part of the methodology record).
- Privacy/secret scan of the staging dir: email addresses, tokens, keys, passwords, isomux tokens. Report every hit.
- README.md at the top, factual, third person, no hype (Nil may edit it later):
  (a) Results table (from RESULTS.md) with links to proofs, audits, Lean theorems and the one check command each.
  (b) Methodology: one closed research session, 2026-10-01/02 (Pacific), in the Isomux multi-agent office, room Research Lab.
      Human: Nil Mamano (co-author of the 2019 paper) set the goal (asymptotic bounds) and required convincing proofs.
      Agents and models: Chief Researcher (Claude Opus 5.5, coordination); KT Integrator (Claude Opus 5.5: tour assembly,
      CP-SAT corner completion, period arguments, demo); KT Structures (Claude Opus 5.5: global layouts: folds, seams, jog bands);
      KT Lower Bounds (Claude Opus 5.5: lower-bound framework, strip transfer graphs, stability certificates; later the blog
      drafts); KT Edge Searcher (Claude Opus 5.5: edge gadget search by CP-SAT and C++ transfer matrices; independent C++
      certification); KT Verifier (GPT-6 Astra: adversarial audits with its own code, Claims 1-22 in w-verifier/FINDINGS.md);
      KT Turns Theory (GPT-6 Astra: proofs); KT Lean (Claude Opus 5.5: Lean 4 + Mathlib); KT Turns Builder (Codex, early turn
      heel searches, retired). Verification rules: every claim audited by a different agent with independent code; finite
      certificates checked by 2-3 independent implementations; key lower bounds in Lean (4n - 2, 8n - 64; 14n/3 with strip
      stability as an explicit hypothesis). Negative results kept (jog bands, layout G, carrier search).
  (c) Reproduce: Python version and a requirements.txt (only what is used: ortools, python-sat, numpy, scipy, networkx; pin
      the versions in .venv), the Lean toolchain (ktlean/lean-toolchain, lake build), the demo (static, demo/serve.py).
  (d) Map of directories (one line each). (e) Credits: the paper authors, Parker Williams, Shisheng Li (links). (f) License:
      write "TODO: license (Nil)" for now.
- git init, one commit (default git identity; message ends with: Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>).
STEP 2: report to me: file count, total size, the exclusion list, scan results, README path. Push only after I say go.
