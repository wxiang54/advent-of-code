import collections
import functools
import itertools
import unittest

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().split()
    start_positions = list(map(int, input[4::5]))
    return (start_positions,)

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input21_test.txt"]
    else:
        num_cases_to_test = 1
        cases = ["input21_test%s.txt" % (case+1) for case in range(num_cases_to_test)]
    return cases

def solve(f):
    input = parse_input("input21.txt")
    return f(input)

#######################   Day 21.1: Dirac Dice  #######################
class Game:
    WIN_THRESH = 1000
    ROLLS_PER_TURN = 3

    def __init__(self, start_positions, die):
        self.turns = 0
        self.die = die  # Expect an infinite iterator.
        self.num_players = len(start_positions)
        self.next_player = itertools.cycle(range(self.num_players))
        self.scores = [0] * self.num_players
        self.spaces = start_positions.copy()
        self.finished = False

    def advance_player(self, player, roll):
        def advance(old_space, roll):
            return (((old_space - 1) + roll) % 10) + 1
        new_space = advance(self.spaces[player], roll)
        self.spaces[player] = new_space
        self.scores[player] += new_space

    def step(self):
        roll_sum = sum(itertools.islice(self.die, self.ROLLS_PER_TURN))
        player = next(self.next_player)
        self.advance_player(player, roll_sum)
        self.turns += 1

        if self.scores[player] >= self.WIN_THRESH:
            print(f"Winner: Player {player+1} with score {self.scores[player]}.")
            self.finished = True

    def play(self):
        while not self.finished:
            self.step()


def part1(input):
    start_positions, = input
    die = itertools.cycle(range(1, 101))
    game = Game(start_positions, die)
    game.play()
    return min(game.scores) * (game.turns * game.ROLLS_PER_TURN)

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [739785]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 21.2: Dirac Dice  #######################
class DiracGameState():
    def __init__(self, start_positions):
        num_players = len(start_positions)
        self.scores = [0] * num_players
        self.spaces = start_positions.copy()
        self.next_player = 0    # Player who last moved.

    def __hash__(self):
        return hash((tuple(self.scores), tuple(self.spaces), self.next_player))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def copy(self):
        ret = DiracGameState(self.spaces)
        ret.scores = self.scores.copy()
        ret.next_player = self.next_player
        return ret

class DiracGame:
    WIN_THRESH = 21
    MAX_ROLL = 3
    ROLLS_PER_TURN = 3

    def get_sums(max_roll, rolls_per_turn):
        all_sums = map(sum, itertools.product(range(1, max_roll+1),
            repeat=rolls_per_turn))
        sum_counts = collections.Counter(all_sums)
        return sum_counts

    ALL_ROLL_COUNTS = get_sums(MAX_ROLL, ROLLS_PER_TURN)

    def __init__(self, start_positions):
        self.num_players = len(start_positions)
        self.init_state = DiracGameState(start_positions)

    @staticmethod
    def advance(old_space, roll):
        return (((old_space - 1) + roll) % 10) + 1

    @functools.cache
    def calculate_wins(self, state=None):
        """Returns (num_p1_wins, num_p2_wins, ...)"""
        if state is None:
            state = self.init_state
        cur_player = state.next_player
        cur_space = state.spaces[cur_player]
        cur_score = state.scores[cur_player]

        next_state = state.copy()
        next_player = (cur_player + 1) % self.num_players
        next_state.next_player = next_player

        all_wins = [0] * self.num_players
        for roll, count in self.ALL_ROLL_COUNTS.items():
            new_space = DiracGame.advance(cur_space, roll)
            new_score = cur_score + new_space
            if new_score >= self.WIN_THRESH:
                all_wins[cur_player] += count
            else:   # Keep playing
                next_state.spaces[cur_player] = new_space
                next_state.scores[cur_player] = new_score
                future_wins = self.calculate_wins(next_state)
                for i, wins in enumerate(future_wins):
                    all_wins[i] += count * wins

        return tuple(all_wins)


def part2(input):
    start_positions, = input
    game = DiracGame(start_positions)
    wins = game.calculate_wins()
    return max(wins)

class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [444356092776315]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
