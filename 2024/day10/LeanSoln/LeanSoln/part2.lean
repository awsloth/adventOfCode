import LeanSoln.data

-- Custom data types
inductive Dir where
  | Up | Down | Left | Right
  deriving Repr, BEq

-- safe
def Dir.addVec : Dir → Nat × Nat → Nat × Nat → (Nat × Nat) × Bool
  | Dir.Up, (x, y), (_, _) => if y > 0 then ((x, y-1), true) else ((0, 0), false)
  | Dir.Left, (x, y), (_, _) => if x > 0 then ((x-1, y), true) else ((0, 0), false)
  | Dir.Right, (x, y), (mx, _) => if x < mx-1 then ((x+1, y), true) else ((0, 0), false)
  | Dir.Down, (x, y), (_, my) => if y < my-1 then ((x, y+1), true) else ((0, 0), false)

def allDirs : List Dir := [Dir.Up, Dir.Right, Dir.Down, Dir.Left]

def List.flatten {α : Type} : List (List α) → List α
  | [] => []
  | (x :: xs) => x ++ xs.flatten

def List.sum : List Nat → Nat := List.foldl (.+.) 0

def formGrid (s : String) : List (List Nat) := List.map (λ x ↦ List.map (λ y ↦ y.toNat - 48) x.data) (s.splitOn "\n")

def validWalks : Nat → List (List Nat) → Nat × Nat → List (Nat × Nat)
  | 0, _, xy => [xy]
  | (n + 1), grid, (x, y) => let gridDims := (grid.head!.length, grid.length);
                             (List.map (validWalks n grid .) (List.map (λ y ↦ y.fst) (List.filter (λ ((u, v), b) ↦ Bool.and b ((grid.get! y).get! x < (grid.get! v).get! u)) (List.map (Dir.addVec . (x, y) gridDims) allDirs)))).flatten

def locateHeads (grid : List (List Nat)) : List (Nat × Nat) := List.map (λ ((x, _), y) ↦ (x, y)) (List.filter (λ ((_, d), _) ↦ d == 0) (List.map (λ (y, xs) ↦ List.map (λ xd ↦ (xd, y)) (List.enum xs)) (List.enum grid)).flatten)

def answer (grid : List (List Nat)) : Nat := List.sum (List.map (λ start ↦ (validWalks 9 grid start).length) (locateHeads grid))
