main :: IO ()
main = do
  interact prob1
  putStrLn ""

prob1 :: String -> String
prob1 = show . solve1 . readIn

-- SUM
solve1 :: [Int] -> (Int, [Int])
solve1 x = (sum x, x)

-- READ
readIn :: String -> [Int]
readIn x = map readNum (lines x)

readNum :: String -> Int
readNum x = (10 * readFirst x) + readLast x

readFirst :: String -> Int
readFirst (x : xs) =
  if and [x >= '0', x <= '9']
    then read [x]
    else readFirst xs

readLast :: String -> Int
readLast x = case readLastMaybe x of
  Just num -> num
  Nothing -> -1

readLastMaybe :: String -> Maybe Int
readLastMaybe [] = Nothing
readLastMaybe [x] =
  if and [x >= '0', x <= '9']
    then Just (read [x])
    else Nothing
readLastMaybe (x : xs) = case readLastMaybe xs of
  Just num -> Just num
  Nothing -> readLastMaybe [x]
