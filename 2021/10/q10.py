import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    return (input,)

#######################   Day 10.1: Syntax Scoring  #######################
L = ["(", "[", "{", "<"]
R = [")", "]", "}", ">"]
R2L = dict(zip(R, L))
L_SET = frozenset(L)
R_SET = frozenset(R)

def part1(input):
    scores = dict(zip(R, [3, 57, 1197, 25137]))
    total_score = 0
    for line in input:
        stack = []  # Maintain all left symbols.
        for char in line:
            if char in L_SET:
                stack.append(char)
            else:
                assert char in R_SET
                if stack.pop() != R2L[char]:
                    # Corrupted line
                    total_score += scores[char]
                    break
    return total_score

def solve_part1():
    input = parse_input("input10.txt")
    return part1(*input)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part1":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part1(self):
        cases = ["input10_test.txt"]
        expecteds = [26397]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 10.2: Syntax Scoring  #######################
def get_median(L):
    return sorted(L)[len(L) // 2]   # Favors right in case of tie (len is even).

def part2(input):
    L_to_score = dict(zip(L, [1, 2, 3, 4]))
    score_multiplier = 5
    scores = []
    for line in input:
        stack = []  # Maintain all left symbols.
        corrupted = False
        for char in line:
            if char in L_SET:
                stack.append(char)
            else:
                assert char in R_SET
                if stack.pop() != R2L[char]:
                    corrupted = True
                    break   # Corrupted line
        
        if corrupted or len(stack) == 0:    # Empty stack = complete line
            continue
        
        # If got here, must be incomplete line.
        cur_score = 0
        while len(stack):
            cur_score = (cur_score * score_multiplier) + L_to_score[stack.pop()]
        scores.append(cur_score)
    
    return get_median(scores)

def solve_part2():
    input = parse_input("input10.txt")
    return part2(*input)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part2":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part2(self):
        cases = ["input10_test.txt"]
        expecteds = [288957]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = "part2"

if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
