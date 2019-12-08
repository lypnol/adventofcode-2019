from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        orbiting = {}
        for orb in s.splitlines():
            a, b = orb.strip().split(')')
            orbiting[b] = a

        you_dist_counts = {}
        cur = 'YOU'
        c = -1
        while cur in orbiting:
            you_dist_counts[cur] = c
            c += 1
            cur = orbiting[cur]

        cur = 'SAN'
        c = -1
        while cur in orbiting:
            if cur in you_dist_counts:
                return c + you_dist_counts[cur]
            c += 1
            cur = orbiting[cur]

        return -1
