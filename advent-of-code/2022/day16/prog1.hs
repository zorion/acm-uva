import qualified Data.Map as Map

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.readGraph

type Status = Map.Map Valve Bool
type Valve = String
type Valves = Map.Map Valve (Pressure, [Valve])
type Pressure = Int


----------------------------------------------
-- Read Input
----------------------------------------------
readGraph :: String -> Valves
readGraph input = foldl Map.union Map.empty $ map readValve (lines input)

-- Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
readValve :: String -> Valves
readValve inLine = Map.singleton valve (pressure, neighbours)
    where ws = words inLine
          valve = ws !! 1
          rate = ws !! 4
          pressure = read $ toSemiColon (drop 5 rate)
          toSemiColon numSC = take (length numSC - 1) numSC
          neighbours = map removeTrailingComma (drop 9 ws)
          removeTrailingComma vC = if vC !! lastChar == ',' then take lastChar vC else vC
            where lastChar = length vC - 1

