import LeanSoln.data

--def data := "....#.....
--.........#
--..........
--..#.......
--.......#..
--..........
--.#..^.....
--........#.
--#.........
--......#..."

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

def findXCol : Nat → List (Nat × Nat × Char) → List (Nat × Nat × Char)
  | x, xs => List.filter (λ y ↦ y.fst = x) xs

def findYRow : Nat → List (Nat × Nat × Char) → List (Nat × Nat × Char)
  | y, xs => List.filter (λ x ↦ x.snd.fst = y) xs

def findFirst : (Nat × Nat × Char → Bool) → List (Nat × Nat × Char) → Nat × Nat × Char → Nat × Nat × Char
  | _, [], dummy => dummy
  | f, (x :: xs), dummy => if f x then x else findFirst f xs dummy

def findEnd : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → Nat × Nat
  | (_, _), x, y, Dir.Up, xs => let pend := stripLast (findFirst (λ p ↦ p.snd.fst < y) (findXCol x xs).reverse (x, 1000, '#')) ; if pend.snd = 1000 then (pend.fst, 0) else (pend.fst, pend.snd + 1)
  | (_, maxy), x, y, Dir.Down, xs => let pend := stripLast (findFirst (λ p ↦ p.snd.fst > y) (findXCol x xs) (x, 1000, '#')) ; if pend.snd = 1000 then (pend.fst, maxy-1) else (pend.fst, pend.snd - 1)
  | (_, _), x, y, Dir.Left, xs => let pend := stripLast (findFirst (λ p ↦ p.fst < x) (findYRow y xs).reverse (1000, y, '#')); if pend.fst = 1000 then (0, pend.snd) else (pend.fst + 1, pend.snd)
  | (maxx, _), x, y, Dir.Right, xs => let pend := stripLast (findFirst (λ p ↦ p.fst > x) (findYRow y xs) (1000, y, '#')) ; if pend.fst = 1000 then (maxx-1, pend.snd) else (pend.fst - 1, pend.snd)

def rangeBetween : Nat → Nat → List Nat
  | x, y => List.map (.+x) (List.range (y - x + 1))

def repeatN {α : Type} : α → Nat → List α
  | _, 0 => []
  | a, Nat.succ n => a :: (repeatN a n)

def visitedLine : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → List (Nat × Nat × Dir)
  | mxmy, x, y, Dir.Up, xs => let pend := (findEnd mxmy x y Dir.Up xs).snd ; List.zip (repeatN x (y - pend + 1)) (List.zip (rangeBetween pend y).reverse (repeatN Dir.Up (y - pend + 1)))
  | mxmy, x, y, Dir.Down, xs => let pend := (findEnd mxmy x y Dir.Down xs).snd ; List.zip (repeatN x (pend - y + 1)) (List.zip (rangeBetween y pend) (repeatN Dir.Down (pend - y + 1)))
  | mxmy, x, y, Dir.Right, xs => let pend := (findEnd mxmy x y Dir.Right xs).fst ; List.zip (rangeBetween x pend) (List.zip (repeatN y (pend - x + 1)) (repeatN Dir.Right (pend - x + 1))) 
  | mxmy, x, y, Dir.Left, xs => let pend := (findEnd mxmy x y Dir.Left xs).fst ; List.zip (rangeBetween pend x).reverse (List.zip (repeatN y (x - pend + 1)) (repeatN Dir.Left (x - pend + 1)))

def matchOnLast : (Nat × Nat) → (Nat × Nat) → Bool
  | (maxx, maxy), (x, y) => Bool.or (Bool.or (x = maxx-1) (y = maxy-1)) (Bool.or (x = 0) (y = 0))

def nextDir : Dir → Dir
  | Dir.Up => Dir.Right
  | Dir.Right => Dir.Down
  | Dir.Down => Dir.Left
  | Dir.Left => Dir.Up

def isLoop : List (Nat × Nat × Dir) → Bool
  | [] => False
  | (x :: xs) => if xs.contains x then true else isLoop xs 

def weird : (Nat × Nat) × Dir → Nat × Nat × Dir
  | ((x, y), z) => (x, y, z)

def recurDo : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → Nat → List (Nat × Nat × Dir) → List (Nat × Nat × Dir)
  | _, _, _, _, _, 0, prev => prev
  | mxmy, x, y, d, xs, Nat.succ n, prev => let line := visitedLine mxmy x y d xs ; if (matchOnLast mxmy (stripLast line.getLast!)) then (List.map weird (List.zip (List.map stripLast line) (repeatN d line.length))) else if (prev.contains line.getLast!) then  (List.map weird (List.zip (List.map stripLast line) (repeatN d line.length))) else line ++ (recurDo mxmy line.getLast!.fst line.getLast!.snd.fst (nextDir d) xs n (line.getLast! :: prev))

def recurDo'' : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → Nat → List (Nat × Nat × Dir) → Bool
  | _, _, _, _, _, 0, prev => isLoop prev
  | mxmy, x, y, d, xs, Nat.succ n, prev => let line := visitedLine mxmy x y d xs ; if (matchOnLast mxmy (stripLast line.getLast!)) then false else if (prev.contains line.getLast!) then true else (recurDo'' mxmy line.getLast!.fst line.getLast!.snd.fst (nextDir d) xs n (line.getLast! :: prev))

def recurDo' : Nat × Nat → Nat → Nat → Dir → List (Nat × Nat × Char) → Nat → List (Nat × Nat × Dir)
  | _, _, _, _, _, 0 => []
  | mxmy, x, y, d, xs, Nat.succ n => let line := visitedLine mxmy x y d xs ; if (matchOnLast mxmy (stripLast line.getLast!)) then (List.map weird (List.zip (List.map stripLast line) (repeatN d line.length))) else line ++ (recurDo' mxmy line.getLast!.fst line.getLast!.snd.fst (nextDir d) xs n)

def gridDims : Nat × Nat := ((grid $ lines data).length, (grid $ lines data).head!.length)

def walk' (gxy : Nat × Nat) (obstacl : List (Nat × Nat × Char))  : List (Nat × Nat × Dir) := recurDo gridDims gxy.fst gxy.snd Dir.Up obstacl 1000 []

def cornerWalk (gxy : Nat × Nat) (obstacl : List (Nat × Nat × Char)) : Bool := recurDo'' gridDims gxy.fst gxy.snd Dir.Up obstacl 1000 []

def walk (gxy : Nat × Nat) (obstacl : List (Nat × Nat × Char))  : List (Nat × Nat × Dir) := recurDo' gridDims gxy.fst gxy.snd Dir.Up obstacl 1000

def detBet : Nat × Nat → Nat × Nat → Nat × Nat → Bool
  | (x, y), (x1, y1), (x2, y2) => if y1 = y2 then Bool.and (x1 ≤ x) (x ≤ x2) else if (y = y1) then (x1 ≤ x) else if (y = y2) then (x ≤ x2) else (Bool.and (y1 ≤ y) (y ≤ y2))

def insertObst : Nat × Nat × Char → List (Nat × Nat × Char) → List (Nat × Nat × Char)
  | (x, y, c), [] => [(x, y, c)]
  | (x, y, c), ((x1, y1, _) :: []) => if Bool.and (x1 ≤ x) (y1 ≤ y) then [(x1, y1, c), (x, y, c)] else [(x1, y1, c), (x, y, c)]
  | (x, y, c), ((x1, y1, _) :: ((x2, y2, _) :: xs)) => if detBet (x, y) (x1, y1) (x2, y2) then (x1, y1, c) :: ((x, y, c) :: ((x2, y2, c) :: xs)) else (x1, y1, c) :: (insertObst (x, y, c) ((x2, y2, c) :: xs))

def newBoards : List (Nat × Nat × Char) → List (Nat × Nat × Dir) → List (List (Nat × Nat × Char))
  | _, [] => []
  | obs, (x :: xs) => (insertObst (x.fst, x.snd.fst, '#') obs) :: (newBoards obs xs)

def countTrue : List Bool → Nat
  | [] => 0
  | (true :: xs) => 1 + countTrue xs
  | (false :: xs) => countTrue xs

def nearEqual : Nat × Nat × Dir → Nat × Nat × Dir → Bool
  | (x, y, _), (x1, y1, _) => Bool.and (x == x1) (y == y1)

def uniqueLine : List (Nat × Nat × Dir) → List (Nat × Nat × Dir)
  | [] => []
  | (x :: xs) => x :: uniqueLine (List.dropWhile (nearEqual x .) xs)

def splitInto : List (Nat × Nat × Dir) → List (List (Nat × Nat × Dir))
  | [] => []
  | (x :: xs) => (x :: List.takeWhile (λ y ↦ y.fst=x.fst) xs) :: (splitInto (List.dropWhile (λ y ↦ y.fst=x.fst) xs))

def prodOrder : Nat × Nat × Dir → Nat × Nat × Dir → Bool
  | (_, y, _), (_, b, _) => y < b

def uniqueWalk (xs : List (Nat × Nat × Dir)) : List (Nat × Nat × Dir) := flatten (List.map (λ y ↦ uniqueLine (Array.qsort (y.toArray) prodOrder).toList) (splitInto (Array.qsort xs.toArray (λ xy ↦ (λ ab ↦ xy.fst < ab.fst))).toList))

def guardPosI : Nat × Nat := (stripLast (guardPos $ grid $ lines data))

-- Steps xyd, mxmy, obs
def goesToEdge : Nat → (Nat × Nat × Dir) → Nat × Nat → List (Nat × Nat × Char) → Bool
  | 0, _, _, _ => false
  | n, (x, y, d), mxmy, obs => recurDo'' mxmy x y d obs n []

def cutCases : List (Nat × Nat × Dir) := let points := (walk guardPosI (obstacles $ grid $ lines data)) ; (List.map (λ x ↦ x.snd) (List.filter (λ y ↦ Bool.not $ goesToEdge 500 (y.fst) gridDims (insertObst (y.snd.fst, y.snd.snd.fst, '#') (obstacles $ grid $ lines data))) (List.zip points points.tail!)))

-- Critical (3, 6), (6, 7), (7, 7), (1, 8), (3, 8), (7, 9)
-- #eval! (List.filter (λ y ↦ cornerWalk guardPosI y) (newBoards (obstacles $ grid $ lines data) (uniqueWalk (walk guardPosI (obstacles $ grid $ lines data))))).length
