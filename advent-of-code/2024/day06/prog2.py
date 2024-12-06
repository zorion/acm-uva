from __future__ import annotations


def main():
    puzzle = read_puzzle()
    path = solve_puzzle(puzzle)
    print_results(path)


def solve_puzzle(puzzle: list[str]) -> set[(int, int)]:
    x, y, status = find_initial(puzzle)
    result = set()
    real_path = solve_part1(puzzle)
    for i, j in real_path:
        new_puzzle = add_obstacle(puzzle, i, j)
        if find_loop(x, y, status, new_puzzle):
            result.add((i, j))
    return result


def solve_part1(puzzle: list[str]) -> set[(int, int)]:
    x, y, status = find_initial(puzzle)
    path = set()
    while status != "end":
        path.add((x, y))
        x, y, status = find_next(x, y, status, puzzle)
    return path


def add_obstacle(puzzle: list[str], i: int, j: int) -> list[str]:
    new_puzzle = puzzle.copy()
    new_puzzle[i] = new_puzzle[i][:j] + "#" + new_puzzle[i][j + 1 :]
    return new_puzzle


def find_loop(x: int, y: int, status: str, puzzle: list[str]) -> bool:
    path = set()
    while status != "end":
        path.add((x, y, status))
        x, y, status = find_next(x, y, status, puzzle)
        if (x, y, status) in path:
            # LOOP!!!
            return True
    return False  # 'end' got!


def find_initial(puzzle: list[str]) -> tuple[int, int, str]:
    for i, line in enumerate(puzzle):
        for j, val in enumerate(line):
            if val in "^<v>":
                return i, j, val
    raise ValueError(f"Invalid puzzle:\n{'\n'.join(puzzle)}")


def find_next(x: int, y: int, status: str, puzzle: list[str]) -> tuple[int, int, str]:
    if status == "<":
        i = x
        j = y - 1
        if j < 0:
            return x, y, "end"
    elif status == "^":
        i = x - 1
        j = y
        if i < 0:
            return x, y, "end"
    elif status == "v":
        i = x + 1
        j = y
        if i >= len(puzzle[0]):
            return x, y, "end"
    elif status == ">":
        i = x
        j = y + 1
        if j >= len(puzzle):
            return x, y, "end"
    else:
        raise ValueError(f"Invalid status: {status}")
    if puzzle[i][j] == "#":
        status = rotate(status)
        # From the previous position, new direction.
        return x, y, status
    return i, j, status


def rotate(status: str) -> str:
    if status == "<":
        return "^"
    elif status == "^":
        return ">"
    elif status == "v":
        return "<"
    elif status == ">":
        return "v"
    else:
        raise ValueError(f"Invalid status: {status}")


def print_results(path: set[(int, int)]) -> None:
    print("Result:", len(path))


def read_puzzle() -> list[str]:
    result = []
    finished = False
    while not finished:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            finished = True
        else:
            result.append(line)
    return result


if __name__ == "__main__":
    main()
