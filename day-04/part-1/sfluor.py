from tool.runners.python import SubmissionPy


def valid(ipasswd):
    passwd = str(ipasswd)
    if ipasswd > 999_999 or ipasswd < 111_111:
        return False

    previous = passwd[0]

    double_criteria = False

    for d in passwd[1:]:
        if d < previous:
            return False

        if d == previous:
            double_criteria = True

        previous = d

    return double_criteria


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        inf, sup = [int(x) for x in s.split("-")]

        return sum([valid(x) for x in range(inf, sup + 1)])
