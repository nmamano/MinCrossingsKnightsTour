Chief Researcher -> KT Integrator (2026-10-03): Nil's feedback on the blog posts. Nil is ALSO editing these two files in his editor,
so make only the minimal insertions below, in one quick pass, and report the exact changed lines (he will reload).
1. Link to the paper at its FIRST mention in each post: https://arxiv.org/abs/1904.02824 . Turns post: line ~19 "At the end of the
   paper," -> "At the end of the [paper](https://arxiv.org/abs/1904.02824),". Crossings post: the first body mention of "the paper"
   (grep; around line 62 "In the paper's tours") gets the same link. Change nothing else in the sentence.
2. Show the heel picture where "heel" is first mentioned. Turns post: first mention is in the list around line 46 (the optimized
   heels have 21 turns per 8 columns, after Parker's improvement); there is no heel picture in that post. Insert a BlogImage right
   after that list: a figure of the paper's optimized heel (21 turns per 8 columns; your reconstruction gadgets/heel21.json, audited
   in Claim 22), drawn in the same style as the post's other figures (white background, dark text #22303a, turns marked), saved in
   writeup/turns/images/ and served as /blog/knights-tour-turns/<name>.png, with a short plain caption. Crossings post: heels.png
   already follows the first mention; check that it is right after the first mention, else move nothing and tell me.
3. "Avoid light gray text on white. That's an issue on the lower bound proof." Find which text in the crossings post's lower-bound
   part renders light gray on white (figure labels in writeup/crossings/figures/lower_figs.py use GREY #9aa5b1 / DIM #5a6872, or
   site styling of code / details / captions): take a headless screenshot of that section of the preview
   (http://127.0.0.1:21019/blog/knights-tour-crossings), identify it, and fix it: figures -> re-render with text in #22303a (or at
   least #3d4a55); if it is site CSS, do NOT edit the site; tell me what it is.
Check the MDX compile and the preview (200) after the edits. Do not push (held milestone).
