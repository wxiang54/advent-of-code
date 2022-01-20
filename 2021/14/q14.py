from datastructs import LinkedList
from collections import Counter, defaultdict
from itertools import tee
import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split("\n")
    template_str = input[0]
    rules = {}
    for line in input[2:]:
        pair, new_element = line.split(" -> ")
        rules[pair] = new_element
    return (template_str, rules)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input14_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input14_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input14.txt")
    return f(*input)

#######################   Day 14.1: Extended Polymerization  #######################
def step(template, rules):  # Modifies template in-place.
    cur_node = template.head
    if cur_node is None:
        return
    while True:
        next_node = cur_node.next
        if next_node is None:
            return
        pair = cur_node.value + next_node.value
        if pair in rules:
            new_element = rules[pair]
            template.insert_after_node(cur_node, new_element)
        cur_node = next_node

def part1(template_str, rules):
    num_steps = 10
    template = LinkedList(list(template_str))
    for _ in range(num_steps):
        step(template, rules)
    counts = Counter(template)
    max_count = max(counts.values())
    min_count = min(counts.values())
    return max_count - min_count

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part1(self):
        cases = get_test_cases()
        expecteds = [1588]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 14.2: Extended Polymerization  #######################
def step_counts(counts, rules):  # Return new pair counts.
    new_counts = defaultdict(int)
    for pair in counts:
        if pair in rules:
            new_element = rules[pair]
            new_counts[pair[0] + new_element] += counts[pair]
            new_counts[new_element + pair[1]] += counts[pair]
        else:   # No rule for pair.
            new_counts[pair] += counts[pair]
    return new_counts

def pairwise(iterable):
    iter1, iter2 = tee(iterable)
    next(iter2, None)
    return (e1+e2 for e1, e2 in zip(iter1, iter2))

def part2(template_str, rules):
    num_steps = 40
    
    # Simulate steps, maintaining only count of each pair.
    counts = defaultdict(int)
    for pair in pairwise(template_str):
        counts[pair] += 1
    for _ in range(num_steps):
        counts = step_counts(counts, rules)
    
    # Tally up counts of elements.
    # Every element will be double-counted except for the ends (first and last).
    element_counts = defaultdict(int)
    for pair in counts:
        e1, e2 = pair
        element_counts[e1] += counts[pair]
        element_counts[e2] += counts[pair]
    
    # Normalize counts. Count of first/last elements will be odd, so round up.
    for element in element_counts:
        element_counts[element] = (element_counts[element] + 1) // 2
    
    max_count = max(element_counts.values())
    min_count = min(element_counts.values())
    return max_count - min_count

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part2(self):
        cases = get_test_cases()
        expecteds = [2188189693529]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
    