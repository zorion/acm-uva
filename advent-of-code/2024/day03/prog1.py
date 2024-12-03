import re


def main():
    instructions = read_instructions()
    values = execute_instructions(instructions)
    print_results(values)


def execute_instructions(instructions: list[str]) -> list[int]:
    result = []
    for instruct in instructions:
        matches = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", instruct)
        for match in matches:
            match = match[4:-1]
            result.append(int(match.split(",")[0]) * int(match.split(",")[1]))
    return result


def print_results(values: list[int]) -> None:
    print("Result:", sum(values))


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
