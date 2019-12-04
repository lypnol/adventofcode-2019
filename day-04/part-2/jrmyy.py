from tool.runners.python import SubmissionPy


class JrmyySubmission(SubmissionPy):

    def run(self, s: str) -> int:
        # :param s: input in string format
        # :return: solution flag
        lower, upper = [int(x) for x in s.split("-")]
        return sum(self.match_password(str(x)) for x in range(lower, upper + 1))

    def match_password(self, password: str) -> int:
        ints = [int(x) for x in list(password)]
        double_occurrences = [(x, ints.count(x)) for x in set(ints) if ints.count(x) == 2]
        return int(not (sorted(ints) != ints or list(set(ints)) == ints or not double_occurrences))
