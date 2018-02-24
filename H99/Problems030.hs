module Problems030 (
insertAt,     --Problem 21
range,        --Problema22
rnd_select,   --Problem 23
diff_select,  --Problem 24
rnd_permu,    --Problem 25
combinations, --Problem 26
group,        --Problem 27
lsort,        --Problem 28a
lfsort,       --Problem 28b
) where

import Problems010
import Problems020
import System.Random


insertAt :: a -> [a] -> Int -> [a]
insertAt x xs 0 = x:xs
insertAt x [] _ = [x]
insertAt x xs n 
    | n > len   = insertAt x xs (n - len)
    | n > 0     = y:(insertAt x ys (n-1))
    | otherwise = insertAt x xs (len + n)
    where len    = myLength xs
          (y:ys) = xs

range       :: Int -> Int -> [Int]
range m n   | n < m     = []
            | otherwise = m:range (m+1) n


rnd_select x = x
diff_select x = x
rnd_permu x = x
combinations x = x
group x = x
lsort x = x
lfsort x = x

