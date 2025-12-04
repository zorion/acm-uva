Puzzle = str
Problem = list[Puzzle]
Result = int

PAPER = "@"
SPACE = "."
DEBUG = True


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


def log_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def run(data: Problem) -> Result:
    res = 0
    for i, row in enumerate(data):
        for j, pos in enumerate(row):
            aux = 0
            if pos == PAPER:
                aux = explore_paper(data, i, j)
            res += aux
            if aux:
                log_print("x", end="")
            else:
                log_print(pos, end="")
        log_print("")
    return res


def explore_paper(data: Problem, i: int, j: int) -> int:
    return (
        1
        if 4
        > sum(
            [
                is_paper(data, x, y)
                for x in [i - 1, i, i + 1]
                for y in [j - 1, j, j + 1]
                if (x, y) != (i, j)
            ]
        )
        else 0
    )


def is_paper(data: Problem, i: int, j: int) -> int:
    return (0 <= i < len(data)) and (0 <= j < len(data[0])) and (data[i][j] == PAPER)


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


if __name__ == "__main__":
    main()
