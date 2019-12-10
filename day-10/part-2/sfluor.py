from collections import defaultdict
import itertools
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


sup = 10000


def compute_angle(x, y):
    # Fake angle fast computation
    if x == 0:
        return sup * int(1 if y > 0 else -1)

    if y == 0:
        if x > 0:
            return 0
        else:
            return 2 * sup

    # x > 0 and (y < 0 or y > 0)
    if x > 0:
        return y / x

    # y > 0, x < 0
    if y > 0:
        return sup - (y / x)
    # y < 0 and x < 0
    else:
        return 2 * sup + (y / x)


def intersections(center, asteroids):
    d = {}
    points = []

    c_x, c_y = center

    for (x, y) in asteroids:
        if x == c_x and y == c_y:
            continue

        v_x = x - c_x
        v_y = y - c_y

        # PGCD to normalize so we ensure we stay in Z
        norm = pgcd(abs(v_x), abs(v_y))

        pseudo_angle = compute_angle(v_x, v_y)

        data = (pseudo_angle, (v_x, v_y))
        d[(v_x // norm, v_y // norm)] = 1
        points.append(data)

    return d, points


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        asteroids = list(parse_asteroids(s))

        ins = ((a, *intersections(a, asteroids)) for a in asteroids)

        maxi = max(
            ((len(i), a, i, points) for (a, i, points) in ins), key=lambda l: l[0]
        )
        # maxi = [(len(i), a, i, points) for (a, i, points) in ins if a == (8, 3)][0]
        _, center, _, points = maxi

        # Create buckets per angle
        buckets = {}

        angles = []

        for angle, point in points:
            if not angle in buckets:
                buckets[angle] = [point]
                angles.append(angle)
            else:
                buckets[angle].append(point)

        # Sort buckets by manhattan distance to center
        for angle, bucket in buckets.items():
            buckets[angle] = sorted(bucket, key=lambda p: abs(p[0]) + abs(p[1]))

        # Sort angles
        angles = sorted(angles)

        count = 0

        def orig(point):
            x, y = point
            return (x + center[0], y + center[1])

        for angle in itertools.cycle(angles):
            points = buckets[angle]

            if not points:
                continue

            count += 1
            p = points.pop(0)

            if count == 200:
                x, y = orig(p)
                return y + 100 * x
