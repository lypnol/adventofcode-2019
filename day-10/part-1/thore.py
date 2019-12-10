from math import sqrt, isclose, pi, atan2

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        asteroids = parse_asteroids(s)

        return best_monitoring_location(asteroids)


def parse_asteroids(map_string, asteroid_char="#"):
    asteroids = set()
    for i, line in enumerate(map_string.splitlines()):
        asteroids.update([(i, j) for j in range(len(line)) if line[j] == asteroid_char])
    return list(asteroids)


def best_monitoring_location(asteroids):
    n_asteroids = len(asteroids)
    line_of_sights = [[0 for j in range(n_asteroids)] for i in range(n_asteroids)]
    angles = [[-1 for j in range(n_asteroids)] for i in range(n_asteroids)]

    for i in range(n_asteroids):
        for j in range(i + 1, n_asteroids):
            angles[i][j] = angle(asteroids[i], asteroids[j])
            angles[j][i] = (angles[i][j] + 180) % 360

    best_n_visible = -1
    for i in range(n_asteroids):
        sorted_angles = sorted(angles[i])
        n_visible = 0
        for j in range(1, n_asteroids):
            if not isclose(sorted_angles[j], sorted_angles[j - 1]):
                n_visible += 1
        if n_visible > best_n_visible:
            best_n_visible = n_visible

    return best_n_visible


def angle(a, b):
    """ Compute oriented angle (in degrees) between y axis and AB """
    ab_vec = (b[0] - a[0], b[1] - a[1])
    res = atan2(*ab_vec) * 180 / pi
    return res if res >= 0 else res + 360


def is_between(src, target, candidate, eps=1e-8):
    """ Check if candidate asteroid is between src and target """
    return isclose(dist(src, candidate) + dist(candidate, target), dist(src, target))


def dist(a, b):
    """ Compute euclidean distance between two points """
    return sqrt(sum([(xa - xb) ** 2 for xa, xb in zip(a, b)]))
