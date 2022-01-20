class Subtract:
    @staticmethod
    def get_rel(outer_range, hole_range):
        if outer_range[0] == hole_range[0]:
            if outer_range[1] == hole_range[1]:
                return "A"  # All
            return "E"  # End
        if outer_range[1] == hole_range[1]:
            return "E"  # End
        return "M"  # Middle

    # Assume ranges are on axis with relationship "E".
    @staticmethod
    def valid_range_E(outer_range, hole_range):
        if outer_range[0] == hole_range[0]: # Left-aligned
            return (hole_range[1]+1, outer_range[1])
        assert outer_range[1] == hole_range[1]  # Right-aligned
        return (outer_range[0], hole_range[0]-1)

    # Assume ranges are on axis with relationship "M".
    @staticmethod
    def valid_ranges_M(outer_range, hole_range):
        range_M1 = (outer_range[0], hole_range[0]-1)
        range_M2 = (hole_range[1]+1, outer_range[1])
        return (range_M1, range_M2)

    @staticmethod
    def replace_rel(rels, ind, char):
        new_rels = list(rels)
        new_rels[ind] = char
        return "".join(new_rels)


    @staticmethod   # Completely covered.
    def AAA(rels, outer_ranges, hole_ranges):
        return set()

    @staticmethod   # A big slice off one side.
    def AAE(rels, outer_ranges, hole_ranges):
        ind_E = rels.index("E")
        range_E = Subtract.valid_range_E(outer_ranges[ind_E], hole_ranges[ind_E])
        new_ranges = list(outer_ranges)
        new_ranges[ind_E] = range_E
        return {Cuboid(*new_ranges)}

    @staticmethod   # Two whole slices.
    def AAM(rels, outer_ranges, hole_ranges):
        ind_M = rels.index("M")
        ret_cuboids = set()
        for range_M in Subtract.valid_ranges_M(outer_ranges[ind_M], hole_ranges[ind_M]):
            new_ranges = list(outer_ranges)
            new_ranges[ind_M] = range_M
            ret_cuboids.add(Cuboid(*new_ranges))
        return ret_cuboids

    @staticmethod   # Three slices, 2 big on ends, 1 small in middle.
    def AEM(rels, outer_ranges, hole_ranges):
        ind_E = rels.index("E")
        ind_M = rels.index("M")
        range_E = Subtract.valid_range_E(outer_ranges[ind_E], hole_ranges[ind_E])
        new_ranges = list(outer_ranges)
        new_ranges[ind_E] = range_E
        new_ranges[ind_M] = hole_ranges[ind_M]
        return {Cuboid(*new_ranges)} | Subtract.AAM(rels, outer_ranges, hole_ranges)

    @staticmethod   # L case
    def AEE(rels, outer_ranges, hole_ranges):
        ind_E1, ind_E2 = rels.index("E"), rels.rindex("E")
        range_E1 = Subtract.valid_range_E(outer_ranges[ind_E1], hole_ranges[ind_E1])
        range_E2 = Subtract.valid_range_E(outer_ranges[ind_E2], hole_ranges[ind_E2])

        new_ranges1 = list(outer_ranges)
        new_ranges1[ind_E1] = range_E1

        new_ranges2 = list(outer_ranges)
        new_ranges2[ind_E2] = range_E2
        new_ranges2[ind_E1] = hole_ranges[ind_E1]
        return {Cuboid(*new_ranges1), Cuboid(*new_ranges2)}

    @staticmethod   # Donut case
    def AMM(rels, outer_ranges, hole_ranges):
        # Run AAM, then turn first M into A and run AAM again.
        ret_cuboids = Subtract.AAM(rels, outer_ranges, hole_ranges)
        ind_M = rels.index("M")
        new_outer_ranges = list(outer_ranges)
        new_outer_ranges[ind_M] = hole_ranges[ind_M]
        ret_cuboids |= Subtract.AAM(
            Subtract.replace_rel(rels, ind_M, "A"), new_outer_ranges, hole_ranges)
        return ret_cuboids

    @staticmethod   # Corner case, reliant on AEE (L)
    def EEE(rels, outer_ranges, hole_ranges):
        # Run AEE (L case), then turn outer 2 E's into A's and run AAE.
        ret_cuboids = Subtract.AEE(rels, outer_ranges, hole_ranges)
        ind_E1, ind_E2 = rels.index("E"), rels.rindex("E")
        new_outer_ranges = list(outer_ranges)
        new_outer_ranges[ind_E1] = hole_ranges[ind_E1]
        new_outer_ranges[ind_E2] = hole_ranges[ind_E2]
        new_rels = list(rels)
        new_rels[ind_E1] = new_rels[ind_E2] = "A"
        ret_cuboids |= Subtract.AAE(new_rels, new_outer_ranges, hole_ranges)
        return ret_cuboids

    @staticmethod   # Middle corner, reliant on AEE (L)
    def EEM(rels, outer_ranges, hole_ranges):
        # Run AEE (L case), then turn E's into A's and run AAM.
        ret_cuboids = Subtract.AEE(rels, outer_ranges, hole_ranges)
        ind_E1, ind_E2 = rels.index("E"), rels.rindex("E")
        new_outer_ranges = list(outer_ranges)
        new_outer_ranges[ind_E1] = hole_ranges[ind_E1]
        new_outer_ranges[ind_E2] = hole_ranges[ind_E2]
        new_rels = list(rels)
        new_rels[ind_E1] = new_rels[ind_E2] = "A"
        ret_cuboids |= Subtract.AAM(new_rels, new_outer_ranges, hole_ranges)
        return ret_cuboids

    @staticmethod   # Donut filled on one end, reliant on AMM (donut)
    def EMM(rels, outer_ranges, hole_ranges):
        # Run AAE, then turn E into A and run AMM.
        ret_cuboids = Subtract.AAE(rels, outer_ranges, hole_ranges)
        ind_E = rels.index("E")
        new_outer_ranges = list(outer_ranges)
        new_outer_ranges[ind_E] = hole_ranges[ind_E]
        ret_cuboids |= Subtract.AMM(
            Subtract.replace_rel(rels, ind_E, "A"), new_outer_ranges, hole_ranges)
        return ret_cuboids

    @staticmethod   # Cubic hole encapsulated in outer cube.
    def MMM(rels, outer_ranges, hole_ranges):
        # Run AAM, then turn first M into A and run AMM.
        ret_cuboids = Subtract.AAM(rels, outer_ranges, hole_ranges)
        ind_M = rels.index("M")
        new_outer_ranges = list(outer_ranges)
        new_outer_ranges[ind_M] = hole_ranges[ind_M]
        ret_cuboids |= Subtract.AMM(
            Subtract.replace_rel(rels, ind_M, "A"), new_outer_ranges, hole_ranges)
        return ret_cuboids

    @staticmethod
    def subtract(outer, hole):
        rels = []   # Dim. relationships btwn outer and hole.
        outer_ranges = tuple(map(lambda r: getattr(outer, r), RANGES))
        hole_ranges = tuple(map(lambda r: getattr(hole, r), RANGES))
        ret_cuboids = []
        rels = "".join(itertools.starmap(Subtract.get_rel, zip(outer_ranges, hole_ranges)))
        subtract_func = eval(f"Subtract.{''.join(sorted(rels))}")
        return subtract_func(rels, outer_ranges, hole_ranges)



def test_shapes():
    def pc(c):
        return f"{c}, V={volume(c)}"

    outer = Cuboid((0, 4), (0, 4), (0, 4))    # Volume 125
    print(pc(outer))

    def to_hole_ranges(str):
        hole_ranges = {"A": (0, 4), "E": (0, 2), "M": (1, 2)}
        return Cuboid(*map(lambda s: hole_ranges[s], str))

    holes = {
        "AAA": to_hole_ranges("AAA"),
        "AAE": to_hole_ranges("AAE"),
        "AAM": to_hole_ranges("AAM"),
        "AEM": to_hole_ranges("AEM"),
        "AEE": to_hole_ranges("AEE"),
        "AMM": to_hole_ranges("AMM"),
        "EEE": to_hole_ranges("EEE"),
        "EEM": to_hole_ranges("EEM"),
        "EMM": to_hole_ranges("EMM"),
        "MMM": to_hole_ranges("MMM"),
        "MMM2": Cuboid((1, 2), (2, 3), (1, 3)),
    }

    for hole_name, hole in holes.items():
        print(f"\n{hole_name}: Subtracting {pc(hole)}, "
            f"expV = {volume(outer) - volume(hole)}")
        ret = Subtract.subtract(outer, hole)
        print("\n".join([f"  * {pc(c)}" for c in ret]))
