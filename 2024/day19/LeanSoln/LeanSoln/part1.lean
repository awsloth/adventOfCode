import LeanSoln.data

def Towel : Type := List Char

deriving instance Inhabited for Towel
deriving instance BEq for Towel

def baseTowels (str : String) : List Towel := (Array.qsort (List.map String.data $ (str.splitOn "\n\n").head!.splitOn ", ").toArray (.<.)).toList

def patterns (str : String) : List Towel := List.map String.data $ (str.splitOn "\n\n").getLast!.splitOn "\n"

def baseColourTowels (cs : List Char): List Towel → List Towel := List.filter (λ y ↦ List.any cs (y.contains .))

def detPoss : List Towel → Towel → Bool
  | _, [] => true
  | towels, xs => let poss := List.filter (λ y ↦ y == List.take y.length xs) towels;
                  let nextWords := List.map (λ y ↦ List.drop (y.length) xs) poss;
                  if poss == [] then false
                  else List.any nextWords (detPoss towels .)

def missingTowels : List Towel := [['b'], ['u'], ['w'], ['r']]

#eval! (List.filter (detPoss ((baseColourTowels ['g'] (baseTowels data)) ++ missingTowels)) (patterns data)).length
