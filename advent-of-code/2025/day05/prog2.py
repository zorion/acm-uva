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


def join_ranges(ranges: Ranges) -> Ranges:
    result = [ranges[0]]
    for r in ranges[1:]:
        log_print(result)
        log_print("add", r)
        result = sort_join_new_range(result, r)
    return result


def sort_join_new_range(ranges: Ranges, rg: Range) -> Ranges:
    a, b = rg
    result = []
    for i, r in enumerate(ranges):
        if r[1] < a - 1:
            # New range is bigger
            result.append(r)
        elif r[0] > b + 1:
            # New range is smaller, add before
            result.append((a, b))
            result.append(r)
            result += ranges[i + 1 :]
            break
        else:
            # There is an "almost" intersection, treat both ranges as one
            a, b = union_ranges(r, (a, b))
    else:
        # We went all ranges without breaking, so new_range is bigger
        result.append((a, b))
    return result


def union_ranges(r1: Range, r2: Range) -> Range:
    a = min(r1[0], r2[0])
    b = max(r1[1], r2[1])
    log_print("union", r1, r2, a, b)
    return a, b


def count_values(ranges: Ranges) -> int:
    log_print(ranges)
    return sum(r[1] - r[0] + 1 for r in ranges)


def run(data: Problem) -> Result:
    res = 0
    ranges, _ = data
    new_ranges = join_ranges(ranges)
    res = count_values(new_ranges)
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
