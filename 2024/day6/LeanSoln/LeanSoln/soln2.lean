import LeanSoln.data

def lines (s : String) : List String := s.splitOn "\n"

def grid : List String → List (List Char) := List.map (λ s ↦ s.data)

def flatten {α : Type} : List (List α) → List α
  | [] => []
  | (x :: xs) => x ++ (flatten xs)

-- Note these are sorted by y and then x
def obstacles (xs : List (List Char)) : List (Nat × Nat × Char) := List.filter (λ (_,_,char) ↦ char = '#') (flatten $ List.map (λ (line, y) ↦ List.map (λ (char, x) ↦ (x, y, char)) (List.zip line (List.range line.length))) (List.zip xs (List.range xs.length)))

def guardPos (xs : List (List Char)) : Nat × Nat × Char := (List.filter (λ (_,_,char) ↦ char = '^') (flatten $ List.map (λ (line, y) ↦ List.map (λ (char, x) ↦ (x, y, char)) (List.zip line (List.range line.length))) (List.zip xs (List.range xs.length)))).head!

def stripLast {α : Type} : Nat × Nat × α → Nat × Nat
  | (x, y, _) => (x, y)

inductive Dir where
  | Up | Down | Left | Right

def Dir.beq : Dir → Dir → Bool
  | Dir.Up, Dir.Up => true
  | Dir.Down, Dir.Down => true
  | Dir.Left, Dir.Left => true
  | Dir.Right, Dir.Right => true
  | _, _ => false

instance : BEq Dir where
  beq := Dir.beq

instance : Inhabited Dir where
  default := Dir.Left

def Dir.toString : Dir → String
  | Dir.Up => "Up"
  | Dir.Down => "Down"
  | Dir.Left => "Left"
  | Dir.Right => "Right"

instance : ToString Dir where
  toString d := Dir.toString d

def findXCol : Nat → List (Nat × Nat) → List (Nat × Nat)
  | x, xs => List.filter (λ y ↦ y.fst = x) xs

def findYRow : Nat → List (Nat × Nat) → List (Nat × Nat)
  | y, xs => List.filter (λ x ↦ x.snd = y) xs

def findFirst : (Nat × Nat → Bool) → List (Nat × Nat) → Nat × Nat → Nat × Nat
  | _, [], dummy => dummy
  | f, (x :: xs), dummy => if f x then x else findFirst f xs dummy

def findEnd : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat) → ((Nat × Nat) × Bool)
  | (_, _), x, y, Dir.Up, xs => let pend := findFirst (λ p ↦ p.snd < y) (findXCol x xs).reverse (x, 10000) ; if pend.snd = 10000 then ((pend.fst, 0), true) else ((pend.fst, pend.snd + 1), false)
  | (_, maxy), x, y, Dir.Down, xs => let pend := findFirst (λ p ↦ p.snd > y) (findXCol x xs) (x, 10000) ; if pend.snd = 10000 then ((pend.fst, maxy-1), true) else ((pend.fst, pend.snd - 1), false)
  | (_, _), x, y, Dir.Left, xs => let pend := findFirst (λ p ↦ p.fst < x) (findYRow y xs).reverse (10000, y); if pend.fst = 10000 then ((0, pend.snd), true) else ((pend.fst + 1, pend.snd), false)
  | (maxx, _), x, y, Dir.Right, xs => let pend := findFirst (λ p ↦ p.fst > x) (findYRow y xs) (10000, y) ; if pend.fst = 10000 then ((maxx-1, pend.snd), true) else ((pend.fst - 1, pend.snd), false)

def matchOnLast : (Nat × Nat) → (Nat × Nat) → Bool
  | (maxx, maxy), (x, y) => Bool.or (Bool.or (x = maxx-1) (y = maxy-1)) (Bool.or (x = 0) (y = 0))

def nextDir : Dir → Dir
  | Dir.Up => Dir.Right
  | Dir.Right => Dir.Down
  | Dir.Down => Dir.Left
  | Dir.Left => Dir.Up

def gridDims : Nat × Nat := ((grid $ lines data).length, (grid $ lines data).head!.length)

def guardStart : Nat × Nat × Dir := let xy := stripLast $ guardPos $ grid $ lines data; (xy.fst, xy.snd, Dir.Up)

def obst : List (Nat × Nat) := List.map stripLast (obstacles $ grid $ lines $ data)

def nextCorner : Nat × Nat → Nat × Nat × Dir → List (Nat × Nat × Dir) → List (Nat × Nat) → Nat → List (Nat × Nat × Dir)
  | _, _, prev, _, 0 => prev
  | mxmy, (x, y, d), prev, obs, Nat.succ n => let cend := (findEnd mxmy x y d obs); if cend.snd then (prev ++ [(cend.fst.fst, cend.fst.snd, d)]) else if prev.contains (cend.fst.fst, cend.fst.snd, d) then (prev ++ [(cend.fst.fst, cend.fst.snd, d)]) else nextCorner mxmy (cend.fst.fst, cend.fst.snd, nextDir d) (prev ++ [(cend.fst.fst, cend.fst.snd, d)]) obs n
 
def repeatN {α : Type} : α → Nat → List α
  | _, 0 => []
  | a, Nat.succ n => a :: (repeatN a n)

-- inclusive
def range : Nat → Nat → List Nat
  | x, y => List.map (.+x) (List.range (y - x + 1))

def lineFind : Nat × Nat × Dir → Nat × Nat × Dir → List (Nat × Nat × Dir)
  | (x1, y1, _), (_, y2, Dir.Up) => (List.zip (repeatN x1 (y1-y2 + 1)) (List.zip ((range y2 y1).reverse) (repeatN Dir.Up (y1-y2 + 1))))
  | (x1, y1, _), (_, y2, Dir.Down) => (List.zip (repeatN x1 (y2-y1 + 1)) (List.zip (range y1 y2) (repeatN Dir.Down (y2-y1 + 1))))
  | (x1, y1, _), (x2, _, Dir.Right) => (List.zip (range x1 x2) (List.zip (repeatN y1 (x2-x1 + 1)) (repeatN Dir.Right (x2-x1 + 1))))
  | (x1, y1, _), (x2, _, Dir.Left) => (List.zip ((range x2 x1).reverse) (List.zip (repeatN y1 (x1-x2 + 1)) (repeatN Dir.Left (x1-x2 + 1))))

def boolCorner : Nat × Nat → Nat × Nat × Dir → List (Nat × Nat × Dir) → List (Nat × Nat) → Nat → Bool × Bool
  | _, _, _, _, 0 => (false, false)
  | mxmy, (x, y, d), prev, obs, Nat.succ n => let cend := (findEnd mxmy x y d obs); if cend.snd then (false, true) else if prev.contains (cend.fst.fst, cend.fst.snd, d) then (true, true) else boolCorner mxmy (cend.fst.fst, cend.fst.snd, nextDir d) (prev ++ [(cend.fst.fst, cend.fst.snd, d)]) obs n

def cornersToSquares : List (Nat × Nat × Dir) → List (Nat × Nat × Dir)
  | [] => []
  | (_ :: []) => []
  | (xy1 :: (xy2 :: xs)) => lineFind xy1 xy2 ++ cornersToSquares (xy2 :: xs)

def detBet : Nat × Nat → Nat × Nat → Nat × Nat → Bool
  | (x, y), (x1, y1), (x2, y2) => if y1 = y2 then Bool.and (x1 ≤ x) (x ≤ x2) else if (y = y1) then (x1 ≤ x) else if (y = y2) then (x ≤ x2) else (Bool.and (y1 < y) (y < y2))

def insertObst : Nat × Nat → List (Nat × Nat) → List (Nat × Nat)
  | (x, y), [] => [(x, y)]
  | (x, y), ((x1, y1) :: xs) => if (y < y1) then (x, y) :: ((x1, y1) :: xs) else if Bool.and (y == y1) (x < x1) then (x, y) :: ((x1, y1) :: xs) else (x1, y1) :: (insertObst (x, y) xs)

def newBoard : List (Nat × Nat) → (Nat × Nat × Dir) → List (Nat × Nat)
  | obs, x => insertObst (x.fst, x.snd.fst) obs

def walk : List (Nat × Nat × Dir) := (nextCorner gridDims guardStart [guardStart] obst 500)

def loopWalk (obstac : List (Nat × Nat)) (start : (Nat × Nat × Dir)) (prev : List (Nat × Nat × Dir)) (count : Nat) : Bool × Bool := boolCorner gridDims start prev obstac count

def nearEqual : Nat × Nat × Dir → Nat × Nat × Dir → Bool
  | (x, y, _), (x1, y1, _) => Bool.and (x == x1) (y == y1)

theorem dropWhileL (x : Nat × Nat × Dir) (xs : List (Nat × Nat × Dir)) : sizeOf (List.dropWhile (nearEqual x .) xs) < 1 + sizeOf xs := by
  match xs with
  | [] => simp[Nat.add_comm 1 (sizeOf x)]
  | (y :: ys) => simp[List.dropWhile]
                 match nearEqual x y with
                 | true => simp[Nat.add_comm 1 (sizeOf y)]
                           simp[Nat.add_assoc (sizeOf y) 1 (sizeOf ys)]
                           simp[←Nat.add_assoc 1 (sizeOf y) (1 + sizeOf ys)]
                           simp[Nat.lt_add_left (1 + sizeOf y) (dropWhileL x ys)]
                 | false => simp[Nat.add_comm 1 (sizeOf x)]

theorem dropWhileL' (x : Nat × Nat × Dir) (xs : List (Nat × Nat × Dir)) : sizeOf (List.dropWhile (fun y => decide (y.fst = x.fst)) xs) < 1 + sizeOf xs := by
  match xs with
  | [] => simp[Nat.add_comm 1 (sizeOf x)]
  | (y :: ys) => simp[List.dropWhile]
                 match decide (y.fst = x.fst) with
                 | true => simp[Nat.add_comm 1 (sizeOf y)]
                           simp[Nat.add_assoc (sizeOf y) 1 (sizeOf ys)]
                           simp[←Nat.add_assoc 1 (sizeOf y) (1 + sizeOf ys)]
                           simp[Nat.lt_add_left (1 + sizeOf y) (dropWhileL' x ys)]
                 | false => simp[Nat.add_comm 1 (sizeOf x)]


def uniqueLine : List (Nat × Nat × Dir) → List (Nat × Nat × Dir)
  | [] => []
  | (x :: xs) => x :: uniqueLine (List.dropWhile (nearEqual x .) xs)
decreasing_by
  simp_wf
  simp[Nat.add_comm 1 (sizeOf x)]
  simp[Nat.add_assoc]
  simp[Nat.lt_add_left (sizeOf x) (dropWhileL x xs)]

def splitInto : List (Nat × Nat × Dir) → List (List (Nat × Nat × Dir))
  | [] => []
  | (x :: xs) => (x :: List.takeWhile (λ y ↦ y.fst == x.fst) xs) :: (splitInto (List.dropWhile (λ y ↦ y.fst=x.fst) xs))
decreasing_by
  simp_wf
  simp[Nat.add_comm 1 (sizeOf x)]
  simp[Nat.add_assoc]
  simp[Nat.lt_add_left (sizeOf x) (dropWhileL' x xs)]

def prodOrder : Nat × Nat × Dir → Nat × Nat × Dir → Bool
  | (_, y, _), (_, b, _) => y < b

def uniqueWalk (xs : List (Nat × Nat × Dir)) : List (Nat × Nat × Dir) := flatten (List.map (λ y ↦ uniqueLine (Array.qsort (y.toArray) prodOrder).toList) (splitInto (Array.qsort xs.toArray (λ xy ↦ (λ ab ↦ xy.fst < ab.fst))).toList))

def zipFunc {α β : Type} : (α → β) → List α → List (α × β)
  | _, [] => []
  | f, (a :: as) => (a, f a) :: zipFunc f as

def zipTripFunc {α β δ : Type} : (α → β) → (α → δ) → List α → List (α × β × δ)
  | _, _, [] => []
  | f, g, (a :: as) => (a, f a, g a) :: zipTripFunc f g as

def walkUpTo (xy : (Nat × Nat × Dir)) (path : List (Nat × Nat × Dir)) : List (Nat × Nat × Dir) := List.takeWhile (λ y ↦ Bool.not (stripLast xy == stripLast y)) path

def findPrev : Nat × Nat × Dir → List (Nat × Nat × Dir) → Nat × Nat × Dir
  | x, [] => x -- Should never happen
  | x, (_ :: []) => x -- Similarly should never happen
  | x, (x1 :: (y :: xs)) => if (stripLast x == stripLast y) then x1 else findPrev x (y :: xs)

def answer : Nat := let corners := cornersToSquares walk.tail!; (List.filter (λ obs ↦ (loopWalk obs guardStart [guardStart] 1000).fst) (List.map (newBoard obst .) (uniqueWalk corners))).length
