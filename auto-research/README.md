# auto-research/

Shared results from agents working on this repository, including failed experiments and negative results.
Read [../auto-research.md](../auto-research.md) first. It describes the problem, the current bounds, and how
to verify a claim.

## Layout

One subfolder per research track:

| Folder | Track |
| --- | --- |
| [crossings-upper/](crossings-upper/) | Tours with fewer than 19n/3 + O(1) crossings. |
| [crossings-lower/](crossings-lower/) | A crossings lower bound above 5n - O(1). |
| [crossings-5n-review/](crossings-5n-review/) | Independent review or simplification of the tentative 5n - 597 proof. |
| [turns-constant/](turns-constant/) | The additive constant c in T_min(n) = 8n - c. |
| [formalization/](formalization/) | Lean proofs of bounds that are not formalized yet. |

Each track folder has a README with context and known dead ends. Read it, and the notes already in the
folder, before you start.

## One result per entry

- A single note: `<track>/YYYY-MM-DD-<handle>-<short-slug>.md`
- A note with code or data: `<track>/YYYY-MM-DD-<handle>-<short-slug>/README.md`, plus its files
  (for example `code/`, `data/`, `check.py`).

Use the date you finish, your GitHub handle, and a slug of a few words. Do not edit another contributor's entry.
To correct or extend it, add a new entry that links to it.

The note must state: the base commit, the question and approach, the outcome (positive, negative or
inconclusive, with a status label per claim: PROVEN, CERTIFIED, ARGUMENT or CONJECTURE), the models and harness,
the cost if known, and one reproducible command with its expected output. See
[../auto-research.md](../auto-research.md), section "How to share results", for the full list.

## Relation to bounds-2026/

[../bounds-2026/](../bounds-2026/) is the record of the 2026 agent session. Its check commands pin paths in that
folder, so leave it as it is. New work goes here. If a result is accepted, the maintainer adds it to
[../bounds-2026/RESULTS.md](../bounds-2026/RESULTS.md).
