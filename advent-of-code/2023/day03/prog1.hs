import Data.Map qualified as Map

main :: IO ()
main = do
  interact prob
  putStrLn ""

prob :: String -> String
prob = show . solve . readIn

-- TYPES

type Engine = Map.Map Position Value

type Position = (Int, Int)

type Value = Char

emptyEngine :: Engine
emptyEngine = Map.empty

addToEngine :: Engine -> Position -> Value -> Engine
addToEngine eng pos val = Map.insert pos val eng

joinEngines :: Engine -> Engine -> Engine
joinEngines = Map.union

doesExist :: Position -> Engine -> Bool
doesExist = Map.member

charAtEngine :: Engine -> Position -> Value
charAtEngine = (Map.!)

-- LOGIC
solve :: Engine -> Int
solve = sum . getNumbers 0

getNumbers :: Int -> Engine -> [Int]
getNumbers n eng =
  if doesExist (0, n) eng
    then getLineNumbers n eng ++ getNumbers (n + 1) eng
    else []

getLineNumbers :: Int -> Engine -> [Int]
getLineNumbers = getFromEmpty 0

getFromEmpty :: Int -> Int -> Engine -> [Int]
getFromEmpty x y eng =
  if doesExist (x, y) eng
    then case charAtEngine eng (x, y) of
      '0' -> getFromNum (x + 1) y 0 b eng
      '1' -> getFromNum (x + 1) y 1 b eng
      '2' -> getFromNum (x + 1) y 2 b eng
      '3' -> getFromNum (x + 1) y 3 b eng
      '4' -> getFromNum (x + 1) y 4 b eng
      '5' -> getFromNum (x + 1) y 5 b eng
      '6' -> getFromNum (x + 1) y 6 b eng
      '7' -> getFromNum (x + 1) y 7 b eng
      '8' -> getFromNum (x + 1) y 8 b eng
      '9' -> getFromNum (x + 1) y 9 b eng
      _ -> getFromEmpty (x + 1) y eng
    else []
  where
    b = shouldKeep x y eng

getFromNum :: Int -> Int -> Int -> Bool -> Engine -> [Int]
getFromNum x y acc bKeep eng =
  if doesExist (x, y) eng
    then case charAtEngine eng (x, y) of
      '0' -> getFromNum (x + 1) y (10 * acc + 0) b eng
      '1' -> getFromNum (x + 1) y (10 * acc + 1) b eng
      '2' -> getFromNum (x + 1) y (10 * acc + 2) b eng
      '3' -> getFromNum (x + 1) y (10 * acc + 3) b eng
      '4' -> getFromNum (x + 1) y (10 * acc + 4) b eng
      '5' -> getFromNum (x + 1) y (10 * acc + 5) b eng
      '6' -> getFromNum (x + 1) y (10 * acc + 6) b eng
      '7' -> getFromNum (x + 1) y (10 * acc + 7) b eng
      '8' -> getFromNum (x + 1) y (10 * acc + 8) b eng
      '9' -> getFromNum (x + 1) y (10 * acc + 9) b eng
      _ -> [acc | bKeep] ++ getFromEmpty (x + 1) y eng
    else [acc | bKeep]
  where
    b = bKeep || shouldKeep x y eng

shouldKeep :: Int -> Int -> Engine -> Bool
shouldKeep x y eng =
  or
    [ isNice (charAtEngine eng (a, b))
      | a <- [x - 1, x, x + 1],
        b <- [y - 1, y, y + 1],
        doesExist (a, b) eng
    ]

isNice :: Char -> Bool
isNice c
  | c == '.' = False
  | c <= '9' && c >= '0' = False
  | otherwise = True

-- READ
readIn :: String -> Engine
readIn x = readLines 0 (lines x)

readLines :: Int -> [String] -> Engine
readLines n [] = emptyEngine
readLines n (x : xs) = joinEngines (readLine n 0 x) (readLines (n + 1) xs)

readLine :: Int -> Int -> String -> Engine
readLine y x [] = emptyEngine
readLine y x (z : zs) = addToEngine eng (x, y) z
  where
    eng = readLine y (x + 1) zs

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
