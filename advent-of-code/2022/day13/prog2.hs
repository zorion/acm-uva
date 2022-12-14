
main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.getSolution.(map getPacket).addDividers.lines

type Packet = PData
data PData = List [PData] | Data Int deriving (Show)
data Token = Open | Close | Comma | Val Int deriving (Show)
data Ordenation = OGT | OLT | OEQ deriving (Show, Eq)

qs :: [Packet] -> [Packet]
qs [] = []
qs (x:xs) = (qs lowers) ++ [x] ++ qs greaters
    where lowers = filter (\y-> getOrdered (x, y) == OLT) xs
          greaters = filter (\y-> getOrdered (x, y) == OGT) xs

getSolution :: [Packet]  -> Int
getSolution = (\ (x, y) -> x*y).findDividers.(zip [0..]).qs

addDividers :: [String] -> [String]
addDividers xs = "[[2]]":"[[6]]":xs

findDividers :: [(Int, Packet)] -> (Int, Int)
findDividers xs = (divider1, divider2)
    where divider1 = findPack (getPacket "[[2]]") xs
          divider2 = findPack (getPacket "[[6]]") xs
          findPack packet (x:xs) = if (getOrdered (packet, p) == OEQ) then n else m
            where (n, p) = x
                  m = findPack packet xs

showPacket :: Packet -> String
showPacket (List []) = ""
showPacket (List (x:xs)) = '[':showPacket(x)++showPacket(List xs)++"]"
showPacket (Data x) = show x

getPacket :: String -> Packet
getPacket input = packet
    where tokens = parseTokens input
          (packet, _) = parsePacket [] tokens
          (packet', _) = parsePacket [] (tail tokens) -- We already assume in the first list

parsePacket :: [PData] -> [Token] -> (Packet, [Token])
parsePacket acc [] = (List acc, [])
parsePacket acc (Close:xs) = (List acc, xs)
parsePacket acc (Open:xs) = parsePacket prePack ys
    where (subPack, ys) = parsePacket [] xs
          prePack = acc ++ [subPack]
          prePack' = joinPackets acc (List [subPack])

parsePacket acc (Comma:xs) = parsePacket acc xs -- Commas are ignored in tokens
parsePacket acc (Val x:xs) = parsePacket(acc ++ [Data x]) xs

joinPackets :: [PData] -> Packet -> Packet
joinPackets [] y = y
joinPackets xs (Data y) = List (xs++[Data y])
joinPackets xs (List ys) = List (xs++ys)

parseTokens :: String -> [Token]
parseTokens [] = []
parseTokens ('[':xs) = Open:parseTokens xs
parseTokens (']':xs) = Close:parseTokens xs
parseTokens (',':xs) = Comma:parseTokens xs
parseTokens xs = Val num:parseTokens rest
    where (toComma, fromComma) = break (==',') xs
          (toPar, fromPar) = break (==']') toComma
          num = read toPar
          rest = fromPar ++ fromComma

getOrdered :: (Packet, Packet) ->  Ordenation
getOrdered (pA,pB) = case isOrdered pA pB of
    Just True -> OGT 
    Just False -> OLT 
    Nothing -> OEQ

isOrdered :: Packet -> Packet -> Maybe Bool
isOrdered (Data a) (Data b) = if a == b then Nothing else Just (a<b)
isOrdered (Data a) (List b) = isOrdered (List [Data a]) (List b)
isOrdered (List a) (Data b) = isOrdered (List a) (List [Data b])
isOrdered (List []) (List []) = Nothing
isOrdered (List (x:xs)) (List []) = Just False
isOrdered (List []) (List (x:xs)) = Just True
isOrdered (List (x:xs)) (List (y:ys)) = case isOrdered x y of
    Nothing -> isOrdered (List xs) (List ys)
    Just b -> Just b
