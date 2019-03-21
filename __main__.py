import itertools
import more_itertools

def factorize_into_digits(n):
    primes = [2, 3, 5, 7]
    factors = []
    for prime in primes:
        while n % prime == 0:
            n //= prime
            factors.append(prime)
        if n == 0:
            raise ValueError("n == 0")
        elif n == 1:
            break
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
    return (len(steps), steps)

def find_mul_with_result(n):
    if n < 10:
        yield 10 + n
        if n > 1:
            yield n * 10 + 1
        # Could yield more 1's, but I decided to stop.
    else:
        n_len = len(str(n))
        factors = factorize_into_digits(n)
        if len(factors) == 0:
            return
        for r in range(n_len, len(factors) + 1):
            if r == len(factors):
                yield from yield_numbers_from(factors)
            else:
                combination_len = len(factors) - r
                yielded_factors = set()
                for combination in itertools.combinations(set(factors), combination_len):
                    new_factors = factors.copy()
                    for value in combination:
                        new_factors.remove(value)
                    for mul_list in itertools.permutations(range(len(new_factors)), combination_len):
                        multiplied_factors = multiply_lists(new_factors, combination, mul_list)
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
        if result[0] > 5:
            print(mul, result)
        if result[0] > 10:
            input()
        do(mul)

for i in range(0, 10):
    do(i)

# 1: 0, 1, 2, 3, 4
# 2: (0, 0), (0, 1), (0, 2) .., (3, 4), (4, 1) .. (4, 3), (4, 4)





## Second attempt
# 1 [1, 1]
# 11 [1, 11]

# 2 [1, 2] / [2, 1]
# 12 [2, 2, 3] / [2, 6] / [6, 2] / [4, 3]
# 322

# [2, 3, 4, 5]



## First attempt
#4 : [2, 2]
#22 : [2, 11]

#7 : [1, 7]
#17 : [1, 17]

#0 : [X, 0]
#10 : [2, 5]
#25 : [5, 5]
#55 : [5, 11]
