import LeanSoln.data

def lines (s : String) : List String := s.splitOn "\n"

def grid : List String → List (List Char) := List.map (λ s ↦ s.data)

def flatten {α : Type} : List (List α) → List α
  | [] => []
  | (x :: xs) => x ++ (flatten xs)

-- Note these are sorted by y and then x
def obstacles (xs : List (List Char)) : List (Nat × Nat × Char) := List.filter (λ (_,_,char) ↦ char = '#') (flatten $ List.map (λ (line, y) ↦ List.map (λ (char, x) ↦ (x, y, char)) (List.zip line (List.range line.length))) (List.zip xs (List.range xs.length)))

def guardPos (xs : List (List Char)) : Nat × Nat × Char := (List.filter (λ (_,_,char) ↦ char = '^') (flatten $ List.map (λ (line, y) ↦ List.map (λ (char, x) ↦ (x, y, char)) (List.zip line (List.range line.length))) (List.zip xs (List.range xs.length)))).head!

def stripChar : Nat × Nat × Char → Nat × Nat
  | (x, y, _) => (x, y)

inductive Dir where
  | Up : Dir
  | Down : Dir
  | Left : Dir
  | Right : Dir

def findXCol : Nat → List (Nat × Nat × Char) → List (Nat × Nat × Char)
  | x, xs => List.filter (λ y ↦ y.fst = x) xs

def findYRow : Nat → List (Nat × Nat × Char) → List (Nat × Nat × Char)
  | y, xs => List.filter (λ x ↦ x.snd.fst = y) xs

def findFirst : (Nat × Nat × Char → Bool) → List (Nat × Nat × Char) → Nat × Nat × Char → Nat × Nat × Char
  | _, [], dummy => dummy
  | f, (x :: xs), dummy => if f x then x else findFirst f xs dummy

def findEnd : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → Nat × Nat
  | (_, _), x, y, Dir.Up, xs => let pend := stripChar (findFirst (λ p ↦ p.snd.fst < y) (findXCol x xs).reverse (x, 1000, '#')) ; if pend.snd = 1000 then (pend.fst, 0) else (pend.fst, pend.snd + 1)
  | (_, maxy), x, y, Dir.Down, xs => let pend := stripChar (findFirst (λ p ↦ p.snd.fst > y) (findXCol x xs) (x, 1000, '#')) ; if pend.snd = 1000 then (pend.fst, maxy-1) else (pend.fst, pend.snd - 1)
  | (_, _), x, y, Dir.Left, xs => let pend := stripChar (findFirst (λ p ↦ p.fst < x) (findYRow y xs).reverse (1000, y, '#')); if pend.fst = 1000 then (0, pend.snd) else (pend.fst + 1, pend.snd)
  | (maxx, _), x, y, Dir.Right, xs => let pend := stripChar (findFirst (λ p ↦ p.fst > x) (findYRow y xs) (1000, y, '#')) ; if pend.fst = 1000 then (maxx-1, pend.snd) else (pend.fst - 1, pend.snd)

def rangeBetween : Nat → Nat → List Nat
  | x, y => List.map (.+x) (List.range (y - x + 1))

def repeatN {α : Type} : α → Nat → List α
  | _, 0 => []
  | a, Nat.succ n => a :: (repeatN a n)

def visitedLine : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → List (Nat × Nat)
  | mxmy, x, y, Dir.Up, xs => let pend := (findEnd mxmy x y Dir.Up xs).snd ; List.zip (repeatN x (y - pend + 1)) (rangeBetween pend y).reverse
  | mxmy, x, y, Dir.Down, xs => let pend := (findEnd mxmy x y Dir.Down xs).snd ; List.zip (repeatN x (pend - y + 1)) (rangeBetween y pend)
  | mxmy, x, y, Dir.Right, xs => let pend := (findEnd mxmy x y Dir.Right xs).fst ; List.zip (rangeBetween x pend) (repeatN y (pend - x + 1)) 
  | mxmy, x, y, Dir.Left, xs => let pend := (findEnd mxmy x y Dir.Left xs).fst ; List.zip (rangeBetween pend x).reverse (repeatN y (x - pend + 1))

def matchOnLast : (Nat × Nat) → (Nat × Nat) → Bool
  | (maxx, maxy), (x, y) => Bool.or (Bool.or (x = maxx-1) (y = maxy-1)) (Bool.or (x = 0) (y = 0))

def nextDir : Dir → Dir
  | Dir.Up => Dir.Right
  | Dir.Right => Dir.Down
  | Dir.Down => Dir.Left
  | Dir.Left => Dir.Up

def recurDo : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → Nat → List (Nat × Nat)
  | _, _, _, _, _, 0 => []
  | mxmy, x, y, d, xs, Nat.succ n => let line := visitedLine mxmy x y d xs ; if (matchOnLast mxmy line.getLast!) then line else line ++ (recurDo mxmy line.getLast!.fst line.getLast!.snd (nextDir d) xs n)

def gridDims : Nat × Nat := ((grid $ lines data).length, (grid $ lines data).head!.length)

def walk : List (Nat × Nat) := recurDo gridDims (stripChar $ guardPos $ grid $ lines data).fst (stripChar $ guardPos $ grid $ lines data).snd Dir.Up (obstacles $ grid $ lines data) 500

def uniqueLine : List (Nat × Nat) → List (Nat × Nat)
  | [] => []
  | (x :: xs) => x :: uniqueLine (List.dropWhile (.=x) xs)

def splitInto : List (Nat × Nat) → List (List (Nat × Nat))
  | [] => []
  | (x :: xs) => (x :: List.takeWhile (λ y ↦ y.fst=x.fst) xs) :: (splitInto (List.dropWhile (λ y ↦ y.fst=x.fst) xs))

def prodOrder : Nat × Nat → Nat × Nat → Bool
  | (_, y), (_, b) => y < b

def uniqueWalk (xs : List (Nat × Nat)) : List (Nat × Nat) := flatten (List.map (λ y ↦ uniqueLine (Array.qsort (y.toArray) prodOrder).toList) (splitInto (Array.qsort xs.toArray (λ xy ↦ (λ ab ↦ xy.fst < ab.fst))).toList))

#eval! (uniqueWalk walk).length

