-- >>> main
-- 1349

import Control.Monad.State

main :: IO Int
main = do
       x <- readFile "input.txt"
       pure (part2 x)

toSnd :: (a -> b) -> a -> (a, b)
toSnd f a = (a , f a)

part1 :: String -> Int
part1 = overFour . toSnd toCount . map (map (=='@')) . lines

columns :: [[a]] -> [[a]]
columns xs = [map (!!i) xs | i <- [0..length (head xs) - 1]]

toGrids :: [[a]] -> [[[[a]]]]
toGrids xs = [[map (take 2) r] ++ toCols (columns r) ++ [map (drop (length (head r) - 2)) r] | r <- rows]
 where
  firstrow = [take 2 xs]
  lastrow = [drop (length xs - 2) xs]
  rows = firstrow ++ zipWith (\ (x , y) z -> [x, y, z]) (zip xs (tail xs)) (tail (tail xs)) ++ lastrow
  toCols xs = zipWith (\ (x , y) z -> [x, y, z]) (zip xs (tail xs)) (tail (tail xs))

toCount :: [[Bool]] -> [[Int]]
toCount = map (map (sum . map (foldr (\x y -> if x then y + 1 else y) 0))) . toGrids

overFour :: ([[Bool]], [[Int]]) -> Int
overFour (bss, xss) = sum [1 | (bs, xs) <- zip bss xss, (b, x) <- zip bs xs, b, x <= 4]

part2 :: String -> Int
part2 s = execState ((helper . map (map (=='@')) . lines) s) 0

helper :: [[Bool]] -> State Int ()
helper bss = do
             let (bss', x) = (newGrid . toSnd toCount) bss
             modify (+x)
             if x == 0 then return ()
                       else helper bss' 

newGrid :: ([[Bool]], [[Int]]) -> ([[Bool]], Int)
newGrid (bss, xss) = ([[if b && (x <= 4) then False else b | (b, x) <- zip bs xs] | (bs, xs) <- zip bss xss], overFour (bss, xss))

