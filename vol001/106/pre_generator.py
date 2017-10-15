"""Get the results for problem 106.

Number of pitagoras-triples-with-relative-primes and 
the not used in general-pitagoras-triples.
"""
import functools
import math

try:
    from tqdm import tqdm
except:  # tqdm may be not installed
    tqdm = lambda x: x

DEBUG = False
N = 1000000
if DEBUG:
    N = 100


@functools.lru_cache(None)
def is_square(a_num):
    candidate = int(math.sqrt(a_num))
    if candidate * candidate == a_num:
        return candidate
    return None

def are_relative_primes(a, b, c):
    if not (a <= b <= c):  # Normalize
        l = [a, b, c]
        l.sort()
        assert l[0] <= l[1] <= l[2], "Waat {}".format(l)
        return are_relative_primes(*l)
    return _relative(a, b) and _relative(a, c) and _relative(b, c)

def _relative(a, b):
    return math.gcd(a, b) == 1

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

    for i in progress_func(range(1, max_n + 1)):
        for j in range(1, i + 1):
            kk = i * i + j * j
            if kk > max_n * max_n:
                break
            if is_square(kk):
                k = is_square(kk)
                assert k <= max_n, ("foo", k, max_n)
                level = k
                if DEBUG:
                    print(i, "^2  + ", j, "^2  = ", k, "^2", is_square(kk), "->", level)
                for aux in [i, j, k]:
                    first_time_used_general[aux] = min(
                        first_time_used_general.get(aux, max_n + 1),
                        level)
                if are_relative_primes(i, j, k):
                    first_coprimes[level] = 1 + first_coprimes.get(level, 0)
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
