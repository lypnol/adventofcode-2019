from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        lines = s.strip().split("\n")

        pos = []
        for l in lines:
            pos.append([int(p.strip().split("=")[1]) for p in l.strip("<>").split(",")])

        n = len(pos)
        dim = len(pos[0])

        vel = [[0]*dim for _ in range(n)]

        for _ in range(1000):

            for i in range(n):
                for j in range(i+1, n):

                    for d in range(dim):

                        xi = pos[i][d]
                        xj = pos[j][d]
                        if xi < xj:
                            vel[i][d] += 1
                            vel[j][d] -= 1
                        elif xj < xi:
                            vel[i][d] -= 1
                            vel[j][d] += 1

            for i in range(n):
                for d in range(dim):
                    pos[i][d] += vel[i][d]

        return sum(sum(abs(v) for v in pos[i]) * sum(abs(v) for v in vel[i]) for i in range(n))

