import Std.Data.HashSet
/-! Width-2 strip transfer graph (port of strip2_independent.successors). -/

abbrev P := Int × Int
abbrev PE := P × P × Nat   -- lower end, upper end, component
abbrev St := Nat × List PE

def sgn (v : Int) : Int := if v > 0 then 1 else if v < 0 then -1 else 0
def turn (a b c : P) : Int := sgn ((b.1 - a.1) * (c.2 - a.2) - (b.2 - a.2) * (c.1 - a.1))
def proper (a b c d : P) : Bool :=
  turn a b c * turn a b d == -1 && turn c d a * turn c d b == -1

def upMoves : List P := [(1, 2), (-1, 2), (2, 1), (-2, 1)]

def ltP (a b : P) : Bool := a.1 < b.1 || (a.1 == b.1 && a.2 < b.2)
def ltKey (x y : PE) : Bool := ltP x.1 y.1 || (x.1 == y.1 && ltP x.2.1 y.2.1)

def insertSorted (x : PE) : List PE → List PE
  | [] => [x]
  | y :: ys => if ltKey y x then y :: insertSorted x ys else x :: y :: ys
def sortPE (l : List PE) : List PE := l.foldr insertSorted []

/-- relabel components in order of first appearance -/
def relabel (l : List (P × P × Int)) : List PE :=
  let rec go (l : List (P × P × Int)) (ren : List (Int × Nat)) : List PE :=
    match l with
    | [] => []
    | (a, b, c) :: rest =>
      match ren.lookup c with
      | some k => (a, b, k) :: go rest ren
      | none => (a, b, ren.length) :: go rest (ren ++ [(c, ren.length)])
  go l []

def insertSortedI (x : P × P × Int) : List (P × P × Int) → List (P × P × Int)
  | [] => [x]
  | y :: ys => if ltP y.1 x.1 || (y.1 == x.1 && ltP y.2.1 x.2.1) then y :: insertSortedI x ys
      else x :: y :: ys

def picks (cand : List P) (k : Nat) : List (List P) :=
  match k with
  | 0 => [[]]
  | 1 => cand.map fun t => [t]
  | _ =>
    let rec pairs : List P → List (List P)
      | [] => []
      | x :: xs => xs.map (fun y => [x, y]) ++ pairs xs
    pairs cand

def successors (s : St) : List (St × Nat) :=
  let col := s.1
  let pend := s.2
  let here : P := (col, 0)
  let inc := pend.filter fun p => p.2.1 == here
  let others := pend.filter fun p => p.2.1 != here
  let strip := col < 2
  let cand := upMoves.filterMap fun (dx, dy) =>
    let t : P := ((col : Int) + dx, dy)
    if 0 ≤ t.1 ∧ t.1 < 4 ∧ (strip ∨ t.1 < 2) then some t else none
  if inc.length > 2 then [] else
  if strip && inc.length > 2 then [] else
  if inc.length == 2 && (inc[0]!).2.2 == (inc[1]!).2.2 then [] else
  let need : List Nat := if strip then [2 - inc.length] else List.range (3 - inc.length)
  need.flatMap fun k =>
    (picks cand k).filterMap fun pick =>
      let load (t : P) : Nat := (others.filter fun p => p.2.1 == t).length + (pick.filter (· == t)).length
      if pick.any (fun t => load t > 2) then none else
      let newe := pick.map fun t => (here, t)
      let wOld := (newe.map fun e => (others.filter fun p => proper p.1 p.2.1 e.1 e.2).length).sum
      let wNew := match newe with
        | [e1, e2] => if proper e1.1 e1.2 e2.1 e2.2 then 1 else 0
        | _ => 0
      let (lab, merge) : Int × Option Nat :=
        match inc with
        | [] => (-1, none)
        | [p] => ((p.2.2 : Int), none)
        | p :: q :: _ => ((p.2.2 : Int), some q.2.2)
      let lst1 : List (P × P × Int) := others.map fun p =>
        (p.1, p.2.1, if merge == some p.2.2 then lab else (p.2.2 : Int))
      let lst2 := lst1 ++ newe.map fun e => (e.1, e.2, lab)
      let (ncol, dy) : Nat × Int := if col + 1 == 4 then (0, 1) else (col + 1, 0)
      let lst3 := lst2.map fun (a, b, c) => ((a.1, a.2 - dy), (b.1, b.2 - dy), c)
      let lst4 := lst3.foldr insertSortedI []
      some ((ncol, relabel lst4), wOld + wNew)

open Std
#eval do
  let start : St := (0, [])
  let mut seen : HashSet St := ({} : HashSet St).insert start
  let mut queue : Array St := #[start]
  let mut i := 0
  let mut arcs := 0
  while i < queue.size do
    let s := queue[i]!
    i := i + 1
    let succ : List (St × Nat) := successors s
    let mut tg : HashSet St := {}
    for (st : St × Nat) in succ do
      let t := st.1
      tg := tg.insert t
      if !seen.contains t then
        seen := seen.insert t
        queue := queue.push t
    arcs := arcs + tg.size
  return (queue.size, arcs)
