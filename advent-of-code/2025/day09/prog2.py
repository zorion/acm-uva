StrLine = str
StrLines = list[StrLine]
Problem = StrLines
Point = tuple[int, int]
Vector = Point
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

    for i, point1 in enumerate(polygon):
        for point2 in polygon[i + 1 :]:
            aux = area(point1, point2)
            if result < aux:  # Get the area is cheaper than checking insideness
                if is_rectangle_contained(polygon, point1, point2):
                    log_print("Rectangle", point1, point2, f"--  {aux} <-- {result}")
                    result = aux
    return result


def is_rectangle_contained(polygon: list[Point], p1: Point, p2: Point) -> bool:
    min_x = min(p1[0], p2[0])
    max_x = max(p1[0], p2[0])
    min_y = min(p1[1], p2[1])
    max_y = max(p1[1], p2[1])
    # Check the 4 rectangle's vertex are inside the polygon
    if not is_point_contained(polygon, (min_x, min_y)):
        return False
    if not is_point_contained(polygon, (min_x, max_y)):
        return False
    if not is_point_contained(polygon, (max_x, min_y)):
        return False
    if not is_point_contained(polygon, (max_x, max_y)):
        return False
    # Check the 4 rectangle's edges
    if not is_line_also_contained(polygon, (min_x, min_y), (min_x, max_y)):
        return False
    if not is_line_also_contained(polygon, (min_x, min_y), (max_x, min_y)):
        return False
    if not is_line_also_contained(polygon, (max_x, max_y), (min_x, max_y)):
        return False
    if not is_line_also_contained(polygon, (max_x, max_y), (max_x, min_y)):
        return False

    return True


def is_line_also_contained(polygon: list[Point], p1: Point, p2: Point) -> bool:
    """Provided p1 and p2 are within polygon, is the segment p1-p2 as well?"""
    pi = polygon[-1]
    for pj in polygon:
        if do_segments_intersect(pi, pj, p1, p2):
            return False
    return True


def _are_parallel(vi: Vector, vp: Vector) -> bool:
    return vi[0] * vp[1] == vi[1] * vp[0]


def do_segments_intersect(pi: Point, pj: Point, p1: Point, p2: Point) -> bool:
    """Do segments pi-pj and p1-p2 intersect?

    We check if the inner part of the line p1-p2 intersects this edge of the polygon
    Edge cases:
     - If they are parallel, it's ok. We don't mind if it partially out, yet.
     - If they intersect in p1 or p2 it's ok.

    pi-pj: P = pi + lambda * (pj - pi) for lambda in [0,1]
    p1-p2: P = p1 + mu * (p2 - p1) for mu in (0,1) (exclude p1 and p2)

    pi + lambda * (pj - pi) = p1 + mu * (p2 - p1)
    pix + lambda(pjx - pix) = p1x + mu(p2x - p1x)
    piy + lambda(pjy - piy) = p1y + mu(p2y - p1y)
    lambda(pjx - pix) = mu(p2x - p1x) - pix + p1x
    lambda(pjy - piy) = mu(p2y - p1y) - piy + p1y
    lambda = (mu(p2y - p1y) - piy + p1y) / (pjy - piy)
    lambda = (mu(p2x - p1x) - pix + p1x) / (pjx - pix)
    (mu(p2y - p1y) - piy + p1y) / (pjy - piy) = (mu(p2x - p1x) - pix + p1x) / (pjx - pix)
    mu(p2y - p1y)/(pjy - piy) - mu(p2x - p1x)/(pjx - pix) = (pix - p1x)/(pjx - pix) - (piy - p1y)/(pjy - piy)
    mu = ((pix - p1x)/(pjx - pix) - (piy - p1y)/(pjy - piy)) / ((p2y - p1y)/(pjy - piy) - (p2x - p1x)/(pjx - pix))

    Check if 0 < mu < 1

    """
    vi = (pj[0] - pi[0], pj[1] - pi[1])
    vp = (p2[0] - p1[0], p2[1] - p1[1])
    if _are_parallel(vi, vp):
        log_print("Parallel", vi, vp, "from", pi, pj, p1, p2)
        return False
    log_print("Not parallel", vi, vp, "from", pi, pj, p1, p2)
    mu = ((pi[0] - p1[0]) / (pj[0] - pi[0]) - (pi[1] - p1[1]) / (pj[1] - pi[1])) / (
        (p2[1] - p1[1]) / (pj[1] - pi[1]) - (p2[0] - p1[0]) / (pj[0] - pi[0])
    )
    log_print("mu", mu, "from", pi, pj, p1, p2)
    return 0 < mu < 1


def is_point_contained(polygon: list[Point], point: Point) -> bool:
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
