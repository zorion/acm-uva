import qualified Data.Set as Set

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.getRocks.lines

type Rocks = Set.Set Pos
type Pos = (Int, Int)

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
