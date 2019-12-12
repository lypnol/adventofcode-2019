from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        coords = set({})
        for j, line in enumerate(s.splitlines()):
            for i in range(len(line)):
                if line[i] == "#":
                    coords.add((i, j))
        counts = set()
        for mon in coords:
            lines = set()
            for ast in coords:
                if ast == mon:
                    continue
                if ast[0] == mon[0]:
                    m = 1000000
                    dir = (ast[1] - mon[1]) / abs(ast[1] - mon[1])
                else:
                    m = (ast[1] - mon[1]) / (ast[0] - mon[0])
                    dir = (ast[0] - mon[0]) / abs(ast[0] - mon[0])
                lines.add((m, dir))
            counts.add(len(lines))
        return max(counts)
