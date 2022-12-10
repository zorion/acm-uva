import qualified Data.Map as M

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.sum.evaluate.(simulate 1).lines

simulate :: Int -> [String] -> [Int]
simulate n [] = []
simulate n (x:xs) = subResult ++ (simulate m xs)
    where (m, subResult) = simulateOp n x

simulateOp ::  Int -> String -> (Int, [Int])
simulateOp n "noop" = (n, [n])
simulateOp n ('a':'d':'d':'x':' ':val) = (m, [n, n])
    where m = (read val) + n

evaluate :: [Int] -> [Int]
evaluate xs = (map (evalVal xs) [20, 60, 100, 140, 180, 220])

evalVal :: [Int] -> Int -> Int
evalVal xs n = (xs !! (n-1)) * n  -- Index-0 vs index-1