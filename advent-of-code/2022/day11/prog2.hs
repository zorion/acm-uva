import qualified Data.Map as DM

main :: IO ()
main = do
    interact prob1
    putStrLn ""

prob1 :: String -> String
prob1 = show.evaluate.getStatus.(simulate 10000).getInput

type State = (Inspections, Items)
type Inspections = DM.Map Monkey Int
type Items = DM.Map Monkey [Item]
type Item = Int  -- with the "`mod` 2*3*5*7*11*13*17*19*23" hack we don't need Integer

type Monkey = Int
type Rules = DM.Map Monkey Rule
type Rule = (Operation, Test, Monkey, Monkey)
type Operation = Item -> Item
type Test = Item -> Bool
fakeRule :: Rule
fakeRule = ((+0), (==0), 0,0)


getStatus :: (Int, Rules, State) -> State
getStatus (_, _, s) = s
getInspections :: State -> Inspections
getInspections (ins, its) = ins

evaluate :: State -> Int
evaluate (inspections, _) = product (take 2 bestValues)
    where bestValues = qs allValues  --quicksort
          allValues = DM.elems inspections

simulate :: Int -> (Int, Rules, State) -> (Int, Rules, State)
simulate 0 (reducer, rules, state) = (reducer, rules, state)
simulate n (reducer, rules, state) = simulate (n-1) (reducer, rules, simulateRound reducer rules state)

simulateRound :: Int -> Rules -> State -> State
simulateRound reducer rules state = foldl (simulateTurn reducer rules) state (DM.keys rules)

-- For each item in the Monkey's Items apply the Rule, add Inspections and throw it
simulateTurn :: Int -> Rules -> State -> Monkey -> State
simulateTurn reducer rules state monkey = foldl (simulateRule reducer ruleMonkey) statePartial oldItemsMonkey
    where (oldInspections, oldItems) = state
          oldInspMonkey = DM.findWithDefault 0 monkey oldInspections
          newInspections = DM.insert monkey (oldInspMonkey + (length oldItemsMonkey)) oldInspections
          oldItemsMonkey = DM.findWithDefault [] monkey oldItems
          statePartial = (newInspections, itemsPartial)
          itemsPartial = DM.insert monkey [] oldItems
          ruleMonkey = DM.findWithDefault fakeRule monkey rules

simulateRule :: Int -> Rule -> State -> Item -> State
simulateRule reducer rule state item = (inspections, newItems)
    where (op, t, mTrue, mFalse) = rule
          (inspections, oldItems) = state
          newItem = (op item) `mod` reducer  -- no longer divided by three
          newMonkey = if t newItem then mTrue else mFalse
          oldMonkeyItems = DM.findWithDefault [] newMonkey oldItems
          newItems = DM.insert newMonkey (oldMonkeyItems ++ [newItem]) oldItems

-- reducer = 23*19*13*17*5*7*2*3*11

----------------------------------------
-- WORK ON INPUTS
----------------------------------------
--Monkey Int:
--  Starting items: [Int]
--  Operation: new = old Operation
--  Test: divisible by Int
--    If true: throw to monkey Int
--    If false: throw to monkey Int
--(ENDLINE)

getInput :: String -> (Int, Rules, State)
getInput input = getPartialInput (1, DM.empty, (DM.empty, DM.empty)) 0 (lines input)

getPartialInput :: (Int, Rules, State) -> Monkey -> [String] -> (Int, Rules, State)
getPartialInput status _ [] = status
getPartialInput status n ("":ys) = getPartialInput status n ys
getPartialInput status _ (('M':'o':'n':'k':'e':'y':' ':xs):ys) = getPartialInput status (read(take 1 xs)) ys
getPartialInput status n ((' ':' ':'S':'t':'a':'r':'t':'i':'n':'g':' ':'i':'t':'e':'m':'s':':':' ':xs):ys) = getPartialInput newStatus n ys
    where newStatus = (moder, rules, newStat)
          (moder, rules, oldStat) = status
          newStat = (inspections, newItems)
          (inspections, oldItems) = oldStat
          newItems = DM.insert n (parseItems xs) oldItems
getPartialInput status n (ops:test:monkeyTrue:monkeyFalse:ys3) = getPartialInput newStatus n ys3
    where newStatus = (newModer, newRules, stat)
          (moder, oldRules, stat) = status
          operation = parseOperation(ops)
          (newM, testOp) = parseTest(test)
          mTrue = parseMonkey(monkeyTrue)
          mFalse = parseMonkey(monkeyFalse)
          newRules = DM.insert n (operation, testOp, mTrue, mFalse) oldRules
          newModer = moder * newM


parseItems :: String -> [Item]
parseItems [] = []
parseItems xs = (read y) : parseItems zs
    where (y, ys) = break (==',') xs
          zs = case ys of
            [] -> []
            ',':' ':ss -> ss

--  Operation: new = old Operation  (* 6, * old, + 7, ...) 
parseOperation :: String -> (Item -> Item)
parseOperation xs 
    | restOp == "* old" = (^2)
    | headrestOp == '*' = (* (read (drop2restOp)))
    | headrestOp == '+' = (+ (read (drop2restOp)))
        where restOp = drop (length "  Operation: new = old ") xs
              headrestOp = head restOp
              drop2restOp = drop 2 restOp

--  Test: divisible by Int
parseTest :: String -> (Int, Item -> Bool)
parseTest xs = (numDiv, \x -> 0 == (mod x numDiv))
    where numDiv= read (drop (length "  Test: divisible by ") xs)

--    If true: throw to monkey Int
--    If false: throw to monkey Int
parseMonkey :: String -> Monkey
parseMonkey xs = read x
    where (_, ys) = break (=='y') xs -- ("If xxx: throw to monke", "y Int")
          x = drop 2 ys -- Int

qs :: [Int] -> [Int]
qs [] = []
qs (x:xs) = qs (filter (>x) xs) ++ [x] ++ qs (filter (<=x) xs)