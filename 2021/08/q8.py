import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        lines = f.read().strip().split("\n")
    signals = []
    outputs = []
    for line in lines:
        splitted = line.split(" ")
        ind_pipe = splitted.index("|")
        signals.append(splitted[:ind_pipe])
        outputs.append(splitted[ind_pipe+1:])
    return (zip(signals, outputs),)

#######################   Day 8.1: Seven Segment Search  #######################

LEN_TO_DIGIT = {
    2: {1},
    3: {7},
    4: {4},
    5: {2, 3, 5},
    6: {0, 6, 9},
    7: {8}
}

ALL_DIGITS = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
CONTAINS_CF = {0, 1, 3, 4, 7, 8, 9}
CONTAINS_BD = {4, 5, 6, 8, 9}

def part1(input):
    count = 0
    for signals, output in input:
        for digit_chars in output:
             if len(LEN_TO_DIGIT[len(digit_chars)]) == 1:
                 count += 1
    return count

def solve_part1():
    input = parse_input("input8.txt")
    return part1(*input)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part1":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part1(self):
        cases = ["input8_test.txt"]
        expecteds = [26]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 8.2: Seven Segment Search  #######################
'''
Strategy: Classify by # segments, then further classify by containing cf or bd.
    * cf = <pattern for 1>
    * bd = <pattern for 4> - <pattern for 1>
    
    5-seg: {2, 3, 5}
        * Contains cf: 3
        * Doesn't contain cf: {2, 5}
            * Contains bd: 5
            * Doesn't contain bd: 2
    
    6-seg: {0, 6, 9}
        * Contains cf: {0, 9}
            * Contains bd: 9
            * Doesn't contain bd: 0
        * Doesn't contain cf: 6
'''

def part2(input):
    total = 0
    for signals, digits in input:
        signal_to_digit = {}
        signal_1 = None
        signal_4 = None
        
        # Pass 1: Find signals for 1 and 4.
        for signal in signals:
            if len(signal) == 2:
                signal_1 = signal
            elif len(signal) == 4:
                signal_4 = signal
        
        set_cf = set(signal_1)
        set_bd = set(signal_4) - set_cf
        
        # Pass 2: Process all signals.
        for signal in signals:
            set_signal = frozenset(signal)
            cands_by_len = LEN_TO_DIGIT[len(signal)]
            filter_cf = CONTAINS_CF if set_signal >= set_cf else (ALL_DIGITS - CONTAINS_CF)
            filter_bd = CONTAINS_BD if set_signal >= set_bd else (ALL_DIGITS - CONTAINS_BD)
            cands_by_len_cf_bd = cands_by_len & filter_cf & filter_bd     # Expect set of length 1.
            digit = next(iter(cands_by_len_cf_bd))
            signal_to_digit[set_signal] = digit

        output = 0
        for signal in digits:
            output = output*10 + signal_to_digit[frozenset(signal)]
        total += output 
    return total

def solve_part2():
    input = parse_input("input8.txt")
    return part2(*input)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != "part2":
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part2(self):
        cases = ["input8_test.txt"]
        expecteds = [61229]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = "part2"

if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
