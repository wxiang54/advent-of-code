import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split("\n")
    ind_middle = input.index("")
    
    dots = set()
    for dot_str in input[:ind_middle]:
        x_str, y_str = dot_str.split(",")
        dots.add((int(x_str), int(y_str)))
    
    folds = []
    for fold_str in input[ind_middle+1:]:
        _, _, fold_str = fold_str.split()
        dim, pos_str = fold_str.split("=")
        dim = ("x", "y").index(dim)
        folds.append((dim, int(pos_str)))
        
    return (dots, folds)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input13_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input13_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input13.txt")
    return f(*input)

#######################   Day 13.1: Transparent Origami  #######################
def dot_fold(dot, fold):
    axis, pos = fold
    assert dot[axis] != pos 
    if dot[axis] < pos: # No need to fold
        return dot
    new_dot = list(dot)
    delta = dot[axis] - pos
    new_dot[axis] = pos - delta
    return tuple(new_dot)

def simulate_fold(dots, fold):  # Modifies dots set
    dots_to_add = set()
    dots_to_remove = set()
    for dot in dots:
        new_dot = dot_fold(dot, fold)
        # Case 1: No change (same dot).
        if new_dot == dot:
            continue
        # Case 2: Dot folds onto existing dot --> Remove old dot
        dots_to_remove.add(dot)
        # Case 3: Dot folds onto new dot --> Remove old dot, add new dot 
        if new_dot not in dots:
            dots_to_add.add(new_dot)
    for dot in dots_to_remove:
        dots.remove(dot)
    for dot in dots_to_add:
        dots.add(dot)

def part1(dots, folds):
    simulate_fold(dots, folds[0])
    return len(dots)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")
    
    def test_part1(self):
        cases = get_test_cases()
        expecteds = [17]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(*parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 13.2: Transparent Origami  #######################
def part2(dots, folds):
    for fold in folds:
        simulate_fold(dots, fold)
    print(dots)
    return

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
