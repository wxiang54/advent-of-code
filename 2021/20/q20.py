import algo.matrix_util as mu
import itertools
import numpy as np
import unittest

LIT = "1"
UNLIT = "0"
TO_BIT = {"#": LIT, ".": UNLIT}
INIT_SIZE = 1000

def expand_array(arr, fill_char):
    nr, nc = arr.shape

    # Add columns first.
    new_col = np.full((nr, 1), fill_char)
    arr = np.concatenate((new_col, arr, new_col), axis=1)

    # Then add rows.
    new_row = np.full((1, nc+2), fill_char)
    arr = np.concatenate((new_row, arr, new_row), axis=0)
    return arr

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    enhance_str = "".join(map(lambda c: TO_BIT[c], input[0]))
    img = np.array([list(s) for s in input[1:]])
    to_bit = np.vectorize(lambda c: TO_BIT[c])
    img = to_bit(img)
    img = expand_array(img, UNLIT)
    return (enhance_str, img)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input20_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input20_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input20.txt")
    return f(*input)

#######################   Day 20.1: Trench Map  #######################
def to_pixels(img):
    to_pixel = {}
    for k, v in TO_BIT.items():
        to_pixel[v] = k
    to_pixel_func = np.vectorize(lambda c: to_pixel[c])
    img = to_pixel_func(img)
    return "\n".join(["".join(row) for row in img])

def count_lit(img):
    return len(img[img == LIT])

def step(enhance_str, img):
    void_char = img[0][0]
    next_void_char = enhance_str[0 if void_char == UNLIT else -1]

    def next_bit(img, r, c):
        row_in_range = mu.in_range((0, len(img)))
        col_in_range = mu.in_range((0, len(img[0])))
        bits = []
        # for ar, ac in itertools.product(range(r-1, r+2), range(c-1, c+2)):
        for ar in range(r-1, r+2):
            for ac in range(c-1, c+2):
                if row_in_range(ar) and col_in_range(ac):
                    bits.append(img[ar][ac])
                else:
                    bits.append(void_char)
        enhance_ind = int("".join(bits), 2)
        return enhance_str[enhance_ind]

    new_img = img.copy()
    for r, c in itertools.product(range(len(img)), range(len(img[0]))):
        new_img[r][c] = next_bit(img, r, c)

    new_img = expand_array(new_img, next_void_char)
    return new_img

def part1(enhance_str, img):
    num_steps = 2
    # print(to_pixels(img))
    for i in range(num_steps):
        img = step(enhance_str, img)
    return count_lit(img)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [35]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 20.2: Trench Map  #######################
def part2(enhance_str, img):
    num_steps = 50
    # print(to_pixels(img))
    for i in range(num_steps):
        img = step(enhance_str, img)
    return count_lit(img)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [3351]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
