Line = str
Lines = list[Line]
Problem = Lines
Result = int

DEBUG = True
SPLITTER = "^"
STARTER = "S"
EMPTY = "."


def read_data() -> Problem:
    raw = read_subproblem()
    return raw


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
    beams = []
    splits = 0
    log_print(problem)
    for line in problem:
        aux, beams = simulate_drop(beams, line)
        splits += aux
    return splits


def simulate_drop(beams: list[int], line: str) -> tuple[int, list[int]]:
    def _add(pos, already_pos):
        if pos not in already_pos and 0 <= pos < len(line):
            already_pos.append(pos)

    res_beams = []
    splits = 0
    for b in beams:
        if line[b] == SPLITTER:
            splits += 1
            _add(b - 1, res_beams)
            _add(b + 1, res_beams)
        else:
            assert line[b] == EMPTY, line[b]
            _add(b, res_beams)
    if not res_beams:
        # Find starter
        for i, s in enumerate(line):
            if s == STARTER:
                res_beams.append(i)
                break

    return splits, res_beams


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


def log_print(*args, **kwargs):
    if DEBUG:
        pprint(*args, **kwargs)


def pprint(*args, **kwargs):
    text = args[0]
    if isinstance(text, list) and isinstance(text[0], str):
        for line in text:
            print(line, *args[1:], **kwargs)
    else:
        print(*args, **kwargs)


if __name__ == "__main__":
    main()
