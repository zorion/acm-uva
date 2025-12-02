import math

Puzzle = tuple[str, str]
Problem = list[Puzzle]
Result = int


def read_data() -> Problem:
    line = input()
    pairs = line.split(",")
    res = [tuple(p.split("-")) for p in pairs]
    return res


def run(data: Problem) -> Result:
    res = 0
    for pair in data:
        aux = get_invalids(pair)
        print(pair, aux)
        res += aux

    return res


def get_invalids(pair: Puzzle) -> int:
    sza, szb = pair
    b = int(szb)
    tester = "1" + "0" * (math.ceil(len(sza) / 2) - 1)
    res = 0
    while not_too_big(tester, b):
        tt = tester + tester
        if len(tt) > len(sza) or (tt >= sza and len(tt) == len(sza)):
            res += int(tt)
        tester = next(tester)
    return res


def not_too_big(tester: str, b: int) -> bool:
    aux = int(tester + tester) <= b
    return aux


def next(tester: str) -> str:
    return str(int(tester) + 1)


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


if __name__ == "__main__":
    main()
