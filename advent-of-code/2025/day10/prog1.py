import re

Line = str
Lines = list[Line]
Button = list[int]
Lights = list[bool]
Machine = tuple[Lights, list[Button], list[str]]
Problem = list[Machine]
Result = int

DEBUG = True


def solve(prob: Problem) -> Result:
    result = 0
    for machine in prob:
        result += get_min_solution(machine)
    return result


def get_min_solution(machine: Machine) -> Result:
    log_print(machine)
    lights, buttons, _ = machine
    state = [False] * len(lights)
    min_press = simulate(state, buttons, lights)

    return min_press


def simulate(
    state: Lights, buttons: list[Button], lights: Lights, *, acc: int = 0
) -> Result | None:
    if state == lights:
        return acc
    for button in buttons:
        state_press = press_button(state, button)
        res1 = simulate(state_press, buttons[1:], lights, acc=acc + 1)
        res2 = simulate(state, buttons[1:], lights, acc=acc)
        if res1 is None:
            return res2
        if res2 is None:
            return res1
        # both are numbers
        return min(res1, res2)
    return None


def press_button(state: Lights, button: Button) -> Lights:
    result = state.copy()
    for i in button:
        result[i] = not result[i]
    return result


def evaluate(result: Result) -> Result:
    return result


def parse_problem(data: Lines) -> Problem:
    result = []
    for line in data:
        machine = parse_line(line)
        result.append(machine)
    return result


TEMPLATE = (
    r"\[(?P<lights>[#\.]+)\] (?P<buttons>(?:\([0-9,]+\) )+)\{(?P<joltage>[0-9,]*)\}"
)


def parse_line(line: Line) -> Machine:
    m = re.match(
        TEMPLATE,
        line,
    )
    return (
        parse_lights(m["lights"]),
        parse_buttons(m["buttons"]),
        parse_joltage(m["joltage"]),
    )


def parse_lights(lights: str) -> Lights:
    return [light == "#" for light in lights]


def parse_buttons(buttons: str) -> list[Button]:
    button_list = buttons.split()
    result = []
    for button in button_list:
        result.append(parse_button(button))
    return result


def parse_button(button: str) -> Button:
    return list(map(int, button[1:-1].split(",")))


def parse_joltage(joltage: str) -> list[str]:
    return joltage.split(",")


def read_data() -> Lines:
    raw = read_subproblem()
    return raw


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


def run(data: Lines) -> Result:
    problem = parse_problem(data)
    solution = solve(problem)
    result = evaluate(solution)
    return result


def main():
    data = read_data()
    result = run(data)
    print("Result:", result)


def log_print(*args, **kwargs):
    if DEBUG:
        pprint(*args, **kwargs)


def pprint(*args, **kwargs):
    text = args[0]
    if isinstance(text, list) and isinstance(text[0], str):
        for line in text:
            print(line, *args[1:], **kwargs)
    else:
        print(*args, **kwargs)


if __name__ == "__main__":
    main()
