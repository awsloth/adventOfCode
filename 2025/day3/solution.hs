import Data.Char
import Data.List

main :: IO Int
main = do
       x <- readFile "input.txt"
       pure (part2 $ lines x)

dropLast :: [a] -> [a]
dropLast [x] = []
dropLast (x : xs) = x : dropLast xs

part1 :: [String] -> Int
part1 = foldr ((+) . findMax . map digitToInt) 0

findMax :: [Int] -> Int
findMax xs = let s = maximum (dropLast xs)
              in
               case elemIndex s xs of
                Nothing -> undefined
                (Just i) -> 10*s + maximum (drop (i + 1) xs)

part2 :: [String] -> Int
part2 = foldr ((+) . findMaxGen 12 . map digitToInt) 0

findMaxGen :: Int -> [Int] -> Int
findMaxGen 1 xs = maximum xs
findMaxGen x xs = let s = maximum (take (length xs - x + 1) xs)
                   in
                    case elemIndex s xs of
                     Nothing -> undefined
                     (Just i) -> (10^(x-1)*s) + findMaxGen (x - 1) (drop (i + 1) xs)
