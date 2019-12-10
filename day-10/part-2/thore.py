from collections import deque
from math import atan2, isclose, pi

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        N_VAPORIZED = 200

        asteroids = parse_asteroids(s)
        _, sorted_visibilities = best_monitoring_location(asteroids)

        visibilities = deque(sorted_visibilities)
        visibilities.popleft()
        for n_vaporized in range(N_VAPORIZED - 1):
            angle, _, _ = visibilities.popleft()  # vaporization

            while isclose(visibilities[0][0], angle):  # behind vaporized asteroid
                visibilities.rotate(-1)

        vaporized_200th = visibilities[0][2]
        return vaporized_200th[1] * 100 + vaporized_200th[0]


def parse_asteroids(map_string, asteroid_char="#"):
    asteroids = set()
    for i, line in enumerate(map_string.splitlines()):
        asteroids.update([(i, j) for j in range(len(line)) if line[j] == asteroid_char])
    return list(asteroids)


def best_monitoring_location(asteroids):
    n_asteroids = len(asteroids)

    angles = [[-1 for j in range(n_asteroids)] for i in range(n_asteroids)]
    distances = [[-1 for j in range(n_asteroids)] for i in range(n_asteroids)]

    for i in range(n_asteroids):
        for j in range(i + 1, n_asteroids):
            angles[i][j] = angle(asteroids[i], asteroids[j])
            angles[j][i] = (angles[i][j] + 180) % 360
            distances[i][j] = dist_sq(asteroids[i], asteroids[j])
            distances[j][i] = distances[i][j]

    best_n_visible = -1
    best_asteroid = None
    best_sorted_visibilities = None
    for i in range(n_asteroids):
        sorted_visibilities = sorted(zip(angles[i], distances[i], asteroids))

        n_visible = 0
        for j in range(1, n_asteroids):
            if not isclose(sorted_visibilities[j][0], sorted_visibilities[j - 1][0]):
                n_visible += 1

        if n_visible > best_n_visible:
            best_n_visible = n_visible
            best_asteroid = asteroids[i]
            best_sorted_visibilities = sorted_visibilities

    return best_asteroid, best_sorted_visibilities


def angle(a, b):
    """ Compute oriented angle (in degrees) between "up" axis and AB.
        a and b coordinates are from a top-left origin """
    ab_vec = (b[1] - a[1], a[0] - b[0])  # vector with bottom-right origin
    res = atan2(*ab_vec) * 180 / pi  # angle with yaxis in [-180, 180]
    if res < 0:  # from [-180, 180] to [0, 360]
        res += 360
    return res


def dist_sq(a, b):
    """ Compute euclidean distance between two points """
    return sum([(xa - xb) ** 2 for xa, xb in zip(a, b)])
