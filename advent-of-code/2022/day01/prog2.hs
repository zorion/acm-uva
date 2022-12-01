
main = interact prob1

prob1 :: String -> String
prob1 = show.getMax3.groupSum.group

prob1debug :: String -> String
prob1debug = show.quicksort.groupSum.group

getMax :: [Int] -> Int
getMax [x] = x
getMax (x:xs) = if x > nextMax then x else nextMax where nextMax = getMax(xs)

getMax3 :: [Int] -> Int
getMax3 x = sum(take 3 (quicksort x))

quicksort :: [Int] -> [Int]
quicksort [] = []
quicksort (x:xs) = quicksort (filter (>x) xs) ++ [x] ++ quicksort (filter (<=x) xs)

group :: String -> [String]
group x = lines x

groupSum :: [String] -> [Int]
groupSum [] = []
groupSum xs = groupSumAux xs []

groupSumAux :: [String] -> [Int] -> [Int]
groupSumAux [] ys = ys
groupSumAux ("":xs) ys = groupSumAux xs (0:ys)
groupSumAux (x:xs) [] = groupSumAux xs [read x]
groupSumAux (x:xs) (y:ys) = groupSumAux xs ((read x)+y:ys)
