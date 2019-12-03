from typing import List, Tuple

from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        wires_paths = [wire.split(",") for wire in s.splitlines()]
        first_path, second_path = [self._build_path(path) for path in wires_paths]
        intersections = set(first_path).intersection(set(second_path))
        return min(first_path.index(pos) + second_path.index(pos) + 2 for pos in intersections)

    def _build_path(self, path: List[str]) -> List[Tuple[int, int]]:
        x, y = 0, 0
        positions = []
        for step in path:
            direction = step[0]
            distance = int(step[1:])
            if direction == "U":
                positions.extend([(x, y - i) for i in range(1, distance + 1)])
                y -= distance
            elif direction == "D":
                positions.extend([(x, y + i) for i in range(1, distance + 1)])
                y += distance
            elif direction == "R":
                positions.extend([(x + i, y) for i in range(1, distance + 1)])
                x += distance
            else:
                positions.extend([(x - i, y) for i in range(1, distance + 1)])
                x -= distance
        return positions

