
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
simulateTurn (a, b) = (getPointsAux a b) + (getTurnPoints b)

getPointsAux :: String -> String -> Int
getPointsAux a "Y" = getPoints a
getPointsAux a "X" = getPoints.toLose $ a
getPointsAux a "Z" = getPoints.toWin $ a

getPoints :: String -> Int
getPoints "A" = 1
getPoints "B" = 2
getPoints "C" = 3

getTurnPoints :: String -> Int
getTurnPoints x = case x of 
    "X" -> 0
    "Y" -> 3
    "Z" -> 6

toWin :: String -> String
toWin x = case x of
    "A" -> "B"
    "B" -> "C"
    "C" -> "A"

toLose :: String -> String
toLose x
    | x == "A" = "C"
    | x == "B" = "A"
    | x == "C" = "B"
