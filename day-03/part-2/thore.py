from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def wire_positions(self, s):
        x, y = 0, 0
        positions = set()
        steps = {}
        step = 0
        for ins in s.split(","):
            if ins[0] == "R":
                length = int(ins[1:])
                for i in range(1, length + 1):
                    positions.add((x + i, y))
                    steps[(x + i, y)] = step + i
                x += length
                step += length
            elif ins[0] == "L":
                length = int(ins[1:])
                for i in range(1, length + 1):
                    positions.add((x - i, y))
                    steps[(x - i, y)] = step + i
                x -= length
                step += length
            elif ins[0] == "U":
                length = int(ins[1:])
                for i in range(1, length + 1):
                    positions.add((x, y + i))
                    steps[(x, y + i)] = step + i
                y += length
                step += length
            elif ins[0] == "D":
                length = int(ins[1:])
                for i in range(1, length + 1):
                    positions.add((x, y - i))
                    steps[(x, y - i)] = step + i
                y -= length
                step += length
        return positions, steps

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        wire_1, wire_2 = [self.wire_positions(path) for path in s.splitlines()]
        intersections = wire_1[0] & wire_2[0]
        return min([wire_1[1][i] + wire_2[1][i] for i in intersections])
