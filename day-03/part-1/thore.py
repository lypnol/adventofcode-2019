from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def wire_positions(self, s):
        x, y = 0, 0
        positions = set()
        for ins in s.split(","):
            if ins[0] == "R":
                length = int(ins[1:])
                positions.update([(x + i, y) for i in range(1, length + 1)])
                x += length
            elif ins[0] == "L":
                length = int(ins[1:])
                positions.update([(x - i, y) for i in range(1, length + 1)])
                x -= length
            elif ins[0] == "U":
                length = int(ins[1:])
                positions.update([(x, y + i) for i in range(1, length + 1)])
                y += length
            elif ins[0] == "D":
                length = int(ins[1:])
                positions.update([(x, y - i) for i in range(1, length + 1)])
                y -= length
        return positions

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        wire_1, wire_2 = [self.wire_positions(path) for path in s.splitlines()]
        intersections = wire_1 & wire_2
        return min([abs(x) + abs(y) for x, y in intersections])
