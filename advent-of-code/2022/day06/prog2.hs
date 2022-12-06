main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.(map (getDiffChar 14)).lines

getDiffChar :: Int -> String -> Int
getDiffChar n xs = aux n xs []
    where aux 0 xs' ys = gdAux n xs' ys
          aux m (x:xs') ys = aux (m-1) xs' (ys++[x])

gdAux4 :: Char -> Char -> Char -> Char -> Int -> String -> Int
gdAux4 a b c d n [] = n
gdAux4 a b c d n (x:xs)
    | not (repeated [a,b,c,d]) = n
    | otherwise = gdAux4 b c d x (n+1) xs

gdAux :: Int -> String -> String -> Int
gdaux n [] (y:ys) = n
gdAux n (x:xs) (y:ys)
    | not (repeated (y:ys)) = n
    | otherwise = gdAux (n+1) xs (ys ++ [x])



repeated [] = False
repeated (x:xs)
    | elem x xs = True
    | otherwise = repeated xs
