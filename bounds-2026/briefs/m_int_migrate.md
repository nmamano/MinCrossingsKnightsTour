Chief Researcher -> KT Integrator (2026-10-03). You are in a FRESH session. Context: Research Lab, knight's tour bounds
research (root ~/nil/knight-formation-research; index RESULTS.md; your past notes w-integrator/FINDINGS.md, incl. section
"Public repo sync recipe"). Our public repo so far: https://github.com/nmamano/knights-tour-bounds (staging clone
~/nil/knights-tour-bounds, main at b42135b, pushed). Both blog drafts (writeup/turns/post.mdx, writeup/crossings/post.mdx)
are audited and final (Claims 23A/23B).

NIL'S ORDER (2026-10-03): take over his older repo https://github.com/nmamano/MinCrossingsKnightsTour (code for the
original paper; default branch master; MIT License.txt "Copyright (c) 2019 Nil Mamano"; GitHub Pages serves master "/" at
https://nmamano.github.io/MinCrossingsKnightsTour/ with index.html + board.js, the old demo) and put ALL our work online
through it. You may push directly to master as Nil. No branches, no PRs.

Task:
1. Clone it to ~/nil/MinCrossingsKnightsTour (path is free as of now; check again).
2. Import knights-tour-bounds WITH its history into the subfolder bounds-2026/ (git subtree add --prefix=bounds-2026
   ~/nil/knights-tour-bounds main, no --squash). Do not move, rename or change any old file except README.md; the old
   Pages demo must keep working at the same URL.
3. The root .gitignore ignores *.log, *.aux, *.out, *.toc: tracked files stay, but future syncs would drop new audit
   logs. Add bounds-2026/.gitignore that re-includes what the research tree needs (e.g. !*.log), so the tracked set after
   a fresh sync equals what the old recipe gave. Verify with git ls-files counts.
4. Root README.md: keep the old text; add a short section at the top: 2026 new bounds on crossings and turns (one line
   each with the bounds from RESULTS.md), a link to bounds-2026/ (its README is the entry point) and to the interactive
   demo (step 6). Plain, factual, no hype; no claims beyond RESULTS.md. bounds-2026/README.md: replace "TODO: license
   (Nil)" with a pointer to the root MIT License.txt.
5. Update both posts in the RESEARCH dir (not only in the repo): every link to knights-tour-bounds becomes
   https://github.com/nmamano/MinCrossingsKnightsTour/tree/master/bounds-2026 , and wording like "from the repo/project
   root" becomes "from the bounds-2026 folder of the repository". Change nothing else. Keep the MDX compile OK
   (node writeup/crossings/check_mdx.mjs; the live preview http://127.0.0.1:21019/blog/... must return 200). Send me the
   exact list of changed lines.
6. Demo: if demo/ is a static site (no server logic), make it work under GitHub Pages at
   https://nmamano.github.io/MinCrossingsKnightsTour/bounds-2026/demo/ (relative paths; no office URLs; same content as the
   audited Claim 22 version). If it needs a server, do not publish it; report what it needs.
7. New sync recipe: research dir -> ~/nil/MinCrossingsKnightsTour/bounds-2026/ with the SAME excludes as before (incl.
   writeup/WRITER_STATE.md, w-verifier/claim23*_clean/, CR_STATE.md, .venv, ktlean/.lake + .git, paper.pdf/txt,
   board-patched.js, *.npy, compiled C++ binaries, claim22 extracts; office URL replaced in w-integrator/FINDINGS.md).
   A new folder gap/ (speculative research, starting now) IS included. Write the recipe in w-integrator/FINDINGS.md.
8. Re-sync once with the new recipe (it picks up the post link edits), run all 13 appendix commands from a git-ls-files
   copy of bounds-2026/ with system python3 (as you did for b42135b), privacy scan, then commit and push to master.
9. Do NOT archive or delete knights-tour-bounds. Prepare (do not push) a one-commit README pointer for it ("moved to
   MinCrossingsKnightsTour/bounds-2026") and tell me; Nil decides archive vs keep.
Report: commit hashes, Pages demo URL status (HTTP code after the Pages build), command run summary, privacy scan.
One or two CPU cores; other agents run research jobs. Hand off at ~50% context with state in w-integrator/FINDINGS.md.
