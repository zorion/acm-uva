
test :: Bool -- sample needs 20 x 20 and my input 4 000 000 x 4 000 000
test = False

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.getResult.getMissingPos.readMap

type SenBea = (Sensor, Beacon)
type Sensor = Pos
type Beacon = Pos
type Pos = (Mint, Mint)
type Mint = Int  -- MyInt
type Segments = [Segment]
type Segment = (Mint, Mint)
--type DebugRes = [(Mint, Segments)]
type DebugRes = Pos

maxDim :: Mint
maxDim = if test then 20 else maxDimProd
maxDimProd :: Mint
maxDimProd = 4*1000*1000

getResult :: Pos -> Mint
getResult (x,y) = maxDimProd * x + y

getManhattan :: Sensor -> Beacon -> Mint
getManhattan (a, b) (x, y) = (abs (a-x)) + (abs (b-y))

getSegment :: Mint -> Sensor -> Mint -> Maybe Segment
getSegment lineCheck (a, b) size = case pendingSize of
    Just psize -> Just (a - psize, a + psize)
    Nothing -> Nothing
    where pendingSize = if size - done > 0 then Just (size - done) else Nothing
          done = abs (b - lineCheck)

getSegments :: Mint -> [SenBea] -> Segments
getSegments lineCheck inpairs = (segments)
    where foo a b = case newSegment b of
            Nothing -> a
            Just newSeg -> addSegment a newSeg
          newSegment (sensor, beacon) = getSegment lineCheck sensor (getManhattan sensor beacon)
          segments = foldl foo [] inpairs
          beacons = map snd inpairs

getMissingPos :: [SenBea] -> DebugRes
getMissingPos = getMissingUntilLine maxDim

getMissingUntilLine :: Mint -> [SenBea] -> DebugRes
--getMissingUntilLine n inpairs = if notFound then (n,res):recCall else [(n,res)]
getMissingUntilLine n inpairs = if notFound then recCall else (missingX, n)
    where res = getSegments n inpairs
          notFound = sizeSegments res == maxDim + 1
          recCall = getMissingUntilLine (n-1) inpairs
          missingX = getMissingX res

getMissingX :: Segments -> Mint
getMissingX [] = -1
getMissingX [(mn, mx)] = if mn > 0 then 0 else (if mx < maxDim then maxDim else -2)
getMissingX ((a,b):(c,d):xs) = if b == c-1 then getMissingX ((a,d):xs) else c-1

qs :: Ord a => [a] -> [a]
qs [] = []
qs (x:xs) = qs (filter (<x) xs) ++ [x] ++ qs (filter (>x) xs)


----------------------------------------------
-- Segment
----------------------------------------------
sizeSegments :: Segments -> Mint
sizeSegments [] = 0
sizeSegments (x:xs) = (sizeSeg x) + sizeSegments xs 

sizeSeg :: Segment -> Mint
sizeSeg (a, b) =  b - a + 1

reduceSeg :: Segments -> Segments
reduceSeg [] = []
reduceSeg [s] = [s]
reduceSeg ((a,b):(c,d):xs) = if b == c-1 then reduceSeg ((a,d):xs) else (a,b):reduceSeg ((c,d):xs)

addSegment :: Segments -> Segment -> Segments
addSegment group new = reduceSeg.qs $ ((max minIntersect 0, min maxIntersect maxDim):disjointSegments)
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
readSensor :: String -> SenBea
readSensor inLine = ((atoi a, atoi b), (atoi x, atoi y))
    where abxy = drop (length "Sensor at x=") inLine
          (a, commabxy) = break (==',') abxy
          bxy = drop (length ", y=") commabxy
          (b, colonxy) = break (==':') bxy
          xy = drop (length ": closest beacon is at x=") colonxy
          (x, commay) = break (==',') xy
          y = drop (length ", y=") commay
          atoi s = read s :: Mint  -- String to Mint

