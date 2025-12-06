Line = str
Lines = list[Line]
Puzzle = tuple[str, list[int]]
Problem = list[Puzzle]
Result = int

DEBUG = True


def read_data() -> Problem:
    raw = read_subproblem()
    puzzles = to_problem(raw)
    return puzzles


def to_problem(raw: Lines) -> Problem:
    puzzles = []
    aux = []
    for i in reversed(range(len(raw[0]))):
        val = []
        for r in raw[:-1]:
            val.append(r[i])
        log_print(i, val)
        if set(val) == {" "}:
            log_print("continue", op)
            continue
        aux.append(int("".join(val)))
        op = raw[-1][i]
        if op != " ":
            log_print("add", op, aux)
            puzzles.append((op, aux))
            aux = []
    return puzzles


def read_subproblem() -> Lines:
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


def run(problem: Problem) -> Result:
    res = 0
    for puzzle in problem:
        op, data = puzzle
        aux = apply_op(op, data)
        res += aux
    return res


def apply_op(op: str, rows: list[int]) -> int:
    if op == "*":
        res = 1
        for r in rows:
            res *= r
        return res
    if op == "+":
        res = 0
        for r in rows:
            res += r
        return res
    raise Exception(f"Unknown op {op}")


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


def log_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


if __name__ == "__main__":
    main()
