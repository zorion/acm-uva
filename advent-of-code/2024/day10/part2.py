from __future__ import annotations

type Pos = tuple[int, int]


def main():
    puzzle = read_map()
    result = solve_puzzle(puzzle)
    print_results(result)


def solve_puzzle(puzzle: list[str]) -> list[int]:
    result = []
    for i, line in enumerate(puzzle):
        for j, start in enumerate(line):
            if start == "0":
                result.append(_explore((i, j), puzzle))
    return result


def _explore(p: Pos, puzzle: list[str], *, __cache={}) -> list[int]:
    if p in __cache:
        return __cache[p]
    if not _is_valid(p, puzzle):
        return 0
    i, j = p
    height = puzzle[i][j]
    if height == "9":
        return 1
    subtotal = 0
    for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if not _is_valid((i + x, j + y), puzzle):
            continue
        new_val = puzzle[i + x][j + y]
        if new_val == str(int(height) + 1):
            subtotal += _explore((i + x, j + y), puzzle, __cache=__cache)
    __cache[(i, j)] = subtotal
    return subtotal


def _is_valid(p: Pos, puzzle: list[str]) -> bool:
    i, j = p
    if i < 0 or j < 0 or i >= len(puzzle) or j >= len(puzzle[0]):
        return False
    else:
        return True


def print_results(result: list[int]) -> None:
    print("Result:", sum(result))


def read_map() -> list[str]:
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
