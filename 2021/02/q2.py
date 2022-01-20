import unittest
import textwrap

FUNC_TO_TEST = "dive2"

#######################   X.x: Dive  #######################
def dive(commands):
    depth = 0
    horiz = 0
    for command in commands:
        direc, mag = command.split(" ")
        mag = int(mag)
        if direc == "forward":
            horiz += mag
        elif direc == "up":
            depth -= mag
        elif direc == "down":
            depth += mag
    return depth * horiz

def solve_dive(): # -> ?
    path_in = "input2.txt"
    with open(path_in, 'r') as f:
        commands = f.read().strip().split("\n")
    return dive(commands)

@unittest.skipUnless(FUNC_TO_TEST == "dive", f"Testing: {FUNC_TO_TEST}()")
class DiveTest(unittest.TestCase):
    def test_dive(self):
        cases = [textwrap.dedent('''
            forward 5
            down 5
            forward 8
            up 3
            down 8
            forward 2''').strip().split("\n")]
        expecteds = [150]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = dive(case)
                self.assertEqual(expected, actual)


#######################   Day 2.2: Dive2  #######################
def dive2(commands):
    depth = 0
    horiz = 0
    aim = 0
    for command in commands:
        direc, mag = command.split(" ")
        mag = int(mag)
        if direc == "forward":
            horiz += mag
            depth += aim * mag
        elif direc == "up":
            aim -= mag
        elif direc == "down":
            aim += mag
    return depth * horiz

def solve_dive2(): # -> ?
    path_in = "input2.txt"
    with open(path_in, 'r') as f:
        commands = f.read().strip().split("\n")
    return dive2(commands)

@unittest.skipUnless(FUNC_TO_TEST == "dive2", f"Testing: {FUNC_TO_TEST}()")
class Dive2Test(unittest.TestCase):
    def test_dive2(self):
        cases = [textwrap.dedent('''
            forward 5
            down 5
            forward 8
            up 3
            down 8
            forward 2''').strip().split("\n")]
        expecteds = [900]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = dive2(case)
                self.assertEqual(expected, actual)



if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
