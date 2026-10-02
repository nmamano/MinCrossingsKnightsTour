# Knight formation research — parked

Nil parked this project on 2026-09-21. Resume only when Nil asks.

## Objective

Find a new knight formation configuration with provably fewer turns or crossings. Start with Nil's idea: permit the four knights to change order within a heel or a group of heels, and investigate whether corners can restore tour connectivity at constant cost. Other formation-based approaches are allowed. Nil requested extensive parallel agent work.

## Sources saved

- `paper.pdf`: https://arxiv.org/pdf/1904.02824 (latest version requested).
- `board-original.js`: https://raw.githubusercontent.com/nmamano/MinCrossingsKnightsTour/master/board.js
- `board-patched.js`: https://raw.githubusercontent.com/daizisheng/MinCrossingsKnightsTour/master/board.js
- Demo: https://daizisheng.github.io/MinCrossingsKnightsTour/index.html

Shisheng Li's email says a 4x40 template replaces five Sequence1 templates while preserving boundary edges, endpoints, and internal path pairing. It claims 130 crossings and an 11.5n asymptotic coefficient. Nil proposes relaxing the pairing constraint and repairing at corners with O(1) extra work. Email and full user instructions are in Game Maker's chat immediately before the pause.

## State at pause

Only the source downloads and initial inspection are complete. No search results, new configuration, or verified proof exist. One proof subagent was started and then interrupted at Nil's request. No dependencies were installed and no app was registered. The round-trip-chess repo had existing uncommitted changes; we did not edit it.

The subagent reported, but the parent has NOT independently checked: the patched JS distinguishes the original demo's 32-crossing heel (13n) from the paper's 28-crossing heel (12n). On that account, the 130-crossing block saves 10 against five paper heels, yielding 11.5n. Check this distinction before comparing results. The subagent also suggested that preserving a positional matching H may suffice instead of full path pairing; this remains an unverified lead.

## Resume steps

1. Read the paper and patch; establish the exact baseline, boundary conditions, and crossing convention.
2. Resolve the pending request to install OR-Tools and pypdf in a virtual environment here. Nil did not answer before parking. Python 3 is available; pypdf, fitz, ortools, scipy, and pdftotext were absent at the initial check.
3. Split work among configuration search, composition proof, and independent verification. Keep each agent's files separate.
4. Check candidate edges, coverage, path components, boundary interfaces, crossings, turns, and global tour connectivity. Save explicit certificates and a proof before claiming an improvement.

No commit or push was made.
