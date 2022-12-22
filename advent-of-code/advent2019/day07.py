def get_program(s):
    return [int(i) for i in s.strip().split(',')]


def fillzeroes(s, num_zeroes):
    return f'{int(s):0{num_zeroes}}'


def run_instr(program, next_inst, input_code, out):
    code = fillzeroes(program[next_inst], 5)
    opco = int(code[-2:])
    if opco in [1, 2, 7, 8]:
        apply_func3(program, next_inst)
        next_inst += 4
    elif opco in [3, 4]:
        if not apply_func1(program, next_inst, input_code, out):
            return [next_inst]
        next_inst += 2
    elif opco in [5, 6]:
        next_inst = apply_func2(program, next_inst)
    else:
        assert False, f'Weird opco {opco} in {code}'
    return next_inst


def apply_func1(program, next_inst, input_code, out):
    code = fillzeroes(program[next_inst], 5)
    if code[2] == '0':
        reg = program[next_inst+1]
    else:
        assert code[2] == '1'
        assert code[-1] == '4', f'Opcode 3 can not get input into a immediate mode: {code}'
        reg = next_inst+1
    if code[-1] == '3':
        #print(f'Adding 1 to {reg}')
        if len(input_code) == 0:
            return False
        program[reg] = input_code.pop()
    else:
        assert code[-1] == '4'
        print(reg, 'output:', program[reg])
        out['result'] = program[reg]
    return True


def apply_func2(program, next_inst):
    code = fillzeroes(program[next_inst], 5)
    sreg1 = program[next_inst+1]
    sreg2 = program[next_inst+2]
    if code[2] == '0':
        reg1 = program[sreg1]
    else:
        assert code[2] == '1'
        reg1 = sreg1
    if code[1] == '0':
        reg2 = program[sreg2]
    else:
        assert code[1] == '1'
        reg2 = sreg2
    if code[-1] == '5':
        return reg2 if reg1 != 0 else next_inst + 3
    else:
        assert code[-1] == '6'
        return reg2 if reg1 == 0 else next_inst + 3


def apply_func3(program, next_inst):
    code = fillzeroes(program[next_inst], 5)
    sreg1 = program[next_inst+1]
    sreg2 = program[next_inst+2]
    if code[2] == '0':
        reg1 = program[sreg1]
    else:
        assert code[2] == '1'
        reg1 = sreg1
    if code[1] == '0':
        reg2 = program[sreg2]
    else:
        assert code[1] == '1'
        reg2 = sreg2
    assert code[0] == '0'
    reg3 = program[next_inst+3]
    if code[-1] == '1':
        #print(code, 'sum', reg1, sreg1, '+', reg2, sreg2, 'into', reg3)
        try:
            program[reg3] = reg1 + reg2
        except TypeError:
            print('TYpe Error in sum: ')
            print(program)
            print(f'{reg1} + {reg2} -> {reg3}')
            print(f'{program[reg1]} + {program[reg2]} -> {program[reg3]}')
            raise
    elif code[-1] == '2':
        program[reg3] = reg1 * reg2
    elif code[-1] == '7':
        program[reg3] = 1 if reg1 < reg2 else 0
    elif code[-1] == '8':
        program[reg3] = 1 if reg1 == reg2 else 0
    else:
        assert False, code
    return


def simulate(program, inputs):
    last_out = 0
    for i in range(5):
        last_out = simulate_program(program, [last_out, inputs[i]])
        print(f'Iteration {i}: {last_out}')
    return last_out


def simulate_partial(program, inputs):
    last_out = [0]
    programs = []
    for i in range(5):
        last_out = simulate_program(program, [last_out[0], inputs[i]])
        print(f'partial iteration {i}: {last_out}')
        if isinstance(last_out, int):
            last_out = [last_out, 25]
        programs.append((program, last_out[1]))
    return last_out[0], programs


def simulate_program(program, input_codes, next_inst=0):
    out = {'result': None}
    while isinstance(next_inst, int) and program[next_inst] != 99:
        next_inst = run_instr(program, next_inst, input_codes, out)
    print(out, next_inst)
    if isinstance(next_inst, int):
        return out['result']
    else:
        assert isinstance(next_inst, list)
        return out['result'], next_inst[0]


def shuffle(a_tuple):
    if not a_tuple:
        yield tuple()
    for i in a_tuple:
        for t in shuffle([_i for _i in a_tuple if _i != i]):
            yield (i, ) + tuple(t)


assert list(shuffle([])) == [tuple()], list(shuffle([]))
assert list(shuffle([0])) == [(0, )], list(shuffle((0, )))
assert list(shuffle((0, 1))) == [(0, 1), (1, 0)], list(shuffle((0, 1)))


def prob1(s):
    tests = tuple(range(5))
    max_wow = None
    for in_list in shuffle(tests):
        print(f'------- Try {in_list} ---------')
        wow = simulate(get_program(s), in_list)
        if max_wow is None or max_wow < wow:
            max_wow = wow
    return max_wow


def prob2(s):
    tests = tuple(range(5, 10))
    max_wow = None
    next_inst = 0
    for in_list in shuffle(tests):
        print(f'======== Try {in_list} ===========')
        inp, progs = simulate_partial(get_program(s), in_list)
        while progs:
            prog, start_instr = progs.pop(0)
            inp = simulate_program(prog, [inp], next_inst=start_instr)
            print('nextprog, out:', inp)
            if isinstance(inp, int):
                break
            else:
                progs.append((prog, inp[1]))
                inp = inp[0]
            
        if inp > max_wow:
            max_wow = inp
    return max_wow


samples = [
    ['3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', 43210, [4, 3, 2, 1, 0]],
    ['3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0',
     54321, [0, 1, 2, 3, 4]],
    ['3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0',
     65210, [1, 0, 4, 3, 2]],
]
for s in samples:
    t = simulate(get_program(s[0]), s[2])
    assert t == s[1], f'Got {t}. Expected {s[1]}: {s}'
    t = prob1(s[0])
    assert t == s[1], f'FAILED: {t} instead of {s[1]}'
print('OK')

my_in = '3,8,1001,8,10,8,105,1,0,0,21,42,67,88,101,114,195,276,357,438,99999,3,9,101,3,9,9,1002,9,4,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,2,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,102,4,9,9,1001,9,3,9,102,4,9,9,101,4,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99'
res1 = prob1(my_in)
print(f'Part1: {res1}')
assert res1 == 99376


samples2 = [
    ['3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,' +
     '27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', 139629729],
    ['3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,' +
     '1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,' +
     '54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,' +
     '1005,56,6,99,0,0,0,0,10', 18216],
]
for s in samples2:
    t = prob2(s[0])
    assert t == s[1], f'FAILED: {t} instead of {s[1]}'
print('OK')


res2 = prob2(my_in)
print(f'Part2: {res2}')
