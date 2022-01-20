# import algo.matrix_utils as mu
import collections
from cli_util import *
# import functools
import itertools
# import operator as op
# from pprint import pprint
import re
import unittest

INIT_LIMIT = (-50, 50)
RE_RANGES = re.compile(".=(-?\d+)..(-?\d+)")
RANGES = ("x", "y", "z")
Cuboid = collections.namedtuple("Cuboid", RANGES)
Command = collections.namedtuple("Command", ["on", "cuboid"])

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split("\n")
    commands = []
    for line in input:
        is_on = line[:line.index(" ")] == "on"
        ranges = map(lambda tup: tuple(map(int, tup)), RE_RANGES.findall(line))
        cuboid = Cuboid(*ranges)
        command = Command(is_on, cuboid)
        commands.append(command)
    return (commands,)

def get_test_cases():
    num_cases = 2
    if num_cases == 1:
        cases = ["input22_test.txt"]
    else:
        tests_to_run = [3]
        cases = ["input22_test%d.txt" % (test) for test in tests_to_run]
    return cases

def solve(f):
    input = parse_input("input22.txt")
    return f(input)

#######################   Day 22.1: Reactor Reboot  #######################
def limit_range(rng):
    return (max(rng[0], INIT_LIMIT[0]), min(rng[1], INIT_LIMIT[1]))

def get_cubes(range_x, range_y, range_z, init=True):
    ranges = (range_x, range_y, range_z)
    if init:
        ranges = map(limit_range, ranges)
    # Bug: Doesn't check whether input range is actually in [-50, 50].
    # Gives flipped ranges, which conveniently produces empty iterators.
    range_objs = map(lambda rng: range(rng[0], rng[1]+1), ranges)
    return set(itertools.product(*range_objs))

def part1(input):
    commands, = input  # Unpack
    cubes = set()
    for command in commands:
        cuboid = command.cuboid
        new_cubes = get_cubes(*cuboid)
        if command.on:
            cubes |= new_cubes
        else:
            cubes -= new_cubes
    return len(cubes)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [39, 590784]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 22.2: Reactor Reboot  #######################
""" === PLAN ===
* Compute intersection between each processed cuboid and new cuboid.
* Subtract intxn from old cuboid (split if needed).
* New command is on: add new cuboid(s) to processed set.
* New command is off: do nothing.
"""
def range_intersects(r1, r2):
    return ((r1[0] <= r2[0] <= r1[1]) or (r1[0] <= r2[1] <= r1[1])
        or ((r2[0] <= r1[0] <= r2[1])))

def range_overlap(r1, r2):
    return (max(r1[0], r2[0]), min(r1[1], r2[1]))

def intersects(c1, c2):
    return all(itertools.starmap(range_intersects, zip(c1, c2)))

def intersection(c1, c2):   # Return intersecting volume.
    if not intersects(c1, c2):
        return None
    overlaps = itertools.starmap(range_overlap, zip(c1, c2))
    return Cuboid(*overlaps)

def subtract(outer_ranges, hole_ranges):
    ranges = list(outer_ranges)
    cuboids = set()
    for axis in range(len(ranges)):
        outer_range = outer_ranges[axis]
        hole_range = hole_ranges[axis]
        if hole_range[0] > outer_range[0]:
            ranges[axis] = (outer_range[0], hole_range[0]-1)
            cuboids.add(Cuboid(*ranges))
        if hole_range[1] < outer_range[1]:
            ranges[axis] = (hole_range[1]+1, outer_range[1])
            cuboids.add(Cuboid(*ranges))
        ranges[axis] = hole_ranges[axis]
    return cuboids

def volume(cuboid): # Volume in 1x1x1 unit cubes.
    prod = 1
    for rng in RANGES:
        lo, hi = getattr(cuboid, rng)
        prod *= hi - lo + 1
    return prod

def limit_ranges(c):
    return Cuboid(*map(limit_range, c))

def part2(input):
    commands, = input  # Unpack
    processed = set()
    for command in commands:
        cuboid = command.cuboid

        for p_cuboid in tuple(processed):
            hole = intersection(p_cuboid, cuboid)
            if not hole:
                continue
            processed.remove(p_cuboid)  # Discard old cuboid.
            processed |= subtract(p_cuboid, hole)   # Add new "fragments".

        if command.on:
            processed.add(cuboid)
    return sum(map(volume, processed))


class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [2758514936282235]
        # expecteds = [39, 590784]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
