import unittest
import textwrap

FUNC_TO_TEST = "part2"

#######################   Day 3.1: Binary Diagnostic  #######################\\
def flipBits(n, mask_len):
    mask = (1 << mask_len) - 1
    return n ^ mask

def part1(input):
    counts = [0] * len(input[0])
    for s in input:
        for i in range(len(s)):
            counts[i] += int(s[i])
    gamma = []
    for i in range(len(counts)):
        if counts[i] >= len(input)/2:
            gamma.append("1")
        else:
            gamma.append("0")
    # epsilon = ["0" if ch == "1" else "1" for ch in gamma]
    gamma = int("".join(gamma), 2)
    # epsilon = int("".join(epsilon), 2)
    epsilon = flipBits(gamma, len(input[0]))
    return gamma * epsilon

def solve_part1(): # -> ?
  path_in = "input3.txt"
  with open(path_in, 'r') as f:
      input = f.read().split()
  return part1(input)

@unittest.skipUnless(FUNC_TO_TEST == "part1", f"Testing: {FUNC_TO_TEST}()")
class Part1Test(unittest.TestCase):
  def test_part1(self):
      cases = [textwrap.dedent('''00100
        11110
        10110
        10111
        10101
        01111
        00111
        11100
        10000
        11001
        00010
        01010''').split()]
      expecteds = [198]
      for case, expected in zip(cases, expecteds):
          with self.subTest(case=case):
              actual = part1(case)
              self.assertEqual(expected, actual)

#######################   Day 3.3: Binary Diagnostic  #######################
def calc_gamma(candidates):
    size = len(next(iter(candidates)))
    counts = [0] * size
    for s in candidates:
        for i in range(len(s)):
            counts[i] += int(s[i])
    gamma = []
    for i in range(len(counts)):
        if counts[i] >= len(candidates)/2:
            gamma.append("1")
        else:
            gamma.append("0")
    return gamma

def calc_epsilon(candidates):
    return ["1" if ch == "0" else "0" for ch in calc_gamma(candidates)]

def filter_matches(candidates, to_match, bit_pos):
    new_cands = candidates.copy()
    for s in candidates:
        if s[bit_pos] != to_match[bit_pos]:
            new_cands.remove(s)
    return new_cands

def part2(input):
    o2_candidates = set(input)
    o2_rating = None
    bit_pos = 0
    while True:
        gamma = calc_gamma(o2_candidates)
        o2_candidates = filter_matches(o2_candidates, gamma, bit_pos)
        # print(o2_candidates)
        if len(o2_candidates) == 1:
            o2_rating = next(iter(o2_candidates))
            break
        bit_pos += 1

    co2_candidates = set(input)
    co2_rating = None
    bit_pos = 0
    while True:
        gamma = calc_epsilon(co2_candidates)
        co2_candidates = filter_matches(co2_candidates, gamma, bit_pos)
        if len(co2_candidates) == 1:
            co2_rating = next(iter(co2_candidates))
            break
        bit_pos += 1

    o2_rating = int(o2_rating, 2)
    co2_rating = int(co2_rating, 2)
    return o2_rating * co2_rating

def solve_part2(): # -> 4550283
  path_in = "input3.txt"
  with open(path_in, 'r') as f:
      input = f.read().split()
  return part2(input)

@unittest.skipUnless(FUNC_TO_TEST == "part2", f"Testing: {FUNC_TO_TEST}()")
class Part2Test(unittest.TestCase):
  def test_part2(self):
      cases = [textwrap.dedent('''00100
        11110
        10110
        10111
        10101
        01111
        00111
        11100
        10000
        11001
        00010
        01010''').split()]
      expecteds = [230]
      for case, expected in zip(cases, expecteds):
          with self.subTest(case=case):
              actual = part2(case)
              self.assertEqual(expected, actual)


if __name__ == "__main__":
    # unittest.main()
    print(eval(f"solve_{FUNC_TO_TEST}")())
