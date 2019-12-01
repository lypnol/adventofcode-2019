from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        return sum(module_fuel(int(v)) for v in s.splitlines())


def module_fuel(mass):
    f = mass
    tot = 0
    while f > 8:
        f = f // 3 - 2
        tot += f
    return tot
