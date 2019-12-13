from math import gcd
from functools import reduce
import itertools
import numpy as np
from tool.runners.python import SubmissionPy


class Moon:
    def __init__(self, positions):
        self.pos = np.array(positions)
        self.dim = len(positions)
        self.v = np.zeros((self.dim,)).astype(np.int64)
        self.initial = np.array(positions.copy())
        self.tmp = np.zeros((self.dim,)).astype(np.int64)

    def apply_gravity(self, other):
        self.v += np.sign(other.pos - self.pos)

    def move(self):
        self.pos += self.v

    def at_start(self, i):
        return self.pos[i] == self.initial[i]

    def dimensions(self):
        return self.dim

    def __repr__(self):
        return f"Moon(pos={self.pos}, velocity={self.v})"

def lcm(a, b):
    return a * b // gcd(a, b)

def parse_moons(s):
    for line in s.splitlines():
        pos = [int(el.strip(">")[3:]) for el in line.split(",")]
        yield Moon(pos)


def apply_gravity(moons):
    for m, m2 in itertools.product(moons, repeat=2):
        m.apply_gravity(m2)


def move(moons):
    for m in moons:
        m.move()


def step(moons):
    apply_gravity(moons)
    move(moons)


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        moons = list(parse_moons(s))
        step(moons)
        counts = 2

        loop_indices = [None for _ in range(moons[0].dimensions())]
        to_find = set(range(moons[0].dimensions()))

        while to_find:
            found = []
            for i in to_find:
                if all(m.at_start(i) for m in moons):
                    loop_indices[i] = counts
                    found.append(i)

            for f in found:
                to_find.remove(f)

            counts += 1
            step(moons)

        return reduce(lcm, loop_indices)
