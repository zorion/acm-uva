from __future__ import annotations
import re

type Robot = tuple[int, int]
type Movement = tuple[int, int]


def main():
    robots, movements = read_robots()
    result = run_robots(robots, movements, 101, 103, 100)
    print_results(result, 101, 103)


def run_robots(
    robots: list[Robot], movements: list[Movement], width: int, height: int, steps: int
) -> list[Robot]:
    result = []
    for i, rob in enumerate(robots):
        result.append(_explore(rob, movements[i], width, height, steps))
    return result


def _explore(
    robot: Robot, movement: Movement, width: int, height: int, steps: int
) -> Robot:
    x, y = robot
    dx, dy = movement
    x += dx * steps
    y += dy * steps
    x = x % width
    y = y % height
    return (x, y)


def print_results(result: list[Robot], width: int, height: int) -> int:
    print(get_results(result, width, height))


def get_results(robots: list[Robot], width: int, height: int) -> int:
    split_wide = width // 2
    split_tall = height // 2
    total_q1 = 0  # Up left
    total_q2 = 0  # Up right
    total_q3 = 0  # Down left
    total_q4 = 0  # Down right
    for rob in robots:
        if rob[0] < split_wide and rob[1] < split_tall:
            total_q1 += 1
        if rob[0] > split_wide and rob[1] < split_tall:
            total_q2 += 1
        if rob[0] < split_wide and rob[1] > split_tall:
            total_q3 += 1
        if rob[0] > split_wide and rob[1] > split_tall:
            total_q4 += 1
    return total_q1 * total_q2 * total_q3 * total_q4


def read_robots() -> tuple[list[Robot], list[Movement]]:
    robots = []
    movements = []
    while True:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            break
        rob, mov = read_robot(line)
        robots.append(rob)
        movements.append(mov)
    return robots, movements


def read_robot(line: str) -> tuple[Robot, Movement]:
    match = re.search(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
    x, y, dx, dy = match.groups()
    return (int(x), int(y)), (int(dx), int(dy))


def test():
    robots = []
    movements = []
    with open("sample.in") as f:
        for line in f.readlines():
            rob, mov = read_robot(line)
            robots.append(rob)
            movements.append(mov)

    result = run_robots(robots, movements, 11, 7, 100)
    assert sorted(result) == sorted(
        [
            (6, 0),
            (6, 0),
            (9, 0),
            (0, 2),
            (1, 3),
            (2, 3),
            (5, 4),
            (3, 5),
            (4, 5),
            (4, 5),
            (1, 6),
            (6, 6),
        ]
    ), sorted(result)
    assert (res := get_results(result, 11, 7) == 12), f"Result {res} should be 12"


test()

if __name__ == "__main__":
    main()
