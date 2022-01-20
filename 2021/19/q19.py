from itertools import product, combinations, starmap
import numpy as np
import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split("\n")
    scanners = []
    cur_scanner = Scanner()
    for line in input:
        if line.startswith("---"):
            ind_num = len("--- scanner ")
            cur_scanner.num = int(line[ind_num:line.rindex(" ---")])
        elif not line:
            scanners.append(cur_scanner)
            cur_scanner = Scanner()
        else:
            coords = map(int, line.split(","))
            cur_scanner.add_beacon(*coords)
    return (scanners,)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input19_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input19_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input19.txt")
    return f(*input)

#######################   Day 19.1: Beacon Scanner  #######################
AXIS = {"x": 0, "y": 1, "z": 2}
SIGNS = {"+", "-"}

class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.x},{self.y},{self.z})"

    def __iter__(self):
        yield from (self.x, self.y, self.z)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(tuple(iter(self)))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

class Vector(Point3D):
    pass

class UnitVector(Vector):
    def __init__(self, axis):
        super().__init__()
        # +x --> +(sign) x(dir)
        self.sign, self.dir = axis
        self.sign = {"+": 1, "-": -1}[self.sign]
        setattr(self, self.dir, self.sign)


class Orientation:
    def __init__(self, axis_x="+x", axis_y="+y"):
        self.axis_x = UnitVector(axis_x)    # Actually +x, but scanner believes it's axis_x.
        self.axis_y = UnitVector(axis_y)    # Actually +y, but scanner believes it's axis_y.
        z_axis = next(iter(set(AXIS.keys()) - set(self.axis_x.dir) - set(self.axis_y.dir)))
        z_sign = np.cross(tuple(self.axis_x), tuple(self.axis_y))[AXIS[z_axis]]
        self.axis_z = UnitVector(("+" if z_sign > 0 else "-") + z_axis)
        # print(self.axis_x, self.axis_y, "-->", self.axis_z)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.axis_x},{self.axis_y},{self.axis_z})"

    def transform(self, point):   # Assume 0 offset (rooted at same point).
        new_x = self.axis_x.sign * getattr(point, self.axis_x.dir)
        new_y = self.axis_y.sign * getattr(point, self.axis_y.dir)
        new_z = self.axis_z.sign * getattr(point, self.axis_z.dir)
        new_point = Point3D(new_x, new_y, new_z)
        return new_point

def get_all_orientations():
    orientations = set()
    for sign_x in SIGNS:
        for axis_x in AXIS:
            for sign_y in SIGNS:
                for axis_y in AXIS:
                    if axis_x == axis_y:
                        continue
                    orientations.add(Orientation(sign_x+axis_x, sign_y+axis_y))
    return orientations

ALL_ORIENTATIONS = get_all_orientations()


class Scanner:
    OVERLAP_THRESH = 12

    def __init__(self):
        self.beacons = set()
        self.num = -1
        self.offset = Vector(0, 0, 0)

    def __repr__(self):
        return f"Scanner {self.num}: {self.beacons}"

    def add_beacon(self, x, y, z):
        self.beacons.add(Point3D(x, y, z))

    def find_overlap(self, ref_scanner):
        # Brute-force all my orientations w.r.t. reference scanner.
        # print(f"Testing: {ref_scanner.num} and {self.num}:")
        all_alignments = product(ref_scanner.beacons, self.beacons)
        for ref_beacon, my_beacon in all_alignments:
            for ori in ALL_ORIENTATIONS:
                # Try a new alignment.
                offset = ref_beacon - ori.transform(my_beacon)
                if max(abs(offset.x), abs(offset.y), abs(offset.z)) > 2000:
                    continue
                beacons_trans = set()
                num_overlap = 0
                for p in self.beacons:
                    p_trans = ori.transform(p)
                    if p_trans + offset in ref_scanner.beacons:
                        num_overlap += 1
                    beacons_trans.add(p_trans)

                    num_beacons_rem = len(self.beacons) - len(beacons_trans)
                    if num_beacons_rem < (Scanner.OVERLAP_THRESH - num_overlap):
                        # Not enough beacons left to make it -> skip.
                        break
                else:
                    # FOUND OVERLAPPING
                    print(f"Found alignment btwn beacons {ref_scanner.num} and {self.num}:")
                    print(f" * Orientation: {ori}")
                    print(f" * Point match (ref || me): {ref_beacon} || {my_beacon}")
                    self.offset = offset + ref_scanner.offset
                    self.beacons = beacons_trans
                    return True
        # Tried all orientations and alignments with no result.
        return False


def part1(scanners):
    first_scanner = scanners[0]
    ref_scanners = {first_scanner}
    rem_scanners = set(scanners[1:])
    depleted_scanners = set()
    while rem_scanners:
        overlapping_scanner = None
        for ref_scanner in (ref_scanners - depleted_scanners):
            for scanner in rem_scanners:
                found_overlap = scanner.find_overlap(ref_scanner)
                if found_overlap:
                    overlapping_scanner = scanner
                    break
            else:   # for-loop didn't break, meaning no overlap found.
                # This ref_scanner has been depleted.
                depleted_scanners.add(ref_scanner)
                continue
            rem_scanners.remove(overlapping_scanner)
            break
        else:
            raise RuntimeError("Unable to find overlap between scanners.")
        ref_scanners.add(overlapping_scanner)

    all_beacons = set()
    for scanner in ref_scanners:
        beacons_offset = set(map(lambda b: b+scanner.offset, scanner.beacons))
        all_beacons |= beacons_offset
    return len(all_beacons)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [79]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 19.2: Beacon Scanner  #######################
def manhattan_distance(s1, s2):
    return sum(map(abs, s1.offset - s2.offset))

def part2(scanners):
    pairs = [
        (0, 11), (0, 9), (9, 19), (9, 10), (19, 26), (0, 29),
        (10, 34), (34, 14), (34, 15), (10, 28), (28, 36), (28, 6),
        (6, 18), (18, 16), (28, 1), (1, 25), (1, 4), (25, 33),
        (4, 5), (4, 21), (4, 7), (7, 3), (3, 32), (32, 2), (32, 31),
        (15, 27), (27, 13), (15, 20), (36, 8), (8, 12), (12, 37),
        (37, 22), (8, 35), (35, 24), (35, 23), (2, 17), (2, 30)]
    # pairs = [(0, 1), (1, 3), (1, 4), (4, 2)]
    for s1, s2 in pairs:
        found_overlap = scanners[s2].find_overlap(scanners[s1])
        if not found_overlap:
            raise RuntimeError("???")

    return max(starmap(manhattan_distance, combinations(scanners, 2)))

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [3621]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
