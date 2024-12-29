from __future__ import annotations

import queue

type Maze = tuple[tuple[str]]

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


def main():
    maze = read_maze()
    solution = find_solutions(maze)
    print_solution(solution)


def find_solutions(maze: Maze) -> int:
    def explore_paths(pos: tuple[int, int], dir: int) -> int:
        x, y = pos
        results = {}
        pending = queue.PriorityQueue()
        cost = 0
        pending.put((cost, x, y, dir))
        while not pending.empty():
            cost, x, y, dir = pending.get()
            if cost >= results.get((x, y, dir), cost + 1):
                continue
            if maze[y][x] == "#":
                continue
            for direction in [LEFT, UP, RIGHT, DOWN]:
                new_cost = cost
                if direction % 4 == (dir + 2) % 4:
                    new_cost += 2000
                if direction % 4 == (dir + 1) % 4:
                    new_cost += 1000
                if direction % 4 == (dir + 3) % 4:
                    new_cost += 1000
                if (x, y, direction) in results:
                    old_cost = results[(x, y, direction)]
                    if new_cost < old_cost:
                        results[(x, y, direction)] = new_cost
                else:
                    results[(x, y, direction)] = new_cost
                new_x, new_y = get_new_position((x, y), direction)
                new_cost += 1
                pending.put((new_cost, new_x, new_y, direction))
        x, y = find_position(maze, "E")
        return min(
            [results[(x, y, direction)] for direction in [LEFT, UP, RIGHT, DOWN]]
        )

    initial = find_position(maze, "S")
    res = explore_paths(initial, LEFT)
    return res


def find_position(maze: Maze, char: str) -> tuple[int, int]:
    for j, line in enumerate(maze):
        for i, c in enumerate(line):
            if c == char:
                return i, j


def get_new_position(pos: tuple[int, int], direction: int) -> tuple[int, int]:
    x, y = pos
    if direction == LEFT:
        return x - 1, y
    if direction == UP:
        return x, y - 1
    if direction == RIGHT:
        return x + 1, y
    if direction == DOWN:
        return x, y + 1


def print_maze(maze: Maze) -> None:
    print("\n".join(["".join(line) for line in maze]))


def read_maze() -> Maze:
    maze = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
        except Exception:
            break
        maze.append(tuple([c for c in line]))
    return tuple(maze)


def print_solution(solution: int) -> None:
    print("Result:", solution)


def score(solution: tuple[int, int]) -> int:
    (turns, forwards) = solution
    return 1000 * turns + forwards


if __name__ == "__main__":
    main()
