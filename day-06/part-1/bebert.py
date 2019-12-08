from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        orbiting = {}
        for orb in s.splitlines():
            a, b = orb.strip().split(')')
            orbiting[b] = a

        orb_counts = {}
        for b in orbiting:
            cur = b
            c = 0
            while cur in orbiting:
                c += 1
                cur = orbiting[cur]
            orb_counts[b] = c

        return sum(orb_counts.values())
