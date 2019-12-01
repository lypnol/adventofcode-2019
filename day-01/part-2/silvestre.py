from tool.runners.python import SubmissionPy


class SilvestreSubmission(SubmissionPy):

    def run(self, s):

        def total_fuel(el):
            if el < 8:
                return 0
            else:
                fuel = el // 3 - 2
                return total_fuel(fuel) + fuel

        return sum(total_fuel(el) for el in map(int, s.split("\n")))
