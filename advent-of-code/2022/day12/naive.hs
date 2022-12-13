import qualified Data.Map as DM
import qualified Data.Char as DC

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.simulate.getBoard

type Board = [String]
type Pos = (Int, Int)
type Results = DM.Map Pos Steps
type Steps = Int

bigNum :: Steps
bigNum = 999999999999

evaluate :: (Results, Pos) -> Steps
evaluate (result, goal) = DM.findWithDefault bigNum goal result

findFirstPos :: Board -> Char -> Pos
findFirstPos board char = head (filter (\p -> getPos board p == char) all_positions)
    where all_positions = multiply [0..lenCols-1] [0..lenRows-1]
          lenCols = length(head board)
          lenRows = length board

multiply :: Foldable t => [a] -> t b -> [(a, b)]
multiply [x] ys = foldl (\acc y -> (x, y):acc) [] ys
multiply (x:xs) ys = multiply [x] ys ++ multiply xs ys

simulate :: Board -> (Results, Pos)
simulate board = (simulateAux board initialResult start end, end)
    where start = findFirstPos board 'S'
          end = findFirstPos board 'E'
          initialResult = DM.singleton start 0

simulateAux :: Board -> Results -> Pos -> Pos -> Results
simulateAux board result start end
    | start == end = result
    | neighbours == [] = result
    | otherwise = getMinRes visits
        where neighbours = getNeighbours board start
              steps = (DM.!) result start 
              visits = map (simulateAux2 board end steps result) neighbours
              getMinRes [x] = x
              getMinRes (x:xs) = if valX < valXS then x else minXS
                where valX = evaluate (x, end)
                      minXS = getMinRes xs
                      valXS = evaluate (minXS, end)

simulateAux2 :: Board -> Pos -> Steps -> Results -> Pos -> Results
simulateAux2 board end steps results start
    | startVisited = results
    | otherwise = simulateAux board newResult start end
        where startVisited = DM.member start results
              newResult = DM.insert start (steps+1) results

getBoard :: String -> Board
getBoard = lines

getPos :: Board -> Pos -> Char
getPos board (x, y) = (board !! y) !! x

getValue :: Board -> Pos -> Int
getValue board pos 
    | val == 'E' = DC.ord 'z'
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
