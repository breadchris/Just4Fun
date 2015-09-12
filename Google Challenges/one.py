def answer(y, x):
    test = set([(test_x - test_y) / float(test_x) for test_x, test_y in zip(sorted(x), sorted(y))])
    return int(test.pop() * 100)

assert answer([1.0], [1.0]) == 0
assert answer([2.2999999999999998, 15.0, 102.40000000000001, 3486.8000000000002], [23.0, 150.0, 1024.0, 34868.0]) == 90
assert answer([23, 11.1, 50.4], [22.2, 46, 100.8]) == 50
