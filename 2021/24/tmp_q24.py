class Value:
    def __init__(self, val=None):
        if val == None:
            self.cands = set(range(1, 10))
        else:
            self.cands = {val}
        self.changed = False    # Whether value changed after computation.

    def __repr__(self):
        return str(self.cands)

    def __str__(self):
        known = self.get_known()
        if known is None:
            return "?"
        return str(known)

    def is_known(self): # Whether value is known.
        return len(self.cands) == 1

    def get_known(self):
        if not self.is_known():
            return None
        return next(iter(self.cands))

    def apply_all(self, other, name):
        inputs = itertools.product(self.cands, other.cands)
        self.cands = set(itertools.starmap(NAME_TO_OP[name], inputs))
        self.changed = True
        return self

    # ====  OVERLOADED OPERATIONS  ====
    def __add__(self, other):
        other_val = other.get_known()
        if other_val is not None:   # Other is known.
            if other_val == 0:
                self.changed = False
                return self
        return self.apply_all(other, "add")

    def __mul__(self, other):
        other_val = other.get_known()
        if other_val is not None:   # Other is known.
            if other_val == 0:
                self.cands = {0}
                self.changed = True
                return self
            elif other_val == 1:
                self.changed = False
                return self
        return self.apply_all(other, "mul")

    def __floordiv__(self, other):
        other_val = other.get_known()
        if other_val is not None:   # Other is known.
            if other_val == 1:
                self.changed = False
                return self
        return self.apply_all(other, "truncdiv")

    def __mod__(self, other):
        return self.apply_all(other, "mod")

    def __eq__(self, other):
        self_known = self.get_known()
        self.changed = True
        if self_known is not None and self_known == other.get_known():
            self.cands = {1}
        elif self.cands.isdisjoint(other.cands):
            self.cands = {0}
        else:
            self.cands = {0, 1}
        return self


def __add__(self, other):
    if isinstance(other, int):
        self.min += other
        self.max += other
    else:   # Assume an unknown.
        self.min += other.min
        self.max += other.max
    return self
self.__radd__ = self.__add__

def __mul__(self, other):
    if isinstance(other, int):
        self.min *= other
        self.max *= other
    else:   # Assume an unknown.
        self.min *= other.min
        self.max *= other.max
    return self
self.__rmul__ = self.__mul__

def __div__(self, other):
    if isinstance(other, int):
        self.min = int(self.min / other)
        self.max = int(self.max / other)
    else:   # Assume an unknown.
        self.min = min(int(self.min / other.min), int(self.min / other.max))
        self.max = max(int(self.max / other.min), int(self.max / other.max))
    return self
self.__rmul__ = self.__mul__

def __mod__(self, other):

    return

def __eq__(self, other):
    def range_intersects(r1, r2):
        return ((r1[0] <= r2[0] <= r1[1]) or (r1[0] <= r2[1] <= r1[1])
            or ((r2[0] <= r1[0] <= r2[1])))
    return range_intersects((self.min, self.max), (other.min, other.max))




def run_command(self, com):
    name, arg1, arg2 = com
    arg1_val = getattr(self, arg1)
    if name == "inp":
        if arg2 is None:
            setattr(self, arg1, Value())  # Mark unknown
        else:
            setattr(self, arg1, Value(int(arg2)))
        self.history.append(com)
        return

    try:
        arg2_val = Value(int(arg2))
    except:
        arg2_val = getattr(self, arg2)

    # Apply the operation.
    NAME_TO_OP[name](arg1_val, arg2_val)

    arg1_known = arg1_val.get_known()
    if arg1_known is not None:  # Became known as result of current command:
        # Remove all earlier assignments to arg1, up to most recent usage.
        keep = []
        while self.history:
            com = self.history[-1]
            if com.arg2 == arg1:
                # Stopping point: first usage of arg1.
                break
            self.history.pop()

            # Discard all computations assigned to arg1.
            if com.arg1 != arg1:
                keep.append(com)

        # Insert custom imp statement.
        if self.history or arg1_known != 0:
            self.history.append(Command("inp", arg1, arg1_known))

        # Refill history with commands to keep
        while keep:
            self.history.append(keep.pop())

        # print(self.history)
    else:
        if arg1_val.changed:
            self.history.append(com)


def run_command_stream(self, com, stream):
    name, arg1, arg2 = com
    arg1_val = getattr(self, arg1)

    if name == "inp":
        if arg2 is None:
            setattr(self, arg1, next(stream))
        else:
            setattr(self, arg1, int(arg2))
        return
    try:
        arg2_val = int(arg2)
    except:
        arg2_val = getattr(self, arg2)

    if name == "div":
        name = "truncdiv"
    elif name == "eql":
        name = "eql2"
    setattr(self, arg1, NAME_TO_OP[name](arg1_val, arg2_val))
    return
