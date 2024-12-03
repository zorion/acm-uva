import re


def main():
    instructions = read_instructions()
    values = execute_instructions(instructions)
    print_results(values)


def execute_instructions(instructions: list[str]) -> list[int]:
    result = 0
    use = True
    instruct = "".join(instructions)
    matches = re.findall(r"(mul\([0-9]{1,3},[0-9]{1,3}\))|(don't)|(do)", instruct)
    for mul, dont, do in matches:
        if dont == "don't":
            use = False
            continue
        elif do == "do":
            use = True
            continue
        if use:
            prod = mul[4:-1]
            a, b = map(int, prod.split(","))
            result += a * b
    return result


def print_results(values: list[int]) -> None:
    print("Result:", values)


def read_instructions() -> list[str]:
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


if __name__ == "__main__":
    main()
