import Data.Char (digitToInt)
import Data.List (elemIndex)
import Data.Maybe (fromJust)

main :: IO Int
main = do
       x <- readFile "input.txt"
       pure (part1 $ lines x)

findMaxGen :: Int -> [Int] -> Int
findMaxGen 1 xs = maximum xs
findMaxGen x xs = 10^(x-1)*s + findMaxGen (x - 1) (drop (fromJust (elemIndex s xs) + 1) xs)
 where
  s :: Int
  s = maximum (take (length xs - x + 1) xs)

part1 :: [String] -> Int
part1 = foldr ((+) . findMaxGen 2 . map digitToInt) 0

part2 :: [String] -> Int
part2 = foldr ((+) . findMaxGen 12 . map digitToInt) 0

