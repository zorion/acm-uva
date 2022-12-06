main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.(map getDiffChar).lines

getDiffChar :: String -> Int
getDiffChar (a:b:c:d:xs) = gdAux a b c d 4 xs

gdAux :: Char -> Char -> Char -> Char -> Int -> String -> Int
gdAux a b c d n [] = n
gdAux a b c d n (x:xs)
    | not (repeated a b c d) = n
    | otherwise = gdAux b c d x (n+1) xs

repeated a b c d
    | elem a [b, c, d] = True
    | elem b [c, d] = True
    | otherwise = (c==d)
