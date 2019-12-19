from collections import deque
import heapq
import re

from tool.runners.python import SubmissionPy

WALL = "#"
EMPTY = "."
START = "@"
KEY_PATTERN = "[a-z]"
DOOR_PATTERN = "[A-Z]"


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        return solve_part1(s)


def solve_part1(s):
    all_keys, start = find_keys_and_start(s)
    world = s.splitlines()

    dist_comp = DistanceComputer(world)
    get_distance = dist_comp.distance

    def get_accessible_new_keys(pos, keys):
        for key in set(all_keys.keys()) - keys:
            key_pos = all_keys[key]
            dist_to_key, keys_needed = get_distance(pos, key_pos)
            if dist_to_key >= 0 and len(keys_needed & keys) == len(keys_needed):
                yield key, key_pos, dist_to_key

    # Dijsktra on (pos, keys) graph
    queue = [(0, start, frozenset())]
    visited = set()

    while len(queue) > 0:
        dist, pos, keys = heapq.heappop(queue)

        if len(keys) == len(all_keys):
            return dist

        if (pos, keys) in visited:
            continue

        for key, key_pos, key_dist in get_accessible_new_keys(pos, keys):
            heapq.heappush(queue, (dist + key_dist, key_pos, keys | frozenset([key])))

        visited.add((pos, keys))

    return -1


def find_keys_and_start(world):
    width = len(world.splitlines()[0]) + 1
    keys = {
        m[0]: (m.start() // width, m.start() % width)
        for m in re.finditer(KEY_PATTERN, world)
    }
    start_idx = world.find(START)
    start = (start_idx // width, start_idx % width)
    return keys, start


class DistanceComputer:
    """" Helper class to cache neighbours and distances computations """

    def __init__(self, world):
        self.world = world
        self.distances = {}
        self.neighbours = {}

    def distance(self, frm, to):
        """ Return distance between frm and to using BFS """
        if (frm, to) in self.distances:
            return self.distances[(frm, to)]

        queue = deque([(frm, 0, set())])
        visited = set()
        while len(queue) != 0:
            pos, dist, keys_needed = queue.popleft()
            if pos in visited:
                continue
            else:
                self.distances[(frm, pos)] = (dist, keys_needed)
                self.distances[(pos, frm)] = (dist, keys_needed)
            if pos == to:
                return self.distances[(frm, pos)]
            for x, y in self.get_neighbours(pos):
                if self.world[x][y].isalpha() and self.world[x][y].isupper():
                    key = self.world[x][y].lower()
                    keys_needed = keys_needed | set(key)
                queue.append(((x, y), dist + 1, keys_needed))

            visited.add(pos)

        return -1, set()

    def get_neighbours(self, pos):
        if pos in self.neighbours:
            return self.neighbours[pos]

        neighbours = []
        for (i, j) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            try:
                if (
                    self.world[pos[0] + i][pos[1] + j] == EMPTY
                    or self.world[pos[0] + i][pos[1] + j].isalpha()
                    or self.world[pos[0] + i][pos[1] + j] == "@"
                ):
                    neighbours.append((pos[0] + i, pos[1] + j))
            except:
                continue

        self.neighbours[pos] = neighbours
        return self.neighbours[pos]
