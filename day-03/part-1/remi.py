from tool.runners.python import SubmissionPy


class RemiSubmission(SubmissionPy):
    def way(self, wire):
        points = [(0, 0)]
        for (d, dist) in wire:
            step = points[-1]
            for inter in range(1, dist + 1):
                (x, y) = step
                new_point = (0, 0)
                if d == "U":
                    new_point = (x, y + inter)
                elif d == "D":
                    new_point = (x, y - inter)
                elif d == "R":
                    new_point = (x + inter, y)
                elif d == "L":
                    new_point = (x - inter, y)
                points.append(new_point)

        return set(points[1:])

    def manhattan(self, point):
        return abs(point[0]) + abs(point[1])

    def run(self, s):
        [wire1, wire2] = [
            [(step[0], int(step[1:])) for step in wire.split(",")]
            for wire in s.split("\n")
        ]

        way1 = self.way(wire1)
        way2 = self.way(wire2)

        common = way1.intersection(way2)

        return min(self.manhattan(p) for p in common)
