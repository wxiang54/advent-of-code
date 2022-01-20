import unittest

FUNC_TO_TEST = "count_increase_window"

#######################   Day 1.1: Sonar Sweep  #######################
def count_increase(depths):
    if len(depths) <= 1:
        return 0
    count = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i-1]:
            count += 1
    return count

def solve_count_increase(): # -> 1766
    path_in = "input1.txt"
    with open(path_in, 'r') as f:
        depths = f.read().split()
        depths = [int(depth) for depth in depths]
    return count_increase(depths)

@unittest.skipUnless(FUNC_TO_TEST == "count_increase", f"Testing: {FUNC_TO_TEST}()")
class SonarSweepTest1(unittest.TestCase):
    def test_count_increase(self):
        cases = [(199, 200, 208, 207, 207)]
        expecteds = [2]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = count_increase(case)
                self.assertEqual(expected, actual)

#######################   Day 1.2: Sonar Sweep  #######################
def count_increase_window(depths, window_size):
    if len(depths) <= window_size:
        return 0
    count = 0
    prev_window_sum = sum(depths[:window_size])
    for i in range(window_size, len(depths)):
        cur_window_sum = prev_window_sum - depths[i-window_size] + depths[i]
        if cur_window_sum > prev_window_sum:
            count += 1
        prev_window_sum = cur_window_sum
    return count

def solve_count_increase_window(): # -> 1797
    path_in = "input1.txt"
    with open(path_in, 'r') as f:
        depths = f.read().split()
        depths = [int(depth) for depth in depths]
    return count_increase_window(depths, 3)

@unittest.skipUnless(FUNC_TO_TEST == "count_increase_window", f"Testing: {FUNC_TO_TEST}()")
class SonarSweepTest2(unittest.TestCase):
    def test_count_increase_window(self):
        cases = [(199, 200, 208, 207, 207, 0)]
        expecteds = [2]
        window_size = 3
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = count_increase_window(case, window_size)
                self.assertEqual(expected, actual)

if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
