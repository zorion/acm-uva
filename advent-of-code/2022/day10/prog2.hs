
main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = evaluate.(simulate 1).lines

simulate :: Int -> [String] -> [Int]
simulate n [] = []
simulate n (x:xs) = subResult ++ (simulate m xs)
    where (m, subResult) = simulateOp n x

simulateOp ::  Int -> String -> (Int, [Int])
simulateOp n "noop" = (n, [n])
simulateOp n ('a':'d':'d':'x':' ':val) = (m, [n, n])
    where m = (read val) + n

evaluate :: [Int] -> String
evaluate = getCRT 0

getCRT :: Int -> [Int] -> String
getCRT _ [] = []
getCRT n (x:xs) = if (mod n 40) == 39 then pixel:endline:nextCRT else pixel:nextCRT
    where endline = '\n'
          nextCRT = getCRT (n+1) xs
          pixel = if abs ((mod n 40)-x) < 2 then '#' else '.'

