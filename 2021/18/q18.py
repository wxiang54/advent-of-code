from datastructs import BinaryNode
from itertools import permutations, starmap
from functools import reduce
import operator as op
import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    input = [eval(line) for line in input]
    return (input,)

def get_test_cases():
    num_cases = 3
    if num_cases == 1:
        cases = ["input18_test.txt"]
    else:
        num_cases_to_test = 3
        cases = ["input18_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input18.txt")
    return f(*input)

#######################   Day 18.1: Snailfish  #######################
def first_true(iterable, cond):
    return next(filter(cond, iterable), None)   # default None.


class SnailNode(BinaryNode):
    PAIR = "<pair>"
    THRESH_EXPLODE = 4
    THRESH_SPLIT = 10

    def __init__(self, value=PAIR, *, left=None, right=None):
        super().__init__(value, left=left, right=right)

    @classmethod
    def from_list(cls, list_in):
        left, right = list_in
        if isinstance(left, list):
            left = cls.from_list(left)
        else:   # Assume left is int.
            left = SnailNode(left)
        if isinstance(right, list):
            right = cls.from_list(right)
        else:
            right = SnailNode(right)
        root = SnailNode(cls.PAIR, left=left, right=right)
        return root

    def __str__(self):
        def recurse(root):
            if root is None:
                return ""
            if root.value != root.PAIR:
                return str(root.value)
            return f"[{recurse(root.left)}, {recurse(root.right)}]"
        return recurse(self)

    def find_split_candidate(self):
        def _split_cond(root):
            return isinstance(root.value, int) and root.value >= self.THRESH_SPLIT
        return first_true(iter(self), _split_cond)

    def find_explode_candidate(self):
        def inorder(root, depth):
            if root is None:
                return None
            left_cand = inorder(root.left, depth+1)
            if left_cand:
                return left_cand
            if root.value == root.PAIR and depth >= self.THRESH_EXPLODE:
                return root
            return inorder(root.right, depth+1)
        return inorder(self, 0)

    def __iter__(self): # In-order traversal.
        def inorder(root):
            if root is None:
                yield from ()   # Empty iterable
                return
            yield from inorder(root.left)
            yield root
            yield from inorder(root.right)
        return inorder(self)

    def __add__(self, other):
        if not isinstance(other, SnailNode):
            cls = self.__class__.__name__
            raise TypeError(f"Can only add {cls} (not {type(other)}) to {cls}.")
        root = SnailNode(value=self.PAIR, left=self, right=other)
        while True:
            cand = root.find_explode_candidate()
            if cand:
                cand.explode()
                continue
            cand = root.find_split_candidate()
            if cand:
                cand.split()
                continue
            break   # No candidates found for explode/split.
        return root

    def leftmost(self):
        cur = self
        while cur.left is not None:
            cur = cur.left
        return cur

    def rightmost(self):
        cur = self
        while cur.right is not None:
            cur = cur.right
        return cur

    def predecessor(self):
        cur = self
        while cur.parent is not None:
            if cur is cur.parent.right:  # Is right child?
                return cur.parent.left.rightmost()
            cur = cur.parent
        return None

    def successor(self):
        cur = self
        while cur.parent is not None:
            if cur is cur.parent.left:  # Is left child?
                return cur.parent.right.leftmost()
            cur = cur.parent
        return None

    def explode(self):
        pred = self.predecessor()
        succ = self.successor()
        if pred is not None:
            pred.value += self.left.value
        if succ is not None:
            succ.value += self.right.value

        # Set self to zero-node.
        self.value = 0
        self.left = None
        self.right = None
        return

    def split(self):
        q, r = divmod(self.value, 2)
        self.left = SnailNode(q)
        self.right = SnailNode(q+r)
        self.value = self.PAIR  # Class constant
        return

    def magnitude(self):
        if self.value == self.PAIR:
            return (3 * self.left.magnitude()) + (2 * self.right.magnitude())
        else:
            return self.value


def part1(input):
    return reduce(op.add, map(SnailNode.from_list, input)).magnitude()

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [1137, 3488, 4140]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 18.2: Snailfish  #######################
def part2(input):
    return max(starmap(
        lambda s1, s2: (SnailNode.from_list(s1) + SnailNode.from_list(s2)).magnitude(),
        permutations(input, 2)))

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [140, 3805, 3993]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
