def answer(x):
    elem_sum = sum(x)
    return len(x) - 1 if elem_sum % len(x) != 0 else len(x)

def test():
    from random import randrange, randint
    x = [randint(0, 1) for _ in range(0, randint(2, 100))]

assert answer([1, 4, 1]) == 3
assert answer([1, 2]) == 1

test()
