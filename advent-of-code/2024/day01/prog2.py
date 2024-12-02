def find_differences(list1: list[int], list2: list[int]) -> list[int]:
    results = []
    for i in list1:
        freq = len([y for y in list2 if y == i])
        results.append(freq * i)
    return results


def print_results(difs: list[int]) -> None:
    print(sum(difs))


def read_lists() -> tuple[list[int], list[int]]:
    finished = False
    res1 = []
    res2 = []
    while not finished:
        try:
            line = input()
        except Exception:
            break
        if line == "":
            finished = True
        else:
            data1, data2 = list(map(int, line.split()))
            res1.append(data1)
            res2.append(data2)
    return res1, res2


def main() -> None:
    list1, list2 = read_lists()
    difs = find_differences(list1, list2)
    print_results(difs)


if __name__ == "__main__":
    main()
