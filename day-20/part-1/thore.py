from collections import deque, defaultdict
import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        maze, portals, start, end = parse_maze(s)

        return bfs(maze, portals, start, end)


def parse_maze(s):
    maze = s.splitlines()
    width = len(maze[0]) + 1

    portals_pos = defaultdict(list)
    for m in re.finditer("([A-Z][A-Z])\.", s):
        portals_pos[m.group(1)].append((m.end(1) // width, m.end(1) % width))
    for m in re.finditer("\.([A-Z][A-Z])", s):
        portals_pos[m.group(1)].append((m.start(0) // width, m.start(0) % width))
    for m in re.finditer(" ([A-Z])(?= )", s):
        x, y = (m.start(1) // width, m.start(1) % width)
        if x + 1 >= len(maze) or not maze[x + 1][y].isalpha():
            continue
        portal = m.group(1) + maze[x + 1][y]
        if x + 2 < len(maze) and maze[x + 2][y] == ".":
            portals_pos[portal].append((x + 2, y))
        else:
            portals_pos[portal].append((x - 1, y))

    portals = {}
    for portal, positions in portals_pos.items():
        if portal == "AA":
            start = positions[0]
            continue
        if portal == "ZZ":
            end = positions[0]
            continue
        portals[positions[0]] = positions[1]
        portals[positions[1]] = positions[0]

    return maze, portals, start, end


def bfs(maze, portals, start, end):
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        pos, dist = queue.popleft()

        if pos == end:
            return dist

        if pos in visited:
            continue

        for neighour in get_neighbours(maze, portals, pos):
            queue.append((neighour, dist + 1))

        visited.add(pos)


def get_neighbours(maze, portals, pos):
    x, y = pos
    if pos in portals:
        yield portals[pos]
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = (x + dx, y + dy)
        try:
            if maze[nx][ny] == ".":
                yield nx, ny
        except IndexError:
            continue
