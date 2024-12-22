import LeanSoln.data

def starts (str : String) : List Nat := List.map String.toNat! (str.splitOn "\n")

def altNSteps : Nat → Nat → Nat
  | 0, b => b
  | (n + 1), b => let p1 := Nat.mod (Nat.xor (b * 64) b) 16777216;
                  let p2 := (Nat.xor (p1/32) p1);
                  altNSteps n (Nat.mod (Nat.xor (p2 * 2048) p2) 16777216)

def answer' (str : String) : Nat := Nat.sum $ List.map (altNSteps 2000 .) $ starts str
