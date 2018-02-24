module Problems020 (
encodeModified,        --Problem11
decodeModified,        --Problem12
encodeDirect,          --Problem13
dupli,                 --Problem14
repli,                 --Problem 15
dropEvery,             --Problem16
split,                 --Problem17
slice,                 --Problem18
rotate,                --Problem19
removeAt,              --Problem20
) where

import Problems010

data MxThing a = Single a | Multiple Int a
  deriving (Show)


encodeModified :: Eq a => [a] -> [MxThing a]
encodeModified = (map transfAux) . encode
  where
    transfAux (1, x) = Single x
    transfAux (n, x) = Multiple n x


decodeModified :: [MxThing a] -> [a]
decodeModified [] = []
decodeModified (x:xs) = (decodeAux x) ++ decodeModified xs
  where
    decodeAux (Single y) = [y]
    decodeAux (Multiple 2 y) = [y, y]
    decodeAux (Multiple n y) = y:(decodeAux (Multiple (n-1) y))


encodeDirect :: Eq a => [a] -> [MxThing a]
encodeDirect [] = []
encodeDirect (x:xs) = encodeAux [] (1, x) xs
  where
    encodeAux rs (n, y) [] = if n == 1
        then rs ++ [Single y]
        else rs ++ [Multiple n y]
    encodeAux rs (n, y) (z:zs) = if y == z
        then encodeAux rs (n+1, y) zs
        else (encodeAux rs (n, y) []) ++ (encodeAux [] (1, z) zs)


dupli :: [a] -> [a]
dupli [] = []
dupli (x:xs) = x:x:dupli xs


repli :: [a] -> Int -> [a]
repli [] _ = []
repli (x:xs) n = repliOne x n ++ repli xs n
  where
    repliOne :: a -> Int -> [a]
    repliOne _ 0 = []
    repliOne y m = y:repliOne y (m-1)


dropEvery :: [a] -> Int -> [a]
dropEvery _ 0 = error "Don't try to drop every 0. What did you mean?"
dropEvery xs n = dropEveryAux xs n n
  where
    dropEveryAux [] _ _ = []
    dropEveryAux (x:xs) n 1 = dropEveryAux xs n n
    dropEveryAux (x:xs) n m = x:dropEveryAux xs n (m-1)


split :: [a] -> Int -> ([a], [a])
-- split [] _ = ([], [])
split xs n = splitAux [] xs n
  where
    splitAux xs [] _ = (xs, [])
    splitAux xs ys 0 = (xs, ys)
    splitAux xs (y:ys) n = splitAux (xs ++ [y]) ys (n-1)


slice :: [a] -> Int -> Int -> [a]
slice [] _ _     = []
slice _ 0 _      = error "Slice can't start by zero."
slice _ 1 0      = []
slice (x:xs) 1 n = x:slice xs 1 (n-1)
slice (x:xs) m n = slice xs (m-1) (n-1)


rotate :: [a] -> Int -> [a]
rotate xs 0 = xs
rotate (x:xs) n 
    | n > 0     = rotate (xs ++ [x]) (n-1)
    | otherwise = rotate (y:x:ys) (n+1)
        where
            ys = slice xs 1 (myLength xs - 1)
            y  = myLast xs


removeAt :: Int -> [a] -> (a, [a])
removeAt n xs = removeAtAux [] xs n
  where
    removeAtAux             :: [a] -> [a] -> Int -> (a, [a])
    removeAtAux _  []     _ = error "removeAt out of bounds."
    removeAtAux rs (x:xs) 1 = (x, rs ++ xs)
    removeAtAux rs (x:xs) n = removeAtAux (rs ++ [x]) xs (n-1)

