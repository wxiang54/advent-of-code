import unittest
from collections import deque

FUNC_TO_TEST = "part2"

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip()
    # Leave as strings for now.
    timers = input.split(",")
    return (timers,)

#######################   Day 6.1: Lanternfish  #######################
def simulate_day(queue):
    births = queue.popleft();   # num of lanternfish with zero timer.
    queue.append(births)        # newly birthed lanternfish at 8
    queue[6] += births      # TODO: make this not O(n), e.g. using DLL

def get_counts(timers):
    counts = [0] * 9    # Timers can only take values from 0-8
    for timer in timers:
        counts[int(timer)] += 1
    queue = deque(counts)
    return queue

def part1(input):
    num_days = 80
    queue = get_counts(input)
    for i in range(num_days):
        simulate_day(queue)
    return sum(queue)

def solve_part1(): # -> ?
    input = parse_input("input6.txt")
    return part1(*input)

@unittest.skipUnless(FUNC_TO_TEST == "part1", f"Testing: {FUNC_TO_TEST}()")
class Part1Test(unittest.TestCase):
    def test_part1(self):
        cases = ["input6_test.txt"]
        expecteds = [5934]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 6.2: Lanternfish  #######################
def part2(input):
    num_days = 256
    queue = get_counts(input)
    for i in range(num_days):
        simulate_day(queue)
    return sum(queue)

def solve_part2(): # -> ?
    input = parse_input("input6.txt")
    return part2(*input)

@unittest.skipUnless(FUNC_TO_TEST == "part2", f"Testing: {FUNC_TO_TEST}()")
class Part2Test(unittest.TestCase):
    def test_part2(self):
        cases = ["input6_test.txt"]
        expecteds = [26984457539]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
