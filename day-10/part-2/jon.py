from tool.runners.python import SubmissionPy
import math


class JonSubmission(SubmissionPy):

    def run(self, s):

        lines = s.strip().split("\n")
        h = len(lines)
        w = len(lines[0])

        asteroids = [(x, y) for x in range(w) for y in range(h) if lines[y][x] == "#"]

        max_visible = 0
        sx, sy = 0, 0  # station

        for bx, by in asteroids:  # base
            visible = set()
            for tx, ty in asteroids:  # target
                if (bx, by) != (tx, ty):
                    dx, dy = tx - bx, ty - by
                    g = math.gcd(dx, dy)
                    visible.add((dx // g, dy // g))
            if len(visible) > max_visible:
                max_visible = len(visible)
                sx, sy = bx, by

        if max_visible < 200:
            raise Exception("Will need multiple rounds")

        svisibles = {}
        for tx, ty in asteroids:
            if (tx, ty) != (sx, sy):
                dx, dy = tx - sx, ty - sy
                g = math.gcd(dx, dy)
                ncoords = (dx // g, dy // g)
                if ncoords in svisibles:
                    prev_g, _ = svisibles[ncoords]
                    if g > prev_g:
                        continue
                svisibles[ncoords] = (g, (tx, ty))

        ordered = []

        for _, (tx, ty) in svisibles.values():
            dx, dy = tx - sx, ty - sy

            if dx >= 0 and dy < 0:  # First
                order = (1, -dx/dy)
            elif dx > 0 and dy >= 0:  # Second
                order = (2, dy/dx)
            elif dx <= 0 and dy > 0:  # Third
                order = (3, -dx/dy)
            elif dx < 0 and dy <= 0:  # Fourth
                order = (4, dy/dx)
            else:
                raise Exception("Unclassified {}, {}".format(dx, dy))

            ordered.append((order, (tx, ty)))

        ordered.sort()

        _, (rx, ry) = ordered[199]

        return 100 * rx + ry
