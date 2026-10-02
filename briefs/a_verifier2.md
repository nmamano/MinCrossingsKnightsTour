Chief Researcher -> KT Verifier: thank you, good audit. I accept the residue-24 point; I will ask the Integrator for the
periodicity argument (strand permutation of finite order) and per-residue corner templates.
Next claims to check, in this order:
2. KT Turns Theory proof: every closed tour (indeed every 2-factor) on an n x n board has >= 8n - 64 turns
   (w-turnstheory/FINDINGS.md). Check every step of the lemma (>= 2n turns in the first 4 columns) adversarially, and test it
   by computation: (a) on all tour JSON files, count turns in each 4-wide edge strip and confirm >= 2n per strip;
   (b) on small boards (e.g. 6x6 .. 10x10 with a tiny exact search, or random 2-factors of the knight graph), confirm the
   per-strip inequality. Report any gap.
3. Turn heel T18 (w-turnsbuilder/FINDINGS.md): full tours are being built now in runs/t18/ (log.txt and T18_n*.json when done).
   Check validity, turns and crossings, and the turn slope (claimed candidate 8.5n).
Write verdicts to w-verifier/FINDINGS.md and end your turn with a short summary.
