import qualified Data.Map as Map

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


-- LOGIC
solve :: Engine -> Engine
solve x = x

-- READ
readIn :: String -> Engine
readIn x = readLines 0 (lines x)

readLines :: Int -> [String] -> Engine
readLines n [] = emptyEngine
readLines n (x:xs) = joinEngines (readLine n 0 x) (readLines (n+1) xs)

readLine :: Int -> Int -> String -> Engine
readLine y x [] = emptyEngine
readLine y x (z:zs) = addToEngine eng (x, y) z
  where
    eng = readLine y (x+1) zs


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
