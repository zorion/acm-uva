Line = str
Lines = list[Line]
Problem = Lines
Point = tuple[int, int, int]
Points = list[Point]
Circuit = list[Point]
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
    result = get_circuits(problem)
    return result


def get_circuits(problem: Problem) -> Result:
    points = parse_points(problem)
    distance_points = get_distances_sorted(points)
    circuit_by_point = {}
    points_in_circuit = {}
    max_circuit = 0
    for dist_points in distance_points:
        _, point1, point2 = dist_points
        c1 = circuit_by_point.get(point1)
        c2 = circuit_by_point.get(point2)
        if c1 is None and c2 is None:
            # New circuit
            idx = max_circuit
            max_circuit += 1
            points_in_circuit[idx] = [point1, point2]
            circuit_by_point[point1] = idx
            circuit_by_point[point2] = idx
        elif c1 is None and c2 is not None:
            points_in_circuit[c2].append(point1)
            circuit_by_point[point1] = c2
            idx = c2
        elif c2 is None and c1 is not None:
            points_in_circuit[c1].append(point2)
            circuit_by_point[point2] = c1
            idx = c1
        elif c1 == c2:
            # same circuit, already, should it count for size?
            idx = c1
        else:
            # Merge the two circuits
            points_in_circuit[c1].extend(points_in_circuit[c2])
            for p in points_in_circuit[c2]:
                circuit_by_point[p] = c1
            del points_in_circuit[c2]
            idx = c1
        if len(points_in_circuit[idx]) == len(problem):
            log_print("one circuit in junction", point1, point2)
            return point1[0] * point2[0]


def get_distances_sorted(points: Points) -> list[tuple[int, Point, Point]]:
    result = []
    for i, point1 in enumerate(points):
        for point2 in points[i + 1 :]:
            result.append((distance(point1, point2), point1, point2))
    return sorted(result)


def distance(point1: Point, point2: Point) -> int:
    def sq(x: int) -> int:
        return x * x

    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return sq(x1 - x2) + sq(y1 - y2) + sq(z1 - z2)


def parse_points(problem: Problem) -> Points:
    points = {}
    for line in problem:
        x, y, z = map(int, line.split(","))
        points[(x, y, z)] = None
    return list(points.keys())


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
