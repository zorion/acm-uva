Problem = list[str]
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
    status = 50
    res = 0
    for instr in data:
        aux, status = run_instr(instr, status)
        res += aux
    return res


def _f(dir: str) -> int:
    return {"R": 1, "L": -1}[dir]


def run_instr(instr: str, status: int) -> tuple[int, int]:
    dir = instr[0]
    steps = int(instr[1:])
    new_status = (status + _f(dir) * steps) % 100
    print(new_status)
    return 1 if new_status == 0 else 0, new_status


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


if __name__ == "__main__":
    main()
