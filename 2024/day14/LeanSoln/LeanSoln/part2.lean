import LeanSoln.data

def gridDims : Int × Int := (101, 103)

def List.firstProd : List String → String × String
  | (x :: (y :: _)) => (x, y)
  | _ => ("", "")

def Guard : Type := ((Int × Int) × (Int × Int))

def Guard.moveN : Guard → (Int × Int) → Nat → Guard
  | ((x, y), (vx, vy)), (gx, gy), n => ((Int.fmod (x + n*vx) gx, Int.fmod (y + n*vy) gy), (vx, vy))

def parseGuard (s : String) : Guard := let (pos, vec) := List.firstProd $ s.splitOn " ";
                                       let (p1, p2) := List.firstProd $ pos.splitOn ",";
                                       let (v1, v2) := List.firstProd $ vec.splitOn ",";
                                       (((List.drop 2 p1.data).asString.toInt!, p2.toInt!),
                                        ((List.drop 2 v1.data).asString.toInt!, v2.toInt!))

def lines (s : String) : List String := s.splitOn "\n"

def guardStrings (s : String) : List Guard := List.map parseGuard $ lines s

def moveGuards (guards : List Guard) (steps : Nat) (grid : (Int × Int)) : List Guard := List.map (λ g ↦ g.moveN grid steps) guards

def drawGuards : List Guard → List Char → List Char
  | [], str => str
  | (((x, y), _) :: xs), str => drawGuards xs (str.set ((gridDims.fst+1)*y + x).toNat '*')

def List.flatten  {α : Type} (xs : List (List α)) : List α := List.foldl (.++.) [] xs

def board : List Char := (List.replicate (gridDims.snd).toNat ((List.replicate gridDims.fst.toNat ' ') ++ ['\n'])).flatten

def boardAtN (n : Nat) : String := (drawGuards (moveGuards (guardStrings data) n gridDims) board).asString 

def boardsUpToN : Nat → String
  | 0 => ""
  | (n + 1) => ((boardsUpToN n).append (List.replicate gridDims.fst.toNat '=' ++ ['\n']).asString).append (boardAtN n)

def uniqueGuardPos : List (Int × Int) → List (Int × Int)
  | [] => []
  | (x :: xs) => if xs.contains x then uniqueGuardPos xs else x :: uniqueGuardPos xs

def guardsToPos : List Guard → List (Int × Int) := List.map (λ (xy, _) ↦ xy)

def comp : Int × Int → Int × Int → Bool
  | (x, y), (a, b) => if (x < a) then true
                      else
                      if (x > a) then false
                      else (y < b)

def lineOfSeven : List (Int × Int) → Bool
  | (a :: (b :: (c :: (d :: (e :: (f :: (g :: xs))))))) => if Bool.and (g.fst == a.fst) (g.snd - a.snd == 6) then true else lineOfSeven (b :: (c :: (d :: (e :: (f :: (g :: xs))))))
  | _ => false

def fitsIdeas (guards : List Guard) : Bool := lineOfSeven $ (Array.qsort (uniqueGuardPos $ guardsToPos guards).toArray comp).toList

def possSolns : List Nat := List.map (λ (n, _) ↦ n) (List.filter (λ (_, guards) ↦ fitsIdeas guards) (List.map (λ n ↦ (n, moveGuards (guardStrings data) n gridDims)) (List.range 10403)))
