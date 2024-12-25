import LeanSoln.data

def grids (str : String) : List (List String) := List.map (String.splitOn . "\n") $ str.splitOn "\n\n"

def locks : List (List String) → List (List String) := List.filter (λ xs ↦ xs.head! == "#####")

def keys : List (List String) → List (List String) := List.filter (λ xs ↦ xs.getLast! == "#####")

def List.transpose : List (List α) → List (List α)
  | [] => []
  | [x] => List.map (λ y ↦ [y]) x
  | (x :: xs) => List.zipWith (.::.) x xs.transpose

def lockToCols : List (List String) → List (List Nat) := List.map (λ xs ↦ List.map (λ s ↦ (s.takeWhile (.=='#')).length) (List.map String.data xs).transpose)

def keysToCols : List (List String) → List (List Nat) := List.map (λ xs ↦ List.map (λ s ↦ (s.dropWhile (.=='.')).length) (List.map String.data xs).transpose)

def fits (key lock : List Nat) : Bool := List.all (List.zipWith (.+.) key lock) (. ≤ 7)

def findFitting : List (List Nat) → List (List Nat) → Nat
  | [], _ => 0
  | (key :: keys), locks => (List.filter (fits key .) locks).length + findFitting keys locks

def answer (str : String) : Nat := findFitting (keysToCols $ keys $ grids str) (lockToCols $ locks $ grids str)
