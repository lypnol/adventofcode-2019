from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        wires = [{(0, 0): 0}, {(0, 0): 0}]
        cross = set()
        w1t, w2t = s.splitlines()
        w1 = w1t.strip().split(',')
        w2 = w2t.strip().split(',')
        for i, w in enumerate([w1, w2]):
            x, y, wl = 0, 0, 0
            for c in w:
                direction = c[0]
                step = int(c[1:])
                if direction == "U":
                    dx, dy = 0, 1
                elif direction == "D":
                    dx, dy = 0, -1
                elif direction == "R":
                    dx, dy = 1, 0
                else:  # direction == "L":
                    dx, dy = -1, 0

                for _ in range(step):
                    x, y = x + dx, y + dy
                    wl += 1
                    if (x, y) not in wires[i]:
                        wires[i][(x, y)] = wl
                    if i == 1 and wires[0].get((x, y)):
                        cross.add((x, y))

        min_cross = 1_000_000
        for x, y in cross:
            if wires[0][(x, y)] + wires[1][(x, y)] < min_cross:
                min_cross = wires[0][(x, y)] + wires[1][(x, y)]

        return min_cross
