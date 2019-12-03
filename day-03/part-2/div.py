from tool.runners.python import SubmissionPy


class DivSubmission(SubmissionPy):

    def build_path(self, moves, start):
        path = [start]
        x, y = start
        for m in moves:
            d = m[0]
            l = int(m[1:])
            if d == "D":
                for i in range(l):
                    y -= 1
                    path.append((x,y))
            elif d == "U":
                for i in range(l):
                    y += 1
                    path.append((x,y))
            elif d == "R":
                for i in range(l):
                    x += 1
                    path.append((x,y))
            elif d == "L":
                for i in range(l):
                    x -= 1
                    path.append((x,y))
        return path

    def run(self, s):
        wires = [l.split(",") for l in s.splitlines()]
        start_pos = (0,0)

        path1, path2 = [self.build_path(w, start_pos) for w in wires]

        intersection = set(path1[1:]) & set(path2[1:])

        scores = set()
        for pos in intersection:
            scores.add(path1.index(pos) + path2.index(pos))

        return min(scores)
