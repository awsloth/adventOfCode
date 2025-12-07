import Data.List
import Data.List.Split

main :: IO ()
main = do
       x <- readFile "input.txt"
       print $ part2 x

type Grid = [[Char]]

part1 :: String -> Int
part1 = countSplits . runAutomata . lines

nTimes :: Int -> (a -> a) -> a -> a
nTimes 1 f a = f a
nTimes n f a = f (nTimes (n-1) f a)

runAutomata :: Grid -> Grid
runAutomata g = nTimes (length g) automataStep g

getRelArea :: Grid -> [[Grid]]
getRelArea g = [take 2 xs : cols xs ++ [drop (length xs - 2) xs] | xs <- rows]
 where
  rows = map transpose $ zipWith (\x y -> [x, y]) g (tail g)
  cols xs = zipWith (:) xs (zipWith (\x y -> [x, y]) (tail xs) (tail (tail xs)))

automataStep :: Grid -> Grid
automataStep g = head g : [[getSymb c a | (c, a) <- row] | row <- zipWith zip (tail g) (getRelArea g)]

getSymb :: Char -> Grid -> Char
getSymb '.' [_, "S."] = '|'
getSymb '.' ["S.", _] = '|'
getSymb '.' [_, "S.", _] = '|'
getSymb '.' [_, "|."] = '|'
getSymb '.' ["|.", _] = '|'
getSymb '.' [_, "|.", _] = '|'
getSymb '.' [_, "|^"] = '|'
getSymb '.' ["|^", _] = '|'
getSymb '.' [_, _ , "|^"] = '|'
getSymb '.' ["|^", _, _] = '|'
getSymb c _ = c

countSplits :: Grid -> Int
countSplits g = sum $ map ((\y -> y - 1).length . splitOn "|^") $ transpose g

type GridLayered = [[(Char, Int)]]

part2 :: String -> Int
part2 = countPaths . runAutomata' . map (map (, 0)) . lines

runAutomata' :: GridLayered -> GridLayered
runAutomata' g = nTimes (length g) automataStep' g

getRelArea' :: GridLayered -> [[GridLayered]]
getRelArea' g = [take 2 xs : cols xs ++ [drop (length xs - 2) xs] | xs <- rows]
 where
  rows = map transpose $ zipWith (\x y -> [x, y]) g (tail g)
  cols xs = zipWith (:) xs (zipWith (\x y -> [x, y]) (tail xs) (tail (tail xs)))

automataStep' :: GridLayered -> GridLayered
automataStep' g = head g : [[updateSymb i c a | (i, (c, a)) <- zip [0..length row -1] row] | row <- zipWith zip (tail g) (getRelArea' g)]

updateSymb :: Int -> (Char, Int) -> GridLayered -> (Char, Int)
updateSymb _ ('.', _) [_, [('S', _), ('.', _)]]     = ('|', 1)
updateSymb _ ('.', _) [[('S', _), ('.', _)], _]     = ('|', 1)
updateSymb _ ('.', _) [_, [('S', _), ('.', _)], _]  = ('|', 1)
updateSymb _ ('.', _) [[('|', i), ('^', _)], [('|', j), _], [('|', k), ('^', _)]]  = ('|', i + j + k)
updateSymb _ ('.', _) [[('|', i), ('^', _)], _, [('|', j), ('^', _)]]  = ('|', i + j)
updateSymb _ ('.', _) [[('|', i), _], [('|', j), ('^', _)]]     = ('|', i + j)
updateSymb _ ('.', _) [[('|', i), ('^', _)], [('|', j), _]]     = ('|', i + j)
updateSymb _ ('.', _) [_, [('|', i), _] , [('|', j), ('^', _)]] = ('|', i + j)
updateSymb _ ('.', _) [[('|', i), ('^', _)], [('|', j), _], _]  = ('|', i + j)
updateSymb a ('.', _) [_, [('|', i), ('.', _)]]     = if a == 0 then ('.', 0) else ('|', i)
updateSymb 0 ('.', _) [[('|', i), ('.', _)], _]     = ('|', i)
updateSymb _ ('.', _) [_, [('|', i), ('.', _)], _]  = ('|', i)
updateSymb _ ('.', _) [_, [('|', i), ('^', _)]]     = ('|', i)
updateSymb _ ('.', _) [[('|', i), ('^', _)], _]     = ('|', i)
updateSymb _ ('.', _) [_, _ , [('|', i), ('^', _)]] = ('|', i)
updateSymb _ ('.', _) [[('|', i), ('^', _)], _, _]  = ('|', i)
updateSymb _ c _ = c

countPaths :: GridLayered -> Int
countPaths g = sum $ map snd $ filter (\(x, y) -> x == '|') $ last g
