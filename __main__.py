import math
import itertools
import more_itertools

def factorize_into_digits(n):
    digits = list(range(9, 1, -1))
    factors = []
    target = n
    for digit in digits:
        while n % digit == 0:
            n //= digit
            factors.append(digit)
        if n == 1:
            break
    result = 1
    for factor in factors:
        result *= factor
    if result != target:
        return []
    return factors

def factors_of_factors(factors):
    primes = [2, 3]
    yield tuple(factors)
    for i in range(len(factors)):
        for prime in primes:
            if factors[i] > 3 and factors[i] % prime == 0:
                new_factors = factors.copy()
                factor = factors[i]
                new_factors.remove(factor)
                new_factors.append(factor // prime)
                new_factors.append(prime)
                new_factors.sort()
                yield from factors_of_factors(new_factors)

def yield_numbers_from(factors):
    for fl in more_itertools.distinct_permutations(factors):
        yield int("".join(map(str, fl)))

def mul_result(n):
    steps = [n]
    while n > 10:
        next_n = 1
        for digit in [int(x) for x in str(n)]:
            next_n *= digit
        n = next_n
        steps.append(n)
    return (len(steps) - 1, steps)

def find_mul_with_result(n):
    if n < 10:
        p = 10
        while True:
            yield p + n
            if n > 1:
                yield n * p + 1
            p *= 10
    else:
        factors = factorize_into_digits(n)
        if len(factors) == 0:
            return
        for fs in set(factors_of_factors(factors)):
            yield from yield_numbers_from(fs)

checked = set()

def do(n):
    if n in checked:
        return
    checked.add(n)
    for mul in find_mul_with_result(n):
        result = mul_result(mul)
        print(result)
        if result[0] > 11:
            input()
        do(mul)

if __name__ == "__main__":
    for i in itertools.count():
        i += 10
        do(i)
