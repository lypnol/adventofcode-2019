from tool.runners.python import SubmissionPy

from math import gcd


class RemiSubmission(SubmissionPy):
    def run(self, s):
        asteroids = []
        for i, line in enumerate(s.split("\n")):
            for j, ch in enumerate(list(line)):
                if ch == "#":
                    asteroids.append((i, j))

        visibles = {}

        for (i1, j1) in asteroids:
            visibles[(i1, j1)] = set()
            for (i2, j2) in asteroids:
                if i1 == i2 and j1 == j2:
                    continue
                angle = (i2 - i1, j2 - j1)
                pgcd = gcd(angle[0], angle[1])
                angle = (angle[0] // pgcd, angle[1] // pgcd)
                visibles[(i1, j1)].add(angle)

        m = max(
            (asteroid for asteroid in visibles.keys()),
            key=lambda asteroid: len(visibles[asteroid]),
        )
        return len(visibles[m])

