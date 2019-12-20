from collections import deque, defaultdict
import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        maze, portals, start, end = parse_maze(s)

        return bfs(maze, portals, (*start, 0), (*end, 0))


def parse_maze(s):
    portals = get_portals(s)
    maze = s.splitlines()

    portals_links = {}
    for portal, positions in portals.items():
        if portal == "AA":
            start = positions[0][:2]
            continue
        if portal == "ZZ":
            end = positions[0][:2]
            continue
        assert len(positions) == 2
        x0, y0, is_outer0 = positions[0]
        x1, y1, is_outer1 = positions[1]
        portals_links[(x0, y0)] = (x1, y1, -1 if is_outer0 else 1)
        portals_links[(x1, y1)] = (x0, y0, -1 if is_outer1 else 1)

    return maze, portals_links, start, end


def get_portals(s):
    maze = s.splitlines()
    width = len(maze[0]) + 1

    portals = defaultdict(list)

    for m in re.finditer("([A-Z][A-Z])\.", s):
        x, y = m.end(1) // width, m.end(1) % width
        is_outer = y - 2 == 0
        portals[m.group(1)].append((x, y, is_outer))

    for m in re.finditer("\.([A-Z][A-Z])", s):
        x, y = m.start(0) // width, m.start(0) % width
        is_outer = y + 2 == width - 2
        portals[m.group(1)].append((x, y, is_outer))

    for m in re.finditer(" ([A-Z])(?= )", s):
        x, y = (m.start(1) // width, m.start(1) % width)

        if x + 1 >= len(maze) or not maze[x + 1][y].isalpha():
            continue

        portal = m.group(1) + maze[x + 1][y]
        if x + 2 < len(maze) and maze[x + 2][y] == ".":
            is_outer = x == 0
            portals[portal].append((x + 2, y, is_outer))
        else:
            is_outer = x + 1 == len(maze) - 1
            portals[portal].append((x - 1, y, is_outer))

    return portals


def bfs(maze, portals, start, end):
    queue = deque([(start, 0)])
    visited = set()

    while queue:
        pos, dist = queue.popleft()

        if pos in visited:
            continue
        else:
            visited.add(pos)

        if pos == end:
            return dist

        for neighbour in get_neighbours(maze, portals, pos):
            if neighbour not in visited:
                queue.append((neighbour, dist + 1))

    raise ValueError("End not found")


def get_neighbours(maze, portals, pos):
    x, y, level = pos

    if (x, y) in portals:
        new_x, new_y, delta_level = portals[(x, y)]
        if level + delta_level >= 0:  # not outermost level
            yield new_x, new_y, level + delta_level

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = (x + dx, y + dy)
        try:
            if maze[nx][ny] == ".":
                yield nx, ny, level
        except IndexError:
            continue
