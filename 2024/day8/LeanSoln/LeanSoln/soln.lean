import LeanSoln.data

def lines : List String := data.splitOn "\n"

def gridDims : (Nat × Nat) := (lines.head!.length, lines.length)

def List.enumerate {α : Type} (xs : List α) : List (Nat × α) := List.zip (List.range xs.length) xs

def List.flatten {α : Type} : List (List α) → List α
  | [] => []
  | (x :: xs) => x ++ xs.flatten

def items (xs : List String) : List (Nat × Nat × Char) := (List.map (λ (y, s) ↦ (List.map (λ (x, c) ↦ (x, y, c)) (List.enumerate s))) (List.enumerate (List.map (λ s ↦ s.data) xs))).flatten

def itemFilter : List (Nat × Nat × Char) → List (Nat × Nat × Char) := List.filter (λ (_, _, c) ↦ c ≠ '.')

def itemOrdering : (Nat × Nat × Char) → (Nat × Nat × Char) → Bool
  | (_, _, c), (_, _, c2) => c < c2

def sortItems (xs : List (Nat × Nat × Char)) : List (Nat × Nat × Char) := (Array.qsort xs.toArray itemOrdering).toList

def groupItems : List (Nat × Nat × Char) → List (Char × (List (Nat × Nat)))
  | [] => []
  | ((x, y, c) :: xs) => [(c, (x, y) :: (List.map (λ (x, y, _) ↦ (x, y)) (List.takeWhile (λ (_, _, c1) ↦ c == c1) xs)))] ++ (groupItems (List.dropWhile (λ (_, _, c1) ↦ c == c1) xs))

def List.pairs {α : Type} : List α → List (α × α)
  | [] => []
  | (_ :: []) => []
  | (x :: xs) => (List.map (λ y ↦ (x, y)) xs) ++ List.pairs xs

def genCoords : Int × Int → Int × Int → ((Int × Int) × (Int × Int))
  | (x1, y1), (x2, y2) => let diff := (x2-x1, y2-y1) ; ((x2 + diff.fst, y2 + diff.snd), (x1 - diff.fst, y1 - diff.snd))

def isValid : (Nat × Nat) → (Int × Int) → Bool
  | (maxx, maxy), (x, y) => Bool.not (Bool.or (Bool.or (x < 0) (y < 0)) (Bool.or (x ≥ (Int.ofNat maxx)) (y ≥ (Int.ofNat maxy))))

def pairToInt : Nat × Nat → Int × Int
  | (x, y) => (Int.ofNat x, Int.ofNat y)

def intToPair : Int × Int → Nat × Nat
  | (x, y) => (x.toNat, y.toNat)

def findCoords (xs : List (Nat × Nat)) : List (Nat × Nat) := List.map intToPair (List.map (λ (xy, ab) ↦ let ans := genCoords xy ab; (if isValid gridDims ans.fst then [ans.fst] else []) ++ (if isValid gridDims ans.snd then [ans.snd] else [])) (List.pairs (List.map pairToInt xs))).flatten

def allPoints (xss : List (Char × List (Nat × Nat))) : (List (Nat × Nat)) := (List.map (λ (_, xs) ↦ findCoords xs) xss).flatten

def uniquePoints : List (Nat × Nat) → List (Nat × Nat)
  | [] => []
  | (x :: xs) => if xs.contains x then (uniquePoints xs) else x :: uniquePoints xs

#eval! (uniquePoints $ allPoints $ groupItems $ sortItems $ itemFilter $ items lines).length

def answer := 1
