from __future__ import annotations

type Maze = list[str]


def main():
    mapin, instructions = read_puzzle()
    solution = solve_puzzle(mapin, instructions)
    print_results(solution)


def solve_puzzle(mapin: Maze, instructions: str) -> Maze:
    print(mapin)
    print(instructions)
    return mapin


def read_puzzle() -> tuple[Maze, str]:
    maze = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
        except Exception:
            break
        maze.append(line)
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
