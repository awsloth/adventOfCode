import LeanSoln.data

def testData : String := "2333133121414131402"

inductive Tag where
  | Gap | Inserted | ToInsert

-- Get numbers
def numeralData (s : String) : List Nat := List.map (λ c ↦ c.toNat - 48) s.data

-- Get last id
def lastID (xs : List Nat) : Nat := if (Nat.mod xs.length 2) == 1 then (xs.length - 1) / 2 else (xs.length / 2) - 1

def List.rangeFrom (s e : Nat) : List Nat := List.map (.+s) (List.range (e - s))

def List.sum : List Nat → Nat := List.foldl (.+.) 0 

def List.interweave {α : Type} (xs ys : List α) : List α := List.foldl (λ a ↦ (λ (x, y) ↦ a ++ [x, y])) [] (List.zip xs ys)

def List.cumSum : List Nat → List Nat := List.foldl (λ nums ↦ (λ n ↦ nums ++ [nums.getLast! + n])) [0]

def dummy : Nat := 10000000

def IDList (nums : List Nat) : List Nat := List.interweave (List.range (lastID nums + 1)) (List.replicate ((lastID nums) + 1) dummy)

def pairWithID (nums : List Nat) : List (Nat × Nat) := List.zip nums (IDList nums)

-- (size, pos), gaps with pos → (insert, newgaps)
def tryInsert : (Nat × Nat) → List (Nat × Nat) → (Nat × List (Nat × Nat))
  | (size, pos), gaps => let potential := List.filter (λ (_, (_, gap)) ↦ gap ≥ size) (List.enum gaps);
                         match potential.length with
                         | 0 => (pos, gaps)
                         | _ => if potential.head!.snd.fst ≥ pos then (pos, gaps) else (potential.head!.snd.fst, gaps.set (potential.head!.fst) (potential.head!.snd.fst + size, potential.head!.snd.snd - size))

def gaps (str : String) : List (Nat × Nat) := List.map (λ ((size, _), pos) ↦ (pos, size)) $ List.filter (λ ((_, id), _) ↦ id==dummy) (List.zip (pairWithID $ numeralData str) (numeralData str).cumSum)

-- To insert (Id, size, pos), gaps, end positions (Id, size, pos)
def insertAll : List (Nat × Nat × Nat) → List (Nat × Nat) → List (Nat × Nat × Nat)
  | [], _ => []
  | ((id, size, pos) :: xs), gaps => let (newpos, newgaps) := tryInsert (size, pos) gaps;
                                     (id, size, newpos) :: (insertAll xs newgaps)

def idSizePos (str : String) :List (Nat × Nat × Nat) := List.map (λ (size, id, pos) ↦ (id, size, pos)) $ List.filter (λ (_, id, _) ↦ id ≠ dummy) (List.zip (numeralData str) (List.zip (IDList $ numeralData str) (numeralData str).cumSum))

def setN : List Char → List (Nat × Char) → List Char
  | chars, [] => chars
  | chars, ((pos, x) :: xs) => setN (chars.set pos x) xs

def answerString : List (Nat × Nat × Nat) → List Char → List Char
  | [], ans => ans
  | ((id, size, pos) :: xs), ans => if pos ≥ ans.length then answerString xs (ans ++ (List.replicate (pos-ans.length) '.') ++ (List.replicate size (Nat.digitChar id)))
                                    else answerString xs (setN ans (List.zip (List.rangeFrom pos (pos+size)) (List.replicate size (Nat.digitChar id))))

def calcChecksum : (Nat × Nat × Nat) → Nat
  | (ID, size, pos) => List.sum $ List.map (λ (x, y) ↦ x*y) (List.zip (List.rangeFrom pos (pos+size)) (List.replicate size ID)) 

def answer (str : String) : Nat := List.sum $ List.map calcChecksum $ insertAll (idSizePos str).reverse (gaps str)
