import collections
import functools
import itertools
import operator as op
from pprint import pprint
import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    return (input,)

def get_test_cases():
    num_cases = ${3:1}
    if num_cases == 1:
        cases = ["input${1}_test.txt"]
    else:
        tests_to_run = [1, 2]
        cases = ["input${1}_test%d.txt" % (test) for test in tests_to_run]
    return cases

def solve(f):
    input = parse_input("input${1}.txt")
    return f(input)

#######################   Day ${1:X}.1: ${2:Problem}  #######################
def part1(input):
    input, = input  # Unpack
    return

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [0]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day ${1:X}.2: ${2:Problem}  #######################
def part2(input):
    input, = input  # Unpack
    return

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [0]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part1

if __name__ == "__main__":
    unittest.main()
    # print(solve(FUNC_TO_TEST))
