def get_program(s):
    return [int(i) for i in s.strip().split(',')]


def prob1(s):
    program = get_program(s)
    next_inst = 0
    while program[next_inst] != 99:
        # print(next_inst, program[next_inst])
        next_inst = run_instr(program, next_inst)
    return program[next_inst], next_inst


def fillzeroes(s, num_zeroes):
    return f'{int(s):0{num_zeroes}}'


def run_instr(program, next_inst, input_code=1):
    code = fillzeroes(program[next_inst], 5)
    opco = int(code[-2:])
    if opco in [1, 2, 7, 8]:
        apply_func3(program, next_inst)
        next_inst += 4
    elif opco in [3, 4]:
        apply_func1(program, next_inst, input_code)
        next_inst += 2
    elif opco in [5, 6]:
        next_inst = apply_func2(program, next_inst)
    else:
        assert False, f'Weird opco {opco} in {code}'
    return next_inst


def apply_func1(program, next_inst, input_code):
    code = fillzeroes(program[next_inst], 5)
    if code[2] == '0':
        reg = program[next_inst+1]
    else:
        assert code[2] == '1'
        assert code[-1] == '4', f'Opcode 3 can not get input into a immediate mode: {code}'
        reg = next_inst+1
    if code[-1] == '3':
        #print(f'Adding 1 to {reg}')
        program[reg] = input_code
    else:
        assert code[-1] == '4'
        print('output:', program[reg])
    return


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
        program[reg3] = reg1 + reg2
    elif code[-1] == '2':
        program[reg3] = reg1 * reg2
    elif code[-1] == '7':
        program[reg3] = 1 if reg1 < reg2 else 0
    elif code[-1] == '8':
        program[reg3] = 1 if reg1 == reg2 else 0
    else:
        assert False, code
    return


def prob2(s):
    program = get_program(s)
    next_inst = 0
    while program[next_inst] != 99:
        # print(next_inst, program[next_inst])
        next_inst = run_instr(program, next_inst, input_code=5)
    return program[next_inst], next_inst


my_in = (
    '3,225,1,225,6,6,1100,1,238,225,104,0,1101,78,5,225,1,166,139,224,101,' +
    '-74,224,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1002,136,' +
    '18,224,101,-918,224,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,' +
    '223,1001,83,84,224,1001,224,-139,224,4,224,102,8,223,223,101,3,224,224,' +
    '1,224,223,223,1102,55,20,225,1101,53,94,225,2,217,87,224,1001,224,-2120,' +
    '224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,102,37,14,224,101,' +
    '-185,224,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1101,8,' +
    '51,225,1102,46,15,225,1102,88,87,224,1001,224,-7656,224,4,224,102,8,223,' +
    '223,101,7,224,224,1,223,224,223,1101,29,28,225,1101,58,43,224,1001,224,' +
    '-101,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,1101,93,54,' +
    '225,101,40,191,224,1001,224,-133,224,4,224,102,8,223,223,101,3,224,224,' +
    '1,223,224,223,1101,40,79,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,' +
    '1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,' +
    '99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,' +
    '1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,' +
    '1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,' +
    '1105,1,99999,1008,226,677,224,1002,223,2,223,1005,224,329,1001,223,1,' +
    '223,1107,226,677,224,1002,223,2,223,1005,224,344,1001,223,1,223,8,677,' +
    '226,224,1002,223,2,223,1006,224,359,1001,223,1,223,1108,226,677,224,' +
    '1002,223,2,223,1006,224,374,101,1,223,223,1007,677,677,224,102,2,223,' +
    '223,1006,224,389,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,' +
    '404,101,1,223,223,1007,226,226,224,1002,223,2,223,1006,224,419,101,1,' +
    '223,223,107,677,226,224,1002,223,2,223,1006,224,434,1001,223,1,223,1007,' +
    '226,677,224,102,2,223,223,1005,224,449,101,1,223,223,1107,226,226,224,' +
    '1002,223,2,223,1005,224,464,1001,223,1,223,107,226,226,224,102,2,223,223,' +
    '1006,224,479,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,494,' +
    '101,1,223,223,107,677,677,224,102,2,223,223,1005,224,509,1001,223,1,223,' +
    '1008,677,677,224,1002,223,2,223,1006,224,524,101,1,223,223,1107,677,226,' +
    '224,102,2,223,223,1006,224,539,1001,223,1,223,108,677,226,224,102,2,223,' +
    '223,1006,224,554,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,' +
    '569,1001,223,1,223,8,677,677,224,1002,223,2,223,1005,224,584,1001,223,' +
    '1,223,7,677,677,224,1002,223,2,223,1005,224,599,101,1,223,223,1108,226,' +
    '226,224,102,2,223,223,1006,224,614,101,1,223,223,1008,226,226,224,1002,' +
    '223,2,223,1005,224,629,101,1,223,223,7,677,226,224,102,2,223,223,1006,' +
    '224,644,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,659,101,1,' +
    '223,223,108,677,677,224,1002,223,2,223,1006,224,674,101,1,223,223,4,223,' +
    '99,226')
res1 = prob1(my_in)
print(f'Part1: {res1}')
res2 = prob2(my_in)
print(f'Part2: {res2}')
