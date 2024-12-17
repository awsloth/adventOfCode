import LeanSoln.data

-- Operands
-- 0 - 3 literal value
-- 4 - register A
-- 5 - register B
-- 6 - register C
-- 7 unassigned

-- Opcodes
-- 0 = A // 2^(lookup .) -> A
-- 1 = (B ⊗ .) -> B
-- 2 = ((lookup .) mod 8 -> B
-- 3 = (if A == 0 then nothing else jump .)
-- 4 = (B ⊗ C) → B (reads operand but does nothing with it
-- 5 = (print ((lookup .) mod 8))
-- 6 = A // 2^(lookup .) -> B
-- 7 = A // 2^(lookup .) -> C

def dummy : Nat := 100000000

def lookupOperand : Nat → (Nat × Nat × Nat) → Nat
  | 0 => (λ _ ↦ 0)
  | 1 => (λ _ ↦ 1)
  | 2 => (λ _ ↦ 2)
  | 3 => (λ _ ↦ 3)
  | 4 => (λ (a, _, _) ↦ a)
  | 5 => (λ (_, b, _) ↦ b)
  | 6 => (λ (_, _, c) ↦ c)
  | _ => (λ _ ↦ dummy)

def lookupOpcode : Nat → (Nat → (Nat × Nat × Nat × Nat) → ((Nat × Nat × Nat × Nat) × (List Nat)))
  | 0 => (λ n ↦ (λ (a, b, c, p) ↦ 
                      ((a / (Nat.pow 2 (lookupOperand n (a, b, c))), b, c, p+2), [])
                      ))
  | 1 => (λ n ↦ (λ (a, b, c, p) ↦ 
                      ((a, (Nat.xor b n), c, p+2), [])
                      ))
  | 2 => (λ n ↦ (λ (a, b, c, p) ↦ 
                      ((a, (Nat.mod (lookupOperand n (a, b, c)) 8), c, p+2), [])
                      ))
  | 3 => (λ n ↦ (λ (a, b, c, p) ↦ if a == 0 then ((a, b, c, p+2), [])
                               else ((a, b, c, n), []) 
                      ))
  | 4 => (λ _ ↦ (λ (a, b, c, p) ↦ 
                      ((a, Nat.xor b c, c, p+2), [])
                      ))
  | 5 => (λ n ↦ (λ (a, b, c, p) ↦ 
                      ((a, b, c, p+2), [(Nat.mod (lookupOperand n (a, b, c)) 8)])
                      ))
  | 6 => (λ n ↦ (λ (a, b, c, p) ↦ 
                      ((a, a / (Nat.pow 2 (lookupOperand n (a, b, c))), c, p+2), [])
                      ))
  | 7 => (λ n ↦ (λ (a, b, c, p) ↦ 
                      ((a, b, a / (Nat.pow 2 (lookupOperand n (a, b, c))), p+2), [])
                      ))
  | _ => (λ _ ↦ (λ regs ↦ (regs, [])))

-- instructions, pointer
def runMachine : List Nat → Nat → StateT (Nat × Nat × Nat) Id (List Nat)
  | instructions, pointer => if pointer ≥ instructions.length
                             then pure []
                             else do
                             let (a, b, c) <- get
                             let ((newa, newb, newc, newp), out) := lookupOpcode (instructions.get! pointer)
                                                                                 (instructions.get! (pointer + 1))
                                                                                 (a, b, c, pointer)
                             set (newa, newb, newc)
                             let rest <- runMachine instructions newp
                             pure (out ++ rest)


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

def getStateAnswer (str : String) : Id ((List Nat) × (Nat × Nat × Nat)) :=
  let (regs, instructions) := (parseInput str);
  StateT.run (runMachine instructions 0) regs

def answer (str : String) : String := let nums := (getStateAnswer str).fst;
                                      List.foldl (λ start ↦ (λ n ↦ start.append (",".append n.repr))) nums.head!.repr nums.tail!

#eval! answer data
