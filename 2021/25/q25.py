import unittest

RIGHT = ">"
DOWN = "v"
EMPTY = "."

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    input = [list(line) for line in input]
    return (input,)

def get_test_cases():
    num_cases = 2
    if num_cases == 1:
        cases = ["input25_test.txt"]
    else:
        tests_to_run = [2]
        cases = ["input25_test%d.txt" % (test) for test in tests_to_run]
    return cases

def solve(f):
    input = parse_input("input25.txt")
    return f(input)

#######################   Day 25.1: Sea Cucumber  #######################
def next_func(grid, direction):
    if direction == RIGHT:
        return lambda r, c: (r, c+1 if c+1 < len(grid[0]) else 0)
    elif direction == DOWN:
        return lambda r, c: (r+1 if r+1 < len(grid) else 0, c)
    return None

def step(grid, direction):
    next_coords = next_func(grid, direction)
    to_move = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == direction:
                next_r, next_c = next_coords(r, c)
                if grid[next_r][next_c] == EMPTY:
                    to_move.add((r, c))
    for r, c in to_move:
        next_r, next_c = next_coords(r, c)
        grid[r][c] = EMPTY
        grid[next_r][next_c] = direction
    return len(to_move) > 0

def print_grid(grid):
    print("\n".join(["".join(line) for line in grid]))
    print()

def part1(input):
    grid, = input  # Unpack
    num_steps = 0
    while True:
    # for i in range(10):
        right_moved = step(grid, RIGHT)
        down_moved = step(grid, DOWN)
        num_steps += 1
        # print(f"After {num_steps} steps:")
        # print_grid(grid)
        if not (right_moved or down_moved):
            return num_steps
    return

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [58]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(parse_input(case))
                self.assertEqual(expected, actual)


###############################      Main     ###############################
FUNC_TO_TEST = part1

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
