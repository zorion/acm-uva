import qualified Data.Map as Map
import qualified Data.Set as Set

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.(visit 22).readGraph

type Status = Set.Set Valve
type Valve = String
type Valves = Map.Map Valve (Pressure, [Valve])
type Pressure = Int

visit :: Int -> Valves -> Pressure
visit n valves = visitNode n 0 valves Set.empty "AA"

visitNode :: Int -> Pressure -> Valves -> Status -> Valve -> Pressure
visitNode (-1) result _ _ _ = result
visitNode 0 result _ _ _ = result
visitNode remTime accPress valves status valve = maxResult $ map (visitNode newRemTime newAcc valves newStatus) neighbours
    where neighboursValve = snd valveInfo
          valveInfo = valves Map.! valve
          alreadySwitched = Set.member valve status
          newStatus = Set.insert valve status 
          newRemTime = remTime - waitHere
          waitHere = if and [not alreadySwitched, fst valveInfo > 0] then 2 else 1
          newAcc = if alreadySwitched then accPress else accPress + (fst valveInfo) * (remTime - 1)
          neighbours = if newStatus == Set.fromList (Map.keys valves) then ["AA"] else neighboursValve

maxResult :: [Pressure] -> Pressure
maxResult = foldl max 0

----------------------------------------------
-- Read Input
----------------------------------------------
readGraph :: String -> Valves
readGraph input = foldl Map.union Map.empty $ map readValve (lines input)

--   0    1  2    3     4       5      6   7    8  |->drop 9
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

