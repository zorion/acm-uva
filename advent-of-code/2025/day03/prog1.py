Puzzle = str
Problem = list[Puzzle]
Result = int


def read_data() -> Problem:
    finished = False
    res = []
    while not finished:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            finished = True
        else:
            res.append(line)
    return res


def run(data: Problem) -> Result:
    res = 0
    for puzzle in data:
        aux = get_max_2num(puzzle)
        print(puzzle, aux)
        res += aux

    return res


def get_max_2num(puzzle: Puzzle) -> int:
    maxnum = 0
    for i, c1 in enumerate(puzzle):
        for c2 in puzzle[i + 1 :]:
            num = int(c1 + c2)
            if num > maxnum:
                maxnum = num
    return maxnum


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


if __name__ == "__main__":
    main()
