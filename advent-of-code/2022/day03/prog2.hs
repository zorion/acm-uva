import Data.Char

main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.sum.(map translate).(map head).(map findIntersection3).group3.getInput

getInput :: String -> [String]
getInput = lines

group3 :: [String] -> [(String, String, String)]
group3 [] = []
group3 (x:y:z:xs) = [(x, y, z)] ++ (group3 xs)

findIntersection :: ([Char], [Char]) -> [Char]
findIntersection (xs, ys) = filter (`elem` ys) xs

findIntersection3 :: ([Char], [Char], [Char]) -> [Char]
findIntersection3 (xs, ys, zs) = findIntersection (findIntersection (xs, ys), zs)

translate :: Char -> Int
translate x
    | ord(x) < ord('a') = ord(x) - ord('A') + 27
    | ord(x) >= ord('a') = ord(x) - ord('a') + 1
