from tool.runners.python import SubmissionPy


from string import ascii_lowercase, ascii_uppercase
import heapq
from collections import defaultdict, deque


def next_positions(pos):
    return [
        tuple(x + y for x, y in zip(pos, delta))
        for delta in [(1, 0), (-1, 0), (0, -1), (0, 1)]
    ]


def reduce_maze(maze):
    """
    This function returns a adjacency matrix representing the tree-like structure of the
    maze.

    It only contains the initial position(s), the keys and the doors.

    There is an edge between 2 given vertices x and y, iff one can go from x to y in the
    maze without passing through another key / door.

    This function is mainly used to quickly figure out which keys are accessible or not.
    """
    q = deque()
    seen = set()
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in ["@", "1", "2", "3", "4"]:
                q.append(((i, j), None))
                seen.add((i, j))

    reduced_maze = defaultdict(set)

    while q:
        pos, pred = q.popleft()
        current = maze[pos[0]][pos[1]]
        if current not in ["#", "."]:
            if pred is not None:
                reduced_maze[pred].add(current)
                reduced_maze[current].add(pred)
            pred = current

        for next_pos in next_positions(pos):
            if maze[next_pos[0]][next_pos[1]] == "#" or next_pos in seen:
                continue
            seen.add(next_pos)
            q.append((next_pos, pred))

    return dict(reduced_maze)


def get_accessible_keys(reduced_maze, keys, pos="@"):
    """
    Uses the reduced maze to quickly figure out which keys are accessible from a given
    position.
    """
    q = deque([pos])
    seen = set()
    accessible = set()

    while q:
        pos = q.popleft()
        if pos in ascii_lowercase:
            accessible.add(pos)
        for next_pos in reduced_maze[pos]:
            if next_pos in seen:
                continue
            seen.add(next_pos)
            if next_pos in ascii_uppercase and next_pos.lower() not in keys:
                continue
            q.append(next_pos)

    return accessible


def compute_distances(maze):
    """
    Returns a matrix of distances between all the points of interest.
    d[x][y] is the distance of the only path that goes from x to y by only passing
    through keys and doors.
    """
    positions = {}

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] not in ["#", "."]:
                positions[maze[i][j]] = (i, j)

    def dfs(pos):
        q = deque([(pos, 0)])
        seen = {pos}
        distances = {}

        while q:
            pos, distance = q.popleft()
            current = maze[pos[0]][pos[1]]
            if current not in ["#", "."] and not current.isupper():
                distances[current] = distance

            for next_pos in next_positions(pos):
                if maze[next_pos[0]][next_pos[1]] == "#":
                    continue
                if next_pos in seen:
                    continue
                seen.add(next_pos)
                q.append((next_pos, distance + 1))

        return distances

    return positions, {key: dfs(pos) for key, pos in positions.items()}


def solve_part1(maze):
    # Dijkstra-like algorithm

    maze = maze.strip().split("\n")
    positions, distances = compute_distances(maze)
    reduced_maze = reduce_maze(maze)

    total_keys = len([s for s in positions if s in ascii_lowercase])

    q = [(0, ("@"), frozenset())]
    seen = set()

    while q:
        distance, pos, keys = heapq.heappop(q)

        if len(keys) == total_keys:
            return distance

        if (pos, keys) in seen:
            continue
        seen.add((pos, keys))

        for next_pos in get_accessible_keys(reduced_maze, keys) - keys:
            next_keys = (
                keys | frozenset([next_pos]) if next_pos in ascii_lowercase else keys
            )
            heapq.heappush(
                q, (distance + distances[pos][next_pos], next_pos, next_keys)
            )


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part1(s)
