import Ktlean.Tour

/-!
# A sanity check: an explicit closed tour of the 8 × 8 board

This file shows that the structure `ClosedTour` is not empty (so the main theorem is not
vacuous), and that `numTurns` counts what we expect: this tour has 61 turns, the same count
as an independent Python check. The main theorem gives `8 * 8 - 64 = 0 ≤ 61`.
-/

namespace KT.Example

/-- The cells of the tour, in order. -/
def tourCells : Fin 64 → Cell 8 :=
  ![(0, 0), (1, 2), (0, 4), (1, 6), (3, 7), (5, 6), (7, 7), (6, 5),
    (5, 7), (7, 6), (6, 4), (7, 2), (6, 0), (4, 1), (2, 0), (0, 1),
    (1, 3), (0, 5), (1, 7), (2, 5), (0, 6), (2, 7), (4, 6), (6, 7),
    (7, 5), (6, 3), (7, 1), (5, 0), (6, 2), (7, 0), (5, 1), (3, 0),
    (1, 1), (0, 3), (1, 5), (0, 7), (2, 6), (4, 7), (6, 6), (7, 4),
    (5, 5), (3, 6), (4, 4), (3, 2), (2, 4), (4, 5), (5, 3), (3, 4),
    (2, 2), (4, 3), (3, 5), (1, 4), (3, 3), (5, 4), (7, 3), (6, 1),
    (4, 2), (2, 3), (0, 2), (1, 0), (3, 1), (5, 2), (4, 0), (2, 1)]

/-- The position of each cell `(x, y)` in the tour. -/
def tourIndex (c : Cell 8) : Fin 64 :=
  !![0, 15, 58, 33, 2, 17, 20, 35;
    59, 32, 1, 16, 51, 34, 3, 18;
    14, 63, 48, 57, 44, 19, 36, 21;
    31, 60, 43, 52, 47, 50, 41, 4;
    62, 13, 56, 49, 42, 45, 22, 37;
    27, 30, 61, 46, 53, 40, 5, 8;
    12, 55, 28, 25, 10, 7, 38, 23;
    29, 26, 11, 54, 39, 24, 9, 6] c.1 c.2

/-- An explicit closed knight's tour of the 8 × 8 board. -/
def tour8 : ClosedTour 8 where
  cell := ⟨tourCells, tourIndex, by decide +kernel, by decide +kernel⟩
  isKnightMove := by decide +kernel

theorem tour8_numTurns : tour8.numTurns = 61 := by decide +kernel

end KT.Example
