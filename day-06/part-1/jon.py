from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        parents = {}

        for l in s.strip().split("\n"):
            a, b = l.split(")")
            parents[b] = a

        dists = {"COM": 0}

        def dist(n):
            if n in dists:
                return dists[n]
            d = 1 + dist(parents[n])
            dists[n] = d
            return d

        return sum(dist(n) for n in parents.keys())

    # My initial solution, which is slower
    def run_slower(self, s):
        parents = {}

        for l in s.strip().split("\n"):
            a, b = l.split(")")
            parents[b] = a

        sum_dist = 0

        for node in parents.keys():
            n = node
            while n != "COM":
                n = parents[n]
                sum_dist += 1

        return sum_dist
