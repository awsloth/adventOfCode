import Data.Char

splitOnChar :: Char -> String -> [String]
splitOnChar c [] = []
splitOnChar c xs = helper [] xs
    where
        helper :: String -> String -> [String]
        helper xs [] = [xs]
        helper xs (y : ys) | y == c = xs : helper [] ys
                           | otherwise = helper (xs ++ [y]) ys


strToInt :: String -> Int
strToInt [] = 0
strToInt [x] = digitToInt x
strToInt (x : xs) = digitToInt x * (10 ^ length xs) + strToInt xs 

intToStr :: Int -> String
intToStr x = _

seeds :: String -> [Int]
seeds xs = map strToInt (tail (splitOnChar ' ' xs))

listStr :: [Int] -> String
listStr (x : xs) = intToDigit x :", " ++ listStr xs

main :: IO()
main = do
    contents <- readFile "data.txt"
    let lines = splitOnChar '\n' contents in putStrLn $ listStr (seeds (head lines))
