import Ktlean.Overlap

/-!
# The four frames of the board

Frame `k` is the board rotated `k` times by a quarter turn (`rotPt n`). Column 0 of frame `k` is
side `k` of the board (left, top, right, bottom for `k = 0, 1, 2, 3`). This file gives:

* `rotPt_iter_four`, `rotL_iter_four`: four quarter turns are the identity;
* `rowB_of_rowL`: a critical row `n - 2 - R` on column 0 of a frame gives the bottom hypothesis of
  `corner_charge_row` at column `R` in the next frame (the critical sets correspond, `P ↔ P'`);
* the rotation of quarter triangles (`rotTri`) and unit squares (`rotSq`), the rotation of tiles
  (`mem_tri_rot`), and the squares beside a rotated grid edge (`besideSq_rotE`).
-/

open Finset

namespace KT

lemma rotPt_iter_four (n : ℤ) (p : Pt) : (rotPt n)^[4] p = p := by
  simp only [Function.iterate_succ, Function.iterate_zero, Function.comp_apply, id, rotPt]
  ext <;> simp

lemma rotL_iter_four (d : Pt) : rotL^[4] d = d := by
  simp only [Function.iterate_succ, Function.iterate_zero, Function.comp_apply, id, rotL]
  ext <;> simp

/-! ### Critical rows of one frame give the bottom hypothesis of the next frame -/

/-- The correspondence of canonical left edges (relative to row `n - 2 - R`) with canonical
bottom edges of the next frame (relative to column `R`). -/
def Tmap (e : Pt × Pt) : Pt × Pt := ((1 - e.1.2 - e.2.2, e.1.1 + e.2.1), (e.2.2, -e.2.1))

lemma Tmap_injective : Function.Injective Tmap := by
  rintro ⟨⟨a, b⟩, ⟨c, e⟩⟩ ⟨⟨a', b'⟩, ⟨c', e'⟩⟩ h
  simp only [Tmap, Prod.mk.injEq] at h
  ext <;> simp <;> omega

lemma canon_snd_pos {d : Pt} (hd : d ∈ knightVecs) (p : Pt) : 0 < (canon Prod.snd p d).2.2 := by
  have : d.2 ≠ 0 := by
    simp only [knightVecs, mem_insert, mem_singleton] at hd
    rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide
  unfold canon; split_ifs with h
  · exact h
  · simp only [Prod.snd_neg]; omega

lemma Tmap_canon {d : Pt} (hd : d ∈ knightVecs) (n R : ℤ) (p : Pt) :
    canon Prod.fst (rotPt n p - (R, 0)) (rotL d) =
      Tmap (canon Prod.snd (p - (0, n - 2 - R)) d) := by
  have : d.2 ≠ 0 := by
    simp only [knightVecs, mem_insert, mem_singleton] at hd
    rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide
  unfold canon Tmap rotPt rotL
  simp only
  split_ifs with h1 h2 h2 <;> first | omega | ((ext <;> simp); ring)

lemma stradB_Tmap (e : Pt × Pt) : StradB (Tmap e) ↔ StradL e := by
  unfold StradB StradL Tmap
  simp only
  omega

lemma PL_image_Tmap : ∀ s ∈ ({1, -1} : Finset ℤ), (PL s).image Tmap = PB (-s) := by
  decide +kernel

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

lemma rowB_of_rowL (hd : ∀ i, d i ∈ knightVecs) (n R s : ℤ) (hs : s ∈ ({1, -1} : Finset ℤ))
    (hrow : (univ.filter fun i => StradL (canon Prod.snd (a i - (0, n - 2 - R)) (d i))).image
      (fun i => canon Prod.snd (a i - (0, n - 2 - R)) (d i)) = PL s) :
    (univ.filter fun i => StradB (canon Prod.fst (rotPt n (a i) - (R, 0)) (rotL (d i)))).image
      (fun i => canon Prod.fst (rotPt n (a i) - (R, 0)) (rotL (d i))) = PB (-s) := by
  simp only [Tmap_canon (hd _), stradB_Tmap]
  have e : (fun i => Tmap (canon Prod.snd (a i - (0, n - 2 - R)) (d i))) =
      Tmap ∘ (fun i => canon Prod.snd (a i - (0, n - 2 - R)) (d i)) := rfl
  rw [e, ← image_image, hrow, PL_image_Tmap s hs]

end Family

/-! ### Rotation of quarter triangles and unit squares -/

/-- The quarter turn of a quarter triangle: the square `(x, y)` goes to `(n - 2 - y, x)`, and the
bottom/right/top/left quarter goes to the right/top/left/bottom quarter. -/
def rotTri (n : ℤ) (t : QTri) : QTri := (n - 2 - t.2.1, t.1, t.2.2 + 1)

/-- The quarter turn of a unit square (given by its lower-left corner). -/
def rotSq (n : ℤ) (s : Pt) : Pt := (n - 2 - s.2, s.1)

lemma rotTri_injective (n : ℤ) : Function.Injective (rotTri n) := by
  rintro ⟨x, y, q⟩ ⟨x', y', q'⟩ h
  simp only [rotTri, Prod.mk.injEq, add_left_inj] at h
  ext <;> simp <;> omega

lemma sqOf_rotTri (n : ℤ) (t : QTri) : sqOf (rotTri n t) = rotSq n (sqOf t) := rfl

def rotTri0 (t : QTri) : QTri := (-1 - t.2.1, t.1, t.2.2 + 1)

lemma tri0_rotL : ∀ d ∈ knightVecs, tri0 (rotL d) = (tri0 d).image rotTri0 := by decide

lemma tri_rot {d : Pt} (hd : d ∈ knightVecs) (n : ℤ) (p : Pt) :
    tri (rotPt n p) (rotL d) = (tri p d).image (rotTri n) := by
  rw [tri, tri, tri0_rotL d hd, image_image, image_image]
  congr 1
  funext t
  simp only [Function.comp, shift, rotTri0, rotTri, rotPt, Prod.mk.injEq]
  exact ⟨by ring, trivial⟩

lemma mem_tri_rot {d : Pt} (hd : d ∈ knightVecs) (n : ℤ) (p : Pt) (t : QTri) :
    rotTri n t ∈ tri (rotPt n p) (rotL d) ↔ t ∈ tri p d := by
  rw [tri_rot hd, (rotTri_injective n).mem_finset_image]

/-- The two unit squares beside a grid edge. -/
def besideSq (q : GridEdge) : Finset Pt := {sqOf (nearLo q), sqOf (nearHi q)}

lemma besideSq_rotE (n : ℤ) (q : GridEdge) :
    besideSq (rotE n q) = (besideSq q).image (rotSq n) := by
  obtain ⟨⟨x, y⟩, v⟩ := q
  ext ⟨u, w⟩
  cases v <;> simp only [besideSq, rotE, nearLo, nearHi, sqOf, rotSq, rotPt, Bool.false_eq_true,
    ite_false, ite_true, image_insert, image_singleton, mem_insert, mem_singleton,
    Prod.mk.injEq, Prod.fst_sub, Prod.snd_sub] <;> constructor <;> intro h <;> omega

lemma besideSq_rotE_iter (n : ℤ) (k : ℕ) (q : GridEdge) :
    besideSq ((rotE n)^[k] q) = (besideSq q).image (rotSq n)^[k] := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply', besideSq_rotE, ih, image_image,
      Function.iterate_succ']

lemma mem_tri_rot_iter {d : Pt} (hd : d ∈ knightVecs) (n : ℤ) (k : ℕ) (p : Pt) (t : QTri) :
    (rotTri n)^[k] t ∈ tri ((rotPt n)^[k] p) (rotL^[k] d) ↔ t ∈ tri p d := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [Function.iterate_succ_apply']
    rw [mem_tri_rot (rotL_iter_mem hd k), ih]

lemma sqOf_rotTri_iter (n : ℤ) (k : ℕ) (t : QTri) :
    sqOf ((rotTri n)^[k] t) = (rotSq n)^[k] (sqOf t) := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [Function.iterate_succ_apply', sqOf_rotTri, ih]

end KT
