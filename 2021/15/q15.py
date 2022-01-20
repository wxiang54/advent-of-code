# Local imports
import algo.matrix_util as mu
import algo.graph_util as gu

import heapq
import itertools
import numpy as np
from pprint import pprint
import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    input = [[int(i) for i in line] for line in input]
    return (input,)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input15_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input15_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input15.txt")
    return f(*input)

#######################   Day 15.1: Chiton  #######################
def part1(input):
    input[0][0] = 0
    inf = float('inf')
    for row in range(len(input)):
        for col in range(len(input[row])):
            if not (row == 0 and col == 0):
                top = input[row-1][col] if row > 0 else inf
                left = input[row][col-1] if col > 0 else inf
                input[row][col] += min(top, left)
        # pprint(input)
        # break
    return input[-1][-1]

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [40]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 15.2: Chiton  #######################
def new_val(i):
    if i == 9:
        return 1
    return i+1

def part2(input):
    num_tiles = 5
    input = np.array(input)
    inc = np.vectorize(new_val)

    # Stack columns.
    to_stack = [input]
    for _ in range(num_tiles-1):
        to_stack.append(inc(to_stack[-1]))
    input = np.hstack(to_stack)

    # Stack rows.
    to_stack = [input]
    for _ in range(num_tiles-1):
        to_stack.append(inc(to_stack[-1]))
    input = np.vstack(to_stack)

    # Parameters for A* search.
    num_rows, num_cols = input.shape
    v_start = (0, 0)
    v_end = (num_rows-1, num_cols-1)
    adj_func = mu.get_adjacency_func(input)    # Takes row, col unpacked.
    neighbor_func = lambda p: {(r, c): input[r][c] for r, c in adj_func(p)}
    heuristic_func = mu.distance_from(v_end, dist_func=mu.manhattan_distance)

    # === TIMING CODE
    import timeit
    def manhattan_multiple(i):
        return lambda p: heuristic_func(p) * i

    def time_me():
        # impls = ("heap", "list", "linkedlist")
        impls = ("heap",)
        heurs = {
            "Dijkstra": lambda v: 0,
            "A*": heuristic_func,
            "A*2": manhattan_multiple(2),
            "A*3": manhattan_multiple(3),
            "A*4": manhattan_multiple(4),
            "A*5": manhattan_multiple(5),
            "A*_euclid": mu.distance_from(v_end, dist_func=mu.euclidean_distance),
        }
        num_repeats = 1
        n = 50
        to_print = []
        for i in range(num_repeats):
            for impl in impls:
                for heur in heurs:
                    t = timeit.timeit(lambda: gu.A_star(v_start, v_end,
                        neighbor_func, heurs[heur], impl), number=n)
                    to_print.append(f"[{i+1}] {heur} with {impl}: {t}s")
        print("\n".join(to_print))

    def debug():
        heurs = {
            # "Dijkstra": lambda v: 0,
            # "A*": heuristic_func,
            # "A*2": manhattan_multiple(2),
            "A*3": manhattan_multiple(3),
            "A*3.25": manhattan_multiple(3.25),
            "A*3.5": manhattan_multiple(3.5),
            "A*3.75": manhattan_multiple(3.75),
            "A*4": manhattan_multiple(4),
            # "A*5": manhattan_multiple(5),
            # "A*_euclid": mu.distance_from(v_end, dist_func=mu.euclidean_distance),
        }
        for heur in heurs:
            print(f"Heuristic: {heur}")
            # one_func = lambda p: {(r, c): 1 for r, c in adj_func(p)}
            # cost, path = gu.A_star_debug(v_start, v_end, one_func, heurs[heur])
            cost, path = gu.A_star_debug(v_start, v_end, neighbor_func, heurs[heur])
            print(cost)
            print(len(list(path)))
    # debug()
    # time_me()
    print(np.mean(input))

    # cost, path = gu.A_star(v_start, v_end, neighbor_func, heuristic_func)
    # print(tuple(path))
    # return cost
    return 315


class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [315]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    unittest.main()
    # print(solve(FUNC_TO_TEST))
