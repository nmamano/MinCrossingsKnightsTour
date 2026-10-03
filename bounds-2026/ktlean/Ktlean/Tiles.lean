import Mathlib

/-!
# Knight tiles: the finite geometric lemma

Each unit square `[i, i+1] × [j, j+1]` is cut by its two diagonals into four quarter triangles,
labelled `(i, j, k)` with `k = 0, 1, 2, 3` for the bottom, right, top and left triangle.
The tile of a knight edge from `a` to `a + d` is a set of four quarter triangles
(`tri a d`). The proof below uses only these finite facts:

* each tile has 4 quarter triangles, all inside the bounding box of the edge;
* the tiles of two distinct edges share at most 2 quarter triangles, and they share one only if
  the two edges cross properly.
-/

open Finset

namespace KT

/-- A lattice point. -/
abbrev Pt := ℤ × ℤ

/-- A quarter triangle `(i, j, k)`. -/
abbrev QTri := ℤ × ℤ × Fin 4

/-- The eight knight vectors. -/
def knightVecs : Finset Pt :=
  {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}

/-- The tile of the knight edge from `(0, 0)` to `d`. -/
def tri0 : Pt → Finset QTri
  | (1, 2) => {(0, 0, 2), (0, 0, 3), (0, 1, 0), (0, 1, 1)}
  | (1, -2) => {(0, -2, 1), (0, -2, 2), (0, -1, 0), (0, -1, 3)}
  | (-1, 2) => {(-1, 0, 1), (-1, 0, 2), (-1, 1, 0), (-1, 1, 3)}
  | (-1, -2) => {(-1, -2, 2), (-1, -2, 3), (-1, -1, 0), (-1, -1, 1)}
  | (2, 1) => {(0, 0, 0), (0, 0, 1), (1, 0, 2), (1, 0, 3)}
  | (2, -1) => {(0, -1, 1), (0, -1, 2), (1, -1, 0), (1, -1, 3)}
  | (-2, 1) => {(-2, 0, 1), (-2, 0, 2), (-1, 0, 0), (-1, 0, 3)}
  | (-2, -1) => {(-2, -1, 0), (-2, -1, 1), (-1, -1, 2), (-1, -1, 3)}
  | _ => ∅

/-- Translation of a quarter triangle by the vector `a`. -/
def shift (a : Pt) (t : QTri) : QTri := (t.1 + a.1, t.2.1 + a.2, t.2.2)

lemma shift_injective (a : Pt) : Function.Injective (shift a) := by
  intro s t h
  simp only [shift, Prod.mk.injEq, add_left_inj] at h
  exact Prod.ext h.1 (Prod.ext h.2.1 h.2.2)

/-- The tile of the knight edge from `a` to `a + d`. -/
def tri (a d : Pt) : Finset QTri := (tri0 d).image (shift a)

/-- Orientation determinant of the points `a, b, c`. -/
def det (a b c : Pt) : ℤ := (b.1 - a.1) * (c.2 - a.2) - (b.2 - a.2) * (c.1 - a.1)

/-- The segments `ab` and `cd` cross properly: `c, d` are strictly on opposite sides of the line
`ab`, and `a, b` are strictly on opposite sides of the line `cd`. -/
def ProperCross (a b c d : Pt) : Prop := det a b c * det a b d < 0 ∧ det c d a * det c d b < 0

instance (a b c d : Pt) : Decidable (ProperCross a b c d) := by
  unfold ProperCross; infer_instance

lemma tri0_card : ∀ d ∈ knightVecs, (tri0 d).card = 4 := by decide

lemma tri0_bounds : ∀ d ∈ knightVecs, ∀ t ∈ tri0 d,
    min 0 d.1 ≤ t.1 ∧ t.1 < max 0 d.1 ∧ min 0 d.2 ≤ t.2.1 ∧ t.2.1 < max 0 d.2 := by decide

/-- The finite certificate, for one edge from the origin and a second edge with its start in
`[-3, 3]²`. -/
lemma tri0_inter_le : ∀ x ∈ Icc (-3 : ℤ) 3, ∀ y ∈ Icc (-3 : ℤ) 3, ∀ d ∈ knightVecs,
    ∀ e ∈ knightVecs,
    ¬ (((0 : Pt) = (x, y) ∧ d = (x, y) + e) ∨ ((0 : Pt) = (x, y) + e ∧ d = (x, y))) →
    (tri0 d ∩ tri (x, y) e).card ≤
      2 * (if ProperCross 0 d (x, y) ((x, y) + e) then 1 else 0) := by
  decide +kernel

end KT
