from __future__ import annotations

import re

type Robot = tuple[int, int]
type Movement = tuple[int, int]


def main():
    robots, movements = read_robots()
    for i in range(5):  # I runned this with 103 to check, change it to 5 as a sample
        test_pos = run_robots(robots, movements, 101, 103, i)
        print("\nRobots at second:", i)
        print_robots_map(test_pos)

    test_pos = run_robots(robots, movements, 101, 103, 29)
    print("At second 4 it was ok here above.")
    print("Also have a look at second number 29:")
    print_robots_map(test_pos)
    # Printing some results we see that the robots align in horizontal lines at 4 mod 103
    # And in vertical lines at 29 mod 101
    # So applying chinese reminders -> 6493
    solution = 6493
    res_map = run_robots(robots, movements, 101, 103, solution)
    print("\nSee the tree at second 6493:")
    print_robots_map(res_map)
    print("Solution:", solution)


def run_robots(
    robots: list[Robot], movements: list[Movement], width: int, height: int, steps: int
) -> list[Robot]:
    result = []
    for i, rob in enumerate(robots):
        result.append(_explore(rob, movements[i], width, height, steps))
    return result


def print_robots_map(robots: list[Robot], width: int = 101, height: int = 103):
    for y in range(height):
        for x in range(width):
            n = robots.count((x, y))
            if n == 0:
                print(" ", end="")
            else:
                print(n, end="")
        print("")


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


if __name__ == "__main__":
    main()
