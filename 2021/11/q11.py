import unittest
import itertools
from pprint import pprint

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    input = [[int(i) for i in line] for line in input]
    return (input,)

def in_range(bounds):
    return lambda ind: bounds[0] <= ind < bounds[1]

def get_adjacents(matrix, row, col):
    if matrix is None or len(matrix) == 0 or len(matrix[0]) == 0:
        raise StopIteration
    row_bounds = (0, len(matrix))
    col_bounds = (0, len(matrix[0]))
    adj_rows = filter(in_range(row_bounds), (row-1, row, row+1))
    # Must convert adj_cols to list/tuple to prevent it from being exhausted as iterator.
    adj_cols = tuple(filter(in_range(col_bounds), (col-1, col, col+1)))
    for adj_row in adj_rows:
        for adj_col in adj_cols:
            if adj_row == row and adj_col == col:
                continue
            yield (adj_row, adj_col)

#######################   Day 11.1: Dumbo Octopus  #######################
def increment(input, row, col):
    input[row][col] = (input[row][col] + 1) % 10

def increment_all(input):
    for row in range(len(input)):
        for col in range(len(input[row])):
            increment(input, row, col)

def spread_flash(input, row, col):
    num_flashes = 1 # Including current row/col.
    for arow, acol in get_adjacents(input, row, col):
        if input[arow][acol] == 0:
            continue    # Already flashed.
        increment(input, arow, acol)
        if input[arow][acol] == 0:
            num_flashes += spread_flash(input, arow, acol)  # MAYBE BUG HERE!
    return num_flashes

def step(input):
    increment_all(input)
    total_flashes = 0
    flashes = []
    for row in range(len(input)):
        for col in range(len(input[row])):
            if input[row][col] == 0:
                flashes.append((row, col))
    for flash in flashes:
        total_flashes += spread_flash(input, *flash)
    return total_flashes

def part1(input):
    num_steps = 100
    total_flashes = 0
    for i in range(num_steps):
        # print(f"===  Step {i} ===")
        # pprint(input)
        total_flashes += step(input)
    return total_flashes

def solve_part1():
    input = parse_input("input11.txt")
    return part1(*input)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part1":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part1(self):
        cases = ["input11_test.txt"]
        expecteds = [1656]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 11.2: Dumbo Octopus  #######################
def part2(input):
    cur_step = 0
    cur_flashes = 0
    while cur_flashes < (len(input) * len(input[0])):
        cur_flashes = step(input)
        # print(cur_flashes)
        cur_step += 1
    return cur_step

def solve_part2():
    input = parse_input("input11.txt")
    return part2(*input)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part2":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part2(self):
        cases = ["input11_test.txt"]
        expecteds = [195]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = "part2"

if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
