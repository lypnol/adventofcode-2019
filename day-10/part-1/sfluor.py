from functools import lru_cache
from tool.runners.python import SubmissionPy


def parse_asteroids(s):
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                yield (x, y)


@lru_cache(maxsize=None)
def pgcd(a, b):
    if b == 0:
        return a

    r = a % b
    return pgcd(b, r)


def count_intersections(center, asteroids):
    d = {}

    c_x, c_y = center

    for (x, y) in asteroids:
        if x == c_x and y == c_y:
            continue

        v_x = x - c_x
        v_y = y - c_y

        # PGCD to normalize so we ensure we stay in Z
        norm = pgcd(abs(v_x), abs(v_y))
        d[(v_x // norm, v_y // norm)] = 1

    return len(d)


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        asteroids = list(parse_asteroids(s))

        return max(count_intersections(a, asteroids) for a in asteroids)
