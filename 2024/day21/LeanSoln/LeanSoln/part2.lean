import LeanSoln.data

inductive NumPad where
  | zero | one | two | three | four | five | six | seven | eight | nine | A

def NumPad.pos : NumPad → Int × Int
  | NumPad.zero => (1, 3)
  | NumPad.one => (0, 2)
  | NumPad.two => (1, 2)
  | NumPad.three => (2, 2)
  | NumPad.four => (0, 1)
  | NumPad.five => (1, 1)
  | NumPad.six => (2, 1)
  | NumPad.seven => (0, 0)
  | NumPad.eight => (1, 0)
  | NumPad.nine => (2, 0)
  | NumPad.A => (2, 3)

def NumPad.ToString : NumPad → String
  | NumPad.zero => "0"
  | NumPad.one => "1"
  | NumPad.two => "2"
  | NumPad.three => "3"
  | NumPad.four => "4"
  | NumPad.five => "5"
  | NumPad.six => "6"
  | NumPad.seven => "7"
  | NumPad.eight => "8"
  | NumPad.nine => "9"
  | NumPad.A => "A"

instance : ToString NumPad where
  toString n := n.ToString

instance : ToString (List NumPad) where
  toString xs := List.foldl (.++.) "" (List.map NumPad.ToString xs)

inductive Step where
  | U | D | L | R | A

def Step.pos : Step → Int × Int
  | Step.U => (1, 0)
  | Step.D => (1, 1)
  | Step.L => (0, 1)
  | Step.R => (2, 1)
  | Step.A => (2, 0)

def Step.move : Step → Int × Int
  | Step.U => (0, -1)
  | Step.D => (0, 1)
  | Step.L => (-1, 0)
  | Step.R => (1, 0)
  | Step.A => (0, 0)

def Step.ToString : Step → String
  | Step.U => "^"
  | Step.D => "v"
  | Step.L => "<"
  | Step.R => ">"
  | Step.A => "A"

def Step.lookup : Int × Int → Step
  | (1, 0) => Step.U
  | (1, 1) => Step.D
  | (0, 1) => Step.L
  | (2, 1) => Step.R
  | (2, 0) => Step.A
  | _ => Step.R

def Step.num : Step → Nat
  | Step.U => 1
  | Step.L => 0
  | Step.D => 2
  | Step.R => 3

-- Always last
  | Step.A => 4

instance : ToString Step where
  toString s := s.ToString

deriving instance BEq for Step

def inputs : String → List (List Char) := (List.map String.data) ∘ (String.splitOn . "\n")

def readToNumPad : List Char → List NumPad
  | [] => []
  | ('0' :: xs) => NumPad.zero :: (readToNumPad xs)
  | ('1' :: xs) => NumPad.one :: (readToNumPad xs)
  | ('2' :: xs) => NumPad.two :: (readToNumPad xs)
  | ('3' :: xs) => NumPad.three :: (readToNumPad xs)
  | ('4' :: xs) => NumPad.four :: (readToNumPad xs)
  | ('5' :: xs) => NumPad.five :: (readToNumPad xs)
  | ('6' :: xs) => NumPad.six :: (readToNumPad xs)
  | ('7' :: xs) => NumPad.seven :: (readToNumPad xs)
  | ('8' :: xs) => NumPad.eight :: (readToNumPad xs)
  | ('9' :: xs) => NumPad.nine :: (readToNumPad xs)
  | ('A' :: xs) => NumPad.A :: (readToNumPad xs)
  | (_ :: xs) => (readToNumPad xs)

def prependA : List NumPad → List NumPad := (NumPad.A :: .)

def prependAStep : List Step → List Step := (Step.A :: .)

def subVec : Int × Int → Int × Int → Int × Int
  | (a, b), (c, d) => (a - c, b - d)

def addVec : Int × Int → Int × Int → Int × Int
  | (a, b), (c, d) => (a + c, b + d)

instance : HSub (Int × Int) (Int × Int) (Int × Int) where
  hSub a b := subVec a b

instance : HAdd (Int × Int) (Int × Int) (Int × Int) where
  hAdd a b := addVec a b

def dirComp : Step → Step → Bool
  | a, b => a.num < b.num

def lastA : Step → Step → Bool
  | _, Step.A => true
  | Step.A, _ => false
  | _, _ => true

def vecToDir : Int × Int → List Step
  | (a, b) => let moves := (if a < 0 then (List.replicate a.natAbs Step.L)
                            else (List.replicate a.natAbs Step.R)) ++
                           (if b < 0 then (List.replicate b.natAbs Step.U)
                            else (List.replicate b.natAbs Step.D));

               -- moves
               (Array.qsort moves.toArray dirComp).toList

def stepsForCode : List NumPad → List Step
  | [] => []
  | [_] => []
  | (NumPad.A :: (NumPad.zero :: xs)) => [Step.L, Step.A] ++ (stepsForCode (NumPad.zero :: xs)) 
  | (NumPad.A :: (NumPad.one :: xs)) => [Step.U, Step.L, Step.L, Step.A] ++ (stepsForCode (NumPad.one :: xs))
  | (NumPad.A :: (NumPad.four :: xs)) => [Step.U, Step.U, Step.L, Step.L, Step.A] ++ (stepsForCode (NumPad.four :: xs))
  | (NumPad.A :: (NumPad.seven :: xs)) => [Step.U, Step.U, Step.U, Step.L, Step.L, Step.A] ++ (stepsForCode (NumPad.seven :: xs))
  | (NumPad.zero :: (NumPad.A :: xs)) => [Step.R, Step.A] ++ (stepsForCode (NumPad.A :: xs)) 
  | (NumPad.zero :: (NumPad.one :: xs)) => [Step.U, Step.L, Step.A] ++ (stepsForCode (NumPad.one :: xs))
  | (NumPad.zero :: (NumPad.four :: xs)) => [Step.U, Step.U, Step.L, Step.A] ++ (stepsForCode (NumPad.four :: xs))
  | (NumPad.zero :: (NumPad.seven :: xs)) => [Step.U, Step.U, Step.U, Step.L, Step.A] ++ (stepsForCode (NumPad.seven :: xs))
  | (NumPad.one :: (NumPad.zero :: xs)) => [Step.R, Step.D, Step.A] ++ (stepsForCode (NumPad.zero :: xs))
  | (NumPad.one :: (NumPad.A :: xs)) => [Step.R, Step.R, Step.D, Step.A] ++ (stepsForCode (NumPad.A :: xs))
  | (NumPad.four :: (NumPad.zero :: xs)) => [Step.R, Step.D, Step.D, Step.A] ++ (stepsForCode (NumPad.zero :: xs))
  | (NumPad.four :: (NumPad.A :: xs)) => [Step.R, Step.R, Step.D, Step.D, Step.A] ++ (stepsForCode (NumPad.A :: xs))
  | (NumPad.seven :: (NumPad.zero :: xs)) => [Step.R, Step.D, Step.D, Step.D, Step.A] ++ (stepsForCode (NumPad.zero :: xs))
  | (NumPad.seven :: (NumPad.A :: xs)) => [Step.R, Step.R, Step.D, Step.D, Step.D, Step.A] ++ (stepsForCode (NumPad.A :: xs))
  | (x :: (y :: xs)) => vecToDir (y.pos - x.pos) ++ [Step.A] ++ (stepsForCode (y :: xs))

def stepsForNRobot : List Step → List Step
  | [] => []
  | [_] => []
  | (Step.A :: (Step.L :: xs)) => [Step.D, Step.L, Step.L, Step.A] ++ (stepsForNRobot (Step.L :: xs))
  | (Step.U :: (Step.L :: xs)) => [Step.D, Step.L, Step.A] ++ (stepsForNRobot (Step.L :: xs))
  | (Step.L :: (Step.A :: xs)) => [Step.R, Step.R, Step.U, Step.A] ++ (stepsForNRobot (Step.A :: xs))
  | (Step.L :: (Step.U :: xs)) => [Step.R, Step.U, Step.A] ++ (stepsForNRobot (Step.U :: xs))
  | (x :: (y :: xs)) => vecToDir (y.pos - x.pos) ++ [Step.A] ++ (stepsForNRobot (y :: xs))

def List.countAll [BEq α] : List α → List (Nat × α)
  | [] => []
  | (x :: xs) => (xs.count x + 1, x) :: (List.filter (λ y ↦ Bool.not (x == y)) xs).countAll
decreasing_by
  simp
  sorry

def List.joinUp [BEq α] : List (Nat × α) → List (Nat × α)
  | [] => []
  | ((c, a) :: xs) => (c + Nat.sum (List.map (λ (x, b) ↦ if a == b then x else 0) xs), a) ::
                      (List.filter (λ (_, b) ↦ Bool.not (a == b)) xs).joinUp
decreasing_by
  sorry

def doNRobots : Nat → List (Nat × (List Step)) → List (Nat × (List Step))
  | 0, steps => steps
  | (n + 1), steps => let next := (List.map (λ (c, m) ↦ (c, stepsForNRobot (Step.A :: m))) steps);
                      let splitUp := (List.map (λ (c, m) ↦ let chunks := List.groupBy lastA m;
                                                          List.map (λ (d, n) ↦ (c*d, n)) (List.countAll chunks)) next).join;

                      doNRobots n splitUp.joinUp

def countMoves : List (Nat × (List Step)) → Nat
  | [] => 0
  | ((n, moves) :: xs) => n * moves.length + countMoves xs

def answer : Nat := Nat.sum $ List.zipWith (.*.) (List.map (λ s ↦ s.dropLast.asString.toNat!) $ inputs data)
                      ((List.map (countMoves ∘ (doNRobots 25 .) ∘ List.countAll ∘ (List.groupBy lastA .) ∘ stepsForCode ∘ prependA ∘ readToNumPad) $ inputs data))
