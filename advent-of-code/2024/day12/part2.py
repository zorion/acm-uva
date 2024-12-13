from __future__ import annotations

type Garden = list[list[str]]
type Position = tuple[int, int]
type Visited = set[Position]
type Region = set[Position]


def main():
    garden = read_garden()
    price = get_price(garden)
    print_result(price)


def get_price(garden: Garden) -> int:
    visited: Visited = set()
    price: int = 0
    for y, line in enumerate(garden):
        for x, _ in enumerate(line):
            region = explore(x, y, garden, visited)
            area, perimeter = calc_region(region)
            price += area * perimeter
    return price


def explore(x: int, y: int, garden: Garden, visited: Visited) -> Region:
    if (x, y) in visited:
        return set()
    visited.add((x, y))
    region = set()
    region.add((x, y))
    value = garden[y][x]
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if not valid(x + dx, y + dy, garden):
            continue
        new_val = garden[y + dy][x + dx]
        if new_val == value:
            new_region = explore(x + dx, y + dy, garden, visited)
            region.update(new_region)

    return region


def calc_region(region: Region) -> tuple[int, int]:
    area = len(region)
    perimeter = 0
    for x, y in region:
        has_up = (x, y - 1) in region
        has_down = (x, y + 1) in region
        has_left = (x - 1, y) in region
        has_right = (x + 1, y) in region
        does_up_have_left = (x - 1, y - 1) in region
        does_up_have_right = (x + 1, y - 1) in region
        does_left_have_up = (x - 1, y - 1) in region
        does_left_have_down = (x - 1, y + 1) in region
        # left side: border new (comparing to up neighbour)
        if not has_left and (not has_up or does_up_have_left):
            perimeter += 1
        # right side: border new (comparing to up neighbour)
        if not has_right and (not has_up or does_up_have_right):
            perimeter += 1
        # up side: border new (comparing to left neighbour)
        if not has_up and (not has_left or does_left_have_up):
            perimeter += 1
        # down side: bodrer new (comparing to left neighbour)
        if not has_down and (not has_left or does_left_have_down):
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
