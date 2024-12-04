import LeanSoln.data

def lines : List String := data.splitOn "\n"

def verticals : List String → List String
  | [] => []
  | (x :: []) => List.map (λ y ↦ y.toString) x.data
  | (x :: xs) => List.zipWith (λ y ↦ (λ z ↦ (y :: z).asString)) x.data (List.map (λ y ↦ y.data) (verticals xs))

def repeatN {α : Type} : α → Nat → List α
  | _, 0 => []
  | a, Nat.succ n => a :: (repeatN a n)

def leftDiagonalStarts (xs : List String) : List (Nat × Nat) := List.zip (repeatN 0 (xs.length - 1) ++ List.range xs.head!.length) ((List.range xs.length).reverse ++ repeatN 0 (xs.head!.length - 1))

def rightDiagonalStarts (xs : List String) : List (Nat × Nat) := List.zip (List.range xs.head!.length ++ repeatN (xs.head!.length - 1) (xs.length - 1)) (repeatN 0 (xs.head!.length - 1) ++ (List.range xs.length))

def genLeftLine : (Nat × Nat) → (Nat × Nat) → List (Nat × Nat)
  | (sx, sy), (mx, my) => List.map (λ mul ↦ (sx + mul, sy + mul)) (List.range (if (mx-sx) < (my - sy) then (mx-sx) else (my - sy)))

def genRightLine : (Nat × Nat) → (Nat × Nat) → List (Nat × Nat)
  | (sx, sy), (mx, my) => List.map (λ mul ↦ (sx - mul, sy + mul)) (List.range (if (sx-mx+1) < (my - sy) then (sx-mx+1) else (my - sy)))

def leftDiagonals (xs : List String) : List String := List.map (λ y ↦ (List.map (λ (xp, yp) ↦ (xs.get! yp).data.get! xp) (genLeftLine y (xs.head!.length, xs.length))).asString) (leftDiagonalStarts xs)

def rightDiagonals (xs : List String) : List String := List.map (λ y ↦ (List.map (λ (xp, yp) ↦ (xs.get! yp).data.get! xp) (genRightLine y (0, xs.length))).asString) (rightDiagonalStarts xs)

def flatten {α : Type} : List (List α) → List α
  | [] => []
  | (x :: xs) => x ++ (flatten xs)

def silly : List (Char × Char × Char × Char) → Bool
  | [] => false
  | _ => true

def groupAsFour (xss : List String) : List (List (Char × Char × Char × Char)) := List.filter silly (List.map (λ s ↦ let xs := s.data ; List.zip xs (List.zip (xs.tail!) (List.zip xs.tail!.tail! xs.tail!.tail!.tail!))) (List.filter (λ s ↦ s.length ≥ 4) xss))

def allLines : List String → List String := (λ xs ↦ (verticals xs) ++ (leftDiagonals xs)++  (rightDiagonals xs) ++ lines)

def isXmas : Char × Char × Char × Char → Bool
  | ('X', 'M', 'A', 'S') => true
  | ('S', 'A', 'M', 'X') => true
  | _ => false

def countTrue : List Bool → Nat
  | [] => 0
  | (true :: xs) => Nat.succ (countTrue xs)
  | (false :: xs) => countTrue xs

#eval countTrue $ List.map isXmas (flatten $ groupAsFour $ allLines lines)
