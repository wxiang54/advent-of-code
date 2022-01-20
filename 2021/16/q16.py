import unittest
from functools import reduce
import operator

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    return (input[0],)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input16_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input16_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input16.txt")
    return f(*input)

#######################   Day 16.1: Packet Decoder  #######################
def consume(stream, n):
    return "".join([next(stream) for i in range(n)])

def consume_int(stream, n):
    return int(consume(stream, n), 2)

VERSION_SUM = 0

def read_packet(stream):    # return number of bytes consumed
    global VERSION_SUM
    version = consume_int(stream, 3)
    print(f"====\nversion: {version}")
    VERSION_SUM += version
    type_id = consume_int(stream, 3)
    print(f"type ID: {type_id}")
    num_bits_read = 6
    if type_id == 4:
        pad = 1
        bit_str = ""
        while pad != 0:
            pad = consume_int(stream, 1)
            bit_str += consume(stream, 4)
            num_bits_read += 5
        literal = int(bit_str, 2)
        return num_bits_read, literal
    else:
        # Operator
        length_type = consume_int(stream, 1)
        print(f"length type: {length_type}")
        num_bits_read += 1
        sub_bits_read = 0
        sub_packets = []
        if length_type == 0:
            total_len = consume_int(stream, 15)
            num_bits_read += 15
            print(f"total length: {total_len}")
            while sub_bits_read < total_len:
                bits_read, val = read_packet(stream)
                print(f"parsed {val}, {bits_read} bits")
                sub_packets.append(val)
                sub_bits_read += bits_read
        else:
            num_subpackets = consume_int(stream, 11)
            num_bits_read += 11
            print(f"# subpackets: {num_subpackets}")
            for i in range(num_subpackets):
                bits_read, val = read_packet(stream)
                print(f"parsed {val}, {bits_read} bits")
                sub_packets.append(val)
                sub_bits_read += bits_read
        num_bits_read += sub_bits_read
        
        ret = None
        if type_id == 0:
            ret = sum(sub_packets)
        elif type_id == 1:
            ret = reduce(operator.mul, sub_packets, 1)
        elif type_id == 2:
            ret = min(sub_packets)
        elif type_id == 3:
            ret = max(sub_packets)
        else:
            first, second = sub_packets
            if type_id == 5:
                ret = 1 if first > second else 0
            elif type_id == 6:
                ret = 1 if first < second else 0
            elif type_id == 7:
                ret = 1 if first == second else 0
        return num_bits_read, ret

def part1(input):
    bin_str = bin(int(input, 16))[2:]   # BUG: does not retain leading zeroes.
    if len(bin_str) % 4:
        padding = 4 - (len(bin_str) % 4)
        bin_str = "0"*padding + bin_str
    # print(bin_str)
    stream = iter(bin_str)
    read_packet(stream)
    return VERSION_SUM

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part1(self):
        cases = get_test_cases()
        expecteds = [0]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 16.2: Packet Decoder  #######################
def part2(input):
    bin_str = bin(int(input, 16))[2:]
    if len(bin_str) % 4:
        padding = 4 - (len(bin_str) % 4)
        bin_str = "0"*padding + bin_str
    # print(bin_str)
    stream = iter(bin_str)
    ret = read_packet(stream)
    return ret[1]

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part2(self):
        cases = get_test_cases()
        expecteds = [0]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    unittest.main()
    # print(solve(FUNC_TO_TEST))
