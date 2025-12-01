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
    dir = _f(instr[0])
    steps = int(instr[1:])
    new_status = status + dir * steps
    if dir < 0:
        if new_status <= 0:
            extra = (-new_status // 100) + (1 if status != 0 or new_status == 0 else 0)
        else:
            extra = 0
    else:
        extra = new_status // 100
    print(extra, status, new_status, instr, dir)
    new_status = new_status % 100

    return extra, new_status


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


if __name__ == "__main__":
    main()
