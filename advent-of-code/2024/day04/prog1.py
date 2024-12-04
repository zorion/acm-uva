def main():
    puzzle = read_puzzle()
    result = solve_puzzle(puzzle)
    print_results(result)


def solve_puzzle(puzzle: list[str]) -> int:
    result = 0
    for i, line in enumerate(puzzle):
        for j, start in enumerate(line):
            if start == "X":
                result += _explore(i, j, puzzle)
    return result


def _explore(i: int, j: int, puzzle: list[str]) -> int:
    directions = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x or y]
    result = 0
    for vel in directions:
        x, y = vel
        if _explore_direction(i, j, x, y, puzzle, "XMAS"):
            result += 1
    return result


def _explore_direction(
    i: int, j: int, x: int, y: int, puzzle: list[str], rem: str
) -> bool:
    if not rem:
        return True
    if i < 0 or j < 0 or i >= len(puzzle) or j >= len(puzzle[0]):
        return False
    if puzzle[i][j] != rem[0]:
        return False
    return _explore_direction(i + x, j + y, x, y, puzzle, rem[1:])


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


def print_results(result: int) -> None:
    print("Result:", result)


if __name__ == "__main__":
    main()
