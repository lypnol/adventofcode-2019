from tool.runners.python import SubmissionPy
import math


class JonSubmission(SubmissionPy):

    def run(self, s):

        lines = s.strip().split("\n")
        h = len(lines)
        w = len(lines[0])

        asteroids = [(x, y) for x in range(w) for y in range(h) if lines[y][x] == "#"]

        max_visible = 0

        for bx, by in asteroids:
            visible = set()
            for tx, ty in asteroids:
                if (bx, by) != (tx, ty):
                    dx, dy = tx - bx, ty - by
                    g = math.gcd(dx, dy)
                    visible.add((dx // g, dy // g))
            max_visible = max(max_visible, len(visible))

        return max_visible
