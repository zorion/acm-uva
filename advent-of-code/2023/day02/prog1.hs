main :: IO ()
main = do
  interact prob
  putStrLn ""

prob :: String -> String
prob = show . solve . readIn

-- TYPES

type Game = (GameId, [CubeSet])

type GameId = Int

type CubeSet = (CubeRed, CubeGreen, CubeBlue)

type CubeRed = Cubes

type CubeGreen = Cubes

type CubeBlue = Cubes

type Cubes = Int

-- LOGIC

solve :: [Game] -> (Int, [Game])
solve x = (sumValid x, x)

sumValid :: [Game] -> Int
sumValid [] = 0
sumValid (x : xs) = sumValid xs + (if isValid(snd x) then fst x else 0)

isValid :: [CubeSet] -> Bool
isValid = foldr((&&).isValid') True

isValid' :: CubeSet -> Bool
isValid' cubes = (reds <= 12) && (blues <= 13) && (greens <= 14)
  where
    (reds, greens, blues) = cubes


-- READ
readIn :: String -> [Game]
readIn x = map readGame (lines x)

-- "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
readGame :: String -> Game
readGame x = (readCubeGame (head semicolonSplit), readCubeSets (head (tail semicolonSplit)))
  where
    semicolonSplit = splitString ":" x

-- "Game 1"
readCubeGame :: String -> Int
readCubeGame = read . drop 5

-- " 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
readCubeSets :: String -> [CubeSet]
readCubeSets x = map readCubeSet (splitString ";" x)

-- " 3 blue, 4 red"
-- " 2 green"
readCubeSet :: String -> CubeSet
readCubeSet x = (readCubes "red" x, readCubes "green" x, readCubes "blue" x)

-- "blue" -> " 3 blue, 4 red" -> 3
-- "blue" -> " 2 green" -> 0
readCubes :: String -> String -> Cubes
readCubes color x = sum (map (readCubeColor color) (splitString "," x))

-- "blue" -> " 3 blue" -> 3
-- "blue" -> " 2 green" -> 0
readCubeColor :: String -> String -> Cubes
readCubeColor color x = if color == splitX !! 2 then read (splitX !! 1) else 0
  where
    splitX = splitString " " x

-- SUPA HELPERS!

splitString :: String -> String -> [String]
splitString _ [] = []
splitString substring str = firstPart : splitString substring lastPart
  where
    (firstPart, lastPart) = splitString1 "" substring str

splitString1 :: String -> String -> String -> (String, String)
splitString1 prefix _ [] = (prefix, [])
splitString1 prefix substring str =
  if take (length substring) str == substring
    then (prefix, drop (length substring) str)
    else splitString1 (prefix ++ [head str]) substring (tail str)
