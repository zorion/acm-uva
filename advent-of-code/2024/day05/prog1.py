def main():
    rules = read_rules()
    pages = read_page_lists()
    ok_pages = find_ok_pages(rules, pages)
    print_results(ok_pages)


type TypeRules = list[tuple[int, int]]


def find_ok_pages(rules: TypeRules, list_pages: list[list[int]]) -> list[list[int]]:
    return [pages for pages in list_pages if check_page(pages, rules)]


def check_page(pages: list[int], rules: TypeRules) -> bool:
    for i, page_left in enumerate(pages):
        for j, page_right in enumerate(pages):
            if i >= j:
                continue
            for rule in rules:
                if rule == (page_right, page_left):
                    return False
    return True


def read_rules() -> TypeRules:
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
            res.append(tuple(map(int, line.split("|"))))
    return res


def read_page_lists() -> list[list[int]]:
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
            res.append(list(map(int, line.split(","))))
    return res


def print_results(ok_pages: list[list[int]]) -> None:
    middles = map(get_middle_page, ok_pages)
    print("Result:", sum(middles))


def get_middle_page(page: list[int]) -> int:
    return page[len(page) // 2]


if __name__ == "__main__":
    main()
