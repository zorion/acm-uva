main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.sum.(map findRedundants).(map reorder).getInput

getInput :: String -> [(Int, Int, Int, Int)]
getInput = (map split4).lines

split4 :: String -> (Int, Int, Int, Int)
split4 s = (read a, read b, read c, read d)
    where
        (a, b) = split2 '-' x
        (c, d) = split2 '-' y
        (x, y) = split2 ',' s

split2 :: Char -> String -> (String, String)
split2 d s = (a, tail b)
    where (a, b) = break (==d) s

reorder :: (Int, Int, Int, Int) -> (Int, Int, Int, Int)
reorder (w,x,y,z) = (a,b,c,d)
    where
        minmax p q = (min p q, max p q)
        (a, b) = minmax w x
        (c, d) = minmax y z

findRedundants :: (Int, Int, Int, Int) -> Int
findRedundants (w, x, y, z)
    | and [(w <= z), (x >= y)] = 1
    | and [(y <= x), (z >= w)] = 1
    | otherwise = 0

