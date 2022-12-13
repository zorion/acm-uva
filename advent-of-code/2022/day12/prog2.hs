import qualified Data.Map as DM
import qualified Data.Char as DC
import qualified Data.Set as DS

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.evaluate.simulate.getBoard

type Board = [String]
type Pos = (Int, Int)
type Results = DM.Map Pos Steps
type Steps = Int

bigNum :: Steps
bigNum = 999999999999

debug :: (Results, Pos) -> (Int, Steps, Pos)
debug (r,p) = (length(DM.elems r),evaluate (r,p),p)
evaluate :: (Results, Pos) -> Steps
evaluate (result, goal) = DM.findWithDefault bigNum goal result

findAllPos :: Board -> Char -> [Pos]
findAllPos board char = filter (\p -> getPos board p == char) all_positions
    where all_positions = multiply [0..lenCols-1] [0..lenRows-1]
          lenCols = length(head board)
          lenRows = length board


multiply :: Foldable t => [a] -> t b -> [(a, b)]
multiply [x] ys = foldl (\acc y -> (x, y):acc) [] ys
multiply (x:xs) ys = multiply [x] ys ++ multiply xs ys

simulate :: Board -> (Results, Pos)
simulate board = foldl getMinPath (DM.empty, end) simulations
    where end = head $ findAllPos board 'E'
          allStarts = findAllPos board 'a'
          simulations = map (\start -> simulateStart board start end) allStarts
          getMinPath simulation best = if evaluate simulation < evaluate best then simulation else best

simulateStart :: Board -> Pos -> Pos -> (Results, Pos)
simulateStart board start end = (simulateAux board initialResult [start] end 0 bigNum, end)
    where initialResult = DM.singleton start 0

simulateAux :: Board -> Results -> [Pos] -> Pos -> Steps -> Int -> Results
simulateAux board result starts end steps limit
    | elem end starts = result
    | filteredNeighbours == [] = result
    | limit == 0 = result
    | otherwise = simulateAux board newResult filteredNeighbours end (steps+1) (limit-1)
        where neighboursLists = map (getNeighbours board) starts
              neighboursSet = DS.fromList (foldl (++) [] neighboursLists)
              filteredNeighbours = filter isNotVisited neighboursL
              neighboursL = DS.foldr (:) [] neighboursSet
              isNotVisited pos = not (DM.member pos result)
              newResult' = foldl (insertPos (steps+1)) result filteredNeighbours
              insertPos steps' result' pos' = DM.insert pos' steps' result'
              newResult = DM.insert (bigNum, steps) (length filteredNeighbours) newResult' 


getBoard :: String -> Board
getBoard = lines.replaceStart

replaceStart :: String -> String
replaceStart [] = []
replaceStart (x:xs) = x': replaceStart xs
    where x' = if x == 'S' then 'a' else x



getPos :: Board -> Pos -> Char
getPos board (x, y) = (board !! y) !! x

getValue :: Board -> Pos -> Int
getValue board pos 
    | val == 'E' = DC.ord 'z'
    | val == 'S' = DC.ord 'a'
    | otherwise = DC.ord val
        where val = getPos board pos

getNeighbours :: Board -> Pos -> [Pos]
getNeighbours board (x, y) = filter isValid positions
    where lenRows = length board
          lenCols = length (head board)
          isValid pos = if isInBounds pos then isAccessible pos else False
          isInBounds (x', y') = and[x' >= 0, x' < lenCols, y' >= 0, y' < lenRows]
          isAccessible pos = or[curPos == 'S', getValue board pos <= curVal +1 ]
          curPos = getPos board (x, y)
          curVal = getValue board (x, y)
          positions = generateNeighbourPositions (x, y)

generateNeighbourPositions :: Pos -> [Pos]
generateNeighbourPositions (x, y) = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
