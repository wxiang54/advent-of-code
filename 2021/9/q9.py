import functools
import heapq
import itertools
import operator
import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split()
    input = [[int(digit) for digit in line] for line in input]
    return (input,)

class BitVector:
    def __init__(self, val=0):
        self.value = val  # Default: all false.

    def __repr__(self):
        return bin(self.value)

    def __getitem__(self, index):
        if index < 0:
            raise ValueError(f"Invalid index: {index}")
        # print(f"Getting index: {index} from {repr(self)}")
        return (self.value & (1 << index)) != 0

    def __setitem__(self, index, val):
        if val not in (0, 1, True, False):
            raise ValueError(f"Invalid bit value: {val}")
        if val:
            self.setIndex(index)
        else:
            self.clearIndex(index)

    def setIndex(self, index):
        self.value |= 1 << index

    def clearIndex(self, index):
        self.value &= ~(1 << index)

def print_bitvecs(bitvecs, width):
    for bv in bitvecs:
        print(repr(bv)[2:].zfill(width)[::-1])

class BitVectorTest(unittest.TestCase):
    def test_getitem(self):
        bv = BitVector(0b10010111)
        self.assertEqual(bv[0], True)
        self.assertEqual(bv[1], True)
        self.assertEqual(bv[3], False)
        self.assertEqual(bv[20], False)

    def test_setitem(self):
        bv = BitVector()
        bv[0] = 1
        self.assertEqual(bv[0], True)
        bv[2] = True
        self.assertEqual(bv[2], True)
        bv[0] = 0
        self.assertEqual(bv[0], False)

    @unittest.expectedFailure
    def test_setitem_invalid(self):
        bv = BitVector()
        bv[0] = 2

#######################   Day 9.1: Smoke Basin  #######################
def in_range(bounds):
    return lambda ind: bounds[0] <= ind < bounds[1]

def get_adjacents(matrix, row, col):
    if matrix is None or len(matrix) == 0 or len(matrix[0]) == 0:
        raise StopIteration
    row_bounds = (0, len(matrix))
    col_bounds = (0, len(matrix[0]))
    adj_rows = filter(in_range(row_bounds), (row-1, row+1))
    adj_cols = filter(in_range(col_bounds), (col-1, col+1))
    for adj_row in adj_rows:
        yield (adj_row, col)
    for adj_col in adj_cols:
        yield (row, adj_col)

def is_low_point(matrix, row, col):
    return all(matrix[row][col] < matrix[arow][acol]
        for arow, acol in get_adjacents(matrix, row, col))

def part1(matrix):
    total = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if is_low_point(matrix, row, col):
                total += matrix[row][col] + 1
    return total

def solve_part1():
    input = parse_input("input9.txt")
    return part1(*input)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part1":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_get_adjacents(self):
        matrix = parse_input("input9_test.txt")[0]
        last_row = len(matrix)-1
        cases = [(0, 0), (2, 3), (last_row, 0), (0, 1)]
        expecteds = [
            {(0, 1), (1, 0)},
            {(3, 3), (1, 3), (2, 4), (2, 2)},
            {(last_row, 1), (last_row-1, 0)},
            {(0, 0), (0, 2), (1, 1)},
        ]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = set(get_adjacents(matrix, *case))
                self.assertEqual(expected, actual)

    def test_part1(self):
        cases = ["input9_test.txt"]
        expecteds = [15]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 9.2: Smoke Basin  #######################
def part2(matrix):
    num_rows = len(matrix)

    # Maintain "visited" bit vector for each row.
    visited = []
    for row in range(num_rows):
        visited.append(BitVector())

    # Find low points.
    low_points = []
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if is_low_point(matrix, row, col):
                low_points.append((row, col))

    # DFS from each low_point.
    basin_sizes = []
    for row_start, col_start in low_points:
        stack = [(row_start, col_start)]
        cur_basin_size = 0
        while len(stack) != 0:
            row, col = stack.pop()
            if visited[row][col] or matrix[row][col] == 9:
                # "Locations of height 9 do not count as being in any basin"
                continue
            in_basin = True     # Flag indicating whether current point is in basin.
            cands = []
            for arow, acol in get_adjacents(matrix, row, col):
                if visited[arow][acol]:
                    continue
                if matrix[row][col] > matrix[arow][acol]:
                    in_basin = False
                    break   # Alternative path down: Not currently part of basin.
                # NOTE: Currently considers equal-altitude points.
                cands.append((arow, acol))
            if not in_basin:
                continue

            # print(f"  cur point in basin: ({row}, {col})")
            cur_basin_size += 1
            visited[row][col] = True    # Set visited
            for cand in cands:
                stack.append(cand)
        basin_sizes.append(cur_basin_size)
        # === DEBUGGING ===
        # print(f"After processing low point: ({row_start}, {col_start})")
        # print_bitvecs(visited, len(matrix[0]))
        # print(f"Basin size: {cur_basin_size}")

    return functools.reduce(operator.mul, heapq.nlargest(3, basin_sizes))


def solve_part2():
    input = parse_input("input9.txt")
    return part2(*input)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part2":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = ["input9_test.txt"]
        expecteds = [1134]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = "part2"

if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
