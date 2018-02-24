module Problems010
(
myLast,       --Problem01
myButLast,    --Problem02
elementAt,    --Problem03
myLength,     --Problem04
myReverse,    --Problem05
isPalindrome, --Problem06
flatten,      --Problem07
compress,     --Problem08 
pack,         --Problem09
encode,       --Problem10
) where

myLast        :: [a] -> a
myLast (x:[]) = x
myLast (x:xs) = myLast xs

myButLast          :: [a] -> a
myButLast (x:y:[]) = x
myButLast (x:xs)   = myButLast(xs)

elementAt :: [a] -> Int -> a
elementAt (x:xs) 1 = x
elementAt (x:xs) i = elementAt xs (i-1)

myLength :: [a] -> Int
myLength [] = 0
myLength (x:xs) = 1 + myLength xs
 
myReverse :: [a] -> [a]
myReverse [] = []
myReverse (x:xs) = myReverse(xs) ++ [x]

isPalindrome :: (Eq a) => [a] -> Bool
isPalindrome []   = True
isPalindrome (x:[]) = True
isPalindrome (x:y:[]) = x == y
isPalindrome xs = myReverse xs == xs

data NestedList a = Elem a | List [NestedList a]
flatten :: NestedList a -> [a]
flatten (Elem a) = [a]
flatten (List []) = []
flatten (List (a:as)) = flatten a ++ flatten (List as)

compress :: Eq a => [a] -> [a]
compress [] = []
compress [x] = [x]
compress [x, y] = if x == y then [x] else [x, y]
compress (x:y:z:xs) = compress3 x y z ++ compress (z:xs)
    where
        compress3 x y z = if x == y then compress2 y z else (x:compress2 y z)
        compress2 x y = if x == y then [] else [x]

pack        :: Eq a => [a] -> [[a]]
pack []     = []
pack (x:xs) = pack_aux [] [x] xs
    where pack_aux rs ys []         = rs ++ [ys]
          pack_aux rs (y:ys) (z:zs) = if y == z
            then pack_aux rs (z:y:ys) zs
            else pack_aux (rs++[y:ys]) [z] zs

encode        :: Eq a => [a] -> [(Int, a)]
encode []     = []
encode (x:xs) = encode_aux [] (1, x) xs
    where encode_aux rs yt []         = rs ++ [yt]
          encode_aux rs (i, y) (z:zs) = if y == z
            then encode_aux rs (i + 1, y) zs           -- Accumulate old Value
            else encode_aux (rs++[(i, y)]) (1, z) zs   -- New value
