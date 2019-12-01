from tool.runners.python import SubmissionPy


class LudogeSubmission(SubmissionPy):
    def compute_requirement(self, n):
        new_fuel = n // 3 - 2
        total_fuel = 0
        while new_fuel > 0:
            total_fuel += new_fuel
            new_fuel = new_fuel // 3 - 2
        return total_fuel

    def run(self, s):
        return sum(self.compute_requirement(int(line)) for line in s.split())
