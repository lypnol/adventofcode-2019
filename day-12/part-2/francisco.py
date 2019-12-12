from tool.runners.python import SubmissionPy


from copy import copy
from functools import reduce
from math import gcd


def parse_input(s):
    positions = []
    for line in s.splitlines():
        numbers = line.strip()[1:-1].split(",")
        positions.append(tuple(int(n.split("=")[1]) for n in numbers))
    return positions


def find_repeat(positions):
    velocities = [0 for _ in range(len(positions))]
    state_0 = copy(positions), copy(velocities)
    steps = 0
    while True:
        # update velocities
        for i in range(len(positions)):
            for j in range(len(positions)):
                velocities[i] += (
                    1
                    if positions[i] < positions[j]
                    else -1
                    if positions[i] > positions[j]
                    else 0
                )

        # update positions
        for i in range(len(positions)):
            positions[i] += velocities[i]

        steps += 1

        # stop condition
        if (positions, velocities) == state_0:
            return steps


def solve_part2(positions):
    repeats = [find_repeat([e[i] for e in positions]) for i in range(3)]
    # lowest common multiple
    return reduce(lambda x, y: x * y // gcd(x, y), repeats)


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part2(parse_input(s))
