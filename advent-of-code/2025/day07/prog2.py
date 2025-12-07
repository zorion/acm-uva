Line = str
Lines = list[Line]
Problem = Lines
Result = int
Beams = dict[int, int]

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
    beams = {}
    log_print(problem)
    for line in problem:
        beams = simulate_drop(beams, line)
        log_print(line, beams)
    return sum(beams.values())


def simulate_drop(beams: Beams, line: str) -> Beams:
    def _add(pos, already_pos, howmany):
        if 0 <= pos < len(line):
            if pos not in already_pos:
                already_pos[pos] = 0
            already_pos[pos] += howmany

    beam_res = {}
    for b in beams:
        if line[b] == SPLITTER:
            _add(b - 1, beam_res, beams[b])
            _add(b + 1, beam_res, beams[b])
        else:
            assert line[b] == EMPTY, line[b]
            _add(b, beam_res, beams[b])
    if not beam_res:
        # Find starter
        for i, s in enumerate(line):
            if s == STARTER:
                beam_res[i] = 1
                break
    return beam_res


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
