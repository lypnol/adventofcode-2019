from tool.runners.python import SubmissionPy


class SfluorSubmission(SubmissionPy):

    def fuel(self, mass):
        return ((mass // 3) - 2)

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag

        return sum([self.fuel(int(m)) for m in s.split("\n")])
