from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        parents = {}

        for l in s.strip().split("\n"):
            a, b = l.split(")")
            parents[b] = a

        def ancestors(n):
            if n == "COM":
                return []
            p = parents[n]
            return ancestors(p) + [p]

        a1 = ancestors("YOU")
        a2 = ancestors("SAN")

        common = 0
        while a1[common] == a2[common]:
            common += 1

        return len(a1) + len(a2) - 2*common
