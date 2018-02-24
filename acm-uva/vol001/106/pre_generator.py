"""Get the results for problem 106.

Number of pitagoras-triples-with-relative-primes and 
the not used in general-pitagoras-triples.
"""
import math

try:
    from tqdm import tqdm
except:  # tqdm may be not installed
    tqdm = lambda x: x

DEBUG = False
N = 1000000
if DEBUG:
    N = 100


def get_triples(max_n):
    """Get both results for each N until max_n."""
    first_time_used_general = {}  # Key: number, value: first time used
    # Key: level  -  value: number of numbers first usded
    first_coprimes = {}
    first_generals = {}

    if not DEBUG:
        progress_func = tqdm
    else:
        progress_func = lambda x: x

    max_p = int(math.sqrt(max_n - 1)) + 1
    for __p in progress_func(range(1, max_p)):
        max_q = int(math.sqrt(max_n - __p * __p))
        # Also we will set q < p
        max_q = min(max_q, __p - 1) + 1
        for __q in range(1, max_q):
            if __q % 2 != __p % 2:
                divisor = math.gcd(__p, __q)
                if divisor == 1:
                    __x = 2 * __p * __q
                    __y = __p * __p - __q * __q
                    __z = __p * __p + __q * __q
                    first_coprimes[__z] = first_coprimes.get(__z, 0) + 1
                    __d = 1
                    while (__d * __z <= max_n):
                        # print("Adding", __d * __z, "^2 =", __d * __y, "^2 +", __x * __d, "^2")
                        # Check used numbers being or not coprimes
                        level = __d * __z
                        for value in [__x * __d, __y * __d, level]:
                            first_time_used_general[value] = min(
                                first_time_used_general.get(value, level), level)
                        __d += 1
    for ftu, level in first_time_used_general.items():
        if DEBUG:
            print(ftu, "unused at level", level)
        first_generals[level] = 1 + first_generals.get(level, 0)

    return first_coprimes, first_generals


def get_accum(fuc, lung, max_n):
    accum = 0
    decum = max_n
    for i in range(1 + max_n):
        accum += fuc.get(i, 0)
        decum -= lung.get(i, 0)
    return accum, decum


def main():
    first_used_coprimes, last_unused_general = get_triples(N)
    print("first_used_coprimes =", first_used_coprimes)
    print("last_unused_general =", last_unused_general)
    for r in [10, 25, N]:
        print(r, get_accum(first_used_coprimes, last_unused_general, r))


if __name__ == '__main__':
    main()
