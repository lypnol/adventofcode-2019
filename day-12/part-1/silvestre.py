import itertools

import numpy as np

from tool.runners.python import SubmissionPy

class Moon:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

class SilvestreSubmission(SubmissionPy):

    @staticmethod
    def parse_line(l):
        """<x=-4, y=3, z=15>"""
        return [int(el.strip()[2:]) for el in l[1:-1].split(",")]

    def run(self, s):
        moons = []
        for l in s.strip().splitlines():
            position = np.array(self.parse_line(l))
            moons.append(Moon(position, np.zeros_like(position)))

        for _ in range(1000):
            # apply gravity
            for m1, m2 in itertools.combinations(moons, 2):
                sign = np.sign(m1.position - m2.position)
                m1.velocity -= sign
                m2.velocity += sign

            # apply velocity
            for m in moons:
                m.position += m.velocity

        potential_energy = np.array([np.sum(np.abs(m.position)) for m in moons])
        kinetic_energy = np.array([np.sum(np.abs(m.velocity)) for m in moons])

        return np.sum(potential_energy * kinetic_energy)