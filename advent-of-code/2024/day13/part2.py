from __future__ import annotations

import re

EXTRA_PRIZE = 10000000000000

type Position = tuple[int, int]
type Button = Position
type Prize = Position
type ClawMachine = tuple[Button, Button, Prize]


def main():
    claw_list = read_claw_list()
    result = solve_puzzle(claw_list)
    print_results(result)


def solve_puzzle(claw_list: list[ClawMachine]) -> int:
    result = 0
    for machine in claw_list:
        res = solve_claw_machine(machine)
        result += res
    return result


def solve_claw_machine(machine: ClawMachine) -> int:
    # Not diophantine solution: HARD
    button_a, button_b, prize = machine
    for i in range(101):
        for j in range(101):
            if add_pos(move_times(button_a, i), move_times(button_b, j)) == prize:
                return 3 * i + j
    return 0


def add_pos(a: Position, b: Position) -> Position:
    return (a[0] + b[0], a[1] + b[1])


def move_times(a: Position, n: int) -> Position:
    return (a[0] * n, a[1] * n)


def read_claw_list() -> list[ClawMachine]:
    result = []
    button_a = None
    button_b = None
    prize = None
    while True:
        try:
            line = input()
        except Exception:
            if button_a is not None:
                _append_claw(result, button_a, button_b, prize)
            break
        if m := re.match(r"Button A: X\+([0-9]+), Y\+([0-9]+)", line):
            button_a = (int(m.group(1)), int(m.group(2)))
        elif m := re.match(r"Button B: X\+([0-9]+), Y\+([0-9]+)", line):
            button_b = (int(m.group(1)), int(m.group(2)))
        elif m := re.match(r"Prize: X=([0-9]+), Y=([0-9]+)", line):
            prize = (int(m.group(1)), int(m.group(2)))
        else:  # White line
            _append_claw(result, button_a, button_b, prize)
            button_a = None
            button_b = None
            prize = None

    return result


def _append_claw(
    claw_list: list[ClawMachine],
    button_a: Position,
    button_b: Position,
    prize: Position,
) -> None:
    assert button_a is not None, "Assert not partial"
    assert button_b is not None, "Assert not partial"
    assert prize is not None, "Assert not partial"
    claw_list.append((button_a, button_b, add_pos(prize, (EXTRA_PRIZE, EXTRA_PRIZE))))


def print_results(result: int) -> None:
    print("Result:", result)


if __name__ == "__main__":
    main()
