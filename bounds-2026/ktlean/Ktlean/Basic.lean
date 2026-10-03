import Mathlib

/-!
# Definitions: knight moves, 2-factors, closed tours, turns

A cell of the `n × n` board is a pair `(x, y)` with `x y : Fin n` (column `x`, row `y`).
-/

open Finset

namespace KT

/-- The cells of the `n × n` board: `(x, y)` is the cell in column `x` and row `y`. -/
abbrev Cell (n : ℕ) := Fin n × Fin n

variable {n : ℕ}

/-- The displacement vector from cell `u` to cell `v`, in integer coordinates. -/
def disp (u v : Cell n) : ℤ × ℤ := ((v.1 : ℤ) - u.1, (v.2 : ℤ) - u.2)

/-- A knight vector: one coordinate is `±1` and the other is `±2`. -/
def IsKnightVec (d : ℤ × ℤ) : Prop :=
  (|d.1| = 1 ∧ |d.2| = 2) ∨ (|d.1| = 2 ∧ |d.2| = 1)

instance (d : ℤ × ℤ) : Decidable (IsKnightVec d) := by unfold IsKnightVec; infer_instance

/-- Cells `u` and `v` are a knight's move apart. -/
def IsKnightMove (u v : Cell n) : Prop := IsKnightVec (disp u v)

instance (u v : Cell n) : Decidable (IsKnightMove u v) := by
  unfold IsKnightMove; infer_instance

/-- A 2-factor of the knight's graph: every cell has exactly two chosen neighbours, each a
knight's move away, and the relation "is a chosen neighbour of" is symmetric.
(A closed knight's tour is a 2-factor with a single cycle.) -/
structure TwoFactor (n : ℕ) where
  /-- The two chosen neighbours of each cell. -/
  nbrs : Cell n → Finset (Cell n)
  card_nbrs : ∀ v, (nbrs v).card = 2
  isKnightMove : ∀ v, ∀ u ∈ nbrs v, IsKnightMove v u
  symm : ∀ v u, u ∈ nbrs v → v ∈ nbrs u

/-- A cell `v` is a turn of the 2-factor `F` if its two moves are not opposite, that is,
there are no chosen neighbours `u, w` of `v` with `u - v = -(w - v)`. -/
def TwoFactor.IsTurn (F : TwoFactor n) (v : Cell n) : Prop :=
  ¬ ∃ u ∈ F.nbrs v, ∃ w ∈ F.nbrs v, disp v u = - disp v w

open Classical in
/-- The number of turns of a 2-factor. -/
noncomputable def TwoFactor.numTurns (F : TwoFactor n) : ℕ :=
  (univ.filter F.IsTurn).card

/-- The cell `v` as a point of the real plane `ℝ²`. -/
def toPlane (v : Cell n) : ℝ × ℝ := ((v.1 : ℝ), (v.2 : ℝ))

/-- The open segments `(a, b)` and `(c, d)` of the real plane intersect. -/
def OpenSegmentsMeet (a b c d : Cell n) : Prop :=
  (openSegment ℝ (toPlane a) (toPlane b) ∩ openSegment ℝ (toPlane c) (toPlane d)).Nonempty

/-- The graph of a 2-factor: `u` and `v` are adjacent if `v` is a chosen neighbour of `u`. -/
def TwoFactor.graph (F : TwoFactor n) : SimpleGraph (Cell n) where
  Adj u v := v ∈ F.nbrs u
  symm := ⟨fun u v h => F.symm u v h⟩
  loopless := ⟨fun v h => by
    have := F.isKnightMove v v h
    simp [IsKnightMove, IsKnightVec, disp] at this⟩

/-- Two edges `e` and `f` (unordered pairs of cells) cross: their open segments intersect. -/
def EdgesCross (e f : Sym2 (Cell n)) : Prop :=
  ∃ a b c d, e = s(a, b) ∧ f = s(c, d) ∧ OpenSegmentsMeet a b c d

open Classical in
/-- The number of crossings of a 2-factor: the number of sets `{e, f}` of two distinct edges
whose open segments intersect (Definition 2 of the paper). -/
noncomputable def TwoFactor.numCrossings (F : TwoFactor n) : ℕ :=
  ((F.graph.edgeFinset.powersetCard 2).filter fun P =>
    ∃ e ∈ P, ∃ f ∈ P, e ≠ f ∧ EdgesCross e f).card

/-- Three cells `a, b, c` are collinear: the cross product of `b - a` and `c - a` is zero. -/
def Collinear3 (a b c : Cell n) : Prop :=
  (disp a b).1 * (disp a c).2 - (disp a b).2 * (disp a c).1 = 0

instance (a b c : Cell n) : Decidable (Collinear3 a b c) := by unfold Collinear3; infer_instance

/-- A closed knight's tour of the `n × n` board: an enumeration `cell 0, cell 1, …,
cell (n*n - 1)` of all the cells, each cell exactly once, such that each cell and the next
one are a knight's move apart. "Next" is cyclic (`finRotate` maps `i` to `i + 1` and the last
index to `0`), so the last cell is also a knight's move away from the first cell. -/
structure ClosedTour (n : ℕ) where
  /-- `cell i` is the `i`-th cell of the tour. -/
  cell : Fin (n * n) ≃ Cell n
  isKnightMove : ∀ i, IsKnightMove (cell i) (cell (finRotate _ i))

/-- The tour has a turn at its `i`-th cell if the previous, the current and the next cell of
the tour are not collinear (Definition 1 of Besa–Johnson–Mamano–Osegueda–Williams). -/
def ClosedTour.IsTurn (T : ClosedTour n) (i : Fin (n * n)) : Prop :=
  ¬ Collinear3 (T.cell ((finRotate _).symm i)) (T.cell i) (T.cell (finRotate _ i))

instance (T : ClosedTour n) : DecidablePred T.IsTurn := fun i => by
  unfold ClosedTour.IsTurn; infer_instance

/-- The number of turns of a closed tour. -/
def ClosedTour.numTurns (T : ClosedTour n) : ℕ :=
  (univ.filter T.IsTurn).card

open Classical in
/-- The number of crossings of a closed tour: the number of pairs of positions `i < j` such that
the open segments of the moves `cell i → cell (i + 1)` and `cell j → cell (j + 1)` intersect
(Definition 2 of the paper). -/
noncomputable def ClosedTour.numCrossings (T : ClosedTour n) : ℕ :=
  (univ.filter fun p : Fin (n * n) × Fin (n * n) => p.1 < p.2 ∧
    OpenSegmentsMeet (T.cell p.1) (T.cell (finRotate _ p.1))
      (T.cell p.2) (T.cell (finRotate _ p.2))).card

end KT
