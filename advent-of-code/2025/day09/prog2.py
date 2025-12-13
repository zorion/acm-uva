from tqdm.auto import tqdm

StrLine = str
StrLines = list[StrLine]
Problem = StrLines
Point = tuple[int, int]
Area = int
Result = Area

DEBUG = True


def read_data() -> Problem:
    raw = read_subproblem()
    return raw


def read_subproblem() -> StrLines:
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


def solve(polygon: list[Point]) -> Result:
    result = 0

    for i, point1 in tqdm(enumerate(polygon)):
        for point2 in polygon[i + 1 :]:
            aux = area(point1, point2)
            if result < aux:  # Get the area is cheaper than checking insideness
                if is_rectangle_inside(polygon, point1, point2):
                    log_print("Rectangle", point1, point2, f"--  {aux} <-- {result}")
                    result = aux
    return result


def is_rectangle_inside(polygon: list[Point], p1: Point, p2: Point) -> bool:
    min_x = min(p1[0], p2[0])
    max_x = max(p1[0], p2[0])
    min_y = min(p1[1], p2[1])
    max_y = max(p1[1], p2[1])
    for i in range(min_x, max_x + 1):
        # Check horizontal lines are inside
        if not is_point_inside(polygon, (i, min_y)):
            return False
        if not is_point_inside(polygon, (i, max_y)):
            return False
    for i in range(min_y, max_y + 1):
        # Check vertical lines are inside
        if not is_point_inside(polygon, (min_x, i)):
            return False
        if not is_point_inside(polygon, (max_x, i)):
            return False
    return True


def is_point_inside(polygon: list[Point], point: Point) -> bool:
    # https://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html
    x, y = point
    # Closing the poligon with arrow point_N -> point_0
    pi = polygon[-1]
    inside = False
    for pj in polygon:
        if x == pi[0] == pj[0] and min(pi[1], pj[1]) <= y <= max(pi[1], pj[1]):
            # vertical edge
            return True
        if y == pi[1] == pj[1] and min(pi[0], pj[0]) <= x <= max(pi[0], pj[0]):
            # horizontal edge
            return True
        # arrow point_i -> point_j where j = i+1
        if y > min(pi[1], pj[1]):
            if y <= max(pi[1], pj[1]):
                if x <= max(pi[0], pj[0]):
                    if pi[1] != pj[1]:
                        xints = (y - pi[1]) * (pj[0] - pi[0]) / (pj[1] - pi[1]) + pi[0]
                    if pi[0] == pj[0] or x <= xints:
                        inside = not inside

        # get next point_i (the current point_j)
        pi = pj

    return inside


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
