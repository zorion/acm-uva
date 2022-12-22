sample_in1 = {
    "1,9,10,3,2,3,11,0,99,30,40,50": 3500,
    "1,0,0,0,99": 2,
    "2,3,0,3,99": 2,
    "2,4,4,5,99,0": 2,
    "1,1,1,4,99,5,6,0,99": 30,
}


def get_input(s):
    return [int(i) for i in s.strip().split(',')]


def prob1(s):
    program = get_input(s)
    for i in range(0, len(program) + 1, 4):
        if program[i] == 99:
            break
        if program[i] == 1:
            op_add(program, i)
        elif program[i] == 2:
            op_mul(program, i)
        else:
            assert False, f'Failed at step {i}: {program}'
    result = program[0]
    # print(program)
    # print(f'Result: {result}')

    return result


def op_add(program, i):
    reg1 = program[i+1]
    reg2 = program[i+2]
    res = program[i+3]
    program[res] = program[reg1] + program[reg2]


def op_mul(program, i):
    reg1 = program[i+1]
    reg2 = program[i+2]
    res = program[i+3]
    program[res] = program[reg1] * program[reg2]


for sin, sout in sample_in1.items():
    test = prob1(sin)
    assert test == sout, f'prob1({sin})={repr(test)} (expected: {sout})'
print('Tests ok')
my_in = (
    '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,1,10,19,23,2,9,23,27,1,6,27,31,' +
    '1,10,31,35,1,35,10,39,1,9,39,43,1,6,43,47,1,10,47,51,1,6,51,55,2,13,55,' +
    '59,1,6,59,63,1,10,63,67,2,67,9,71,1,71,5,75,1,13,75,79,2,79,13,83,1,83,9,' +
    '87,2,10,87,91,2,91,6,95,2,13,95,99,1,10,99,103,2,9,103,107,1,107,5,111,2,' +
    '9,111,115,1,5,115,119,1,9,119,123,2,123,6,127,1,5,127,131,1,10,131,135,1,' +
    '135,6,139,1,139,5,143,1,143,9,147,1,5,147,151,1,151,13,155,1,5,155,159,1,' +
    '2,159,163,1,163,6,0,99,2,0,14,0')


def prob1_mod(s):
    my_in_mod = s[:2] + '12,2' + s[5:]
    return prob1(my_in_mod)


my_res = prob1_mod(my_in)
assert my_res > 1870666
print(f'Part1: {my_res}')


def prob2(s):
    for noun in range(100):
        for verb in range(100):
            my_in_mod = s[:2] + f'{noun},{verb}' + s[5:]
            aux = prob1(my_in_mod)
            if aux == 19690720:
                return 100 * noun + verb


print(f'Part2: {prob2(my_in)}')
