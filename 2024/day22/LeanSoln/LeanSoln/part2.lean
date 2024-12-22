import LeanSoln.data
import Std

def starts (str : String) : List Nat := List.map String.toNat! (str.splitOn "\n")

def altNSteps : Nat → Nat → List Nat
  | 0, _ => []
  | (n + 1), b => let p1 := Nat.mod (Nat.xor (b * 64) b) 16777216;
                         let p2 := (Nat.xor (p1/32) p1);
                         let p3 := (Nat.mod (Nat.xor (p2 * 2048) p2) 16777216);
                         (Nat.mod p3 10) :: altNSteps n p3

def Changes : Type := Int × Int × Int × Int

deriving instance BEq for Changes
deriving instance Inhabited for Changes
deriving instance Hashable for Changes

 
def numsToChanges : List Nat → List (Changes × Nat)
  | ys => let xs := List.map Int.ofNat ys;
          List.map (λ (a, b, c, d, e) ↦ ((b-a, c-b, d-c, e-d), e.natAbs)) $ List.zip xs (List.zip xs.tail! (List.zip xs.tail!.tail! (List.zip xs.tail!.tail!.tail! xs.tail!.tail!.tail!.tail!)))

def uniqueNumChanges : List (Changes × Nat) → Std.HashMap Changes Nat
  | [] => Std.HashMap.empty
  | (x :: xs) => (uniqueNumChanges (List.filter (λ (c, _) ↦ Bool.not (c == x.fst)) xs)).insert x.fst x.snd
decreasing_by
  sorry

def lookupCost : Changes → List (List (Changes × Nat)) → List Nat
  | c, xss => List.map (λ xs ↦ let m := List.filter (λ (d, _) ↦ c == d) xs;
                               if m.length == 0 then 0
                               else m.head!.snd) xss

-- Nat.sum $ 
def answer' (str : String) : List (List Nat) := (List.map (altNSteps 2000 .) $ starts str)

def remEmpty : List (Changes × Nat) → List (Changes × Nat) := (List.filter (λ (_, c) ↦ c > 0) .)

def testChanges (str : String) : List (Std.HashMap Changes Nat) := List.map (uniqueNumChanges ∘ numsToChanges) $ answer' str

def mergeLists : List (Changes × Nat) → List (Changes × Nat) → List (Changes × Nat)
  | xs, [] => xs
  | xs, (y :: ys) => if (List.map Prod.fst xs).contains y.fst
                     then mergeLists (List.map (λ (x, c) ↦ if x == y.fst then (x, c + y.snd) else (x, c)) xs) ys
                     else mergeLists (y :: xs) ys

def mergeInto : Std.HashMap Changes Nat → List (Std.HashMap Changes Nat) → Std.HashMap Changes Nat
  | x, [] => x
  | x, (y :: ys) => mergeInto (Std.HashMap.fold (λ hs ↦ (λ c ↦ (λ n ↦ if hs.contains c
                                                                      then let t := hs[c]!;
                                                                           (hs.erase c).insert c (n + t)
                                                                      else hs.insert c n))) x y) ys


def answer (str : String) : Nat := let data := (testChanges str);
                                   List.foldl (λ p ↦ (λ n ↦ Nat.max p n)) 0 $ List.map Prod.snd (mergeInto data.head! data.tail!).toList
