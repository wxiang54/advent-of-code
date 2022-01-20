import unittest
import textwrap

FUNC_TO_TEST = "part2"

class Board:
    def __init__(self):
        self.rows = []
        self.cols = []
        self.board_size = 0
        self.completed = False
    
    def add_row(self, row):
        self.board_size = len(row)
        self.rows.append(set(row))
        if len(self.cols) == 0:
            for col in row:
                self.cols.append(set())
        for i in range(len(self.cols)):
            self.cols[i].add(row[i])        
    
    def score(self, winning_number):
        total_uncrossed = 0
        for row in self.rows:
            for num_str in row:
                total_uncrossed += int(num_str)
        return total_uncrossed * int(winning_number)
    
    def cross_sets(self, sets, number):
        for set_ in sets:
            if number in set_:
                set_.remove(number)
                if len(set_) == 0:   # Finished row.
                    self.completed = True
                break
    
    def cross(self, number):
        self.cross_sets(self.rows, number)
        self.cross_sets(self.cols, number)
    
    def __repr__(self):
        ret = ""
        for row in self.rows:
            for i in range(self.board_size):
                intxn = row & self.cols[i]
                if len(intxn) > 0:
                    cur_number = next(iter(row & self.cols[i]))
                else:
                    cur_number = "X"
                if len(cur_number) == 1:
                    cur_number = " " + cur_number
                ret += cur_number + " "
            ret += "\n"
        return ret

#######################   Day 4.1: Giant Squid  #######################
def part1(order, boards):
    for number in order:
        for board in boards:
            board.cross(number)
            if board.completed:
                return board.score(number)
    return

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split("\n")
    order = input[0].split(",")
    boards = set()
    cur_board = Board()
    for line in input[2:]:
        if line == "":
            # print(cur_board)
            boards.add(cur_board)
            cur_board = Board()
            continue
        cur_board.add_row(line.split())
    return order, boards
    
def solve_part1(): # -> 55770
    input = parse_input("input4.txt")
    return part1(*input)

@unittest.skipUnless(FUNC_TO_TEST == "part1", f"Testing: {FUNC_TO_TEST}()")
class Part1Test(unittest.TestCase):
    def test_part1(self):
        cases = ["input4_test.txt"]
        expecteds = [4512]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 4.3: Giant Squid  #######################
def part2(order, boards):
    for number in order:
        # print(number)
        boards_to_remove = []
        for board in boards:
            board.cross(number)
            if board.completed:
                # print(f"{number} completed board:\n{board}")
                boards_to_remove.append(board)
        if len(boards) == len(boards_to_remove): # Should happen when both are 1.
            score = boards_to_remove[0].score(number)
            return score
        for board in boards_to_remove:
            boards.remove(board)
    return

def solve_part2(): # -> ?
    input = parse_input("input4.txt")
    return part2(*input)

@unittest.skipUnless(FUNC_TO_TEST == "part2", f"Testing: {FUNC_TO_TEST}()")
class Part2Test(unittest.TestCase):
    def test_part2(self):
        cases = ["input4_test.txt"]
        expecteds = [1924]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                print("Score:", actual)
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
