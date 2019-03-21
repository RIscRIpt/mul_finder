import math
import itertools
import more_itertools

def factorize_into_digits(n):
    primes = [2, 3, 5, 7]
    factors = []
    target = n
    for prime in primes:
        while n % prime == 0:
            n //= prime
            factors.append(prime)
        if n == 1:
            break
    result = 1
    for factor in factors:
        result *= factor
    if result != target:
        return []
    return factors

def yield_numbers_from(factors):
    for fl in more_itertools.distinct_permutations(factors):
        yield int("".join(map(str, fl)))

def multiply_lists(to_multiply, factors, mul_list):
    result = to_multiply.copy()
    for i in range(len(factors)):
        result[mul_list[i]] *= factors[i]
    return result

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
        for r in range(math.ceil(n ** (1/7)), len(factors) + 1):
            if r == len(factors):
                yield from yield_numbers_from(factors)
            else:
                mul_comb_len = len(factors) - r
                yielded_factors = set()
                for mul_comb in set(itertools.combinations(factors, mul_comb_len)):
                    new_factors = factors.copy()
                    for value in mul_comb:
                        new_factors.remove(value)
                    for mul_list in itertools.product(range(len(new_factors)), repeat=len(mul_comb)):
                        multiplied_factors = multiply_lists(new_factors, mul_comb, mul_list)
                        fz_multiplied_factors = frozenset(multiplied_factors)
                        if fz_multiplied_factors not in yielded_factors:
                            yielded_factors.add(fz_multiplied_factors)
                            if max(multiplied_factors) < 10:
                                yield from yield_numbers_from(multiplied_factors)

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
