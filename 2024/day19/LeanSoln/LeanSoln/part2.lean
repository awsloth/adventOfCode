import LeanSoln.data

def Towel : Type := List Char

deriving instance Inhabited for Towel
deriving instance BEq for Towel

def baseTowels (str : String) : List Towel := (Array.qsort (List.map String.data $ (str.splitOn "\n\n").head!.splitOn ", ").toArray (.<.)).toList

def patterns (str : String) : List Towel := List.map String.data $ (str.splitOn "\n\n").getLast!.splitOn "\n"

def orderOnLen {α : Type} : List α → List α → Bool
  | xs, ys => xs.length < ys.length

def detPoss (towels : List Towel) : Towel → StateT (List (Towel × Nat)) Id Nat
  | [] => pure 1
  | xs => let poss := List.filter (λ y ↦ y == List.take y.length xs) towels;
          let nextWords := (Array.qsort (List.map (λ y ↦ List.drop (y.length) xs) poss).toArray orderOnLen).toList;
          if poss == [] then pure 0
          else do
            let cache ← get
            let weightlessCache := List.map Prod.fst cache
            let done := List.filter (λ w ↦ (weightlessCache.findIdx (. == w) < cache.length)) nextWords
            let doneCost := Nat.sum $ List.map (λ w ↦ (cache.get! (weightlessCache.findIdx (.==w))).snd) done

            let notDone := List.filter (λ w ↦ weightlessCache.findIdx (. == w) == cache.length) nextWords
            let vals ← List.mapM (detPoss towels .) notDone
            let toAdd := List.zip notDone vals;

            set $ (cache ++ toAdd).eraseDups
            pure $ doneCost + Nat.sum vals
termination_by sorry

def baseColourTowels (cs : List Char): List Towel → List Towel := List.filter (λ y ↦ List.any cs (y.contains .))

def detPoss' : List Towel → Towel → Bool
  | _, [] => true
  | towels, xs => let poss := List.filter (λ y ↦ y == List.take y.length xs) towels;
                  let nextWords := List.map (λ y ↦ List.drop (y.length) xs) poss;
                  if poss == [] then false
                  else List.any nextWords (detPoss' towels .)

def missingTowels : List Towel := [['b'], ['u'], ['w'], ['r']]

def toCheck : List Towel := List.filter (detPoss' ((baseColourTowels ['g'] (baseTowels data)) ++ missingTowels)) (patterns data)

#eval! Nat.sum $ List.map (Prod.fst) (List.mapM (λ pat ↦ (StateT.run (detPoss (baseTowels data) pat) [])) toCheck)
