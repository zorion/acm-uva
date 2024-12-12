from __future__ import annotations


def main():
    stones = read_list_of_stones()
    for _ in range(25):
        stones = blink(stones)
    print_results(stones)


def blink(stones: list[int]) -> list[int]:
    result = []
    for stone in stones:
        if stone == 0:
            result.append(1)
            continue
        sz_stone = str(stone)
        if len(sz_stone) % 2 == 0:
            result.append(int(sz_stone[: len(sz_stone) // 2]))
            result.append(int(sz_stone[len(sz_stone) // 2 :]))
            continue
        result.append(stone * 2024)

    return result


assert (res := blink([0, 1, 10, 99, 999])) == [1, 2024, 1, 0, 9, 9, 2021976], res


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
    print("Result:", len(result))


if __name__ == "__main__":
    main()
