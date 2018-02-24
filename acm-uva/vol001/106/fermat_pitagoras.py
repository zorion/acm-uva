# 1) a^2 + b^2 = c^2  => (k*a)^2 + (k*b)^2 = (k*c)^2
# 2) if coprime(a,b) => coprime(a, a*a + b*b) and coprime(b, a*a + b*b)
# 3) if not(coprime(a,b)) (i.e.) there exists k,a',b' with a=k*a' and b=k*b' and coprime(a',b')
#    Then c*c = k*k(a'*a' + b'*b') so c' = a'*a' + b'*b' 
# 4) a^2 - b^2 = a^2 + b^2 - 2*a*b  => a*a+b*b = a*a - b*b + 2*a*b

import math
import time
N = 1000 * 1000


def calculate(max_n):
    """Get the results for max_n."""
    used_numbers = [False] * (max_n + 1)
    coprimes_counter = 0
    # Since Z will be p^2 + something, p^2 shouldn't be above max_n:
    max_p = int(math.sqrt(max_n - 1)) + 1
    for __p in range(2, max_p):
        # Again, Z will be p^2 + q^2, so q^2 shouldn't be above max_n - p^2
        max_q = int(math.sqrt(max_n - __p * __p))
        # Also we will set q < p
        max_q = min(max_q, __p - 1) + 1
        for __q in range(1, max_q):
            if __q % 2 != __p % 2:
                divisor = math.gcd(__p, __q)
                if divisor == 1:
                    # We have a new pair of coprimes.
                    coprimes_counter += 1
                    __z = __p * __p + __q * __q
                    __y = __p * __p - __q * __q
                    __x = 2 * __p * __q
                    __d = 1
                    while (__d * __z <= max_n):
                        # print("Adding", __d * __z, "^2 =", __d * __y, "^2 +", __x * __d, "^2")
                        # Check used numbers being or not coprimes
                        used_numbers[__y * __d] = True
                        used_numbers[__z * __d] = True
                        used_numbers[__x * __d] = True
                        __d += 1
    unused_counter = 0
    for i in range(1, max_n +1):
        if not used_numbers[i]:
            unused_counter += 1
    return (coprimes_counter, unused_counter)


def main():
    while True:
        try:
            data = input()
        except EOFError:
            data = None
        if not data:
            break
        c_used, g_unused = calculate(int(data.split()[0]))
        print(c_used, g_unused)

if __name__ == '__main__':
    main()
