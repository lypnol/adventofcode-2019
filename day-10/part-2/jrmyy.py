import math
from typing import Tuple, Dict

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        ast_map = {}
        asteroids = []
        for row_num, row in enumerate(s.splitlines()):
            for col_num, value in enumerate(list(row)):
                pos = (col_num, row_num)
                if value == "#":
                    asteroids.append(pos)
                ast_map[pos] = value

        station, seen_asteroids = max(
            [(x, [y for y in asteroids if y != x and self.can_see(x, y, ast_map)]) for x in asteroids],
            key=lambda t: len(t[1])
        )
        angles = [(self.get_angle(station, ast), ast) for ast in seen_asteroids]
        seq_angles = {}
        for angle, ast in angles:
            if angle in seq_angles:
                seq_angles[angle].append(ast)
            else:
                seq_angles[angle] = [ast]

        list_angles = sorted([
            (k, sorted(v, key=lambda coord: math.sqrt((coord[1] - station[1]) ** 2 + (coord[0] - station[0]) ** 2)))
            for k, v in seq_angles.items()
        ], key=lambda t: t[0])

        j = 0
        for i in range(199):
            list_angles[j][1].pop()
            j = (j + 1) % len(list_angles)

        res = list_angles[j][1].pop()
        return res[0] * 100 + res[1]

    def get_angle(self, station: Tuple[int, int], asteroid: Tuple[int, int]):
        x1, y1 = asteroid
        x2, y2 = station
        res = math.atan2(x1 - x2,  y2 - y1) * 180 / math.pi
        if res < 0:
            res += 360
        return res

    def can_see(self, x: Tuple[int, int], y: Tuple[int, int], ast_map: Dict[Tuple[int, int], str]) -> int:
        x1, y1 = x
        x2, y2 = y

        if y1 == y2:
            return int(all(
                [ast_map[i, y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))]
            ))

        if x1 == x2:
            return int(all(
                [ast_map[x1, i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))]
            ))

        delta_x, delta_y = x2 - x1, y2 - y1
        steps = math.gcd(delta_x, delta_y)
        if steps == 1:
            return 1

        for i in range(1, steps):
            if ast_map[(x1 + delta_x // steps * i, y1 + delta_y // steps * i)] == "#":
                return 0
        return 1
