import Control.Monad.State

main :: IO Integer
main = do
       x <- readFile "input.txt"
       pure (evalState (part2 $ lines x) 50)

changeState :: String -> Integer -> Integer
changeState ('L' : a) x = (x - (read a :: Integer)) `mod` 100
changeState ('R' : a) x = (x + (read a :: Integer)) `mod` 100

part1 :: [String] -> State Integer Integer
part1 [] = pure 0
part1 (c : xs) = do
                 modify (changeState c)
                 x <- get
                 y <- part1 xs
                 if x == 0
                   then pure (y + 1)
                   else pure y

throughZero :: String -> Integer -> Integer
throughZero ('L' : a) x = let (d, m) = divMod (read a :: Integer) 100 in
                           d + (if (x - m) > 0 || x == 0 then 0 else 1)
throughZero ('R' : a) x = let (d, m) = divMod (read a :: Integer) 100 in
                           d + (if (x + m) > 99 then 1 else 0)

part2 :: [String] -> State Integer Integer
part2 [] = pure 0
part2 (c : xs) = do
                 x <- get
                 modify (changeState c)
                 y <- part2 xs
                 pure (y + throughZero c x)
