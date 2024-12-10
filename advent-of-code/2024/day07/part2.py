from __future__ import annotations


def main():
    puzzle = read_puzzle()
    result = solve_puzzle(puzzle)
    print_results(result)


type Equation = tuple[int, list[int]]


def solve_puzzle(puzzles: list[Equation]) -> list[int]:
    result = []
    for equation in puzzles:
        target, steps = equation
        if solve_eq(steps[0], target, steps[1:]):
            result.append(target)
    return result


def solve_eq(acc: int, target: int, steps: list[int]) -> bool:
    if not steps:
        return acc == target
    for f in [add, mul, conc]:
        res = f(acc, steps[0])
        if solve_eq(res, target, steps[1:]):
            return True
    return False


def print_results(result: list[int]) -> None:
    print("Result:", sum(result))


def mul(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a + b


def conc(a: int, b: int) -> int:
    return int(str(a) + str(b))


def read_puzzle() -> list[Equation]:
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
            parts = line.split(": ")
            target = int(parts[0])
            subparts = map(int, parts[1].split(" "))
            res = (target, list(subparts))

            result.append(res)
    return result


if __name__ == "__main__":
    main()
