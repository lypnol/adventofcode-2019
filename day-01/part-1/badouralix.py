from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        modules = s.split("\n")
        rounded_third_mass = 0

        for module in modules:
            rounded_third_mass += int(module) // 3
        total_fuel = rounded_third_mass - 2 * len(modules)

        return total_fuel
