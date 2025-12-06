import Data.List
import Data.List.Split

main :: IO Int
main = do
       x <- readFile "input.txt"
       pure (part2 x)

detOp :: String -> Int -> Int -> Int
detOp "+" = (+)
detOp "*" = (*)

start :: String -> Int
start "+" = 0
start "*" = 1

part1 :: String -> Int
part1 s = sum [foldr (detOp op) (start op) xs | (op, xs) <- zip ops nums]
 where
  (ops : numss) = reverse $ map words $ lines s

  nums :: [[Int]]
  nums = transpose $ map (map read) numss

part2 :: String -> Int
part2 s = sum [foldr (detOp op) (start op) xs | (op, xs) <- zip ops nums]
 where
  (ops' : nums') = reverse $ lines s
  ops = words ops'
  nums'' = transpose (reverse nums')

  nums :: [[Int]]
  nums = map (map read) $ splitOn [replicate (length (head nums'')) ' '] nums''
