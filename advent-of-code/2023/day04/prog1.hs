import Data.Set qualified as Set

main :: IO ()
main = do
  interact prob
  putStrLn ""

prob :: String -> String
prob = show . solve . readIn

-- TYPES

type ScratchCard = (Number, Players, Winners)
type Players = SetNums
type Winners = SetNums
type SetNums = Set.Set Number
type Number = Int

emptyNumbers :: SetNums
emptyNumbers = Set.empty
intersectNumbers :: SetNums -> SetNums -> SetNums
intersectNumbers = Set.intersection
joinNumbers :: SetNums -> SetNums -> SetNums
joinNumbers = Set.union
fromListNumbers :: [Number] -> SetNums
fromListNumbers = Set.fromList


-- LOGIC
solve :: [ScratchCard] -> (Int, [ScratchCard])
solve x = (foldr sumSolveSC 0 x, x)

sumSolveSC :: ScratchCard -> Int -> Int
sumSolveSC card acc = acc + solveSC card

solveSC :: ScratchCard -> Int
solveSC (_, players, winners) = if totNums > 0 then pow 2 (totNums - 1) else 0
  where
    totNums = length (intersectNumbers players winners)

pow :: (Eq t1, Num t1, Num t2) => t2 -> t1 -> t2
pow _ 0 = 1
pow m n = m * pow m (n - 1)

-- READ
readIn :: String -> [ScratchCard]
readIn x = map readSC (lines x)

-- Card N: 5nums | 8nums
readSC :: String -> ScratchCard
readSC cardBoard = (cardNum, winners, players)
  where
    cardNum = readCardNum cardPart
    winners = readSetNum winnerPart
    players = readSetNum playersPart
    mainParts = splitString ": " cardBoard
    cardPart = head mainParts
    restPart = head.tail $ mainParts
    numParts = splitString " | " restPart
    winnerPart = head numParts
    playersPart = head.tail $ numParts

-- Card N
readCardNum :: [Char] -> Number
readCardNum = read.drop 5

-- " 1 12 23 34  2"
readSetNum :: String -> SetNums
readSetNum x = fromListNumbers (map read (words x))

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
