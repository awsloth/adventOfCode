import Data.Function
import Data.Maybe
import Data.List.Split
import Data.List

main :: IO ()
main = do
       x <- readFile "test.txt"
       print $ part2 x

type Point = (Int, Int)

part1 :: String -> Int
part1 = maximum . map area . allPairs . findRed

area :: (Point, Point) -> Int
area ((a, b), (x, y)) = (abs (x - a) + 1) * (abs (y - b) + 1)

allPairs :: [a] -> [(a, a)]
allPairs [] = []
allPairs (x : xs) = [(x, y) | y <- xs] ++ allPairs xs

findRed :: String -> [Point]
findRed s = map ((\(x : y :_) -> (read x, read y)) . splitOn ",") $ lines s

-- part2 :: String -> Int
part2 s = maximum . map area . filter (inGreen points) $ allPairs points
 where
  points = findRed s

inside :: Point -> Point -> Point -> Bool
inside (a, b) (c, d) (x, y) = x < max a c && x > min a x && y < max b d && y > min b d

onleft   (a, b) (c, d) (x, y) = x == min a c && min b d <= y && y <= max b d
onright  (a, b) (c, d) (x, y) = x == max a c && min b d <= y && y <= max b d
onbottom (a, b) (c, d) (x, y) = y == max b d && min a c <= x && x <= max a c
ontop    (a, b) (c, d) (x, y) = y == min b d && min a c <= x && x <= max a c
corner   (a, b) (c, d) (x, y) = (x == a || x == c) && (y == b || y == d)

edge :: Point -> Point -> [Point] -> [(Point, Point, Point)]
edge a b xs = [(x, y, z) | (x, (y, z)) <- zip xs (zip (tail xs ++ [head xs]) (tail (tail xs) ++ [head xs, head (tail xs)])), y /= a, y /= b, ontop a b y || onbottom a b y || onleft a b y || onright a b y]

noLinesThrough :: (Point, Point) -> [Point] -> Bool
noLinesThrough (a, b) xs = null [(x, y) | (x, y) <- zip xs (tail xs ++ [head xs]), (verticalLine (x, y) && (fst x == fst y)) || (horizontalLine (x, y) && (snd x == snd y))]
 where
  verticalLine (x, y) = min (snd x) (snd y) < min (snd a) (snd b)
                      && max (snd x) (snd y) > max (snd a) (snd b)
  horizontalLine (x, y) = min (fst x) (fst y) < min (fst a) (fst b)
                      && max (fst x) (fst y) > max (fst a) (fst b)

inGreen :: [Point] -> (Point, Point) -> Bool
inGreen xs (a, b) = not (any (inside a b) xs)
                  && all notthrough (edge a b xs)
                  && noLinesThrough (a, b) xs
 where
  notthrough ((v, w), e, (x, y)) | corner a b e   = validCorner e
                                 | ontop a b e    = y <= snd e && w <= snd e
                                 | onbottom a b e = y >= snd e && w >= snd e
                                 | onright a b e  = x >= fst e && v >= fst e
                                 | onleft a b e   = x <= fst e && v <= fst e
 
  validCorner :: Point -> Bool
  validCorner e | fromJust (elemIndex e xs) < fromJust (elemIndex b xs)
               && fromJust (elemIndex e xs) > fromJust (elemIndex a xs) = validHelper b a e
                | otherwise = validHelper a b e
               
  validHelper :: Point -> Point -> Point -> Bool
  validHelper a b e | fst a <= fst b && snd a <= snd b = fst e == fst a
                    | fst a <= fst b && snd a >= snd b = fst e == fst b
                    | fst a >= fst b && snd a <= snd b = fst e == fst b
                    | fst a >= fst b && snd a >= snd b = fst e == fst a
