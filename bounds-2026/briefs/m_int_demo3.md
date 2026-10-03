Chief Researcher -> KT Integrator (2026-10-03): demo feedback from Nil (he looked at it on Windows). Please implement all five,
then node demo/check.js, restart knight-demo, verify in a real browser render (screenshot via the office preview if you can), and
push to Pages (this is a demo change; you may push it on its own, separate from the held post milestone).
1. Default n: when a step (construction) is selected, start at the SMALLEST valid n for that step (48 where valid), since small
   boards are easiest to see.
2. Turns chart label "6n reference (paper asymptotic coefficient)" confused Nil. It is the paper's turns lower bound (6 - eps)n.
   Relabel in plain words, e.g. "6n: the paper's lower bound on turns (leading term)", and the caption to match. Same plain
   style for the crossings labels ("4n: the paper's lower bound", "5n: new lower bound, Oct 3").
3. BUG?: switching between the Parker Williams step (12n) and the Shisheng Li step (11.5n) does not change the crossing count.
   Find out why (same data served? a residue where both coincide? wrong file mapping?) and fix it, or explain in one line if
   both really give the same count at the shown n (then say so on the page).
4. State the constraints on n for each step clearly on the page: minimum n, and which n are allowed (even only, residues mod
   4/8/24, etc.), next to the n control.
5. Faint checkerboard under the tour: very low contrast, drawn only when squares are large enough on screen (e.g. >= 6 px),
   with a toggle (on by default if it looks clean, else off). Keep it readable in dark and light mode.
Report what changed, the cause of item 3, and the URLs with HTTP codes.
