
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.sum.simulateGame.getInput

prob1debug :: String -> String
prob1debug = show.simulateGame.getInput

getInput :: String -> [(String, String)]
getInput x = map (getPair.words) rounds where
    rounds = lines x
    getPair [y, z] = (y, z)

simulateGame :: [(String, String)] -> [Int]
simulateGame x = map simulateTurn x

simulateTurn :: (String, String) -> Int
simulateTurn (a, b) = (getPoints b) + (getTurnPoints a b)

getPoints :: String -> Int
getPoints "X" = 1
getPoints "Y" = 2
getPoints "Z" = 3

getTurnPoints :: String -> String -> Int
getTurnPoints x y = case (y, x) of
    ("X", "C") -> 6
    ("Y", "A") -> 6
    ("Z", "B") -> 6
    ("X", "A") -> 3
    ("Y", "B") -> 3
    ("Z", "C") -> 3
    _ -> 0
