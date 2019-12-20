from tool.runners.python import SubmissionPy


from collections import defaultdict, deque
import heapq

INSIDE, OUTSIDE = 0, 1


def parse_doors(lines):
    doors = {}

    # top/outside
    for i in range(len(lines[0])):
        if lines[0][i] != " ":
            doors[(2, i)] = OUTSIDE, f"{lines[0][i]}{lines[1][i]}"

    # bottom/outside
    for i in range(len(lines[0])):
        if lines[-2][i] != " ":
            doors[(len(lines) - 3, i)] = OUTSIDE, f"{lines[-2][i]}{lines[-1][i]}"

    # left/outside
    for i in range(len(lines) - 1):
        if lines[i][0] != " ":
            doors[(i, 2)] = OUTSIDE, f"{lines[i][0]}{lines[i][1]}"

    # right/outside
    for i in range(len(lines) - 1):
        if lines[i][-1] != " ":
            doors[(i, len(lines[0]) - 3)] = OUTSIDE, f"{lines[i][-2]}{lines[i][-1]}"

    # inside size
    middle = len(lines[0]) // 2
    top = 2
    bottom = len(lines) - 4
    while lines[top][middle] in ["#", "."]:
        top += 1
    while lines[bottom][middle] in ["#", "."]:
        bottom -= 1

    middle = len(lines) // 2
    left = 2
    right = len(lines[0]) - 3
    while lines[middle][left] in ["#", "."]:
        left += 1
    while lines[middle][right] in ["#", "."]:
        right -= 1

    # top/inside
    for i in range(left, right + 1):
        if lines[top][i] != " ":
            doors[(top - 1, i)] = INSIDE, f"{lines[top][i]}{lines[top+1][i]}"

    # bottom/inside
    for i in range(left, right + 1):
        if lines[bottom][i] != " ":
            doors[(bottom + 1, i)] = INSIDE, f"{lines[bottom-1][i]}{lines[bottom][i]}"

    # left/inside
    for i in range(top, bottom + 1):
        if lines[i][left] != " ":
            doors[(i, left - 1)] = INSIDE, f"{lines[i][left]}{lines[i][left+1]}"

    # right/inside
    for i in range(top, bottom + 1):
        if lines[i][right] != " ":
            doors[(i, right + 1)] = INSIDE, f"{lines[i][right-1]}{lines[i][right]}"

    return doors


def adj_positions(pos):
    return [
        tuple(a + b for a, b in zip(pos, delta))
        for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ]


def reduce_maze(lines):
    doors = parse_doors(lines)
    adj = dict()

    def bfs(start):
        q = deque([(start, 0)])
        seen = set([start])
        while q:
            pos, distance = q.popleft()
            if pos != start and pos in doors:
                adj[doors[start]][doors[pos]] = distance

            for next_pos in adj_positions(pos):
                if lines[next_pos[0]][next_pos[1]] != ".":
                    continue
                if next_pos in seen:
                    continue
                seen.add(next_pos)

                q.append((next_pos, distance + 1))

    for start, door in doors.items():
        adj[door] = dict()
        bfs(start)

    return adj


def solve_part1(lines):
    adj = reduce_maze(lines)

    start = "AA"
    end = "ZZ"

    q = [(0, (OUTSIDE, start))]
    seen = set([(INSIDE, start)])
    while True:
        distance, pos = heapq.heappop(q)
        if pos in seen:
            continue
        seen.add(pos)

        if pos == (OUTSIDE, end):
            return distance

        (side, code) = pos
        other_side = (side + 1) % 2

        # go through door
        if (other_side, code) not in seen:
            heapq.heappush(q, (distance + 1, (other_side, code)))

        # regular move
        for next_pos, distance_pos in adj[pos].items():
            if next_pos in seen:
                continue

            heapq.heappush(q, (distance + distance_pos, next_pos))


class FranciscoSubmission(SubmissionPy):
    def run(self, s):
        return solve_part1(s.split("\n"))
