main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.(map head).applyMoves.getInput

type Stack = [Char] -- piece labels, the head will be the top of stack
type Movement = (Int, Int, Int) -- num pieces, from stack, to stack

applyMoves :: ([Stack], [Movement]) -> [Stack]
applyMoves (stacks, []) = stacks
applyMoves (stacks, (x:xs)) = applyMoves ((applyOneMove stacks x), xs)

applyOneMove :: [Stack] -> Movement -> [Stack]
applyOneMove stacks (0, from, to) = stacks
applyOneMove stacks (n, from, to) = applyOneMove (movePiece stacks from to) ((n-1), from, to)

movePiece :: [Stack] -> Int -> Int -> [Stack]
movePiece [] _ _ = []
movePiece stacks from to = movePieceTo stacksfrom piece to
    where (stacksfrom, piece) = movePieceFrom stacks from

movePieceFrom :: [Stack] -> Int -> ([Stack], Char)
movePieceFrom (s:ss) 0 = ((xs:ss), x)
    where (x:xs) = s
movePieceFrom (s:ss) n = (s:ms, p)
    where (ms, p) = movePieceFrom ss (n-1)

movePieceTo :: [Stack] -> Char -> Int -> [Stack]
movePieceTo (s:ss) p 0 = ((p:s):ss)
movePieceTo (s:ss) p n = s:(movePieceTo ss p (n-1))

getInput :: String -> ([Stack], [Movement])
getInput s = (stacks, movements)  -- we won't read the line with the stack "names"
    where ls = lines s
          stackLines = filter (elem '[') ls
          movementLines = filter condMov ls
          movements = map parseMov movementLines
          stacks = (map dropSpaces).transposeStacks.(map readRow) $ stackLines
          condMov line = if length line > 0 then head line == 'm' else False

readRow :: [Char] -> Stack
readRow "" = []
readRow "   " = " "
readRow (' ':' ':' ':xs) = ' ':(readRow ys)
    where (_:ys) = xs
readRow xs = x:(readRow ys)
    where '[':x:']':zs = xs
          ys
            | length zs == 0 = ""  -- end of line
            | otherwise = tail zs  -- We need to remove the space

transposeStacks :: [Stack] -> [Stack]
transposeStacks ([]:_) = []
transposeStacks x = (map head x) : transposeStacks (map tail x)

dropSpaces :: Stack -> Stack
dropSpaces [] = []
dropSpaces (' ':xs) = dropSpaces xs
dropSpaces (x:xs) = x:(dropSpaces xs)

parseMov :: String -> Movement
parseMov s = subParseMov.words $ s

subParseMov :: [String] -> Movement
subParseMov ws = (read a, readFoo b, readFoo c)
    where [_, a, _, b, _, c] = ws
          readFoo x = (read x) - 1 -- 0-based arays
