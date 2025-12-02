-- >>> main
-- 20942028255

import Data.List

main :: IO Integer
main = do
       x <- readFile "input.txt"
       pure (part2 (split ',' (dropLast x)))

dropLast :: String -> String
dropLast [x] = []
dropLast (x : xs) = x : dropLast xs

split :: Char -> String -> [String]
split _ [] = []
split c [x] | c == x = []
            | otherwise = [[x]]
split c (a : x : s) | x == c = [a] : split c s
                    | otherwise = (a : head (split c (x : s))) : tail (split c (x : s))

newtype Range = Range (String, String) deriving (Show)

part1 :: [String] -> Integer
part1 s = sum $ map countNums $ concatMap (chunkRange . toRange) s

toRange :: String -> Range
toRange s = let xs = split '-' s in Range (head xs, (head . tail) xs)

chunkRange :: Range -> [Range]
chunkRange (Range (a , b)) | length a == length b && even (length a) = [Range (a , b)]
                           | length a == length b && odd (length a)  = []
                           | otherwise = let (lower, upper) = (length a, length b) in
                                          [Range (a, replicate lower '9') | even lower] ++
                                          [Range ("1" ++ replicate (upper-1) '0', b) | even upper] ++
                                          [Range ("1" ++ replicate (x-1) '0', replicate x '9') | x <- [lower+1..upper-1], even x]

countNums :: Range -> Integer
countNums (Range (a , b)) = let (la , lb) = (length a `div` 2, length b `div` 2) in
                             let leftbound = (read (take la a) :: Integer) + (if (read (take la a) :: Integer) >= read (drop la a) then 0 else 1) in
                             let rightbound = (read (take lb b) :: Integer) + (if (read (take lb b) :: Integer) <= read (drop lb b) then 0 else (-1)) in
                              sum [read (show x ++ show x) :: Integer | x <- [leftbound .. rightbound]]

part2 :: [String] -> Integer
part2 s = sum $ map countNums' $ concatMap (chunkRange' . toRange) s

chunkRange' :: Range -> [Range]
chunkRange' (Range (a , b)) | length a == length b = [Range (a, b)]
                            | otherwise = let (lower, upper) = (length a, length b) in
                                 [Range (a, replicate lower '9')] ++
                                 [Range ("1" ++ replicate (upper-1) '0', b)] ++
                                 [Range ("1" ++ replicate (x-1) '0', replicate x '9') | x <- [lower+1..upper-1]]

factors :: Int -> [Int]
factors a = [x | x <- [1..(a - 1)], a `mod` x == 0]

countNums' :: Range -> Integer
countNums' (Range (a, b)) = sum $ nub $ concatMap (nums (Range (a, b))) (factors (length a))

nums :: Range -> Int -> [Integer]
nums (Range (a, b)) x = let d = (length a `div` x) in
                         [repeated y d | y <- [(read (take x a) :: Integer)..(read (take x b) :: Integer)], repeated y d >= (read a :: Integer), repeated y d <= (read b :: Integer)]

repeated :: Integer -> Int -> Integer
repeated s x = read (concat (replicate x (show s))) :: Integer
