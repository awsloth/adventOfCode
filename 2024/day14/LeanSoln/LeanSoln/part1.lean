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

def guards (s : String) : List Guard := List.map parseGuard $ lines s

def moveGuards (guards : List Guard) (steps : Nat) (grid : (Int × Int)) : List Guard := List.map (λ g ↦ g.moveN grid steps) guards

-- guards, grid, quad counts
def countQuadrants : List Guard → (Int × Int) → (Nat × Nat × Nat × Nat) → (Nat × Nat × Nat × Nat)
  | [], _, ans => ans
  | (((x, y), _) :: xs), (gx, gy), (a, b, c, d) => if (x < (gx-1)/2) then 
                                                        if (y < (gy-1)/2) then countQuadrants xs (gx, gy) (a+1, b, c, d)
                                                        else if (y > (gy-1)/2) then countQuadrants xs (gx, gy) (a, b, c+1, d)
                                                             else countQuadrants xs (gx, gy) (a, b, c, d)
                                                   else if (x > (gx-1)/2) then
                                                          if (y < (gy-1)/2) then countQuadrants xs (gx, gy) (a, b+1, c, d)
                                                          else if (y > (gy-1)/2) then countQuadrants xs (gx, gy) (a, b, c, d+1)
                                                          else countQuadrants xs (gx, gy) (a, b, c, d)
                                                        else countQuadrants xs (gx, gy) (a, b, c, d)

def calcCost : (Nat × Nat × Nat × Nat) → Nat
  | (a, b, c, d) => a * b * c * d

#eval calcCost $ countQuadrants (moveGuards (guards data) 100 gridDims) gridDims (0, 0, 0, 0)
