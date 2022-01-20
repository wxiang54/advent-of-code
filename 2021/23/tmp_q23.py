class Amphipod:
    def __init__(self, type_, room, ind):  # room -1 is hallway.
        self.type = type_
        self.room = room
        self.ind = ind
        self.cost = 10 ** ind

    def __repr__(self):
        return chr(ord("A") + self.type)

    def __eq__(self, other):
        return self.type == other.type

    @property
    def happy(self):
        return self.room == self.type

class State:
    def __init__(self, hallway_size, rooms):
        self.hallway = [EMPTY] * hallway_size
        for i in range(2, hallway_size-2, 2):
            self.hallway[i] = DOOR
        self.rooms = rooms  # Each room is [lower, upper]
        self.remaining = 0
        self.pods = []
        self.last_moved = None
        for i in range(len(rooms)):
            rooms[i][0] = Amphipod(rooms[i][0], i, 0)
            rooms[i][1] = Amphipod(rooms[i][1], i, 1)
            if rooms[i][0].type != i:    # Not already in right room.
                self.pods.append(rooms[i][0])
                self.remaining += 1
            elif rooms[i][1].type == i:
                continue    # Both pods in right room.
            self.pods.append(rooms[i][1])
            if rooms[i][1].type != i:
                self.remaining += 1

    def __repr__(self):
        padding = PADDING * ((len(self.hallway) - (2 * len(self.rooms) - 1)) // 2)
        ret = []
        ret.append(f"last moved: {self.last_moved} // {self.remaining} remaining")
        ret.append("".join(map(str, self.hallway)))
        lower, upper = zip(*self.rooms)
        ret.append(f"{padding}{WALL.join(map(str, upper))}{padding}")
        ret.append(f"{padding}{WALL.join(map(str, lower))}{padding}")
        return "\n".join(ret)

    def neighbors(self):
        def get_valid_dests(pod):
            dests = {}  # map dest to cost

            def per_hallway(cur_ind):
                """Returns False if no further progress is possible."""
                if cur_ind < 0 or isinstance(self.hallway[cur_ind], Amphipod):
                    return False    # End of the road
                elif self.hallway[cur_ind] == DOOR:  # Above room.
                    room = (cur_ind-2) // 2
                    if room != pod.type or self.rooms[room][1]:
                        return True    # Rule 2 or blocked
                    lower = self.rooms[room][0]
                    if isinstance(lower, Amphipod) and lower != pod:
                        return True    # Rule 2
                    dests[(room, 1)] = pod.cost * (abs(pod.ind - cur_ind) + 1)
                    if lower == EMPTY:   # More space at bottom.
                        dests[(room, 0)] = dests[(room, 1)] + pod.cost
                else:   # Assume empty space.
                    dests[(HALLWAY, cur_ind)]


            if pod.room == HALLWAY:
                # First try going left.
                cur_ind = pod.ind
                while True:
                    cur_ind -= 1


            else:
                pass

        movable = self.pods - {self.last_moved}
        for pod in movable:
            orig_room, orig_ind = pod.room, pod.ind
