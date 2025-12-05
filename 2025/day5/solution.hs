import Data.List.Split (splitOn)
import Data.List (sort)

main :: IO Int
main = do
       x <- readFile "input.txt"
       pure (part2 x)

newtype Range = R(Int, Int)
                     deriving (Show, Eq)

parseRange :: String -> Range
parseRange s = R(read a, read b)
 where
  (a : b :_) = splitOn "-" s

mergeRange :: Range -> [Range] -> [Range]
mergeRange (R(a, b)) [] = [R(a, b)]
mergeRange (R(a, b)) (R(c, d) : xs) | a <= c && b < c  = R(a, b) : R(c, d) : xs
                                    | a <= c && b <= d = R(a, d) : xs
                                    | a <= c           = mergeRange (R(a, b)) xs
                                    | a <= d && b <= d = R(c, d) : xs
                                    | a <= d           = mergeRange (R(c, b)) xs
                                    | otherwise        = R(c, d) : mergeRange (R(a, b)) xs



part1 :: String -> Int
part1 s = findValid (foldr (mergeRange . parseRange) [] ranges) (sort $ map (\x -> read x :: Int) items)
 where
  (ranges : items : _) = map lines $ splitOn "\n\n" s

findValid :: [Range] -> [Int] -> Int
findValid _ [] = 0
findValid [] xs = 0
findValid (R(a,b) : rs) (x : xs) | a <= x && x <= b = 1 + findValid (R(x, b) : rs) xs
                                 | b <= x = findValid rs (x : xs)
                                 | otherwise = findValid (R(a, b) : rs) xs

part2 :: String -> Int
part2 s = sum $ map (\(R(a, b)) -> b - a + 1) $ foldr (mergeRange . parseRange) [] ranges
 where
  (ranges : items : _) = map lines $ splitOn "\n\n" s
