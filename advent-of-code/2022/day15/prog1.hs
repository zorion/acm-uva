
test :: Bool -- sample needs line 10 and my input line 2 000 000
test = True

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.readMap

type Result = Segments
type SenBea = (Sensor, Beacon)
type Sensor = Pos
type Beacon = Pos
type Pos = (Mint, Mint)
type Mint = Int  -- MyInt
type Segments = [Segment]
type Segment = (Mint, Mint)

lineCheck :: Mint
lineCheck = if test then 10 else 2*1000*1000


----------------------------------------------
-- Segment
----------------------------------------------
sizeSegments :: Segments -> Mint
sizeSegments [] = 0
sizeSegments (x:xs) = (sizeSeg x) + sizeSegments xs 

sizeSeg :: Segment -> Mint
sizeSeg (a, b) =  b - a + 1

addSegment :: Segments -> Segment -> Segments
addSegment group new = (minIntersect, maxIntersect):disjointSegments
    where
        intersectSegments = filter (intersectSeg new) group
        disjointSegments = filter (not.intersectSeg new) group
        minIntersect = foldl min (fst new) (map fst intersectSegments)
        maxIntersect = foldl max (snd new) (map snd intersectSegments)

intersectSeg :: Segment -> Segment -> Bool
intersectSeg (a, b) (x, y) = and [a<=y, x<=b]



----------------------------------------------
-- Read Input
----------------------------------------------
readMap :: String -> [SenBea]
readMap = (map readSensor).lines

-- Sensor at x=2, y=18: closest beacon is at x=-2, y=15
readSensor :: String -> (Sensor, Beacon)
readSensor inLine = ((atoi a, atoi b), (atoi x, atoi y))
    where abxy = drop (length "Sensor at x=") inLine
          (a, commabxy) = break (==',') abxy
          bxy = drop (length ", y=") commabxy
          (b, colonxy) = break (==':') bxy
          xy = drop (length ": closest beacon is at x=") colonxy
          (x, commay) = break (==',') xy
          y = drop (length ", y=") commay
          atoi s = read s :: Mint  -- String to Mint

