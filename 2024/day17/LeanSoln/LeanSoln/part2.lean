import LeanSoln.data

def dummy : Nat := 1000000

def List.Prod2 {α : Type} : α → List α → α × α
  | _, (x :: (y :: _)) => (x, y)
  | a, _ => (a, a)

def List.Prod3 {α : Type} : α → List α → α × α × α
  | _, (x :: (y :: (z :: _))) => (x, y, z)
  | a, _ => (a, a, a)

def parseInput (str : String) : (Nat × Nat × Nat) × (List Nat) :=
  let (registers, program) := List.Prod2 "" $ str.splitOn "\n\n";
  let (r1, r2, r3) := List.Prod3 dummy $ List.map (λ line ↦ (line.splitOn " ").getLast!.toNat!) $ List.take 3 (registers.splitOn "\n");
  let progInts := List.map (λ d ↦ d.toNat!) $ ((program.splitOn " ").getLast!).splitOn ","
  ((r1, r2, r3), progInts)

def memory (str : String) : List Nat := List.map (λ d ↦ d.toNat!) $ ((str.splitOn "\n\n").getLast!.splitOn " ").getLast!.splitOn ","

-- value of A → Output, value of A
def doStep : Nat → (Nat × Nat)
  | a => let mod8 := Nat.xor (Nat.mod a 8) 1;
         (Nat.xor mod8 (Nat.xor (a / (Nat.pow 2 mod8)) 5), a/8)

def runMachineN : Nat → Nat → List Nat
  | 0, _ => []
  | (n+1), a => let (out, next) := doStep a;
                if next == 0 then [out]
                else (runMachineN n next) ++ [out]


def List.rangeFrom (s e : Nat) := List.map (.+s) $ List.range (e-s)

-- Start nat, aim value, 
def undo : Nat → Nat → List Nat
  | a, aim => let poss := List.rangeFrom (a*8) ((a+1)*8)
              List.filter (λ n ↦ aim == Nat.mod (Nat.xor (Nat.xor (Nat.mod n 8) 1) (Nat.xor (n / (Nat.pow 2 (Nat.xor (Nat.mod n 8) 1))) 5)) 8) poss

def rewind : List Nat → List Nat
  | [] => []
  | [x] => undo 0 x 
  | (x :: xs) => (List.map (λ n ↦ undo n x) (rewind xs)).join

def answer : Nat := let ans := memory data; (rewind ans).head!

