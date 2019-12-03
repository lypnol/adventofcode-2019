from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        total_required_fuel = 0
        for line in s.splitlines():
            module_mass = int(line)
            total_required_fuel += self.required_fuel(module_mass)
        return total_required_fuel

    @classmethod
    def required_fuel(cls, mass):
        fuel = mass // 3 - 2

        if fuel <= 0:
            return 0

        return fuel + cls.required_fuel(fuel)
