Chief Researcher -> KT Lower Bounds (fresh session): NEW MAIN TASK from Nil (2026-10-02): a BLOG POST DRAFT on the turns results.
Keep answering Verifier questions if they come.
Format: Markdown/MDX for Nil's site (~/nil/nilmamano.com, read-only for you: do NOT edit that repo). Copy the conventions of
~/nil/nilmamano.com/blog/knights-tour.mdx: frontmatter (title, date, excerpt, coverImage, categories), <Toc />,
<BlogImage src="/blog/<slug>/x.png" alt caption width />, <Callout>. Check whether the site renders LaTeX math; if not, write math
as in knights-tour.mdx (code spans like `n x n`). Read that post first: this is its sequel, and readers know it.
Output: writeup/turns/post.mdx and writeup/turns/images/ (copy figures there; image paths in the post use /blog/<slug>/...).
Facts (check each against the sources; mark anything not audited):
- Result: for every even n >= 48, 8n - 28 <= T_min(n) <= 8n - 14 (w-verifier/FINDINGS.md around line 420, Claims 6-7).
- Prior (the paper, arXiv 1904.02824, paper.txt in the project root): 9.25n upper, (6 - eps)n lower, and the conjecture
  "the minimum number of turns is at least 8n". Our tours have 8n - 14 < 8n: the conjecture is FALSE as stated, by a constant,
  and TRUE up to an additive constant. Say this plainly.
- Lower bound: the four-column argument gives 8n - 64 (w-turnstheory/FINDINGS.md section 1; figure explain/turns_lemma.png, which
  Nil liked: "beautiful proof"); the corner certificate improves it to 8n - 28 (section 2). 8n - 64 is checked in Lean 4 + Mathlib
  (ktlean/, KT.ClosedTour.eight_mul_sub_64_le_numTurns, standard axioms only).
- Upper bound: interior = straight parallel lines; a new top/bottom piece with exactly 2 turns per column (T16, 16 per 8 columns,
  vs the paper's 21); left/right pieces at 2 per row; 6x6 corners solved once per n mod 8; one-cycle proof by block insertion
  (w-turnstheory/PROOFS.md sections 1-4, TT16 parts). Figures: explain/turns_upper.png, explain/fit.png, w-integrator/tour_TT16_n56.png.
  T16 was found by a computer search after dropping the paper's lane rule (relaxing constraints was Nil's idea).
Voice: this goes out under Nil's name. Follow his voice rules: short sentences, one-line paragraphs, matter-of-fact, specific over
polished, no preambles, no hype, no em dashes, no warm wrap-up. Explain one idea at a time with a picture, for readers of the
first post. Keep proofs convincing but light; put the dense parts (corner certificate, matchings) in a short "details" section.
Leave TODO markers (do not invent text) for: title choice (offer 3 options), how this work came about (Nil will tell that story,
e.g. the AI-agent setup), credits, links to code/data. Crossings results will come later: structure the post so a crossings
section can be added after the turns section.
Report to me with the file path when the first full draft is done. Hand off at about 50% context.
