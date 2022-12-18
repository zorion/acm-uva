import qualified Data.Set as Set

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.length.simulate.getMinRock.getRocks.lines

type Rocks = Set.Set Pos
type Pos = (Int, Int)

positionInitial :: Pos
positionInitial = (500,0)

simulate :: (Int, Rocks) -> [Rocks]
simulate (minRock, r) = if r == r' then [] else r:res'
    where
        r' = dropSand minRock r positionInitial
        res' = simulate (minRock, r')

extendRock :: Rocks -> Rocks -> Bool
extendRock a b = Set.null $ Set.difference b a

dropSand :: Int -> Rocks -> Pos -> Rocks
dropSand n r p
    | n < y = r
    | isFree r downPos = dropSand n r downPos
    | isFree r dleftPos = dropSand n r dleftPos
    | isFree r drightPos = dropSand n r drightPos
    | otherwise = addRock r p
        where downPos = movePos p (0,1)
              dleftPos = movePos p (-1,1)
              drightPos = movePos p (1,1)
              (_, y) = p

addRock :: Rocks -> Pos -> Rocks
addRock r p = Set.insert p r

movePos :: Pos -> Pos -> Pos
movePos (a, b) (x, y) = (a+x, b+y)

isFree :: Rocks -> Pos -> Bool
isFree r p = not $ Set.member p r

------------------------
-- Read the input
------------------------

getMinRock :: Rocks -> (Int, Rocks)
getMinRock rs = (maxYNum , rs)  -- Then minimum position is what have the maximum Y
    where maxYNum = Set.foldl getMaxY 0 rs
          getMaxY n (_,y) = if n < y then y else n

getRocks :: [String] -> Rocks
getRocks [] = Set.empty
getRocks (x:xs) = Set.union (getRockLines x) (getRocks xs)

getRockLines :: String -> Rocks
getRockLines x = foldr Set.insert Set.empty (getRockSegments x)

getRockSegments :: String -> [Pos]
getRockSegments x =  foldl (++) [] (map getRockSubSegments starEndPairs)
    where starEndPairs = toPairs $ brokenPos x

toPairs :: [a] -> [(a, a)]
toPairs [] = []
toPairs [x] = [(x, x)] --Segment of only one item
toPairs (x:y:xs) = (x, y):toPairs(y:xs)

brokenPos :: String -> [Pos]
brokenPos [] = []
brokenPos x = (parsePos z):brokenPos (drop 2 ys) -- drop "> "
    where (y, ys) = break (=='>') x -- break here "num -" / "> rest"
          (z, _) = break (==' ') y  -- break here "num"   / " -"

parsePos :: String -> Pos
parsePos p = (read x, read (drop 1 xs))
    where (x,xs) = break (==',') p

getRockSubSegments :: (Pos,Pos) -> [Pos]
getRockSubSegments ((x1, y1), (x2, y2))
    | x1 == x2 = map (\y -> (x1, y)) [miny..maxy]
    | y1 == y2 = map (\x -> (x, y1)) [minx..maxx]
        where minx = min x1 x2
              maxx = max x1 x2
              miny = min y1 y2
              maxy = max y1 y2
