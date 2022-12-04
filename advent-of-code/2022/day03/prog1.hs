import Data.Char

main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.sum.(map translate).(map head).(map findIntersection).getInput

getInput :: String -> [([Char], [Char])]
getInput = (map splitLine).lines

splitLine :: String -> ([Char], [Char])
splitLine x = (take n x, drop n x)
    where n = div (length x) 2

findIntersection :: ([Char], [Char]) -> [Char]
findIntersection (xs, ys) = filter (`elem` ys) xs

translate :: Char -> Int
translate x
    | ord(x) < ord('a') = ord(x) - ord('A') + 27
    | ord(x) >= ord('a') = ord(x) - ord('a') + 1
