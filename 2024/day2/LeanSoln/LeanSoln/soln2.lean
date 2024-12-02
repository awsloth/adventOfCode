import LeanSoln.data

def levels : List (List Int) := List.map (fun x => List.map (fun y => y.toInt!) (x.splitOn " ")) (data.splitOn "\n")

def levelsToDiffs (xs : List (List Int)) : List (List Int) := List.map (fun x => List.map (fun yz => yz.snd - yz.fst) (List.zip x (List.tail x))) xs

def arrayMissingN : List Int → Nat → List Int
  | [], _ => []
  | (_ :: xs), 0 => xs
  | (x :: xs), (Nat.succ n) => x :: (arrayMissingN xs n)

def arraysMissingN (xs : List Int) : List (List Int) := List.map (fun x => arrayMissingN xs x) (List.range (xs.length))

def levelsToMultiDiffs (xs : List (List Int)) : List (List (List Int)) := List.map (fun x => arraysMissingN x) xs

def max : List Int → Int
  | [] => -10000 -- placeholder value
  | (x :: []) => x
  | (x :: xs) => let pmax := max xs ; if x > pmax then x else pmax

def min : List Int → Int
  | [] => 10000 -- placeholder value
  | (x :: []) => x
  | (x :: xs) => let pmin := min xs ; if x < pmin then x else pmin

def diffsToMinMax (xs : List (List Int)) : List (Int × Int) := List.map (fun x => (min x, max x)) xs

def validMinMax : (Int × Int) → Bool
  | (x , y) => if (Bool.or (Bool.and (Bool.and (1 ≤ x) (x ≤ 3)) (Bool.and (1 ≤ y) (y ≤ 3))) (Bool.and (Bool.and (x ≤ -1) (-3 ≤ x)) (Bool.and (y ≤ -1) (-3 ≤ y)))) then true else false

def countBools : List Bool → Nat
  | [] => 0
  | (x :: xs) => (if x then 1 else 0) + countBools xs

def zipOr : List Bool → List Bool → List Bool
  | [], [] => []
  | [], _ => []
  | _, [] => []
  | (x :: xs), (y :: ys) => (Bool.or x y) :: (zipOr xs ys)

def anyMultiDiffsValid (xs : List (List (List Int))) : List Bool := List.map (fun x => List.any (diffsToMinMax x) validMinMax) xs

def validBaseLevels : List Bool := List.map validMinMax (diffsToMinMax (levelsToDiffs levels))

def validModifiedLevels : List Bool := anyMultiDiffsValid (List.map levelsToDiffs (levelsToMultiDiffs levels))

#eval countBools $ zipOr validBaseLevels validModifiedLevels 
