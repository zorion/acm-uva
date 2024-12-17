from __future__ import annotations

type Maze = list[list[str]]


def main():
    mapin, instructions = read_puzzle()
    solution = solve_puzzle(mapin, instructions)
    print_results(solution)


def solve_puzzle(mapin: Maze, instructions: str) -> Maze:
    for instr in instructions:
        # print_maze(mapin)
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
    if can_be_moved(mapin, rx + move[0], ry + move[1], move):
        move_pieces(mapin, rx + move[0], ry + move[1], move, mapin[ry][rx])
        mapin[ry][rx] = "."


def can_be_moved(mapin: Maze, rx: int, ry: int, move: tuple[int, int]) -> bool:
    data = mapin[ry][rx]
    if data == "#":
        return False  # Cant't move
    if data == ".":
        return True
    if move[1] == 0:  # Horizontal move
        return can_be_moved(mapin, rx + move[0], ry, move)
    # Vertical move, double trouble
    if data == "[":
        can_left = can_be_moved(mapin, rx, ry + move[1], move)
        can_right = can_be_moved(mapin, rx + 1, ry + move[1], move)
        return can_left and can_right
    if data == "]":
        can_right = can_be_moved(mapin, rx, ry + move[1], move)
        can_left = can_be_moved(mapin, rx - 1, ry + move[1], move)
        return can_left and can_right
    raise ValueError(f"Invalid data: {data} in rx={rx}, ry={ry}")


def move_pieces(
    mapin: Maze, rx: int, ry: int, move: tuple[int, int], move_data: str
) -> None:
    data = mapin[ry][rx]
    if data == ".":
        pass  # Do nothing else
    elif move[1] == 0:  # Horizontal move
        move_pieces(mapin, rx + move[0], ry, move, data)
    elif data == "[":  # vertical move
        move_pieces(mapin, rx, ry + move[1], move, "[")
        move_pieces(mapin, rx + 1, ry + move[1], move, "]")
        mapin[ry][rx + 1] = "."
    elif data == "]":  # vertical move
        move_pieces(mapin, rx - 1, ry + move[1], move, "[")
        move_pieces(mapin, rx, ry + move[1], move, "]")
        mapin[ry][rx - 1] = "."
    else:
        raise ValueError(f"Invalid data: {data} in rx={rx}, ry={ry}")
    mapin[ry][rx] = move_data


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
        maze_line = []
        for c in line:
            if c in "#.":
                maze_line.append(c)
                maze_line.append(c)
            elif c == "@":
                maze_line.append(c)
                maze_line.append(".")
            elif c == "O":
                maze_line.append("[")
                maze_line.append("]")
            else:
                raise ValueError(f"Invalid character: {c}")
        maze.append(maze_line)
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
            if c == "[":
                pos = 100 * j + i
                result += pos
    print("Result:", result)


if __name__ == "__main__":
    main()
