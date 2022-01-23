from tool.runners.python import SubmissionPy


def compute_fuel(mass):
    fuel = mass // 3 - 2
    if fuel <= 0:
        return 0
    return fuel + compute_fuel(fuel)


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        return sum(compute_fuel(int(mass)) for mass in s.splitlines())
