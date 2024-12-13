from __future__ import annotations

type Garden = list[list[str]]
type Position = tuple[int, int]
type Visited = set[Position]


def main():
    garden = read_garden()
    price = get_price(garden)
    print_result(price)


def get_price(garden: Garden) -> int:
    visited: Visited = set()
    price: int = 0
    for y, line in enumerate(garden):
        for x, _ in enumerate(line):
            area, perimeter = explore(x, y, garden, visited)
            price += area * perimeter
    return price


def explore(x: int, y: int, garden: Garden, visited: Visited) -> tuple[int, int]:
    if (x, y) in visited:
        return 0, 0
    visited.add((x, y))
    area = 1  # self, not yet counted
    perimeter = 0
    value = garden[y][x]
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if not valid(x + dx, y + dy, garden):
            perimeter += 1
            continue
        new_val = garden[y + dy][x + dx]
        if new_val == value:
            new_area, new_perimeter = explore(x + dx, y + dy, garden, visited)
            area += new_area
            perimeter += new_perimeter
        else:
            perimeter += 1
    return area, perimeter


def valid(x: int, y: int, garden: Garden) -> bool:
    return 0 <= x < len(garden[0]) and 0 <= y < len(garden)


def read_garden() -> Garden:
    result = []
    while True:
        try:
            line = input()
        except Exception:
            break
        result.append(list(line))
    return result


def print_result(price: int) -> None:
    print("Result:", price)


if __name__ == "__main__":
    main()
