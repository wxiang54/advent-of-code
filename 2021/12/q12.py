import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    return (input,)

def get_test_cases():
    num_cases = 3
    if num_cases == 1:
        cases = ["input12_test.txt"]
    else:
        num_cases_to_test = 3
        cases = ["input12_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

class Node:
    def __init__(self, name):
        self.name = name    # Mostly used for debugging.
        self.is_small = (name == name.lower())
        self.neighbors = set()
    
    def __repr__(self):
        return f"Node({self.name}, {set(n.name for n in self.neighbors)})"
    
    def __str__(self):
        return self.name
    
    def add_neighbor(self, node):
        self.neighbors.add(node)
        if self not in node.neighbors:
            node.neighbors.add(self)
    
class Path:
    def __init__(self, start):
        self.path = [start]
        self.visited = {start}    # Stores small vertices visited.
    
    def __len__(self):
        return len(self.path)
    
    def __repr__(self):
        return ",".join([str(node) for node in self.path])

    def push(self, node):     # Return whether push was successful.
        if node in self.visited:
            return False
        self.path.append(node)
        if node.is_small:
            self.visited.add(node)
        return True
    
    def pop(self):
        ret = self.path.pop()
        if ret in self.visited:
            self.visited.remove(ret)
        return ret
    
    def peek(self):
        return self.path[-1]

#######################   Day 12.1: Passage Pathing  #######################
def build_graph(input):
    name_to_node = {}
    for line in input:
        n1_name, n2_name = line.split("-")
        if n1_name not in name_to_node:
            name_to_node[n1_name] = Node(n1_name)
        if n2_name not in name_to_node:
            name_to_node[n2_name] = Node(n2_name)
        name_to_node[n1_name].add_neighbor(name_to_node[n2_name])
    return (name_to_node["start"], name_to_node["end"])

def dfs(init_path, end):
    paths = []  # For debugging.
    cur_path = init_path
    def recurse():
        head = cur_path.peek()   # Path can never be empty since it always has "start".
        # print(f"cur node: {head}")
        if head is end:
            paths.append(str(cur_path))
            return 1
        
        total_paths = 0
        for neighbor in head.neighbors:
            if cur_path.push(neighbor):
                # print(f"  pushing {neighbor}")
                total_paths += recurse()
                cur_path.pop()
        return total_paths
    ret = recurse()
    # print(paths)
    return ret

def part1(input):
    start, end = build_graph(input)
    path = Path(start)    
    total_paths = dfs(path, end)
    # print(paths)
    return total_paths

def solve_part1():
    input = parse_input("input12.txt")
    return part1(*input)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part1(self):
        cases = get_test_cases()
        expecteds = [10, 19, 226]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 12.2: Passage Pathing  #######################
class NewPath(Path):
    def __init__(self, start):
        super().__init__(start)
        self.start = start
        self.visited_twice = None   # If set, that node has been visited twice.
    
    def push(self, node):     # Return whether push was successful.
        if node is self.start:
            return False
        if node in self.visited and self.visited_twice is not None:
            return False
        self.path.append(node)
        if node.is_small:
            if node in self.visited:
                self.visited_twice = node
            else:
                self.visited.add(node)
        return True
    
    def pop(self):
        ret = self.path.pop()
        if ret is self.visited_twice:
            self.visited_twice = None
        elif ret in self.visited:
            self.visited.remove(ret)
        return ret

def part2(input):
    start, end = build_graph(input)
    path = NewPath(start)    
    total_paths = dfs(path, end)
    return total_paths

def solve_part2():
    input = parse_input("input12.txt")
    return part2(*input)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part2(self):
        cases = get_test_cases()
        expecteds = [36, 103, 3509]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(*parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST.__name__}")())
