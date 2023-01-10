import qualified Data.Map as Map
import qualified Data.Set as Set

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.(getMaxPath maxSteps initNode).getAlongShortestPaths.readGraph
    where maxSteps = 30
          initNode = "AA"

type Enabled = Set.Set Valve
type Valve = String
type Valves = Map.Map Valve (Pressure, [Valve])
type Pressure = Int
type Steps = Int
type ShortestPaths = Map.Map Valve (Map.Map Valve Steps)

getAlongShortestPaths :: Valves -> (ShortestPaths, Valves)
getAlongShortestPaths valves = (getVisitGraph valves, valves)

getMaxPath :: Steps -> Valve -> (ShortestPaths, Valves) -> Pressure
getMaxPath steps valve (paths, valves) = thisPressure * newSteps + recSteps
    where recSteps = getMaxSubPath paths valves (Set.singleton valve) valve newSteps
          thisPressure = fst (valves Map.! valve)
          newSteps = if thisPressure > 0 
            then steps - 1  -- open the valve
            else steps

getMaxSubPath :: ShortestPaths -> Valves -> Enabled -> Valve -> Steps-> Pressure
getMaxSubPath paths valves enabled valve steps = maxResult partialResults
    where candidateMaps = paths Map.! valve
          potentialCandidates = Map.keys candidateMaps
          candidates = filter isUsable potentialCandidates    -- only the usables
          isUsable x = and [not.isEnabled $ x, hasPressure x]
          isEnabled x = Set.member x enabled                  -- (not yet) opened
          hasPressure x = 0 < fst(valves Map.! x)             -- has pressure
          partialResults = map getRecMaxSubPath candidates
          getRecMaxSubPath x = thisPressureX * newStepsX + recStepsX
            where thisPressureX = fst $ valves Map.! x
                  newStepsX = steps - candidateMaps Map.! x - 1  -- move to valve + open it
                  recStepsAux = getMaxSubPath paths valves newEnabled x newStepsX
                  recStepsX = if newStepsX > 0 then recStepsAux else 0
                  newEnabled = Set.insert x enabled


maxResult :: [Pressure] -> Pressure
maxResult = foldl max 0


----------------------------------------------
-- Get all shortest paths using Floyd-Warshall
----------------------------------------------

--Floyd Warshall
getVisitGraph :: Valves -> ShortestPaths
getVisitGraph valves = foldl (getVisitGraphFrom valves) initMap vKeys
    where vKeys = Map.keys valves
          initMap = foldl constrInit Map.empty vKeys
          constrInit result pt = Map.insert pt (initSubMap pt) result
          initSubMap pt = foldl insert (Map.singleton pt 0) (snd (valves Map.! pt))
          insert subMap ptTo = Map.insert ptTo 1 subMap

--Folyd Warshall i iter
getVisitGraphFrom :: Valves -> ShortestPaths -> Valve -> ShortestPaths
getVisitGraphFrom valves result valve = foldl (getVisitGraphFromTo valves valve) result vKeys
    where vKeys = Map.keys valves

--Folyd Warshall i-j iter
getVisitGraphFromTo :: Valves -> Valve -> ShortestPaths -> Valve -> ShortestPaths
getVisitGraphFromTo valves fromValve result toValve = foldl gvgftv result vKeys
    where vKeys = Map.keys valves
          gvgftv = getVisitGraphFromToVia valves fromValve toValve

--Folyd Warshall i-j-k iter
getVisitGraphFromToVia :: Valves -> Valve -> Valve -> ShortestPaths -> Valve -> ShortestPaths
getVisitGraphFromToVia valves fromValve toValve result viaValve
    | and[not fromTo, fromVia, viaTo] = update2DMap result fromValve toValve (fromViaValue + viaToValue)
    | and[    fromTo, fromVia, viaTo] = update2DMap result fromValve toValve newValue
    | otherwise                       = result  -- inaccessible "via" so we leave it like it is.
        where fromTo = Map.member toValve fromValveDict    -- is there a To  in fromDict?
              fromVia = Map.member viaValve fromValveDict  -- is there a Via in fromDict?
              viaTo = Map.member toValve viaValveDict      -- is there a To  in viaDict ?
              fromToValue = fromValveDict Map.! toValve
              fromViaValue = fromValveDict Map.! viaValve
              viaToValue = viaValveDict Map.! toValve
              newValue = min fromToValue (fromViaValue + viaToValue)
              fromValveDict = result Map.! fromValve
              viaValveDict = result Map.! viaValve

update2DMap :: ShortestPaths -> Valve -> Valve -> Steps -> ShortestPaths
update2DMap result key1 key2 value = Map.insert key1 updatedRes result
    where updatedRes = Map.insert key2 value (result Map.! key1)


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
