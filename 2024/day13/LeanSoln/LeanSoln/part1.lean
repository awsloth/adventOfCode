import LeanSoln.data

def testData : String := "Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"

def Vec : Type := Int × Int

def Vec.fromList : List Nat → Vec
  | [] => (0, 0)
  | (x :: []) => (x, 0)
  | (x :: (y :: _)) => (x, y)

def dataToMachines (str : String) : List String := str.splitOn "\n\n"

def machineToVecString (mach : String) : List String := List.map (λ s ↦ (s.splitOn ": ").getLast!) (List.take 3 (mach.splitOn "\n"))

def parseVec : String → Vec
  | a => Vec.fromList (List.map (λ s ↦ (List.drop 2 s.data).asString.toNat!)
                                (List.take 2 (a.splitOn ", ")))

def vecString : List String → (Vec × Vec × Vec)
  | (x :: (y :: (z :: []))) => (parseVec x, parseVec y, parseVec z)
  | _ => ((0, 0), (0, 0), (0, 0)) -- dummy case

def vectorEquations (str : String) : List (Vec × Vec × Vec) := List.map (vecString ∘ machineToVecString) (dataToMachines str)

def solveLin : (Vec × Vec) → (Bool × Int)
  | ((a1, a2), (e1, e2)) => if Bool.and (Bool.and (Int.tmod e1 a1 == 0) (Int.tmod e2 a2 == 0)) (e1/a1 == e2/a2) then (true, e1/a1) else (false, 0)

def solveLinEq : (Vec × Vec × Vec) → (Bool × Vec)
  | ((a1, a2), (b1, b2), (e1, e2)) => if ((a1, a2) == (0, 0)) then match solveLin ((b1, b2), (e1, e2)) with
                                                                   | (false, _) => (false, (0, 0))
                                                                   | (true, x) => (true, (0, x))
                                      else if (b1*a2 - b2*a1 == 0) then let (smaller, side) :=
                                                                        if (a1/b1 ≥ 3)
                                                                        then ((a1, a2), true)
                                                                        else ((b1, b2), false);
                                                                        match (solveLin (smaller, (e1, e2)), side) with
                                                                        | ((false, _), _) => (false, (0, 0))
                                                                        | ((true, x), true) => (true, (x, 0))
                                                                        | ((true, x), false) => (true, (0, x))
                                      else let y := (e1*a2 - e2*a1)/(b1*a2 - b2*a1);
                                           let x := (e1 - y*b1)/a1;
                                           if Bool.and (y * (b1*a2 - b2*a1) == (e1*a2 - e2*a1)) (x*a1 == e1 - y*b1) then (true, (x, y)) else (false, (0, 0))

def solveEquations : List (Vec × Vec × Vec) → List (Bool × Vec) := List.map solveLinEq

def List.sum : List Int → Int := List.foldl (λ s ↦ (λ n ↦ s + n)) 0

def answer (str : String) : Int := List.sum $ List.map (λ (solved, (a, b)) ↦ if solved then 3 * a + b else 0) (solveEquations $ vectorEquations str)

#eval answer data
