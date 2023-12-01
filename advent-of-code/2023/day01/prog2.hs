
main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.solve1.readIn

-- SUM
solve1 :: [Int] -> (Int, [Int])
solve1 x = (sum x, x)

-- READ
readIn :: String -> [Int]
readIn x = map readNum (lines x)

readNum :: String -> Int
readNum x = (10 * head tokens) + tokens!!(-1 + length tokens) where
    tokens = getTokens x

getTokens :: String -> [Int]
getTokens [] = []
getTokens xs = case getFirstToken xs of
    Just num -> num : getTokens(tail xs)
    Nothing -> getTokens(tail xs)

getFirstToken :: String -> Maybe Int
getFirstToken x
    | take 1 x == "0" = Just 0
    | take 1 x == "1" = Just 1
    | take 1 x == "2" = Just 2
    | take 1 x == "3" = Just 3
    | take 1 x == "4" = Just 4
    | take 1 x == "5" = Just 5
    | take 1 x == "6" = Just 6
    | take 1 x == "7" = Just 7
    | take 1 x == "8" = Just 8
    | take 1 x == "9" = Just 9
    | otherwise = Nothing
    
