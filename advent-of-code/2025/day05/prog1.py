Range = tuple[int, int]
Ranges = list[Range]
Ingredients = list[int]
Problem = tuple[Ranges, Ingredients]
Lines = list[str]
Result = int

DEBUG = True


def read_data() -> Problem:
    ranges = to_ranges(read_subproblem())
    ings = to_ingredients(read_subproblem())
    return ranges, ings


def to_ranges(lines: Lines) -> Ranges:
    ranges = [to_range(line) for line in lines]
    return ranges


def to_range(line: str) -> Range:
    return tuple(map(int, line.split("-")))


def to_ingredients(lines: Lines) -> Ingredients:
    return [int(line) for line in lines]


def read_subproblem() -> Lines:
    finished = False
    res = []
    while not finished:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            finished = True
        else:
            res.append(line)
    return res


def run(data: Problem) -> Result:
    res = 0
    ranges, ingredients = data
    for ingredient in ingredients:
        for a, b in ranges:
            if a <= ingredient <= b:
                res += 1
                break
    return res


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


def log_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


if __name__ == "__main__":
    main()
