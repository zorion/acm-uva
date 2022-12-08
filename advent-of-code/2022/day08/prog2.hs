import qualified Data.Map as M

main = do
    interact prob1
    putStrLn ""

type Forest = [String]
type Position = (Int, Int)
type Move = (Int, Int)

prob1 :: String -> String
prob1 = show.maxArray.getVisibleTrees.lines

maxArray :: [Int] -> Int
maxArray [] = -1
maxArray (x:xs) = max x (maxArray xs)

getVisibleTrees :: Forest -> [Int]
getVisibleTrees forest = map (getScenicScore forest) (getAllPositions forest)

getAllPositions :: Forest -> [Position]
getAllPositions forest = multiply [0..lenFor] [0..lenLine]
    where lenFor = (length forest) - 1
          lenLine = (length.head $ forest) - 1

multiply :: [Int] -> [Int] -> [Position]
multiply  [x] ys = map (\y -> (x, y)) ys
multiply (x:xs) ys = (multiply [x] ys) ++ (multiply xs ys)

getScenicScore :: Forest -> Position -> Int
getScenicScore forest pos = vLeft * vRight * vUp * vDown
    where tree = position forest pos
          vLeft = checkBigger tree 0 pos (-1, 0) forest
          vRight = checkBigger tree 0 pos (1, 0) forest
          vUp = checkBigger tree 0 pos (0, -1) forest
          vDown = checkBigger tree 0 pos (0, 1) forest
          

position :: Forest -> Position -> Int
position forest (x, y) = read (((forest !! x) !! y):[])

checkBigger :: Int -> Int -> Position -> Move -> Forest -> Int
checkBigger size acc (x, y) (vx, vy) forest
    | outOfBound (newx, newy) forest = acc
    | size > position forest (newx, newy) = checkBigger size (acc+1) (newx, newy) (vx, vy) forest
    | otherwise = acc + 1
        where newx = x + vx
              newy = y + vy
              outOfBound (x, y) forest
                | x < 0 = True
                | y < 0 = True
                | x > (length forest) - 1 = True
                | y > (length.head $ forest) - 1 = True
                | otherwise = False
