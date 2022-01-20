import collections
# import functools
import itertools
import math
import operator as op
from pprint import pprint
import unittest

Command = collections.namedtuple("Command", ("name", "arg1", "arg2"))

import timer
CLOCK = timer.getClock("cmd", notifIncrement=1, goal=14)

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split("\n")
    commands = []
    for line in input:
        line = line.split()
        if line[0] == "inp" and (len(line) < 3 or line[2] == "None"):
            commands.append(Command(line[0], line[1], None))
        else:
            commands.append(Command(line[0], line[1], line[2]))
    return (commands,)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input24_test.txt"]
    else:
        tests_to_run = [1, 2]
        cases = ["input24_test%d.txt" % (test) for test in tests_to_run]
    cases = ["input24_test.txt"]
    return cases

def solve(f):
    input = parse_input("input24.txt")
    # input = parse_input("commands.txt")
    return f(input)

#######################   Day 24.1: Arithmetic Logic Unit  #######################
NAME_TO_OP = {
    "add": op.add,
    "mul": op.mul,
    "div": op.floordiv,
    "mod": op.mod,
    "eql": op.eq,
    "eql2": lambda a, b: int(a == b),
    "truncdiv": lambda a, b: int(a / b),
}

class Value:
    def __init__(self, val=None):
        if val == None:
            self.cands = set(range(1, 10))
        else:
            self.cands = {val}
        self.changed = False    # Whether value changed after computation.

    def __repr__(self):
        return str(self.cands)

    def __str__(self):
        known = self.get_known()
        if known is None:
            return "?"
        return str(known)

    def is_known(self): # Whether value is known.
        return len(self.cands) == 1

    def get_known(self):
        if not self.is_known():
            return None
        return next(iter(self.cands))

    def apply_all(self, other, name):
        inputs = itertools.product(self.cands, other.cands)
        self.cands = set(itertools.starmap(NAME_TO_OP[name], inputs))
        self.changed = True
        return self

    # ====  OVERLOADED OPERATIONS  ====
    def __add__(self, other):
        other_val = other.get_known()
        if other_val is not None:   # Other is known.
            if other_val == 0:
                self.changed = False
                return self
        return self.apply_all(other, "add")

    def __mul__(self, other):
        other_val = other.get_known()
        if other_val is not None:   # Other is known.
            if other_val == 0:
                self.cands = {0}
                self.changed = True
                return self
            elif other_val == 1:
                self.changed = False
                return self
        return self.apply_all(other, "mul")

    def __floordiv__(self, other):
        other_val = other.get_known()
        if other_val is not None:   # Other is known.
            if other_val == 1:
                self.changed = False
                return self
        return self.apply_all(other, "truncdiv")

    def __mod__(self, other):
        return self.apply_all(other, "mod")

    def __eq__(self, other):
        self_known = self.get_known()
        self.changed = True
        if self_known is not None and self_known == other.get_known():
            self.cands = {1}
        elif self.cands.isdisjoint(other.cands):
            self.cands = {0}
        else:
            self.cands = {0, 1}
        return self



def command_str(com):
    return f"{com.name} {com.arg1} {com.arg2}"

VARS = "wxyz"

class ALU:
    def __init__(self, stream=False):
        if stream:
            self.w = self.x = self.y = self.z = 0
            self.z_to_w = {0: ()}
        else:
            self.w = Value(0)
            self.x = Value(0)
            self.y = Value(0)
            self.z = Value(0)
            self.history = []
        # self.history = [Command("inp", var, 0) for var in VARS]

    def __str__(self):
        return " ".join(f"{var}={getattr(self, var)}" for var in VARS)

    def __repr__(self):
        return " ".join(f"{var}={getattr(self, var)!r}" for var in VARS)


    def step(self, coms):   # Step for each w.
        z_to_w = {}
        for w in range(1, 10):
            self.w = w
            for z, ws in self.z_to_w.items():
                self.z = z
                for com in coms:
                    # print(command_str(com), f"with {w=}, {z=}")
                    name, arg1, arg2 = com
                    if name == "inp":
                        continue
                    arg1_val = getattr(self, arg1)

                    try:
                        arg2_val = int(arg2)
                    except:
                        arg2_val = getattr(self, arg2)

                    if name == "div":
                        name = "truncdiv"
                    elif name == "eql":
                        name = "eql2"
                    setattr(self, arg1, NAME_TO_OP[name](arg1_val, arg2_val))

                    # print(self)

                # print(f"Final z: {self.z}")
                z_to_w[self.z] = ws + (w,)
        self.z_to_w = z_to_w
        print(len(z_to_w))
        return


    def run_command(self, com):
        name, arg1, arg2 = com
        arg1_val = getattr(self, arg1)
        if name == "inp":
            if arg2 is None:
                setattr(self, arg1, Value())  # Mark unknown
            else:
                setattr(self, arg1, Value(int(arg2)))
            self.history.append(com)
            return

        try:
            arg2_val = Value(int(arg2))
        except:
            arg2_val = getattr(self, arg2)

        # Apply the operation.
        NAME_TO_OP[name](arg1_val, arg2_val)

        arg1_known = arg1_val.get_known()
        if arg1_known is not None:  # Became known as result of current command:
            # Remove all earlier assignments to arg1, up to most recent usage.
            keep = []
            while self.history:
                com = self.history[-1]
                if com.arg2 == arg1:
                    # Stopping point: first usage of arg1.
                    break
                self.history.pop()

                # Discard all computations assigned to arg1.
                if com.arg1 != arg1:
                    keep.append(com)

            # Insert custom imp statement.
            if self.history or arg1_known != 0:
                self.history.append(Command("inp", arg1, arg1_known))

            # Refill history with commands to keep
            while keep:
                self.history.append(keep.pop())

            # print(self.history)
        else:
            if arg1_val.changed:
                self.history.append(com)


def step(prev_z, div, add1, add2):
    z_to_w = {}
    for w in range(1, 10):
        for z, old_ws in prev_z.items():
            x = int(z%26 + add1 != w)
            z = int(z / div) * (25*x + 1)
            z += x*(w + add2)
            z_to_w[z] = old_ws + (w,)
    return z_to_w


DIVS = [1, 1, 1, 1, 1, 26, 26, 1, 26, 1, 26, 26, 26, 26]
ADD1S = [14, 14, 14, 12, 15, -12, -12, 12, -7, 13, -8, -5, -10, -7]
ADD2S = [14, 2, 1, 13, 5, 5, 5, 9, 3, 13, 2, 1, 11, 8]

def part1(input):
    # commands, = input  # Unpack
    # print(len(commands))
    # commands = (Command("inp", "w", None), Command("add", "w", 5), Command("add", "w", 5))
    # stream = iter([3, 8] * 7) # 14 input numbers
    # alu = ALU(stream=True)
    # alu = ALU(stream=False)

    prev_z = {0: ()}

    CLOCK.start()
    for ins in zip(DIVS, ADD1S, ADD2S):
        prev_z = step(prev_z, *ins)
        CLOCK.incrementCount()
        print(len(prev_z))
    CLOCK.stop()

    ret = prev_z[0]
    return ret

    # repeat_len = 18
    # while commands:
    #     alu.step(commands[:repeat_len])
    #     commands = commands[repeat_len:]
    #     CLOCK.incrementCount()
        # break

    # for command in commands:
    #     alu.run_command(command)
    #     if command.name == "inp":
    #         print(f"z set is size {len(alu.z.cands)}")
        # print(f"{command_str(command)} \t-> {alu!r}")
        # alu.run_command_stream(command, stream)
    # print(alu)
    # print(len(alu.history))
    # print("\n".join(map(command_str, alu.history)))
    # print(alu.z_to_w)
    # ret = alu.z_to_w[0]
    # return ret
    return

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [0]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 24.2: Arithmetic Logic Unit  #######################
def step_reverse(prev_z, div, add1, add2):
    z_to_w = {}
    for w in range(9, 0, -1):
        for z, old_ws in prev_z.items():
            x = int(z%26 + add1 != w)
            z = int(z / div) * (25*x + 1)
            z += x*(w + add2)
            z_to_w[z] = old_ws + (w,)
    return z_to_w

def part2(input):
    prev_z = {0: ()}
    CLOCK.start()
    for ins in zip(DIVS, ADD1S, ADD2S):
        prev_z = step_reverse(prev_z, *ins)
        CLOCK.incrementCount()
        # print(len(prev_z))
    CLOCK.stop()
    ret = prev_z[0]
    return ret

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [0]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
