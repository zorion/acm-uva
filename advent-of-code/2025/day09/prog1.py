Line = str
Lines = list[Line]
Problem = Lines
Point = tuple[int, int]
Area = int
Result = Area

DEBUG = True


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
    points = parse_problem(problem)
    result = solve(points)

    return result


def area(p1: Point, p2: Point):
    return abs(p1[0] - p2[0] + 1) * abs(p1[1] - p2[1] + 1)


def parse_problem(problem: Problem) -> list[Point]:
    points = []
    for line in problem:
        x, y = tuple(int(s) for s in line.split(","))
        points.append((x, y))
    log_print("Points:", points)
    return points


def solve(points: list[Point]) -> Result:
    result = 0
    for i, point1 in enumerate(points):
        for point2 in points[i + 1 :]:
            aux = area(point1, point2)
            if result < aux:
                log_print(point1, point2, aux, result)
                result = aux
    return result


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
