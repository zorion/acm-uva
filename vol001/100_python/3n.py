
def alg(n):
    i = 1
    while n > 1:
        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1
        i += 1
    return i


def get_max_cycles(i, j):
    if j < i:
        i, j = j, i
    current_max = alg(j)
    idx = i
    while idx < j:
        cycles = alg(idx)
        if cycles > current_max:
            current_max = cycles
        idx += 1
    return current_max


def read_input():
    try:
        data_in = input("")
        return data_in
    except EOFError:
        return None


def data_out(i, j, max_cycles):
    print(i, j, max_cycles)

def main():
    while True:
        data_in = read_input()
        if not data_in:
            break
        i, j = map(int, data_in.split(" "))
        max_cycles = get_max_cycles(i, j)
        data_out(i, j, max_cycles)


if __name__ == '__main__':
    main()
