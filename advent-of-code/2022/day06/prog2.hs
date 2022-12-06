main :: IO ()
main = do
    interact prob1
    putStrLn ""


prob1 :: String -> String
prob1 = show.(map (getDiffChar 14)).lines


getDiffChar :: Int -> String -> Int
getDiffChar n xs = getAllDiffPosition n (drop n xs) (take n xs)


getAllDiffPosition :: Int -> String -> String -> Int
getAllDiffPosition n [] (y:ys) = n
getAllDiffPosition n (x:xs) (y:ys)
    | not (hasRepeated (y:ys)) = n
    | otherwise = getAllDiffPosition (n+1) xs (ys ++ [x])


hasRepeated :: Eq a => [a] -> Bool
hasRepeated [] = False
hasRepeated (x:xs)
    | elem x xs = True
    | otherwise = hasRepeated xs
