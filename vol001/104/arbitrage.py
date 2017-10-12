from collections import deque


def find_profit(tcs):
    # We'll need to find path using a Breath First Search (BFS)
    pending_chains = deque()  # tuple: path-so-far, factor-so-far
    for ctry in range(len(tcs)):
        pending_chains.append(([ctry], 1))

    while pending_chains:
        cur_path, cur_factor = pending_chains.popleft()
        if len(cur_path) > len(tcs):
            # We are unable to get money
            break
        from_currency = cur_path[-1]
        to_currency = cur_path[0]
        for via_cur in range(len(tcs)):
            # Try to add i to the path
            if via_cur in [from_currency, to_currency]:
                continue
            keep_factor = get_factor(tcs, from_currency, via_cur)
            check_factor = get_factor(tcs, via_cur, to_currency)

            new_factor = cur_factor * keep_factor
            new_path = cur_path + [via_cur]
            if new_factor * check_factor >= 1.01:
                return new_path + [to_currency]
            pending_chains.append((new_path, new_factor))

    return None


def get_factor(tcs, from_cur, to_cur):
    assert from_cur != to_cur
    if to_cur > from_cur:
        factor = tcs[from_cur][to_cur - 1]
    else:
        factor = tcs[from_cur][to_cur]
    return factor


def get_input():
    try:
        raw = input()
        if not raw:
            return None
    except EOFError:
        return None
    n = int(raw.split()[0])
    tcs = []  # Currency exchanges (tipos de cambio)
    for _ in range(n):
        raw_line = input().split()[:n]
        tcs.append(list(map(float, raw_line)))
    return tcs


def write_output(path):
    if not path:
        print("no arbitrage sequence exists")
    else:
        print(" ".join([str(country + 1) for country in path]))


def main():
    while True:
        tcs = get_input()
        if not tcs:
            break
        result = find_profit(tcs)
        write_output(result)


if __name__ == '__main__':
    main()