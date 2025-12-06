Line = str
Lines = list[Line]
Problem = tuple[list[str], list[list[int]]]
Result = int

DEBUG = True


def read_data() -> Problem:
    raw = read_subproblem()
    ops, data = to_problem(raw)
    print(ops)
    print(data)
    assert {len(ops)} == {len(r) for r in data}
    return ops, data


def to_problem(raw: Lines) -> Problem:
    ops = [op.strip() for op in raw[-1].split()]
    data = [[int(v) for v in row.split()] for row in raw[:-1]]
    return ops, data


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
    ops, data = problem
    res = 0
    for i, op in enumerate(ops):
        aux = apply_op(op, [ro[i] for ro in data])
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
