Chief Researcher -> KT Integrator: NEW MISSION from Nil (2026-10-02): an INTERACTIVE DEMO of our constructions.
Nil's words: "interactive demos where a user can see the different layouts and change board dimensions and see how it changes".
You are at ~41% context: first record anything a fresh session needs in w-integrator/FINDINGS.md, then POST your own /handoff
with this brief (shortened as you see fit).
What to build (demo/ under the research dir; do NOT touch ~/nil/nilmamano.com):
- A self-contained static web page (HTML + JS, no framework build step, so it can later be embedded in Nil's Next.js blog).
- Constructions to choose from: paper heel (12n crossings / 9.25n turns as in the paper), H16a (9n crossings), FOLD (19n/3
  crossings, the best), TT16 (8n - 14 turns, the best). Optional: lane-free LF4 (343n/48).
- A board-size control (even n over the range each construction supports, e.g. 48..200; fold from 96). The tour redraws.
- Display: the tour on a canvas; toggles to highlight crossings (red dots) and turns; colour moves by direction (as in
  explain/folds.png); an overlay of the layout (edge bands, corners, the 8 fold triangles, diagonal corridors); live counts
  next to the formula (e.g. "X = 720 = 19n/3 + 112"); zoom into an edge band.
- Data: precompute tours in Python for every supported n and export compact JSON (lazy-loaded per n), OR generate in JS from
  templates + per-residue corner/base data. Your choice; correctness first: every exported tour must pass kt.core.validate, and
  the counts shown must equal an independent count.
- Run it as an isomux app (POST localhost:4000/api/apps, name "knight-demo", a static server that listens on $PORT and binds
  $ISOMUX_APP_HOST) so Nil can open it. Report the URL to me.
Style: clean, light, readable on a laptop; short plain-English captions for each construction ("why it works" in 2-3 lines).
KT Structures is making the fold illustrations; reuse its colours if they are ready. Ask me if a product choice is unclear.
