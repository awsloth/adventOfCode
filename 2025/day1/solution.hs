-- >>> main
-- 5978

main :: IO Integer
main = do
       x <- readFile "input.txt"
       pure (snd . soln . reverse $ lines x)

soln :: [String] -> (Integer , Integer)
soln [] = (50 , 0)
soln (('L' : a) : xs) = let (x, y) = soln xs in
                         let x' = (x - (read a :: Integer)) `mod` 100 in
                          if x - (read a :: Integer) > 0
                             then (x', y)
                             else (x', if x == 0 then y + ((read a :: Integer) - x) `div` 100 else y + 1 + ((read a :: Integer) - x) `div` 100)
soln (('R' : a) : xs) = let (x, y) = soln xs in
                         let x' = (x + (read a :: Integer)) `mod` 100 in
                          if x + (read a :: Integer) < 100
                             then (x', y)
                             else (x', y + 1 + ((read a :: Integer) - (100 - x)) `div` 100)

