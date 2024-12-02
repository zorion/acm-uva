def main():
    reports = read_reports()
    safety = are_reports_safe(reports)
    print_results(safety)


def read_reports() -> list[list[int]]:
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
            res.append(list(map(int, line.split())))
    return res


def are_reports_safe(reports: list[list[int]]) -> list[bool]:
    return list(map(report_safe, reports))


def report_safe(report: list[int]) -> bool:
    incr = -1 if report[1] < report[0] else 1
    for i in range(1, len(report)):
        if report[i] - report[i - 1] not in [incr, 2 * incr, 3 * incr]:
            return False
    return True


def print_results(safety: list[bool]) -> None:
    print(len(list(filter(None, safety))))


if __name__ == "__main__":
    main()
