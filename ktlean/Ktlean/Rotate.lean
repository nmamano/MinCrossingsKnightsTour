import Ktlean.CornerRow

/-!
# Rotation of the board by a quarter turn

`rotPt n (x, y) = (n - 1 - y, x)` maps the board `[0, n-1]²` to itself. Knight vectors rotate
by `rotL (dx, dy) = (-dy, dx)`. A grid edge `q` maps to the grid edge `rotE n q`; the flux and
`ω = flux + χ` change only by a sign.
-/

open Finset

namespace KT

/-- The quarter turn of the board `[0, n-1]²`. -/
def rotPt (n : ℤ) (p : Pt) : Pt := (n - 1 - p.2, p.1)

/-- The quarter turn of vectors. -/
def rotL (d : Pt) : Pt := (-d.2, d.1)

/-- The image of a grid edge. A horizontal edge becomes vertical with the same direction; a
vertical edge becomes horizontal with the opposite direction. -/
def rotE (n : ℤ) (q : GridEdge) : GridEdge :=
  if q.2 then (rotPt n q.1 - (1, 0), false) else (rotPt n q.1, true)

lemma rotPt_add (n : ℤ) (p d : Pt) : rotPt n (p + d) = rotPt n p + rotL d := by
  ext <;> simp only [rotPt, rotL, Prod.fst_add, Prod.snd_add]
  ring

lemma rotL_mem {d : Pt} (hd : d ∈ knightVecs) : rotL d ∈ knightVecs := by
  simp only [knightVecs, mem_insert, mem_singleton] at hd
  rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

lemma pathSign_rot_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs,
    ∀ v : Bool, pathSign (rotL (x, y) + (if v then (1, 0) else 0)) (rotL d) ((0, 0), !v) =
      (if v then -1 else 1) * pathSign (x, y) d ((0, 0), v) := by
  decide +kernel

lemma rotPt_sub (n : ℤ) (p a : Pt) : rotPt n p - rotPt n a = rotL (p - a) := by
  ext <;> simp only [rotPt, rotL, Prod.fst_sub, Prod.snd_sub]
  ring

lemma rotPt_injective (n : ℤ) : Function.Injective (rotPt n) := by
  intro p r h
  simp only [rotPt, Prod.mk.injEq] at h
  ext <;> omega

lemma chi_rot (n : ℤ) (p : Pt) : chi (rotPt n p) = chi (n - 1, 0) * chi p := by
  unfold chi rotPt
  simp only
  split_ifs <;> omega

/-- The lattice path of a knight edge meets the grid edges at the origin only from nearby. -/
lemma pathSign_zero {d : Pt} (hd : d ∈ knightVecs) (r : Pt) (v : Bool)
    (h : ¬ (-1 ≤ r.1 ∧ r.1 ≤ 2 ∧ -1 ≤ r.2 ∧ r.2 ≤ 2)) : pathSign r d ((0, 0), v) = 0 := by
  have hb := mid_bounds hd
  have z : ∀ u w : Pt, ¬ (0 ≤ u.1 ∧ u.1 ≤ 1 ∧ 0 ≤ u.2 ∧ u.2 ≤ 1) →
      stepSign u w ((0, 0), v) = 0 := fun u w hu => by
    by_contra h; exact hu (stepSign_ne_zero h)
  unfold pathSign
  rw [z, z, z] <;> (try simp only [Prod.fst_add, Prod.snd_add]) <;> omega

lemma pathSign_rot {d : Pt} (hd : d ∈ knightVecs) (r : Pt) (v : Bool) :
    pathSign (rotL r + (if v then (1, 0) else 0)) (rotL d) ((0, 0), !v) =
      (if v then -1 else 1) * pathSign r d ((0, 0), v) := by
  by_cases hn : r.1 ∈ Icc (-4 : ℤ) 4 ∧ r.2 ∈ Icc (-4 : ℤ) 4
  · have := pathSign_rot_rel r.1 hn.1 r.2 hn.2 d hd v
    rwa [Prod.mk.eta] at this
  · simp only [mem_Icc] at hn
    rw [pathSign_zero hd r v (by omega), pathSign_zero (rotL_mem hd)]
    · ring
    · cases v <;> simp [rotL] <;> omega

/-- The sign of the image of a grid edge: `-1` for vertical, `1` for horizontal. -/
def rotSgn (q : GridEdge) : ℤ := if q.2 then -1 else 1

lemma flux1_rot {d : Pt} (hd : d ∈ knightVecs) (n : ℤ) (p : Pt) (q : GridEdge) :
    flux1 (rotPt n p) (rotL d) (rotE n q) = chi (n - 1, 0) * rotSgn q * flux1 p d q := by
  rw [flux1_eq_path (rotL_mem hd), flux1_eq_path hd, chi_rot]
  obtain ⟨a, v⟩ := q
  have key := pathSign_rot hd (p - a) v
  cases v
  · simp only [rotE, rotSgn, Bool.false_eq_true, ite_false, add_zero, Bool.not_false] at key ⊢
    rw [pathSign_sub, rotPt_sub, key, pathSign_sub p d a]
    ring
  · simp only [rotE, rotSgn, ite_true, Bool.not_true] at key ⊢
    rw [pathSign_sub, show rotPt n p - (rotPt n a - (1, 0)) = rotL (p - a) + (1, 0) by
      rw [← rotPt_sub]; abel, key, pathSign_sub p d a]
    ring

lemma chi_rotE (n : ℤ) (q : GridEdge) :
    chi (rotE n q).1 = chi (n - 1, 0) * rotSgn q * chi q.1 := by
  obtain ⟨a, v⟩ := q
  cases v
  · simp [rotE, rotSgn, chi_rot]
  · simp only [rotE, rotSgn, ite_true]
    rw [sub_eq_add_neg, chi_add, chi_rot]
    simp only [chi, Prod.fst_neg, Prod.snd_neg]
    split_ifs <;> omega

lemma rotE_surjective (n : ℤ) : Function.Surjective (rotE n) := by
  rintro ⟨b, v⟩
  cases v
  · refine ⟨((b.2, n - 1 - (b.1 + 1)), true), ?_⟩
    simp only [rotE, rotPt, ite_true, Prod.mk.injEq, and_true]
    ext <;> simp
  · refine ⟨((b.2, n - 1 - b.1), false), ?_⟩
    simp only [rotE, rotPt, Bool.false_eq_true, ite_false, Prod.mk.injEq, and_true]
    ext <;> simp

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

/-- `ω` of the rotated family at the image step is `±ω`. -/
theorem omega_rot (hd : ∀ i, d i ∈ knightVecs) (n : ℤ) (q : GridEdge) :
    flux (fun i => rotPt n (a i)) (fun i => rotL (d i)) (rotE n q) + chi (rotE n q).1 =
      chi (n - 1, 0) * rotSgn q * (flux a d q + chi q.1) := by
  simp only [flux, flux1_rot (hd _), chi_rotE, ← mul_sum]
  ring

lemma three_dvd_omega_rot_iff (hd : ∀ i, d i ∈ knightVecs) (n : ℤ) (q : GridEdge) :
    (3 : ℤ) ∣ flux (fun i => rotPt n (a i)) (fun i => rotL (d i)) (rotE n q) +
      chi (rotE n q).1 ↔ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  rw [omega_rot a d hd]
  have hu : IsUnit (chi (n - 1, 0) * rotSgn q) := by
    unfold chi rotSgn; split_ifs <;> simp
  exact hu.dvd_mul_left

lemma deg_rot (n : ℤ) (v : Pt) :
    deg (fun i => rotPt n (a i)) (fun i => rotL (d i)) (rotPt n v) = deg a d v := by
  simp only [deg, ← rotPt_add, (rotPt_injective n).eq_iff]

omit [Fintype ι] in
lemma DistinctEdges.rot (h : DistinctEdges a d) (n : ℤ) :
    DistinctEdges (fun i => rotPt n (a i)) (fun i => rotL (d i)) := by
  intro i j hij hc
  apply h i j hij
  simpa only [← rotPt_add, (rotPt_injective n).eq_iff] using hc

end Family

/-! ### Iterated rotation: the corner charge at all four corners -/

/-- A point of the board `[0, n-1]²`. -/
def InBoard (n : ℤ) (p : Pt) : Prop := 0 ≤ p.1 ∧ p.1 < n ∧ 0 ≤ p.2 ∧ p.2 < n

lemma InBoard.rot {n : ℤ} {p : Pt} (h : InBoard n p) : InBoard n (rotPt n p) := by
  unfold InBoard rotPt at *; simp only; omega

lemma InBoard.iter {n : ℤ} {p : Pt} (h : InBoard n p) (k : ℕ) : InBoard n ((rotPt n)^[k] p) := by
  induction k with
  | zero => exact h
  | succ k ih => rw [Function.iterate_succ_apply']; exact ih.rot

lemma rotL_iter_mem {d : Pt} (hd : d ∈ knightVecs) (k : ℕ) : rotL^[k] d ∈ knightVecs := by
  induction k with
  | zero => exact hd
  | succ k ih => rw [Function.iterate_succ_apply']; exact rotL_mem ih

lemma rotPt_iter_add (n : ℤ) (k : ℕ) (p d : Pt) :
    (rotPt n)^[k] (p + d) = (rotPt n)^[k] p + rotL^[k] d := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Function.iterate_succ_apply', Function.iterate_succ_apply',
      Function.iterate_succ_apply', ih, rotPt_add]

lemma exists_rot_iter {n : ℤ} {v : Pt} (hv : InBoard n v) (k : ℕ) :
    ∃ u, InBoard n u ∧ (rotPt n)^[k] u = v := by
  induction k generalizing v with
  | zero => exact ⟨v, hv, rfl⟩
  | succ k ih =>
    have hw : InBoard n (v.2, n - 1 - v.1) := by unfold InBoard at *; simp only; omega
    obtain ⟨u, hu, hk⟩ := ih hw
    refine ⟨u, hu, ?_⟩
    rw [Function.iterate_succ_apply', hk]
    ext <;> simp [rotPt]

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

lemma three_dvd_omega_iter_iff (hd : ∀ i, d i ∈ knightVecs) (n : ℤ) (k : ℕ) (q : GridEdge) :
    (3 : ℤ) ∣ flux (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)) ((rotE n)^[k] q) +
      chi ((rotE n)^[k] q).1 ↔ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [Function.iterate_succ_apply']
    rw [three_dvd_omega_rot_iff (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i))
      (fun i => rotL_iter_mem (hd i) k), ih]

lemma deg_iter (n : ℤ) (k : ℕ) (v : Pt) :
    deg (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)) ((rotPt n)^[k] v) =
      deg a d v := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [Function.iterate_succ_apply']
    rw [deg_rot (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)), ih]

omit [Fintype ι] in
lemma DistinctEdges.iter (h : DistinctEdges a d) (n : ℤ) (k : ℕ) :
    DistinctEdges (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)) := by
  induction k with
  | zero => exact h
  | succ k ih =>
    simp only [Function.iterate_succ_apply']
    exact ih.rot _ _ n

/-- **Corner charge at every corner.** Rotate the board `k` times by a quarter turn. If the
rotated family satisfies the one-row hypotheses of `corner_charge_row` at radius `R`, then the
original family has a step `q` with `ω(q)` not divisible by 3 whose image after `k` rotations
lies on `γ_R`. The family must lie in the board, with degree two on every board cell. -/
theorem corner_charge_rot (hd : ∀ i, d i ∈ knightVecs) (n : ℤ)
    (hboard : ∀ i, InBoard n (a i) ∧ InBoard n (a i + d i))
    (hdeg : ∀ v, InBoard n v → deg a d v = 2) (hdist : DistinctEdges a d)
    (k : ℕ) (R : ℕ) (hR : 12 ≤ R) (hRn : (R : ℤ) < n)
    (sL sB : ℤ) (hsL : sL ∈ ({1, -1} : Finset ℤ)) (hsB : sB ∈ ({1, -1} : Finset ℤ))
    (hrowL : (univ.filter fun i => StradL (canon Prod.snd
      ((rotPt n)^[k] (a i) - (0, (R : ℤ))) (rotL^[k] (d i)))).image
      (fun i => canon Prod.snd ((rotPt n)^[k] (a i) - (0, (R : ℤ))) (rotL^[k] (d i))) = PL sL)
    (hrowB : (univ.filter fun i => StradB (canon Prod.fst
      ((rotPt n)^[k] (a i) - ((R : ℤ), 0)) (rotL^[k] (d i)))).image
      (fun i => canon Prod.fst ((rotPt n)^[k] (a i) - ((R : ℤ), 0)) (rotL^[k] (d i))) = PB sB) :
    ∃ q, (rotE n)^[k] q ∈ gammaSteps R ∧ ¬ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  set ak : ι → Pt := fun i => (rotPt n)^[k] (a i)
  set dk : ι → Pt := fun i => rotL^[k] (d i)
  have hdk : ∀ i, dk i ∈ knightVecs := fun i => rotL_iter_mem (hd i) k
  have hpos : ∀ i, 0 ≤ (ak i).1 ∧ 0 ≤ (ak i).2 ∧ 0 ≤ (ak i + dk i).1 ∧ 0 ≤ (ak i + dk i).2 := by
    intro i
    have h1 := (hboard i).1.iter k
    have h2 := (hboard i).2.iter k
    rw [rotPt_iter_add] at h2
    exact ⟨h1.1, h1.2.2.1, h2.1, h2.2.2.1⟩
  have hdegk : ∀ v ∈ box R, deg ak dk v = 2 := by
    intro v hv
    have hvb : InBoard n v := by
      simp only [box, mem_product, mem_Icc] at hv
      unfold InBoard; omega
    obtain ⟨u, hu, rfl⟩ := exists_rot_iter hvb k
    rw [deg_iter a d n k u, hdeg u hu]
  obtain ⟨q', hq', hnd⟩ := corner_charge_row ak dk hdk hpos (hdist.iter a d n k) R hR hdegk
    sL sB hsL hsB hrowL hrowB
  obtain ⟨q, rfl⟩ := ((rotE_surjective n).iterate k) q'
  exact ⟨q, hq', fun h => hnd ((three_dvd_omega_iter_iff a d hd n k q).2 h)⟩

end Family

end KT
