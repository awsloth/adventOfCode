import Data.List
import Data.List.Split
import GHC.Float

main :: IO ()
main = do
       x <- readFile "input.txt"
       print $ part2 x

type Vertex = (Int, Int, Int)
type Edge = ((Vertex, Vertex), Float)

nTimes :: Int -> (a -> a) -> a -> a
nTimes 1 f a = f a
nTimes n f a = f (nTimes (n-1) f a)

part1 :: String -> Int
part1 s = calcScore . reverse . sort . map length $ fst $ nTimes 1000 doStep ([], sortOn snd $ findWeights $ map ((\(x : y : z : _) -> (read x, read y, read z)) . splitOn ",") $ lines s)

calcScore :: [Int] -> Int
calcScore (x : y : z : _) = x * y * z

dist :: Vertex -> Vertex -> Float
dist (x, y, z) (a, b, c) = sqrt (int2Float ((x - a)^2 + (y - b)^2 + (z - c)^2))

findWeights :: [Vertex] -> [Edge]
findWeights [] = []
findWeights (x : xs) = [((x, y), dist x y) | y <- xs] ++ findWeights xs

doStep :: ([[Vertex]], [Edge]) -> ([[Vertex]], [Edge])
doStep (vss, []) = (vss, [])
doStep (vss, e@((a, b), _) : es) | bothInOne vss e = (vss, es)
                                 | inAny vss e = (insertEdge vss e, es)
                                 | otherwise = ([a, b] : vss, es)

bothInOne :: [[Vertex]] -> Edge -> Bool
bothInOne vss ((a, b), _) = any (\vs -> a `elem` vs && b `elem` vs) vss

inAny :: [[Vertex]] -> Edge -> Bool
inAny vss ((a, b), _) = any (\vs -> a `elem` vs || b `elem` vs) vss

insertEdge :: [[Vertex]] -> Edge -> [[Vertex]]
insertEdge (vs : vss) e@((a, b), _) | a `elem` vs = let other = filter (elem b) vss in
                                                      if null other then (b : vs) : vss
                                                                    else (vs ++ head other) : filter (notElem b) vss
                                    | b `elem` vs = let other = filter (elem a) vss in
                                                      if null other then (a : vs) : vss
                                                                    else (vs ++ head other) : filter (notElem a) vss
                                    | otherwise = vs : insertEdge vss e

part2 :: String -> Int
part2 s = findEdge $ nTimes (1000 - 2) doStep' ([], sortOn snd $ findWeights $ map ((\(x : y : z : _) -> (read x, read y, read z)) . splitOn ",") $ lines s)

calc :: Edge -> Int
calc (((a,_,_), (b,_,_)), _) = a * b

doStep' :: ([[Vertex]], [Edge]) -> ([[Vertex]], [Edge])
doStep' (vss, []) = (vss, [])
doStep' (vss, e@((a, b), _) : es) | bothInOne vss e = doStep' (vss, es)
                                  | inAny vss e = (insertEdge vss e, es)
                                  | otherwise = ([a, b] : vss, es)

findEdge :: ([[Vertex]], [Edge]) -> Int
findEdge (vss, []) = 0
findEdge (vss, e@((a@(x,_,_), b@(y,_,_)), _) : es) | bothInOne vss e = findEdge (vss, es)
                                                   | inAny vss e = x * y
                                                   | otherwise = x * y


