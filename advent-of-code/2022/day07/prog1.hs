import qualified Data.Map as M

main = do
    interact prob1
    putStrLn ""


prob1 :: String -> String
prob1 = show.sum.(filter (<100000)).walkTree.applyAllInstr.groupInstructions
prob1' :: String -> String
prob1' = show.applyAllInstr.groupInstructions'.lines

type FS = M.Map String Node
data Node = Tree FS | Node Int deriving (Show)
type Path = [String]
type Status = (Path, FS)

walkTree :: Status -> [Int]
walkTree (_, fs) = tot:subList
    where (tot, subList) = foldl walkRecList (0, []) (M.elems fs)

walkRecList :: (Int, [Int]) -> Node -> (Int, [Int])
walkRecList (tot, acc) (Tree fs) = (tot2+tot, tot2:subList++acc)
    where (tot2, subList) = foldl walkRecList (0, []) (M.elems fs)
walkRecList (tot, acc) (Node fsize) = (fsize+tot, acc)


insertFile :: Path -> Int -> FS -> FS
insertFile [fname] fsize tree = M.insert fname (Node fsize) tree
insertFile (x:xs) fsize tree 
    | M.member x tree = M.insert x (Tree (insertFile xs fsize subtree)) tree
    | otherwise = M.insert x (Tree (insertFile xs fsize M.empty)) tree
        where Tree subtree = tree M.! x

getSizeLimited :: FS -> Int-> Maybe Int
getSizeLimited tree limit = foldl (getSizeLimitedList limit) (Just 0) (M.elems tree)

getSizeLimitedList :: Int -> Maybe Int -> Node -> Maybe Int
getSizeLimitedList _ Nothing _ = Nothing
getSizeLimitedList n (Just acc) (Tree fs) = let treeSize = getSizeLimited fs (n - acc) in case treeSize of
    Nothing -> Nothing
    Just x -> Just (acc+x)
getSizeLimitedList n (Just acc) (Node fsize)
    | total >= n = Nothing
    | otherwise = Just total
        where total = acc + fsize

applyAllInstr :: [[String]] -> Status
applyAllInstr instructions = foldl applyInstr ([], M.empty) instructions

applyInstr :: Status -> [String] -> Status
applyInstr (cw, t) (instruction:result)
    | instruction == "$ ls" = (cw, foldl (maybeAddFile cw) t result)
    | otherwise  = (changeDir cw ((words instruction)!!2), t)

maybeAddFile ::  Path -> FS -> String -> FS
maybeAddFile cw t maybeFile
    | head ws == "dir" = t
    | otherwise = insertFile (cw ++ [fname]) fsize t
        where ws = words maybeFile
              fsize = read.head $ ws
              fname = head.tail $ ws

changeDir :: Path -> String -> Path
changeDir cw x = case x of
    "/" -> []
    ".." -> reverse.tail.reverse $ cw
    otherwise -> cw ++ [x]

------------------------------------------
-- Input treatment: 2 options

-- Split each instruction and results by lines
groupInstructions :: String -> [[String]]
groupInstructions = (map lines).breakInstructions

-- Group the instructions with its results
breakInstructions :: String -> [String]
breakInstructions [] = []
breakInstructions ('$':xs) = ('$':firstInstr):otherInstr
    where (firstInstr, others) = break (=='$') xs
          otherInstr = breakInstructions others

-- Group the instructions with its results from lines
groupInstructions' :: [String] -> [[String]]
groupInstructions' = reverse.giaux []

-- Add instructions on top of, so it must be reversed
giaux :: [[String]] -> [String] -> [[String]]
giaux result [] = result
giaux result (x:xs)
        | head x == '$' = giaux ([x]:result) xs
        | otherwise = giaux ((y++[x]):ys) xs
            where (y:ys) = result
