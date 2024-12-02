import LeanSoln.data

def levels : List (List Int) := List.map (fun x => List.map (fun y => y.toInt!) (x.splitOn " ")) (data.splitOn "\n")

def levelsToDiffs (xs : List (List Int)) : List (List Int) := List.map (fun x => List.map (fun yz => yz.snd - yz.fst) (List.zip x (List.tail x))) xs

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

#eval countBools (List.map validMinMax (diffsToMinMax (levelsToDiffs levels)))
