from tool.runners.python import SubmissionPy

from math import gcd, pi
from collections import defaultdict
import numpy as np
from bisect import insort


def normalized_angle(angle):
    pgcd = gcd(angle[0], angle[1])
    angle = (angle[0] // pgcd, angle[1] // pgcd)
    return angle


def distance(angle):
    return angle[0] * angle[0] + angle[1] * angle[1]


def compare_angle(angle):
    angle = np.angle(complex(*angle)) % (2 * pi)

    return angle


class RemiSubmission(SubmissionPy):
    def run(self, s):
        asteroids = []
        for i, line in enumerate(s.split("\n")):
            for j, ch in enumerate(list(line)):
                if ch == "#":
                    asteroids.append((j, i))

        visibles = {}

        for (j1, i1) in asteroids:
            visibles[(j1, i1)] = defaultdict(list)
            for (j2, i2) in asteroids:
                if i1 == i2 and j1 == j2:
                    continue
                angle = (i1 - i2, j2 - j1)
                d = distance(angle)
                angle = normalized_angle(angle)
                visibles[(j1, i1)][angle].append((d, (j2, i2)))

        # asteroid seeing the most asteroids
        m = max(
            (asteroid for asteroid in visibles.keys()),
            key=lambda asteroid: len(visibles[asteroid]),
        )

        visible = visibles[m]
        # sort angles in clockwise order starting up
        angles = sorted((angle for angle in visible.keys()), key=compare_angle)

        # sort asteroid at each angle by distance
        for d in visible.values():
            d.sort(reverse=True)

        destroyed = 0
        last_destroyed = ()

        # circle through all the angles and destroy 200 asteroids
        while True:
            for angle in angles:
                if len(visible[angle]) > 0:
                    _, last_destroyed = visible[angle].pop()
                    destroyed += 1
                if destroyed == 200:
                    break
            else:
                continue
            break

        return last_destroyed[0] * 100 + last_destroyed[1]
