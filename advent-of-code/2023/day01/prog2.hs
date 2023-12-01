
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
getTokens (x:xs) = if (x <= '9') && (x >= '0')
    then read [x] : getTokens xs
    else getTokens xs
