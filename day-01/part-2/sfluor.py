from tool.runners.python import SubmissionPy


class SfluorSubmission(SubmissionPy):

    def fuel(self, mass):
        if mass // 3 <= 2:
            return 0

        f = ((mass // 3) - 2)
        return f + self.fuel(f)

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        return sum([self.fuel(int(m)) for m in s.split("\n")])
