from functools import lru_cache
import re
from collections import deque
import heapq

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
        world = s
        all_keys, doors, start = find_keys_and_doors(world)
        world = world.splitlines()
        distance = get_distance_fun(world)

        queue = [(0, start, frozenset())]
        visited = set()

        while len(queue) > 0:
            dist, pos, keys = heapq.heappop(queue)
            # print(dist, pos, keys)

            if len(keys) == len(all_keys):
                return dist

            if (pos, keys) in visited:
                continue

            visited.add((pos, keys))

            for key, key_pos, key_dist in get_accessible_keys(
                world, all_keys, pos, keys, distance
            ):
                heapq.heappush(
                    queue, (dist + key_dist, key_pos, keys | frozenset([key]))
                )

        return -1


def get_accessible_keys(world, all_keys, pos, keys, distance_func):
    for key in set(all_keys.keys()) - keys:
        dist_to_key, keys_needed = distance_func(pos, all_keys[key])
        # print(pos, keys, key, all_keys[key], dist_to_key, keys_needed)
        if dist_to_key >= 0 and keys_needed.issubset(keys):
            yield key, all_keys[key], dist_to_key


def collect_keys(world):
    remaining_keys, doors, start = find_keys_and_doors(world)
    world = world.splitlines()
    distance = get_distance_fun(world)

    def collect(pos):
        collect.counter += 1
        # if collect.counter % 100 == 0:
        #     print(collect.counter)
        if len(remaining_keys) == 0:
            return 0, []

        res = float("inf")
        best_key = None
        best_path = []
        for key, key_pos in list(remaining_keys.items()):
            dist_to_key, keys_needed = distance(pos, key_pos)
            # print(f"from={pos} to={keys[key]} dist={d_to_key} doors={keys_needed}")
            if dist_to_key == -1 or len(keys_needed & set(remaining_keys.keys())) > 0:
                # print(
                #     f"Cannot get {key} from {pos}, don't have {keys.keys()} : need {keys_needed & set(keys.keys())}"
                # )
                continue  # cannot reach this key
            # else:
            # print(
            #     f"Can get {key} from {pos}, don't have {keys.keys()} : need {keys_needed}"
            # )

            # print("Taking key", key)
            remaining_keys.pop(key)
            # print("***", collect(key_pos))
            dist_remaining, path = collect(key_pos)
            if dist_to_key + dist_remaining < res:
                res = dist_to_key + dist_remaining
                best_key = key
                best_path = [key] + path
            remaining_keys[key] = key_pos
        # print(
        #     f"remaining_keys={keys.keys()} dist={res} pos={pos} best_path={best_path}"
        # )
        return res, best_path

    collect.counter = 0
    return collect(start)


def get_distance_fun(world):
    @lru_cache(maxsize=None)
    def distance(frm, to):
        # print(f"*** Called distance({frm}, {to})")
        queue = deque([(frm, 0, set())])
        visited = set()
        while len(queue) != 0:
            pos, dist, keys_needed = queue.popleft()
            if pos == to:
                # print("Found")
                return dist, keys_needed
            if pos in visited:
                continue
            for n in get_neighbours(world, pos):
                if world[n[0]][n[1]].isalpha() and world[n[0]][n[1]].isupper():
                    key = world[n[0]][n[1]].lower()
                    keys_needed = keys_needed | set(key)
                queue.append((n, dist + 1, keys_needed))
            visited.add(pos)

        return -1, set()

    return distance


def get_neighbours(world, pos):
    neighbours = []
    for (i, j) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        try:
            if (
                world[pos[0] + i][pos[1] + j] == EMPTY
                or world[pos[0] + i][pos[1] + j].isalpha()
                or world[pos[0] + i][pos[1] + j] == "@"
            ):
                neighbours.append((pos[0] + i, pos[1] + j))
        except:
            continue
    # print("Neighbours of", pos, ":", neighbours)
    return neighbours


def find_keys_and_doors(world):
    width = len(world.splitlines()[0]) + 1
    keys = {
        m[0]: (m.start() // width, m.start() % width)
        for m in re.finditer(KEY_PATTERN, world)
    }
    doors = {
        m[0]: (m.start() // width, m.start() % width)
        for m in re.finditer(DOOR_PATTERN, world)
    }
    start_idx = world.find(START)
    start = (start_idx // width, start_idx % width)
    return keys, doors, start

