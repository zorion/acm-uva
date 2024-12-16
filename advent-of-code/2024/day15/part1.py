from __future__ import annotations

type Maze = list[list[str]]


def main():
    mapin, instructions = read_puzzle()
    solution = solve_puzzle(mapin, instructions)
    print_results(solution)


def solve_puzzle(mapin: Maze, instructions: str) -> Maze:
    for instr in instructions:
        apply_instr(mapin, instr)
    return mapin


def print_maze(mapin: Maze) -> None:
    for line in mapin:
        print("".join(line))


def apply_instr(mapin: Maze, instr: str) -> None:
    rx, ry = find_robot(mapin)
    if instr == "<":
        move = (-1, 0)
    elif instr == ">":
        move = (1, 0)
    elif instr == "^":
        move = (0, -1)
    elif instr == "v":
        move = (0, 1)
    else:
        raise ValueError(f"Invalid instruction: {instr}")
    px, py = rx, ry
    stack = []
    while mapin[py][px] not in ["#", "."]:
        stack.append((px, py))
        px, py = px + move[0], py + move[1]
    if mapin[py][px] == "#":
        # Do nothing
        return
    assert mapin[py][px] == "."
    while stack:
        x, y = stack.pop()
        mapin[py][px] = mapin[y][x]
        px, py = x, y
    mapin[ry][rx] = "."


def find_robot(mapin: Maze) -> tuple[int, int]:
    for j, line in enumerate(mapin):
        for i, c in enumerate(line):
            if c == "@":
                return i, j


def read_puzzle() -> tuple[Maze, str]:
    maze = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
        except Exception:
            break
        maze.append([c for c in line])
    instructions = ""
    while True:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            break
        instructions += line
    return maze, instructions


def print_results(solution: Maze) -> None:
    result = 0
    for j, line in enumerate(solution):
        for i, c in enumerate(line):
            if c == "O":
                pos = 100 * j + i
                result += pos
    print("Result:", result)


if __name__ == "__main__":
    main()
