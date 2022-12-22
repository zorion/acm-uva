my_in = '138241-674034'


def get_input(s):
    return s.strip().split('-')


def prob1(s):
    my_min, my_max = get_input(s)
    result = 0
    for x in range(int(my_min), int(my_max) + 1):
        if is_ok(x):
            result += 1
    return result


def is_ok(x):
    s = str(x)
    pairs = False
    last_char = ''
    for char in s:
        if char == last_char:
            pairs = True
        if char < last_char:
            return False
        last_char = char
    return pairs


my_res = prob1(my_in)
print(f'Part 1: {my_res}')


def prob2(s):
    my_min, my_max = get_input(s)
    result = 0
    for x in range(int(my_min), int(my_max) + 1):
        if is_ok2(x):
            result += 1
    return result


def is_ok2(x):
    s = str(x)
    pairs = False
    last_char = ''
    last_pair = ''
    for char in s:
        if char < last_char:
            return False

        if char == last_char:
            last_pair += char
        else:
            if len(last_pair) == 1:
                pairs = True
            last_pair = ''

        last_char = char

    # Check the end of the string
    if len(last_pair) == 1:
        pairs = True

    return pairs


assert is_ok2(112233)
assert not is_ok2(123444)
assert is_ok2(111122)

my_res = prob2(my_in)
assert my_res > 735, my_res
assert my_res > 1059, my_res
print(f'Part 2: {my_res}')
