from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        return sum(self.get_fuel(int(x)) for x in s.splitlines())

    def get_fuel(self, i: int, fuel_sum: int = 0) -> int:
        fuel_res = int(i) // 3 - 2
        if fuel_res < 0:
            return fuel_sum
        else:
            return self.get_fuel(fuel_res, fuel_sum + fuel_res)
