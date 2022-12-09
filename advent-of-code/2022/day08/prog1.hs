
main :: IO ()
main = do
    interact prob1
    putStrLn ""

type Forest = [String]
type Position = (Int, Int)
type Move = (Int, Int)

prob1 :: String -> String
prob1 = show.sum.getVisibleTrees.lines

getVisibleTrees :: Forest -> [Int]
getVisibleTrees forest = map (isVisible forest) (getAllPositions forest)

getAllPositions :: Forest -> [Position]
getAllPositions forest = multiply [0..lenFor] [0..lenLine]
    where lenFor = (length forest) - 1
          lenLine = (length.head $ forest) - 1

multiply :: [Int] -> [Int] -> [Position]
multiply  [x] ys = map (\y -> (x, y)) ys
multiply (x:xs) ys = (multiply [x] ys) ++ (multiply xs ys)

isVisible :: Forest -> Position -> Int
isVisible forest pos = if visible then 1 else 0
    where visible = or [vLeft, vRight, vUp, vDown]
          vLeft = checkBigger tree pos (-1, 0) forest
          vRight = checkBigger tree pos (1, 0) forest
          vUp = checkBigger tree pos (0, -1) forest
          vDown = checkBigger tree pos (0, 1) forest
          tree = position forest pos

position :: Forest -> Position -> Int
position forest (x, y) = read (((forest !! x) !! y):[])

checkBigger :: Int -> Position -> Move -> Forest -> Bool
checkBigger size (x, y) (vx, vy) forest
    | outOfBound (newx, newy) forest = True
    | size > position forest (newx, newy) = checkBigger size (newx, newy) (vx, vy) forest
    | otherwise = False
        where newx = x + vx
              newy = y + vy
              outOfBound (x, y) forest
                | x < 0 = True
                | y < 0 = True
                | x > (length forest) - 1 = True
                | y > (length.head $ forest) - 1 = True
                | otherwise = False
