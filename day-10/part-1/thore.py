from math import sqrt, isclose

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        asteroids = parse_asteroids(s)

        return best_monitoring_location(asteroids)[1]


def parse_asteroids(map_string, asteroid_char="#"):
    asteroids = set()
    for i, line in enumerate(map_string.splitlines()):
        asteroids.update([(i, j) for j in range(len(line)) if line[j] == asteroid_char])
    return asteroids


def best_monitoring_location(asteroids):
    best_asteroid = None
    best_n_visible = -1

    for asteroid in asteroids:
        n_visible_asteroids = 0

        for target in asteroids:
            if target == asteroid:
                continue
            is_visible = True

            for candidate in asteroids:
                if candidate == asteroid or candidate == target:
                    continue
                if is_between(asteroid, target, candidate):
                    is_visible = False
                    break

            n_visible_asteroids += int(is_visible)
            if n_visible_asteroids > best_n_visible:
                best_n_visible = n_visible_asteroids
                best_asteroid = asteroid

    return best_asteroid, best_n_visible


def is_between(src, target, candidate, eps=1e-8):
    return isclose(dist(src, candidate) + dist(candidate, target), dist(src, target))


def dist(a, b):
    return sqrt(sum([(xa - xb) ** 2 for xa, xb in zip(a, b)]))
