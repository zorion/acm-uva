import qualified Data.Map as M

main :: IO ()
main = do
    interact prob1
    putStrLn ""

type Status = (Pos, Pos, Visited)
type Pos = (Int, Int)
type Visited = M.Map Pos Pos
type Move = (Int, Pos)

prob1 :: String -> String
prob1 = show.countPositions.applyMovements.(map parseMovement).lines

countPositions :: Status -> Int
countPositions (_, _, visited) = length (M.elems visited)

parseMovement :: String -> Move
parseMovement (d:' ':xs)
    | d == 'U' = (n, (0, -1))
    | d == 'D' = (n, (0, 1))
    | d == 'L' = (n, (-1, 0))
    | d == 'R' = (n, (1, 0))
        where n = read xs

applyMovements :: [Move] -> Status
applyMovements = foldl applyMove initialStatus

initialStatus :: Status
initialStatus = ((0,0), (0,0), M.singleton (0, 0) (0, 0))

applyMove :: Status -> Move -> Status
applyMove status (0, v) = status
applyMove status (n, v) = applyMove (applyStep status v) (n-1, v)

applyStep :: Status -> Pos -> Status
applyStep (posH, posT, visited) v = (newPosH, newPosT, M.insert newPosT newPosT visited)
    where newPosH = sumPos posH v
          newPosT = moveTail newPosH posT

sumPos :: Pos -> Pos -> Pos
sumPos (x, y) (vx, vy) = (x+vx, y+vy)

moveTail :: Pos -> Pos -> Pos
moveTail (x, y) (a, b) = sumPos (a, b) (v1, v2)
    where v1 = if or [abs (x-a) > 1, doMove] then div (x-a) (abs (x-a)) else 0
          v2 = if or [abs (y-b) > 1, doMove] then div (y-b) (abs (y-b)) else 0
          doMove = and [x /= a, y /= b, abs(x-a) + abs(y-b) > 2]
