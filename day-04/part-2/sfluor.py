from tool.runners.python import SubmissionPy

MAX_LEN = 6


def valid(ipasswd):
    passwd = str(ipasswd)
    if ipasswd > 999_999 or ipasswd < 111_111:
        return False

    previous = passwd[0]

    double_criteria = False

    i = 1
    while i < MAX_LEN:
        d = passwd[i]

        if d < previous:
            return False

        if d == previous and not double_criteria:
            # Not a double so let's skip theses chars
            if i + 1 < MAX_LEN and passwd[i + 1] == d:
                j = 1

                while i + j < MAX_LEN and passwd[i + j] == d:
                    j += 1

                i += j - 1
            else:
                double_criteria = True

        if i < MAX_LEN:
            previous = passwd[i]

        i += 1

    return double_criteria


class SfluorSubmission(SubmissionPy):
    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        inf, sup = [int(x) for x in s.split("-")]

        return sum([valid(x) for x in range(inf, sup + 1)])
