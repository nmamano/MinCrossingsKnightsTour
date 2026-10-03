Chief Researcher -> KT Integrator (2026-10-03): Nil's order: make OUR demo the landing page at
https://nmamano.github.io/MinCrossingsKnightsTour/ (no bounds-2026/ in the demo URL), bring over anything still relevant from the
OLD 2019 demo (root index.html + board.js), and delete the old demo.
1. Compare the old demo with ours first: list every feature of the old one (n range incl. small/odd n, generation for arbitrary
   n, options, displays, credits/paper link). Port to ours what is still relevant (e.g. if the old one shows Algorithm 1 at n
   values ours lacks, or has a feature Nil may expect). Keep the paper citation and link on the page.
2. Serve the demo at the repo root: the demo files live at the root (index.html etc.) or the root index loads them; the demo's
   data paths must keep working. Remove the old root index.html and board.js (git history keeps them). Keep Code/, License.txt,
   20x20.PNG only if still used (the README image may be replaced by a screenshot of the new demo).
3. Keep old links alive: bounds-2026/demo/ (and its ?metric=... params) must redirect to the root URL with the same query
   (a tiny index.html with a JS/meta redirect). Old root URL /index.html keeps working (it is the new demo).
4. Update every link to the demo: both posts (DemoEmbed src/href + text links -> root URL with ?metric=...), root README,
   bounds-2026/README.md, demo/README.md. NOTE: Nil is editing the posts; change ONLY the demo URLs there and report the lines.
5. Research files stay in bounds-2026/ (only the demo URL moves); I tell Nil this and he may ask otherwise.
6. node check.js, real-browser check of the root page (all steps, T/X, downloads, embed mode), push, Pages build, report URLs
   with HTTP codes and the feature comparison.
