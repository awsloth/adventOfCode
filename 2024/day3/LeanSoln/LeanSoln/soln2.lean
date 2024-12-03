import LeanSoln.data

def singleLine : String := List.foldl (λ x ↦ (λ y ↦ x ++ y)) "" (data.splitOn "\n")

-- Cut down to right bracket
def filterRight : List String → List String := List.map (λ x ↦ (List.takeWhile (λ y ↦ y ≠ ')') x.data).asString)

-- Cut down based on size (9 total for biggest possible)
def filterLength : List String → List String := List.filter (λ x ↦ x.length ≤ 8)

def removeBlanks : List String → List String := List.filter (λ x ↦ x ≠ "")

-- Cut down left bracket
def filterLeft (xs : List String) : List String := List.map (λ x ↦ x.data.tail.asString) (List.filter (λ x ↦ x.data.head! = '(') xs)

-- Split on comma
def splitOnComma : List String → List (List String) := List.map (λ x ↦ x.splitOn ",")

-- Valid number
def validNum (xs : String) : Bool := Bool.and (List.all (List.map Char.isDigit xs.data) (λ x ↦ x)) (xs.length ≤ 3)

-- Cut lines that have more than 1 comma or none
def filterComma : List (List String) → List (List String) := List.filter (λ x ↦ Bool.not (x.length ≠ 2))

def validNums : List (List String) → List (List String) := List.filter (λ x ↦ List.all x validNum)

def toNums : List (List String) → List (List Int) := List.map (λ x ↦ List.map (λ y ↦ y.toInt!) x)

def prod : List Int → Int
  | [] => 1
  | (x :: xs) => x * (prod xs)

def sum : List Int → Int
  | [] => 0
  | (x :: xs) => x + (sum xs)

def sumProd (xs : List (List Int)) : Int := sum (List.map (λ x ↦ prod x) xs)

def containsDont (s : String) : Bool := (s.splitOn "don't()").length ≥ 2

def containsDo (s : String) : Bool := (s.splitOn "do()").length ≥ 2

def mulCommands : List String := singleLine.splitOn "mul"

def enumMuls : List (Nat × String) := List.zip (List.range mulCommands.length) mulCommands

def offPoints : List Nat := List.map (λ x ↦ x.fst) (List.filter (λ x ↦ containsDont x.snd) enumMuls)
 
def onPoints : List Nat := List.map (λ x ↦ x.fst) (List.filter (λ x ↦ containsDo x.snd) enumMuls)

def repeatn : Bool → Nat → List Bool
  | _, 0 => []
  | b, Nat.succ n => b :: (repeatn b n)

def offBools : List (Nat × Bool) := List.zip offPoints (repeatn false offPoints.length)
def onBools : List (Nat × Bool) := List.zip onPoints (repeatn true onPoints.length)

def insert : Nat × Bool → List (Nat × Bool) → List (Nat × Bool)
  | (x, b) , [] => [(x, b)]
  | (x, b) , ((y, b1) :: ys) => if (x < y) then (x, b) :: ((y, b1) :: ys) else (y, b1) :: (insert (x, b) ys)

def listSort : List (Nat × Bool) → List (Nat × Bool)
  | [] => []
  | (x :: xs) => insert x (listSort xs)

def changes : List (Nat × Bool) → List Nat
  | [] => []
  | ((x, b) :: []) => if b then [] else [x]
  | ((_, b) :: ((y, b2) :: [])) => (if (b == b2) then [] else [y])
  | ((_, b) :: ((y, b2) :: xs)) => (if (b == b2) then [] else [y]) ++ changes ((y, b2) :: xs)

-- non-inclusive start and end
def range (se : Nat × Nat) : List Nat := List.map (.+se.fst + 1) (List.range (se.snd - se.fst - 1))

def pairUp : List Nat → List (Nat × Nat)
  | [] => []
  | (_ :: []) => []
  | (x :: (y :: xs)) => (x, y) :: (pairUp xs)

def flatten : List (List Nat) → List Nat
  | [] => []
  | (x :: xs) => x ++ (flatten xs)

def onOffChanges : List Nat := changes (listSort ([(0, true)] ++ onBools ++ offBools))

def onRange : List Nat := 0 :: flatten (List.map range (pairUp (0 :: onOffChanges ++ [mulCommands.length])))

def onOffBools : List Bool := List.map (λ x ↦ onRange.contains x) (List.range (mulCommands.length))

def filterOns : List String := List.map (λ x ↦ x.fst) (List.filter (λ x ↦ x.snd) (List.zip mulCommands onOffBools))

def fringes : List String := List.map (λ x ↦ mulCommands.get! x) onOffChanges

def takeOdd : List String → List String
  | [] => []
  | (x :: []) => [x]
  | (x :: (_ :: xs)) => x :: takeOdd xs

def dontFringes : List String := takeOdd fringes

def dontcommands : List String := List.map (λ x ↦ (x.splitOn "don't()").head!) dontFringes

def allCommands : List String := filterOns ++ dontcommands

#eval sumProd $ toNums $ validNums $ filterComma $ splitOnComma $ filterLeft $ removeBlanks $ filterLength $ filterRight $ allCommands 

-- 77152269 (too big)
-- 72847295 (no comment)
-- 77058504 (no comment)
-- 74361272
