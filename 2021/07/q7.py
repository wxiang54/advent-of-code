import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split(",")
    input = [int(i) for i in input]
    return (input,)

#######################   Day 7.1: Treachery of Whales  #######################
def find_median(input):
    input_sorted = sorted(input)
    return input_sorted[len(input) // 2]    # Favors right elem in case of tie.

def find_deviances(input, center):
    return sum(abs(val - center) for val in input)

def part1(input):
    median = find_median(input)
    deviances = find_deviances(input, median)
    return deviances

def solve_part1(): # -> ?
    input = parse_input("input7.txt")
    return part1(*input)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part1":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part1(self):
        cases = ["input7_test.txt"]
        expecteds = [37]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 7.2: Treachery of Whales  #######################
def arith_sum(n):
    return round(n * (n+1) / 2)

def find_deviances_quadratic(input, center):
    return sum(arith_sum(abs(val - center)) for val in input)

def part2(input):
    mean = sum(input) / len(input)
    # mean = round(mean)
    min_ = min(input)
    max_ = max(input)
    min_deviances = float('inf')
    center = None
    for i in range(min_, max_):
        deviances = find_deviances_quadratic(input, i)
        if deviances < min_deviances:
            min_deviances = deviances
            center = i
    print(center, min_deviances, mean, round(mean))
    return min_deviances

def solve_part2(): # -> ?
    input = parse_input("input7.txt")
    return part2(*input)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part2":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = ["input7_test.txt"]
        expecteds = [168]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)


FUNC_TO_TEST = "part2"

if __name__ == "__main__":
    unittest.main()
    # print(eval(f"solve_{FUNC_TO_TEST}")())
