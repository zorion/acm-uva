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
    for i, puzzle in enumerate(data):
        aux = get_maxnum(puzzle, 12)
        print(f"{i}/{len(data)}", puzzle, aux)
        res += int(aux)

    return res


def get_maxnum(puzzle: Puzzle, n: int) -> str:
    if n < 1:
        return ""
    max_c = "0"
    inits = {str(i): [] for i in range(10)}
    if n == 1:
        max_c = max(puzzle)
        inits[max_c].append(0)
    else:
        for i, c in enumerate(puzzle[: -n + 1]):
            if c >= max_c:  # Keep the first max
                max_c = c
                inits[max_c].append(i)

    max_res = 0
    max_right = ""
    for max_ini in inits[max_c]:
        right_num = get_maxnum(puzzle[max_ini + 1 :], n - 1)
        test_val = int(max_c + right_num)
        if test_val > max_res:
            max_res = test_val
            max_right = right_num

    return max_c + max_right


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


if __name__ == "__main__":
    main()
