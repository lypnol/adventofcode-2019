import math
from typing import Tuple, Dict

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        ast_map = {}
        asteroids = []
        for row_num, row in enumerate(s.splitlines()):
            for col_num, value in enumerate(list(row)):
                pos = (col_num, row_num)
                if value == "#":
                    asteroids.append(pos)
                ast_map[pos] = value

        return max([sum([self.can_see(x, y, ast_map) for y in asteroids if y != x]) for x in asteroids])

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
