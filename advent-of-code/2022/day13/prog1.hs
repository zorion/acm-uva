
main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.sum.(map getOrdered).(getProblems 1).lines

type Packet = PData
data PData = List [PData] | Data Int deriving (Show)
data Token = Open | Close | Comma | Val Int deriving (Show)

getProblems :: Int -> [String] -> [(Int, Packet, Packet)]
getProblems _ [] = []
getProblems n ("":xs) = getProblems n xs
getProblems n (x:y:xs) = (n, getPacket x, getPacket y):getProblems (n+1) xs

-- [ -> getSubpacket
-- , -> continue previous
-- ] -> return (finished)
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

-- -- Result is the packet got, pending string and shallContinue
-- getSubpacket :: String -> (Packet, String, Bool)
-- getSubpacket "" = (List [], "", False)
-- getSubpacket (']':ys) = (List [], tys, hys) 
--     where lys = length ys
--           hys = if lys > 0 then head ys == ',' else False
--           tys = if hys then tail ys else ys
-- getSubpacket (',':xs) = (subPack, ys, True)
--     where (subPack, ys, cont) = getSubpacket xs
-- getSubpacket ('[':xs) = (subPack, tys, hys)
--     where (subPack1, zs, cont) = getSubpacket xs
--           lys = length ys
--           hys = if lys > 0 then head ys == ',' else False
--           tys = if hys then tail ys else ys
-- getSubpacket xs = (subPack1, tys, hys)
--     where
--           lys = length ys
--           hys = if lys > 0 then head ys == ',' else False
--           tys = if hys then tail ys else ys


getOrdered :: (Int, Packet, Packet) ->  Int
getOrdered (n,pA,pB) = case isOrdered pA pB of
    Just True -> n 
    Just False -> 0
    Nothing -> 0 

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
