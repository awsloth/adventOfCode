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

#eval sumProd $ toNums $ validNums $ filterComma $ splitOnComma $ filterLeft $ removeBlanks $ filterLength $ filterRight  (singleLine.splitOn "mul")
