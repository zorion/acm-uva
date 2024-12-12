from __future__ import annotations

from functools import lru_cache


def main():
    stones = read_list_of_stones()
    for i in range(76):
        res = blink(stones, i)
    print_results(res)


def blink(stones: list[int], steps: int) -> list[int]:
    result = []
    for stone in stones:
        result.append(blink_stone(stone, steps))

    return result


@lru_cache(maxsize=None)
def blink_stone(stone: int, steps: int) -> int:
    if steps == 0:
        return 1
    if stone == 0:
        return blink_stone(1, steps - 1)
    sz_stone = str(stone)
    if len(sz_stone) % 2 == 0:
        new_stone1 = int(sz_stone[: len(sz_stone) // 2])
        new_stone2 = int(sz_stone[len(sz_stone) // 2 :])
        return blink_stone(new_stone1, steps - 1) + blink_stone(new_stone2, steps - 1)
    return blink_stone(stone * 2024, steps - 1)


assert (res := sum(blink([0, 1, 10, 99, 999], 1))) == len(
    [1, 2024, 1, 0, 9, 9, 2021976]
), res


def read_list_of_stones() -> list[int]:
    result = []
    while True:
        try:
            line = input()
        except Exception:
            break
        result += list(map(int, line.split()))
    return result


def print_results(result: list[int]) -> None:
    print("Result:", sum(result))


if __name__ == "__main__":
    main()
