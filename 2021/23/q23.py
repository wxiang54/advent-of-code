import algo.graph_util as gu
import collections
import itertools
import unittest

Location = collections.namedtuple("Loc", ("room", "index"))

EMPTY = "."
PADDING = " "
WALL = "|"
DOOR = ","
GOAL = lambda ch: ord(ch) - ord("A")
COST = lambda i: 10 ** i
HALLWAY = -1

def parse_input(path_in):
    with open(path_in, 'r') as f:
        input = f.read().strip().split()
    hallway_size = input[1].count(".")
    upper = map(GOAL, input[2].strip("#").split("#"))
    lower = map(GOAL, input[3].strip("#").split("#"))
    return hallway_size, upper, lower

def get_test_cases():
    num_cases = 1
    if num_cases == 1:
        cases = ["input23_test.txt"]
    else:
        tests_to_run = [1, 2]
        cases = ["input23_test%d.txt" % (test) for test in tests_to_run]
    return cases

def solve(f):
    input = parse_input("input23.txt")
    return f(input)

#######################   Day 23.1: Amphipod  #######################

def to_str(s):
    return chr(ord("A") + s) if isinstance(s, int) else s

class State:
    @classmethod
    def get_init_state(cls, hallway_size, rooms):
        hallway = [EMPTY] * hallway_size
        for i in range(2, hallway_size-2, 2):
            hallway[i] = DOOR
        last_moved = None
        rooms += (tuple(hallway),)
        return State(rooms, last_moved)

    @classmethod
    def get_final_state(cls, hallway_size, rooms):
        hallway = [EMPTY] * hallway_size
        room_size = len(rooms[0])
        for i in range(2, hallway_size-2, 2):
            hallway[i] = DOOR
        rooms = [(i,) * room_size for i in range(len(rooms))]
        rooms.append(tuple(hallway))
        last_moved = None   # Not significant.
        return State(rooms, last_moved)

    def __init__(self, rooms, last_moved):
        self.rooms = tuple(rooms)
        self.last_moved = last_moved

    def __hash__(self):
        return hash(self.rooms)

    def __eq__(self, other):
        return self.rooms == other.rooms

    def __repr__(self):
        ret = []
        if self.last_moved is not None:
            pod = self.rooms[self.last_moved.room][self.last_moved.index]
            ret.append(f"Last moved: {to_str(pod)} @ {self.last_moved}")
        ret.append("".join(map(to_str, self.rooms[HALLWAY])))
        padding = PADDING * ((len(self.rooms[HALLWAY]) - (2 * len(self.rooms) - 3)) // 2)
        for layer in zip(*(self.rooms[:-1])):
            ret.append(f"{padding}{WALL.join(map(to_str, layer))}{padding}")
        return "\n".join(ret)

    def get_room_topmost(self, room):
        cur_room = self.rooms[room]
        topmost_pod_ind = None
        for i in range(len(cur_room)):
            if isinstance(cur_room[i], int):
                topmost_pod_ind = i
                break
        return topmost_pod_ind

    def get_candidate_locations(self):
        """Return iterable over amphipods' map locations."""
        for i in range(len(self.rooms[HALLWAY])):
            if isinstance(self.rooms[HALLWAY][i], int):
                yield Location(HALLWAY, i)
        for room in range(len(self.rooms)-1):
            topmost = self.get_room_topmost(room)
            if topmost is None:
                continue
            # Assume there are no "holes" below topmost pod (all pods below).
            # If all pods are matching, then treat entire room as done.
            # Otherwise, treat the top pod as movable.
            if all((pod == room for pod in self.rooms[room][topmost:])):
                continue
            yield Location(room, topmost)


    def get_room_location(self, room, cand):
        """Return lowest location in room that cand can enter, according to Rule 2."""
        # Heuristic: If entering own room, go in all the way (lowest spot).
        if room != cand:
            return None
        topmost = self.get_room_topmost(room)
        if topmost is None: # Empty room
            return Location(room, len(self.rooms[room])-1)
        elif all((pod == room for pod in self.rooms[room][topmost:])):
            return Location(room, topmost-1)


    def get_valid_dests_hallway(self, ind, cand, start_in_hallway=False):
        """Get all valid destinations from specified index in hallway, mapped to cost."""
        hallway = self.rooms[HALLWAY]
        dests = {}  # Map destination to cost.
        for delta in (-1, 1):   # -1 = step left, +1 = step right
            i = ind + delta
            while 0 <= i < len(hallway):
                if hallway[i] == EMPTY:
                    if not start_in_hallway:   # Rule 3
                        dests[Location(HALLWAY, i)] = abs(i - ind) * COST(cand)
                elif hallway[i] == DOOR:
                    room = (i // 2) - 1
                    dest = self.get_room_location(room, cand)
                    if dest is not None:
                        steps_enter = dest.index + 1
                        dests[dest] = (abs(i - ind) + steps_enter) * COST(cand)
                else:
                    break
                i += delta
        return dests


    def get_valid_dests(self, src):
        # Assume cand is movable and was not last_moved.
        if src.room == HALLWAY:
            cand = self.rooms[HALLWAY][src.index]
            dests = self.get_valid_dests_hallway(src.index, cand, start_in_hallway=True)
        else:
            cand = self.rooms[src.room][src.index]
            door = (src.room + 1) * 2   # Heuristic: Leave room fully if moving out.
            dests = self.get_valid_dests_hallway(door, cand)
            for dest in dests:
                steps_leave = src.index + 1
                dests[dest] += steps_leave * COST(cand)
        return dests


    def next_states(self):
        """Get all states that can legally follow this one, mapped to cost."""
        states = {}
        srcs = (i for i in self.get_candidate_locations() if i != self.last_moved)
        for src in srcs:
            # Reflect change in src location
            cand = self.rooms[src.room][src.index]
            new_rooms = list(self.rooms)
            new_room = list(self.rooms[src.room])
            new_room[src.index] = EMPTY
            new_rooms[src.room] = tuple(new_room)

            dests = self.get_valid_dests(src)
            if dests:
                for dest in dests:
                    new_room = list(self.rooms[dest.room])
                    new_room[dest.index] = cand
                    new_rooms[dest.room] = tuple(new_room)
                    new_state = State(new_rooms, last_moved=dest)
                    states[new_state] = dests[dest]
                    new_rooms[dest.room] = self.rooms[dest.room]    # Revert changes.

        return states


def part1(input):
    hallway_size, upper, lower = input  # Unpack
    rooms = tuple(zip(upper, lower))
    init_state = State.get_init_state(hallway_size, rooms)
    final_state = State.get_final_state(hallway_size, rooms)

    cost, path = gu.A_star(init_state, final_state, State.next_states)
    # print(cost)
    # print("\n".join(map(str, path)))
    return cost

    # TESTING CODE
    # order = [15, 3, 2, 0, 3, 0, 0, 0, 0, 0]
    # prev_state = init_state
    # for i in order:
    #     next_states = prev_state.next_states()
    #     state = list(next_states.keys())[i]
    #     prev_state = state

    # next_states = prev_state.next_states()
    # for i, state in enumerate(next_states):
    #     print()
    #     print(state, i, f"cost={next_states[state]}")
    return

class Part1Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part1:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part1(self):
        cases = get_test_cases()
        expecteds = [12521]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part1(parse_input(case))
                self.assertEqual(expected, actual)

#######################   Day 23.2: Amphipod  #######################
def get_cost(state):    # Test to see if A* works better with heuristic.
    counts = [0] * (len(state.rooms) - 1)
    cost_total = 0
    for room in range(len(state.rooms)-1):
        cur_room = state.rooms[room]
        for i in range(len(cur_room)):
            if isinstance(cur_room[i], int):
                cand = cur_room[i]
                if cand == room:
                    counts[cand] += 1
                    continue
                if room == HALLWAY:
                    steps_leave = 0
                    door_src = i
                else:
                    steps_leave = i + 1
                    door_src = (room + 1) * 2
                door_dest = (cand + 1) * 2
                steps_to_door = abs(door_src - door_dest)
                steps_enter = counts[cand] + 1
                cost_total += (steps_leave + steps_to_door + steps_enter) * COST(cand)
                counts[cand] += 1
    return cost_total

import timeit
def heuristic_multiple(func, alpha):
    return lambda p: func(p) * alpha


def part2(input):
    hallway_size, upper, lower = input  # Unpack
    mid_upper = map(GOAL, "#D#C#B#A#".strip("#").split("#"))
    mid_lower = map(GOAL, "#D#B#A#C#".strip("#").split("#"))
    rooms = tuple(zip(upper, mid_upper, mid_lower, lower))

    init_state = State.get_init_state(hallway_size, rooms)
    final_state = State.get_final_state(hallway_size, rooms)

    # cost, path = gu.A_star(init_state, final_state, State.next_states,
    #     heuristic_func=get_cost)
    # return cost

    def time_me():
        heuristic = get_cost
        heurs = {
            "Dijkstra": lambda v: 0,
            # "A*": heuristic,
            # "A*1.5": heuristic_multiple(heuristic, 1.5),
            # "A*2": heuristic_multiple(heuristic, 2),
            # "A*3": heuristic_multiple(heuristic, 3),
            # "A*5": heuristic_multiple(heuristic, 5),
        }
        for heur in heurs:
            print(f"===  {heur}  ===")
            cost, path = gu.A_star_debug(init_state, final_state,
                State.next_states, heurs[heur])
            print(f"{cost=}")

    time_me()


class Part2Test(unittest.TestCase):
    def setUp(self):
        if FUNC_TO_TEST != part2:
            self.skipTest(f"Testing: {FUNC_TO_TEST.__name__}()")

    def test_part2(self):
        cases = get_test_cases()
        expecteds = [44169]
        for case, expected in zip(cases, expecteds):
            with self.subTest(case=case):
                actual = part2(parse_input(case))
                self.assertEqual(expected, actual)

###############################      Main     ###############################
FUNC_TO_TEST = part2

if __name__ == "__main__":
    # unittest.main()
    print(solve(FUNC_TO_TEST))
