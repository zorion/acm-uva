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
        tot_aux = set()
        for times in range(2, len(pair[1]) + 1):
            aux = get_invalids(pair, times)
            print(pair, "x", times, ":", aux)
            tot_aux.update(aux)
        res += sum(map(int, tot_aux))

    return res


def get_invalids(pair: Puzzle, times: int) -> set[str]:
    sza, szb = pair
    b = int(szb)
    tester = "1" + "0" * (math.ceil(len(sza) / times) - 1)
    res = set()
    while not_too_big(tester, b, times):
        tt = tester * times
        if len(tt) > len(sza) or (tt >= sza and len(tt) == len(sza)):
            res.add(tt)
        tester = next(tester)
    return res


def not_too_big(tester: str, b: int, times: int) -> bool:
    aux = int(tester * times) <= b
    return aux


def next(tester: str) -> str:
    return str(int(tester) + 1)


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


if __name__ == "__main__":
    main()
