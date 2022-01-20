import unittest
from pprint import pprint

FUNC_TO_TEST = "part2"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.is_orthogonal = (p1.x == p2.x) or (p1.y == p2.y)

    def enumerate(self):
        if self.is_orthogonal:
            if self.p1.x == self.p2.x:  # Vertical
                start = self.p1.y
                stop = self.p2.y
                delta = 1 if start <= stop else -1
                while start-delta != stop:
                    yield Point(self.p1.x, start)
                    start += delta
            else:   # Horizontal
                start = self.p1.x
                stop = self.p2.x
                delta = 1 if start <= stop else -1
                while start-delta != stop:
                    yield Point(start, self.p1.y)
                    start += delta
        else:   # Diagonal
            start_x = self.p1.x
            start_y = self.p1.y
            stop_x = self.p2.x
            stop_y = self.p2.y
            delta_x = 1 if start_x <= stop_x else -1
            delta_y = 1 if start_y <= stop_y else -1
            while start_x-delta_x != stop_x:    # x and y should meet at same time
                yield Point(start_x, start_y)
                start_x += delta_x
                start_y += delta_y
            assert start_y - delta_y == stop_y

    def __repr__(self):
        return f"Segment({self.p1}, {self.p2})"


def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split("\n")
    segments = []
    bounds = [0, 0] # inclusive
    for line in input:
        points = line.split(" -> ")
        p1 = points[0].split(",")
        p2 = points[1].split(",")
        x1 = int(p1[0])
        y1 = int(p1[1])
        x2 = int(p2[0])
        y2 = int(p2[1])
        # print(x1, y1, x2, y2)
        if x1 > bounds[0]:
            bounds[0] = x1
        if x2 > bounds[0]:
            bounds[0] = x2
        if y1 > bounds[1]:
            bounds[1] = y1
        if y2 > bounds[1]:
            bounds[1] = y2

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        segment = Segment(p1, p2)
        segments.append(segment)
    return segments, tuple(bounds)

#######################   Day 5.1: Hydrothermal Venture  #######################
def part1(segments, bounds):
    # print(segments, bounds)
    print(bounds)
    bound_x, bound_y = bounds
    grid = []
    for row in range(bound_y + 1):
        grid.append([0] * (bound_x + 1))

    num_hotspots = 0
    for segment in segments:
        if not segment.is_orthogonal:
            continue
        # print(f"{segment} -> {[p for p in segment.enumerate()]}")
        for point in segment.enumerate():
            grid[point.y][point.x] += 1
            if grid[point.y][point.x] == 2:
                num_hotspots += 1
    # pprint(grid)
    return num_hotspots

def solve_part1(): # -> ?
    input = parse_input("input5.txt")
    # print(input)
    return part1(*input)

@unittest.skipUnless(FUNC_TO_TEST == "part1", f"Testing: {FUNC_TO_TEST}()")
class Part1Test(unittest.TestCase):
    def test_part1(self):
        cases = ["input5_test.txt"]
        expecteds = [5]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 5.2: Hydrothermal Venture  #######################
def part2(segments, bounds):
    bound_x, bound_y = bounds
    grid = []
    for row in range(bound_y + 1):
        grid.append([0] * (bound_x + 1))

    num_hotspots = 0
    for segment in segments:
        # print(f"{segment} -> {[p for p in segment.enumerate()]}")
        for point in segment.enumerate():
            grid[point.y][point.x] += 1
            if grid[point.y][point.x] == 2:
                num_hotspots += 1
    # pprint(grid)
    print(num_hotspots)
    return num_hotspots

def solve_part2(): # -> ?
    input = parse_input("input5.txt")
    return part2(*input)

@unittest.skipUnless(FUNC_TO_TEST == "part2", f"Testing: {FUNC_TO_TEST}()")
class Part2Test(unittest.TestCase):
    def test_part2(self):
        cases = ["input5_test.txt"]
        expecteds = [12]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
