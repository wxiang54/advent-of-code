import unittest
from functools import reduce
import math

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    x_range = None
    y_range = None
    for part in input:
        if part[0] == "x":
            x_range = part.strip(",x=")
        if part[0] == "y":
            y_range = part.strip("y=")
    x_min, x_max = x_range.split("..")
    y_min, y_max = y_range.split("..")
    return ((int(x_min), int(x_max)), (int(y_min), int(y_max)))

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input17_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input17_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input17.txt")
    return f(*input)

#######################   Day 17.1: Trick Shot  #######################
def step(x, y, vx, vy):
    x += vx
    y += vy
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    vy -= 1
    return x, y, vx, vy

def part1(x_range, y_range):
    global_max_y = 0
    max_vx = 0
    max_vy = 0
    for vx in range(1, 500):
        for vy in range(-200, 500):
            cvx = vx
            cvy = vy
            x = 0
            y = 0
            max_y = 0
            while y >= y_range[0] and x <= x_range[1]:
                x, y, cvx, cvy = step(x, y, cvx, cvy)
                if y > max_y:
                    max_y = y
                if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                    if max_y > global_max_y:
                        global_max_y = max_y
                        max_vx = vx
                        max_vy = vy
                        # print(f"updated global max: {max_y}")
    # print(max_vx, max_vy)
    # print(global_max_y)
    return ret

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [45]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 17.2: Trick Shot  #######################
def part2(x_range, y_range):
    ret = 0
    for vx in range(1, 500):
        for vy in range(-200, 500):
            cvx = vx
            cvy = vy
            x = 0
            y = 0
            while y >= y_range[0] and x <= x_range[1]:
                x, y, cvx, cvy = step(x, y, cvx, cvy)
                if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                    ret += 1
                    break
    return ret

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [112]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part1

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
