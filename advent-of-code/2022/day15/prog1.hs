
test :: Bool -- sample needs line 10 and my input line 2 000 000
test = False

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.sizeSegments.removeBeacons.getSegments.readMap

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

getManhattan :: Sensor -> Beacon -> Mint
getManhattan (a, b) (x, y) = (abs (a-x)) + (abs (b-y))

getSegment :: Sensor -> Mint -> Segment
getSegment (a, b) size = (a - pendingSize, a + pendingSize)
    where pendingSize = if size - done > 0 then size - done else 0
          done = abs (b - lineCheck)

getSegments :: [(Sensor, Beacon)] -> (Segments, [Beacon])
getSegments inpairs = (segments, beacons)
    where foo a b = addSegment a (newSegment b)
          newSegment (sensor, beacon) = getSegment sensor (getManhattan sensor beacon)
          segments = foldl foo [] inpairs
          beacons = map snd inpairs

removeBeacons :: (Segments, [Beacon]) -> Segments
removeBeacons (segments, beacons) = foldl removePoint segments beacons

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

removePoint :: Segments -> Beacon -> Segments
removePoint segs (x, y) = if y==lineCheck then foldl (splitIfRequired x) [] segs else segs
    where splitIfRequired pt segments (low, high)
            | pt < low = addSegment segments (low, high)
            | pt > high = addSegment segments (low, high)
            | and[pt==low, pt==high] = segments
            | pt == low = addSegment segments (low+1, high)
            | pt == high = addSegment segments (low, high-1)
            | otherwise = addSegment (addSegment segments (low, pt-1)) (pt+1, high)

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

