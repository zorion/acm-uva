def main():
    puzzle = read_puzzle()
    result = solve_puzzle(puzzle)
    print_results(result)


def solve_puzzle(puzzle: list[str]) -> int:
    result = 0
    for i, line in enumerate(puzzle):
        for j, start in enumerate(line):
            if start == "A":
                result += _explore(i, j, puzzle)
    return result


def _explore(i: int, j: int, puzzle: list[str]) -> int:
    expected = {"M", "A", "S"}
    if (
        _get_diagonal(i, j, puzzle, 1) == expected
        and _get_diagonal(i, j, puzzle, -1) == expected
    ):
        return 1
    return 0


def _get_diagonal(i: int, j: int, puzzle: list[str], direction: int) -> set[str]:
    positions = [(-1, -1 * direction), (0, 0), (1, direction)]
    result = {_get_pos(i + x, j + y, puzzle) for x, y in positions}
    return result


def _get_pos(i: int, j: int, puzzle: list[str]) -> str:
    if i < 0 or j < 0 or i >= len(puzzle) or j >= len(puzzle[0]):
        return ""
    return puzzle[i][j]


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
