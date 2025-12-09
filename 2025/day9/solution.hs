import Data.Function
import Data.Maybe
import Data.List.Split
import Data.List

main :: IO ()
main = do
       x <- readFile "input.txt"
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

inGreen :: [Point] -> (Point, Point) -> Bool
inGreen xs (a, b) | null inside && null onedge = noLinesThrough outside
                  | null inside = all notthrough onedge && noLinesThrough outside
                  | otherwise = False
 where
  maxx = max (fst a) (fst b)
  minx = min (fst a) (fst b)

  maxy = max (snd a) (snd b)
  miny = min (snd a) (snd b)

  shiftround = tail (tail xs) ++ [head xs, head (tail xs)]

  inside = [1 | (x, y) <- xs, x < maxx, minx < x, y < maxy, miny < y]
  outside = [(x,y) | (x, y) <- xs, x > maxx || minx > x || y > maxy || miny > y]
  onedge = [(x, y, z) | (x, (y, z)) <- zip xs (zip (tail xs ++ [head xs]) shiftround), y /= a, y /= b, ontop y || onbottom y || onleft y || onright y]

  onleft    (a, b) = a == minx && miny <= b && b <= maxy
  onright (a, b) = a == maxx && miny <= b && b <= maxy
  onbottom (a, b) = b == maxy && minx <= a && a <= maxx
  ontop (a, b) = b == miny && minx <= a && a <= maxx
  corner (a, b) =  a == minx && (b == miny || b == maxy)
                || a == maxx && (b == miny || b == maxy)


  notthrough ((v, w), e, (x, y)) | corner e   = validCorner e
                                 | ontop e    = y <= snd e && w <= snd e
                                 | onbottom e = y >= snd e && w >= snd e
                                 | onright e  = x >= fst e && v >= fst e
                                 | onleft e   = x <= fst e && v <= fst e
 
  validCorner :: Point -> Bool
  validCorner e | fromJust (elemIndex e xs) < fromJust (elemIndex b xs) && fromJust (elemIndex e xs) > fromJust (elemIndex a xs) = validHelper' e
                | otherwise = validHelper e
               
  
  validHelper :: Point -> Bool
  validHelper e | fst a <= fst b && snd a <= snd b = fst e == fst a
                | fst a <= fst b && snd a >= snd b = fst e == fst b
                | fst a >= fst b && snd a <= snd b = fst e == fst b
                | fst a >= fst b && snd a >= snd b = fst e == fst a

  validHelper' :: Point -> Bool
  validHelper' e | fst a <= fst b && snd a <= snd b = fst e == fst b
                 | fst a <= fst b && snd a >= snd b = fst e == fst a
                 | fst a >= fst b && snd a <= snd b = fst e == fst a
                 | fst a >= fst b && snd a >= snd b = fst e == fst b

  verts = [fst x | x <- outside, y <- outside, fst x == fst y, x /= y, minx <= fst x, fst x <= maxx, min (snd x) (snd y) <= miny, maxy <= max (snd x) (snd y)]
  hors  = [snd y | x <- outside, y <- outside, snd x == snd y, x /= y, miny <= snd x, snd x <= maxy, min (fst x) (fst y) <= minx, maxx <= max (fst x) (fst y)]
  noLinesThrough xs = null (verts ++ hors)
