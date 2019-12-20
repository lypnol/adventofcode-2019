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
    portals = get_portals(s)
    maze = s.splitlines()

    portals_links = {}
    for portal, positions in portals.items():
        if portal == "AA":
            start = positions[0]
            continue
        if portal == "ZZ":
            end = positions[0]
            continue
        assert len(positions) == 2
        portals_links[positions[0]] = positions[1]
        portals_links[positions[1]] = positions[0]

    return maze, portals_links, start, end


def get_portals(s):
    maze = s.splitlines()
    width = len(maze[0]) + 1

    portals = defaultdict(list)

    for m in re.finditer("([A-Z][A-Z])\.", s):
        portals[m.group(1)].append((m.end(1) // width, m.end(1) % width))

    for m in re.finditer("\.([A-Z][A-Z])", s):
        portals[m.group(1)].append((m.start(0) // width, m.start(0) % width))

    for m in re.finditer(" ([A-Z])(?= )", s):
        x, y = (m.start(1) // width, m.start(1) % width)

        if x + 1 >= len(maze) or not maze[x + 1][y].isalpha():
            continue

        portal = m.group(1) + maze[x + 1][y]
        if x + 2 < len(maze) and maze[x + 2][y] == ".":
            portals[portal].append((x + 2, y))
        else:
            portals[portal].append((x - 1, y))

    return portals


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
